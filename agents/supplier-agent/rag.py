import os
import requests
import google.generativeai as genai
import json
from datetime import datetime

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def fetch_world_bank_data(country_code: str):
    """
    Fetches economic data from World Bank API.
    Using a public API endpoint for GDP and Inflation.
    """
    # Example: GDP (NY.GDP.MKTP.CD) and Inflation (FP.CPI.TOTL.ZG)
    # This is a simplified implementation.
    base_url = "http://api.worldbank.org/v2/country"
    indicators = ["NY.GDP.MKTP.CD", "FP.CPI.TOTL.ZG"]
    data = {}
    
    for indicator in indicators:
        try:
            url = f"{base_url}/{country_code}/indicator/{indicator}?format=json&per_page=1&date=2022"
            response = requests.get(url)
            if response.status_code == 200:
                raw = response.json()
                if len(raw) > 1 and raw[1]:
                    data[indicator] = raw[1][0].get("value")
        except Exception as e:
            print(f"Error fetching WB data for {indicator}: {e}")
            
    return data

def fetch_wto_data(country_name: str):
    """
    Fetches trade data from WTO. 
    Since WTO API is complex, we will simulate this with a search or simplified retrieval 
    if a direct simple public endpoint isn't easily available without auth.
    For this demo, we'll return a stub based on the country.
    """
    # Stubbed for reliability in demo unless we have a specific WTO API key/endpoint ready.
    # In a real scenario, we would hit api.wto.org
    return {
        "status": "Active Member",
        "tariffs": "Standard MFN",
        "trade_balance": "Available in paid API"
    }

def generate_pestel_analysis(supplier_name: str, country: str):
    """
    Generates PESTEL analysis using Gemini based on fetched data.
    """
    # 1. Fetch Data
    # Map country name to ISO code (simplified)
    country_map = {"Germany": "DE", "Japan": "JP", "USA": "US", "China": "CN", "India": "IN"}
    country_code = country_map.get(country, "US") 
    
    wb_data = fetch_world_bank_data(country_code)
    wto_data = fetch_wto_data(country)
    
    # 2. Construct Prompt
    prompt = f"""
    You are a Supply Chain Risk Analyst. Perform a PESTEL analysis for a supplier named '{supplier_name}' located in '{country}'.
    
    Use the following real-time economic data:
    - World Bank Data: {json.dumps(wb_data)}
    - WTO Trade Status: {json.dumps(wto_data)}
    
    Analyze the following factors:
    1. Political: Stability, trade policies.
    2. Economic: GDP, inflation, exchange rates.
    3. Social: Labor market, demographics.
    4. Technological: Innovation, infrastructure.
    5. Environmental: Regulations, climate risks.
    6. Legal: Labor laws, IP protection.
    
    Output the result as a JSON object with the following structure:
    {{
        "risk_score": <integer 0-100, where 100 is high risk>,
        "summary": "<short summary string>",
        "pestel_breakdown": {{
            "political": "<details>",
            "economic": "<details>",
            ...
        }}
    }}
    Do not include markdown formatting like ```json. Just return the raw JSON string.
    """
    
    # 3. Call Gemini
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt)
    
    try:
        # Clean response if needed
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:-3]
        return json.loads(text)
    except Exception as e:
        print(f"Error parsing Gemini response: {e}")
        return {
            "risk_score": 50,
            "summary": "Error generating analysis. Returning default neutral score.",
            "pestel_breakdown": {}
        }
