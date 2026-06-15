"""Tests for English G2P service."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from nlp_server.services.g2p.en import default as en_default


class G2pEnServiceTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        en_default._g2p = None

    def tearDown(self) -> None:
        en_default._g2p = None

    @patch("nlp_server.services.g2p.en.default.configure_g2p_en_nltk_data")
    def test_sync_g2p_en_passthrough(self, configure_mock: MagicMock) -> None:
        expected = ["HH", "AH0", "L", "OW1", "."]
        mock_g2p = MagicMock(return_value=expected)
        en_default._g2p = mock_g2p

        result = en_default.sync_g2p_en("Hello.")

        self.assertEqual(result, expected)
        mock_g2p.assert_called_once_with("Hello.")
        configure_mock.assert_not_called()

    @patch("nlp_server.services.g2p.en.default.configure_g2p_en_nltk_data")
    def test_get_g2p_configures_nltk_on_first_init(
        self,
        configure_mock: MagicMock,
    ) -> None:
        mock_instance = MagicMock()
        mock_g2p_cls = MagicMock(return_value=mock_instance)
        fake_g2p_en = MagicMock()
        fake_g2p_en.G2p = mock_g2p_cls

        with patch.dict("sys.modules", {"g2p_en": fake_g2p_en}):
            first = en_default._get_g2p()
            second = en_default._get_g2p()

        self.assertIs(first, mock_instance)
        self.assertIs(second, mock_instance)
        configure_mock.assert_called_once()
        mock_g2p_cls.assert_called_once()

    @patch("nlp_server.services.g2p.en.default.sync_g2p_en")
    async def test_async_g2p_en(self, sync_mock: MagicMock) -> None:
        sync_mock.return_value = ["T", "EH1", "S", "T"]

        result = await en_default.g2p_en("test")

        self.assertEqual(result, ["T", "EH1", "S", "T"])
        sync_mock.assert_called_once_with("test")


if __name__ == "__main__":
    unittest.main()
