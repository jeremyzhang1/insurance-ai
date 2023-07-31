import requests

base_url = "http://localhost:5000"

next_endpoint = "/next"

data = {
    "prompt": "What is the capital of France?",
}

try:
    response = requests.post(f"{base_url}{next_endpoint}", json=data)

    response.raise_for_status()

    response_data = response.json()
    if response_data.get("status") == 200:
        answer = response_data.get("answer")
        print("AI Answer:", answer)
    else:
        print("Error:", response_data.get("message", "Unknown error"))
except requests.exceptions.RequestException as e:
    print("Error making the request:", str(e))
except ValueError:
    print("Error decoding JSON response.")
