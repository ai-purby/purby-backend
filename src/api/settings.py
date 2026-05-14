from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from ..core.database import get_db
from ..core.security import get_current_user_id
from ..schemas.settings import SettingsUpdate

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("")
def get_settings(user_id: str = Depends(get_current_user_id)):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM settings WHERE user_id = %s", (user_id,))
        row = cursor.fetchone()

        if not row:
            cursor.execute(
                "INSERT INTO settings (user_id) VALUES (%s) RETURNING *",
                (user_id,),
            )
            row = cursor.fetchone()
            db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"오류 발생: {str(e)}")
    finally:
        cursor.close()
        db.close()

    return {"settings": row}


@router.patch("")
def update_settings(req: SettingsUpdate, user_id: str = Depends(get_current_user_id)):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT id FROM settings WHERE user_id = %s", (user_id,))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO settings (user_id) VALUES (%s)", (user_id,))
            db.commit()

        updates = {k: v for k, v in req.dict().items() if v is not None}
        if not updates:
            raise HTTPException(status_code=400, detail="수정할 내용이 없습니다.")

        updates["updated_at"] = datetime.now()
        set_clause = ", ".join([f"{k} = %s" for k in updates.keys()])
        cursor.execute(
            f"UPDATE settings SET {set_clause} WHERE user_id = %s",
            (*updates.values(), user_id),
        )
        db.commit()

        cursor.execute("SELECT * FROM settings WHERE user_id = %s", (user_id,))
        row = cursor.fetchone()

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"오류 발생: {str(e)}")
    finally:
        cursor.close()
        db.close()

    return {"message": "설정이 저장되었습니다.", "settings": row}
