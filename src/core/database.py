import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is required")


# DATABASE_URL이 postgresql:// 로 시작한다면 postgresql+asyncpg:// 로 변경
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

class Base(DeclarativeBase):
    pass

# 비동기 엔진 생성
engine = create_async_engine(DATABASE_URL, echo=False)

# 비동기 세션 팩토리 생성 (나중에 API에서 DB 연결할 때 사용)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

