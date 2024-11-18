import pandas as pd # for data processing
import random # for testing data
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import pairwise_distances

#################################################
classes = ["CS135", "MATH135", "MATH137", "COMMST223", "ECON101"]
genders = ["Male", "Female"]
study_times = ["Morning", "Afternoon", "Night"]
personalities = ["Introvert", "Extrovert"]
learning_styles = ["Audio", "Visual", "Kinaesthetic"]
names = ["a", "b", "c", "d"]

# test data generated
data = {
    "user_id": [random.choice(names) for _ in range (100)],
    "class": [random.choice(classes) for _ in range(100)],
    "gender": [random.choice(genders) for _ in range(100)],
    "preferred_study_time": [random.choice(study_times) for _ in range(100)],
    "personality": [random.choice(personalities) for _ in range(100)],
    "learning_style": [random.choice(learning_styles) for _ in range(100)]
}

# user_data will be read from database when finished
def buddy_generator(data):
    user_data = pd.DataFrame(data)
    
    #####################################################
    # pre-processing: find number of courses, encode categorical data, scale data
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

    # scale the data so all features contribute equally to the model
    scaler = StandardScaler()

    features_to_scale = ['gender', 'preferred_study_time', 'personality', 'learning_style']
    user_data_scaled = user_data.copy()

    user_data_scaled[features_to_scale] = scaler.fit_transform(user_data[features_to_scale])    

    unique_codes = user_data_scaled['class'].unique()
    course_codes = {code: user_data_scaled[user_data_scaled['class'] == code] for code in unique_codes}

    #print(course_codes.items())

    #############################################################
    # using knn

    final_groupings = []

    for class_label, class_data in course_codes.items():
        print(class_label, class_data)
        num_users = len(class_data)
    # find number of users to determine number of clusters
        if divmod(num_users, 5) == 0:
            num_clusters = num_users / 5
        elif divmod(num_users, 5) == 3 or divmod(num_users, 5) == 4:
            num_clusters = num_users // 5 + 1
        else: 
            num_clusters = num_users // 5

        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        labels = kmeans.fit_predict(class_data)

        clusters = [[] for _ in range(n_clusters)]
        for point, label in zip(class_data, labels):
            clusters[label].append(point.tolist())
        
        final_groupings.append(clusters)

    print(final_groupings)

buddy_generator(data)

# issue: a, b, c, d messing up algo. need to make sure user_id not factored in - only look at some features

    
"""
# apply k means clustering

def generate_buddies (user_info, course_codes, features):
    course = user_info['class']

    group = course_codes[course].copy()

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
"""