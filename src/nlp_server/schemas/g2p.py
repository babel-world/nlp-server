from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

JaG2pMode = Literal["default", "prosody"]


class JaG2pRequestBody(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
        json_schema_extra={
            "examples": [
                {
                    "text": "こんにちは。",
                    "mode": "default",
                }
            ]
        },
    )

    text: str = Field(min_length=1, description="Japanese text to convert to phonemes")
    mode: JaG2pMode = Field(
        default="default",
        description="G2P mode: default (basic phonemes) or prosody (with ^ $ [ ] etc.)",
    )


class JaG2pResponseBody(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
        json_schema_extra={
            "examples": [
                {
                    "phones": ["k", "o", "N", "n", "i", "ch", "i", "w", "a"],
                }
            ]
        },
    )

    phones: list[str] = Field(description="Phoneme token list")


class ZhG2pRequestBody(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
        json_schema_extra={
            "examples": [
                {
                    "text": "你好，世界。",
                }
            ]
        },
    )

    text: str = Field(
        min_length=1,
        description="Chinese text to convert to per-character pinyin",
    )


class ZhG2pResponseBody(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
        json_schema_extra={
            "examples": [
                {
                    "phones": ["ni3", "hao3", None, "shi4", "jie4", None],
                }
            ]
        },
    )

    phones: list[str | None] = Field(
        description="Per-character pinyin list from g2pW; null where g2pW has no reading",
    )


class EnG2pRequestBody(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
        json_schema_extra={
            "examples": [
                {
                    "text": "Hello, world.",
                }
            ]
        },
    )

    text: str = Field(min_length=1, description="English text to convert to phonemes")


class EnG2pResponseBody(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
        json_schema_extra={
            "examples": [
                {
                    "phones": [
                        "HH",
                        "AH0",
                        "L",
                        "OW1",
                        ",",
                        " ",
                        "W",
                        "ER1",
                        "L",
                        "D",
                        ".",
                    ],
                }
            ]
        },
    )

    phones: list[str] = Field(
        description="ARPAbet phoneme sequence from g2p_en; word separators and "
        "punctuation are preserved as tokens",
    )


class G2pWorkerStateResponseBody(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    loaded: bool = False
    message: str = ""
