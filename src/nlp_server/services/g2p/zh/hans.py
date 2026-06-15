"""Simplified Chinese G2P via g2pw worker."""

from __future__ import annotations

import asyncio
import json

from nlp_server.infra.worker.session import get_worker_session
from nlp_server.schemas.g2p import G2pWorkerStateResponseBody

WORKER_ALIAS = "g2pw"

_g2p_lock = asyncio.Lock()


def merge_phones_with_text(
    text: str,
    g2pw_result: list[list[str | None]],
) -> list[str]:
    """Replace g2pW ``null`` slots with the original character at that index."""
    if len(g2pw_result) != 1:
        raise ValueError("g2pW returned multiple sentences; single text expected")
    row = g2pw_result[0]
    if len(row) != len(text):
        raise ValueError(
            f"g2pW length mismatch: text={len(text)} phones={len(row)}"
        )
    return [
        text[i] if token is None else str(token)
        for i, token in enumerate(row)
    ]


def _session():
    return get_worker_session(WORKER_ALIAS)


def sync_g2p_zh_hans(text: str) -> list[str]:
    raw = _session().g2p_text(text)
    parsed = json.loads(raw)
    return merge_phones_with_text(text, parsed)


def sync_start_session() -> G2pWorkerStateResponseBody:
    result = _session().start()
    if result.newly_started:
        return G2pWorkerStateResponseBody(
            loaded=True,
            message="g2pw worker loaded.",
        )
    return G2pWorkerStateResponseBody(
        loaded=True,
        message="g2pw worker was already loaded.",
    )


def sync_stop_session() -> G2pWorkerStateResponseBody:
    released = _session().stop()
    if released:
        return G2pWorkerStateResponseBody(
            loaded=False,
            message="g2pw worker released.",
        )
    return G2pWorkerStateResponseBody(
        loaded=False,
        message="g2pw worker was not loaded.",
    )


async def g2p_zh_hans(text: str) -> list[str]:
    async with _g2p_lock:
        return await asyncio.to_thread(sync_g2p_zh_hans, text)


async def g2p_zh_hans_start() -> G2pWorkerStateResponseBody:
    async with _g2p_lock:
        return await asyncio.to_thread(sync_start_session)


async def g2p_zh_hans_stop() -> G2pWorkerStateResponseBody:
    async with _g2p_lock:
        return await asyncio.to_thread(sync_stop_session)
