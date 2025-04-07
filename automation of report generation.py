import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import os

MOBSF_SERVER = "http://127.0.0.1:8000"
MOBSF_API_KEY = '7901f51039b4ec0664603789f56e31e41c721dd033b836f15f3d5c62a31f49d7'
APK_FOLDER_PATH = r'apps2'  # Path to the folder containing APK files

def upload_apk(file_path):
    print(f"Uploading APK: {file_path}")
    with open(file_path, 'rb') as file:
        files = {'file': (os.path.basename(file_path), file, 'application/octet-stream')}
        headers = {'Authorization': MOBSF_API_KEY}
        response = requests.post(f'{MOBSF_SERVER}/api/v1/upload', files=files, headers=headers)
        return response.json()

def scan_apk(hash_value):
    print("Scanning APK")
    data = {'hash': hash_value}
    headers = {'Authorization': MOBSF_API_KEY}
    response = requests.post(f'{MOBSF_SERVER}/api/v1/scan', data=data, headers=headers)
    return response.json()

def download_pdf_report(hash_value, app_name):
    print(f"Downloading PDF Report for: {app_name}")
    data = {'hash': hash_value}
    headers = {'Authorization': MOBSF_API_KEY}
    response = requests.post(f'{MOBSF_SERVER}/api/v1/download_pdf', data=data, headers=headers, stream=True)
    with open(f"{app_name}_report.pdf", 'wb') as pdf_file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                pdf_file.write(chunk)

def download_json_report(hash_value):
    print("Downloading JSON Report")
    data = {'hash': hash_value}
    headers = {'Authorization': MOBSF_API_KEY}
    response = requests.post(f'{MOBSF_SERVER}/api/v1/report_json', data=data, headers=headers)
    return response.json()

def delete_scan_result(hash_value):
    print("Deleting Scan Result")
    data = {'hash': hash_value}
    headers = {'Authorization': MOBSF_API_KEY}
    response = requests.post(f'{MOBSF_SERVER}/api/v1/delete_scan', data=data, headers=headers)
    return response.json()

# Iterate over APK files in the folder
for root, dirs, files in os.walk(APK_FOLDER_PATH):
    for file in files:
        if file.endswith(".apk"):
            apk_file_path = os.path.join(root, file)
            app_name = os.path.splitext(file)[0]

            upload_response = upload_apk(apk_file_path)
            hash_value = upload_response.get('hash')

            if hash_value:
                scan_response = scan_apk(hash_value)
                download_pdf_report(hash_value, app_name)
                json_report = download_json_report(hash_value)
                delete_response = delete_scan_result(hash_value)

                print(f"Process completed successfully for: {app_name}")
            else:
                print(f"Error uploading APK: {app_name}")
