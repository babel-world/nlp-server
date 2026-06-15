from fastapi import APIRouter, HTTPException, status

from nlp_server.infra.worker.errors import WorkerSpawnFailed, WorkerSpawnTimeout
from nlp_server.schemas.g2p import (
    G2pWorkerStateResponseBody,
    JaG2pRequestBody,
    JaG2pResponseBody,
    ZhHansG2pRequestBody,
    ZhHansG2pResponseBody,
)
from nlp_server.services.g2p import (
    g2p_ja,
    g2p_zh_hans,
    g2p_zh_hans_start,
    g2p_zh_hans_stop,
)


router = APIRouter(prefix="/g2p", tags=["g2p"])


@router.post(
    "/ja",
    response_model=JaG2pResponseBody,
    response_model_by_alias=True,
    summary="Japanese G2P",
    response_description="Phoneme token list",
)
def g2p_ja_endpoint(body: JaG2pRequestBody):
    """
    Convert Japanese text to phonemes.

    - **text**: Japanese input string
    - **mode**: `default` for basic pyopenjtalk.g2p, `prosody` for full-context prosody markers
    """
    try:
        phones = g2p_ja(body.text, body.mode)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"G2P failed: {exc}") from exc

    return JaG2pResponseBody(phones=phones)


@router.post(
    "/zh-hans",
    response_model=ZhHansG2pResponseBody,
    response_model_by_alias=True,
    summary="Simplified Chinese G2P",
    response_description="Per-character pinyin list aligned with input text",
    description=(
        "Convert simplified Chinese text to per-character pinyin via g2pW. "
        "Non-Chinese characters (punctuation, Latin letters, etc.) are preserved "
        "as-is in the output. "
        "The worker starts automatically on the first request; call "
        "``POST /g2p/zh-hans/stop`` after batch processing to release memory."
    ),
)
async def g2p_zh_hans_endpoint(body: ZhHansG2pRequestBody) -> ZhHansG2pResponseBody:
    try:
        phones = await g2p_zh_hans(body.text)
    except WorkerSpawnTimeout as exc:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=str(exc),
        ) from exc
    except WorkerSpawnFailed as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=exc.stderr_tail or str(exc),
        ) from exc
    except (ValueError, RuntimeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc

    return ZhHansG2pResponseBody(phones=phones)


@router.post(
    "/zh-hans/start",
    response_model=G2pWorkerStateResponseBody,
    response_model_by_alias=True,
    summary="Preload g2pw worker (optional)",
    description=(
        "Explicitly start the persistent g2pw worker and load models. "
        "If not called, ``POST /g2p/zh-hans`` will start the worker on first use."
    ),
)
async def g2p_zh_hans_start_endpoint() -> G2pWorkerStateResponseBody:
    try:
        return await g2p_zh_hans_start()
    except WorkerSpawnTimeout as exc:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=str(exc),
        ) from exc
    except WorkerSpawnFailed as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=exc.stderr_tail or str(exc),
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc


@router.post(
    "/zh-hans/stop",
    response_model=G2pWorkerStateResponseBody,
    response_model_by_alias=True,
    summary="Release g2pw worker",
    description="Stop the persistent g2pw worker subprocess and release memory.",
)
async def g2p_zh_hans_stop_endpoint() -> G2pWorkerStateResponseBody:
    return await g2p_zh_hans_stop()
