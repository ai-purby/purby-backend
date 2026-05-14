from fastapi import APIRouter, HTTPException, Depends
from ..core.database import get_db
from ..core.security import get_current_user_id
from ..schemas.device import DeviceLinkRequest

router = APIRouter(prefix="/devices", tags=["devices"])


@router.post("/link")
def link_device(req: DeviceLinkRequest, user_id: str = Depends(get_current_user_id)):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO devices (user_id, device_type, platform)
            VALUES (%s, 'MOBILE', 'ANDROID') RETURNING id
            """,
            (user_id,),
        )
        mobile_device_id = cursor.fetchone()["id"]

        cursor.execute(
            """
            INSERT INTO device_links (desktop_device_id, mobile_device_id, status, linked_at)
            VALUES (%s, %s, 'LINKED', NOW())
            """,
            (req.desktop_device_id, str(mobile_device_id)),
        )
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"오류 발생: {str(e)}")
    finally:
        cursor.close()
        db.close()

    return {"message": "기기 연결이 완료되었습니다."}
