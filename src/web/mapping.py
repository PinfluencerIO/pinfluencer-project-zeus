from typing import Union, Optional

from src.crosscutting import PinfluencerObjectMapper, Rule
from src.domain.models import Brand, Value, Category, Influencer, Campaign, AudienceAgeSplit, AudienceAge, \
    AudienceGenderSplit, GenderEnum, AudienceGender
from src.web.views import BrandRequestDto, BrandResponseDto, InfluencerRequestDto, InfluencerResponseDto, \
    CampaignRequestDto, CampaignResponseDto, AudienceAgeViewDto, AudienceGenderViewDto


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

    def __add_audience_age_rules(self):
        self.__mapper.add_rule(_type_from=AudienceAgeViewDto,
                               _type_to=AudienceAgeSplit,
                               field='audience_age_13_to_17_split',
                               expression=self.__map_audience_age_13_to_17_view_to_split)
        self.__mapper.add_rule(_type_from=AudienceAgeViewDto,
                               _type_to=AudienceAgeSplit,
                               field='audience_age_18_to_24_split',
                               expression=self.__map_audience_age_18_to_24_view_to_split)
        self.__mapper.add_rule(_type_from=AudienceAgeViewDto,
                               _type_to=AudienceAgeSplit,
                               field='audience_age_25_to_34_split',
                               expression=self.__map_audience_age_25_to_34_view_to_split)
        self.__mapper.add_rule(_type_from=AudienceAgeViewDto,
                               _type_to=AudienceAgeSplit,
                               field='audience_age_35_to_44_split',
                               expression=self.__map_audience_age_35_to_44_view_to_split)
        self.__mapper.add_rule(_type_from=AudienceAgeViewDto,
                               _type_to=AudienceAgeSplit,
                               field='audience_age_45_to_54_split',
                               expression=self.__map_audience_age_45_to_54_view_to_split)
        self.__mapper.add_rule(_type_from=AudienceAgeViewDto,
                               _type_to=AudienceAgeSplit,
                               field='audience_age_55_to_64_split',
                               expression=self.__map_audience_age_55_to_64_view_to_split)
        self.__mapper.add_rule(_type_from=AudienceAgeViewDto,
                               _type_to=AudienceAgeSplit,
                               field='audience_age_65_plus_split',
                               expression=self.__map_audience_age_65_plus_view_to_split)

        self.__mapper.add_rule(_type_from=AudienceAgeSplit,
                               _type_to=AudienceAgeViewDto,
                               field='audience_ages',
                               expression=self.__map_audience_age_view_to_audience_age_split)

        # TODO: workaround for updating
        self.__mapper.add_rule(_type_from=AudienceAgeViewDto,
                               _type_to=AudienceAgeSplit,
                               field='audience_ages',
                               expression=self.__map_audience_age_split_to_audience_age_view,
                               update=True)

    def __add_audience_gender_rules(self):
        self.__mapper.add_rule(_type_from=AudienceGenderViewDto,
                               _type_to=AudienceGenderSplit,
                               field='audience_male_split',
                               expression=self.__map_audience_male_view_to_split)
        self.__mapper.add_rule(_type_from=AudienceGenderViewDto,
                               _type_to=AudienceGenderSplit,
                               field='audience_female_split',
                               expression=self.__map_audience_female_view_to_split)

        self.__mapper.add_rule(_type_from=AudienceGenderSplit,
                               _type_to=AudienceGenderViewDto,
                               field='audience_genders',
                               expression=self.__map_audience_gender_view_to_audience_gender_split)

        # TODO: workaround for updating
        self.__mapper.add_rule(_type_from=AudienceGenderViewDto,
                               _type_to=AudienceGenderSplit,
                               field='audience_genders',
                               expression=self.__map_audience_gender_split_to_audience_gender_view,
                               update=True)

    def add_rules(self):
        self.__add_brand_rules()
        self.__add_influencer_rules()
        self.__add_campaign_rules()
        self.__add_audience_age_rules()
        self.__add_audience_gender_rules()

    @staticmethod
    def __map_user_values_to_user_view(
            to: Union[BrandRequestDto, BrandResponseDto, InfluencerRequestDto, InfluencerResponseDto],
            _from: Union[Brand, Influencer]):
        to.values = list(map(lambda x: x.value, _from.values))

    @staticmethod
    def __map_user_values_view_to_user(to: Union[Brand, Influencer], _from: Union[
        BrandRequestDto, BrandResponseDto, InfluencerRequestDto, InfluencerResponseDto]):
        to.values = list(map(lambda x: Value(value=x), _from.values))

    @staticmethod
    def __map_user_categories_to_user_view(
            to: Union[BrandRequestDto, BrandResponseDto, InfluencerRequestDto, InfluencerResponseDto],
            _from: Union[Brand, Influencer]):
        to.categories = list(map(lambda x: x.category, _from.categories))

    @staticmethod
    def __map_user_categories_view_to_user(to: Union[Brand, Influencer], _from: Union[
        BrandRequestDto, BrandResponseDto, InfluencerRequestDto, InfluencerResponseDto]):
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

    def __map_audience_male_view_to_split(self,
                                          to: AudienceGenderSplit,
                                          _from: AudienceGenderViewDto):
        if self.__if_gender_in_split(gender=GenderEnum.MALE, audience_split=to):
            list(filter(lambda x: x.gender == GenderEnum.MALE, to.audience_genders))[
                0].split = _from.audience_male_split
        else:
            to.audience_genders.append(AudienceGender(gender=GenderEnum.MALE, split=_from.audience_male_split))

    def __map_audience_female_view_to_split(self,
                                            to: AudienceGenderSplit,
                                            _from: AudienceGenderViewDto):
        if self.__if_gender_in_split(gender=GenderEnum.FEMALE, audience_split=to):
            list(filter(lambda x: x.gender == GenderEnum.FEMALE, to.audience_genders))[
                0].split = _from.audience_female_split
        else:
            to.audience_genders.append(AudienceGender(gender=GenderEnum.FEMALE, split=_from.audience_female_split))

    def __map_audience_age_13_to_17_view_to_split(self,
                                                  to: AudienceAgeSplit,
                                                  _from: AudienceAgeViewDto):
        if self.__if_age_band_in_split(min=13, max=17, audience_split=to):
            list(filter(lambda x: x.min_age == 13 and x.max_age == 17, to.audience_ages))[
                0].split = _from.audience_age_13_to_17_split
        else:
            to.audience_ages.append(AudienceAge(min_age=13, max_age=17, split=_from.audience_age_13_to_17_split))

    def __map_audience_age_18_to_24_view_to_split(self,
                                                  to: AudienceAgeSplit,
                                                  _from: AudienceAgeViewDto):
        if self.__if_age_band_in_split(min=18, max=24, audience_split=to):
            list(filter(lambda x: x.min_age == 18 and x.max_age == 24, to.audience_ages))[
                0].split = _from.audience_age_18_to_24_split
        else:
            to.audience_ages.append(AudienceAge(min_age=18, max_age=24, split=_from.audience_age_18_to_24_split))

    def __map_audience_age_25_to_34_view_to_split(self,
                                                  to: AudienceAgeSplit,
                                                  _from: AudienceAgeViewDto):
        if self.__if_age_band_in_split(min=25, max=34, audience_split=to):
            list(filter(lambda x: x.min_age == 25 and x.max_age == 34, to.audience_ages))[
                0].split = _from.audience_age_25_to_34_split
        else:
            to.audience_ages.append(AudienceAge(min_age=25, max_age=34, split=_from.audience_age_18_to_24_split))

    def __map_audience_age_35_to_44_view_to_split(self,
                                                  to: AudienceAgeSplit,
                                                  _from: AudienceAgeViewDto):
        if self.__if_age_band_in_split(min=35, max=44, audience_split=to):
            list(filter(lambda x: x.min_age == 35 and x.max_age == 44, to.audience_ages))[
                0].split = _from.audience_age_35_to_44_split
        else:
            to.audience_ages.append(AudienceAge(min_age=35, max_age=44, split=_from.audience_age_35_to_44_split))

    def __map_audience_age_45_to_54_view_to_split(self,
                                                  to: AudienceAgeSplit,
                                                  _from: AudienceAgeViewDto):
        if self.__if_age_band_in_split(min=45, max=54, audience_split=to):
            list(filter(lambda x: x.min_age == 45 and x.max_age == 54, to.audience_ages))[
                0].split = _from.audience_age_45_to_54_split
        else:
            to.audience_ages.append(AudienceAge(min_age=45, max_age=54, split=_from.audience_age_45_to_54_split))

    def __map_audience_age_55_to_64_view_to_split(self,
                                                  to: AudienceAgeSplit,
                                                  _from: AudienceAgeViewDto):
        if self.__if_age_band_in_split(min=55, max=64, audience_split=to):
            list(filter(lambda x: x.min_age == 55 and x.max_age == 64, to.audience_ages))[
                0].split = _from.audience_age_55_to_64_split
        else:
            to.audience_ages.append(AudienceAge(min_age=55, max_age=64, split=_from.audience_age_55_to_64_split))

    def __map_audience_age_65_plus_view_to_split(self,
                                                 to: AudienceAgeSplit,
                                                 _from: AudienceAgeViewDto):
        if self.__if_age_band_in_split(min=65, max=None, audience_split=to):
            list(filter(lambda x: x.min_age == 65, to.audience_ages))[0].split = _from.audience_age_65_plus_split
        else:
            to.audience_ages.append(AudienceAge(min_age=65, split=_from.audience_age_65_plus_split))

    def __map_audience_gender_view_to_audience_gender_split(self,
                                                            to: AudienceGenderViewDto,
                                                            _from: AudienceGenderSplit):
        to.audience_male_split = list(filter(
            lambda x: x.gender == GenderEnum.MALE, _from.audience_genders)
        )[0].split

        to.audience_female_split = list(filter(
            lambda x: x.gender == GenderEnum.FEMALE, _from.audience_genders)
        )[0].split

    def __map_audience_gender_split_to_audience_gender_view(self,
                                                            to: AudienceGenderSplit,
                                                            _from: AudienceGenderViewDto):
        if self.__if_gender_in_split(gender=GenderEnum.FEMALE, audience_split=to):
            list(filter(lambda x: x.gender == GenderEnum.FEMALE, to.audience_genders))[
                0].split = _from.audience_female_split
        else:
            to.audience_genders.append(AudienceGender(gender=GenderEnum.FEMALE, split=_from.audience_female_split))

        if self.__if_gender_in_split(gender=GenderEnum.MALE, audience_split=to):
            list(filter(lambda x: x.gender == GenderEnum.MALE, to.audience_genders))[
                0].split = _from.audience_male_split
        else:
            to.audience_genders.append(AudienceGender(gender=GenderEnum.MALE, split=_from.audience_male_split))

    def __map_audience_age_view_to_audience_age_split(self,
                                                      to: AudienceAgeViewDto,
                                                      _from: AudienceAgeSplit):

        to.audience_age_13_to_17_split = list(filter(
            lambda x: x.min_age == 13 and x.max_age == 17, _from.audience_ages)
        )[0].split

        to.audience_age_18_to_24_split = list(filter(
            lambda x: x.min_age == 18 and x.max_age == 24, _from.audience_ages)
        )[0].split

        to.audience_age_25_to_34_split = list(filter(
            lambda x: x.min_age == 25 and x.max_age == 34, _from.audience_ages)
        )[0].split

        to.audience_age_35_to_44_split = list(filter(
            lambda x: x.min_age == 35 and x.max_age == 44, _from.audience_ages)
        )[0].split

        to.audience_age_45_to_54_split = list(filter(
            lambda x: x.min_age == 45 and x.max_age == 54, _from.audience_ages)
        )[0].split

        to.audience_age_55_to_64_split = list(filter(
            lambda x: x.min_age == 55 and x.max_age == 64, _from.audience_ages)
        )[0].split

        to.audience_age_65_plus_split = list(filter(
            lambda x: x.min_age == 65, _from.audience_ages)
        )[0].split

    def __map_audience_age_split_to_audience_age_view(self,
                                                      to: AudienceAgeSplit,
                                                      _from: AudienceAgeViewDto):

        if _from.audience_age_13_to_17_split != None:
            if self.__if_age_band_in_split(min=13, max=17, audience_split=to):
                list(filter(lambda x: x.min_age == 13 and x.max_age == 17, to.audience_ages))[
                    0].split = _from.audience_age_13_to_17_split
            else:
                to.audience_ages.append(AudienceAge(min_age=13, max_age=17, split=_from.audience_age_13_to_17_split))

        if _from.audience_age_18_to_24_split != None:
            if self.__if_age_band_in_split(min=18, max=24, audience_split=to):
                list(filter(lambda x: x.min_age == 18 and x.max_age == 24, to.audience_ages))[
                    0].split = _from.audience_age_18_to_24_split
            else:
                to.audience_ages.append(AudienceAge(min_age=18, max_age=24, split=_from.audience_age_18_to_24_split))

        if _from.audience_age_25_to_34_split != None:
            if self.__if_age_band_in_split(min=25, max=34, audience_split=to):
                list(filter(lambda x: x.min_age == 25 and x.max_age == 34, to.audience_ages))[
                    0].split = _from.audience_age_25_to_34_split
            else:
                to.audience_ages.append(AudienceAge(min_age=25, max_age=34, split=_from.audience_age_18_to_24_split))

        if _from.audience_age_35_to_44_split != None:
            if self.__if_age_band_in_split(min=35, max=44, audience_split=to):
                list(filter(lambda x: x.min_age == 35 and x.max_age == 44, to.audience_ages))[
                    0].split = _from.audience_age_35_to_44_split
            else:
                to.audience_ages.append(AudienceAge(min_age=35, max_age=44, split=_from.audience_age_35_to_44_split))

        if _from.audience_age_45_to_54_split != None:
            if self.__if_age_band_in_split(min=45, max=54, audience_split=to):
                list(filter(lambda x: x.min_age == 45 and x.max_age == 54, to.audience_ages))[
                    0].split = _from.audience_age_45_to_54_split
            else:
                to.audience_ages.append(AudienceAge(min_age=45, max_age=54, split=_from.audience_age_45_to_54_split))

        if _from.audience_age_55_to_64_split != None:
            if self.__if_age_band_in_split(min=55, max=64, audience_split=to):
                list(filter(lambda x: x.min_age == 55 and x.max_age == 64, to.audience_ages))[
                    0].split = _from.audience_age_55_to_64_split
            else:
                to.audience_ages.append(AudienceAge(min_age=55, max_age=64, split=_from.audience_age_55_to_64_split))

        if _from.audience_age_65_plus_split != None:
            if self.__if_age_band_in_split(min=65, max=None, audience_split=to):
                list(filter(lambda x: x.min_age == 65, to.audience_ages))[0].split = _from.audience_age_65_plus_split
            else:
                to.audience_ages.append(AudienceAge(min_age=65, split=_from.audience_age_65_plus_split))

    @staticmethod
    def __if_age_band_in_split(min: int, max: Optional[int], audience_split: AudienceAgeSplit) -> bool:
        if len(list(filter(
                lambda x: x.min_age == min and x.max_age == max, audience_split.audience_ages
        ))) > 0:
            return True
        return False

    @staticmethod
    def __if_gender_in_split(gender: GenderEnum, audience_split: AudienceGenderSplit) -> bool:
        if len(list(filter(
                lambda x: x.gender == gender, audience_split.audience_genders
        ))) > 0:
            return True
        return False
