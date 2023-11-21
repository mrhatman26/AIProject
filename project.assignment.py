import pandas as pd
pd.set_option('display.max_columns', None)
data_job_skills = pd.read_csv('./Roles/jobs and skills (main dataset).csv')
data_roles = pd.read_csv('./Roles/roles (extra resource).csv')
data_skills = pd.read_csv('./Roles/skills_index (extra resource).csv')
print("data_job_skills Shape is: " + str(data_job_skills.shape))
input("Press ENTER to continue")
print("data_job_skills data in cuts of 10 (Columns are ommited with elipses):\n" + str(data_job_skills[:10]))
while True:
    try:
        rows = int(input("How many rows to show in head function?: "))
        break
    except:
        print("Needs to be int!")
print("\ndata_job_skills data head:\n" + str(data_job_skills.head(rows)))
input("Press ENTER to continue")
print("\ndata_job_skills description is:\n" + str(data_job_skills.describe()))
input("Press ENTER to continue")
print("\ndata_job_skills DTypes are:\n" + str(data_job_skills.dtypes))
print(data_job_skills)
data_job_skills = data_job_skills.drop('hard_skills', axis=1)
data_job_skills = data_job_skills.drop('id', axis=1)
data_job_skills = data_job_skills.drop('text', axis=1)
data_job_skills = data_job_skills.rename(columns={'soft_skills': 'workplace_skills', 'title': 'career_title', 'url': 'career_weblink'})
print(data_job_skills)
