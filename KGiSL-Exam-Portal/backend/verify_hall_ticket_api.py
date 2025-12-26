import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_hall_ticket_flow():
    print("1. Testing Student Login...")
    login_data = {
        "username": "2024001",
        "password": "password123",
        "role": "student"
    }
    
    try:
        # 1. Login
        response = requests.post(f"{BASE_URL}/login/", json=login_data)
        
        if response.status_code == 200:
            print("✅ Login Successful")
            print(f"Response: {response.json()}")
            
            # 2. Fetch Hall Ticket
            print("\n2. Fetching Hall Ticket Data...")
            reg_no = login_data['username']
            hall_ticket_response = requests.get(f"{BASE_URL}/hall-ticket/?register_no={reg_no}")
            
            if hall_ticket_response.status_code == 200:
                print("✅ Hall Ticket API Success!")
                data = hall_ticket_response.json()
                print(f"Student: {data.get('student', {}).get('name')}")
                print(f"Department: {data.get('student', {}).get('department')}")
                print(f"Semesters found: {list(data.get('semesters', {}).keys())}")
            else:
                print(f"❌ Hall Ticket API Failed: {hall_ticket_response.status_code}")
                print(hall_ticket_response.text)
        else:
            print(f"❌ Login Failed: {response.status_code}")
            print(response.text)
            print("\nNOTE: Login failure might be due to missing Student data in DB. "
                  "Try logging in as Admin and uploading the dataset first.")

    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    test_hall_ticket_flow()
