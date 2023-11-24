import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import sys
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.options.mode.chained_assignment = None 
data_job_skills = pd.read_csv('./Roles/jobs and skills (main dataset).csv')
data_roles = pd.read_csv('./Roles/roles (extra resource).csv')
data_skills = pd.read_csv('./Roles/skills_index (extra resource).csv')
print("data_job_skills Shape is: " + str(data_job_skills.shape))
input("Press ENTER to continue")
print("data_job_skills data in cuts of 10 (Columns are ommited with elipses):\n" + str(data_job_skills[:10]))
while True:
    try:
        rows = 5#int(input("How many rows to show in head function?: "))
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
print("Dropping rows with empty workplace_skills...")
data_job_skills = data_job_skills[~data_job_skills.isin(['[]']).any(axis=1)] #https://stackoverflow.com/questions/69497842/how-to-delete-any-row-containing-specific-string-in-pandas
print(data_job_skills)
print("Done\nConverting workplace_skills to multiple columns...")
column_list = []
for item in data_job_skills['workplace_skills']:
    item = item.replace("[", "")
    item = item.replace("]", "")
    item = item.split(", ")
    for skill in item:
        if skill not in column_list and skill is not None and skill is not "":
            column_list.append(skill)
print("workplace_skills amount: " + str(len(column_list)))
for item in column_list:
    item = item.replace("'", "")
    item = item.replace(" ", "_")
    data_job_skills['workskill_' + item] = False
print("Columns created.\nAdding data to new columns...")
y = 0
for item in data_job_skills['workplace_skills']:
    item = item.replace("[", "")
    item = item.replace("]", "")
    item = item.replace("'", "")
    item = item.split(", ")
    for skill in item:
        if skill is not None and skill is not "":
            skill = skill.replace(" ", "_")
            column_list_item = 'workskill_' + skill
            data_job_skills[column_list_item].iloc[y] = True
    y += 1
print("Data added\nReplacing NULL career_level")
data_job_skills.career_level.fillna(value="junior", inplace=True)
print(data_job_skills.career_level)
print("Empty career_levels replaced\nSaving DataFrame to CSV...")
try:
    data_job_skills.to_csv('./Roles/JobsSkillsEdited.csv', mode="w+")
except:
    print("Error: Unable to save to CSV as the file is open or set to read only")
print("Converting data to seperate data frame...")
print("Dropping uneeded columns")
ai_dataframe = data_job_skills.copy()
del data_job_skills
ai_dataframe = ai_dataframe.drop(["career_level", "workplace_skills", "career_weblink"], axis=1)
ai_dataframe["workplace_skills"] = np.nan
ai_dataframe["workplace_skills"] = ai_dataframe["workplace_skills"].astype(object)
print("Converting worksills to single column")
column_num = 0
row_num = 0
for item in ai_dataframe.career_title: 
    column_row_data_list = []
    column_num = 0
    for column in range(0, len(column_list)):
        column_list[column_num] = column_list[column_num].replace(" ", "_")
        column_row_data_list.append(int(ai_dataframe["workskill_" + column_list[column_num].replace("'", "")].iloc[row_num]))
        column_num += 1
    print(column_row_data_list)
    ai_dataframe.workplace_skills.iloc[row_num] = column_row_data_list
    row_num += 1
for item in ai_dataframe:
    print(item)
    if "workskill" in item:
        ai_dataframe = ai_dataframe.drop(item, axis=1)
print("Seperate dataframe created")
ai_dataframe.to_csv('./Roles/IHaveNotBeenTaughtAIProperly.csv', mode="w+")
selected_row = 0
while True:
    try:
        selected_row = int(input("Which row of the ai_dataframe would you like to see? [Between 0 and " + str(len(ai_dataframe.career_title) - 1) + "]: "))
        if selected_row > len(ai_dataframe.career_title) - 1 or selected_row < 0:
            raise Exception("selected_row is larger than the length of ai_dataframe.career_title")
        break
    except:
        print("\nPlease select a number between 0 and " + str(len(ai_dataframe.career_title) - 1))
        input("Press ENTER to continue")
print("\nCareer Title: " + ai_dataframe.career_title.iloc[selected_row], "\nWith the following skills: ", ai_dataframe.workplace_skills.iloc[selected_row])
input("Press ENTER to continue")
print("Creating training and test data...")
X_train, X_test, y_train, y_test =train_test_split(ai_dataframe.workplace_skills, ai_dataframe.career_title, random_state=11, test_size=0.20)
X_train = np.array(list(X_train), dtype=float)
X_test = np.array(list(X_test), dtype=float) #https://stackoverflow.com/questions/40514019/setting-an-array-element-with-a-sequence-error-while-training-svm-to-classify-im
print("Training and test data created")
print("X_train.shape is ", X_train.shape, "\ny_train.shape is ", y_train.shape)
print("X_test.shape is ", X_test.shape, "\ny_test.shape is ", y_test.shape)
input("Press ENTER to continue")
print("Creating KNN...")
knn = KNeighborsClassifier()
length = len(ai_dataframe.workplace_skills.iloc[0])
print("Making sure all workplace_skills are same length...")
for item in ai_dataframe.workplace_skills:
    new_length = len(item)
    if new_length != length:
        raise Exception("One or more workplace_skill lists are not the same length!")
print("All workplace_skill lists are the same length")
knn.fit(X=X_train, y=y_train)
predicted = knn.predict(X=X_test)
expected = y_test
print("KNN created.")
print("Predicted is ", predicted)
print("expected is ", expected)
input("Press ENTER to continue")
print("Getting wrong amount...")
wrong = [(p, e) for (p, e) in zip(predicted, expected) if p != e]
print("Wrong is ", wrong)
print("KNN score is ", f'{knn.score(X_test, y_test):.2%}')
input("Press ENTER to continue")
