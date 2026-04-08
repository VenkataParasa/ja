import pandas as pd
import PyPDF2
import sys

def extract_pdf():
    try:
        pdf_path = "JA BizTown RFP Final March 13 2026.pdf"
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
        with open("rfp_text.txt", "w", encoding="utf-8") as out:
            out.write(text)
    except Exception as e:
        print(f"Error reading PDF: {e}")

def extract_excel():
    try:
        excel_path = "JA_BizTown_RFP_Clarification_Questions.xlsx"
        df = pd.read_excel(excel_path)
        df.to_csv("excel_text.csv", index=False)
    except Exception as e:
        print(f"Error reading Excel: {e}")

if __name__ == "__main__":
    extract_pdf()
    extract_excel()
