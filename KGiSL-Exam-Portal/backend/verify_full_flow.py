import requests
import pandas as pd
import io

BASE_URL = "http://127.0.0.1:8000/api"

# 1. Create Dummy CSV
def create_dummy_excel():
    data = {
        'register_number': ['2024001'],
        'name': ['Test Student'],
        'password': ['password123'],
        'room_number': ['101'],
        'seat_number': ['A1'],
        # Add Hall Ticket fields that might be expected if validation is strict
    }
    
    df = pd.DataFrame(data)
    excel_buffer = io.BytesIO()
    # Use xlsxwriter engine
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    
    excel_buffer.seek(0)
    return excel_buffer

def verify_full_flow():
    print("=== STARTING VERIFICATION ===")
    
    # 1. Admin Login
    print("\n1. Admin Login...")
    admin_creds = {"username": "Kgkite", "password": "Kgkite@123", "role": "admin"}
    try:
        resp = requests.post(f"{BASE_URL}/login/", json=admin_creds)
        if resp.status_code != 200:
            print(f"❌ Admin Login Failed: {resp.status_code} - {resp.text}")
            return
        print("✅ Admin Login Success")
        
        # 2. Upload Excel
        print("\n2. Uploading Student Data (Excel)...")
        file_buffer = create_dummy_excel()
        files = {'file': ('students.xlsx', file_buffer, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
        
        # Note: Upload might require auth headers if protected? 
        # Checking views.py: DatasetUploadView usually isn't protected in this simple app, 
        # or maybe it doesn't check token. Let's try without token first.
        # If it fails, we might need cookie/session? 
        # Looking at LoginView, it returns a dummy token.
        
        if upload_resp.status_code not in [200, 201]:
             print(f"❌ Upload Failed: {upload_resp.status_code} - {upload_resp.text}")
             return
             
        print("✅ Upload Success")
        upload_data = upload_resp.json()
        dataset_id = upload_data.get('dataset_id')
        
        if dataset_id:
            print(f"\n2.5. Activating Dataset {dataset_id}...")
            # Toggle dataset to active
            toggle_resp = requests.post(f"{BASE_URL}/datasets/{dataset_id}/toggle/")
            if toggle_resp.status_code == 200:
                print("✅ Dataset Activated")
            else:
                print(f"❌ Verification Warn: Could not activate dataset: {toggle_resp.status_code}")
        else:
            print("⚠️ No dataset_id returned, skipping activation (might fail login)")
        
        # 3. Student Login
        print("\n3. Student Login...")
        student_creds = {"username": "2024001", "password": "password123", "role": "student"}
        resp = requests.post(f"{BASE_URL}/login/", json=student_creds)
        if resp.status_code != 200:
            print(f"❌ Student Login Failed: {resp.status_code} - {resp.text}")
            return
        print("✅ Student Login Success")
        
        # 4. Fetch Hall Ticket
        print("\n4. Fetching Hall Ticket...")
        # GET /api/hall-ticket/?register_no=...
        ht_resp = requests.get(f"{BASE_URL}/hall-ticket/?register_no=2024001")
        
        if ht_resp.status_code == 200:
            print("✅ HALL TICKET FETCHED SUCCESSFULLY!")
            data = ht_resp.json()
            print(json.dumps(data, indent=2))
        else:
            print(f"❌ Hall Ticket Fetch Failed: {ht_resp.status_code} - {ht_resp.text}")

    except Exception as e:
        print(f"❌ EXCEPTION: {e}")

if __name__ == "__main__":
    verify_full_flow()
