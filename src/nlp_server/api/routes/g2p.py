from fastapi import APIRouter, HTTPException, status

from nlp_server.infra.worker.errors import WorkerSpawnFailed, WorkerSpawnTimeout
from nlp_server.schemas.g2p import (
    EnG2pRequestBody,
    EnG2pResponseBody,
    G2pWorkerStateResponseBody,
    JaG2pRequestBody,
    JaG2pResponseBody,
    ZhG2pRequestBody,
    ZhG2pResponseBody,
)
from nlp_server.services.g2p import (
    g2p_en,
    g2p_ja,
    g2p_zh,
    g2p_zh_start,
    g2p_zh_stop,
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
    "/en",
    response_model=EnG2pResponseBody,
    response_model_by_alias=True,
    summary="English G2P",
    response_description="ARPAbet phoneme token list",
    description=(
        "Convert English text to ARPAbet phonemes via g2p_en. "
        "Output is the raw g2p_en token list, including word-separator "
        "and punctuation tokens."
    ),
)
async def g2p_en_endpoint(body: EnG2pRequestBody) -> EnG2pResponseBody:
    try:
        phones = await g2p_en(body.text)
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"G2P failed: {exc}",
        ) from exc

    return EnG2pResponseBody(phones=phones)


@router.post(
    "/zh",
    response_model=ZhG2pResponseBody,
    response_model_by_alias=True,
    summary="Chinese G2P",
    response_description="Per-character pinyin list from g2pW",
    description=(
        "Convert Chinese text to per-character pinyin via g2pW. "
        "Output is the raw g2pW result (null for positions without a reading). "
        "The worker starts automatically on the first request; call "
        "``POST /g2p/zh/stop`` after batch processing to release memory."
    ),
)
async def g2p_zh_endpoint(body: ZhG2pRequestBody) -> ZhG2pResponseBody:
    try:
        phones = await g2p_zh(body.text)
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

    return ZhG2pResponseBody(phones=phones)


@router.post(
    "/zh/start",
    response_model=G2pWorkerStateResponseBody,
    response_model_by_alias=True,
    summary="Preload g2pw worker (optional)",
    description=(
        "Explicitly start the persistent g2pw worker and load models. "
        "If not called, ``POST /g2p/zh`` will start the worker on first use."
    ),
)
async def g2p_zh_start_endpoint() -> G2pWorkerStateResponseBody:
    try:
        return await g2p_zh_start()
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
    "/zh/stop",
    response_model=G2pWorkerStateResponseBody,
    response_model_by_alias=True,
    summary="Release g2pw worker",
    description="Stop the persistent g2pw worker subprocess and release memory.",
)
async def g2p_zh_stop_endpoint() -> G2pWorkerStateResponseBody:
    return await g2p_zh_stop()
