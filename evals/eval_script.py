import requests
import os
import json
from openai import OpenAI

# Configuration
ORCHESTRATOR_URL = "http://localhost:8003"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

test_cases = [
    {
        "query": "What is the risk score for Bosch in Germany?",
        "expected_agent": "supplier-agent",
        "expected_concepts": ["risk", "PESTEL", "Bosch", "Germany"]
    },
    {
        "query": "Find details for V6 Engine part including price.",
        "expected_agent": "materials-agent",
        "expected_concepts": ["OEM", "price", "V6 Engine"]
    },
    {
        "query": "Show me the Bill of Materials for the Sedan Car.",
        "expected_agent": "bom-agent",
        "expected_concepts": ["BOM", "children", "Sedan Car"]
    }
]

def evaluate_response(query, response, expected_concepts):
    """
    Uses LLM to grade the response.
    """
    prompt = f"""
    Query: {query}
    Response: {response}
    Expected Concepts: {expected_concepts}
    
    Grade the response on a scale of 0-10 based on whether it answers the query and contains the expected concepts.
    Return JSON: {{ "score": <int>, "reason": "<string>" }}
    """
    
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(completion.choices[0].message.content)

def run_evals():
    print("Starting Evals...")
    results = []
    
    for test in test_cases:
        print(f"Testing: {test['query']}")
        try:
            # Send query to Orchestrator
            resp = requests.post(f"{ORCHESTRATOR_URL}/chat", json={"message": test['query']})
            if resp.status_code == 200:
                data = resp.json()
                output = data.get("response", "")
                
                # Grade
                grade = evaluate_response(test['query'], output, test['expected_concepts'])
                
                result = {
                    "query": test['query'],
                    "response_preview": output[:100] + "...",
                    "score": grade["score"],
                    "reason": grade["reason"]
                }
                results.append(result)
                print(f"Score: {grade['score']}/10 - {grade['reason']}")
            else:
                print(f"Error: {resp.status_code}")
                results.append({"query": test['query'], "error": f"HTTP {resp.status_code}"})
                
        except Exception as e:
            print(f"Exception: {e}")
            results.append({"query": test['query'], "error": str(e)})
            
    # Save results
    with open("eval_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("Evals Completed. Results saved to eval_results.json")

if __name__ == "__main__":
    run_evals()
