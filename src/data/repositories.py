import base64
import io
import os
import uuid
from typing import Callable

import boto3
from botocore.exceptions import ClientError
from filetype import filetype

from src._types import DataManager, ImageRepository, Model, User, ObjectMapperAdapter
from src.data.entities import SqlAlchemyBrandEntity, SqlAlchemyInfluencerEntity, create_mappings, \
    SqlAlchemyCampaignEntity
from src.domain.models import Brand, Influencer, Campaign, CampaignStateEnum
from src.domain.models import User as UserModel
from src.exceptions import AlreadyExistsException, ImageException, NotFoundException


class BaseSqlAlchemyRepository:
    def __init__(self,
                 data_manager: DataManager,
                 resource_entity,
                 object_mapper: ObjectMapperAdapter,
                 resource_dto,
                 image_repository: ImageRepository):
        self._image_repository = image_repository
        self._object_mapper = object_mapper
        self._data_manager = data_manager
        self._resource_entity = resource_entity
        self._resource_dto = resource_dto

        create_mappings(mapper=self._object_mapper)

    def load_collection(self) -> list[Model]:
        return list(map(lambda x: self._object_mapper.map(from_obj=x, to_type=self._resource_dto),
                        self._data_manager.session.query(self._resource_entity).all()))

    def load_by_id(self, id_) -> Model:
        entity = self._data_manager.session.query(self._resource_entity).filter(self._resource_entity.id == id_).first()
        if entity:
            return self._object_mapper.map(from_obj=entity, to_type=self._resource_dto)
        else:
            raise NotFoundException(f'model {id} was not found')

    def _update_image_by_id(self, id: str,
                            image_bytes: str,
                            field_setter: Callable[[str, Model], None]):
        print(f"query: <update_image_by_id> for <{self._resource_dto.__name__}||{id}>")
        model = self._data_manager.session.query(self._resource_entity).filter(
            self._resource_entity.id == id).first()
        if model:
            image = self._image_repository.upload(path=model.id,
                                                  image_base64_encoded=image_bytes)
            print(f'setting entity {self._resource_dto.__name__}|{id} image to {image}')
            field_setter(image, model)
            self._data_manager.session.commit()
            print(
                f'Repository Event: user after image set \n{self._object_mapper.map(from_obj=model, to_type=self._resource_dto).__dict__}')
            first = self._data_manager.session \
                .query(self._resource_entity) \
                .filter(self._resource_entity.id == id) \
                .first()
            return self._object_mapper.map(from_obj=first, to_type=self._resource_dto)
        else:
            raise NotFoundException(f'{self._resource_dto.__name__} {id} could not be found')


class BaseSqlAlchemyUserRepository(BaseSqlAlchemyRepository):
    def __init__(self, data_manager: DataManager,
                 resource_entity,
                 image_repository: ImageRepository,
                 object_mapper: ObjectMapperAdapter,
                 resource_dto):
        super().__init__(data_manager=data_manager,
                         resource_entity=resource_entity,
                         object_mapper=object_mapper,
                         resource_dto=resource_dto,
                         image_repository=image_repository)

    def load_for_auth_user(self, auth_user_id) -> User:
        print(f"QUERY: <load for auth user> ENTITY: {self._resource_entity.__name__}")
        first = self._data_manager.session \
            .query(self._resource_entity) \
            .filter(self._resource_entity.auth_user_id == auth_user_id) \
            .first()
        if first:
            return self._object_mapper.map(from_obj=first, to_type=self._resource_dto)
        raise NotFoundException(f'user {auth_user_id} not found')

    def write_new_for_auth_user(self, auth_user_id, payload) -> User:
        try:
            entity = self.load_for_auth_user(auth_user_id)
            raise AlreadyExistsException(f'{self._resource_entity.__name__}'
                                         f'{entity.id} already associated with {auth_user_id}')
        except NotFoundException:
            try:
                payload.auth_user_id = auth_user_id
                entity = self._object_mapper.map(from_obj=payload, to_type=self._resource_entity)
                self._data_manager.session.add(entity)
                self._data_manager.session.commit()
                return self._object_mapper.map(from_obj=entity, to_type=self._resource_dto)
            except Exception as e:
                print(f'Failed to write_new_{self._resource_entity.__class__.__name__}_for_auth_user {e}')
                self._data_manager.session.rollback()
                raise e

    def _update_image(self, auth_user_id, image_bytes, field_setter: Callable[[str, Model], None]):
        user = self._data_manager.session.query(self._resource_entity).filter(
            self._resource_entity.auth_user_id == auth_user_id).first()
        if user:
            image = self._image_repository.upload(path=user.id,
                                                  image_base64_encoded=image_bytes)
            print(f'setting user {auth_user_id} image to {image}')
            field_setter(image, user)
            self._data_manager.session.commit()
            print(
                f'Repository Event: user after image set \n{self._object_mapper.map(from_obj=user, to_type=self._resource_dto).__dict__}')
            first = self._data_manager.session \
                .query(self._resource_entity) \
                .filter(self._resource_entity.auth_user_id == auth_user_id) \
                .first()
            return self._object_mapper.map(from_obj=first, to_type=self._resource_dto)
        else:
            raise NotFoundException(f'brand {auth_user_id} could not be found')


class SqlAlchemyBrandRepository(BaseSqlAlchemyUserRepository):
    def __init__(self,
                 data_manager: DataManager,
                 image_repository: ImageRepository,
                 object_mapper: ObjectMapperAdapter):
        super().__init__(data_manager=data_manager,
                         resource_entity=SqlAlchemyBrandEntity,
                         image_repository=image_repository,
                         object_mapper=object_mapper,
                         resource_dto=Brand)

    def update_for_auth_user(self, auth_user_id, payload: Brand) -> Brand:
        entity = self._data_manager.session.query(self._resource_entity).filter(
            self._resource_entity.auth_user_id == auth_user_id).first()
        if entity:
            entity.brand_name = payload.brand_name
            entity.brand_description = payload.brand_description
            entity.insta_handle = payload.insta_handle
            entity.values = payload.values
            entity.categories = payload.categories
            entity.website = payload.website
            self._data_manager.session.commit()
            return self._object_mapper.map(from_obj=entity, to_type=self._resource_dto)
        else:
            raise NotFoundException(f'brand {auth_user_id} not found')

    def update_logo_for_auth_user(self, auth_user_id, image_bytes) -> Brand:
        return self._update_image(auth_user_id=auth_user_id,
                                  image_bytes=image_bytes,
                                  field_setter=self.__logo_setter)

    def update_header_image_for_auth_user(self, auth_user_id, image_bytes) -> Brand:
        return self._update_image(auth_user_id=auth_user_id,
                                  image_bytes=image_bytes,
                                  field_setter=self.__header_image_setter)

    @staticmethod
    def __logo_setter(logo, brand):
        brand.logo = logo

    @staticmethod
    def __header_image_setter(header_image, brand):
        brand.header_image = header_image


class SqlAlchemyInfluencerRepository(BaseSqlAlchemyUserRepository):
    def __init__(self,
                 data_manager: DataManager,
                 image_repository: ImageRepository,
                 object_mapper: ObjectMapperAdapter):
        super().__init__(data_manager=data_manager,
                         resource_entity=SqlAlchemyInfluencerEntity,
                         image_repository=image_repository,
                         object_mapper=object_mapper,
                         resource_dto=Influencer)

    def update_for_auth_user(self, auth_user_id: str, payload: Influencer) -> Influencer:
        entity: SqlAlchemyInfluencerEntity = self._data_manager.session \
            .query(self._resource_entity) \
            .filter(self._resource_entity.auth_user_id == auth_user_id) \
            .first()
        if entity:
            entity.values = payload.values
            entity.categories = payload.categories
            entity.bio = payload.bio
            entity.website = payload.website
            entity.insta_handle = payload.insta_handle
            entity.audience_male_split = payload.audience_male_split
            entity.audience_female_split = payload.audience_female_split
            entity.audience_age_13_to_17_split = payload.audience_age_13_to_17_split
            entity.audience_age_18_to_24_split = payload.audience_age_18_to_24_split
            entity.audience_age_25_to_34_split = payload.audience_age_25_to_34_split
            entity.audience_age_35_to_44_split = payload.audience_age_35_to_44_split
            entity.audience_age_45_to_54_split = payload.audience_age_45_to_54_split
            entity.audience_age_55_to_64_split = payload.audience_age_55_to_64_split
            entity.audience_age_65_plus_split = payload.audience_age_65_plus_split
            entity.address = payload.address
            self._data_manager.session.commit()
            return self._object_mapper.map(from_obj=entity, to_type=Influencer)
        raise NotFoundException(f"influencer auth_user_id:<{auth_user_id}> not found")

    def update_image_for_auth_user(self, auth_user_id: str, image_bytes: str) -> Influencer:
        return self._update_image(auth_user_id=auth_user_id,
                                  image_bytes=image_bytes,
                                  field_setter=self.__header_image_setter)

    @staticmethod
    def __header_image_setter(profile_image, influencer):
        influencer.image = profile_image


class SqlAlchemyCampaignRepository(BaseSqlAlchemyRepository):

    def __init__(self, data_manager: DataManager,
                 object_mapper: ObjectMapperAdapter,
                 image_repository: ImageRepository):
        super().__init__(data_manager,
                         SqlAlchemyCampaignEntity,
                         object_mapper,
                         Campaign,
                         image_repository=image_repository)

    def write_new_for_brand(self, payload: Campaign,
                            auth_user_id: str) -> Campaign:
        brand = self._data_manager \
            .session \
            .query(SqlAlchemyBrandEntity) \
            .filter(SqlAlchemyBrandEntity.auth_user_id == auth_user_id) \
            .first()
        if brand:
            payload.brand_id = brand.id
            campaign_entity = self \
                ._object_mapper \
                .map(from_obj=payload, to_type=SqlAlchemyCampaignEntity)
            self._data_manager.session.add(campaign_entity)
            self._data_manager.session.commit()
            return payload
        else:
            error_message = f"brand <{auth_user_id}> not found"
            print(error_message)
            raise NotFoundException(error_message)

    def load_for_auth_brand(self, auth_user_id: str) -> list[Campaign]:
        brand = self._data_manager \
            .session \
            .query(SqlAlchemyBrandEntity) \
            .filter(SqlAlchemyBrandEntity.auth_user_id == auth_user_id) \
            .first()
        if brand != None:
            campaigns = self._data_manager \
                .session \
                .query(SqlAlchemyCampaignEntity) \
                .filter(SqlAlchemyCampaignEntity.brand_id == brand.id) \
                .all()
            return list(map(lambda x: self._object_mapper.map(from_obj=x, to_type=Campaign), campaigns))
        else:
            raise NotFoundException("brand not found")

    def update_product_image1(self, id: str, image_bytes: str) -> Campaign:
        return self._update_image_by_id(id=id,
                                        image_bytes=image_bytes,
                                        field_setter=self.__product_image1_setter)

    def update_product_image2(self, id: str, image_bytes: str) -> Campaign:
        return self._update_image_by_id(id=id,
                                        image_bytes=image_bytes,
                                        field_setter=self.__product_image2_setter)

    def update_product_image3(self, id: str, image_bytes: str) -> Campaign:
        return self._update_image_by_id(id=id,
                                        image_bytes=image_bytes,
                                        field_setter=self.__product_image3_setter)

    @staticmethod
    def __product_image1_setter(product_image1, campaign):
        campaign.product_image1 = product_image1

    @staticmethod
    def __product_image2_setter(product_image2, campaign):
        campaign.product_image2 = product_image2

    @staticmethod
    def __product_image3_setter(product_image3, campaign):
        campaign.product_image3 = product_image3

    def update_campaign(self, _id: str, payload: Campaign) -> Campaign:
        campaign: SqlAlchemyCampaignEntity = self._data_manager\
            .session\
            .query(SqlAlchemyCampaignEntity)\
            .filter(SqlAlchemyCampaignEntity.id == _id)\
            .first()
        if campaign != None:
            campaign.campaign_hashtag = payload.campaign_hashtag
            campaign.campaign_categories = payload.campaign_categories
            campaign.product_description = payload.product_description
            campaign.product_title = payload.product_title
            campaign.campaign_discount_code = payload.campaign_discount_code
            campaign.objective = payload.objective
            campaign.campaign_title = payload.campaign_title
            campaign.campaign_description = payload.campaign_description
            campaign.success_description = payload.success_description
            campaign.campaign_values = payload.campaign_values
            campaign.campaign_product_link = payload.campaign_product_link
            self._data_manager\
                .session\
                .commit()
            return self._object_mapper.map(from_obj=campaign, to_type=Campaign)
        else:
            raise NotFoundException(f"{self._resource_dto.__name__}||{_id} not found")

    def update_campaign_state(self, _id: str, payload: CampaignStateEnum) -> Campaign:
        campaign: SqlAlchemyCampaignEntity = self._data_manager\
            .session\
            .query(SqlAlchemyCampaignEntity)\
            .filter(SqlAlchemyCampaignEntity.id == _id)\
            .first()
        if campaign is not None:
            campaign.campaign_state = payload
            self._data_manager.session.commit()
            return self._object_mapper.map(from_obj=campaign, to_type=Campaign)
        else:
            raise NotFoundException(f"cannot find campaign {_id}")


class S3ImageRepository:

    def __init__(self):
        self.__bucket_name = 'pinfluencer-product-images'
        self.__s3_client = boto3.client('s3')

    def upload(self, path, image_base64_encoded):
        print(f"uploading image to S3 repo {image_base64_encoded}")
        image = base64.b64decode(image_base64_encoded)
        print(f"uploading image to S3 repo bytes64 encoded {image}")
        f = io.BytesIO(image)
        print(f"bytesIO file {f}")
        file_type = filetype.get_type(ext='jpg')
        try:
            file_type = filetype.guess(f)
        except Exception:
            ...
        print(f'image uploading to {path}/ of {file_type}')
        if file_type is not None:
            print(f"file type {file_type}")
            mime = file_type.MIME
        else:
            mime = 'image/jpg'
        image_id = str(uuid.uuid4())
        file = f'{image_id}.{file_type.EXTENSION}'
        print(f'image {file}')
        key = f'{path}/{file}'
        print(f'key {key}')
        try:
            self.__s3_client.put_object(Bucket=self.__bucket_name,
                                        Key=key, Body=image,
                                        ContentType=mime,
                                        Tagging='public=yes')
            return key
        except ClientError:
            raise ImageException


class CognitoAuthService:

    def __init__(self):
        print(f"user pool id: {os.environ['USER_POOL_ID']}")
        self.__client = boto3.client('cognito-idp')

    def update_user_claims(self, username: str, attributes: list[dict]) -> None:
        self.__client.admin_update_user_attributes(
            UserPoolId=os.environ["USER_POOL_ID"],
            Username=username,
            UserAttributes=attributes
        )

    def get_user(self, username: str) -> dict:
        return self.__client.admin_get_user(
            UserPoolId=os.environ["USER_POOL_ID"],
            Username=username
        )


class CognitoAuthUserRepository:

    def __init__(self, auth_service: CognitoAuthService):
        self.__auth_service = auth_service

    def get_by_id(self, _id: str) -> User:
        auth_user = self.__auth_service.get_user(username=_id)
        first_name = self.__get_cognito_attribute(user=auth_user,
                                                  attribute_name='given_name')
        last_name = self.__get_cognito_attribute(user=auth_user,
                                                 attribute_name='family_name')
        email = self.__get_cognito_attribute(user=auth_user,
                                             attribute_name='email')
        return UserModel(first_name=first_name,
                         last_name=last_name,
                         email=email)

    def __get_cognito_attribute(self, user: dict, attribute_name: str) -> str:
        return next(filter(lambda x: x['Name'] == attribute_name, user['UserAttributes']))['Value']

    def update_brand_claims(self, user: Brand):
        self.__update_user_claims(user=user, type='brand')

    def update_influencer_claims(self, user: Influencer):
        self.__update_user_claims(user=user, type='influencer')

    def __update_user_claims(self, user: User, type: str):
        self.__auth_service.update_user_claims(username=user.auth_user_id, attributes=[
            {
                'Name': 'custom:usertype',
                'Value': type
            },
            {
                'Name': 'email',
                'Value': user.email
            },
            {
                'Name': 'family_name',
                'Value': user.last_name
            },
            {
                'Name': 'given_name',
                'Value': user.first_name
            }
        ])
