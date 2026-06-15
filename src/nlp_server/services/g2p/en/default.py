"""English G2P via g2p_en (in-process)."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from nlp_server.infra.nltk_data import configure_g2p_en_nltk_data

if TYPE_CHECKING:
    from g2p_en import G2p

_g2p: G2p | None = None
_g2p_lock = asyncio.Lock()


def _get_g2p() -> G2p:
    global _g2p
    if _g2p is None:
        configure_g2p_en_nltk_data()
        from g2p_en import G2p

        _g2p = G2p()
    return _g2p


def sync_g2p_en(text: str) -> list[str]:
    return _get_g2p()(text)


async def g2p_en(text: str) -> list[str]:
    async with _g2p_lock:
        return await asyncio.to_thread(sync_g2p_en, text)
