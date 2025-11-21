import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from pydantic import BaseModel

# Initialize Gemini
google_api_key = os.getenv("GOOGLE_API_KEY")
if google_api_key:
    genai.configure(api_key=google_api_key)

# Use a model that supports tools/grounding
# gemini-1.5-flash is a good default for speed/cost
model = genai.GenerativeModel('gemini-1.5-flash')

class PartDetails(BaseModel):
    part_name: str
    oem_status: str # "OEM" or "Aftermarket"
    manufacturer: str
    origin_country: str
    average_price: str
    source_url: str

def get_search_context(part_name: str) -> dict:
    """
    Uses Gemini with Google Search Grounding to find details about a car part.
    Returns a dict containing the query and the grounded response text.
    """
    if not google_api_key:
        return {"error": "GOOGLE_API_KEY not set."}
        
    query = f"Find details for car part '{part_name}': OEM status, manufacturer, country of origin, and average price."
    
    try:
        # Use the tools argument to enable Google Search
        response = model.generate_content(
            query,
            tools='google_search_retrieval'
        )
        
        # The response text will contain the grounded answer
        return {"query": query, "result": response.text}
    except Exception as e:
        return {"error": f"Error searching with Gemini: {e}"}

# Legacy function signature for compatibility, but we'll rely on the LLM in main.py to parse the context
def search_part_details(part_name: str) -> PartDetails:
    """
    Searches for part details. Returns a placeholder object.
    The actual extraction happens in the main agent loop using the context.
    """
    return PartDetails(
        part_name=part_name,
        oem_status="See Context",
        manufacturer="See Context",
        origin_country="See Context",
        average_price="See Context",
        source_url="Google Search"
    )
