import pandas as pd
data_job_skills = pd.read_csv('./Data/jobs and skills (main dataset).csv')
data_roles = pd.read_csv('./Data/roles (extra resource).csv')
data_skills = pd.read_csv('./Data/skills_index (extra resource).csv')
print("data_job_skills Shape is: " + str(data_job_skills.shape))
print("data_job_skills data in cuts of 10 (Columns are ommited with elipses):\n" + str(data_job_skills[:10]))
print("\ndata_job_skills data head:\n" + str(data_job_skills.head()))