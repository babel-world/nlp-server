"""Chinese text normalization service wrapper."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nlp_server.services.tn.zh.vendor.text_normlization import TextNormalizer

_normalizer: TextNormalizer | None = None


def _get_normalizer() -> TextNormalizer:
    global _normalizer
    if _normalizer is None:
        from nlp_server.services.tn.zh.vendor.text_normlization import TextNormalizer

        _normalizer = TextNormalizer()
    return _normalizer


def tn_zh(text: str) -> str:
    sentences = _get_normalizer().normalize(text)
    return "".join(sentences)
