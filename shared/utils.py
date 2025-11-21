import requests
import os
import time
import threading

def register_agent(agent_name: str, port: int, skills: list):
    """
    Registers the agent with the Orchestrator using the Google A2A Agent Card format.
    """
    orchestrator_url = os.getenv("ORCHESTRATOR_URL", "http://orchestrator:8003")
    
    registration_data = {
        "name": agent_name,
        "description": f"Agent {agent_name} for Google Antigravity System",
        "url": f"http://{agent_name}:{port}",
        "version": "1.0.0",
        "provider": "Google Antigravity",
        "capabilities": {
            "streaming": True,
            "pushNotifications": False
        },
        "skills": skills
    }
    
    def _register():
        retries = 0
        while retries < 10:
            try:
                response = requests.post(f"{orchestrator_url}/register", json=registration_data)
                if response.status_code == 200:
                    print(f"Successfully registered {agent_name} with Orchestrator.")
                    return
            except Exception as e:
                print(f"Registration failed (attempt {retries+1}): {e}")
            
            time.sleep(5)
            retries += 1
        print(f"Failed to register {agent_name} after multiple attempts.")

    # Run in background to not block startup
    thread = threading.Thread(target=_register)
    thread.daemon = True
    thread.start()

def load_cars_data() -> dict:
    """Load static car dataset from shared/data/cars.json.
    Returns a dict with a list of cars and their suppliers/materials.
    """
    import json, os
    data_path = os.path.join(os.path.dirname(__file__), "data", "cars.json")
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading car data: {e}")
        return {"cars": []}

