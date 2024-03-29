from typing import Any
import sys

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import PydanticCustomError, core_schema

if sys.version_info > (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


class CountryAlpha2(str):
    """
    CountryAlpha2 parses country codes in the [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)
    format.

    ```py
    from pydantic import BaseModel

    from pydantic_extra_types.country import CountryAlpha2

    class Product(BaseModel):
        made_in: CountryAlpha2

    product = Product(made_in='ES')
    print(product)
    #> made_in='ES'
    ```
    """

    @classmethod
    def _validate(cls, __input_value: str, _: core_schema.ValidationInfo) -> Self:
        from .subdivision import valid_subdivision_code

        if not valid_subdivision_code(__input_value):
            raise PydanticCustomError("country_alpha2", "Invalid country alpha2 code")
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.AfterValidatorFunctionSchema:
        return core_schema.with_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(to_upper=True),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        json_schema = handler(schema)
        json_schema.update({"pattern": r"^\w{2}$"})
        return json_schema

    @property
    def short_name(self) -> str:
        """The country short name."""
        from .country import get_country_by_code

        return get_country_by_code(self).name
