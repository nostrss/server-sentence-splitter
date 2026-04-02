# Sentence Splitter Server

ML 기반 문장 분리 마이크로서비스입니다. [wtpsplit-lite](https://github.com/bminixhofer/wtpsplit) 모델(`sat-3l-sm`)을 사용하여 텍스트를 문장 단위로 분리합니다.

## 기술 스택

- **런타임**: Python 3.11
- **프레임워크**: FastAPI + Uvicorn
- **ML 모델**: wtpsplit-lite (SaT - Segment any Text, ONNX Runtime)

## API

### POST `/split`

텍스트를 문장 단위로 분리합니다.

**Request**

```json
{
  "text": "안녕하세요. 오늘 날씨가 좋습니다. 산책하러 가고 싶어요.",
  "language": ""
}
```

| 필드       | 타입   | 필수 | 설명                     |
| ---------- | ------ | ---- | ------------------------ |
| `text`     | string | O    | 분리할 텍스트            |
| `language` | string | X    | 언어 코드 (기본값: `""`) |

**Response**

```json
{
  "sentences": ["안녕하세요.", "오늘 날씨가 좋습니다.", "산책하러 가고 싶어요."]
}
```

### GET `/health`

서비스 상태를 확인합니다.

**Response**

```json
{
  "status": "ok"
}
```

## 로컬 실행

### Python 직접 실행

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8001
```

### Docker

```bash
docker build -t sentence-splitter .
docker run -p 8001:8001 sentence-splitter
```

서버가 실행되면 http://localhost:8001 에서 접근 가능합니다.

## 테스트

```bash
# 헬스 체크
curl http://localhost:8001/health

# 문장 분리
curl -X POST http://localhost:8001/split \
  -H "Content-Type: application/json" \
  -d '{"text": "안녕하세요. 오늘 날씨가 좋습니다. 산책하러 가고 싶어요."}'
```

## Google Cloud Run 배포

### 사전 준비

- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) 설치
- `gcloud auth login`으로 인증
- `gcloud config set project <PROJECT_ID>`로 프로젝트 설정

### 배포

```bash
gcloud run deploy sentence-splitter \
  --source . \
  --region asia-northeast3 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --port 8001
```

> ML 모델 로딩에 메모리가 필요하므로 최소 2Gi를 권장합니다.

### 배포 URL

```
https://sentence-splitter-588497594238.asia-northeast3.run.app
```

## 프로젝트 구조

```
.
├── main.py              # FastAPI 애플리케이션 및 API 엔드포인트
├── requirements.txt     # Python 의존성
├── Dockerfile           # 컨테이너 빌드 설정
├── package.json         # Node.js 의존성 (클라이언트 연동용)
└── README.md
```
