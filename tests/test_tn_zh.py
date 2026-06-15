"""Tests for Chinese TN service and API wrapper."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from nlp_server.services.tn.zh import core as tn_core
from nlp_server.services.tn.zh.vendor.text_normlization import TextNormalizer


class TnZhServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        tn_core._normalizer = None

    def tearDown(self) -> None:
        tn_core._normalizer = None

    @patch.object(tn_core, "_get_normalizer")
    def test_tn_zh_joins_sentences(self, get_normalizer_mock: MagicMock) -> None:
        normalizer = MagicMock()
        normalizer.normalize.return_value = ["第一句", "第二句"]
        get_normalizer_mock.return_value = normalizer

        result = tn_core.tn_zh("ignored")

        self.assertEqual(result, "第一句第二句")
        normalizer.normalize.assert_called_once_with("ignored")

    def test_vendor_text_normalizer_import(self) -> None:
        self.assertIsNotNone(TextNormalizer)

    def test_tn_zh_percentage_integration(self) -> None:
        result = tn_core.tn_zh("明天有62%的概率降雨")
        self.assertIn("百分之六十二", result)


if __name__ == "__main__":
    unittest.main()
