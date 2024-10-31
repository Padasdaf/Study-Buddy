import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# dataframe loads in csv file
df = pd.read_csv('ADDFILEHERE', index_col = 'COLUMNFORINDEX')

# finding unique values and 
unique_codes  = df['course_code'].unique()

# dictionary to hold all course codes
course_codes = {}

for code in unique_codes:
    course_codes[code] = df[df['course_code'] == code]

#k means clustering on each group
for code in unique_codes:
    course_codes['specific_code']