import uuid
from unittest import TestCase
from unittest.mock import Mock, MagicMock

from callee import Captor

from src.crosscutting import valid_uuid
from src.domain.models import Influencer, Campaign, CategoryEnum, ValueEnum, CampaignStateEnum
from src.exceptions import AlreadyExistsException, NotFoundException
from src.types import BrandRepository, InfluencerRepository, CampaignRepository
from src.web import PinfluencerContext, PinfluencerResponse
from src.web.controllers import BrandController, InfluencerController, CampaignController
from tests import brand_dto_generator, assert_brand_updatable_fields_are_equal, influencer_dto_generator, RepoEnum, \
    assert_brand_creatable_generated_fields_are_equal, assert_influencer_creatable_generated_fields_are_equal, \
    assert_influencer_update_fields_are_equal, \
    update_brand_payload, create_brand_dto, \
    update_image_payload, update_brand_return_dto, create_influencer_dto, \
    update_influencer_payload, campaign_dto_generator


class TestInfluencerController(TestCase):

    def setUp(self):
        self.__influencer_repository: InfluencerRepository = Mock()
        self.__sut = InfluencerController(influencer_repository=self.__influencer_repository)

    def test_get_by_id(self):
        # arrange
        influencer_in_db = influencer_dto_generator(num=1, repo=RepoEnum.STD_REPO)
        self.__influencer_repository.load_by_id = MagicMock(return_value=influencer_in_db)
        pinfluencer_response = PinfluencerResponse()

        # act
        self.__sut.get_by_id(PinfluencerContext(response=pinfluencer_response,
                                                id=influencer_in_db.id))

        # assert
        assert pinfluencer_response.body == influencer_in_db.__dict__

    def test_get(self):
        # arrange
        db_influencer = influencer_dto_generator(num=1, repo=RepoEnum.STD_REPO)
        self.__influencer_repository.load_for_auth_user = MagicMock(return_value=db_influencer)
        auth_id = "12341"
        response = PinfluencerResponse()

        # act
        self.__sut.get(PinfluencerContext(response=response,
                                          auth_user_id=auth_id))

        # assert
        assert response.body == db_influencer.__dict__
        assert response.status_code == 200

    def test_get_all(self):
        # arrange
        influencers_from_db = [
            influencer_dto_generator(num=1, repo=RepoEnum.STD_REPO),
            influencer_dto_generator(num=2, repo=RepoEnum.STD_REPO),
            influencer_dto_generator(num=3, repo=RepoEnum.STD_REPO),
            influencer_dto_generator(num=4, repo=RepoEnum.STD_REPO)
        ]
        self.__influencer_repository.load_collection = MagicMock(return_value=influencers_from_db)
        pinfluencer_response = PinfluencerResponse()

        # act
        self.__sut.get_all(PinfluencerContext(response=pinfluencer_response,
                                              event={}))

        # assert
        assert pinfluencer_response.body == list(map(lambda x: x.__dict__, influencers_from_db))
        assert pinfluencer_response.status_code == 200

    def test_create(self):
        # arrange
        influencer_db = create_influencer_dto()
        expected_payload = update_influencer_payload()
        auth_id = "1234"
        self.__influencer_repository.write_new_for_auth_user = MagicMock(return_value=influencer_db)
        response = PinfluencerResponse()

        # act
        self.__sut.create(PinfluencerContext(response=response,
                                             body=expected_payload,
                                             auth_user_id=auth_id))

        # assert
        payload_captor = Captor()
        self.__influencer_repository.write_new_for_auth_user.assert_called_once_with(auth_user_id=auth_id,
                                                                                     payload=payload_captor)
        actual_payload: Influencer = payload_captor.arg
        assert valid_uuid(actual_payload.id)
        assert actual_payload.image is None
        assert_influencer_creatable_generated_fields_are_equal(expected_payload, actual_payload.__dict__)
        assert response.status_code == 201
        assert response.body == actual_payload.__dict__
        print(response.body)

    def test_create_when_exists(self):
        # arrange
        auth_id = "12341"
        payload = update_influencer_payload()
        self.__influencer_repository.write_new_for_auth_user = MagicMock(side_effect=AlreadyExistsException())
        response = PinfluencerResponse()

        # act
        context = PinfluencerContext(body=payload, auth_user_id=auth_id, response=response)
        self.__sut.create(context)

        # assert
        assert response.status_code == 400
        assert response.body == {}
        assert context.short_circuit == True

    def test_update_profile_image(self):
        # arrange
        auth_id = "12341"
        payload = update_image_payload()
        expected_influencer = influencer_dto_generator(num=1)
        self.__influencer_repository.update_image_for_auth_user = MagicMock(return_value=expected_influencer)
        response = PinfluencerResponse()

        # act
        self.__sut.update_profile_image(PinfluencerContext(body=payload,
                                                           auth_user_id=auth_id,
                                                           response=response))

        # assert
        assert response.status_code == 201
        assert response.body == expected_influencer.__dict__

    def test_update(self):
        # arrange
        influencer_in_db = create_influencer_dto()
        self.__influencer_repository.update_for_auth_user = MagicMock(return_value=influencer_in_db)
        auth_id = "12341"
        response = PinfluencerResponse()

        # act
        self.__sut.update(PinfluencerContext(
            auth_user_id=auth_id, body=update_influencer_payload(),
            response=response))

        # assert
        arg_captor = Captor()
        self.__influencer_repository.update_for_auth_user.assert_called_once_with(auth_user_id=auth_id,
                                                                                  payload=arg_captor)
        update_for_auth_user_repo_payload: Influencer = arg_captor.arg
        assert_influencer_update_fields_are_equal(influencer1=update_influencer_payload(),
                                                  influencer2=update_for_auth_user_repo_payload.__dict__)
        assert list(map(lambda x: x.name, update_for_auth_user_repo_payload.values)) == update_influencer_payload()[
            "values"]
        assert list(map(lambda x: x.name, update_for_auth_user_repo_payload.categories)) == update_influencer_payload()[
            "categories"]
        assert response.body == influencer_in_db.__dict__
        assert response.status_code == 200

    def test_update_when_not_found(self):
        # arrange
        self.__influencer_repository.update_for_auth_user = MagicMock(
            side_effect=NotFoundException("influencer not found"))
        return_value = PinfluencerResponse()

        # act
        context = PinfluencerContext(
            auth_user_id="12341", body=update_influencer_payload(),
            response=return_value)
        self.__sut.update(context)

        # assert
        assert return_value.body == {}
        assert return_value.status_code == 404
        assert context.short_circuit == True


class TestBrandController(TestCase):

    def setUp(self):
        self.__brand_repository: BrandRepository = Mock()
        self.__sut = BrandController(brand_repository=self.__brand_repository)

    def test_get_by_id(self):
        # arrange
        brand_from_db = brand_dto_generator(num=1, repo=RepoEnum.STD_REPO)
        self.__brand_repository.load_by_id = MagicMock(return_value=brand_from_db)
        pinfluencer_response = PinfluencerResponse()

        # act
        self.__sut.get_by_id(PinfluencerContext(id=brand_from_db.id,
                                                response=pinfluencer_response))

        # assert
        self.__brand_repository.load_by_id.assert_called_once_with(id_=brand_from_db.id)
        assert pinfluencer_response.body == brand_from_db.__dict__
        assert pinfluencer_response.is_ok() is True

    def test_get_by_id_when_not_found(self):
        # arrange
        self.__brand_repository.load_by_id = MagicMock(side_effect=NotFoundException())
        field = str(uuid.uuid4())
        pinfluencer_response = PinfluencerResponse()

        # act
        context = PinfluencerContext(id=field, response=pinfluencer_response)
        self.__sut.get_by_id(context)

        # assert
        self.__brand_repository.load_by_id.assert_called_once_with(id_=field)
        assert pinfluencer_response.body == {}
        assert pinfluencer_response.status_code == 404
        assert context.short_circuit == True

    def test_get_all(self):
        # arrange
        brands_from_db = [
            brand_dto_generator(num=1, repo=RepoEnum.STD_REPO),
            brand_dto_generator(num=2, repo=RepoEnum.STD_REPO),
            brand_dto_generator(num=3, repo=RepoEnum.STD_REPO),
            brand_dto_generator(num=4, repo=RepoEnum.STD_REPO)
        ]
        self.__brand_repository.load_collection = MagicMock(return_value=brands_from_db)
        pinfluencer_response = PinfluencerResponse()

        # act
        self.__sut.get_all(PinfluencerContext(event={},
                                              response=pinfluencer_response))

        # assert
        self.__brand_repository.load_collection.assert_called_once()
        assert pinfluencer_response.body == list(map(lambda x: x.__dict__, brands_from_db))
        assert pinfluencer_response.status_code == 200

    def test_get(self):
        # arrange
        db_brand = brand_dto_generator(num=1, repo=RepoEnum.STD_REPO)
        self.__brand_repository.load_for_auth_user = MagicMock(return_value=db_brand)
        auth_id = "12341"
        response = PinfluencerResponse()

        # act
        self.__sut.get(PinfluencerContext(auth_user_id=auth_id,
                                          response=response))

        # assert
        self.__brand_repository.load_for_auth_user.assert_called_once_with(auth_user_id=auth_id)
        assert response.body == db_brand.__dict__
        assert response.status_code == 200

    def test_get_when_not_found(self):
        # arrange
        self.__brand_repository.load_for_auth_user = MagicMock(side_effect=NotFoundException())
        auth_id = "12341"
        response = PinfluencerResponse()

        # act
        context = PinfluencerContext(auth_user_id=auth_id, response=response)
        self.__sut.get(context)

        # assert
        self.__brand_repository.load_for_auth_user.assert_called_once_with(auth_user_id=auth_id)
        assert response.body == {}
        assert response.status_code == 404
        assert context.short_circuit == True

    def test_create(self):
        # arrange
        brand_db = create_brand_dto()
        expected_payload = update_brand_payload()
        auth_id = "12341"
        self.__brand_repository.write_new_for_auth_user = MagicMock(return_value=brand_db)
        response = PinfluencerResponse()

        # act
        self.__sut.create(PinfluencerContext(body=expected_payload,
                                             auth_user_id=auth_id,
                                             response=response))

        # assert
        payload_captor = Captor()
        self.__brand_repository.write_new_for_auth_user.assert_called_once_with(auth_user_id=auth_id,
                                                                                payload=payload_captor)
        actual_payload = payload_captor.arg
        assert valid_uuid(actual_payload.id)
        assert actual_payload.logo is None
        assert actual_payload.header_image is None
        assert_brand_creatable_generated_fields_are_equal(expected_payload, actual_payload.__dict__)
        assert response.status_code == 201
        assert response.body == actual_payload.__dict__
        print(response.body)

    def test_create_when_exists(self):
        # arrange
        auth_id = "12341"
        self.__brand_repository.write_new_for_auth_user = MagicMock(side_effect=AlreadyExistsException())
        response = PinfluencerResponse()
        brand = update_brand_payload()

        # act
        context = PinfluencerContext(auth_user_id=auth_id, response=response, body=brand)
        self.__sut.create(context)

        # assert
        assert response.status_code == 400
        assert response.body == {}
        assert context.short_circuit == True

    def test_update(self):
        # arrange
        expected_payload = update_brand_payload()
        brand_in_db = update_brand_return_dto()
        auth_id = "12341"
        self.__brand_repository.update_for_auth_user = MagicMock(return_value=brand_in_db)
        response = PinfluencerResponse()

        # act
        self.__sut.update(PinfluencerContext(body=expected_payload,
                                             auth_user_id=auth_id,
                                             response=response))

        # assert
        payload_captor = Captor()
        self.__brand_repository.update_for_auth_user.assert_called_once_with(auth_user_id=auth_id,
                                                                             payload=payload_captor)
        actual_payload = payload_captor.arg
        assert valid_uuid(actual_payload.id)
        assert_brand_updatable_fields_are_equal(actual_payload.__dict__, expected_payload)
        assert list(map(lambda x: x.name, actual_payload.values)) == expected_payload['values']
        assert list(map(lambda x: x.name, actual_payload.categories)) == expected_payload['categories']
        assert response.status_code == 200
        assert response.body == brand_in_db.__dict__

    def test_update_when_not_found(self):
        # arrange
        auth_id = "12341"
        payload = update_brand_payload()
        self.__brand_repository.update_for_auth_user = MagicMock(side_effect=NotFoundException())
        response = PinfluencerResponse()

        # act
        context = PinfluencerContext(body=payload, auth_user_id=auth_id, response=response)
        self.__sut.update(context)

        # assert
        assert response.status_code == 404
        assert response.body == {}
        assert context.short_circuit == True

    def test_update_logo(self):
        # arrange
        auth_id = "12341"
        payload = update_image_payload()
        expected_brand = brand_dto_generator(num=1)
        self.__brand_repository.update_logo_for_auth_user = MagicMock(return_value=expected_brand)
        response = PinfluencerResponse()

        # act
        self.__sut.update_logo(PinfluencerContext(auth_user_id=auth_id,
                                                  body=payload,
                                                  response=response))

        # assert
        assert response.status_code == 201
        assert response.body == expected_brand.__dict__

    def test_update_logo_when_not_found(self):
        # arrange
        auth_id = "12341"
        payload = update_image_payload()
        self.__brand_repository.update_logo_for_auth_user = MagicMock(side_effect=NotFoundException())
        response = PinfluencerResponse()

        # act
        context = PinfluencerContext(body=payload, auth_user_id=auth_id, response=response)
        self.__sut.update_logo(context)

        # assert
        assert response.status_code == 404
        assert response.body == {}
        assert context.short_circuit == True

    def test_update_header_image(self):
        # arrange
        auth_id = "12341"
        payload = update_image_payload()
        expected_brand = brand_dto_generator(num=1)
        self.__brand_repository.update_header_image_for_auth_user = MagicMock(return_value=expected_brand)
        response = PinfluencerResponse()

        # act
        self.__sut.update_header_image(PinfluencerContext(body=payload,
                                                          auth_user_id=auth_id,
                                                          response=response))

        # assert
        assert response.status_code == 201
        assert response.body == expected_brand.__dict__

    def test_update_header_image_when_not_found(self):
        # arrange
        auth_id = "12341"
        payload = update_image_payload()
        self.__brand_repository.update_header_image_for_auth_user = MagicMock(side_effect=NotFoundException())
        response = PinfluencerResponse()

        # act
        context = PinfluencerContext(body=payload, auth_user_id=auth_id, response=response)
        self.__sut.update_header_image(context)

        # assert
        assert response.status_code == 404
        assert response.body == {}
        assert context.short_circuit == True


def create_campaign_from_db() -> Campaign:
    return Campaign(objective="objective1",
                    success_description="success_description1",
                    campaign_title="campaign_title1",
                    campaign_description="campaign_description1",
                    campaign_categories=[CategoryEnum.CATEGORY6, CategoryEnum.CATEGORY5, CategoryEnum.CATEGORY7],
                    campaign_values=[ValueEnum.VALUE5, ValueEnum.VALUE6, ValueEnum.VALUE7],
                    campaign_product_link="campaign_product_link1",
                    campaign_hashtag="campaign_hashtag1",
                    campaign_discount_code="campaign_discount_code1",
                    product_title="product_title1",
                    product_description="product_description1",
                    )


def create_or_update_campaign_body() -> dict:
    return {
        "objective": "objective1",
        "success_description": "success_description1",
        "campaign_title": "campaign_title1",
        "campaign_description": "campaign_description1",
        "campaign_categories": ["CATEGORY6", "CATEGORY5", "CATEGORY7"],
        "campaign_values": ["VALUE5", "VALUE6", "VALUE7"],
        "campaign_product_link": "campaign_product_link1",
        "campaign_hashtag": "campaign_hashtag1",
        "campaign_discount_code": "campaign_discount_code1",
        "product_title": "product_title1",
        "product_description": "product_description1",
    }


def remove_non_updatable_fields_from_campaign(campaign: dict) -> None:
    campaign.pop("id")
    campaign.pop("campaign_state")
    campaign.pop("created")
    campaign.pop("brand_id")
    campaign.pop("product_image1")
    campaign.pop("product_image2")
    campaign.pop("product_image3")
    campaign.pop("campaign_categories")
    campaign.pop("campaign_values")


def remove_non_updatable_fields_from_campaign_body(campaign: dict) -> None:
    campaign.pop("campaign_categories")
    campaign.pop("campaign_values")


class TestCampaignController(TestCase):

    def setUp(self) -> None:
        self.__campaign_repository: CampaignRepository = Mock()
        self.__sut = CampaignController(repository=self.__campaign_repository)

    def test_write_for_brand(self):
        # arrange
        campaign_from_db = create_campaign_from_db()
        context = PinfluencerContext(response=PinfluencerResponse(),
                                     short_circuit=False,
                                     auth_user_id="12341",
                                     body=create_or_update_campaign_body())
        self.__campaign_repository.write_new_for_brand = MagicMock(return_value=campaign_from_db)

        # act
        self.__sut.create(context=context)

        # assert
        payload_captor = Captor()
        self.__campaign_repository.write_new_for_brand.assert_called_once_with(
            payload=payload_captor,
            auth_user_id="12341")
        payload_campaign: Campaign = payload_captor.arg
        payload_campaign_dict = payload_campaign.__dict__
        assert payload_campaign.campaign_state == CampaignStateEnum.DRAFT
        assert payload_campaign.product_image1 is None
        assert payload_campaign.product_image2 is None
        assert payload_campaign.product_image3 is None
        assert list(map(
            lambda x: x.name,
            payload_campaign.campaign_categories)) == create_or_update_campaign_body()["campaign_categories"]
        assert list(map(
            lambda x: x.name,
            payload_campaign.campaign_values)) == create_or_update_campaign_body()["campaign_values"]
        remove_non_updatable_fields_from_campaign(campaign=payload_campaign_dict)
        remove_non_updatable_fields_from_campaign(campaign=context.response.body)
        campaign_body = create_or_update_campaign_body()
        remove_non_updatable_fields_from_campaign_body(campaign=campaign_body)
        assert context.short_circuit == False
        assert context.response.body == payload_campaign_dict
        assert context.response.status_code == 201
        assert payload_campaign_dict == campaign_body

    def test_write_for_brand_when_brand_not_found(self):
        # arrange
        context = PinfluencerContext(response=PinfluencerResponse(),
                                     auth_user_id="1234",
                                     body=create_or_update_campaign_body())
        self.__campaign_repository.write_new_for_brand = MagicMock(side_effect=NotFoundException())

        # act
        self.__sut.create(context=context)

        # assert
        assert context.short_circuit == True
        assert context.response.body == {}
        assert context.response.status_code == 404

    def test_get_by_id(self):
        # arrange
        campaign = campaign_dto_generator(num=1)
        context = PinfluencerContext(id="123456",
                                     response=PinfluencerResponse())
        self.__campaign_repository.load_by_id = MagicMock(return_value=campaign)

        # act
        self.__sut.get_by_id(context=context)

        # assert
        assert context.response.body == campaign.__dict__

    def test_get_for_brand(self):
        # arrange
        campaigns = [
            campaign_dto_generator(num=1),
            campaign_dto_generator(num=2),
            campaign_dto_generator(num=3)
        ]
        auth_user_id = "1234"
        context = PinfluencerContext(auth_user_id=auth_user_id,
                                     response=PinfluencerResponse(),
                                     short_circuit=False)
        self.__campaign_repository.load_for_auth_brand = MagicMock(return_value=campaigns)

        # act
        self.__sut.get_for_brand(context=context)

        # assert
        self.__campaign_repository.load_for_auth_brand.assert_called_once_with(auth_user_id=auth_user_id)
        assert context.short_circuit == False
        assert context.response.body == list(map(lambda x: x.__dict__, campaigns))
        assert context.response.status_code == 200

    def test_get_for_brand_when_brand_not_found(self):

        # arrange
        context = PinfluencerContext(response=PinfluencerResponse(),
                                     short_circuit=False,
                                     auth_user_id="12341")
        self.__campaign_repository.load_for_auth_brand = MagicMock(side_effect=NotFoundException())

        # act
        self.__sut.get_for_brand(context=context)

        # assert
        assert context.short_circuit == True
        assert context.response.body == {}
        assert context.response.status_code == 404

    def test_update_product_image1(self):
        # arrange
        expected_campaign = campaign_dto_generator(num=1)
        self.__campaign_repository.update_product_image1 = MagicMock(return_value=expected_campaign)
        context = PinfluencerContext(body=update_image_payload(),
                                     id="12341",
                                     response=PinfluencerResponse())

        # act
        self.__sut.update_product_image1(context)

        # assert
        self.__campaign_repository.update_product_image1.assert_called_once_with(id=context.id,
                                                                                 image_bytes="random_bytes")
        assert context.response.body == expected_campaign.__dict__

    def test_update_product_image2(self):
        # arrange
        expected_campaign = campaign_dto_generator(num=1)
        self.__campaign_repository.update_product_image2 = MagicMock(return_value=expected_campaign)
        context = PinfluencerContext(body=update_image_payload(),
                                     id="12341",
                                     response=PinfluencerResponse())

        # act
        self.__sut.update_product_image2(context)

        # assert
        self.__campaign_repository.update_product_image2.assert_called_once_with(id=context.id,
                                                                                 image_bytes="random_bytes")
        assert context.response.body == expected_campaign.__dict__

    def test_update_product_image3(self):
        # arrange
        expected_campaign = campaign_dto_generator(num=1)
        self.__campaign_repository.update_product_image3 = MagicMock(return_value=expected_campaign)
        context = PinfluencerContext(body=update_image_payload(),
                                     id="12341",
                                     response=PinfluencerResponse())

        # act
        self.__sut.update_product_image3(context)

        # assert
        self.__campaign_repository.update_product_image3.assert_called_once_with(id=context.id,
                                                                                 image_bytes="random_bytes")
        assert context.response.body == expected_campaign.__dict__

    def test_update(self):
        # arrange

        campaign_body = create_or_update_campaign_body()
        context = PinfluencerContext(body=campaign_body,
                                     response=PinfluencerResponse(),
                                     id="123456",
                                     short_circuit=False)
        updated_campaign_in_db = campaign_dto_generator(num=1)
        updated_campaign_in_db.id = "123456"
        self.__campaign_repository.update_campaign = MagicMock(return_value=updated_campaign_in_db)

        # act
        self.__sut.update(context=context)

        # assert
        captor = Captor()
        self.__campaign_repository.update_campaign.assert_called_once_with(_id="123456",
                                                                           payload=captor)
        actual_payload: Campaign = captor.arg
        assert context.response.body["id"] == "123456"
        assert context.response.body["brand_id"] == "brand_id1"
        assert campaign_body["campaign_values"] == list(map(lambda x: x.name, actual_payload.campaign_values)) == list(map(lambda x: x.name, context.response.body["campaign_values"]))
        assert campaign_body["campaign_categories"] == list(map(lambda x: x.name, actual_payload.campaign_categories)) == list(map(lambda x: x.name, context.response.body["campaign_categories"]))
        remove_non_updatable_fields_from_campaign_body(campaign=campaign_body)
        remove_non_updatable_fields_from_campaign(campaign=context.response.body)
        actual_payload_dict = actual_payload.__dict__
        remove_non_updatable_fields_from_campaign(campaign=actual_payload_dict)
        assert actual_payload_dict == context.response.body == campaign_body
        assert context.response.status_code == 200
        assert context.short_circuit == False

    def test_update_when_not_found(self):
        # arrange
        context = PinfluencerContext(response=PinfluencerResponse(),
                                     short_circuit=False,
                                     body=create_or_update_campaign_body())
        self.__campaign_repository.update_campaign = MagicMock(side_effect=NotFoundException())

        # act
        self.__sut.update(context=context)

        # assert
        assert context.short_circuit == True
        assert context.response.body == {}
        assert context.response.status_code == 404

    def test_update_campaign_state(self):
        # arrange
        context = PinfluencerContext(id="123456",
                                     response=PinfluencerResponse(),
                                     short_circuit=False,
                                     body={
                                         "campaign_state": "ACTIVE"
                                     })
        campaign = campaign_dto_generator(num=1)
        campaign.campaign_state = CampaignStateEnum.ACTIVE
        campaign.id = "123456"
        self.__campaign_repository.update_campaign_state = MagicMock(return_value=campaign)

        # act
        self.__sut.update_campaign_state(context=context)

        # assert
        self.__campaign_repository.update_campaign_state.assert_called_once_with(_id="123456",
                                                                                 payload=CampaignStateEnum.ACTIVE)
        assert context.response.body == campaign.__dict__
        assert context.response.status_code == 200
        assert context.short_circuit == False

    def test_update_campaign_state_when_not_found(self):
        # arrange
        context = PinfluencerContext(id="123456",
                                     response=PinfluencerResponse(),
                                     short_circuit=False,
                                     body={
                                         "campaign_state": "ACTIVE"
                                     })
        self.__campaign_repository.update_campaign_state = MagicMock(side_effect=NotFoundException())

        # act
        self.__sut.update_campaign_state(context=context)

        # assert
        assert context.response.body == {}
        assert context.response.status_code == 404
        assert context.short_circuit == True