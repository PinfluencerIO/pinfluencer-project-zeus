from collections import OrderedDict
from unittest import TestCase
from unittest.mock import Mock, MagicMock, call
from uuid import uuid4

from callee import Captor
from ddt import data, ddt

from src._types import AuthUserRepository, BrandRepository, ImageRepository, NotificationRepository, \
    AudienceAgeRepository, InfluencerRepository, AudienceGenderRepository
from src.crosscutting import JsonCamelToSnakeCaseDeserializer, AutoFixture
from src.domain.models import User, ValueEnum, CategoryEnum, AudienceAgeSplit, AudienceGenderSplit, \
    AudienceAge
from src.domain.validation import InfluencerValidator, BrandValidator, ListingValidator
from src.exceptions import NotFoundException
from src.web import PinfluencerContext, PinfluencerResponse
from src.web.error_capsules import AudienceDataAlreadyExistsErrorCapsule, BrandNotFoundErrorCapsule, \
    InfluencerNotFoundErrorCapsule
from src.web.hooks import UserAfterHooks, UserBeforeHooks, BrandAfterHooks, InfluencerAfterHooks, CommonBeforeHooks, \
    InfluencerBeforeHooks, BrandBeforeHooks, ListingBeforeHooks, ListingAfterHooks, CommonAfterHooks, \
    NotificationAfterHooks, NotificationBeforeHooks, AudienceAgeBeforeHooks, AudienceCommonHooks, \
    AudienceGenderBeforeHooks, InfluencerOnBoardingAfterHooks
from src.web.views import ImageRequestDto, BrandResponseDto, BrandRequestDto, ListingResponseDto, \
    NotificationCreateRequestDto
from tests import get_auth_user_event, create_for_auth_user_event, get_brand_id_event, \
    get_influencer_id_event, get_listing_id_event, get_notification_id_event, test_mapper

TEST_S3_URL = "https://pinfluencer-product-images.s3.eu-west-2.amazonaws.com"


class TestCommonAfterHooks(TestCase):

    def setUp(self) -> None:
        self.__sut = CommonAfterHooks()

    def test_map_enum_collection(self):
        # arrange
        context = PinfluencerContext(response=PinfluencerResponse(body=[
            {"values": ValueEnum.SUSTAINABLE},
            {"values": ValueEnum.VALUE7}
        ]))

        # act
        self.__sut.map_enum_collection(context=context,
                                       key="values")

        # assert
        with self.subTest(msg="first value is correct"):
            assert context.response.body[0]["values"] == "SUSTAINABLE"

        # assert
        with self.subTest(msg="first value is correct"):
            assert context.response.body[1]["values"] == "VALUE7"

    def test_map_enum(self):
        # arrange
        context = PinfluencerContext(
            response=PinfluencerResponse(body={"values": ValueEnum.ORGANIC}))

        # act
        self.__sut.map_enum(context=context,
                            key="values")

        # assert
        assert context.response.body["values"] == "ORGANIC"

    def test_map_enums_collection(self):
        # arrange
        context = PinfluencerContext(response=PinfluencerResponse(body=[
            {"values": [ValueEnum.SUSTAINABLE, ValueEnum.ORGANIC]},
            {"values": [ValueEnum.VALUE7, ValueEnum.VALUE6, ValueEnum.RECYCLED]}
        ]))

        # act
        self.__sut.map_enums_collection(context=context,
                                        key="values")

        # assert
        with self.subTest(msg="first value of first entity is correct"):
            assert context.response.body[0]["values"][0] == "SUSTAINABLE"

        # assert
        with self.subTest(msg="second value of first entity is correct"):
            assert context.response.body[0]["values"][1] == "ORGANIC"

        # assert
        with self.subTest(msg="first value of second entity is correct"):
            assert context.response.body[1]["values"][0] == "VALUE7"

        # assert
        with self.subTest(msg="second value of second entity is correct"):
            assert context.response.body[1]["values"][1] == "VALUE6"

        # assert
        with self.subTest(msg="third value of second entity is correct"):
            assert context.response.body[1]["values"][2] == "RECYCLED"

    def test_map_enums(self):
        # arrange
        context = PinfluencerContext(
            response=PinfluencerResponse(body={"values": [ValueEnum.SUSTAINABLE, ValueEnum.ORGANIC]}))

        # act
        self.__sut.map_enums(context=context,
                             key="values")

        # assert
        with self.subTest(msg="first value is correct"):
            assert context.response.body["values"][0] == "SUSTAINABLE"

        # assert
        with self.subTest(msg="second value is correct"):
            assert context.response.body["values"][1] == "ORGANIC"

    def test_set_image_url(self):
        # arrange
        path = "image_path"
        context = PinfluencerContext(response=PinfluencerResponse(body={
            "image": path
        }))

        # act
        self.__sut.set_image_url(context=context,
                                 image_fields=["image"])

        # assert
        assert context.response.body["image"] == f'{TEST_S3_URL}/{path}'

    def test_set_image_url_for_collection(self):
        # arrange
        path = "image_path"
        path2 = "image_path2"
        context = PinfluencerContext(response=PinfluencerResponse(body=[
            {"image": path},
            {"image": path2}
        ]))

        # act
        self.__sut.set_image_url(context=context,
                                 image_fields=["image"],
                                 collection=True)

        # assert
        with self.subTest(msg="first image is tagged with aws s3 image url"):
            assert context.response.body[0]["image"] == f'{TEST_S3_URL}/{path}'

        # assert
        with self.subTest(msg="second image is tagged with aws s3 image url"):
            assert context.response.body[1]["image"] == f'{TEST_S3_URL}/{path2}'

    def test_set_image_url_where_image_is_none(self):
        # arrange
        path = None
        context = PinfluencerContext(response=PinfluencerResponse(body={
            "image": path
        }))

        # act
        self.__sut.set_image_url(context=context,
                                 image_fields=["image"])

        # assert
        assert context.response.body["image"] is None

    def test_save_response_body_to_cache(self):
        # arrange
        body = {
            "field": 1,
            "field2": "another"
        }
        context = PinfluencerContext(response=PinfluencerResponse(body=body))

        # act
        self.__sut.save_response_body_to_cache(context=context,
                                               key="body_1")

        # assert
        body_from_cache = context.cached_values["body_1"]
        self.assertEqual(body_from_cache, body)

    def test_merge_cached_values_to_response(self):
        # arrange
        body = {
            "field": 1,
            "field2": "another"
        }
        body2 = {
            "field3": 2,
            "field4": "another2"
        }
        body3 = {
            "field5": 5,
            "field6": "another5"
        }
        merged_body = {
            "field": 1,
            "field2": "another",
            "field3": 2,
            "field4": "another2"
        }
        context = PinfluencerContext(cached_values=OrderedDict({
            "body_1": body,
            "body_2": body2,
            "body_3": body3
        }), response=PinfluencerResponse(body={}))

        # act
        self.__sut.merge_cached_values_to_response(context=context,
                                                   keys=["body_1", "body_2"])

        # assert
        body = context.response.body
        self.assertEqual(body, merged_body)


@ddt
class TestBrandBeforeHooks(TestCase):

    def setUp(self) -> None:
        self.__common_before_hooks: CommonBeforeHooks = Mock()
        self.__brand_repository: BrandRepository = Mock()
        self.__brand_validator = BrandValidator()
        self.__mapper = test_mapper()
        self.__sut = BrandBeforeHooks(brand_validator=self.__brand_validator,
                                      brand_repository=self.__brand_repository,
                                      common_before_hooks=self.__common_before_hooks,
                                      logger=Mock(),
                                      user_before_hooks=UserBeforeHooks(common_before_hooks=self.__common_before_hooks,
                                                                        logger=Mock()))

    def test_validate_uuid(self):
        # arrange
        id = str(uuid4())
        context = PinfluencerContext(event=get_brand_id_event(brand_id=id),
                                     short_circuit=False)

        # act
        self.__sut.validate_uuid(context=context)

        # assert
        with self.subTest(msg="middleware does not short"):
            assert not context.short_circuit

        # assert
        with self.subTest(msg="id is set"):
            assert context.id == id

    def test_validate_uuid_when_invalid(self):
        # arrange
        context = PinfluencerContext(event=get_brand_id_event(brand_id="boo"),
                                     short_circuit=False,
                                     response=PinfluencerResponse())

        # act
        self.__sut.validate_uuid(context=context)

        # assert
        with self.subTest(msg="middleware shorts"):
            assert context.short_circuit

        # assert
        with self.subTest(msg="response status code is 400"):
            assert context.response.status_code == 400

        # assert
        with self.subTest(msg="response body is empty"):
            assert context.response.body == {}

        # assert
        with self.subTest(msg="id is set to empty string"):
            assert context.id == ""

    @data("aidan.gannon@gmail.com",
          "aidangannon@hotmail.co.uk",
          "something.or.nothing@beansmail.ac.uk")
    def test_validate_brand_when_valid_email(self, email):
        # arrange
        context = PinfluencerContext(body=self.__mapper.map_to_dict_and_ignore_none_fields(
            _from=BrandRequestDto(email=email),
            to=BrandRequestDto),
            response=PinfluencerResponse(), short_circuit=False)

        # act
        self.__sut.validate_brand(context=context)

        # assert
        assert not context.short_circuit

    @data("aidan gannon@gmail.com",
          "aidangannon*hotmail.co.uk",
          "somethingnothing@beansmail.ac.",
          "somethingnothing@beansmail",
          "@",
          "some@",
          "@some",
          "someemail",
          "someemail.com",
          "someemail.com."
          "///@///")
    def test_validate_brand_when_not_valid_email(self, email):
        # arrange
        context = PinfluencerContext(response=PinfluencerResponse(),
                                     short_circuit=False,
                                     body=self.__mapper.map_to_dict_and_ignore_none_fields(
                                         _from=BrandRequestDto(email=email),
                                         to=BrandRequestDto))

        # act
        self.__sut.validate_brand(context=context)

        # assert
        with self.subTest(msg="middleware shorts"):
            assert context.short_circuit == True

        # assert
        with self.subTest(msg="status code is 400"):
            assert context.response.status_code == 400

        # assert
        with self.subTest(msg="response body is empty"):
            assert context.response.body == {}

    @data("http://www.thisis-a-domain.com",
          "https://www.thisis-a-domain.com",
          "https://www.domain.com",
          "https://www.thisis-a-domain.com/nested-path",
          "https://www.thisis-a-domain.com/nested-path/",
          "https://www.thisis-a-domain.com/nested-path/nested-path2",
          "https://www.instagram.com/aidan_gannon_music/",
          "https://stackoverflow.com/questions/11941817/how-to-avoid-runtimeerror-dictionary-changed-size-during-iteration-error",
          "https://docs.aws.amazon.com/code-samples/latest/catalog/python-sqs-message_wrapper.py.html")
    def test_validate_brand_when_valid_email(self, website):
        # arrange
        context = PinfluencerContext(body=self.__mapper.map_to_dict_and_ignore_none_fields(
            _from=BrandRequestDto(website=website),
            to=BrandRequestDto),
            response=PinfluencerResponse(), short_circuit=False)

        # act
        self.__sut.validate_brand(context=context)

        # assert
        assert not context.short_circuit

    @data("www.google.com",
          "beans",
          "http://http://www.www.google.com.com",
          "http://http://www.www.google.com",
          "http://http://www.google.com")
    def test_validate_brand_when_not_valid_website(self, website):
        # arrange
        context = PinfluencerContext(response=PinfluencerResponse(),
                                     short_circuit=False,
                                     body=self.__mapper.map_to_dict_and_ignore_none_fields(
                                         _from=BrandRequestDto(website=website),
                                         to=BrandRequestDto))

        # act
        self.__sut.validate_brand(context=context)

        # assert
        with self.subTest(msg="middleware shorts"):
            assert context.short_circuit == True

    def test_validate_auth_brand(self):
        # arrange
        self.__brand_repository.load_for_auth_user = MagicMock()
        context = PinfluencerContext(auth_user_id="1234",
                                     response=PinfluencerResponse(),
                                     short_circuit=False)

        # act
        self.__sut.validate_auth_brand(context=context)

        # assert
        with self.subTest(msg="repo was called"):
            self.__brand_repository.load_for_auth_user.assert_called_once_with("1234")

        # assert
        with self.subTest(msg="error capsules are empty"):
            self.assertEqual(0, len(context.error_capsule))

    def test_validate_auth_brand_when_not_found(self):
        # arrange
        self.__brand_repository.load_for_auth_user = MagicMock(side_effect=NotFoundException())
        context = PinfluencerContext(auth_user_id="1234",
                                     response=PinfluencerResponse(),
                                     short_circuit=False)

        # act
        self.__sut.validate_auth_brand(context=context)

        # assert
        with self.subTest(msg="error capsule is set"):
            self.assertEqual(1, len(context.error_capsule))
            self.assertEqual(BrandNotFoundErrorCapsule, type(context.error_capsule[0]))

    def test_upload_image(self):
        # arrange
        context = PinfluencerContext(auth_user_id="12345")
        self.__common_before_hooks.upload_image = MagicMock()

        # act
        self.__sut.upload_image(context=context)

        # assert
        with self.subTest(msg="image was uploaded once"):
            self.__common_before_hooks.upload_image.assert_called_once_with(path="brands/12345",
                                                                            context=context,
                                                                            map_list={
                                                                                "logo": "logo",
                                                                                "header-image": "header_image"
                                                                            })

    def test_validate_image_key(self):
        context = PinfluencerContext()
        self.__common_before_hooks.validate_image_path = MagicMock()
        self.__sut.validate_image_key(context=context)

        # assert
        with self.subTest(msg="keys were validated"):
            self.__common_before_hooks.validate_image_path.assert_called_once_with(context=context,
                                                                                   possible_paths=["logo",
                                                                                                   "header-image"])


class TestInfluencerBeforeHooks(TestCase):

    def setUp(self) -> None:
        self.__common_before_hooks: CommonBeforeHooks = Mock()
        self.__influencer_validator = InfluencerValidator()
        self.__repository: InfluencerRepository = Mock()
        self.__user_before_hooks: UserBeforeHooks = Mock()
        self.__sut = InfluencerBeforeHooks(influencer_validator=self.__influencer_validator,
                                           common_before_hooks=self.__common_before_hooks,
                                           logger=Mock(),
                                           influencer_repository=self.__repository,
                                           user_before_hooks=self.__user_before_hooks)

    def test_validate_uuid(self):
        # arrange
        id = str(uuid4())
        context = PinfluencerContext(event=get_influencer_id_event(id=id),
                                     short_circuit=False)

        # act
        self.__sut.validate_uuid(context=context)

        # assert
        assert not context.short_circuit
        assert context.id == id

    def test_validate_uuid_when_invalid(self):
        # arrange
        id = "boo"
        context = PinfluencerContext(event=get_influencer_id_event(id=id),
                                     short_circuit=False,
                                     response=PinfluencerResponse())

        # act
        self.__sut.validate_uuid(context=context)

        # assert
        assert context.short_circuit
        assert context.response.status_code == 400
        assert context.response.body == {}
        assert context.id == ""

    def test_validate_influencer_when_valid(self):
        # arrange
        context = PinfluencerContext(body={
            "bio": "my brand",
            "website": "https://brand.com"
        }, response=PinfluencerResponse(), short_circuit=False)

        # act
        self.__sut.validate_influencer(context=context)

        # assert
        assert not context.short_circuit

    def test_validate_influencer_when_not_valid(self):
        # arrange
        context = PinfluencerContext(body={
            "bio": "this is my brand",
            "website": "invalid website"
        }, response=PinfluencerResponse(), short_circuit=False)

        # act
        self.__sut.validate_influencer(context=context)

        # assert
        assert context.short_circuit == True
        assert context.response.status_code == 400
        assert context.response.body == {}

    def test_upload_image(self):
        # arrange
        context = PinfluencerContext(auth_user_id="12345")
        self.__common_before_hooks.upload_image = MagicMock()

        # act
        self.__sut.upload_image(context=context)

        # assert
        with self.subTest(msg="image was uploaded once"):
            self.__common_before_hooks.upload_image.assert_called_once_with(path="influencers/12345",
                                                                            context=context,
                                                                            map_list={
                                                                                "image": "image"
                                                                            })

    def test_validate_image_key(self):
        context = PinfluencerContext()
        self.__common_before_hooks.validate_image_path = MagicMock()
        self.__sut.validate_image_key(context=context)

        # assert
        with self.subTest(msg="keys were validated"):
            self.__common_before_hooks.validate_image_path.assert_called_once_with(context=context,
                                                                                   possible_paths=["image"])

    def test_validate_auth_influencer(self):
        # arrage
        context = PinfluencerContext(auth_user_id="1234")
        self.__user_before_hooks.validate_owner = MagicMock()

        # act
        self.__sut.validate_auth_influencer(context=context)

        # assert
        captor = Captor()
        self.__user_before_hooks.validate_owner.assert_called_once_with(context=context,
                                                                        repo_method=self.__repository.load_for_auth_user,
                                                                        capsule=captor)
        self.assertEqual(type(captor.arg), InfluencerNotFoundErrorCapsule)


class TestListingBeforeHooks(TestCase):

    def setUp(self) -> None:
        self.__listing_validator = ListingValidator()
        self.__common_before_hooks: CommonBeforeHooks = Mock()
        self.__sut = ListingBeforeHooks(listing_validator=self.__listing_validator,
                                        common_before_hooks=self.__common_before_hooks,
                                        logger=Mock())

    def test_validate_listing_when_valid(self):
        # arrange
        context = PinfluencerContext(body={
            "title": "nocountryforoldmenisthebestfilmfightme"
        }, response=PinfluencerResponse(), short_circuit=False)

        # act
        self.__sut.validate_listing(context=context)

        # assert
        assert not context.short_circuit

    def test_validate_listing_when_not_valid(self):
        # arrange
        context = PinfluencerContext(body={
            "title": "jfjfjfjfjfjfjfjfjfjfjfufhdsaihfdsuiafhduisahfuiewhasnfherawifujdsabvgfiujbhvgefawbhfewafewaihjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjefwaaaaaaaaa"
        }, response=PinfluencerResponse(), short_circuit=False)

        # act
        self.__sut.validate_listing(context=context)

        # assert
        assert context.short_circuit == True
        assert context.response.status_code == 400
        assert context.response.body == {}

    def test_validate_id(self):
        # arrange
        id = str(uuid4())
        context = PinfluencerContext(event=get_listing_id_event(listing_id=id),
                                     short_circuit=False)

        # act
        self.__sut.validate_id(context=context)

        # assert
        assert context.short_circuit == False
        assert context.id == id

    def test_map_categories_and_values(self):
        # arrange
        self.__common_before_hooks.map_enums = MagicMock()
        context = PinfluencerContext()

        # act
        self.__sut.map_categories_and_values(context=context)

        # assert
        self.__common_before_hooks.map_enums.assert_any_call(context=context,
                                                             key="categories",
                                                             enum_value=CategoryEnum)
        self.__common_before_hooks.map_enums.assert_any_call(context=context,
                                                             key="values",
                                                             enum_value=ValueEnum)

    def test_validate_id_when_invalid(self):
        # arrange
        id = "1234567"
        context = PinfluencerContext(event=get_listing_id_event(listing_id=id),
                                     short_circuit=False,
                                     response=PinfluencerResponse())

        # act
        self.__sut.validate_id(context=context)

        # assert
        assert context.short_circuit == True
        assert context.response.status_code == 400
        assert context.response.body == {}

    def test_upload_image(self):
        # arrange
        context = PinfluencerContext(auth_user_id="12345")
        self.__common_before_hooks.upload_image = MagicMock()

        # act
        self.__sut.upload_image(context=context)

        # assert
        with self.subTest(msg="image was uploaded once"):
            self.__common_before_hooks.upload_image.assert_called_once_with(path="listings/12345",
                                                                            context=context,
                                                                            map_list={
                                                                                "product-image": "product_image"
                                                                            })

    def test_validate_image_key(self):
        context = PinfluencerContext()
        self.__common_before_hooks.validate_image_path = MagicMock()
        self.__sut.validate_image_key(context=context)

        # assert
        with self.subTest(msg="keys were validated"):
            self.__common_before_hooks.validate_image_path.assert_called_once_with(context=context,
                                                                                   possible_paths=["product-image"])


@ddt
class TestCommonHooks(TestCase):

    def setUp(self) -> None:
        self.__object_mapper = test_mapper()
        self.__image_repo: ImageRepository = Mock()
        self.__deserializer = JsonCamelToSnakeCaseDeserializer()
        self.__sut = CommonBeforeHooks(deserializer=self.__deserializer,
                                       image_repo=self.__image_repo,
                                       object_mapper=self.__object_mapper,
                                       logger=Mock())

    @data("logo", "header-image")
    def test_validate_image_path_valid(self, image):
        # arrage
        context = PinfluencerContext(event={
            "pathParameters": {
                "image_field": image
            }
        },
            response=PinfluencerResponse(),
            short_circuit=False)

        # act
        self.__sut.validate_image_path(context=context,
                                       possible_paths=["logo", "header-image"])

        # assert
        with self.subTest(msg="response is 200"):
            assert context.response.status_code == 200

        # assert
        with self.subTest(msg="middleware does not short"):
            assert context.short_circuit == False

    @data("logos", "header-images")
    def test_validate_image_path_invalid(self, image):
        # arrage
        context = PinfluencerContext(event={
            "pathParameters": {
                "image_field": image
            }
        },
            response=PinfluencerResponse(),
            short_circuit=False)

        # act
        self.__sut.validate_image_path(context=context,
                                       possible_paths=["logo", "header-image"])

        # assert
        with self.subTest(msg="response is 400"):
            assert context.response.status_code == 400

        # assert
        with self.subTest(msg="middleware shorts"):
            assert context.short_circuit == True

    def test_upload_image(self):
        # arrange
        key = "some/key.png"
        path = "some/path"
        bytes = "bytes"
        context = PinfluencerContext(body={
            "image_bytes": bytes
        },
            event={
                "pathParameters": {
                    "image_field": "logo"
                }
            })
        self.__image_repo.upload = MagicMock(return_value=key)
        map_list = {
            "logo": "logo_"
        }

        # act
        self.__sut.upload_image(path=path, context=context, map_list=map_list)

        # assert
        with self.subTest(msg="image repo was called"):
            self.__image_repo.upload.assert_called_once_with(path=path, image_base64_encoded=bytes)

        image_request: ImageRequestDto = self.__object_mapper.map_from_dict(_from=context.body, to=ImageRequestDto)

        # assert
        with self.subTest(msg="key was added to request body"):
            assert image_request.image_path == key

        with self.subTest(msg="field was added to request body"):
            assert image_request.image_field == map_list[context.event["pathParameters"]['image_field']]

    def test_map_enum(self):
        # arrange
        context = PinfluencerContext(body={"value": "ORGANIC"})

        # act
        self.__sut.map_enum(context=context,
                            key="value",
                            enum_value=ValueEnum)

        # assert
        assert context.body["value"] == ValueEnum.ORGANIC

    def test_map_enum_when_field_doesnt_exist(self):
        # arrange
        context = PinfluencerContext(body={})

        # act/assert
        with self.subTest(msg="does not throw exception"):
            self.__sut.map_enum(context=context,
                                key="value",
                                enum_value=ValueEnum)

    def test_map_enums(self):
        # arrange
        context = PinfluencerContext(body={"values": ["SUSTAINABLE", "ORGANIC"]})

        # act
        self.__sut.map_enums(context=context,
                             key="values",
                             enum_value=ValueEnum)

        # assert
        assert context.body["values"][0] == ValueEnum.SUSTAINABLE
        assert context.body["values"][1] == ValueEnum.ORGANIC

    def test_map_enums_when_field_does_not_exist(self):
        # arrange
        context = PinfluencerContext(body={})

        # act/assert
        with self.subTest(msg="does not throw"):
            self.__sut.map_enums(context=context,
                                 key="values",
                                 enum_value=ValueEnum)

    def test_set_body(self):
        # arrange
        body = {
            "first_name": "aidan",
            "last_name": "aidan",
            "email": "aidanwilliamgannon@gmail.com"
        }
        pinfluencer_context = PinfluencerContext(event=create_for_auth_user_event(auth_id="1234",
                                                                                  payload=body))

        # act
        self.__sut.set_body(context=pinfluencer_context)

        # assert
        assert pinfluencer_context.body == body


class TestBrandAfterHooks(TestCase):

    def setUp(self) -> None:
        self.__auth_user_repository: AuthUserRepository = Mock()
        self.__common_after_hooks: CommonAfterHooks = Mock()
        self.__mapper = test_mapper()
        self.__sut = BrandAfterHooks(auth_user_repository=self.__auth_user_repository,
                                     common_after_common_hooks=self.__common_after_hooks,
                                     mapper=self.__mapper)

    def test_set_brand_claims(self):
        # arrange
        self.__auth_user_repository.update_brand_claims = MagicMock()
        auth_user_id = "1234"
        user: User = AutoFixture().create(dto=User)
        context = PinfluencerContext(response=PinfluencerResponse(),
                                     auth_user_id=auth_user_id,
                                     body=user.__dict__)

        # act
        self.__sut.set_brand_claims(context=context)

        captor = Captor()

        # assert
        with self.subTest(msg="repo was called"):
            self.__auth_user_repository.update_brand_claims.assert_called_once_with(user=captor,
                                                                                    auth_user_id=auth_user_id)

        # assert
        with self.subTest(msg="first name matches"):
            user_payload_arg: User = captor.arg
            assert user_payload_arg.given_name == user.given_name

        # assert
        with self.subTest(msg="last name matches"):
            assert user_payload_arg.family_name == user.family_name

        # assert
        with self.subTest(msg="email matches"):
            assert user_payload_arg.email == user.email

    def test_tag_bucket_url_to_images(self):
        # arrange
        self.__common_after_hooks.set_image_url = MagicMock()
        context = PinfluencerContext()

        # act
        self.__sut.tag_bucket_url_to_images(context=context)

        # assert
        self.__common_after_hooks.set_image_url.assert_called_once_with(context=context,
                                                                        image_fields=["header_image",
                                                                                      "logo"],
                                                                        collection=False)

    def test_tag_bucket_url_to_images_collection(self):
        # arrange
        self.__common_after_hooks.set_image_url = MagicMock()
        context = PinfluencerContext()

        # act
        self.__sut.tag_bucket_url_to_images_collection(context=context)

        # assert
        self.__common_after_hooks.set_image_url.assert_called_once_with(context=context,
                                                                        image_fields=["header_image",
                                                                                      "logo"],
                                                                        collection=True)


class TestInfluencerAfterHooks(TestCase):

    def setUp(self) -> None:
        self.__auth_user_repository: AuthUserRepository = Mock()
        self.__common_after_hooks: CommonAfterHooks = Mock()
        self.__mapper = test_mapper()
        self.__sut = InfluencerAfterHooks(auth_user_repository=self.__auth_user_repository,
                                          common_after_hooks=self.__common_after_hooks,
                                          mapper=self.__mapper)

    def test_set_influencer_claims(self):
        # arrange
        self.__auth_user_repository.update_influencer_claims = MagicMock()
        auth_user_id = "1234"
        user: User = AutoFixture().create(dto=User)
        context = PinfluencerContext(response=PinfluencerResponse(),
                                     auth_user_id=auth_user_id,
                                     body=user.__dict__)

        # act
        self.__sut.set_influencer_claims(context=context)

        # assert
        captor = Captor()
        with self.subTest(msg="repo was called"):
            self.__auth_user_repository.update_influencer_claims.assert_called_once_with(user=captor,
                                                                                         auth_user_id=auth_user_id)

        # assert
        with self.subTest(msg="first name matches"):
            user_payload_arg: User = captor.arg
            assert user_payload_arg.given_name == user.given_name

        # assert
        with self.subTest(msg="last name matches"):
            assert user_payload_arg.family_name == user.family_name

        # assert
        with self.subTest(msg="email matches"):
            assert user_payload_arg.email == user.email

    def test_tag_bucket_url_to_images(self):
        # arrange
        self.__common_after_hooks.set_image_url = MagicMock()
        context = PinfluencerContext()

        # act
        self.__sut.tag_bucket_url_to_images(context=context)

        # assert
        self.__common_after_hooks.set_image_url.assert_called_once_with(context=context,
                                                                        image_fields=["image"],
                                                                        collection=False)

    def test_tag_bucket_url_to_images_collection(self):
        # arrange
        self.__common_after_hooks.set_image_url = MagicMock()
        context = PinfluencerContext()

        # act
        self.__sut.tag_bucket_url_to_images_collection(context=context)

        # assert
        self.__common_after_hooks.set_image_url.assert_called_once_with(context=context,
                                                                        image_fields=["image"],
                                                                        collection=True)


class TestListingAfterHooks(TestCase):

    def setUp(self) -> None:
        self.__common_after_hooks: CommonAfterHooks = Mock()
        self.__mapper = test_mapper()
        self.__sut = ListingAfterHooks(common_after_hooks=self.__common_after_hooks,
                                       mapper=self.__mapper,
                                       repository=Mock())

    def test_tag_bucket_url_to_images(self):
        # arrange
        self.__common_after_hooks.set_image_url = MagicMock()
        context = PinfluencerContext()

        # act
        self.__sut.tag_bucket_url_to_images(context=context)

        # assert
        self.__common_after_hooks.set_image_url.assert_called_once_with(context=context,
                                                                        image_fields=["product_image"],
                                                                        collection=False)

    def test_format_values_and_categories(self):
        # arrange
        self.__common_after_hooks.map_enums = MagicMock()
        context = PinfluencerContext()

        # act
        self.__sut.format_values_and_categories(context=context)

        # assert
        self.__common_after_hooks.map_enums.assert_any_call(context=context, key="categories")
        self.__common_after_hooks.map_enums.assert_any_call(context=context, key="values")

    def test_format_values_and_categories_collection(self):
        # arrange
        self.__common_after_hooks.map_enums_collection = MagicMock()
        context = PinfluencerContext()

        # act
        self.__sut.format_values_and_categories_collection(context=context)

        # assert
        self.__common_after_hooks.map_enums_collection.assert_any_call(context=context, key="categories")
        self.__common_after_hooks.map_enums_collection.assert_any_call(context=context, key="values")

    def test_tag_bucket_url_to_images_collection(self):
        # arrange
        self.__common_after_hooks.set_image_url = MagicMock()
        context = PinfluencerContext()

        # act
        self.__sut.tag_bucket_url_to_images_collection(context=context)

        # assert
        self.__common_after_hooks.set_image_url.assert_called_once_with(context=context,
                                                                        image_fields=["product_image"],
                                                                        collection=True)

    def test_validate_listing_belongs_to_brand(self):
        # arrange
        listing_response: ListingResponseDto = AutoFixture().create(dto=ListingResponseDto, list_limit=5)
        context = PinfluencerContext(auth_user_id=listing_response.brand_auth_user_id,
                                     response=PinfluencerResponse(body=listing_response.__dict__),
                                     short_circuit=False)

        # act
        self.__sut.validate_listing_belongs_to_brand(context=context)

        # assert
        with self.subTest(msg="then mapped response stays the same"):
            assert self.__mapper.map_from_dict(_from=context.response.body, to=ListingResponseDto) == listing_response

        # assert
        with self.subTest(msg="middleware does not short"):
            assert context.short_circuit == False

        # assert
        with self.subTest(msg="response status code is 200"):
            assert context.response.status_code == 200

    def test_validate_listing_belongs_to_brand_when_brand_doesnt_belong(self):
        # arrange
        listing_response: ListingResponseDto = AutoFixture().create(dto=ListingResponseDto, list_limit=5)
        context = PinfluencerContext(auth_user_id="12345",
                                     response=PinfluencerResponse(body=listing_response.__dict__),
                                     short_circuit=False)

        # act
        self.__sut.validate_listing_belongs_to_brand(context=context)

        # assert
        with self.subTest(msg="body is empty"):
            assert context.response.body == {}

        # assert
        with self.subTest(msg="middleware shorts"):
            assert context.short_circuit == True

        # assert
        with self.subTest(msg="response status code is 403"):
            assert context.response.status_code == 403


class TestUserBeforeHooks(TestCase):

    def setUp(self) -> None:
        self.__common_before_hooks: CommonBeforeHooks = Mock()
        self.__sut = UserBeforeHooks(self.__common_before_hooks,
                                     logger=Mock())

    def test_map_categories_and_values(self):
        # arrange
        self.__common_before_hooks.map_enums = MagicMock()
        context = PinfluencerContext()

        # act
        self.__sut.set_categories_and_values(context=context)

        # assert
        self.__common_before_hooks.map_enums.assert_any_call(context=context,
                                                             key="categories",
                                                             enum_value=CategoryEnum)
        self.__common_before_hooks.map_enums.assert_any_call(context=context,
                                                             key="values",
                                                             enum_value=ValueEnum)

    def test_set_auth_user_id(self):
        # arrange
        response = PinfluencerResponse()
        auth_id = "12341"

        # act
        context = PinfluencerContext(response=response, event=get_auth_user_event(auth_id=auth_id))
        self.__sut.set_auth_user_id(context=context)

        # assert
        assert context.auth_user_id == auth_id


class TestUserAfterHooks(TestCase):

    def setUp(self) -> None:
        self.__common_after_hooks: CommonAfterHooks = Mock()
        self.__auth_user_repository: AuthUserRepository = Mock()
        self.__mapper = test_mapper()
        self.__sut = UserAfterHooks(auth_user_repository=self.__auth_user_repository,
                                    common_after_hooks=self.__common_after_hooks,
                                    mapper=self.__mapper)

    def test_tag_auth_user_claims_to_response(self):
        # arrange
        brand = AutoFixture().create(dto=BrandResponseDto, list_limit=5)
        response = PinfluencerResponse(body=brand.__dict__)
        auth_user: User = AutoFixture().create(dto=User)
        self.__auth_user_repository.get_by_id = MagicMock(return_value=auth_user)

        # act
        self.__sut.tag_auth_user_claims_to_response(context=PinfluencerContext(response=response,
                                                                               event={}))

        # assert
        with self.subTest(msg="user matches"):
            assert self.__mapper.map_from_dict(_from=response.body, to=User) == auth_user

        # assert
        with self.subTest(msg="repo was called"):
            self.__auth_user_repository.get_by_id.assert_called_once_with(_id=brand.auth_user_id)

    def test_tag_auth_user_claims_to_response_collection(self):
        # arrange
        self.__sut._generic_claims_tagger = MagicMock()
        users = AutoFixture().create_many(dto=User, ammount=3)
        context = PinfluencerContext(response=PinfluencerResponse(
            body=list(map(lambda x: x.__dict__, users))
        ))

        # act
        self.__sut.tag_auth_user_claims_to_response_collection(context=context)

        # assert
        with self.subTest(msg="generic claims tagger was called"):
            self.__sut._generic_claims_tagger.assert_has_calls(calls=[
                call(entity=users[0].__dict__),
                call(entity=users[1].__dict__),
                call(entity=users[2].__dict__)
            ])

    def test_format_values_and_categories(self):
        # arrange
        context = PinfluencerContext()
        self.__common_after_hooks.map_enums = MagicMock()

        # act
        self.__sut.format_values_and_categories(context=context)

        # assert
        self.__common_after_hooks.map_enums.assert_any_call(context=context,
                                                            key="values")
        self.__common_after_hooks.map_enums.assert_any_call(context=context,
                                                            key="categories")

    def test_format_values_and_categories_collection(self):
        # arrange
        context = PinfluencerContext()
        self.__common_after_hooks.map_enums_collection = MagicMock()

        # act
        self.__sut.format_values_and_categories_collection(context=context)

        # assert
        self.__common_after_hooks.map_enums_collection.assert_any_call(context=context,
                                                                       key="values")
        self.__common_after_hooks.map_enums_collection.assert_any_call(context=context,
                                                                       key="categories")


class TestNotificationAfterHooks(TestCase):

    def setUp(self) -> None:
        self.__repository: NotificationRepository = Mock()
        self.__sut = NotificationAfterHooks(repository=self.__repository)

    def test_save_notification_state(self):
        # arrange
        self.__repository.save = MagicMock()

        # act
        self.__sut.save_state(context=PinfluencerContext())

        # assert
        self.__repository.save.assert_called_once()


class TestNotificationBeforeHooks(TestCase):

    def setUp(self) -> None:
        self.__mapper = test_mapper()
        self.__sut = NotificationBeforeHooks(mapper=self.__mapper,
                                             logger=Mock())

    def test_save_notification_state(self):
        # arrange
        notification = AutoFixture().create(dto=NotificationCreateRequestDto)
        context = PinfluencerContext(body=notification.__dict__, auth_user_id="1234")

        # act
        self.__sut.override_create_fields(context=context)

        body = self.__mapper.map_from_dict(_from=context.body, to=NotificationCreateRequestDto)

        # assert
        with self.subTest(msg="read was overriden"):
            self.assertEqual(body.read, False)

        # assert
        with self.subTest(msg="sender was overriden"):
            self.assertEqual(body.sender_auth_user_id, "1234")

    def test_validate_uuid(self):
        # arrange
        id = str(uuid4())
        context = PinfluencerContext(event=get_notification_id_event(notification_id=id),
                                     short_circuit=False)

        # act
        self.__sut.validate_uuid(context=context)

        # assert
        with self.subTest(msg="middleware does not short"):
            assert not context.short_circuit

        # assert
        with self.subTest(msg="id is set"):
            assert context.id == id

    def test_validate_uuid_when_invalid(self):
        # arrange
        context = PinfluencerContext(event=get_notification_id_event(notification_id="boo"),
                                     short_circuit=False,
                                     response=PinfluencerResponse())

        # act
        self.__sut.validate_uuid(context=context)

        # assert
        with self.subTest(msg="middleware shorts"):
            assert context.short_circuit

        # assert
        with self.subTest(msg="response status code is 400"):
            assert context.response.status_code == 400

        # assert
        with self.subTest(msg="response body is empty"):
            assert context.response.body == {}


class TestAudienceGenderBeforeHooks(TestCase):

    def setUp(self) -> None:
        self.__repository: AudienceGenderRepository = Mock()
        self.__audience_common_hooks: AudienceCommonHooks = Mock()
        self.__sut = AudienceGenderBeforeHooks(repository=self.__repository,
                                               audience_common_hooks=self.__audience_common_hooks)

    def test_check_audience_genders_are_empty(self):
        # arrange
        context = PinfluencerContext()
        self.__audience_common_hooks.check_audience_data_is_empty = MagicMock()

        # act
        self.__sut.check_audience_genders_are_empty(context=context)

        # assert
        captor = Captor()
        with self.subTest(msg="common hooks was called"):
            self.__audience_common_hooks \
                .check_audience_data_is_empty \
                .assert_called_once_with(context=context,
                                         repo_method=self.__repository.load_for_influencer,
                                         audience_splits_getter=captor)

        with self.subTest(msg="audience genders getter returns audience gender"):
            self.assertEqual([], captor.arg(AudienceGenderSplit()))


class TestAudienceAgeBeforeHooks(TestCase):

    def setUp(self) -> None:
        self.__repository: AudienceAgeRepository = Mock()
        self.__sut = AudienceAgeBeforeHooks(repository=self.__repository,
                                            audience_age_common_hooks=AudienceCommonHooks())

    def test_when_audience_data_is_already_populated(self):
        # arrange
        context = PinfluencerContext(auth_user_id="1234")
        self.__repository.load_for_influencer = MagicMock(return_value=AudienceAgeSplit(audience_ages=AutoFixture()
                                                                                        .create_many(dto=AudienceAge,
                                                                                                     ammount=15)))

        # act
        self.__sut.check_audience_ages_are_empty(context=context)

        # assert
        with self.subTest(msg="error capsule is added"):
            self.assertEqual(1, len(context.error_capsule))
            self.assertEqual(AudienceDataAlreadyExistsErrorCapsule, type(context.error_capsule[0]))

    def test_when_audience_data_is_empty(self):
        # arrange
        context = PinfluencerContext(auth_user_id="1234")
        self.__repository.load_for_influencer = MagicMock(return_value=AudienceAgeSplit(audience_ages=[]))

        # act
        self.__sut.check_audience_ages_are_empty(context=context)

        # assert
        with self.subTest(msg="error capsule list is empty"):
            self.assertEqual(0, len(context.error_capsule))


class TestInfluencerOnBoardingAfterHooks(TestCase):

    def setUp(self):
        self.__common_after_hooks: CommonAfterHooks = Mock()
        self.__sut = InfluencerOnBoardingAfterHooks(self.__common_after_hooks)

    def test_cache_audience_age_data(self):
        # arrange
        context = PinfluencerContext()
        self.__common_after_hooks.save_response_body_to_cache = MagicMock()

        # act
        self.__sut.cache_audience_age_data(context=context)

        # assert
        self.__common_after_hooks\
            .save_response_body_to_cache\
            .assert_called_once_with(context=context,
                                     key="audience_age_cache")

    def test_cache_audience_gender_data(self):
        # arrange
        context = PinfluencerContext()
        self.__common_after_hooks.save_response_body_to_cache = MagicMock()

        # act
        self.__sut.cache_audience_gender_data(context=context)

        # assert
        self.__common_after_hooks\
            .save_response_body_to_cache\
            .assert_called_once_with(context=context,
                                     key="audience_gender_cache")

    def test_cache_influencer_data(self):
        # arrange
        context = PinfluencerContext()
        self.__common_after_hooks.save_response_body_to_cache = MagicMock()

        # act
        self.__sut.cache_influencer_data(context=context)

        # assert
        self.__common_after_hooks\
            .save_response_body_to_cache\
            .assert_called_once_with(context=context,
                                     key="influencer_details_cache")

    def test_merge_influencer_cache(self):
        # arrange
        context = PinfluencerContext()
        self.__common_after_hooks.merge_cached_values_to_response = MagicMock()

        # act
        self.__sut.merge_influencer_cache(context=context)

        # assert
        self.__common_after_hooks\
            .merge_cached_values_to_response\
            .assert_called_once_with(context=context,
                                     keys=[
                                         "influencer_details_cache",
                                         "audience_age_cache",
                                         "audience_gender_cache"
                                     ])