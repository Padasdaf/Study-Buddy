import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import os

file_path = 'generated_users.csv'
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"Error: {file_path} not found.")
    exit()

# finding unique course codes from csv
unique_codes  = df['course_code'].unique()

# create empty dictionary to hold all course codes
course_codes = {}

# add each course code into course_codes dictionary
for code in unique_codes:
    course_codes[code] = df[df['course_code'] == code].reset_index(drop=True)

if 'COMMST223' in course_codes:
    print(course_codes['CS135'])
else:
    print("No data found for 'CS135'.")