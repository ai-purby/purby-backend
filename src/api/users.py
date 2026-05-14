from fastapi import APIRouter, HTTPException, Depends
from ..core.database import get_db
from ..core.security import get_current_user_id

router = APIRouter(prefix="/users", tags=["users"])


@router.delete("/me")
def delete_account(user_id: str = Depends(get_current_user_id)):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM schedules WHERE user_id = %s", (user_id,))
        cursor.execute("DELETE FROM settings WHERE user_id = %s", (user_id,))
        cursor.execute("DELETE FROM devices WHERE user_id = %s", (user_id,))
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"오류 발생: {str(e)}")
    finally:
        cursor.close()
        db.close()

    return {"message": "계정이 삭제되었습니다."}
