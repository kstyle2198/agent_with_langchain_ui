# 1. LangGraph 공식 베이스 이미지 사용
FROM langchain/langgraph-api:3.11

# 2. 작업 디렉토리 설정
WORKDIR /deps/app

# 3. requirements.txt 먼저 복사 및 설치 (캐시 최적화)
COPY requirements.txt .
RUN PYTHONDONTWRITEBYTECODE=1 uv pip install --system --no-cache-dir -r requirements.txt

# 4. 에이전트 코드 및 설정 파일 복사
COPY . .

# 5. 환경 변수 설정 (langgraph.json의 내용을 서버에 알려줌)
ENV LANGSERVE_GRAPHS='{"agent": "agent_code.agent:agent"}'

# 6. (선택사항) PYTHONPATH 설정 - 임포트 에러 방지
ENV PYTHONPATH=/deps/app