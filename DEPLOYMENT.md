# PPT to Script - Railway 배포 가이드

## Railway에 배포하기

### 1. Railway 계정 준비
1. [Railway](https://railway.app/)에 가입하세요
2. GitHub 계정과 연동하세요

### 2. 프로젝트 배포

#### 방법 1: GitHub 연동 (권장)
1. 이 프로젝트를 GitHub 리포지토리에 푸시하세요
2. Railway 대시보드에서 "New Project" 클릭
3. "Deploy from GitHub repo" 선택
4. 리포지토리 선택
5. Railway가 자동으로 Dockerfile을 감지하고 배포합니다

#### 방법 2: Railway CLI 사용
```bash
# Railway CLI 설치
npm i -g @railway/cli

# 로그인
railway login

# 프로젝트 초기화
railway init

# 배포
railway up
```

### 3. 환경 변수 설정 (선택사항)
Railway 대시보드에서 다음 환경 변수를 설정할 수 있습니다:
- `PORT`: Railway가 자동으로 설정 (기본값: 8080)
- `LIBREOFFICE_URL`: Docker LibreOffice 사용 시 (선택사항)

### 4. 도메인 설정
- Railway는 자동으로 `https://<your-app>.up.railway.app` 형식의 도메인을 제공합니다
- Settings에서 커스텀 도메인을 추가할 수 있습니다

## 사용 방법

1. 배포된 웹사이트에 접속하세요
2. PPT/PPTX 파일을 업로드하세요
3. API 키를 입력하세요:
   - OpenAI: https://platform.openai.com/api-keys
   - Anthropic: https://console.anthropic.com/
   - Google: https://ai.google.dev/
4. 선택사항으로 추가 지시사항을 입력하세요
5. "스크립트 생성하기" 버튼을 클릭하세요
6. 생성된 스크립트를 확인하고 JSON으로 다운로드하세요

## 로컬 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# LibreOffice 설치 확인
soffice --version

# 서버 실행
python web_app.py

# 브라우저에서 열기
# http://localhost:8080
```

## 주의사항

1. **파일 크기 제한**: 최대 50MB까지 업로드 가능합니다
2. **API 키 보안**: API 키는 서버로 전송되지만 저장되지 않습니다. 매번 입력해야 합니다
3. **처리 시간**: 슬라이드 수에 따라 몇 분이 걸릴 수 있습니다
4. **비용**: LLM API 사용량에 따라 비용이 발생합니다

## 지원되는 LLM

- **OpenAI**: gpt-4o, gpt-4o-mini, gpt-4-turbo 등
- **Anthropic**: claude-3-5-sonnet-latest, claude-3-opus-latest 등
- **Google**: gemini-2.0-flash-exp, gemini-1.5-pro 등

## 문제 해결

### LibreOffice 오류
Railway 배포 시 LibreOffice가 자동으로 설치됩니다. 로컬 실행 시:
- **Windows**: [LibreOffice 다운로드](https://www.libreoffice.org/)
- **Mac**: `brew install libreoffice`
- **Linux**: `sudo apt-get install libreoffice`

### API 키 오류
- API 키가 유효한지 확인하세요
- API 키에 충분한 크레딧/할당량이 있는지 확인하세요

### 업로드 실패
- 파일이 PPT 또는 PPTX 형식인지 확인하세요
- 파일 크기가 50MB 이하인지 확인하세요
