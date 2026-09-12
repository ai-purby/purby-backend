# Purby Backend

음성으로 대화하는 스마트 디스플레이 **Purby**의 FastAPI 기반 메인서버입니다.

## 기술 스택

| 구분 | 기술 |
| --- | --- |
| 언어 | Python 3.12 |
| API 프레임워크 | FastAPI |
| 애플리케이션 서버 | Uvicorn |
| 개발 환경 | Docker · Docker Compose |

## 빠른 시작

Docker와 Docker Compose가 설치되어 있어야 합니다. macOS에서는 Docker Desktop을 실행한 뒤, `purby-backend` 폴더에서 아래 명령을 실행하세요.

### 1. 개발 서버 실행

```bash
docker compose up --build
```

이미지를 빌드하고 컨테이너 안에서 Uvicorn을 실행합니다. 로컬 가상환경 활성화나 패키지 설치는 필요하지 않습니다. 기존 서버가 8000번 포트를 사용 중이라면 먼저 종료하세요.

`app/`의 코드를 수정하고 저장하면 서버가 자동으로 다시 불러옵니다. 서버를 종료하려면 `Ctrl+C`를 누르세요.

### 2. 실행 확인

| 주소 | 설명 |
| --- | --- |
| [헬스 체크](http://127.0.0.1:8000/api/health) | 서버 응답 확인 |
| [API 문서](http://127.0.0.1:8000/docs) | API 목록 확인 및 요청 테스트 |

헬스 체크 응답:

```json
{"status": "ok"}
```

현재 포트 설정은 개발 컴퓨터에서의 접속만 허용합니다.

## 개발 명령

| 작업 | 명령 |
| --- | --- |
| 개발 서버 실행 | `docker compose up` |
| 백그라운드 실행 | `docker compose up -d` |
| 로그 확인 | `docker compose logs -f backend` |
| 패키지 목록 변경 후 재빌드·실행 | `docker compose up --build` |
| 컨테이너 및 Compose 네트워크 제거 | `docker compose down` |

패키지를 추가하거나 버전을 변경하면 `requirements.txt`에 반영하고 이미지를 다시 빌드하세요. 실행 중인 컨테이너에만 설치한 패키지는 컨테이너 재생성 시 유지되지 않습니다.

## Docker 없이 직접 실행

Python 3.12가 설치된 macOS·Linux에서 실행할 수 있습니다. Docker 개발 서버와 동시에 실행하면 8000번 포트가 충돌하므로 하나만 실행하세요.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

## 폴더 구조

```text
purby-backend/
├── app/
│   ├── __init__.py
│   └── main.py          # FastAPI 앱 및 헬스 체크 API
├── .dockerignore       # Docker 빌드 제외 규칙
├── .gitignore
├── compose.yaml        # Docker 개발 실행 설정
├── Dockerfile          # 백엔드 이미지 빌드 설정
├── README.md
└── requirements.txt    # 패키지 목록 및 버전
```
