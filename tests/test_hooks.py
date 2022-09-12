from unittest import TestCase
from unittest.mock import Mock, MagicMock, call
from uuid import uuid4

from callee import Captor

from src._types import AuthUserRepository, BrandRepository
from src.crosscutting import JsonCamelToSnakeCaseDeserializer
from src.domain.models import User, Brand, Influencer, ValueEnum, CategoryEnum, CampaignStateEnum
from src.domain.validation import InfluencerValidator, BrandValidator, CampaignValidator
from src.exceptions import NotFoundException
from src.web import PinfluencerContext, PinfluencerResponse
from src.web.hooks import UserAfterHooks, UserBeforeHooks, BrandAfterHooks, InfluencerAfterHooks, CommonBeforeHooks, \
    InfluencerBeforeHooks, BrandBeforeHooks, CampaignBeforeHooks, CampaignAfterHooks, CommonAfterHooks
from tests import brand_dto_generator, RepoEnum, get_auth_user_event, create_for_auth_user_event, get_brand_id_event, \
    get_influencer_id_event, get_campaign_id_event

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
        assert context.response.body[0]["values"] == "SUSTAINABLE"
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
        assert context.response.body[0]["values"][0] == "SUSTAINABLE"
        assert context.response.body[0]["values"][1] == "ORGANIC"
        assert context.response.body[1]["values"][0] == "VALUE7"
        assert context.response.body[1]["values"][1] == "VALUE6"
        assert context.response.body[1]["values"][2] == "RECYCLED"

    def test_map_enums(self):
        # arrange
        context = PinfluencerContext(
            response=PinfluencerResponse(body={"values": [ValueEnum.SUSTAINABLE, ValueEnum.ORGANIC]}))

        # act
        self.__sut.map_enums(context=context,
                             key="values")

        # assert
        assert context.response.body["values"][0] == "SUSTAINABLE"
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
        assert context.response.body[0]["image"] == f'{TEST_S3_URL}/{path}'
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


class TestBrandBeforeHooks(TestCase):

    def setUp(self) -> None:
        self.__brand_repository: BrandRepository = Mock()
        self.__brand_validator = BrandValidator()
        self.__sut = BrandBeforeHooks(brand_validator=self.__brand_validator,
                                      brand_repository=self.__brand_repository)

    def test_validate_uuid(self):
        # arrange
        id = str(uuid4())
        context = PinfluencerContext(event=get_brand_id_event(brand_id=id),
                                     short_circuit=False)

        # act
        self.__sut.validate_uuid(context=context)

        # assert
        assert not context.short_circuit
        assert context.id == id

    def test_validate_uuid_when_invalid(self):
        # arrange
        context = PinfluencerContext(event=get_brand_id_event(brand_id="boo"),
                                     short_circuit=False,
                                     response=PinfluencerResponse())

        # act
        self.__sut.validate_uuid(context=context)

        # assert
        assert context.short_circuit
        assert context.response.status_code == 400
        assert context.response.body == {}
        assert context.id == ""

    def test_validate_brand_when_valid(self):
        # arrange
        context = PinfluencerContext(body={
            "brand_name": "my brand",
            "brand_description": "this is my brand",
            "website": "https://brand.com"
        }, response=PinfluencerResponse(), short_circuit=False)

        # act
        self.__sut.validate_brand(context=context)

        # assert
        assert not context.short_circuit

    def test_validate_brand_when_not_valid(self):
        # arrange
        context = PinfluencerContext(body={
            "brand_name": "my brand",
            "brand_description": "this is my brand",
            "website": "invalid website"
        }, response=PinfluencerResponse(), short_circuit=False)

        # act
        self.__sut.validate_brand(context=context)

        # assert
        assert context.short_circuit == True
        assert context.response.status_code == 400
        assert context.response.body == {}

    def test_validate_auth_brand(self):
        # arrange
        self.__brand_repository.load_for_auth_user = MagicMock()
        context = PinfluencerContext(auth_user_id="1234",
                                     response=PinfluencerResponse(),
                                     short_circuit=False)

        # act
        self.__sut.validate_auth_brand(context=context)

        # assert
        self.__brand_repository.load_for_auth_user.assert_called_once_with(auth_user_id="1234")
        assert context.short_circuit == False

    def test_validate_auth_brand_when_not_found(self):
        # arrange
        self.__brand_repository.load_for_auth_user = MagicMock(side_effect=NotFoundException())
        context = PinfluencerContext(auth_user_id="1234",
                                     response=PinfluencerResponse(),
                                     short_circuit=False)

        # act
        self.__sut.validate_auth_brand(context=context)

        # assert
        assert context.short_circuit == True
        assert context.response.body == {}
        assert context.response.status_code == 404


class TestInfluencerBeforeHooks(TestCase):

    def setUp(self) -> None:
        self.__influencer_validator = InfluencerValidator()
        self.__sut = InfluencerBeforeHooks(influencer_validator=self.__influencer_validator)

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


class TestCampaignBeforeHooks(TestCase):

    def setUp(self) -> None:
        self.__campaign_validator = CampaignValidator()
        self.__common_before_hooks: CommonBeforeHooks = Mock()
        self.__sut = CampaignBeforeHooks(campaign_validator=self.__campaign_validator,
                                         common_before_hooks=self.__common_before_hooks)

    def test_validate_campaign_when_valid(self):
        # arrange
        context = PinfluencerContext(body={
            "campaign_hashtag": "nocountryforoldmenisthebestfilmfightme"
        }, response=PinfluencerResponse(), short_circuit=False)

        # act
        self.__sut.validate_campaign(context=context)

        # assert
        assert not context.short_circuit

    def test_validate_campaign_when_not_valid(self):
        # arrange
        context = PinfluencerContext(body={
            "campaign_hashtag": "jfjfjfjfjfjfjfjfjfjfjfufhdsaihfdsuiafhduisahfuiewhasnfherawifujdsabvgfiujbhvgefawbhfewafewaihjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjefwaaaaaaaaa"
        }, response=PinfluencerResponse(), short_circuit=False)

        # act
        self.__sut.validate_campaign(context=context)

        # assert
        assert context.short_circuit == True
        assert context.response.status_code == 400
        assert context.response.body == {}

    def test_validate_id(self):
        # arrange
        id = str(uuid4())
        context = PinfluencerContext(event=get_campaign_id_event(campaign_id=id),
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
        self.__sut.map_campaign_categories_and_values(context=context)

        # assert
        self.__common_before_hooks.map_enums.assert_any_call(context=context,
                                                             key="campaign_categories",
                                                             enum_value=CategoryEnum)
        self.__common_before_hooks.map_enums.assert_any_call(context=context,
                                                             key="campaign_values",
                                                             enum_value=ValueEnum)

    def test_map_state(self):
        # arrange
        self.__common_before_hooks.map_enum = MagicMock()
        context = PinfluencerContext()

        # act
        self.__sut.map_campaign_state(context=context)

        # assert
        self.__common_before_hooks.map_enum.assert_any_call(context=context,
                                                             key="campaign_state",
                                                             enum_value=CampaignStateEnum)

    def test_validate_id_when_invalid(self):
        # arrange
        id = "1234567"
        context = PinfluencerContext(event=get_campaign_id_event(campaign_id=id),
                                     short_circuit=False,
                                     response=PinfluencerResponse())

        # act
        self.__sut.validate_id(context=context)

        # assert
        assert context.short_circuit == True
        assert context.response.status_code == 400
        assert context.response.body == {}


class TestCommonHooks(TestCase):

    def setUp(self) -> None:
        self.__deserializer = JsonCamelToSnakeCaseDeserializer()
        self.__sut = CommonBeforeHooks(deserializer=self.__deserializer)

    def test_map_enum(self):
        # arrange
        context = PinfluencerContext(body={"value": "ORGANIC"})

        # act
        self.__sut.map_enum(context=context,
                            key="value",
                            enum_value=ValueEnum)

        # assert
        assert context.body["value"] == ValueEnum.ORGANIC

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
        self.__sut = BrandAfterHooks(auth_user_repository=self.__auth_user_repository,
                                     common_after_common_hooks=self.__common_after_hooks)

    def test_set_brand_claims(self):
        # arrange
        self.__auth_user_repository.update_brand_claims = MagicMock()
        auth_user_id = "12341"
        first_name = "aidan"
        last_name = "gannon"
        email = "aidanwilliamgannon@gmail.com"
        context = PinfluencerContext(response=PinfluencerResponse(),
                                     auth_user_id=auth_user_id,
                                     body={
                                         "first_name": first_name,
                                         "last_name": last_name,
                                         "email": email
                                     })

        # act
        self.__sut.set_brand_claims(context=context)

        # assert
        captor = Captor()
        self.__auth_user_repository.update_brand_claims.assert_called_once_with(user=captor)
        user_payload_arg: Brand = captor.arg
        assert user_payload_arg.first_name == first_name
        assert user_payload_arg.last_name == last_name
        assert user_payload_arg.email == email
        assert user_payload_arg.auth_user_id == auth_user_id

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
        self.__sut = InfluencerAfterHooks(auth_user_repository=self.__auth_user_repository,
                                          common_after_hooks=self.__common_after_hooks)

    def test_set_brand_claims(self):
        # arrange
        self.__auth_user_repository.update_influencer_claims = MagicMock()
        auth_user_id = "12341"
        first_name = "aidan"
        last_name = "gannon"
        email = "aidanwilliamgannon@gmail.com"
        context = PinfluencerContext(response=PinfluencerResponse(),
                                     auth_user_id=auth_user_id,
                                     body={
                                         "first_name": first_name,
                                         "last_name": last_name,
                                         "email": email
                                     })

        # act
        self.__sut.set_influencer_claims(context=context)

        # assert
        captor = Captor()
        self.__auth_user_repository.update_influencer_claims.assert_called_once_with(user=captor)
        user_payload_arg: Influencer = captor.arg
        assert user_payload_arg.first_name == first_name
        assert user_payload_arg.last_name == last_name
        assert user_payload_arg.email == email
        assert user_payload_arg.auth_user_id == auth_user_id

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


class TestCampaignAfterHooks(TestCase):

    def setUp(self) -> None:
        self.__common_after_hooks: CommonAfterHooks = Mock()
        self.__sut = CampaignAfterHooks(common_after_hooks=self.__common_after_hooks)

    def test_tag_bucket_url_to_images(self):
        # arrange
        self.__common_after_hooks.set_image_url = MagicMock()
        context = PinfluencerContext()

        # act
        self.__sut.tag_bucket_url_to_images(context=context)

        # assert
        self.__common_after_hooks.set_image_url.assert_called_once_with(context=context,
                                                                        image_fields=["product_image1",
                                                                                      "product_image2",
                                                                                      "product_image3"],
                                                                        collection=False)

    def test_format_values_and_categories(self):
        # arrange
        self.__common_after_hooks.map_enums = MagicMock()
        context = PinfluencerContext()

        # act
        self.__sut.format_values_and_categories(context=context)

        # assert
        self.__common_after_hooks.map_enums.assert_any_call(context=context, key="campaign_categories")
        self.__common_after_hooks.map_enums.assert_any_call(context=context, key="campaign_values")

    def test_format_values_and_categories_collection(self):
        # arrange
        self.__common_after_hooks.map_enums_collection = MagicMock()
        context = PinfluencerContext()

        # act
        self.__sut.format_values_and_categories_collection(context=context)

        # assert
        self.__common_after_hooks.map_enums_collection.assert_any_call(context=context, key="campaign_categories")
        self.__common_after_hooks.map_enums_collection.assert_any_call(context=context, key="campaign_values")

    def test_tag_bucket_url_to_images_collection(self):
        # arrange
        self.__common_after_hooks.set_image_url = MagicMock()
        context = PinfluencerContext()

        # act
        self.__sut.tag_bucket_url_to_images_collection(context=context)

        # assert
        self.__common_after_hooks.set_image_url.assert_called_once_with(context=context,
                                                                        image_fields=["product_image1",
                                                                                      "product_image2",
                                                                                      "product_image3"],
                                                                        collection=True)

    def test_format_campaign_state(self):
        # arrange
        context = PinfluencerContext()
        self.__common_after_hooks.map_enum = MagicMock()

        # act
        self.__sut.format_campaign_state(context=context)

        # assert
        self.__common_after_hooks.map_enum(context=context,
                                           key="campaign_state")

    def test_format_campaign_state_collection(self):
        # arrange
        context = PinfluencerContext()
        self.__common_after_hooks.map_enum_collection = MagicMock()

        # act
        self.__sut.format_campaign_state_collection(context=context)

        # assert
        self.__common_after_hooks.map_enums(context=context,
                                            key="campaign_state")


class TestUserBeforeHooks(TestCase):

    def setUp(self) -> None:
        self.__common_before_hooks: CommonBeforeHooks = Mock()
        self.__sut = UserBeforeHooks(self.__common_before_hooks)

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
        self.__sut = UserAfterHooks(auth_user_repository=self.__auth_user_repository,
                                    common_after_hooks=self.__common_after_hooks)

    def test_tag_auth_user_claims_to_response(self):
        # arrange
        brand = brand_dto_generator(num=1, repo=RepoEnum.STD_REPO)
        response = PinfluencerResponse(body=brand.__dict__)
        auth_user = User(first_name="cognito_first_name",
                         last_name="cognito_last_name",
                         email="cognito_email")
        self.__auth_user_repository.get_by_id = MagicMock(return_value=auth_user)

        # act
        self.__sut.tag_auth_user_claims_to_response(context=PinfluencerContext(response=response,
                                                                               event={}))

        # assert
        assert response.body["first_name"] == auth_user.first_name
        assert response.body["last_name"] == auth_user.last_name
        assert response.body["email"] == auth_user.email
        self.__auth_user_repository.get_by_id.assert_called_once_with(_id=brand.auth_user_id)

    def test_tag_auth_user_claims_to_response_collection(self):
        # arrange
        users = [
            User(first_name="cognito_first_name1",
                 last_name="cognito_last_name1",
                 email="cognito_email1"),
            User(first_name="cognito_first_name2",
                 last_name="cognito_last_name2",
                 email="cognito_email2"),
            User(first_name="cognito_first_name3",
                 last_name="cognito_last_name3",
                 email="cognito_email3")
        ]
        brands = [
            brand_dto_generator(num=1).__dict__,
            brand_dto_generator(num=2).__dict__,
            brand_dto_generator(num=3).__dict__
        ]
        self.__auth_user_repository.get_by_id = MagicMock(side_effect=users)
        response = PinfluencerResponse(body=brands)

        # act
        self.__sut.tag_auth_user_claims_to_response_collection(context=PinfluencerContext(response=response,
                                                                                          event={}))

        # assert
        assert response.body[0]["first_name"] == users[0].first_name
        assert response.body[0]["last_name"] == users[0].last_name
        assert response.body[0]["email"] == users[0].email

        assert response.body[1]["first_name"] == users[1].first_name
        assert response.body[1]["last_name"] == users[1].last_name
        assert response.body[1]["email"] == users[1].email

        assert response.body[2]["first_name"] == users[2].first_name
        assert response.body[2]["last_name"] == users[2].last_name
        assert response.body[2]["email"] == users[2].email

        self.__auth_user_repository.get_by_id.assert_has_calls(calls=[
            call(_id=brands[0]["auth_user_id"]),
            call(_id=brands[1]["auth_user_id"]),
            call(_id=brands[2]["auth_user_id"])
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
