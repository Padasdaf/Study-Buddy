import pandas as pd
import random

# Define sample data options
classes = ["CS135", "MATH135", "MATH137", "COMMST223", "ECON101"]
genders = ["Male", "Female"]
study_times = ["Morning", "Afternoon", "Night"]
personalities = ["INTJ", "ENFP", "ISTP", "INFJ", "ESFJ", "ENTP", "ISFJ", "INFP"]
learning_styles = ["Audio", "Visual", "Kinaesthetic"]

# Generate random data for 50 users
data = {
    "class": [random.choice(classes) for _ in range(50)],
    "gender": [random.choice(genders) for _ in range(50)],
    "preferred_study_time": [random.choice(study_times) for _ in range(50)],
    "personality": [random.choice(personalities) for _ in range(50)],
    "learning_style": [random.choice(learning_styles) for _ in range(50)]
}

# Create DataFrame
user_data = pd.DataFrame(data)

# Display first few rows of the DataFrame
print (user_data.head())