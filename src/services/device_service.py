from src.core.redis import redis_client
from src.schemas.device import PairingCodeResponse
from src.utils.pairing_code import (
    format_pairing_code,
    generate_pairing_code,
    normalize_pairing_code,
)
from dotenv import load_dotenv
import os

load_dotenv()

PAIRING_CODE_TTL_SECONDS = 300


# 페어링 코드 발급
async def issue_pairing_code(desktop_device_id: str) -> PairingCodeResponse:
    app_url = os.getenv("APP_URL")
    if not app_url:
        raise RuntimeError("APP_URL environment variable is required")

    device_key = f"pairing:device:{desktop_device_id}"

    existing_code = await redis_client.get(device_key)

    if existing_code:
        return PairingCodeResponse(
            pairing_code=format_pairing_code(existing_code),
            qr_payload=f"{app_url.rstrip('/')}/pair/{existing_code}",
        )

    code = generate_pairing_code()
    normalized_code = normalize_pairing_code(code)

    created = await redis_client.set(
        device_key,
        normalized_code,
        ex=PAIRING_CODE_TTL_SECONDS,
        nx=True,
    )

    if not created:
        existing_code = await redis_client.get(device_key)
        if existing_code:
            return PairingCodeResponse(
                pairing_code=format_pairing_code(existing_code),
                qr_payload=f"{app_url.rstrip('/')}/pair/{existing_code}",
            )

        return await issue_pairing_code(desktop_device_id)

    code_key = f"pairing:code:{normalized_code}"

    await redis_client.set(
        code_key,
        desktop_device_id,
        ex=PAIRING_CODE_TTL_SECONDS,
    )

    return PairingCodeResponse(
        pairing_code=code,
        qr_payload=f"purby://pair/{normalized_code}",
    )
