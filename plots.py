import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from datetime import datetime

# Calculate Age at Visit
icu_sepsis_patients['age_at_visit'] = datetime.now().year - icu_sepsis_patients['year_of_birth']

# Age Distribution
plt.figure(figsize=(10, 6))
sns.histplot(icu_sepsis_patients['age_at_visit'], bins=20, kde=True, color='skyblue')
plt.title('Age Distribution of ICU Sepsis Patients')
plt.xlabel('Age at Visit')
plt.ylabel('Number of Patients')
plt.show()

# Gender Distribution
plt.figure(figsize=(8, 6))
icu_sepsis_patients['gender_concept_id'].value_counts().plot(kind='bar', color='lightcoral')
plt.title('Gender Distribution of ICU Sepsis Patients')
plt.xlabel('Gender Concept ID')
plt.ylabel('Number of Patients')
plt.show()

# Race Distribution
plt.figure(figsize=(10, 6))
icu_sepsis_patients['race_concept_id'].value_counts().plot(kind='bar', color='teal')
plt.title('Race Distribution of ICU Sepsis Patients')
plt.xlabel('Race Concept ID')
plt.ylabel('Number of Patients')
plt.show()

# Extract year and month from visit_start_date for time-based analysis
icu_sepsis_patients['visit_year'] = pd.to_datetime(icu_sepsis_patients['visit_start_date']).dt.year
icu_sepsis_patients['visit_month'] = pd.to_datetime(icu_sepsis_patients['visit_start_date']).dt.to_period('M')

# Monthly Admissions Trend
monthly_admissions = icu_sepsis_patients['visit_month'].value_counts().sort_index()
plt.figure(figsize=(12, 6))
monthly_admissions.plot(kind='line', marker='o', color='royalblue')
plt.title('Monthly Admissions of ICU Sepsis Patients')
plt.xlabel('Month')
plt.ylabel('Number of Admissions')
plt.xticks(rotation=45)
plt.show()

# Yearly Admissions Trend
yearly_admissions = icu_sepsis_patients['visit_year'].value_counts().sort_index()
plt.figure(figsize=(10, 6))
yearly_admissions.plot(kind='bar', color='orchid')
plt.title('Yearly Admissions of ICU Sepsis Patients')
plt.xlabel('Year')
plt.ylabel('Number of Admissions')
plt.show()

# Define age groups
age_bins = [0, 18, 35, 60, 100]
age_labels = ['0-18', '19-35', '36-60', '60+']
icu_sepsis_patients['age_group'] = pd.cut(icu_sepsis_patients['age_at_visit'], bins=age_bins, labels=age_labels)

# Admissions by Age Group and Gender
age_gender = icu_sepsis_patients.groupby(['age_group', 'gender_concept_id']).size().unstack()
age_gender.plot(kind='bar', stacked=True, color=['lightblue', 'salmon'], figsize=(10, 6))
plt.title('ICU Sepsis Admissions by Age Group and Gender')
plt.xlabel('Age Group')
plt.ylabel('Number of Admissions')
plt.legend(title='Gender')
plt.show()

# Admissions by Age Group and Race
age_race = icu_sepsis_patients.groupby(['age_group', 'race_concept_id']).size().unstack()
age_race.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='viridis')
plt.title('ICU Sepsis Admissions by Age Group and Race')
plt.xlabel('Age Group')
plt.ylabel('Number of Admissions')
plt.legend(title='Race')
plt.show()
