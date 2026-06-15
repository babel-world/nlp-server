from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class ZhTnRequestBody(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
        json_schema_extra={
            "examples": [
                {
                    "text": "明天有62%的概率降雨。等会请在12:05请通知我",
                }
            ]
        },
    )

    text: str = Field(min_length=1, description="Chinese text to normalize (NSW verbalization)")


class ZhTnResponseBody(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
        json_schema_extra={
            "examples": [
                {
                    "text": "明天有百分之六十二的概率降雨等会请在十二点零五分请通知我",
                }
            ]
        },
    )

    text: str = Field(description="Normalized Chinese text with NSW converted to spoken form")
