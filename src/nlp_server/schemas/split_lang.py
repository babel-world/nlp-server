from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

SPLIT_LANG_RESPONSE_EXAMPLE: list[dict[str, str | int]] = [
    {
        "lang": "zh",
        "text": "你喜欢看",
        "index": 0,
        "length": 4,
    },
    {
        "lang": "ja",
        "text": "アニメ",
        "index": 4,
        "length": 3,
    },
    {
        "lang": "zh",
        "text": "吗",
        "index": 7,
        "length": 1,
    },
    {
        "lang": "punctuation",
        "text": "？",
        "index": 8,
        "length": 1,
    },
]


class SplitLangRequestBody(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
        json_schema_extra={
            "examples": [
                {
                    "text": "你喜欢看アニメ吗？",
                }
            ]
        },
    )

    text: str = Field(
        min_length=1,
        description="Single sentence to split by detected language",
    )


class SplitLangSegmentBody(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
    )

    lang: str = Field(
        description="Language tag from split-lang (e.g. zh, ja, en, punctuation, digit)",
    )
    text: str = Field(description="Substring text for this segment")
    index: int = Field(ge=0, description="0-based start offset in the input text")
    length: int = Field(ge=1, description="Character length of this segment")
