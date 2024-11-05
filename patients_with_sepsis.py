# Get concept_id for Sepsis
sepsis_concept = client.query(
    '''
    SELECT concept_id
    FROM concept
    WHERE concept_class_id = 'Disorder'
    AND concept_name = 'Sepsis'
    '''
    , job_config=job_config).to_dataframe()

# Extract concept_id for Sepsis
sepsis_concept_id = sepsis_concept['concept_id'].iloc[0]

# Join visit_occurrence with the diagnosis table on sepsis_concept_id
sepsis_patients = client.query(
    f'''
    SELECT v.*
    FROM visit_occurrence v
    JOIN condition_occurrence co ON v.visit_occurrence_id = co.visit_occurrence_id
    WHERE co.condition_concept_id = {sepsis_concept_id}
    '''
    , job_config=job_config).to_dataframe()

# Query without the care_site_id filter
icu_sepsis_patients = client.query(
    f'''
    SELECT p.*, v.visit_start_date
    FROM person p
    JOIN (
        SELECT v.person_id, v.visit_start_date
        FROM visit_occurrence v
        JOIN condition_occurrence co ON v.visit_occurrence_id = co.visit_occurrence_id
        WHERE co.condition_concept_id = {sepsis_concept_id}
    ) v ON p.person_id = v.person_id
    '''
    , job_config=job_config).to_dataframe()

# Display a sample of the result to confirm matches
icu_sepsis_patients
