# Agent with Langchain&Langgraph



1. 프론트엔드 실행명령
```
cd agent-chat-ui 
pnpm dev
```

2. 백엔드 실행명령
```
cd backend
.venv\scripts\activate
# 개발용
langgraph dev --host localhost --port 2024   
# langgraph dev 디폴트 URL은 http://localhost:2024 임
```


3. langgraph.json 
- langgraph dev 명령시 langgraph.json 세팅에 따라 실행됨
- 아래 예시에서 프론트 연결시 중요한 Graph ID는 "graphs" 안에 있는 "agent" 이다. 
  (소스코드의 구조가 변경되면 langgraph.json 파일도 그에 맞춰서 수정 필요)

```
{
  "dependencies": ["."],
  "graphs": {
    "agent": "./src/agent.py:agent"
  },
  "env": ".env"
}
```


5. Production-level에서 고려할 사항..

- langgraph dev를 사용은 적합하지 않다.
- fastapi와 langserve를 사용해야 한다.
- 근데 이러면.. 엔드포인트가 달라져서.. langchain-chat-ui와 자동으로 연결되지 않는다. (langgraph dev에서는 자동으로 연결)
- 결국 프론트에서 엔드포인트 멥핑 로직을 수정해야 한다.