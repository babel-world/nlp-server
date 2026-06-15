from fastapi import APIRouter, HTTPException

from nlp_server.schemas.split_lang import (
    SPLIT_LANG_RESPONSE_EXAMPLE,
    SplitLangRequestBody,
    SplitLangSegmentBody,
)
from nlp_server.services.split_lang import split_lang as split_lang_service


router = APIRouter(prefix="/split-lang", tags=["split-lang"])


@router.post(
    "",
    response_model=list[SplitLangSegmentBody],
    response_model_by_alias=True,
    summary="Split text by language",
    response_description="Flat array of language segments with offsets",
    description=(
        "Split a single mixed-language sentence into consecutive segments. "
        "Each item contains ``lang``, ``text``, ``index`` (0-based offset), "
        "and ``length``. Punctuation is emitted as separate segments with "
        "``lang: punctuation``. Segment texts concatenate back to the input."
    ),
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": SPLIT_LANG_RESPONSE_EXAMPLE,
                }
            }
        }
    },
)
def split_lang_endpoint(body: SplitLangRequestBody) -> list[SplitLangSegmentBody]:
    try:
        return split_lang_service(body.text)
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"split-lang failed: {exc}",
        ) from exc
