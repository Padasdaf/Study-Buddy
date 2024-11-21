import pandas as pd
import os
import django
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import pairwise_distances
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studbud.settings')
django.setup() 

from studbud.import_cluster import import_top_users

csv_file_path = '../generated_users.csv'

def load_and_preprocess(file_path):
    try:
        user_data = pd.read_csv(file_path)
        print("Loaded data from generated_users.csv")
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        exit()

    required_columns = ["user_id", "class", "gender", "preferred_study_time", "personality", "learning_style"]
    if not all(col in user_data.columns for col in required_columns):
        print(f"Error: The file {file_path} must contain the following columns: {required_columns}")
        exit()

    label_encoders = {
        'gender': LabelEncoder(),
        'personality': LabelEncoder(),
        'preferred_study_time': LabelEncoder(),
        'learning_style': LabelEncoder()
    }

    for feature, encoder in label_encoders.items():
        user_data[feature] = encoder.fit_transform(user_data[feature])

    scaler = StandardScaler()
    features_to_scale = ['gender', 'preferred_study_time', 'personality', 'learning_style']
    user_data_scaled = user_data.copy()
    user_data_scaled[features_to_scale] = scaler.fit_transform(user_data[features_to_scale])
    user_info = user_data_scaled.iloc[-1]

    unique_codes = user_data_scaled['class'].unique()
    course_codes = {code: user_data_scaled[user_data_scaled['class'] == code] for code in unique_codes}

    return user_info, user_data, course_codes, features_to_scale


def generate_buddies(user_info, user_data, course_codes, features):
    course = user_info['class']
    
    if course not in course_codes:
        print(f"Error: Course {course} not found in course_codes.")
        return None

    group = course_codes[course].copy()
    num_clusters = max(1, len(group) // 5)
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    group['cluster'] = kmeans.fit_predict(group[features])

    target_user_features = user_info[features].values.reshape(1, -1)
    target_user_cluster = kmeans.predict(target_user_features)[0]

    same_cluster = group[group['cluster'] == target_user_cluster]
    distances = pairwise_distances(target_user_features, same_cluster[features])

    same_cluster = same_cluster.assign(distance=distances[0])

    top_5_similar = same_cluster.sort_values(by='distance').head(5)
    top_5_indices = top_5_similar.index
    return user_data.loc[top_5_indices]

def process_latest_user(file_path):
    user_info, user_data, course_codes, features_to_scale = load_and_preprocess(file_path)
    top_5_buddies = generate_buddies(user_info, user_data, course_codes, features_to_scale)
    return top_5_buddies

def save_top_buddies(top_5_buddies):
    folder_path = os.path.join(os.path.expanduser('~'), 'CSC', 'Study-Buddy', 'backend')
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, 'top_5_buddies.csv')
    top_5_buddies.to_csv(file_path, index=False)
    import_top_users(file_path)

def main():
    top_5_buddies = process_latest_user(csv_file_path)
    if top_5_buddies is not None:
        save_top_buddies(top_5_buddies)
        print(f"Top 5 buddies have been saved to {os.path.join(os.path.expanduser('~'), 'CSC', 'Study-Buddy', 'backend', 'top_5_buddies.csv')}")
    else:
        print("No top buddies found.")

def check_file_changes(last_modified_time):
    try:
        current_modified_time = os.path.getmtime(csv_file_path)
        print(f"Last checked at {time.ctime(current_modified_time)}")
        if current_modified_time != last_modified_time:
            print(f"The file was modified at {time.ctime(current_modified_time)}")
            main()
            return current_modified_time
        return last_modified_time
    except Exception as e:
        print(f"Error checking file modification time: {e}")
        return last_modified_time

if __name__ == "__main__":
    last_modified_time = os.path.getmtime(csv_file_path)
    while True:
        last_modified_time = check_file_changes(last_modified_time)
        time.sleep(2)
