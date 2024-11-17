import pandas as pd
import random
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import pairwise_distances
import os



classes = ["CS135", "MATH135", "MATH137", "COMMST223", "ECON101"]
genders = ["Male", "Female"]
study_times = ["Morning", "Afternoon", "Night"]
personalities = ["Introvert", "Extrovert"]
learning_styles = ["Audio", "Visual", "Kinaesthetic"]
names = ["a", "b", "c", "d"]


data = {
    "user_id": [random.choice(names) for _ in range (100)],
    "class": [random.choice(classes) for _ in range(100)],
    "gender": [random.choice(genders) for _ in range(100)],
    "preferred_study_time": [random.choice(study_times) for _ in range(100)],
    "personality": [random.choice(personalities) for _ in range(100)],
    "learning_style": [random.choice(learning_styles) for _ in range(100)]
}

user_data = pd.DataFrame(data)
# %%
unique_codes = user_data['class'].unique()

course_codes = {}

for code in unique_codes:
    course_codes[code] = user_data[user_data['class'] == code]


# find the number of distinct courses in user_data -> used to create the number of clusters, k

# encode categorial variables -> gender, personality and preferred study time
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

user_info = user_data_scaled.iloc[0] # first user in dataframe
top_5_buddies = generate_buddies(user_info, course_codes, features_to_scale)
print (top_5_buddies)

folder_path = os.path.join(os.path.expanduser('~'), 'CSC', 'Study-Buddy', 'backend')
os.makedirs(folder_path, exist_ok=True)
file_path = os.path.join(folder_path, 'top_5_buddies.csv')

top_5_buddies.to_csv(file_path, index=False)
