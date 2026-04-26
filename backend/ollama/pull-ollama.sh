./bin/ollama serve &

pid=$!

sleep 5

echo "Pulling Ollama models"

ollama pull bge-m3:latest

wait $pid
