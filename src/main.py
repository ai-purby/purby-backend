import random
import smtplib
import os
from email.mime.text import MIMEText
from datetime import datetime, timedelta, date, time
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from jose import JWTError, jwt
from typing import Optional

load_dotenv()

app = FastAPI()
security = HTTPBearer()

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

# ───────────────────────────────────────────────
# JWT 설정
# ───────────────────────────────────────────────
SECRET_KEY = "persona_frame_secret_key_change_this"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24 * 7  # 7일

def create_access_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="토큰이 유효하지 않습니다.")

# ───────────────────────────────────────────────
# DB 연결
# ───────────────────────────────────────────────
def get_db():
    conn = psycopg2.connect(
        "host=127.0.0.1 port=5432 user=postgres password=postgres123 dbname=persona_frame",
        cursor_factory=RealDictCursor
    )
    return conn

# ───────────────────────────────────────────────
# 스키마
# ───────────────────────────────────────────────
class EmailRequest(BaseModel):
    email: str

class VerifyRequest(BaseModel):
    email: str
    code: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    nickname: str | None = None

class LoginRequest(BaseModel):
    email: str
    password: str

class ScheduleCreate(BaseModel):
    title: str
    start_time: datetime
    end_time: Optional[datetime] = None

class ScheduleUpdate(BaseModel):
    title: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

class SettingsUpdate(BaseModel):
    ai_name:          Optional[str]   = None
    personality:      Optional[str]   = None
    sleep_enabled:    Optional[bool]  = None
    sleep_start:      Optional[str]   = None  # "22:00"
    sleep_end:        Optional[str]   = None  # "06:00"
    briefing_enabled: Optional[bool]  = None
    briefing_time:    Optional[str]   = None  # "07:00"
    retro_enabled:    Optional[bool]  = None
    retro_time:       Optional[str]   = None  # "22:00"
    volume:           Optional[float] = None
    brightness:       Optional[float] = None

# ───────────────────────────────────────────────
# 기존 인증 API (변경 없음)
# ───────────────────────────────────────────────
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/auth/send-code")
def send_code(req: EmailRequest):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT id FROM users WHERE email = %s", (req.email,))
        existing = cursor.fetchone()
        if existing:
            raise HTTPException(status_code=400, detail="이미 가입된 이메일입니다.")

        code = str(random.randint(100000, 999999))
        expires_at = datetime.now() + timedelta(minutes=5)

        cursor.execute(
            "INSERT INTO email_verifications (email, code, expires_at) VALUES (%s, %s, %s)",
            (req.email, code, expires_at)
        )
        db.commit()

        msg = MIMEText(f"Persona Frame 인증번호: {code}\n\n5분 이내에 입력해주세요.")
        msg["Subject"] = "[Persona Frame] 이메일 인증번호"
        msg["From"] = GMAIL_USER
        msg["To"] = req.email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_PASSWORD)
            smtp.sendmail(GMAIL_USER, req.email, msg.as_string())

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"오류 발생: {str(e)}")
    finally:
        cursor.close()
        db.close()

    return {"message": "인증번호가 발송되었습니다."}

@app.post("/auth/verify-code")
def verify_code(req: VerifyRequest):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            """
            SELECT * FROM email_verifications
            WHERE email = %s AND code = %s AND is_used = FALSE
            ORDER BY created_at DESC LIMIT 1
            """,
            (req.email, req.code)
        )
        entry = cursor.fetchone()

        if not entry:
            raise HTTPException(status_code=400, detail="인증번호가 올바르지 않습니다.")

        if datetime.now() > entry["expires_at"]:
            raise HTTPException(status_code=400, detail="인증번호가 만료되었습니다.")

        cursor.execute(
            "UPDATE email_verifications SET is_used = TRUE WHERE id = %s",
            (entry["id"],)
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

    return {"message": "인증 완료"}

@app.post("/auth/register")
def register(req: RegisterRequest):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT id FROM users WHERE email = %s", (req.email,))
        existing = cursor.fetchone()
        if existing:
            raise HTTPException(status_code=400, detail="이미 가입된 이메일입니다.")

        cursor.execute(
            """
            SELECT * FROM email_verifications
            WHERE email = %s AND is_used = TRUE
            ORDER BY created_at DESC LIMIT 1
            """,
            (req.email,)
        )
        verified = cursor.fetchone()
        if not verified:
            raise HTTPException(status_code=400, detail="이메일 인증이 필요합니다.")

        cursor.execute(
            "INSERT INTO users (email, password_hash, nickname, is_verified) VALUES (%s, %s, %s, TRUE)",
            (req.email, req.password, req.nickname)
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

    return {"message": "회원가입이 완료되었습니다."}

@app.post("/auth/login")
def login(req: LoginRequest):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (req.email,))
        user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=400, detail="이메일 또는 비밀번호가 올바르지 않습니다.")

        if not user["is_verified"]:
            raise HTTPException(status_code=400, detail="이메일 인증이 필요합니다.")

        if user["password_hash"] != req.password:
            raise HTTPException(status_code=400, detail="이메일 또는 비밀번호가 올바르지 않습니다.")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"오류 발생: {str(e)}")
    finally:
        cursor.close()
        db.close()

    token = create_access_token(user["id"])
    return {"message": "로그인 성공", "email": req.email, "nickname": user["nickname"], "access_token": token}

# ───────────────────────────────────────────────
# 일정 API (JWT 인증 필요)
# ───────────────────────────────────────────────
@app.get("/schedules")
def get_schedules(date: date, user_id: int = Depends(get_current_user_id)):
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
            (user_id, date)
        )
        rows = cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"오류 발생: {str(e)}")
    finally:
        cursor.close()
        db.close()

    return {"schedules": rows}

@app.post("/schedules")
def create_schedule(req: ScheduleCreate, user_id: int = Depends(get_current_user_id)):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO schedules (user_id, title, start_time, end_time)
            VALUES (%s, %s, %s, %s) RETURNING id
            """,
            (user_id, req.title, req.start_time, req.end_time)
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

@app.patch("/schedules/{schedule_id}")
def update_schedule(schedule_id: int, req: ScheduleUpdate, user_id: int = Depends(get_current_user_id)):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "SELECT id FROM schedules WHERE id = %s AND user_id = %s",
            (schedule_id, user_id)
        )
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="일정을 찾을 수 없습니다.")

        updates = {k: v for k, v in req.dict().items() if v is not None}
        if not updates:
            raise HTTPException(status_code=400, detail="수정할 내용이 없습니다.")

        set_clause = ", ".join([f"{k} = %s" for k in updates.keys()])
        cursor.execute(
            f"UPDATE schedules SET {set_clause} WHERE id = %s",
            (*updates.values(), schedule_id)
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

@app.delete("/schedules/{schedule_id}")
def delete_schedule(schedule_id: int, user_id: int = Depends(get_current_user_id)):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "SELECT id FROM schedules WHERE id = %s AND user_id = %s",
            (schedule_id, user_id)
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

@app.patch("/schedules/{schedule_id}/done")
def toggle_done(schedule_id: int, user_id: int = Depends(get_current_user_id)):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "SELECT id, is_done FROM schedules WHERE id = %s AND user_id = %s",
            (schedule_id, user_id)
        )
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="일정을 찾을 수 없습니다.")

        new_done = not row["is_done"]
        cursor.execute(
            "UPDATE schedules SET is_done = %s WHERE id = %s",
            (new_done, schedule_id)
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

# ───────────────────────────────────────────────
# 설정 API (신규 추가 - JWT 인증 필요)
# ───────────────────────────────────────────────

@app.get("/settings")
def get_settings(user_id: int = Depends(get_current_user_id)):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM settings WHERE user_id = %s", (user_id,))
        row = cursor.fetchone()

        # 설정이 없으면 기본값으로 자동 생성
        if not row:
            cursor.execute(
                "INSERT INTO settings (user_id) VALUES (%s) RETURNING *",
                (user_id,)
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

@app.patch("/settings")
def update_settings(req: SettingsUpdate, user_id: int = Depends(get_current_user_id)):
    db = get_db()
    cursor = db.cursor()
    try:
        # 설정이 없으면 자동 생성
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
            (*updates.values(), user_id)
        )
        db.commit()

        # 변경된 설정 전체 반환
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