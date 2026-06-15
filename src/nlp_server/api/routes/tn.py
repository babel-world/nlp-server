from fastapi import APIRouter, HTTPException

from nlp_server.schemas.tn import ZhTnRequestBody, ZhTnResponseBody
from nlp_server.services.tn.zh.core import tn_zh


router = APIRouter(prefix="/tn", tags=["tn"])


@router.post(
    "/zh",
    response_model=ZhTnResponseBody,
    response_model_by_alias=True,
    summary="Chinese text normalization",
    response_description="NSW-normalized Chinese text",
    description=(
        "Normalize Chinese non-standard words (numbers, dates, phones, etc.) "
        "into spoken Chinese characters. Multi-sentence input is split internally, "
        "normalized per sentence, then concatenated without extra separators."
    ),
)
def tn_zh_endpoint(body: ZhTnRequestBody) -> ZhTnResponseBody:
    try:
        return ZhTnResponseBody(text=tn_zh(body.text))
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"tn/zh failed: {exc}",
        ) from exc
