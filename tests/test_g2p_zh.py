"""Unit tests for Chinese G2P worker result parsing (no worker/models required)."""

from __future__ import annotations

import unittest

from nlp_server.services.g2p.zh.default import _extract_phones_row


class ExtractPhonesRowTests(unittest.TestCase):
    def test_passthrough_worker_row(self) -> None:
        g2pw = [["ni3", "hao3", None, "shi4", "jie4", None]]
        self.assertEqual(
            _extract_phones_row(g2pw),
            ["ni3", "hao3", None, "shi4", "jie4", None],
        )

    def test_multiple_sentences_raises(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            _extract_phones_row([["ni3", "hao3"], ["shi4", "jie4"]])
        self.assertIn("multiple sentences", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
