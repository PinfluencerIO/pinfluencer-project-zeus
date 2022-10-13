from typing import Union

from src.crosscutting import PinfluencerObjectMapper, Rule
from src.domain.models import Brand, Value, Category, Influencer, Campaign
from src.web.views import BrandRequestDto, BrandResponseDto, InfluencerRequestDto, InfluencerResponseDto, \
    CampaignRequestDto, CampaignResponseDto


class MappingRules:

    def __init__(self, mapper: PinfluencerObjectMapper):
        self.__mapper = mapper

    @property
    def rules(self) -> list[Rule]:
        return self.__mapper.rules

    def __add_influencer_rules(self):
        # values
        self.__mapper.add_rule(_type_from=Influencer,
                               _type_to=InfluencerRequestDto,
                               field='values',
                               expression=self.__map_user_values_to_user_view)
        self.__mapper.add_rule(_type_from=InfluencerRequestDto,
                               _type_to=Influencer,
                               field='values',
                               expression=self.__map_user_values_view_to_user)
        self.__mapper.add_rule(_type_from=Influencer,
                               _type_to=InfluencerResponseDto,
                               field='values',
                               expression=self.__map_user_values_to_user_view)
        self.__mapper.add_rule(_type_from=InfluencerResponseDto,
                               _type_to=Influencer,
                               field='values',
                               expression=self.__map_user_values_view_to_user)

        # categories
        self.__mapper.add_rule(_type_from=Influencer,
                               _type_to=InfluencerRequestDto,
                               field='categories',
                               expression=self.__map_user_categories_to_user_view)
        self.__mapper.add_rule(_type_from=InfluencerRequestDto,
                               _type_to=Influencer,
                               field='categories',
                               expression=self.__map_user_categories_view_to_user)
        self.__mapper.add_rule(_type_from=Influencer,
                               _type_to=InfluencerResponseDto,
                               field='categories',
                               expression=self.__map_user_categories_to_user_view)
        self.__mapper.add_rule(_type_from=InfluencerResponseDto,
                               _type_to=Influencer,
                               field='categories',
                               expression=self.__map_user_categories_view_to_user)

    def __add_brand_rules(self):
        # values
        self.__mapper.add_rule(_type_from=Brand,
                               _type_to=BrandRequestDto,
                               field='values',
                               expression=self.__map_user_values_to_user_view)
        self.__mapper.add_rule(_type_from=BrandRequestDto,
                               _type_to=Brand,
                               field='values',
                               expression=self.__map_user_values_view_to_user)
        self.__mapper.add_rule(_type_from=Brand,
                               _type_to=BrandResponseDto,
                               field='values',
                               expression=self.__map_user_values_to_user_view)
        self.__mapper.add_rule(_type_from=BrandResponseDto,
                               _type_to=Brand,
                               field='values',
                               expression=self.__map_user_values_view_to_user)

        # categories
        self.__mapper.add_rule(_type_from=Brand,
                               _type_to=BrandRequestDto,
                               field='categories',
                               expression=self.__map_user_categories_to_user_view)
        self.__mapper.add_rule(_type_from=BrandRequestDto,
                               _type_to=Brand,
                               field='categories',
                               expression=self.__map_user_categories_view_to_user)
        self.__mapper.add_rule(_type_from=Brand,
                               _type_to=BrandResponseDto,
                               field='categories',
                               expression=self.__map_user_categories_to_user_view)
        self.__mapper.add_rule(_type_from=BrandResponseDto,
                               _type_to=Brand,
                               field='categories',
                               expression=self.__map_user_categories_view_to_user)

    def __add_campaign_rules(self):
        # values
        self.__mapper.add_rule(_type_from=Campaign,
                               _type_to=CampaignRequestDto,
                               field='campaign_values',
                               expression=self.__map_campaign_values_to_campaign_view)
        self.__mapper.add_rule(_type_from=CampaignRequestDto,
                               _type_to=Campaign,
                               field='campaign_values',
                               expression=self.__map_campaign_values_view_to_campaign)
        self.__mapper.add_rule(_type_from=Campaign,
                               _type_to=CampaignResponseDto,
                               field='campaign_values',
                               expression=self.__map_campaign_values_to_campaign_view)
        self.__mapper.add_rule(_type_from=CampaignResponseDto,
                               _type_to=Campaign,
                               field='campaign_values',
                               expression=self.__map_campaign_values_view_to_campaign)

        # categories
        self.__mapper.add_rule(_type_from=Campaign,
                               _type_to=CampaignRequestDto,
                               field='campaign_categories',
                               expression=self.__map_campaign_categories_to_campaign_view)
        self.__mapper.add_rule(_type_from=CampaignRequestDto,
                               _type_to=Campaign,
                               field='campaign_categories',
                               expression=self.__map_campaign_categories_view_to_campaign)
        self.__mapper.add_rule(_type_from=Campaign,
                               _type_to=CampaignResponseDto,
                               field='campaign_categories',
                               expression=self.__map_campaign_categories_to_campaign_view)
        self.__mapper.add_rule(_type_from=CampaignResponseDto,
                               _type_to=Campaign,
                               field='campaign_categories',
                               expression=self.__map_campaign_categories_view_to_campaign)

    def add_rules(self):
        self.__add_brand_rules()
        self.__add_influencer_rules()
        self.__add_campaign_rules()

    @staticmethod
    def __map_user_values_to_user_view(to: Union[BrandRequestDto, BrandResponseDto, InfluencerRequestDto, InfluencerResponseDto], _from: Union[Brand, Influencer]):
        to.values = list(map(lambda x: x.value, _from.values))

    @staticmethod
    def __map_user_values_view_to_user(to: Union[Brand, Influencer], _from: Union[BrandRequestDto, BrandResponseDto, InfluencerRequestDto, InfluencerResponseDto]):
        to.values = list(map(lambda x: Value(value=x), _from.values))

    @staticmethod
    def __map_user_categories_to_user_view(to: Union[BrandRequestDto, BrandResponseDto, InfluencerRequestDto, InfluencerResponseDto], _from: Union[Brand, Influencer]):
        to.categories = list(map(lambda x: x.category, _from.categories))

    @staticmethod
    def __map_user_categories_view_to_user(to: Union[Brand, Influencer], _from: Union[BrandRequestDto, BrandResponseDto, InfluencerRequestDto, InfluencerResponseDto]):
        to.categories = list(map(lambda x: Category(category=x), _from.categories))

    @staticmethod
    def __map_campaign_values_to_campaign_view(to: Union[CampaignRequestDto, CampaignResponseDto], _from: Campaign):
        to.campaign_values = list(map(lambda x: x.value, _from.campaign_values))

    @staticmethod
    def __map_campaign_values_view_to_campaign(to: Campaign, _from: Union[CampaignRequestDto, CampaignResponseDto]):
        to.campaign_values = list(map(lambda x: Value(value=x), _from.campaign_values))

    @staticmethod
    def __map_campaign_categories_to_campaign_view(
            to: Union[CampaignRequestDto, CampaignResponseDto],
            _from: Campaign):
        to.campaign_categories = list(map(lambda x: x.category, _from.campaign_categories))

    @staticmethod
    def __map_campaign_categories_view_to_campaign(to: Campaign, _from: Union[CampaignRequestDto, CampaignResponseDto]):
        to.campaign_categories = list(map(lambda x: Category(category=x), _from.campaign_categories))