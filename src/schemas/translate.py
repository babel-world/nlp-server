from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Literal

LangCode = Literal["zh", "en", "ja"]


class TranslateRequestBody(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    source_lang: LangCode
    target_lang: LangCode
    source_text: str = Field(min_length=1, max_length=2048)


class TranslateResponseBody(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    translated_text: str = Field(min_length=1, max_length=2048)
