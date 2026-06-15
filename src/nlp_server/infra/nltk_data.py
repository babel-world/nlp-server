"""NLTK data directory resolution for English G2P (g2p_en)."""

from __future__ import annotations

import os
from pathlib import Path

from nlp_server.utils.paths import get_repo_root

G2P_EN_NLTK_PACKAGES = (
    "cmudict",
    "averaged_perceptron_tagger",
    "averaged_perceptron_tagger_eng",
)

_TAGGER_RESOURCES = (
    "taggers/averaged_perceptron_tagger",
    "taggers/averaged_perceptron_tagger_eng",
)


def project_nltk_data_dir() -> Path:
    """Project-local NLTK data root under ``.models/nltk_data``."""
    return get_repo_root() / ".models" / "nltk_data"


def system_nltk_data_dirs() -> list[Path]:
    """Common NLTK data locations on the host (without the project path)."""
    home = Path.home()
    candidates = [
        home / "nltk_data",
        home / "AppData" / "Roaming" / "nltk_data",
        Path("C:/nltk_data"),
    ]
    unique: list[Path] = []
    for path in candidates:
        resolved = path.resolve()
        if resolved not in unique:
            unique.append(resolved)
    return unique


def _nltk_resource_paths() -> tuple[str, ...]:
    return ("corpora/cmudict", *_TAGGER_RESOURCES)


def nltk_resources_available(data_dir: Path) -> bool:
    """Return True when g2p_en-required NLTK resources exist under ``data_dir``."""
    if not data_dir.is_dir():
        return False

    import nltk

    previous_path = list(nltk.data.path)
    data_dir_str = str(data_dir.resolve())
    try:
        if data_dir_str not in nltk.data.path:
            nltk.data.path.insert(0, data_dir_str)
        nltk.data.find("corpora/cmudict")
        for tagger_resource in _TAGGER_RESOURCES:
            try:
                nltk.data.find(tagger_resource)
                return True
            except LookupError:
                continue
        return False
    except LookupError:
        return False
    finally:
        nltk.data.path[:] = previous_path


def activate_nltk_data_dir(data_dir: Path) -> Path:
    """Point NLTK at ``data_dir`` for subsequent imports and lookups."""
    resolved = data_dir.resolve()
    resolved.mkdir(parents=True, exist_ok=True)
    os.environ["NLTK_DATA"] = str(resolved)

    import nltk

    resolved_str = str(resolved)
    if resolved_str not in nltk.data.path:
        nltk.data.path.insert(0, resolved_str)
    return resolved


def download_nltk_resources(data_dir: Path) -> None:
    """Download g2p_en NLTK packages into ``data_dir``."""
    import nltk

    target = data_dir.resolve()
    target.mkdir(parents=True, exist_ok=True)
    activate_nltk_data_dir(target)
    for package in G2P_EN_NLTK_PACKAGES:
        nltk.download(package, download_dir=str(target), quiet=True)


def configure_g2p_en_nltk_data() -> Path:
    """
    Resolve NLTK data for g2p_en:

    1. Use project ``.models/nltk_data`` when it already has required resources.
    2. Else use the first system default location that has them.
    3. Else download required packages into project ``.models/nltk_data``.
    """
    project_dir = project_nltk_data_dir()
    if nltk_resources_available(project_dir):
        return activate_nltk_data_dir(project_dir)

    for system_dir in system_nltk_data_dirs():
        if nltk_resources_available(system_dir):
            return activate_nltk_data_dir(system_dir)

    download_nltk_resources(project_dir)
    if not nltk_resources_available(project_dir):
        raise RuntimeError(f"NLTK resources missing after download: {project_dir}")
    return activate_nltk_data_dir(project_dir)
