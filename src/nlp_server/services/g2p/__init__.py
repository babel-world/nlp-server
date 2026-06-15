from typing import Literal

from nlp_server.schemas.g2p import G2pWorkerStateResponseBody
from nlp_server.services.g2p.en.default import g2p_en
from nlp_server.services.g2p.ja.default import extract
from nlp_server.services.g2p.ja.prosody import extract_prosody
from nlp_server.services.g2p.zh.default import (
    g2p_zh,
    g2p_zh_start,
    g2p_zh_stop,
)

JaG2pMode = Literal["default", "prosody"]


def g2p_ja(text: str, mode: JaG2pMode = "default") -> list[str]:
    """Convert Japanese text to a phoneme list."""
    if mode == "prosody":
        return extract_prosody(text)
    return extract(text)


__all__ = [
    "G2pWorkerStateResponseBody",
    "JaG2pMode",
    "g2p_en",
    "g2p_ja",
    "g2p_zh",
    "g2p_zh_start",
    "g2p_zh_stop",
]
