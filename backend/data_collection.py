import requests

def search_wikipedia(query):
    """
    Use Wikipedia's public API to fetch a summary for a competitor.
    """
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        print(f"DEBUG: Wikipedia response: {data}")

        result = {
            "Title": data.get('title', ''),
            "Extract": data.get('extract', ''),
            "ContentURL": data.get('content_urls', {}).get('desktop', {}).get('page', '')
        }

        return result

    except Exception as e:
        print(f"ERROR: {e}")
        return {"error": str(e)}
