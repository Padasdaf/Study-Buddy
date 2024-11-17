import os
import django
import glob
import csv
from homepage.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studbud.settings')

# Setup Django
django.setup()

def import_top_users(directory_path): 
    csv_files = glob.glob(os.path.join(directory_path, "*.csv"))
    
    if not csv_files:
        print("No CSV files found in the directory.")
        return
    
    latest_file = max(csv_files, key=os.path.getmtime)
    
    print(f"Importing data from the latest file: {latest_file}")
    
    User.objects.all().delete()

    with open(latest_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            User.objects.create(
                name=row['user_id'],
                courseCode=row['class'],
                gender=row['gender'],
                preftime=row['preferred_study_time'],
                personality=row['personality'],
                learning_style=row['learning_style']
            )

if __name__ == '__main__':
    directory_path = '../studbud' 
    import_top_users(directory_path)
