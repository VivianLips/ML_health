# Get creatinine measurements for each patient
creatinine = pd.read_gbq(
    '''
    SELECT
      person_id,
      visit_occurrence_id,
      measurement_datetime,
      value_as_number AS creatinine_value,
      unit_concept_id AS creatinine_unit
    FROM measurement
    WHERE
      NOT provider_id IS NULL -- ignore unvalidated device data
      AND measurement_concept_id IN (
        3004249,  -- Example: creatinine level concept ID (change to actual IDs if different)
        3024561   -- Include other related concept IDs for creatinine if needed
    )
    ''',
    configuration=config_gbq, use_bqstorage_api=True
)

# Convert visit_start_date and measurement_datetime to date format for easier comparison
icu_sepsis_patients['visit_start_date'] = pd.to_datetime(icu_sepsis_patients['visit_start_date']).dt.date
creatinine['measurement_date'] = pd.to_datetime(creatinine['measurement_datetime']).dt.date

# Perform a left join on person_id and the date fields
icu_sepsis_with_creatinine = pd.merge(
    icu_sepsis_patients,
    creatinine,
    left_on=['person_id', 'visit_start_date'],
    right_on=['person_id', 'measurement_date'],
    how='left'
)

# Drop the extra date column from creatinine (if not needed)
icu_sepsis_with_creatinine.drop(columns=['measurement_date'], inplace=True)

# Display a sample to verify the merge
icu_sepsis_with_creatinine.head(1000)
