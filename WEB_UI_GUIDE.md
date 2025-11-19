# PPT to Script - 웹 UI 가이드

## 개요

PPT to Script는 PowerPoint 파일을 업로드하여 자동으로 발표 스크립트를 생성하는 웹 애플리케이션입니다.

## 주요 기능

✅ PPT/PPTX 파일 업로드 (최대 50MB)
✅ 다양한 AI 모델 지원 (OpenAI, Anthropic, Google)
✅ 슬라이드별 스크립트 자동 생성
✅ JSON 형식으로 다운로드
✅ 한국어 사용자 인터페이스
✅ 커스텀 지시사항 추가 가능

## 로컬 실행 방법

### Windows
```bash
# 의존성 설치
pip install -r requirements.txt

# 웹 서버 실행 (방법 1 - 배치 파일 사용)
run_web.bat

# 웹 서버 실행 (방법 2 - 직접 실행)
python web_app.py
```

### Mac/Linux
```bash
# 의존성 설치
pip install -r requirements.txt

# 웹 서버 실행 (방법 1 - 쉘 스크립트 사용)
./run_web.sh

# 웹 서버 실행 (방법 2 - 직접 실행)
python web_app.py
```

서버가 시작되면 브라우저에서 http://localhost:8080 으로 접속하세요.

## Railway 배포 방법

### 사전 준비
1. GitHub 계정
2. Railway 계정 (https://railway.app)

### 배포 단계

1. **GitHub에 코드 푸시**
   ```bash
   git add .
   git commit -m "Add web UI for PPT to Script"
   git push origin main
   ```

2. **Railway에서 배포**
   - Railway 대시보드 접속
   - "New Project" 클릭
   - "Deploy from GitHub repo" 선택
   - 리포지토리 선택
   - Railway가 자동으로 Dockerfile을 감지하고 빌드/배포

3. **배포 완료**
   - Railway가 자동으로 URL 생성 (예: `https://your-app.up.railway.app`)
   - 생성된 URL로 접속하여 사용

### Railway CLI를 통한 배포 (선택사항)

```bash
# Railway CLI 설치
npm install -g @railway/cli

# Railway 로그인
railway login

# 프로젝트 초기화
railway init

# 배포
railway up
```

## 사용 방법

1. **PPT 파일 업로드**
   - "파일을 선택하거나 드래그하세요" 영역 클릭
   - PPT 또는 PPTX 파일 선택

2. **LLM 설정**
   - LLM 선택: OpenAI, Anthropic, Google 중 선택
   - 모델: 사용할 모델 이름 입력
     - OpenAI: `gpt-4o-mini`, `gpt-4o`, `gpt-4-turbo`
     - Anthropic: `claude-3-5-sonnet-latest`, `claude-3-opus-latest`
     - Google: `gemini-2.0-flash-exp`, `gemini-1.5-pro`

3. **API 키 입력**
   - 선택한 LLM의 API 키 입력
   - API 키 발급 방법:
     - OpenAI: https://platform.openai.com/api-keys
     - Anthropic: https://console.anthropic.com/
     - Google: https://ai.google.dev/

4. **추가 지시사항 (선택)**
   - 전체 슬라이드에 공통으로 적용할 요구사항 입력
   - 예: "대학 수의 발생학 관점에서 간단히 설명해주세요"

5. **스크립트 생성**
   - "스크립트 생성하기" 버튼 클릭
   - 처리 완료까지 대기 (슬라이드 수에 따라 몇 분 소요)

6. **결과 확인 및 다운로드**
   - 생성된 스크립트를 슬라이드별로 확인
   - "JSON 다운로드" 버튼으로 결과 저장

## 파일 구조

```
ppt2script/
├── web_app.py              # Flask 웹 애플리케이션
├── templates/
│   └── index.html          # 웹 UI (한국어)
├── requirements.txt        # Python 의존성
├── Dockerfile             # Docker 컨테이너 설정
├── run_web.bat            # Windows 실행 스크립트
├── run_web.sh             # Mac/Linux 실행 스크립트
├── DEPLOYMENT.md          # 배포 가이드
└── WEB_UI_GUIDE.md        # 이 파일
```

## 기술 스택

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript (바닐라)
- **AI Models**: OpenAI GPT, Anthropic Claude, Google Gemini
- **Document Processing**: LibreOffice, PyMuPDF
- **Deployment**: Docker, Railway

## 문제 해결

### LibreOffice 오류
**증상**: "LibreOffice가 설치되지 않았습니다" 오류

**해결방법**:
- **Windows**: https://www.libreoffice.org/ 에서 다운로드 및 설치
- **Mac**: `brew install libreoffice`
- **Linux**: `sudo apt-get install libreoffice`
- **Docker/Railway**: 자동으로 설치됨 (Dockerfile에 포함)

### API 키 오류
**증상**: API 요청 실패

**해결방법**:
- API 키가 올바른지 확인
- API 키에 충분한 크레딧이 있는지 확인
- 올바른 LLM 제공자를 선택했는지 확인

### 파일 업로드 실패
**증상**: 파일 업로드 시 오류

**해결방법**:
- 파일이 PPT 또는 PPTX 형식인지 확인
- 파일 크기가 50MB 이하인지 확인
- 파일이 손상되지 않았는지 확인

### 처리 시간이 너무 오래 걸림
**증상**: 스크립트 생성이 매우 느림

**원인**: 슬라이드 수가 많거나 API 응답이 느릴 수 있음

**해결방법**:
- 슬라이드 수가 적은 파일로 테스트
- 더 빠른 모델 사용 (예: `gpt-4o-mini`, `gemini-2.0-flash-exp`)
- 네트워크 연결 확인

## 비용 안내

이 애플리케이션은 AI API를 사용하므로 비용이 발생합니다:

- **OpenAI GPT-4o-mini**: 슬라이드당 약 $0.01-0.02
- **Anthropic Claude**: 슬라이드당 약 $0.02-0.03
- **Google Gemini Flash**: 슬라이드당 약 $0.001-0.005

실제 비용은 슬라이드 내용과 모델에 따라 다를 수 있습니다.

## 보안 주의사항

⚠️ **API 키 보안**:
- API 키는 서버로 전송되지만 저장되지 않습니다
- 매 세션마다 새로 입력해야 합니다
- 공개적으로 공유하지 마세요

⚠️ **파일 보안**:
- 업로드된 파일은 처리 후 자동으로 삭제됩니다
- 민감한 정보가 포함된 PPT는 주의해서 업로드하세요

## 추가 정보

- **상세 배포 가이드**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **CLI 사용법**: [README.md](README.md)
- **소스 코드**: GitHub 리포지토리 참조

## 지원

문제가 발생하거나 기능 요청이 있으시면 GitHub Issues를 통해 알려주세요.
