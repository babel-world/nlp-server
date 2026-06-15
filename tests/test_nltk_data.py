"""Tests for NLTK data directory resolution."""

from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import patch

from nlp_server.infra import nltk_data


class NltkDataPathTests(unittest.TestCase):
    def test_project_nltk_data_dir_under_models(self) -> None:
        path = nltk_data.project_nltk_data_dir()
        self.assertEqual(path.name, "nltk_data")
        self.assertEqual(path.parent.name, ".models")

    @patch("nlp_server.infra.nltk_data.nltk_resources_available")
    @patch("nlp_server.infra.nltk_data.activate_nltk_data_dir")
    def test_prefers_project_models_when_present(
        self,
        activate_mock,
        available_mock,
    ) -> None:
        project_dir = Path("E:/repo/.models/nltk_data")

        def available_side_effect(path: Path) -> bool:
            return path == project_dir

        available_mock.side_effect = available_side_effect
        activate_mock.return_value = project_dir

        with patch.object(nltk_data, "project_nltk_data_dir", return_value=project_dir):
            result = nltk_data.configure_g2p_en_nltk_data()

        self.assertEqual(result, project_dir)
        activate_mock.assert_called_once_with(project_dir)

    @patch("nlp_server.infra.nltk_data.download_nltk_resources")
    @patch("nlp_server.infra.nltk_data.nltk_resources_available")
    @patch("nlp_server.infra.nltk_data.activate_nltk_data_dir")
    def test_falls_back_to_system_dir(
        self,
        activate_mock,
        available_mock,
        download_mock,
    ) -> None:
        project_dir = Path("E:/repo/.models/nltk_data")
        system_dir = Path("C:/Users/me/nltk_data")

        def available_side_effect(path: Path) -> bool:
            return path == system_dir

        available_mock.side_effect = available_side_effect
        activate_mock.return_value = system_dir

        with patch.object(nltk_data, "project_nltk_data_dir", return_value=project_dir):
            with patch.object(
                nltk_data,
                "system_nltk_data_dirs",
                return_value=[system_dir],
            ):
                result = nltk_data.configure_g2p_en_nltk_data()

        self.assertEqual(result, system_dir)
        download_mock.assert_not_called()

    @patch("nlp_server.infra.nltk_data.download_nltk_resources")
    @patch("nlp_server.infra.nltk_data.nltk_resources_available")
    @patch("nlp_server.infra.nltk_data.activate_nltk_data_dir")
    def test_downloads_to_project_when_missing_everywhere(
        self,
        activate_mock,
        available_mock,
        download_mock,
    ) -> None:
        project_dir = Path("E:/repo/.models/nltk_data")
        available_mock.side_effect = [False, True]
        activate_mock.return_value = project_dir

        with patch.object(nltk_data, "project_nltk_data_dir", return_value=project_dir):
            with patch.object(nltk_data, "system_nltk_data_dirs", return_value=[]):
                result = nltk_data.configure_g2p_en_nltk_data()

        download_mock.assert_called_once_with(project_dir)
        self.assertEqual(result, project_dir)


if __name__ == "__main__":
    unittest.main()
