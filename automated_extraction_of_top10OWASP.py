import fitz  # PyMuPDF

def extract_owasp_vulnerabilities(pdf_path):
    doc = fitz.open(pdf_path)
    vulnerabilities = []
    in_code_analysis = False
    severity = None

    for page_number, page in enumerate(doc):
        text_blocks = page.get_text("blocks")
        for block in text_blocks:
            text = " ".join(block[4].strip().split())  # Normalize whitespace

            if 'CODE ANALYSIS' in text:
                in_code_analysis = True
            elif 'SHARED LIBRARY BINARY ANALYSIS' in text:
                in_code_analysis = False
                break  

            if in_code_analysis:
                if 'high' in text.lower():
                    severity = 'HIGH'
                elif 'warning' in text.lower():
                    severity = 'WARNING'
                
                # Check if the current block is a standards description
                if severity and ('OWASP Top 10:' in text or 'OWASP MASVS:' in text):
                    vulnerabilities.append({
                        'Severity': severity,
                        'Standards': text
                    })
                    severity = None  

    return vulnerabilities

# Path to the PDF file
pdf_path = 'pdfreports\stretching.stretch.exercises.back-2.0.10-APK4Fun.com_report.pdf'
vulnerabilities = extract_owasp_vulnerabilities(pdf_path)

if vulnerabilities:
    for vulnerability in vulnerabilities:
        print(vulnerability)
else:
    print("No vulnerabilities found matching the criteria.")
