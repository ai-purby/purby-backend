# Purby Backend

음성으로 대화하는 스마트 디스플레이 **Purby**의 FastAPI 기반 메인서버입니다.

## 기술 스택

| 구분 | 기술 |
| --- | --- |
| 언어 | Python 3.12 |
| API 프레임워크 | FastAPI |
| 애플리케이션 서버 | Uvicorn |

## 빠른 시작

macOS·Linux 기준입니다. `purby-backend` 폴더에서 실행하세요.

### 1. 가상환경 준비

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. 패키지 설치

```bash
python -m pip install -r requirements.txt
```

### 3. 개발 서버 실행

```bash
python -m uvicorn app.main:app --reload
```

코드를 저장하면 자동으로 반영됩니다. 서버를 종료하려면 `Ctrl+C`를 누르세요.

### 4. 실행 확인

| 주소 | 설명 |
| --- | --- |
| [헬스 체크](http://127.0.0.1:8000/api/health) | 서버 응답 확인 |
| [API 문서](http://127.0.0.1:8000/docs) | API 목록 확인 및 요청 테스트 |

헬스 체크 응답:

```json
{"status": "ok"}
```

## 폴더 구조

```text
purby-backend/
├── app/
│   ├── __init__.py
│   └── main.py          # FastAPI 앱 및 헬스 체크 API
├── .gitignore
├── README.md
└── requirements.txt     # 패키지 목록 및 버전
```
