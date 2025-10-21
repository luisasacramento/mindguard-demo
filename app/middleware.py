from fastapi import Request
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger("mindguard")

async def exception_handler(request: Request, exc):
    # Log com detalhes apenas em logs internos (SIEM)
    logger.exception("Unhandled error: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"error": "Ocorreu um erro interno. Contate o suporte."}
    )
