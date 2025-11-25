import os
from pypdf import PdfReader

def read_pdf(file_path, output_file):
    output_file.write(f"--- Reading {os.path.basename(file_path)} ---\n")
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        output_file.write(text + "\n")
    except Exception as e:
        output_file.write(f"Error reading {file_path}: {e}\n")
    output_file.write(f"--- End of {os.path.basename(file_path)} ---\n\n")

base_dir = r"c:/Users/rattu/Downloads/L-13 & L-14 Kafka"
files = ["Kafka___Data_Engineering.pdf", "Kakfa_real_time_processing.pdf"]
output_path = os.path.join(base_dir, "pdf_content.txt")

with open(output_path, "w", encoding="utf-8") as f:
    for file in files:
        path = os.path.join(base_dir, file)
        read_pdf(path, f)
