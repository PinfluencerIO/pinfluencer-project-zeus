import uuid
from unittest import TestCase
from unittest.mock import Mock, MagicMock

from callee import Captor
from ddt import ddt, data

from src._types import BrandRepository, InfluencerRepository, CampaignRepository, NotificationRepository
from src.app import logger_factory
from src.crosscutting import PinfluencerObjectMapper, AutoFixture, FlexiUpdater
from src.domain.models import Influencer, Campaign, Brand, Notification
from src.exceptions import AlreadyExistsException, NotFoundException
from src.web import PinfluencerContext, PinfluencerResponse
from src.web.controllers import BrandController, InfluencerController, CampaignController, NotificationController
from src.web.views import BrandRequestDto, BrandResponseDto, ImageRequestDto, InfluencerRequestDto, \
    InfluencerResponseDto, CampaignRequestDto, CampaignResponseDto, NotificationCreateRequestDto, \
    NotificationResponseDto


class TestInfluencerController(TestCase):

    def setUp(self):
        self.__flexi_updater = FlexiUpdater()
        self.__influencer_repository: InfluencerRepository = Mock()
        self.__object_mapper = PinfluencerObjectMapper(logger=Mock())
        self.__sut = InfluencerController(influencer_repository=self.__influencer_repository,
                                          object_mapper=self.__object_mapper,
                                          flexi_updater=self.__flexi_updater,
                                          logger=Mock())

    def test_get_by_id(self):
        # arrange
        self.__sut._get_by_id = MagicMock()
        context = PinfluencerContext()

        # act
        self.__sut.get_by_id(context)

        # assert
        self.__sut._get_by_id.assert_called_once_with(context=context, response=InfluencerResponseDto)

    def test_get(self):
        # arrange
        self.__sut._get = MagicMock()
        context = PinfluencerContext()

        # act
        self.__sut.get(context)

        # assert
        self.__sut._get.assert_called_once_with(context=context, response=InfluencerResponseDto)

    def test_get_all(self):
        # arrange
        self.__sut._get_all = MagicMock()
        context = PinfluencerContext()

        # act
        self.__sut.get_all(context)

        # assert
        self.__sut._get_all.assert_called_once_with(context=context, response=InfluencerResponseDto)

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
        self.__sut.update_for_user(context=context)

        # assert
        self.__sut._update.assert_called_once_with(context=context,
                                                   request=InfluencerRequestDto,
                                                   response=InfluencerResponseDto)

    def test_update_image_field(self):
        # arrange
        context = PinfluencerContext()
        self.__sut._update_image_field = MagicMock()

        # act
        self.__sut.update_image_field_for_user(context=context)

        # assert
        self.__sut._update_image_field.assert_called_once_with(context=context,
                                                               response=InfluencerResponseDto)


@ddt
class TestBrandController(TestCase):

    def setUp(self):
        self.__flexi_updater = FlexiUpdater()
        self.__brand_repository: BrandRepository = Mock()
        self.__object_mapper = PinfluencerObjectMapper(logger=Mock())
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

        self.__sut.update_image_field_for_user(context=context)

        # assert
        with self.subTest(msg="work was done in UoW"):
            self.__sut._unit_of_work.assert_called_once()

        # assert
        with self.subTest(msg="repo was called"):
            self.__brand_repository.load_for_auth_user.assert_called_once_with(auth_user_id=brand_in_db.auth_user_id)

        # assert
        with self.subTest(msg="image field was updated"):
            assert getattr(brand_in_db, image_field) == image_request.image_path

        # assert
        with self.subTest(msg="200 was returned"):
            assert context.response.status_code == 200

        # assert
        with self.subTest(msg="middleware does not short"):
            assert context.short_circuit == False

        # assert
        with self.subTest(msg="brand was returned"):
            assert context.response.body == self.__object_mapper.map(_from=brand_in_db, to=BrandResponseDto).__dict__

    def test_update_image_field_when_not_found(self):
        # arrange
        self.__brand_repository.load_for_auth_user = MagicMock(side_effect=NotFoundException())
        self.__sut._unit_of_work = MagicMock()
        image_request: ImageRequestDto = AutoFixture().create(dto=ImageRequestDto)
        image_request.image_field = "logo"
        context = PinfluencerContext(body=image_request.__dict__,
                                     auth_user_id="1234",
                                     response=PinfluencerResponse(body={}))

        self.__sut.update_image_field_for_user(context=context)

        # assert
        with self.subTest(msg="404 was returned"):
            assert context.response.status_code == 404

        # assert
        with self.subTest(msg="middleware shorts"):
            assert context.short_circuit == True

        # assert
        with self.subTest(msg="empty body is returned"):
            assert context.response.body == {}

    def test_unit_of_work(self):
        # arrange
        self.__brand_repository.load_by_id = MagicMock()
        self.__brand_repository.save = MagicMock()

        # act
        self.test_unit_of_work_call()

        # assert
        with self.subTest(msg="brand repository is called"):
            self.__brand_repository.load_by_id.assert_called_once()

        # assert
        with self.subTest(msg="commit is called"):
            self.__brand_repository.save.assert_called_once()

    def test_unit_of_work_when_error_occurs(self):
        # arrange
        self.__brand_repository.load_by_id = MagicMock(side_effect=NotFoundException())
        self.__brand_repository.save = MagicMock()

        # act/assert
        with self.subTest(msg="unit of work still throws"):
            self.assertRaises(NotFoundException, lambda: self.test_unit_of_work_call())

        # assert
        with self.subTest(msg="brand repository is called"):
            self.__brand_repository.load_by_id.assert_called_once()

        # assert
        with self.subTest(msg="commit is not called"):
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
        with self.subTest(msg="brand repository was called"):
            self.__brand_repository.load_by_id.assert_called_once_with(id_=brand_from_db.id)

        # assert
        with self.subTest(msg="returned brand is the same as brand in db"):
            assert pinfluencer_response.body == self.__object_mapper.map(_from=brand_from_db,
                                                                         to=BrandResponseDto).__dict__

        # assert
        with self.subTest(msg="response is ok"):
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
        with self.subTest(msg="brand repository was called"):
            self.__brand_repository.load_by_id.assert_called_once_with(id_=field)

        # assert
        with self.subTest(msg="body is empty"):
            assert pinfluencer_response.body == {}

        # assert
        with self.subTest(msg="response code is 404"):
            assert pinfluencer_response.status_code == 404

        # assert
        with self.subTest(msg="middleware will short circuit"):
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
        with self.subTest(msg="brand repository was called"):
            self.__brand_repository.load_collection.assert_called_once()

        # assert
        with self.subTest(msg="response body is equal to list of brands in db"):
            assert pinfluencer_response.body == list(
                map(lambda x: self.__object_mapper.map(_from=x, to=BrandResponseDto).__dict__, brands_from_db))

        # assert
        with self.subTest(msg="response status code is 200"):
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
        with self.subTest(msg="brand repository is called"):
            self.__brand_repository.load_for_auth_user.assert_called_once_with(auth_user_id=db_brand.auth_user_id)

        # assert
        with self.subTest(msg="response body is equal to brand in db"):
            assert response.body == self.__object_mapper.map(_from=db_brand, to=BrandResponseDto).__dict__

        # assert
        with self.subTest(msg="response status code is 200"):
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
        with self.subTest(msg="brand repository is called"):
            self.__brand_repository.load_for_auth_user.assert_called_once_with(auth_user_id=auth_id)

        # assert
        with self.subTest(msg="response body is empty"):
            assert response.body == {}

        # assert
        with self.subTest(msg="response status code is 404"):
            assert response.status_code == 404

        # assert
        with self.subTest(msg="middleware short circuits"):
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
        with self.subTest(msg="unit of work called"):
            self.__sut._unit_of_work.assert_called_once()

        # assert
        with self.subTest(msg="brand repository was called"):
            self.__brand_repository.write_new_for_auth_user.assert_called_once_with(auth_user_id=brand_db.auth_user_id,
                                                                                    payload=payload_captor)
        actual_payload: Brand = payload_captor.arg

        # assert
        with self.subTest(msg="response code was created"):
            assert response.status_code == 201

        mapped_brand_body: BrandResponseDto = self.__object_mapper.map_from_dict(_from=response.body,
                                                                                 to=BrandResponseDto)

        # assert
        with self.subTest(msg="response id was equal to brand id in db and body"):
            assert brand_db.id == mapped_brand_body.id

        # assert
        with self.subTest(msg="response created was equal to brand created in db and body"):
            assert brand_db.created == mapped_brand_body.created

        # assert
        with self.subTest(msg="response header image was equal to brand header image in db and body"):
            assert brand_db.header_image == mapped_brand_body.header_image

        # assert
        with self.subTest(msg="response logo was equal to brand logo in db and body"):
            assert brand_db.logo == mapped_brand_body.logo

        # assert
        with self.subTest(msg="response brand description was equal to brand brand description in db and request brand description and body brand description"):
            assert actual_payload.brand_description == brand_request.brand_description == mapped_brand_body.brand_description == brand_db.brand_description

        # assert
        with self.subTest(msg="response brand name was equal to brand brand name in db and request brand name and body brand name"):
            assert actual_payload.brand_name == brand_request.brand_name == mapped_brand_body.brand_name == brand_db.brand_name

        # assert
        with self.subTest(msg="response categories was equal to brand categories in db and request categories and body categories"):
            assert actual_payload.categories == brand_request.categories == mapped_brand_body.categories == brand_db.categories

        # assert
        with self.subTest(msg="response insta handle was equal to brand insta handle in db and request insta handle and body insta handle"):
            assert actual_payload.insta_handle == brand_request.insta_handle == mapped_brand_body.insta_handle == brand_db.insta_handle

        # assert
        with self.subTest(msg="response values was equal to brand values in db and request values and body values"):
            assert actual_payload.values == brand_request.values == mapped_brand_body.values == brand_db.values

        # assert
        with self.subTest(msg="response website was equal to brand website in db and request website and body website"):
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
        with self.subTest(msg="response status code is 400"):
            assert response.status_code == 400

        # assert
        with self.subTest(msg="response body is empty"):
            assert response.body == {}

        # assert
        with self.subTest(msg="middleware should short circuit"):
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
        self.__sut.update_for_user(PinfluencerContext(body=brand_request.__dict__,
                                                      auth_user_id=brand_db.auth_user_id,
                                                      response=response))

        # assert
        with self.subTest(msg="repository was called"):
            self.__brand_repository.load_for_auth_user.assert_called_once_with(auth_user_id=brand_db.auth_user_id)

        # assert
        with self.subTest(msg="repository was called"):
            assert response.status_code == 200

        mapped_brand_body: BrandResponseDto = self.__object_mapper.map_from_dict(_from=response.body,
                                                                                 to=BrandResponseDto)

        # assert
        with self.subTest(msg="brand in db, request and response body match"):
            # brand response asserts
            assert brand_db.brand_description == brand_request.brand_description == mapped_brand_body.brand_description
            assert brand_db.brand_name == brand_request.brand_name == mapped_brand_body.brand_name
            assert brand_db.categories == brand_request.categories == mapped_brand_body.categories
            assert brand_db.insta_handle == brand_request.insta_handle == mapped_brand_body.insta_handle
            assert brand_db.values == brand_request.values == mapped_brand_body.values
            assert brand_db.website == brand_request.website == mapped_brand_body.website

        # assert
        with self.subTest(msg="brand in db and response body match"):
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
        self.__sut.update_for_user(PinfluencerContext(body=brand_request.__dict__,
                                                      auth_user_id=brand_db.auth_user_id,
                                                      response=response))

        mapped_brand_body: BrandResponseDto = self.__object_mapper.map_from_dict(_from=response.body,
                                                                                 to=BrandResponseDto)

        # assert
        with self.subTest(msg="brand in db, request and response body match"):
            # brand response asserts
            assert deep_copy_of_brand_db.brand_description == mapped_brand_body.brand_description
            assert brand_db.brand_name == brand_request.brand_name == mapped_brand_body.brand_name
            assert deep_copy_of_brand_db.categories == mapped_brand_body.categories
            assert brand_db.insta_handle == brand_request.insta_handle == mapped_brand_body.insta_handle
            assert brand_db.values == brand_request.values == mapped_brand_body.values
            assert deep_copy_of_brand_db.website == mapped_brand_body.website

        # assert
        with self.subTest(msg="brand in db and response body match"):
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
        self.__sut.update_for_user(context)

        # assert
        with self.subTest(msg="status code is 404"):
            assert response.status_code == 404

        # assert
        with self.subTest(msg="response body is empty"):
            assert response.body == {}

        # assert
        with self.subTest(msg="middleware short circuits"):
            assert context.short_circuit == True


class TestCampaignController(TestCase):

    def setUp(self) -> None:
        self.__flexi_updater = FlexiUpdater()
        self.__campaign_repository: CampaignRepository = Mock()
        self.__object_mapper = PinfluencerObjectMapper(logger=Mock())
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
        with self.subTest(msg="work was done in unit of work"):
            self.__sut._unit_of_work.assert_called_once()

        # assert
        with self.subTest(msg="repo was called"):
            self.__campaign_repository.write_new_for_brand.assert_called_once_with(
                payload=payload_captor,
                auth_user_id="12341")
        payload_campaign: Campaign = payload_captor.arg

        # assert
        with self.subTest(msg="middleware does not short"):
            assert context.short_circuit == False

        # assert
        with self.subTest(msg="body equals returned campaign"):
            assert self.__object_mapper.map_from_dict(_from=context.response.body, to=CampaignResponseDto) == \
                   self.__object_mapper.map(_from=campaign_from_db, to=CampaignResponseDto)

        # assert
        with self.subTest(msg="success response is returned"):
            assert context.response.status_code == 201

        # assert
        with self.subTest(msg="campaign fields match"):
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
        with self.subTest(msg="middleware shorts"):
            assert context.short_circuit == True

        # assert
        with self.subTest(msg="body is empty"):
            assert context.response.body == {}

        # assert
        with self.subTest(msg="response is not found"):
            assert context.response.status_code == 404

    def test_get_by_id(self):
        # arrange
        self.__sut._get_by_id = MagicMock()
        context = PinfluencerContext()

        # act
        self.__sut.get_by_id(context)

        # assert
        self.__sut._get_by_id.assert_called_once_with(context=context, response=CampaignResponseDto)

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
        with self.subTest(msg="repo is called"):
            self.__campaign_repository.load_for_auth_brand.assert_called_once_with(auth_user_id=auth_user_id)

        # assert
        with self.subTest(msg="middleware shorts"):
            assert context.short_circuit == False

        # assert
        with self.subTest(msg="campaigns are returned"):
            assert context.response.body == list(
                map(lambda x: self.__object_mapper.map(_from=x, to=CampaignResponseDto).__dict__, campaigns))

        # assert
        with self.subTest(msg="response is success"):
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
        with self.subTest(msg="middleware shorts"):
            assert context.short_circuit == True

        # assert
        with self.subTest(msg="body is empty"):
            assert context.response.body == {}

        # assert
        with self.subTest(msg="response is not found"):
            assert context.response.status_code == 404

    def test_update(self):
        # arrange
        context = PinfluencerContext(id="12345")
        self.__sut._generic_update = MagicMock()
        self.__campaign_repository.load_by_id = MagicMock()

        # act
        self.__sut.update_campaign(context=context)

        # assert
        captor = Captor()

        with self.subTest(msg="generic update was made"):
            self.__sut._generic_update.assert_called_once_with(context=context, request=CampaignRequestDto,
                                                               response=CampaignResponseDto,
                                                               repo_func=captor)

        with self.subTest(msg="repo was called"):
            captor.arg()
            self.__campaign_repository.load_by_id.assert_called_once_with(id_=context.id)

    def test_update_image_field(self):
        # arrange
        context = PinfluencerContext(id="12345")
        self.__sut._generic_update_image_field = MagicMock()
        self.__campaign_repository.load_by_id = MagicMock()

        # act
        self.__sut.update_campaign_image(context=context)

        # assert
        captor = Captor()

        with self.subTest(msg="generic update was made"):
            self.__sut._generic_update_image_field.assert_called_once_with(context=context,
                                                                           response=CampaignResponseDto,
                                                                           repo_func=captor)

        with self.subTest(msg="repo was called"):
            captor.arg()
            self.__campaign_repository.load_by_id.assert_called_once_with(id_=context.id)


class TestNotificationController(TestCase):

    def setUp(self) -> None:
        self.__repository: NotificationRepository = Mock()
        self.__mapper = PinfluencerObjectMapper(logger=logger_factory())
        self.__flexi_updater = FlexiUpdater()
        self.__sut = NotificationController(repository=self.__repository,
                                            mapper=self.__mapper,
                                            flexi_updater=self.__flexi_updater,
                                            logger=logger_factory())

    def test_create(self):
        # arrange
        self.__sut._create = MagicMock()
        context = PinfluencerContext()

        # act
        self.__sut.create(context=context)

        # assert
        self.__sut._create.assert_called_once_with(context=context,
                                                   model=Notification,
                                                   request=NotificationCreateRequestDto,
                                                   response=NotificationResponseDto)