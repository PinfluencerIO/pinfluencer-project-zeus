from typing import Callable

from src._types import BrandRepository, UserRepository, InfluencerRepository, Repository, CampaignRepository
from src.crosscutting import print_exception
from src.domain.models import ValueEnum, CategoryEnum, Brand, Influencer, Campaign, CampaignStateEnum
from src.exceptions import AlreadyExistsException, NotFoundException
from src.web import PinfluencerResponse, BRAND_ID_PATH_KEY, INFLUENCER_ID_PATH_KEY, PinfluencerContext


class BaseController:

    def __init__(self, repository: Repository):
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


class BaseUserController(BaseController):

    def __init__(self, user_repository: UserRepository, resource_id: str):
        super().__init__(user_repository)
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


class BrandController(BaseUserController):
    def __init__(self, brand_repository: BrandRepository):
        super().__init__(brand_repository, BRAND_ID_PATH_KEY)

    def create(self, context: PinfluencerContext) -> None:
        auth_user_id = context.auth_user_id
        payload_dict = context.body
        try:
            brand = Brand(brand_name=payload_dict["brand_name"],
                          brand_description=payload_dict["brand_description"],
                          website=payload_dict["website"],
                          insta_handle=payload_dict["insta_handle"],
                          values=list(map(lambda x: ValueEnum[x], payload_dict["values"])),
                          categories=list(map(lambda x: CategoryEnum[x], payload_dict["categories"])))
            self._repository.write_new_for_auth_user(auth_user_id=auth_user_id, payload=brand)
        except (AlreadyExistsException) as e:
            print_exception(e)
            context.short_circuit = True
            context.response.body = {}
            context.response.status_code = 400
            return
        context.response.body = brand.__dict__
        context.response.status_code = 201

    def update(self, context: PinfluencerContext) -> None:
        auth_user_id = context.auth_user_id
        payload_dict = context.body
        try:
            brand = Brand(brand_name=payload_dict["brand_name"],
                          brand_description=payload_dict["brand_description"],
                          website=payload_dict["website"],
                          insta_handle=payload_dict["insta_handle"],
                          values=list(map(lambda x: ValueEnum[x], payload_dict["values"])),
                          categories=list(map(lambda x: CategoryEnum[x], payload_dict["categories"])))
            brand_to_return = self._repository.update_for_auth_user(auth_user_id=auth_user_id, payload=brand)
            context.response.body = brand_to_return.__dict__
            context.response.status_code = 200
            return
        except NotFoundException as e:
            print_exception(e)
            context.short_circuit = True
            context.response.body = {}
            context.response.status_code = 404

    def update_logo(self, context: PinfluencerContext) -> None:
        [response, short_circuit] = self._update_image(context=context,
                                                       updater=lambda auth_id,
                                                                      bytes: self._repository.update_logo_for_auth_user(
                                                           auth_id,
                                                           bytes).__dict__,
                                                       id=context.auth_user_id)
        context.short_circuit = short_circuit
        context.response.body = response.body
        context.response.status_code = response.status_code

    def update_header_image(self, context: PinfluencerContext) -> None:
        [response, short_circuit] = self._update_image(context=context,
                                                       updater=lambda auth_id,
                                                                      bytes: self._repository.update_header_image_for_auth_user(
                                                           auth_id,
                                                           bytes).__dict__,
                                                       id=context.auth_user_id)
        context.short_circuit = short_circuit
        context.response.status_code = response.status_code
        context.response.body = response.body


class InfluencerController(BaseUserController):

    def __init__(self, influencer_repository: InfluencerRepository):
        super().__init__(influencer_repository, INFLUENCER_ID_PATH_KEY)

    def create(self, context: PinfluencerContext) -> None:
        auth_user_id = context.auth_user_id
        payload_dict = context.body
        try:
            influencer = Influencer(first_name=payload_dict["first_name"],
                                    last_name=payload_dict["last_name"],
                                    email=payload_dict["email"],
                                    bio=payload_dict["bio"],
                                    website=payload_dict["website"],
                                    insta_handle=payload_dict["insta_handle"],
                                    values=list(map(lambda x: ValueEnum[x], payload_dict["values"])),
                                    categories=list(map(lambda x: CategoryEnum[x], payload_dict["categories"])),
                                    auth_user_id=auth_user_id,
                                    audience_male_split=payload_dict["audience_male_split"],
                                    audience_female_split=payload_dict["audience_female_split"],
                                    audience_age_13_to_17_split=payload_dict["audience_age_13_to_17_split"],
                                    audience_age_18_to_24_split=payload_dict["audience_age_18_to_24_split"],
                                    audience_age_25_to_34_split=payload_dict["audience_age_25_to_34_split"],
                                    audience_age_35_to_44_split=payload_dict["audience_age_35_to_44_split"],
                                    audience_age_45_to_54_split=payload_dict["audience_age_45_to_54_split"],
                                    audience_age_55_to_64_split=payload_dict["audience_age_55_to_64_split"],
                                    audience_age_65_plus_split=payload_dict["audience_age_65_plus_split"],
                                    address=payload_dict["address"])
            self._repository.write_new_for_auth_user(auth_user_id=auth_user_id, payload=influencer)
        except (AlreadyExistsException) as e:
            print_exception(e)
            context.short_circuit = True
            context.response.body = {}
            context.response.status_code = 400
            return
        context.response.body = influencer.__dict__
        context.response.status_code = 201

    def update_profile_image(self, context: PinfluencerContext) -> None:
        [response, short_circuit] = self._update_image(context=context,
                                                       updater=lambda auth_id,
                                                                      bytes: self._repository.update_image_for_auth_user(
                                                           auth_id,
                                                           bytes).__dict__,
                                                       id=context.auth_user_id)
        context.short_circuit = short_circuit
        context.response.status_code = response.status_code
        context.response.body = response.body

    def update(self, context: PinfluencerContext) -> None:
        auth_user_id = context.auth_user_id
        payload_dict = context.body
        try:
            influencer_from_db = self._repository.update_for_auth_user(auth_user_id=auth_user_id,
                                                                       payload=Influencer(
                                                                           auth_user_id=auth_user_id,
                                                                           insta_handle=payload_dict[
                                                                               'insta_handle'],
                                                                           website=payload_dict["website"],
                                                                           bio=payload_dict["bio"],
                                                                           audience_male_split=payload_dict[
                                                                               "audience_male_split"],
                                                                           audience_female_split=payload_dict[
                                                                               "audience_female_split"],
                                                                           audience_age_13_to_17_split=
                                                                           payload_dict[
                                                                               "audience_age_13_to_17_split"],
                                                                           audience_age_18_to_24_split=
                                                                           payload_dict[
                                                                               "audience_age_18_to_24_split"],
                                                                           audience_age_25_to_34_split=
                                                                           payload_dict[
                                                                               "audience_age_25_to_34_split"],
                                                                           audience_age_35_to_44_split=
                                                                           payload_dict[
                                                                               "audience_age_35_to_44_split"],
                                                                           audience_age_45_to_54_split=
                                                                           payload_dict[
                                                                               "audience_age_45_to_54_split"],
                                                                           audience_age_55_to_64_split=
                                                                           payload_dict[
                                                                               "audience_age_55_to_64_split"],
                                                                           audience_age_65_plus_split=payload_dict[
                                                                               "audience_age_65_plus_split"],
                                                                           values=list(map(lambda x: ValueEnum[x],
                                                                                           payload_dict[
                                                                                               "values"])),
                                                                           categories=list(
                                                                               map(lambda x: CategoryEnum[x],
                                                                                   payload_dict["categories"])),
                                                                           address=payload_dict["address"]
                                                                       ))
            context.response.status_code = 200
            context.response.body = influencer_from_db.__dict__
            return
        except NotFoundException as e:
            print_exception(e)
            context.short_circuit = True
            context.response.status_code = 404
            context.response.body = {}


class CampaignController(BaseController):

    def __init__(self, repository: CampaignRepository):
        super().__init__(repository)

    def create(self, context: PinfluencerContext) -> None:
        try:
            campaign = self._repository.write_new_for_brand(payload=Campaign(
                objective=context.body["objective"],
                success_description=context.body["success_description"],
                campaign_title=context.body["campaign_title"],
                campaign_description=context.body["campaign_description"],
                campaign_categories=list(map(lambda x: CategoryEnum[x], context.body["campaign_categories"])),
                campaign_values=list(map(lambda x: ValueEnum[x], context.body["campaign_values"])),
                campaign_product_link=context.body["campaign_product_link"],
                campaign_hashtag=context.body["campaign_hashtag"],
                campaign_discount_code=context.body["campaign_discount_code"],
                product_title=context.body["product_title"],
                product_description=context.body["product_description"]
            ), auth_user_id=context.auth_user_id)
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
        try:
            campaign = self._repository.update_campaign(_id=context.id, payload=Campaign(
                objective=context.body["objective"],
                success_description=context.body["success_description"],
                campaign_title=context.body["campaign_title"],
                campaign_description=context.body["campaign_description"],
                campaign_categories=list(map(lambda x: CategoryEnum[x], context.body["campaign_categories"])),
                campaign_values=list(map(lambda x: ValueEnum[x], context.body["campaign_values"])),
                campaign_product_link=context.body["campaign_product_link"],
                campaign_hashtag=context.body["campaign_hashtag"],
                campaign_discount_code=context.body["campaign_discount_code"],
                product_title=context.body["product_title"],
                product_description=context.body["product_description"]
            ))
            context.response.body = campaign.__dict__
            context.response.status_code = 200
        except NotFoundException as e:
            print_exception(e)
            context.response.body = {}
            context.response.status_code = 404
            context.short_circuit = True

    def update_campaign_state(self, context: PinfluencerContext) -> None:
        try:
            campaign = self\
                ._repository\
                .update_campaign_state(_id=context.id,
                                       payload=CampaignStateEnum[context.body["campaign_state"]])
            context.response.body = campaign.__dict__
            context.response.status_code = 200
        except NotFoundException as e:
            print_exception(e)
            context.response.body = {}
            context.response.status_code = 404
            context.short_circuit = True


    def update_product_image1(self, context: PinfluencerContext) -> None:
        [response, short_circuit] = self._update_image(context=context,
                                                       updater=self.product_image1_updater,
                                                       id=context.id)
        context.short_circuit = short_circuit
        context.response.status_code = response.status_code
        context.response.body = response.body

    def product_image1_updater(self, id: str, bytes: str) -> dict:
        return self._repository.update_product_image1(id=id, image_bytes=bytes).__dict__

    def update_product_image2(self, context: PinfluencerContext) -> None:
        [response, short_circuit] = self._update_image(context=context,
                                                       updater=self.product_image2_updater,
                                                       id=context.id)
        context.short_circuit = short_circuit
        context.response.status_code = response.status_code
        context.response.body = response.body

    def product_image2_updater(self, id: str, bytes: str) -> dict:
        return self._repository.update_product_image2(id=id, image_bytes=bytes).__dict__

    def update_product_image3(self, context: PinfluencerContext) -> None:
        [response, short_circuit] = self._update_image(context=context,
                                                       updater=self.product_image3_updater,
                                                       id=context.id)
        context.short_circuit = short_circuit
        context.response.status_code = response.status_code
        context.response.body = response.body

    def product_image3_updater(self, id: str, bytes: str) -> dict:
        return self._repository.update_product_image3(id=id, image_bytes=bytes).__dict__
