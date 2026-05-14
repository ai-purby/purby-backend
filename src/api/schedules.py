from datetime import date
from fastapi import APIRouter, HTTPException, Depends
from ..core.database import get_db
from ..core.security import get_current_user_id
from ..schemas.schedule import ScheduleCreate, ScheduleUpdate

router = APIRouter(prefix="/schedules", tags=["schedules"])


@router.get("")
def get_schedules(date: date, user_id: str = Depends(get_current_user_id)):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            """
            SELECT id, title, start_time, end_time, is_done, created_at
            FROM schedules
            WHERE user_id = %s AND DATE(start_time) = %s
            ORDER BY start_time ASC
            """,
            (user_id, date),
        )
        rows = cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"오류 발생: {str(e)}")
    finally:
        cursor.close()
        db.close()

    return {"schedules": rows}


@router.post("")
def create_schedule(req: ScheduleCreate, user_id: str = Depends(get_current_user_id)):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO schedules (user_id, title, start_time, end_time, is_all_day, is_recurring)
            VALUES (%s, %s, %s, %s, FALSE, FALSE) RETURNING id
            """,
            (user_id, req.title, req.start_time, req.end_time),
        )
        new_id = cursor.fetchone()["id"]
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"오류 발생: {str(e)}")
    finally:
        cursor.close()
        db.close()

    return {"message": "일정이 추가되었습니다.", "id": new_id}


@router.patch("/{schedule_id}")
def update_schedule(schedule_id: int, req: ScheduleUpdate, user_id: str = Depends(get_current_user_id)):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "SELECT id FROM schedules WHERE id = %s AND user_id = %s",
            (schedule_id, user_id),
        )
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="일정을 찾을 수 없습니다.")

        updates = {k: v for k, v in req.dict().items() if v is not None}
        if not updates:
            raise HTTPException(status_code=400, detail="수정할 내용이 없습니다.")

        set_clause = ", ".join([f"{k} = %s" for k in updates.keys()])
        cursor.execute(
            f"UPDATE schedules SET {set_clause} WHERE id = %s",
            (*updates.values(), schedule_id),
        )
        db.commit()
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"오류 발생: {str(e)}")
    finally:
        cursor.close()
        db.close()

    return {"message": "일정이 수정되었습니다."}


@router.delete("/{schedule_id}")
def delete_schedule(schedule_id: int, user_id: str = Depends(get_current_user_id)):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "SELECT id FROM schedules WHERE id = %s AND user_id = %s",
            (schedule_id, user_id),
        )
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="일정을 찾을 수 없습니다.")

        cursor.execute("DELETE FROM schedules WHERE id = %s", (schedule_id,))
        db.commit()
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"오류 발생: {str(e)}")
    finally:
        cursor.close()
        db.close()

    return {"message": "일정이 삭제되었습니다."}


@router.patch("/{schedule_id}/done")
def toggle_done(schedule_id: int, user_id: str = Depends(get_current_user_id)):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "SELECT id, is_done FROM schedules WHERE id = %s AND user_id = %s",
            (schedule_id, user_id),
        )
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="일정을 찾을 수 없습니다.")

        new_done = not row["is_done"]
        cursor.execute(
            "UPDATE schedules SET is_done = %s WHERE id = %s",
            (new_done, schedule_id),
        )
        db.commit()
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"오류 발생: {str(e)}")
    finally:
        cursor.close()
        db.close()

    return {"message": "완료 상태가 변경되었습니다.", "is_done": new_done}
