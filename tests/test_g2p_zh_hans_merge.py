"""Unit tests for zh-hans G2P merge logic (no worker/models required)."""

from __future__ import annotations

import unittest

from nlp_server.services.g2p.zh.hans import merge_phones_with_text


class MergePhonesWithTextTests(unittest.TestCase):
    def test_all_chinese_pinyin_preserved(self) -> None:
        text = "你好"
        g2pw = [["ni3", "hao3"]]
        self.assertEqual(merge_phones_with_text(text, g2pw), ["ni3", "hao3"])

    def test_null_slots_replaced_with_original_chars(self) -> None:
        text = "你好，世界。"
        g2pw = [["ni3", "hao3", None, "shi4", "jie4", None]]
        self.assertEqual(
            merge_phones_with_text(text, g2pw),
            ["ni3", "hao3", "，", "shi4", "jie4", "。"],
        )

    def test_length_mismatch_raises(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            merge_phones_with_text("ab", [["a"]])
        self.assertIn("length mismatch", str(ctx.exception))

    def test_multiple_sentences_raises(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            merge_phones_with_text("你好", [["ni3", "hao3"], ["shi4", "jie4"]])
        self.assertIn("multiple sentences", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
