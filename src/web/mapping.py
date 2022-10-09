from typing import Union

from src.crosscutting import PinfluencerObjectMapper, Rule
from src.domain.models import Brand, Value, ValueEnum
from src.web.views import BrandRequestDto, BrandResponseDto


class MappingRules:

    def __init__(self, mapper: PinfluencerObjectMapper):
        self.__mapper = mapper

    @property
    def rules(self) -> list[Rule]:
        return self.__mapper.rules

    def add_rules(self):
        self.__mapper.add_rule(_type_from=Brand,
                               _type_to=BrandRequestDto,
                               field='values',
                               expression=self.__map_brand_to_brand_view)
        self.__mapper.add_rule(_type_from=BrandRequestDto,
                               _type_to=Brand,
                               field='values',
                               expression=self.__map_brand_view_to_brand)
        self.__mapper.add_rule(_type_from=Brand,
                               _type_to=BrandResponseDto,
                               field='values',
                               expression=self.__map_brand_to_brand_view)
        self.__mapper.add_rule(_type_from=BrandResponseDto,
                               _type_to=Brand,
                               field='values',
                               expression=self.__map_brand_view_to_brand)

    @staticmethod
    def __map_brand_to_brand_view(to: Union[BrandRequestDto, BrandResponseDto], _from: Brand):
        to.values = list(map(lambda x: x.value, _from.values))

    @staticmethod
    def __map_brand_view_to_brand(to: Brand, _from: Union[BrandRequestDto, BrandResponseDto]):
        to.values = list(map(lambda x: Value(value=x), _from.values))
