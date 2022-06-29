import uuid
from unittest import TestCase
from unittest.mock import Mock, MagicMock

from callee import Captor

from src.domain.models import Influencer, Campaign, CategoryEnum, ValueEnum
from src.exceptions import AlreadyExistsException, NotFoundException
from src.types import BrandRepository, InfluencerRepository, CampaignRepository
from src.web import PinfluencerContext, PinfluencerResponse
from src.web.controllers import BrandController, InfluencerController, CampaignController
from src.web.validation import valid_uuid
from tests import brand_dto_generator, assert_brand_updatable_fields_are_equal, TEST_DEFAULT_BRAND_LOGO, \
    TEST_DEFAULT_BRAND_HEADER_IMAGE, influencer_dto_generator, RepoEnum, \
    assert_brand_creatable_generated_fields_are_equal, TEST_DEFAULT_INFLUENCER_PROFILE_IMAGE, \
    assert_influencer_creatable_generated_fields_are_equal, assert_influencer_update_fields_are_equal, \
    update_brand_payload, create_brand_dto, \
    update_image_payload, update_brand_return_dto, create_influencer_dto, \
    update_influencer_payload, TEST_DEFAULT_PRODUCT_IMAGE1, TEST_DEFAULT_PRODUCT_IMAGE2, \
    TEST_DEFAULT_PRODUCT_IMAGE3


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
        assert actual_payload.image == TEST_DEFAULT_INFLUENCER_PROFILE_IMAGE
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
        assert actual_payload.logo == TEST_DEFAULT_BRAND_LOGO
        assert actual_payload.header_image == TEST_DEFAULT_BRAND_HEADER_IMAGE
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


def create_campaign_body() -> dict:
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
                                     body=create_campaign_body())
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
        assert payload_campaign.product_image1 == TEST_DEFAULT_PRODUCT_IMAGE1
        assert payload_campaign.product_image2 == TEST_DEFAULT_PRODUCT_IMAGE2
        assert payload_campaign.product_image3 == TEST_DEFAULT_PRODUCT_IMAGE3
        payload_campaign_dict.pop("id")
        payload_campaign_dict.pop("created")
        payload_campaign_dict.pop("brand_id")
        payload_campaign_dict.pop("product_image1")
        payload_campaign_dict.pop("product_image2")
        payload_campaign_dict.pop("product_image3")
        context.response.body.pop("id")
        context.response.body.pop("created")
        context.response.body.pop("brand_id")
        context.response.body.pop("product_image1")
        context.response.body.pop("product_image2")
        context.response.body.pop("product_image3")
        assert context.short_circuit == False
        assert context.response.body == payload_campaign_dict
        assert context.response.status_code == 201
        assert list(map(
            lambda x: x.name,
            payload_campaign.campaign_categories)) == create_campaign_body()["campaign_categories"]
        assert list(map(
            lambda x: x.name,
            payload_campaign.campaign_values)) == create_campaign_body()["campaign_values"]
        campaign_body = create_campaign_body()
        campaign_body.pop("campaign_categories")
        campaign_body.pop("campaign_values")
        payload_campaign_dict.pop("campaign_categories")
        payload_campaign_dict.pop("campaign_values")
        assert payload_campaign_dict == campaign_body

    def test_write_for_brand_when_brand_not_found(self):

        # arrange
        context = PinfluencerContext(response=PinfluencerResponse(),
                                     auth_user_id="1234",
                                     body=create_campaign_body())
        self.__campaign_repository.write_new_for_brand = MagicMock(side_effect=NotFoundException())

        # act
        self.__sut.create(context=context)

        # assert
        assert context.short_circuit == True
        assert context.response.body == {}
        assert context.response.status_code == 404