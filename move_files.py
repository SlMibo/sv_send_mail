import os
import shutil
from datetime import datetime

# Directorio donde se descargan los archivos
download_dir = "C:\Users\USER1\Downloads"
# Directorio donde deben moverse los archivos
pdf_dir = "./pdf"

def move_files():
    current_date = datetime.now().strftime("%Y%m%d")
    filename1 = f"{current_date} - ReporteDashboard.pdf"
    filename2 = f"{current_date} - ReporteDashboardFyD.pdf"
    
    file1_path = os.path.join(download_dir, filename1)
    file2_path = os.path.join(download_dir, filename2)

    if os.path.exists(file1_path):
        shutil.move(file1_path, os.path.join(pdf_dir, filename1))
    if os.path.exists(file2_path):
        shutil.move(file2_path, os.path.join(pdf_dir, filename2))

if __name__ == '__main__':
    move_files()