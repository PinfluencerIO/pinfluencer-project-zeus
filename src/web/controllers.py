from contextlib import contextmanager
from typing import Callable, Any

from src._types import BrandRepository, UserRepository, InfluencerRepository, Repository, CampaignRepository, Logger, \
    Model, NotificationRepository, AudienceAgeRepository
from src.crosscutting import PinfluencerObjectMapper, FlexiUpdater
from src.domain.models import Brand, Influencer, Campaign, Notification, AudienceAgeSplit
from src.exceptions import AlreadyExistsException, NotFoundException
from src.web import BRAND_ID_PATH_KEY, INFLUENCER_ID_PATH_KEY, PinfluencerContext
from src.web.views import BrandRequestDto, BrandResponseDto, ImageRequestDto, InfluencerRequestDto, \
    InfluencerResponseDto, CampaignRequestDto, CampaignResponseDto, NotificationCreateRequestDto, \
    NotificationResponseDto, AudienceAgeViewDto


class BaseController:

    def __init__(self, repository: Repository,
                 mapper: PinfluencerObjectMapper,
                 flexi_updater: FlexiUpdater,
                 logger: Logger,
                 response,
                 request):
        self._request = request
        self._response = response
        self._logger = logger
        self._flexi_updater = flexi_updater
        self._mapper = mapper
        self._repository = repository

    def _get_all(self, context: PinfluencerContext, response) -> None:
        users = self._repository.load_collection()
        context.response.status_code = 200
        context.response.body = list(map(lambda x: self._mapper.map(_from=x, to=response).__dict__, users))

    def get_all(self, context: PinfluencerContext) -> None:
        self._get_all(context=context, response=self._response)

    def _generic_update_image_field(self, context: PinfluencerContext, response, repo_func: Callable[[], Model]):
        request: ImageRequestDto = self._mapper.map_from_dict(_from=context.body, to=ImageRequestDto)
        with self._unit_of_work():
            try:
                brand = repo_func()
                setattr(brand, request.image_field, request.image_path)
                context.response.body = self._mapper.map(_from=brand, to=response).__dict__
            except NotFoundException as e:
                self._logger.log_error(str(e))
                context.short_circuit = True
                context.response.body = {}
                context.response.status_code = 404

    def _update_image_field(self, context: PinfluencerContext, response):
        self._generic_update_image_field(context=context,
                                         response=response,
                                         repo_func=lambda: self._repository.load_for_auth_user(
                                             auth_user_id=context.auth_user_id
                                         ))

    def get_by_id(self, context: PinfluencerContext) -> None:
        self._get_by_id(context=context, response=self._response)

    def _get_by_id(self, context: PinfluencerContext, response) -> None:
        try:
            user = self._repository.load_by_id(id_=context.id)
            context.response.status_code = 200
            context.response.body = self._mapper.map(_from=user, to=response).__dict__
            return
        except NotFoundException as e:
            self._logger.log_exception(e)
            context.short_circuit = True
            context.response.status_code = 404
            context.response.body = {}

    @contextmanager
    def _unit_of_work(self):
        try:
            yield
            self._repository.save()
        except Exception:
            raise

    def _update(self, context: PinfluencerContext, request, response):
        self._generic_update(context=context,
                             request=request,
                             response=response,
                             repo_func=lambda: self._repository.load_for_auth_user(
                                 auth_user_id=context.auth_user_id)
                             )

    def _generic_update(self, context: PinfluencerContext, request, response, repo_func: Callable[[], Model]):
        payload_dict = context.body
        with self._unit_of_work():
            try:
                request = self._mapper.map_from_dict(_from=payload_dict,
                                                     to=request)
                entity_in_db = repo_func()
                self._flexi_updater.update(request=request,
                                           object_to_update=entity_in_db)
            except NotFoundException as e:
                self._logger.log_exception(e)
                context.short_circuit = True
                context.response.body = {}
                context.response.status_code = 404
                return
            mapped_response = self._mapper.map(_from=entity_in_db, to=response)
            context.response.body = mapped_response.__dict__
            context.response.status_code = 200

    def _create(self,
                context: PinfluencerContext,
                model,
                request,
                response):
        auth_user_id = context.auth_user_id
        payload_dict = context.body
        with self._unit_of_work():
            try:
                entity = self._mapper.map(_from=self._mapper.map_from_dict(_from=payload_dict,
                                                                           to=request),
                                          to=model)

                entity_to_return = self._repository.write_new_for_auth_user(auth_user_id=auth_user_id, payload=entity)
            except AlreadyExistsException as e:
                self._logger.log_exception(e)
                context.short_circuit = True
                context.response.body = {}
                context.response.status_code = 400
                return
            self._logger.log_trace(f"entity to return {entity_to_return}")
            self._logger.log_trace(f"mapping {model.__name__} to {response.__name__}")
            response = self._mapper.map(_from=entity_to_return, to=response)
            self._logger.log_trace(f"mapped response: {response}")
            context.response.body = response.__dict__
            context.response.status_code = 201


class BaseOwnerController(BaseController):

    def __init__(self, user_repository: Repository,
                 object_mapper: PinfluencerObjectMapper,
                 flexi_updater: FlexiUpdater,
                 logger: Logger,
                 response,
                 request):
        super().__init__(user_repository,
                         object_mapper,
                         flexi_updater,
                         logger=logger,
                         response=response,
                         request=request)

    def _create_for_owner(self,
                          context: PinfluencerContext,
                          repo_method: Callable[[Any, str], Any],
                          request,
                          response,
                          model) -> None:
        with self._unit_of_work():
            try:

                returned_model = repo_method(self._mapper.map(
                    _from=self._mapper.map_from_dict(
                        _from=context.body,
                        to=request),
                    to=model),
                    context.auth_user_id)
                self._logger.log_trace(f"{returned_model}")
                self._logger.log_trace(f"{returned_model.__dict__}")
                context.response.body = self._mapper.map(_from=returned_model, to=response).__dict__
                context.response.status_code = 201
                return
            except NotFoundException as e:
                self._logger.log_exception(e)
                context.response.body = {}
                context.response.status_code = 404
                context.short_circuit = True

    def _get_for_owner(self,
                       context: PinfluencerContext,
                       repo_method: Callable[[str], Any],
                       response) -> None:
        try:
            children = repo_method(context.auth_user_id)
            context.response.status_code = 200
            context.response.body = list(
                map(lambda x: self._mapper.map(_from=x, to=response).__dict__, children))
        except NotFoundException as e:
            self._logger.log_exception(e)
            context.response.status_code = 404
            context.response.body = {}
            context.short_circuit = True

class BaseUserController(BaseController):

    def __init__(self, user_repository: UserRepository, resource_id: str, object_mapper: PinfluencerObjectMapper,
                 flexi_updater: FlexiUpdater,
                 logger: Logger,
                 response,
                 request,
                 model):
        super().__init__(user_repository, object_mapper, flexi_updater, logger=logger, response=response,
                         request=request)
        self._model = model
        self._resource_id = resource_id

    def _get(self, context: PinfluencerContext, response) -> None:
        auth_user_id = context.auth_user_id
        if auth_user_id:
            try:
                brand = self._repository.load_for_auth_user(auth_user_id=auth_user_id)
                context.response.status_code = 200
                context.response.body = self._mapper.map(_from=brand, to=response).__dict__
                return
            except NotFoundException as e:
                self._logger.log_exception(e)
        context.short_circuit = True
        context.response.status_code = 404
        context.response.body = {}

    def get(self, context: PinfluencerContext) -> None:
        self._get(context=context, response=self._response)

    def create(self, context: PinfluencerContext) -> None:
        self._create(context=context,
                     model=self._model,
                     request=self._request,
                     response=self._response)

    def update_for_user(self, context: PinfluencerContext) -> None:
        self._update(context=context, request=self._request, response=self._response)

    def update_image_field_for_user(self, context: PinfluencerContext):
        self._update_image_field(context=context, response=self._response)


class BrandController(BaseUserController):
    def __init__(self, brand_repository: BrandRepository, object_mapper: PinfluencerObjectMapper,
                 flexi_updater: FlexiUpdater, logger: Logger):
        super().__init__(brand_repository, BRAND_ID_PATH_KEY, object_mapper, flexi_updater, logger,
                         response=BrandResponseDto,
                         request=BrandRequestDto,
                         model=Brand)


class InfluencerController(BaseUserController):

    def __init__(self, influencer_repository: InfluencerRepository, object_mapper: PinfluencerObjectMapper,
                 flexi_updater: FlexiUpdater, logger: Logger):
        super().__init__(influencer_repository, INFLUENCER_ID_PATH_KEY, object_mapper, flexi_updater, logger,
                         response=InfluencerResponseDto,
                         request=InfluencerRequestDto,
                         model=Influencer)


class AudienceAgeController(BaseOwnerController):

    def __init__(self, repository: AudienceAgeRepository,
                 mapper: PinfluencerObjectMapper,
                 flexi_updater: FlexiUpdater,
                 logger: Logger):
        super().__init__(repository,
                         mapper,
                         flexi_updater,
                         logger,
                         AudienceAgeViewDto,
                         AudienceAgeViewDto)

    def create_for_influencer(self, context: PinfluencerContext):
        self._create_for_owner(context=context,
                               repo_method=self._repository.write_new_for_influencer,
                               request=AudienceAgeViewDto,
                               response=AudienceAgeViewDto,
                               model=AudienceAgeSplit)

    def get_for_influencer(self, context: PinfluencerContext):
        self._get_for_owner(context=context,
                            repo_method=self._repository.load_for_influencer,
                            response=AudienceAgeViewDto)


class CampaignController(BaseOwnerController):

    def __init__(self, repository: CampaignRepository, object_mapper: PinfluencerObjectMapper,
                 flexi_updater: FlexiUpdater, logger: Logger):
        super().__init__(repository, object_mapper, flexi_updater, logger,
                         response=CampaignResponseDto,
                         request=CampaignRequestDto)

    def create_for_brand(self, context: PinfluencerContext) -> None:
        self._create_for_owner(context=context,
                               repo_method=self._repository.write_new_for_brand,
                               request=CampaignRequestDto,
                               response=CampaignResponseDto,
                               model=Campaign)

    def get_for_brand(self, context: PinfluencerContext) -> None:
        self._get_for_owner(context=context,
                            repo_method=self._repository.load_for_auth_brand,
                            response=CampaignResponseDto)

    def update_campaign(self, context: PinfluencerContext):
        self._generic_update(context=context,
                             request=CampaignRequestDto,
                             response=CampaignResponseDto,
                             repo_func=lambda: self._repository.load_by_id(id_=context.id))

    def update_campaign_image(self, context: PinfluencerContext):
        self._generic_update_image_field(context=context,
                                         response=CampaignResponseDto,
                                         repo_func=lambda: self._repository.load_by_id(id_=context.id))



class NotificationController(BaseController):

    def __init__(self, repository: NotificationRepository,
                 mapper: PinfluencerObjectMapper,
                 flexi_updater: FlexiUpdater,
                 logger: Logger):
        super().__init__(repository,
                         mapper,
                         flexi_updater,
                         logger,
                         NotificationCreateRequestDto,
                         NotificationResponseDto)

    def create(self, context: PinfluencerContext):
        self._create(context=context,
                     model=Notification,
                     request=NotificationCreateRequestDto,
                     response=NotificationResponseDto)
