import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# dataframe loads in csv file
df = pd.read_csv('generated_users.csv')

# finding unique course codes from csv
unique_codes  = df['course_code'].unique()

# create empty dictionary to hold all course codes
course_codes = {}

# add each course code into course_codes dictionary
for code in unique_codes:
    course_codes[code] = df[df['course_code'] == code]

print(course_codes['CS135'])

# #k means clustering on each group
# for code in unique_codes:
#     course_codes['specific_code']