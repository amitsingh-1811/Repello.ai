import requests
from app.config import SERPAPI_KEY
from app.config import SERPAPI_SEARCH_ENDPOINT

def search_web(query, count=3):
    try:
        params = {
            "q": query,
            "num": count,
            "responseFilter": "Webpages",
            "api_key": SERPAPI_KEY
        }

        response = requests.get(SERPAPI_SEARCH_ENDPOINT, params=params)
        response.raise_for_status()

        data = response.json()

        results = data.get("organic_results")
        return results

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error: {req_err}")
    except ValueError as json_err:
        print(f"Error decoding JSON: {json_err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return None