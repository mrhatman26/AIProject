import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import sklearn
import os


def typewriter(text):
	import sys
	from time import sleep
	for char in text:
		sleep(0.1)
		sys.stderr.write(char)


def listConversion(item):  # Converts a list that is a string back into an actual list
	item = item.replace("[", "")
	item = item.replace("]", "")
	item = item.split(", ")
	return item


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.options.mode.chained_assignment = None

# typewriter("A.I. Model Started...\n")
# typewriter("Reading Jobs and Skills Dataset...\n")

try:
	df = pd.read_csv("./jobs and skills (main dataset).csv")
	#df2 = pd.read_csv("./Dataset and resources-20231024/roles.csv")
	#df3 = pd.read_csv("./Dataset and resources-20231024/skills_index (extra resource).csv")
except:
	typewriter("Error: Dataset not found. Please download the dataset and place it in the same directory as this file.")
	exit()

# typewriter("Dataset Loaded Successfully!\n")
# pause = input("Press Enter to continue...\n")
#
#
# typewriter("Dataset shape is: " + str(df.shape) + "\n")

# print(str(df[:10]) + "\n")

while True:
	try:
		rows = int(input("How many rows should i show?: "))
		break
	except:
		typewriter("Needs to be an int")

print("Jobs and Skills Dataset Head" + str(df.head(rows)))
os.system('cls' if os.name == 'nt' else 'clear')
print("Jobs and Skills Dataset Description" + str(df.describe()) + "\n")

df = df.drop(['hard_skills', 'id', 'text'], axis=1)
df = df.rename(
	columns={'Unnamed: 0': 'ID', 'career_level': 'Career_Level', 'soft_skills': 'Competencies', 'title': 'Job_Title',
	         'url': 'Job_Entry_URL'})
df = df[~df.isin(['[]']).any(axis=1)]
print(df.head(rows))
clist = []

for item in df['Competencies']:
	item = listConversion(item)
	for skill in item:
		if skill not in clist and skill != None and skill != "":
			clist.append(skill)

for item in clist:
	item = item.replace("'", "")
	item = item.replace(" ", "_")
	df['Competencies_' + item] = False

y = -1

for item in df['Competencies']:
	item = item.replace("'", "")
	item = listConversion(item)
	y += 1
	for skill in item:
		if skill != None and skill != "":
			skill = skill.replace(" ", "_")
			clist[y] = 'Competencies_' + skill
			df[clist].iloc[y] = True

df.Career_Level.fillna(value="junior", inplace=True)

df = df.reset_index(drop=True)

os.system('cls' if os.name == 'nt' else 'clear')

try:
	df.to_csv('JobsSkilledEdited.csv', index=False)
	print("Done")
except:
	print("Error: Unable to save CSV")

df.drop(["Career_Level", "Competencies", "Job_Entry_URL"], axis=1)

df["Compentencies"] = np.nan
df["Compentencies"] = df["Compentencies"].astype(object)

cnum = 0
rnum = 0
print(clist)
for item in df.Job_Title:
        crowlist = []
        cnum = 0
        for column in range(0, len(clist)):
                print(type(clist[cnum]))
                clist[cnum] = clist[cnum].replace(" ", "_")
                if df[clist[cnum]].iloc[rnum] == True:
                        crowlist.append(int(df["Compentencies" + clist[cnum].replace("'", "")].iloc[rnum]))
                cnum += 1
		# crowlist.append(int(df["Compentencies" + clist[cnum].replace("'", "")].iloc[rnum]))
		# cnum += 1
        df["Competencies"].iloc[rnum] = crowlist
        rnum += 1

for item in df:
	if "workskill" in item:
		df = df.drop(item, axis=1)

field_map = {"Developer": 0, "Engineer": 1, "Analyst": 2, "Designer": 3, "Technician": 4, "Consultant": 5, "Adviser": 6,
             "Architect": 7, "Administrator": 8, "Strategist": 9}

r = 0

for item in df.Job_title:
	for job in field_map:
		if job in item:
			df["Job_title"].iloc[r] = field_map[job]
	r += 1
