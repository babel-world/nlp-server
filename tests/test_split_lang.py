"""Unit tests for split-lang service (no HTTP server required)."""

from __future__ import annotations

import unittest

from nlp_server.services.split_lang import split_lang


class SplitLangServiceTests(unittest.TestCase):
    def test_mixed_zh_ja_segments(self) -> None:
        text = "你喜欢看アニメ吗"
        segments = split_lang(text)
        self.assertGreaterEqual(len(segments), 2)
        langs = {segment.lang for segment in segments}
        self.assertIn("zh", langs)
        self.assertIn("ja", langs)

    def test_segments_reconstruct_input(self) -> None:
        text = "你喜欢看アニメ吗"
        segments = split_lang(text)
        self.assertEqual("".join(segment.text for segment in segments), text)

    def test_index_and_length_align_with_input(self) -> None:
        text = "你喜欢看アニメ吗"
        segments = split_lang(text)
        for segment in segments:
            self.assertEqual(
                text[segment.index : segment.index + segment.length],
                segment.text,
            )
            self.assertEqual(segment.length, len(segment.text))

    def test_indices_are_monotonic(self) -> None:
        text = "你喜欢看アニメ吗"
        segments = split_lang(text)
        expected_index = 0
        for segment in segments:
            self.assertEqual(segment.index, expected_index)
            expected_index += segment.length

    def test_english_single_language(self) -> None:
        text = "hello world"
        segments = split_lang(text)
        self.assertGreaterEqual(len(segments), 1)
        self.assertEqual("".join(segment.text for segment in segments), text)
        self.assertTrue(all(segment.lang == "en" for segment in segments))

    def test_punctuation_is_separate_segment(self) -> None:
        text = "你喜欢看アニメ吗？"
        segments = split_lang(text)
        self.assertEqual(segments[-1].lang, "punctuation")
        self.assertEqual(segments[-1].text, "？")
        self.assertEqual("".join(segment.text for segment in segments), text)


if __name__ == "__main__":
    unittest.main()
