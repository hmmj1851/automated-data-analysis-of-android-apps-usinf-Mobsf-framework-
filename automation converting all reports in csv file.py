import os
import fitz  # PyMuPDF
import pandas as pd

def extract_permissions(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()

    start = text.find('APPLICATION PERMISSIONS')
    end = text.find('APKID ANALYSIS', start)
    table_text = text[start:end]
    lines = table_text.split('\n')

    current_permission = []
    permissions_list = []
    for line in lines:
        if 'android.permission.' in line or 'com.google.android' in line:
            if current_permission:
                permissions_list.append(" ".join(current_permission))
                current_permission = [line]
            else:
                current_permission = [line]
        else:
            current_permission.append(line)
    if current_permission:
        permissions_list.append(" ".join(current_permission))

    data = []
    for permission in permissions_list:
        parts = permission.split()
        perm_name = parts[0]
        status = parts[1]
        info = parts[2] if len(parts) > 2 else "Not specified"
        description = " ".join(parts[3:]) if len(parts) > 3 else "Not specified"
        data.append([perm_name, status, info, description])
    return data

def process_pdfs(folder_path, output_csv):
    headers_needed = not os.path.isfile(output_csv) 
    print(f"Headers needed: {headers_needed}")

    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            print(f"Processing {pdf_path}...")
            data = extract_permissions(pdf_path)
            df = pd.DataFrame(data, columns=['Permission', 'Status', 'Info', 'Description'])
            if headers_needed:
                df.to_csv(output_csv, mode='w', index=False, header=True)
                headers_needed = False  
            else:
                df.to_csv(output_csv, mode='a', index=False, header=False)


folder_path = r'C:\Users\ANAM KHAN\Documents\Data Science\.vscode\minor2project\pdfreports'
output_csv = r'C:\Users\ANAM KHAN\Documents\Data Science\.vscode\minor2project\permissions.csv'


process_pdfs(folder_path, output_csv)
