import pandas as pd
import random
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import pairwise_distances
from filtering import course_codes

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','studbud.settings')

import django
django.setup()

from homepage.models import User
from studbud.import_cluster import import_top_users

classes = ["CS135", "MATH135", "MATH137", "COMMST223", "ECON101"]
genders = ["Male", "Female"]
study_times = ["Morning", "Afternoon", "Night"]
personalities = ["Introvert", "Extrovert"]
learning_styles = ["Audio", "Visual", "Kinaesthetic"]
names = ["a", "b", "c", "d"]

data = {
    "user_id": [random.choice(names) for _ in range(100)],
    "course_code": [random.choice(classes) for _ in range(100)],
    "gender": [random.choice(genders) for _ in range(100)],
    "preferred_study_time": [random.choice(study_times) for _ in range(100)],
    "personality": [random.choice(personalities) for _ in range(100)],
    "learning_style": [random.choice(learning_styles) for _ in range(100)]
}

user_data = pd.DataFrame(data)

# Encode categorical variables
label_encoder_gender = LabelEncoder()
user_data['gender'] = label_encoder_gender.fit_transform(user_data['gender'])

label_encoder_personality = LabelEncoder()
user_data['personality'] = label_encoder_personality.fit_transform(user_data['personality'])

label_encoder_studytime = LabelEncoder()
user_data['preferred_study_time'] = label_encoder_studytime.fit_transform(user_data['preferred_study_time'])

label_encoder_learning = LabelEncoder()
user_data['learning_style'] = label_encoder_learning.fit_transform(user_data['learning_style'])

# Scale the data
scaler = StandardScaler()
features_to_scale = ['gender', 'preferred_study_time', 'personality', 'learning_style']
user_data_scaled = user_data.copy()
user_data_scaled[features_to_scale] = scaler.fit_transform(user_data[features_to_scale])

# Function to generate study buddies
def generate_buddies(user_info, course_codes, features):
    course = user_info['class']
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
    top_5_original = user_data.loc[top_5_indices]
    return top_5_original

# Select first user and find top 5 similar buddies
user_info = user_data_scaled.iloc[0]
top_5_buddies = generate_buddies(user_info, course_codes, features_to_scale)

# Save to CSV and update DB
folder_path = os.path.join(os.path.expanduser('~'), 'CSC', 'Study-Buddy', 'backend')
os.makedirs(folder_path, exist_ok=True)
file_path = os.path.join(folder_path, 'top_5_buddies.csv')
top_5_buddies.to_csv(file_path, index=False)

def updateDB():
    import_top_users(file_path)

updateDB()
