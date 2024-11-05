# Fetch multiple measurements for each patient in a single query
measurements = pd.read_gbq(
    '''
    SELECT
      person_id,
      visit_occurrence_id,
      measurement_concept_id,
      measurement_datetime,
      value_as_number,
      unit_concept_id
    FROM measurement
    WHERE
      NOT provider_id IS NULL -- ignore unvalidated device data
      AND measurement_concept_id IN (
        3004249,   -- creatinine
        3024561,   -- additional creatinine
        3027018,   -- heart rate
        3013290,   -- carbon dioxide
        3027315,   -- oxygen partial pressure
        21490674,  -- aorta systolic BP
        21490672,  -- aorta diastolic BP
        21490673,  -- aorta mean BP
        3024171,   -- respiratory rate
        42869608,  -- oxygen saturation
        40762351,  -- hemoglobin
        3004410,   -- hemoglobin total
        3007930,   -- additional measurement
        3003344,   -- hemoglobin presence in urine
        3009508,   -- creatinine in urine
        3020564,   -- creatinine in serum/plasma
        4084275    -- SAPS
      )
    ''',
    configuration=config_gbq, use_bqstorage_api=True
)

# Convert visit_start_date and measurement_datetime to date format
icu_sepsis_patients['visit_start_date'] = pd.to_datetime(icu_sepsis_patients['visit_start_date']).dt.date
measurements['measurement_date'] = pd.to_datetime(measurements['measurement_datetime']).dt.date

# Pivot measurements to get separate columns for each measurement type
measurements_pivoted = measurements.pivot_table(
    index=['person_id', 'visit_occurrence_id', 'measurement_date'],
    columns='measurement_concept_id',
    values='value_as_number'
).reset_index()

# Get current columns after pivoting
column_names = measurements_pivoted.columns.tolist()

# Define a dictionary mapping measurement_concept_id to descriptive names (adjust IDs to names as needed)
column_rename_map = {
    'person_id': 'person_id',
    'visit_occurrence_id': 'visit_occurrence_id',
    'measurement_date': 'measurement_date',
    3004249: 'creatinine_level',
    3024561: 'additional_creatinine',
    3027018: 'heart_rate',
    3013290: 'co2_partial_pressure',
    3027315: 'oxygen_partial_pressure',
    21490674: 'systolic_bp',
    21490672: 'diastolic_bp',
    21490673: 'mean_bp',
    3024171: 'respiratory_rate',
    42869608: 'oxygen_saturation',
    40762351: 'hemoglobin_moles',
    3004410: 'hemoglobin_total',
    3007930: 'additional_measurement',
    3003344: 'hemoglobin_urine_presence',
    3009508: 'creatinine_urine',
    3020564: 'creatinine_serum_plasma',
    4084275: 'saps'
}

# Rename columns based on column_rename_map, only for columns that exist
measurements_pivoted.rename(columns={col: column_rename_map.get(col, col) for col in column_names}, inplace=True)

# Merge icu_sepsis_patients with measurements_pivoted based on person_id and date
icu_sepsis_with_measurements = pd.merge(
    icu_sepsis_patients,
    measurements_pivoted,
    left_on=['person_id', 'visit_start_date'],
    right_on=['person_id', 'measurement_date'],
    how='left'
)

# Drop the extra date column from measurements (if not needed)
icu_sepsis_with_measurements.drop(columns=['measurement_date'], inplace=True)

# Display a sample to verify the merge
icu_sepsis_with_measurements.head(1000)
