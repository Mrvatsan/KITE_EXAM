import requests

BASE_URL = "http://127.0.0.1:8000/api"

def call(reg):
    resp = requests.get(f"{BASE_URL}/hall-ticket/?register_no={reg}")
    print(resp.status_code)
    try:
        print(resp.json())
    except:
        print(resp.text)

if __name__ == '__main__':
    call('711623UCS089')
