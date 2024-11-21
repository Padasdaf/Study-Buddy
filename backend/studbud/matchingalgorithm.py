import pandas as pd
import random
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import pairwise_distances
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studbud.settings')
django.setup() 

from studbud.import_cluster import import_top_users

csv_file_path = '../generated_users.csv'

try:
    user_data = pd.read_csv(csv_file_path)
    print("Loaded data from generated_users.csv")
except FileNotFoundError:
    print(f"Error: The file {csv_file_path} does not exist.")
    exit()

required_columns = ["user_id", "class", "gender", "preferred_study_time", "personality", "learning_style"]
if not all(col in user_data.columns for col in required_columns):
    print(f"Error: The file {csv_file_path} must contain the following columns: {required_columns}")
    exit()
# %%
unique_codes = user_data['class'].unique()

course_codes = {}

for code in unique_codes:
    course_codes[code] = user_data[user_data['class'] == code] # not right



label_encoder_gender = LabelEncoder()
user_data['gender'] = label_encoder_gender.fit_transform(user_data['gender'])

label_encoder_personality = LabelEncoder()
user_data['personality'] = label_encoder_personality.fit_transform(user_data['personality'])

label_encoder_studytime = LabelEncoder()
user_data['preferred_study_time'] = label_encoder_studytime.fit_transform(user_data['preferred_study_time'])

label_encoder_learning = LabelEncoder()
user_data['learning_style'] = label_encoder_learning.fit_transform(user_data['learning_style'])

# print(user_data.head())
# print (user_data['preferred_study_time'].to_string(index=False))

# %%
# scale the data so all features contribute equally to the model
scaler = StandardScaler()

features_to_scale = ['gender', 'preferred_study_time', 'personality', 'learning_style']
user_data_scaled = user_data.copy()

user_data_scaled[features_to_scale] = scaler.fit_transform(user_data[features_to_scale])

#print (user_data_scaled.head())


# %%
# apply k means clustering

unique_codes = user_data_scaled['class'].unique()
course_codes = {code: user_data_scaled[user_data_scaled['class'] == code] for code in unique_codes}

def generate_buddies (user_info, course_codes, features):
    course = user_info['class']

    group = course_codes[course].copy()


    num_clusters = max(1, len(group) // 5)
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    group['cluster'] = kmeans.fit_predict(group[features])

    target_user_features = user_info[features].values.reshape(1,-1)
    target_user_cluster = kmeans.predict(target_user_features)[0]

    same_cluster = group[group['cluster'] == target_user_cluster]
    
    distances = pairwise_distances(target_user_features, same_cluster[features])
    same_cluster = same_cluster.assign(distance = distances[0])
    top_5_similar = same_cluster.sort_values(by='distance').head(5)

    top_5_indices = top_5_similar.index
    top_5_original = user_data.loc[top_5_indices]
    return top_5_original

user_info = user_data_scaled.iloc[-1] 
top_5_buddies = generate_buddies(user_info, course_codes, features_to_scale)
print (top_5_buddies)

folder_path = os.path.join(os.path.expanduser('~'), 'CSC', 'Study-Buddy', 'backend')
os.makedirs(folder_path, exist_ok=True)
file_path = os.path.join(folder_path, 'top_5_buddies.csv')

top_5_buddies.to_csv(file_path, index=False)


def updateDB():
    import_top_users(file_path)

updateDB()
