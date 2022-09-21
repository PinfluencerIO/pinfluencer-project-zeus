from contextlib import contextmanager
from typing import Callable

from src._types import BrandRepository, UserRepository, InfluencerRepository, Repository, CampaignRepository
from src.crosscutting import print_exception, PinfluencerObjectMapper, FlexiUpdater
from src.domain.models import Brand, Influencer, Campaign
from src.exceptions import AlreadyExistsException, NotFoundException
from src.web import PinfluencerResponse, BRAND_ID_PATH_KEY, INFLUENCER_ID_PATH_KEY, PinfluencerContext
from src.web.views import BrandRequestDto, BrandResponseDto, ImageRequestDto, InfluencerRequestDto, \
    InfluencerResponseDto, CampaignRequestDto, CampaignResponseDto


class BaseController:

    def __init__(self, repository: Repository,
                 mapper: PinfluencerObjectMapper,
                 flexi_updater: FlexiUpdater):
        self._flexi_updater = flexi_updater
        self._mapper = mapper
        self._repository = repository

    def get_all(self, context: PinfluencerContext) -> None:
        users = self._repository.load_collection()
        context.response.status_code = 200
        context.response.body = list(map(lambda x: x.__dict__, users))

    def _update_image(self,
                      context: PinfluencerContext,
                      id: str,
                      updater: Callable[[str, str], dict]) -> [PinfluencerResponse,
                                                               bool]:
        payload_dict = context.body
        try:
            user = updater(id, payload_dict['image_bytes'])
            return [PinfluencerResponse(status_code=201,
                                        body=user), False]
        except NotFoundException as e:
            print_exception(e)
            return [PinfluencerResponse(status_code=404, body={}), True]

    def update_image_field(self, context: PinfluencerContext):
        request: ImageRequestDto = self._mapper.map_from_dict(_from=context.body, to=ImageRequestDto)
        with self._unit_of_work():
            brand = self._repository.load_for_auth_user(auth_user_id=context.auth_user_id)
            setattr(brand, request.image_field, request.image_path)

    def get_by_id(self, context: PinfluencerContext) -> None:
        try:
            user = self._repository.load_by_id(id_=context.id)
            context.response.status_code = 200
            context.response.body = user.__dict__
            return
        except NotFoundException as e:
            print_exception(e)
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
        auth_user_id = context.auth_user_id
        payload_dict = context.body
        try:
            request = self._mapper.map_from_dict(_from=payload_dict,
                                                                        to=request)
            entity_in_db = self._repository.load_for_auth_user(auth_user_id=auth_user_id)
            with self._unit_of_work():
                self._flexi_updater.update(request=request,
                                           object_to_update=entity_in_db)
        except NotFoundException as e:
            print_exception(e)
            context.short_circuit = True
            context.response.body = {}
            context.response.status_code = 404
            return
        context.response.body = self._mapper.map(_from=entity_in_db, to=response).__dict__
        context.response.status_code = 200


class BaseUserController(BaseController):

    def __init__(self, user_repository: UserRepository, resource_id: str, object_mapper: PinfluencerObjectMapper,
                 flexi_updater: FlexiUpdater):
        super().__init__(user_repository, object_mapper, flexi_updater)
        self._resource_id = resource_id

    def get(self, context: PinfluencerContext) -> None:
        auth_user_id = context.auth_user_id
        if auth_user_id:
            try:
                brand = self._repository.load_for_auth_user(auth_user_id=auth_user_id)
                context.response.status_code = 200
                context.response.body = brand.__dict__
                return
            except NotFoundException as e:
                print_exception(e)
        context.short_circuit = True
        context.response.status_code = 404
        context.response.body = {}

    def _create(self, context: PinfluencerContext, model, request, response):
        auth_user_id = context.auth_user_id
        payload_dict = context.body
        try:
            entity = self._mapper.map(_from=self._mapper.map_from_dict(_from=payload_dict,
                                                                      to=request),
                                     to=model)
            with self._unit_of_work():
                entity_to_return = self._repository.write_new_for_auth_user(auth_user_id=auth_user_id, payload=entity)
        except AlreadyExistsException as e:
            print_exception(e)
            context.short_circuit = True
            context.response.body = {}
            context.response.status_code = 400
            return
        context.response.body = self._mapper.map(_from=entity_to_return, to=response).__dict__
        context.response.status_code = 201


class BrandController(BaseUserController):
    def __init__(self, brand_repository: BrandRepository, object_mapper: PinfluencerObjectMapper, flexi_updater: FlexiUpdater):
        super().__init__(brand_repository, BRAND_ID_PATH_KEY, object_mapper, flexi_updater)

    def create(self, context: PinfluencerContext) -> None:
        self._create(context=context,
                     model=Brand,
                     request=BrandRequestDto,
                     response=BrandResponseDto)

    def update(self, context: PinfluencerContext) -> None:
        self._update(context=context, request=BrandRequestDto, response=BrandResponseDto)


class InfluencerController(BaseUserController):

    def __init__(self, influencer_repository: InfluencerRepository, object_mapper: PinfluencerObjectMapper,
                 flexi_updater: FlexiUpdater):
        super().__init__(influencer_repository, INFLUENCER_ID_PATH_KEY, object_mapper, flexi_updater)

    def create(self, context: PinfluencerContext) -> None:
        self._create(context=context,
                     model=Influencer,
                     request=InfluencerRequestDto,
                     response=InfluencerResponseDto)

    def update(self, context: PinfluencerContext) -> None:
        self._update(context=context, request=InfluencerRequestDto, response=InfluencerResponseDto)


class CampaignController(BaseController):

    def __init__(self, repository: CampaignRepository, object_mapper: PinfluencerObjectMapper, flexi_updater: FlexiUpdater):
        super().__init__(repository, object_mapper, flexi_updater)

    def create(self, context: PinfluencerContext) -> None:
        try:
            campaign = self._repository.write_new_for_brand(payload=self._mapper.map(
                _from=self._mapper.map_from_dict(
                    _from=context.body,
                    to=CampaignRequestDto),
                to=Campaign),
                auth_user_id=context.auth_user_id)
            context.response.body = campaign.__dict__
            context.response.status_code = 201
            return
        except NotFoundException as e:
            print_exception(e)
            context.response.body = {}
            context.response.status_code = 404
            context.short_circuit = True

    def get_for_brand(self, context: PinfluencerContext) -> None:
        try:
            campaigns = self._repository.load_for_auth_brand(auth_user_id=context.auth_user_id)
            context.response.status_code = 200
            context.response.body = list(map(lambda x: x.__dict__, campaigns))
        except NotFoundException as e:
            print_exception(e)
            context.response.status_code = 404
            context.response.body = {}
            context.short_circuit = True

    def update(self, context: PinfluencerContext) -> None:
        self._update(context=context, request=CampaignRequestDto, response=CampaignResponseDto)
