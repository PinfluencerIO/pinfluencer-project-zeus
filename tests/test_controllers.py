import uuid
from unittest.mock import Mock, MagicMock

from callee import Captor
from ddt import ddt, data

from src._types import BrandRepository, InfluencerRepository, CampaignRepository
from src.crosscutting import PinfluencerObjectMapper, AutoFixture, FlexiUpdater
from src.domain.models import Influencer, Campaign, Brand
from src.exceptions import AlreadyExistsException, NotFoundException
from src.web import PinfluencerContext, PinfluencerResponse
from src.web.controllers import BrandController, InfluencerController, CampaignController
from src.web.views import BrandRequestDto, BrandResponseDto, ImageRequestDto, InfluencerRequestDto, \
    InfluencerResponseDto, CampaignRequestDto, CampaignResponseDto
from tests import PinfluencerTestCase


class TestInfluencerController(PinfluencerTestCase):

    def setUp(self):
        self.__flexi_updater = FlexiUpdater()
        self.__influencer_repository: InfluencerRepository = Mock()
        self.__object_mapper = PinfluencerObjectMapper()
        self.__sut = InfluencerController(influencer_repository=self.__influencer_repository,
                                          object_mapper=self.__object_mapper,
                                          flexi_updater=self.__flexi_updater,
                                          logger=Mock())

    def test_get_by_id(self):
        # arrange
        influencer_in_db = AutoFixture().create(dto=Influencer, list_limit=5)
        self.__influencer_repository.load_by_id = MagicMock(return_value=influencer_in_db)
        pinfluencer_response = PinfluencerResponse()

        # act
        self.__sut.get_by_id(PinfluencerContext(response=pinfluencer_response,
                                                id=influencer_in_db.id))

        # assert
        assert pinfluencer_response.body == influencer_in_db.__dict__

    def test_get(self):
        # arrange
        db_influencer = AutoFixture().create(dto=Influencer, list_limit=5)
        self.__influencer_repository.load_for_auth_user = MagicMock(return_value=db_influencer)
        response = PinfluencerResponse()

        # act
        self.__sut.get(PinfluencerContext(response=response,
                                          auth_user_id=db_influencer.auth_user_id))

        # assert
        with self.tdd_test(msg="influencer is returned"):
            assert response.body == db_influencer.__dict__

        # assert
        with self.tdd_test(msg="200 response is returned"):
            assert response.status_code == 200

    def test_get_all(self):
        # arrange
        influencers_from_db = AutoFixture().create_many(dto=Influencer, list_limit=5, ammount=10)
        self.__influencer_repository.load_collection = MagicMock(return_value=influencers_from_db)
        pinfluencer_response = PinfluencerResponse()

        # act
        self.__sut.get_all(PinfluencerContext(response=pinfluencer_response,
                                              event={}))

        # assert
        with self.tdd_test(msg="influencers are returned"):
            assert pinfluencer_response.body == list(map(lambda x: x.__dict__, influencers_from_db))

        # assert
        with self.tdd_test(msg="200 status is returned"):
            assert pinfluencer_response.status_code == 200

    def test_create(self):
        # arrange
        self.__sut._create = MagicMock()
        context = PinfluencerContext()

        # act
        self.__sut.create(context)

        # assert
        self.__sut._create.assert_called_once_with(context=context,
                                                   model=Influencer,
                                                   request=InfluencerRequestDto,
                                                   response=InfluencerResponseDto)

    def test_update(self):
        # arrange
        context = PinfluencerContext()
        self.__sut._update = MagicMock()

        # act
        self.__sut.update(context=context)

        # assert
        self.__sut._update.assert_called_once_with(context=context,
                                                   request=InfluencerRequestDto,
                                                   response=InfluencerResponseDto)


@ddt
class TestBrandController(PinfluencerTestCase):

    def setUp(self):
        self.__flexi_updater = FlexiUpdater()
        self.__brand_repository: BrandRepository = Mock()
        self.__object_mapper = PinfluencerObjectMapper()
        self.__sut = BrandController(brand_repository=self.__brand_repository,
                                     object_mapper=self.__object_mapper,
                                     flexi_updater=self.__flexi_updater,
                                     logger=Mock())

    @data("logo", "header_image")
    def test_update_image_field(self, image_field):
        # arrange
        brand_in_db: Brand = AutoFixture().create(dto=Brand,
                                           list_limit=5)
        self.__brand_repository.load_for_auth_user = MagicMock(return_value=brand_in_db)
        self.__sut._unit_of_work = MagicMock()
        image_request: ImageRequestDto = AutoFixture().create(dto=ImageRequestDto)
        image_request.image_field = image_field
        context = PinfluencerContext(body=image_request.__dict__,
                                     auth_user_id=brand_in_db.auth_user_id,
                                     response=PinfluencerResponse(body={}),
                                     short_circuit=False)

        self.__sut.update_image_field(context=context)

        # assert
        with self.tdd_test(msg="work was done in UoW"):
            self.__sut._unit_of_work.assert_called_once()

        # assert
        with self.tdd_test(msg="repo was called"):
            self.__brand_repository.load_for_auth_user.assert_called_once_with(auth_user_id=brand_in_db.auth_user_id)

        # assert
        with self.tdd_test(msg="image field was updated"):
            assert getattr(brand_in_db, image_field) == image_request.image_path

        # assert
        with self.tdd_test(msg="200 was returned"):
            assert context.response.status_code == 200

        # assert
        with self.tdd_test(msg="middleware does not short"):
            assert context.short_circuit == False

        # assert
        with self.tdd_test(msg="brand was returned"):
            assert context.response.body == self.__object_mapper.map(_from=brand_in_db, to=BrandResponseDto)


    def test_update_image_field_when_not_found(self):
        # arrange
        self.__brand_repository.load_for_auth_user = MagicMock(side_effect=NotFoundException())
        self.__sut._unit_of_work = MagicMock()
        image_request: ImageRequestDto = AutoFixture().create(dto=ImageRequestDto)
        image_request.image_field = "logo"
        context = PinfluencerContext(body=image_request.__dict__,
                                     auth_user_id="1234",
                                     response=PinfluencerResponse(body={}))

        self.__sut.update_image_field(context=context)

        # assert
        with self.tdd_test(msg="404 was returned"):
            assert context.response.status_code == 404

        # assert
        with self.tdd_test(msg="middleware shorts"):
            assert context.short_circuit == True

        # assert
        with self.tdd_test(msg="empty body is returned"):
            assert context.response.body == {}

    def test_unit_of_work(self):
        # arrange
        self.__brand_repository.load_by_id = MagicMock()
        self.__brand_repository.save = MagicMock()

        # act
        self.test_unit_of_work_call()

        # assert
        with self.tdd_test(msg="brand repository is called"):
            self.__brand_repository.load_by_id.assert_called_once()

        # assert
        with self.tdd_test(msg="commit is called"):
            self.__brand_repository.save.assert_called_once()

    def test_unit_of_work_when_error_occurs(self):
        # arrange
        self.__brand_repository.load_by_id = MagicMock(side_effect=NotFoundException())
        self.__brand_repository.save = MagicMock()

        # act/assert
        with self.tdd_test(msg="unit of work still throws"):
            self.assertRaises(NotFoundException, lambda: self.test_unit_of_work_call())

        # assert
        with self.tdd_test(msg="brand repository is called"):
            self.__brand_repository.load_by_id.assert_called_once()

        # assert
        with self.tdd_test(msg="commit is not called"):
            self.__brand_repository.save.assert_not_called()

    def test_unit_of_work_call(self):
        with self.__sut._unit_of_work():
            self.__brand_repository.load_by_id(id_="")

    def test_get_by_id(self):
        # arrange
        brand_from_db = AutoFixture().create(dto=Brand,
                                             list_limit=5)
        self.__brand_repository.load_by_id = MagicMock(return_value=brand_from_db)
        pinfluencer_response = PinfluencerResponse()

        # act
        self.__sut.get_by_id(PinfluencerContext(id=brand_from_db.id,
                                                response=pinfluencer_response))

        # assert
        with self.tdd_test("brand repository was called"):
            self.__brand_repository.load_by_id.assert_called_once_with(id_=brand_from_db.id)

        # assert
        with self.tdd_test("returned brand is the same as brand in db"):
            assert pinfluencer_response.body == brand_from_db.__dict__

        # assert
        with self.tdd_test("response is ok"):
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
        with self.tdd_test("brand repository was called"):
            self.__brand_repository.load_by_id.assert_called_once_with(id_=field)

        # assert
        with self.tdd_test("body is empty"):
            assert pinfluencer_response.body == {}

        # assert
        with self.tdd_test("response code is 404"):
            assert pinfluencer_response.status_code == 404

        # assert
        with self.tdd_test("middleware will short circuit"):
            assert context.short_circuit == True

    def test_get_all(self):
        # arrange
        brands_from_db = AutoFixture().create_many(dto=Brand,
                                                   ammount=5,
                                                   list_limit=5)
        self.__brand_repository.load_collection = MagicMock(return_value=brands_from_db)
        pinfluencer_response = PinfluencerResponse()

        # act
        self.__sut.get_all(PinfluencerContext(event={},
                                              response=pinfluencer_response))

        # assert
        with self.tdd_test("brand repository was called"):
            self.__brand_repository.load_collection.assert_called_once()

        # assert
        with self.tdd_test("response body is equal to list of brands in db"):
            assert pinfluencer_response.body == list(map(lambda x: x.__dict__, brands_from_db))

        # assert
        with self.tdd_test("response status code is 200"):
            assert pinfluencer_response.status_code == 200

    def test_get(self):
        # arrange
        db_brand: Brand = AutoFixture().create(dto=Brand,
                                               list_limit=5)
        self.__brand_repository.load_for_auth_user = MagicMock(return_value=db_brand)
        response = PinfluencerResponse()

        # act
        self.__sut.get(PinfluencerContext(auth_user_id=db_brand.auth_user_id,
                                          response=response))

        # assert
        with self.tdd_test("brand repository is called"):
            self.__brand_repository.load_for_auth_user.assert_called_once_with(auth_user_id=db_brand.auth_user_id)

        # assert
        with self.tdd_test("response body is equal to brand in db"):
            assert response.body == db_brand.__dict__

        # assert
        with self.tdd_test("response status code is 200"):
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
        with self.tdd_test("brand repository is called"):
            self.__brand_repository.load_for_auth_user.assert_called_once_with(auth_user_id=auth_id)

        # assert
        with self.tdd_test("response body is empty"):
            assert response.body == {}

        # assert
        with self.tdd_test("response status code is 404"):
            assert response.status_code == 404

        # assert
        with self.tdd_test("middleware short circuits"):
            assert context.short_circuit == True

    def test_create(self):
        # arrange
        brand_request: BrandRequestDto = AutoFixture().create(dto=BrandRequestDto,
                                                              list_limit=5)
        brand_db: Brand = self.__object_mapper.map(_from=brand_request,
                                                   to=Brand)
        self.__sut._unit_of_work = MagicMock()
        brand_db.auth_user_id = "12345"
        self.__brand_repository.write_new_for_auth_user = MagicMock(return_value=brand_db)
        response = PinfluencerResponse()

        # act
        self.__sut.create(PinfluencerContext(body=brand_request.__dict__,
                                             auth_user_id=brand_db.auth_user_id,
                                             response=response))
        payload_captor = Captor()

        # assert
        with self.tdd_test("unit of work called"):
            self.__sut._unit_of_work.assert_called_once()

        # assert
        with self.tdd_test("brand repository was called"):
            self.__brand_repository.write_new_for_auth_user.assert_called_once_with(auth_user_id=brand_db.auth_user_id,
                                                                                    payload=payload_captor)
        actual_payload: Brand = payload_captor.arg

        # assert
        with self.tdd_test("response code was created"):
            assert response.status_code == 201

        mapped_brand_body: BrandResponseDto = self.__object_mapper.map_from_dict(_from=response.body,
                                                                                 to=BrandResponseDto)

        # assert
        with self.tdd_test("response was equal to brand in db and body"):
            # brand in db asserts
            assert brand_db.id == mapped_brand_body.id
            assert brand_db.created == mapped_brand_body.created
            assert brand_db.header_image == mapped_brand_body.header_image
            assert brand_db.logo == mapped_brand_body.logo

        # assert
        with self.tdd_test("response was equal to brand in db and request and body"):
            # brand response asserts
            assert actual_payload.brand_description == brand_request.brand_description == mapped_brand_body.brand_description == brand_db.brand_description
            assert actual_payload.brand_name == brand_request.brand_name == mapped_brand_body.brand_name == brand_db.brand_name
            assert actual_payload.categories == brand_request.categories == mapped_brand_body.categories == brand_db.categories
            assert actual_payload.insta_handle == brand_request.insta_handle == mapped_brand_body.insta_handle == brand_db.insta_handle
            assert actual_payload.values == brand_request.values == mapped_brand_body.values == brand_db.values
            assert actual_payload.website == brand_request.website == mapped_brand_body.website == brand_db.website

    def test_create_when_exists(self):
        # arrange
        auth_id = "12341"
        self.__brand_repository.write_new_for_auth_user = MagicMock(side_effect=AlreadyExistsException())
        response = PinfluencerResponse()
        brand_request: dict = AutoFixture().create_dict(dto=BrandRequestDto,
                                                        list_limit=5)

        # act
        context = PinfluencerContext(auth_user_id=auth_id,
                                     response=response,
                                     body=brand_request)
        self.__sut.create(context)

        # assert
        with self.tdd_test("response status code is 400"):
            assert response.status_code == 400

        # assert
        with self.tdd_test("response body is empty"):
            assert response.body == {}

        # assert
        with self.tdd_test("middleware should short circuit"):
            assert context.short_circuit == True

    def test_update_all(self):
        # arrange
        brand_request: BrandRequestDto = AutoFixture().create(dto=BrandRequestDto,
                                                              list_limit=5)
        brand_db: Brand = AutoFixture().create(dto=Brand,
                                               list_limit=5)
        self.__brand_repository.load_for_auth_user = MagicMock(return_value=brand_db)
        response = PinfluencerResponse()
        self.__sut._unit_of_work = MagicMock()

        # act
        self.__sut.update(PinfluencerContext(body=brand_request.__dict__,
                                             auth_user_id=brand_db.auth_user_id,
                                             response=response))

        # assert
        with self.tdd_test(msg="repository was called"):
            self.__brand_repository.load_for_auth_user.assert_called_once_with(auth_user_id=brand_db.auth_user_id)

        # assert
        with self.tdd_test(msg="repository was called"):
            assert response.status_code == 200

        mapped_brand_body: BrandResponseDto = self.__object_mapper.map_from_dict(_from=response.body,
                                                                                 to=BrandResponseDto)

        # assert
        with self.tdd_test(msg="brand in db, request and response body match"):
            # brand response asserts
            assert brand_db.brand_description == brand_request.brand_description == mapped_brand_body.brand_description
            assert brand_db.brand_name == brand_request.brand_name == mapped_brand_body.brand_name
            assert brand_db.categories == brand_request.categories == mapped_brand_body.categories
            assert brand_db.insta_handle == brand_request.insta_handle == mapped_brand_body.insta_handle
            assert brand_db.values == brand_request.values == mapped_brand_body.values
            assert brand_db.website == brand_request.website == mapped_brand_body.website

        # assert
        with self.tdd_test(msg="brand in db and response body match"):
            # brand in db asserts
            assert brand_db.id == mapped_brand_body.id
            assert brand_db.created == mapped_brand_body.created
            assert brand_db.header_image == mapped_brand_body.header_image
            assert brand_db.logo == mapped_brand_body.logo

    def test_update_partial_brand_details(self):
        # arrange
        brand_request: BrandRequestDto = AutoFixture().create(dto=BrandRequestDto,
                                                              list_limit=5)
        del brand_request.brand_description
        del brand_request.categories
        del brand_request.website
        brand_db: Brand = AutoFixture().create(dto=Brand,
                                               list_limit=5)
        deep_copy_of_brand_db: Brand = self.__object_mapper.map(_from=brand_db, to=Brand)
        self.__brand_repository.load_for_auth_user = MagicMock(return_value=brand_db)
        response = PinfluencerResponse()
        self.__sut._unit_of_work = MagicMock()

        # act
        self.__sut.update(PinfluencerContext(body=brand_request.__dict__,
                                             auth_user_id=brand_db.auth_user_id,
                                             response=response))

        mapped_brand_body: BrandResponseDto = self.__object_mapper.map_from_dict(_from=response.body,
                                                                                 to=BrandResponseDto)

        # assert
        with self.tdd_test(msg="brand in db, request and response body match"):
            # brand response asserts
            assert deep_copy_of_brand_db.brand_description == mapped_brand_body.brand_description
            assert brand_db.brand_name == brand_request.brand_name == mapped_brand_body.brand_name
            assert deep_copy_of_brand_db.categories == mapped_brand_body.categories
            assert brand_db.insta_handle == brand_request.insta_handle == mapped_brand_body.insta_handle
            assert brand_db.values == brand_request.values == mapped_brand_body.values
            assert deep_copy_of_brand_db.website == mapped_brand_body.website

        # assert
        with self.tdd_test(msg="brand in db and response body match"):
            # brand in db asserts
            assert brand_db.id == mapped_brand_body.id
            assert brand_db.created == mapped_brand_body.created
            assert brand_db.header_image == mapped_brand_body.header_image
            assert brand_db.logo == mapped_brand_body.logo

    def test_update_when_not_found(self):
        # arrange
        auth_id = "12341"
        payload: BrandRequestDto = AutoFixture().create(dto=BrandRequestDto,
                                                        list_limit=5)
        self.__brand_repository.load_for_auth_user = MagicMock(side_effect=NotFoundException())
        response = PinfluencerResponse()

        # act
        context = PinfluencerContext(body=payload.__dict__,
                                     auth_user_id=auth_id,
                                     response=response)
        self.__sut.update(context)

        # assert
        with self.tdd_test(msg="status code is 404"):
            assert response.status_code == 404

        # assert
        with self.tdd_test(msg="response body is empty"):
            assert response.body == {}

        # assert
        with self.tdd_test(msg="middleware short circuits"):
            assert context.short_circuit == True


class TestCampaignController(PinfluencerTestCase):

    def setUp(self) -> None:
        self.__flexi_updater = FlexiUpdater()
        self.__campaign_repository: CampaignRepository = Mock()
        self.__object_mapper = PinfluencerObjectMapper()
        self.__sut = CampaignController(repository=self.__campaign_repository,
                                        object_mapper=self.__object_mapper,
                                        flexi_updater=self.__flexi_updater,
                                        logger=Mock())

    def test_write_for_campaign(self):
        # arrange
        self.__sut._unit_of_work = MagicMock()
        campaign_from_db = AutoFixture().create(dto=Campaign, list_limit=5)
        campaign_request: CampaignRequestDto = self.__object_mapper.map(_from=campaign_from_db, to=CampaignRequestDto)
        context = PinfluencerContext(response=PinfluencerResponse(),
                                     short_circuit=False,
                                     auth_user_id="12341",
                                     body=campaign_request.__dict__)
        self.__campaign_repository.write_new_for_brand = MagicMock(return_value=campaign_from_db)

        # act
        self.__sut.create(context=context)

        # assert
        payload_captor = Captor()

        # assert
        with self.tdd_test(msg="work was done in unit of work"):
            self.__sut._unit_of_work.assert_called_once()

        # assert
        with self.tdd_test(msg="repo was called"):
            self.__campaign_repository.write_new_for_brand.assert_called_once_with(
                payload=payload_captor,
                auth_user_id="12341")
        payload_campaign: Campaign = payload_captor.arg

        # assert
        with self.tdd_test(msg="middleware does not short"):
            assert context.short_circuit == False

        # assert
        with self.tdd_test(msg="body equals returned campaign"):
            assert self.__object_mapper.map_from_dict(_from=context.response.body, to=CampaignResponseDto) ==\
                   self.__object_mapper.map(_from=campaign_from_db, to=CampaignResponseDto)

        # assert
        with self.tdd_test(msg="success response is returned"):
            assert context.response.status_code == 201

        # assert
        with self.tdd_test(msg="campaign fields match"):
            assert payload_campaign.campaign_hashtag == campaign_request.campaign_hashtag
            assert payload_campaign.campaign_categories == campaign_request.campaign_categories
            assert payload_campaign.campaign_values == campaign_request.campaign_values
            assert payload_campaign.campaign_state == campaign_request.campaign_state
            assert payload_campaign.campaign_description == campaign_request.campaign_description
            assert payload_campaign.campaign_discount_code == campaign_request.campaign_discount_code
            assert payload_campaign.campaign_product_link == campaign_request.campaign_product_link
            assert payload_campaign.campaign_title == campaign_request.campaign_title
            assert payload_campaign.objective == campaign_request.objective
            assert payload_campaign.product_description == campaign_request.product_description
            assert payload_campaign.product_title == campaign_request.product_title
            assert payload_campaign.success_description == campaign_request.success_description

    def test_write_for_brand_when_brand_not_found(self):
        # arrange
        campaign_request: CampaignRequestDto = AutoFixture().create(dto=CampaignRequestDto, list_limit=5)
        context = PinfluencerContext(response=PinfluencerResponse(),
                                     auth_user_id="1234",
                                     body=campaign_request.__dict__)
        self.__campaign_repository.write_new_for_brand = MagicMock(side_effect=NotFoundException())

        # act
        self.__sut.create(context=context)

        # assert
        with self.tdd_test(msg="middleware shorts"):
            assert context.short_circuit == True

        # assert
        with self.tdd_test(msg="body is empty"):
            assert context.response.body == {}

        # assert
        with self.tdd_test(msg="response is not found"):
            assert context.response.status_code == 404

    def test_get_by_id(self):
        # arrange
        campaign = AutoFixture().create(dto=Campaign, list_limit=5)
        context = PinfluencerContext(id=campaign.id,
                                     response=PinfluencerResponse())
        self.__campaign_repository.load_by_id = MagicMock(return_value=campaign)

        # act
        self.__sut.get_by_id(context=context)

        # assert
        assert context.response.body == campaign.__dict__

    def test_get_for_brand(self):
        # arrange
        campaigns = AutoFixture().create_many(dto=Campaign, list_limit=5, ammount=10)
        auth_user_id = "1234"
        context = PinfluencerContext(auth_user_id=auth_user_id,
                                     response=PinfluencerResponse(),
                                     short_circuit=False)
        self.__campaign_repository.load_for_auth_brand = MagicMock(return_value=campaigns)

        # act
        self.__sut.get_for_brand(context=context)

        # assert
        with self.tdd_test(msg="repo is called"):
            self.__campaign_repository.load_for_auth_brand.assert_called_once_with(auth_user_id=auth_user_id)

        # assert
        with self.tdd_test(msg="middleware shorts"):
            assert context.short_circuit == False

        # assert
        with self.tdd_test(msg="campaigns are returned"):
            assert context.response.body == list(map(lambda x: x.__dict__, campaigns))

        # assert
        with self.tdd_test(msg="response is success"):
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
        with self.tdd_test(msg="middleware shorts"):
            assert context.short_circuit == True

        # assert
        with self.tdd_test(msg="body is empty"):
            assert context.response.body == {}

        # assert
        with self.tdd_test(msg="response is not found"):
            assert context.response.status_code == 404

    def test_update(self):
        # arrange
        context = PinfluencerContext()
        self.__sut._update = MagicMock()

        # act
        self.__sut.update(context=context)

        # assert
        self.__sut._update.assert_called_once_with(context=context, request=CampaignRequestDto, response=CampaignResponseDto)