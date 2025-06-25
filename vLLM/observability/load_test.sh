#!/bin/bash

for i in $(seq 1 100); do
  echo "[$i] Sending request..."
  curl -s -X POST http://localhost:8002/rag \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{"query": "What is IBM?"}'
  echo -e "\n"
  sleep 10s
done
