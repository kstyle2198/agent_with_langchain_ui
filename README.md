# Agent with Langchain&Langgraph

---

# 1. 프론트엔드 실행명령
```bash
cd agent-chat-ui 
pnpm dev
```

# 2. 백엔드 도커 실행 명령

```bash

# 1. 컨테이너, 볼륨, 네트워크까지 모두 삭제 (이전 작업 완전 삭제 필요시)
docker-compose down -v --remove-orphans

# 볼륨은 유지하면서 컨테이너 삭제
docker-compose down

# 2. 깨끗한 상태에서 다시 실행
docker-compose up -d --build

# 3. 로그 확인
docker-compose logs -f langgraph-api

# 5. API document 
http://127.0.0.1:8123/docs


```

```python
# 단순 개발용 퀵 명령은 
langgraph dev
```

## 백엔드 폴더 구조

```bash
|   .env
|   .gitignore
|   .python-version
|   docker-compose.yml
|   Dockerfile
|   langgraph.json
|   pyproject.toml
|   README.md
|   requirements.txt
|   structure.txt
|   uv.lock
|           
+---agent_code
|   |   agent.py
|   |   __init__.py
|   |   
|   +---utils
|   |   |   setlogger.py
|   |   |   __init__.py

```


# 3. langgraph.json 
- langgraph dev 명령시 langgraph.json 세팅에 따라 실행됨
- 아래 예시에서 프론트 연결시 중요한 Graph ID는 "graphs" 안에 있는 "agent" 이다. 
  (소스코드의 구조가 변경되면 langgraph.json 파일도 그에 맞춰서 수정 필요)

```json
{
  "dependencies": ["./agent_code", "."],
  "graphs": {
    "agent": "agent_code.agent:agent"
  },
  "env": ".env"
}
```


# 4. 기본 Postgres RDB 사용시 docker compose 파일

```yaml
services:
  # 1. LangGraph API 서버
  langgraph-api:
    build: .
    image: my-langgraph-app:v7
    ports:
      - "8123:8123"
    environment:
      # [수정] 외부 DB 주소로 변경
      # 만약 DB가 같은 PC(로컬)에서 동작 중이라면 'host.docker.internal'을 사용하세요.
      - DATABASE_URI=postgres://postgres:1234@host.docker.internal:5432/postgres
      - LANGGRAPH_POSTGRES_URI=postgres://postgres:1234@host.docker.internal:5432/postgres
      - REDIS_URI=redis://redis:6379

      - GROQ_API_KEY=${GROQ_API_KEY}
      - TAVILY_API_KEY=${TAVILY_API_KEY}
      - LANGSMITH_API_KEY=${LANGSMITH_API_KEY} 
      - LOG_LEVEL=debug
      - LANGGRAPH_DEBUG=1
      - PYTHONPATH=/deps/app
      - LANGGRAPH_GRPC_READY_TIMEOUT=120
      - HOST=0.0.0.0
      - PORT=8123

    volumes:
      - .:/deps/app 
    
    networks:
      - langgraph-net
    
    extra_hosts:
      - "host.docker.internal:host-gateway" # 컨테이너 내부에서 로컬 호스트에 접근하기 위함

    depends_on:
      # postgres 의존성 제거
      redis:
        condition: service_healthy

  # 2. 작업 큐 관리용 Redis
  redis:
    image: redis:7
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - langgraph-net

networks:
  langgraph-net:
    driver: bridge

# pgdata 볼륨 정의 삭제
```

---

## 제선생 참고자료
![alt text](image.png)
![alt text](image-1.png)