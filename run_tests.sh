#!/bin/bash

# Question 2: Graph Exploration
echo "Running Question 2..."
curl -X POST http://localhost:3000/api/copilotkit \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Show me the full Bill of Materials for the V6 Engine, including all sub-components and their suppliers."}]}' \
  > response_q2.json

# Question 3: Comparative Analysis
echo "Running Question 3..."
curl -X POST http://localhost:3000/api/copilotkit \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Compare the supply chain risks for Denso in Japan versus Magna in Canada."}]}' \
  > response_q3.json

# Question 4: PESTEL Risk Analysis
echo "Running Question 4..."
curl -X POST http://localhost:3000/api/copilotkit \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "What is the impact of recent trade tariffs on Hitachi'\''s ability to supply Electronics from Japan?"}]}' \
  > response_q4.json

# Question 5: Edge Case
echo "Running Question 5..."
curl -X POST http://localhost:3000/api/copilotkit \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Analyze the risk for Tesla in Mars."}]}' \
  > response_q5.json

echo "All tests completed."
