import pandas as pd

def extract_format():
    excel_path = "D:\\Venkata\\JA\\Estimates - JA Detailed Breakup.xlsx"
    df = pd.read_excel(excel_path)
    df.to_csv("D:\\Venkata\\JA\\estimates_format.csv", index=False)

if __name__ == "__main__":
    extract_format()
