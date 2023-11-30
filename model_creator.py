import pandas as pd #Import pandas to allow for dataframes.
import numpy as np #Import numpy for numpy arrays.
import matplotlib.pyplot as plt #Import matplotlib to visualise heatmap data.
import seaborn as sns #Import seaborn to allow for data heatmaps.
import os #Imports os to allow for system commands. (Used to allow mkdir)
import pickle #Import pickle to save the AI model.
import sys #Allows for the system (The Python Interpreter) to be manipulated. I use this to kill the program if the .csv file IS NOT read.
from sklearn.model_selection import train_test_split #Importing of the required modules from sklearn to allow for the training of the A.I.
#test_train_split splits the data between training data and test data/
from sklearn.neighbors import KNeighborsClassifier #KNN is what I've used to train the A.I
from sklearn.metrics import confusion_matrix #Allows for the creation of a confusion matrix
from sklearn.metrics import classification_report #Allows for the creation of classification report
from sklearn.model_selection import KFold #Allows for KFold validation
from sklearn.model_selection import cross_val_score #Allows for evaluation of a score by cross validation
from misc_functions import pause #A method by me that pauses the program and waits for the user to press enter with the message "Press ENTER to coninue"
def convert_to_list(item): #Converts a list that is a string back into an actual list
    item = item.replace("[", "")
    item = item.replace("]", "")
    item = item.split(", ")
    return item
skip_pause = True #If set to True, all instances of pause() will NOT interrupt to wait for the user to press ENTER.
print("Creating 'A.I' model. START!")
pd.set_option('display.max_columns', None) #Removes the limit on displayed columns which shows up as elipses. With this, ALL columns are displayed, but the formatting is awful.
pd.set_option('display.max_rows', None) #The same as the above, but it removes the limit on rows instead.
pd.options.mode.chained_assignment = None #Removes the chained assignment warning.
#From the documentation (https://pandas.pydata.org/docs/user_guide/options.html): Raise an exception, warn, or no action if trying to use chained assignment, the default is warn
print("Attempting to read 'jobs and skills (main dataset).csv'...", end="") #Setting "end" to an empty string prevents Python from automatically creating a new line after this print. Thia is mostly just for fun as it allows me to go "Doing something...Done" or "Doing something...Failed".
try:
    data_job_skills = pd.read_csv('./Roles/jobs and skills (main dataset).csv') #Imports the main data file from the Roles folder.
except:
    print("Failed\nThe file may not exist or is not readable.") #If the file fails to be read, I killed the program because the file is required.
    sys.exit()
#Note to self: Python seems to accept Unix directory formatting (./dir/) but can also accept Windows directory formatting by escaping slashes. (\\Dir\\)
print("Success\ndata_job_skills Shape is: " + str(data_job_skills.shape))
pause(skip_pause) #I added pauses to allow for the output to be read. Otherwise the output goes at a million miles an hour. (Hyperbole of course)
print("data_job_skills data in cuts of 10 (Columns are ommited with elipses):\n" + str(data_job_skills[:10])) #Shows the rows in data_job_skills in cuts of 10.
while True: #Allows for the user to see a specified number of rows from the start (head).
    try: #It will keep repeating until the user specifies an number.
        rows = int(input("How many rows to show in head function?: "))
        break
    except:
        print("Needs to be int!")
print("\ndata_job_skills data head:\n" + str(data_job_skills.head(rows))) #Displays the amount of rows from the head that the user specified.
pause(skip_pause)
print("\ndata_job_skills description is:\n" + str(data_job_skills.describe())) #Describes the data. Specifically, it shows the count, the mean, the std, the min, the max and the standard deviation.
pause(skip_pause)
print("\ndata_job_skills DTypes are:\n" + str(data_job_skills.dtypes)) #Shows the datatypes of the columns in the dataframe.
pause(skip_pause)
print("The whole dataframe is:\n", data_job_skills) #Prints the whole dataframe. Is printed as "squeezed text" which means the user has to double click a box to show the print.
pause(skip_pause)
print("Dropping uneeded columns...", end="")
data_job_skills = data_job_skills.drop(['hard_skills', 'id', 'text'], axis=1) #Here I drop the columns I will not use
#I drop hard skills as I will not be using it. Maybe in another iteration I would, but not now.
#I drop the ID column as the dataframe already has its own and this is not needed.
#I drop the text column because I do not need the descriptions of the jobs at all. Maybe in another iteration, I could have the user describe the job they want and use this, but not now.
data_job_skills = data_job_skills.rename(columns={'soft_skills': 'workplace_skills', 'title': 'career_title', 'url': 'career_weblink'}) #Here I rename the columns/headers to reflect what they represent better. (At least, I think they make the names more clearer?)
print("Done\nDataframe is now:\n", data_job_skills)
pause(skip_pause)
print("Dropping rows with empty workplace_skills...", end="")
data_job_skills = data_job_skills[~data_job_skills.isin(['[]']).any(axis=1)]
#Here I drop any rows in the dataframe that contain "[]" (an empty array) as their soft skills.
#I drop them because they do not help with training at all. (I imagine that using the hard skills in the future would help with this")
#The tidle reverses bools. (https://stackoverflow.com/questions/46054318/tilde-sign-in-pandas-dataframe)
#.isin returns bools of if the specified data is in the dataframe (https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.isin.html)
#I am unsure as to what .any does. I do not understand its documentation.(https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.any.html)
#Overall, I do not understand this command and why it works as at no point (from my understanding) do any of the commands drop any rows.
#The source of this command is from StackOverflow and is the link below this comment.
#https://stackoverflow.com/questions/69497842/how-to-delete-any-row-containing-specific-string-in-pandas
print("Done\nDataframe is now:\n", data_job_skills)
pause(skip_pause)
print("Converting workplace_skills to multiple columns...", end="")
column_list = []
#This for loop goes through each row in the soft_skills column and adds any skills that are not already in column_list to said list.
for item in data_job_skills['workplace_skills']:
    '''The lists in the soft_skills column (at this point, the workplace_skills column) are not actually lists but are instead strings.
       Because of this, I need to remove the squared brackets that represent the lists and then convert the resulting strings into actual lists.'''
    item = convert_to_list(item) #Each element of a list is seperated by a comma. This makes it easy to convert these strings back into lists.
    for skill in item: #Iterate through each skill in the converted list and check if it is in "column_list". If it is not in that list, add it it to the list.
        if skill not in column_list and skill != None and skill != "":
            column_list.append(skill)
print("Done\nworkplace_skills amount is: " + str(len(column_list)) + "\nSaving column_list to file...", end="")
skills_file = open("./static/skills_file.txt", "w")
for item in column_list:
    skills_file.write(item + "\n")
skills_file.close()
print("Done\nAdding workskill_ to listed skills...", end="")
for item in column_list: #Loop through column_listt and remove apostrophes and replace spaces with underscores.
    item = item.replace("'", "")
    item = item.replace(" ", "_")
    data_job_skills['workskill_' + item] = False #Create a new column in the dataframe that is named with each skill in the colum_list with "workskill_" added before the name. Then, make the data of these columns equal False. (Or as it is displayed in prints "0")
print("Done\nColumns created.")
pause(skip_pause)
print("Adding data to new columns...", end="")
y = 0
#This for loop goes through the skills column again and, for each skill found, it replaces the current row with True in the column that represents that skill. (I hope that makes sense?)
for item in data_job_skills['workplace_skills']:
    item = item.replace("'", "")
    item = convert_to_list(item)
    for skill in item:
        #Iterate through each found skill and, if it is NOT None and also not an empty string, add True to the current row in the column that represents the skill. (Again, I hope this makes sense)
        if skill != None and skill != "":
            skill = skill.replace(" ", "_")
            column_list_item = 'workskill_' + skill #The column that matches the current skill
            data_job_skills[column_list_item].iloc[y] = True #Replace the current row (iloc[y]) in the colum that matches the skill (data_job_skills[column_list_item]) with True (= True)
    y += 1
print("Done\nReplacing NULL career_level...", end="")
data_job_skills.career_level.fillna(value="junior", inplace=True) #Replaces all None or NaN values in the career_level column with "junior"
print("Done\nDataframe is now:\n", data_job_skills.career_level)
print("Empty career_levels replaced\nSaving DataFrame to CSV...", end="")
#Here I attempt to save the dataframe to a CSV file. This was originally for debugging, but I have decided
#to keep it as I feel it is good to have an output of the dataframe after being edited.
#Unfortunately, the function fails if the CSV file is open.
#Since this is not important, my except does not terminate the program and instead just prints an error.
data_job_skills = data_job_skills.reset_index(drop=True) #Reset the dataframe's index as it is no longer in order. Sort of like defragging a disk.
try:
    data_job_skills.to_csv('./Roles/JobsSkillsEdited.csv', mode="w+")
    print("Done")
except:
    print("Failed\nError: Unable to save to CSV as the file is open or set to read only")
pause(skip_pause)
print("Converting data to seperate data frame.")
print("Dropping uneeded columns")
#Here I copy the dataframe to a new variable to better reflect the next steps better.
ai_dataframe = data_job_skills.copy()
del data_job_skills #Removes the reference of data_job_skills from the dataframe. (And apparently releases the memory held by the dataframe, but I cannot confirm this)
ai_dataframe = ai_dataframe.drop(["career_level", "workplace_skills", "career_weblink"], axis=1) #The A.I will need even less of the columns and so I drop those here. 
ai_dataframe["workplace_skills"] = np.nan #Here I create a new column and set its values to be NaN. (Not a Number)
ai_dataframe["workplace_skills"] = ai_dataframe["workplace_skills"].astype(object) #I then tell pandas that this column's datatype will be object rather than float. (Not doing this will cause errors later)
print("Converting worksills to single column")
#Here I convert the columns of each skill back into one column with lists which will allow the A.I to read them.
column_num = 0
row_num = 0
#This for loop goes through each column listed in column_list and then goes through each row and adds its value to a list.
#This list is then saved to the current row of workplace_skills.
for item in ai_dataframe.career_title:
    column_row_data_list = [] #The list that will be saved to each row.
    column_num = 0
    for column in range(0, len(column_list)): #A C styled for loop to go through the column_list.
        column_list[column_num] = column_list[column_num].replace(" ", "_") #Replaces the current value of column_list to have its spaces be underscores instead.
        column_row_data_list.append(int(ai_dataframe["workskill_" + column_list[column_num].replace("'", "")].iloc[row_num]))
        #Then it appends the current value of the selected column and row its row's value to column_row_data_list. 
        column_num += 1
    print(column_row_data_list) #I print this list here and I cannot remember why, though I think it may have been for debugging. It looks cool though.
    ai_dataframe.workplace_skills.iloc[row_num] = column_row_data_list #Save the list of skills to workplace_skills at the current value of row_number.
    row_num += 1 #Increase row_number at the end of every loop. Do not forget this like I did.
#Finally for this part,l I loop through each column in the dataframe and, if it contains "workskill", then the column is dropped because we don't need it anymore.
print("Dropping worksill columns.")
for item in ai_dataframe:
    if "workskill" in item:
        ai_dataframe = ai_dataframe.drop(item, axis=1)
        print(item + " has been dropped")
print("All worksill columns have been dropped.\nSeperate dataframe created")
pause(skip_pause)
print("Mapping career_title rows.")
ai_dataframe_old = ai_dataframe.copy() #I copy the current state of the dataframe for later.
#career_map = {"Developer": 0, "Engineer": 1, "Analyst": 2, "Designer": 3, "Technician": 4, "Consultant": 5, "Adviser": 6, "Architect": 7, "Administrator": 8, "Strategist": 9, "Tester": 10, "Trainer": 11, "Researcher": 12, "Expert": 13, "Executive": 14, "Apprenticeship": 15, "Manager": 16, "Specialist": 17, "SEO": 18, "Graduate": 19, "UX": 20, "Lead": 21, "Support": 22, "Planner": 23, "CO-ordinator": 24, "Monitoring": 25, "Writer": 26, "Master": 27}
career_map = {"Developer": 0, "Engineer": 1, "Analyst": 2, "Designer": 3, "Techn  ician": 4, "Consultant": 5, "Adviser": 6, "Architect": 7, "Administrator": 8, "Strategist": 9}
#Here I map out job positions found in career_title to numbers. The A.I will only accept numbers and so I need to replace all job titles with numbers.
row = 0
#Here, I loop through each career_title and check if it contains any of the keys from the career_map dictionary.
#If the title does contain a word from it, the value of the career_title is replaced with the key's corresponding value.
for item in ai_dataframe.career_title:
    print("Item is: ", item)
    for career in career_map: #Loop through the keys of the career_map dictionary.
        print("Career is: ", career)
        if career in item: #If the key from the dictionary is found in the current career_title, replace the career_title with the key's value.
            print("Item contains career")
            ai_dataframe.career_title.iloc[row] = career_map[career] #Replace the career_title with the key's value.
            break #Break from this loop to avoid replacing the career_title with anything else.
    print("\n")
    row += 1
print("Checking rows for unmapped items...")
row = 0
ai_dataframe = ai_dataframe.reset_index(drop=True) #Resets the index of the dataframe. This is because it is currently not correct and continuing would cause errors. Again, this is kind of like disk defragging.
#Next, go through each career_title again and check if it can be converted to an integer. If it cannot, this means it has not been mapped and so it should be dropped.
for item in ai_dataframe.career_title:
    print("Item is: ", item)
    try:
        int(item) #Attempt to convert the title into a number.
    except:
        print("Dropping row as item could not be mapped")
        ai_dataframe = ai_dataframe.drop(index=row)#loc[row].drop(index=row)
        #Drop the current row as it has not been mapped due to failing to be converted to an integer.
    row += 1
#ai_dataframe = ai_dataframe.reset_index(drop=True) #Reset the index again.
print("Career titles mapped")
pause(skip_pause)
print("Saving ai_dataframe to CSV...", end="")
#Here I attempt to save the dataframe again to a different file. Again, not important so it will continue if any errors are encountered.
try:
    ai_dataframe.to_csv('./Roles/AIData.csv', mode="w+")
    print("Done")
except:
    print("Failed\nError: Unable to save to CSV as the file is open or set to read only")
    pause(skip_pause)
selected_row = 0
#Have the user select a row from the careet_title to be printed to see how it has been mapped. (And to see its skills)
#Does not continue untile the user enters "E" so that they can view the data.
while True:
    try:
        selected_row = input("Which row of the ai_dataframe would you like to see? [Between 0 and " + str(len(ai_dataframe.career_title) - 1) + "]: ")
        if int(selected_row) > len(ai_dataframe.career_title) - 1 or int(selected_row) < 0:
            raise Exception("selected_row is larger than the length of ai_dataframe.career_title")
        print("\nCareer Title: " + str(ai_dataframe.career_title.iloc[int(selected_row)]), "\nWith the following skills: ", str(ai_dataframe.workplace_skills.iloc[int(selected_row)]))
        print("(Type 'E' continue)")
    except:
        if selected_row.upper() == "E":
            break
        else:
            print("\nPlease select a number between 0 and " + str(len(ai_dataframe.career_title) - 1))
            pause(skip_pause)
print("Creating training and test data...", end="")
#Here set X and y, the variables I will be using for the A.I, to be equal to the career_title column (y) and the workplace_skills column (X)
#For each, I drop the opposite column which helps prevent errors.
y = ai_dataframe.career_title.drop(columns="workplace_skills")
X = ai_dataframe.workplace_skills.drop(columns="career_title")
#X_train, X_test, y_train, y_test = train_test_split(ai_dataframe.workplace_skills, ai_dataframe.career_title, random_state=11, test_size=0.20) Old splitting. Will not work.
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=11, test_size=0.20) #This splits the data of X and y into training data and testing data.
#The training data retains its labels to train the A.I. So its like saying, this picture of a banana is a banana and the banana has "banana" written on it. This is supervised.
#The test data is to test the A.I without labels to see how accurate the A.I is. So, this is like taking another picture of a banana without say it is one and asking what it is. This is unsupervised.
X_train = np.array(list(X_train), dtype=float)
X_test = np.array(list(X_test), dtype=float) #https://stackoverflow.com/questions/40514019/setting-an-array-element-with-a-sequence-error-while-training-svm-to-classify-im
y_train = np.array(list(y_train), dtype=float)
y_test = np.array(list(y_test), dtype=float)
#Here, to avoid a lot of errors, I set every training and test variable to an numpy array and specifiy that the values are floats, not objects. (As it was them being 'objects' that caused a lot of errors)
print("Done\nTraining and test data created")
print("X_train.shape is ", X_train.shape, "\ny_train.shape is ", y_train.shape)
print("X_test.shape is ", X_test.shape, "\ny_test.shape is ", y_test.shape)
pause(skip_pause)
print("Counting words for mapping. Highly inefficient because I'm too tired to make it better...", end="")
#---------------------------------------------------------------------------------------------------------
#This section goes through the ai_dataframe_old and counts every instance of every word in the career_title column. This does not affect
#mapping and was merely for me to visualise the most common words. In future iterations, I could potentially use this to automate the mapping
#but I'm not sure how viable that would be.
#For this reason, I will leave this section uncommeted because it is not important.
word_count = {}
for item in ai_dataframe_old.career_title:
    item = item.split(" ")
    for word in item:
        if word not in word_count:
            word_count[word] = 1
        else:
            word_count[word] += 1
word_count_alt = []
for item in word_count:
    if item not in "-":
        word_count_alt.append((item, word_count[item]))
print("Done\nSaving word counts to word_counts.txt...", end="")
word_count_alt = sorted(word_count_alt, key=lambda x: x[1], reverse=True)
word_count_file = open("word_counts.txt", "w+")
try:
    for item in word_count_alt:
        text = str(item[0]) + " with a count of " + str(item[1]) + "\n"
        word_count_file.write(text)
    print("Done")
except:
    print("Failed\nError: Something went wrong while saving. The file may be read only or this program might not have the correct privillages to write in the directory")
word_count_file.close()
pause(skip_pause)
#---------------------------------------------------------------------------------------------------------
print("Creating KNN.")
knn = KNeighborsClassifier() #Creates an instance of the KNN classifier to evaluate the A.I
length = len(ai_dataframe.workplace_skills.iloc[0]) #Gets the length of the first list of workplace skills.
print("Making sure all workplace_skills are same length...", end="")
#Checks if ALL lists in the workplace_skills columns are the same length.
#If any one of them is not, it will raise an exception as KNN will not work otherwise.
for item in ai_dataframe.workplace_skills:
    new_length = len(item)
    if new_length != length:
        raise Exception("One or more workplace_skill lists are not the same length!")
print("Done\nAll workplace_skill lists are the same length")
print("y_train is:\n", y_train)
knn.fit(X=X_train, y=y_train) #Fits the k-nearest neighbors classifier from the training dataset. (https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html#sklearn.neighbors.KNeighborsClassifier.fit)
#I do note quite understand what this means, but I know it normaliises the data for better clarification.
predicted = knn.predict(X=X_test)
#Testing the A.I. This takes the test data and has the A.I predict the answers.
expected = y_test
#This is the actual answers of the data.
print("KNN created.")
print("Predicted is ", predicted)
print("expected is ", expected)
pause(skip_pause)
print("Getting wrong amount...", end="")
wrong = [(p, e) for (p, e) in zip(predicted, expected) if p != e]
#A very confusing for loop that I've never seen before somehow. I looked up how it works and it is rather cool :)
#However, even though I now understand it, this particular one is still very odd and confusing.
#I am not sure if it were to simply save lines or if it's more efficient, but I feel that a normal for loop
#would make this far more readable.
#Anyway, it seems to create a tuple with p and e inside where p is predicted and e is expected (which have been made a tuple themselves).
#If p and e are not equal, it saves them to wrong.
print("Done\nWrong is ", wrong)
print("KNN score is ", f'{knn.score(X_test, y_test):.2%}')
pause(skip_pause)
print("Creating confusion matrix...", end="")
confusion = confusion_matrix(y_true=expected, y_pred=predicted)
#Creates a confusion matrix which shows the answers given by the A.I. These go from 0 to 9 and each number is how many times the A.I guessed that answer. (Damn, I'm bad at explaining that)
print("Done\nConfusion matrix is: \n", confusion)
print("Creating classification report...", end="")
names = []
#Gets the values from the career_map and stores them as a list called names.
for career_number in career_map:
    names.append(career_map[career_number])
del names[len(names) - 1] #Deletes the last item from names.
print("Done\nNames are:\n", names)
try:
    print("Classification report is:\n", classification_report(expected, predicted))#, target_names=names))
    #Generates a classifcation report which shows how accurate the A.I is. It shows the precision, recall, f1-score and support of each data (from 0 to 9)
    #It also shows the micro average and weighted average accuracy.
    #It should also list what each answer is rather than the number, but I am not sure what the target_names is supposed to be.
    #I thought it should be the labels from my career_map, but that caused it to not work at all, hence why it is commented out.
    #I could NOT find a solution to this.
except:
    print("Classification report failed because I have absolutely no idea what I'm doing") #lol
pause(skip_pause)
print("Creating heatmap and scores.")
confusion_dataframe = pd.DataFrame(confusion, index=range(0, len(confusion)), columns=range(0, len(confusion))) #Converts the confusion matrix into a dataframe.
#I might consider saving this to a CSV file. If this code doesn't do that, consider me to have forgetten about it.
print("Confusion DataFrame is:\n", confusion_dataframe) 
plt.figure() #Creates a new figure using matplotlib
axes = sns.heatmap (confusion_dataframe, annot=True, cmap='nipy_spectral_r') #Creates a heatmap of the confusion matrix and saves it as 'axes'.
axes.figure.show() #Displays the heatmap. If this were a jupyter notebook, this line wouldn't be needed as the notebook seems to print everything... Which is very strange.
#I still don't like jupyter notebook, but at this point I'm mostly indifferent to it.
pause(skip_pause)
kfold = KFold(n_splits=len(ai_dataframe.career_title) - 1, random_state=11, shuffle=True) #From what I understand, this trains the A.I as many times as the number of rows in the ai_dataframe dataframe.
scores = cross_val_score(estimator=knn, X=np.array(list(ai_dataframe.workplace_skills), dtype=float), y=np.array(list(ai_dataframe.career_title), dtype=float), cv=kfold)
#Gets the scores of the cross validations. All of the scores range from 0 to 1, but when you have too many, the decimals are not printed and it only shows "1." or "0." which is odd.
print("Scores are:\n", scores) #Prints the scores
print(f'Mean accuracy: {scores.mean():.2%}') #Prints the mean average of all the scores.
print(f'Accuracy standard deviation: {scores.std():.2%}') #Prints the standard deviation of the scores.
pause(skip_pause)
print("Saving model using pickle...", end="")
os.makedirs("./static/Model/")#Creates the directory "Model" in the same directory as this python file if the directory does not already exist.
knn_pickle = open('./static/Model/jobs_model', 'wb') #Opens or creates job_model.
pickle.dump(knn, knn_pickle) #Saves the A.I model to the opened file using pickle.
knn_pickle.close() #Closes the file.
print("Done\n'A.I' complete (lol)") #And breath... It's all over now... No more nightmares... For now...
pause(skip_pause) #Not sure why I put one more here, but whatever.
#A.I accuracy is quite low. (~34%)
#This is because of the low amount of samples which is made even lower as I had to drop some of them due to their soft skills being empty.
#I consider it to also be low as I feel that my career_map is really poor.
#I feel like the accuracy could be improved by using a better map and having more samples that contain a more varied selection of skills.
#It could also be made better by using other data such as the hard_skills, but I do not have the time for that.

