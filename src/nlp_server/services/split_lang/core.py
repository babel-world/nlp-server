"""In-process split-lang wrapper."""

from __future__ import annotations

from pathlib import Path

import fast_langdetect
from split_lang import LangSplitter

from nlp_server.schemas.split_lang import SplitLangSegmentBody
from nlp_server.utils.paths import get_repo_root

_CACHE_DIR = get_repo_root() / ".models" / "fast_langdetect"
_SPLITTER: LangSplitter | None = None


def _configure_fast_langdetect_cache() -> Path:
    cache_dir = _CACHE_DIR
    cache_dir.mkdir(parents=True, exist_ok=True)
    fast_langdetect.infer._default_detector = fast_langdetect.infer.LangDetector(
        fast_langdetect.infer.LangDetectConfig(cache_dir=cache_dir)
    )
    return cache_dir


def _get_splitter() -> LangSplitter:
    global _SPLITTER
    if _SPLITTER is None:
        _configure_fast_langdetect_cache()
        _SPLITTER = LangSplitter(debug=False, merge_across_punctuation=False)
    return _SPLITTER


def split_lang(text: str) -> list[SplitLangSegmentBody]:
    """Split one sentence into language-tagged segments with offsets."""
    substr = _get_splitter().split_by_lang(text=text)
    segments: list[SplitLangSegmentBody] = []
    offset = 0

    for item in substr:
        segment_text = item.text
        length = len(segment_text)
        if length == 0:
            continue
        segments.append(
            SplitLangSegmentBody(
                lang=item.lang,
                text=segment_text,
                index=offset,
                length=length,
            )
        )
        offset += length

    reconstructed = "".join(segment.text for segment in segments)
    if reconstructed != text:
        raise ValueError(
            f"split-lang segments do not reconstruct input: "
            f"input={len(text)} reconstructed={len(reconstructed)}"
        )

    return segments
