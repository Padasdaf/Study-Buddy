import os
import csv
from homepage.models import User


def import_top_users(file_path): 
    if not os.path.exists(file_path):
        print(f"CSV file does not exist at path: {file_path}")
        return
    
    print(f"Importing data from the file: {file_path}")
    
    User.objects.all().delete()

    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(row)
                # breakpoint()
                User.objects.create(
                    name=row['user_id'],
                    course_code=row['class'],
                    gender=row['gender'],
                    preftime=row['preferred_study_time'],
                    personality=row['personality'],
                    learning_style=row['learning_style']
                )
        print(f"Data imported successfully from {file_path}")
    
    except Exception as e:
        print(f"An error occurred while importing data: {e}")

if __name__ == '__main__':
    file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'top_5_buddies.csv')
    file_path = os.path.abspath(file_path)  # To ensure it's an absolute path


    import_top_users(file_path)


