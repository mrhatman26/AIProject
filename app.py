from flask import Flask, render_template, url_for, request, redirect
from misc_functions import multi_replace
from sklearn.neighbors import KNeighborsClassifier
import sys, pickle
import numpy as np

app = Flask(__name__)

#Home
@app.route('/')
def home(): #Just the home page. Nothing noteworthy.
    return render_template('home.html', page_name="About")

@app.route('/job_search/data=<ai_answer>') #This page handles the user's skills. Here they can add them to a list and the submit them for the A.I
#The A.I also redirects here with its answer which will change what's displayed slightly. But that part is controlled by the JavaScript file.
def job_search(ai_answer):
    skills_file = open("./static/skills_file.txt", "r") #Open the list of skills from the file
    skills_list = []
    for item in skills_file:
        item = multi_replace(item, "", "'", "\n") #Format the skills to remove underscores and hyphens and other formatting stuff.
        item = item.title().replace("-", " ")
        skills_list.append(item)
    skills_file.close()
    if ai_answer is None or ai_answer == "None":
        ai_answer = "NoAnswer" #If the A.I has not given an answer because the user just loaded this page, set the answer to NoAnswer so that the
        #JavaScript file knows to continue as normal.
    return render_template('skills.html', page="Job Search", skills=skills_list, ai_answer=ai_answer)

@app.route('/process/skills_data=<skills_data>')
def ai_process(skills_data):
    skill_data = skills_data #Kind of redundant, but just to make sure.
    print("skill_data is " + skill_data + "\nskill_data length is " + str(len(skill_data)))
    if skill_data is not None and len(skill_data) >= 1: #Make sure there is actually text in the skill list.
        skill_data = skill_data.replace("%20", " ") #Replace HTTP encoding of spaces with actual spaces.
        skill_data = skill_data.split("+") #Split the skilsl data into a list and use + as the divider.
        print(skill_data, flush=True) #Flush is required for consistent printing in Flask. Without it, printing usually does nothing.
        ai_model_file = open("./static/Model/jobs_model", "rb") #Open the A.I model's pickle file.
        ai_model = pickle.load(ai_model_file) #Load the A.I from its pickle file.
        ai_model_file.close()
        list_order_file = open("./static/Model/list_order.txt", "r")
        ai_skill_data = []
        skill_found = False
        for column in list_order_file:
            skill_found = False
            column = column.replace("-", " ")
            column = column.replace("_", " ")
            for skill in skill_data:
                print("Skill is " + skill, flush=True)
                if skill.lower() in column.lower():
                    ai_skill_data.append(1)
                    skill_found = True
            if skill_found is not True:
                ai_skill_data.append(0)
        print(ai_skill_data, flush=True)
        ai_skill_data = np.array(list(ai_skill_data), dtype=float)
        ai_skill_data = ai_skill_data.reshape(1, -1)
        out = ai_model.predict(X=ai_skill_data)
        print(out, flush=True)
        career_map = {"Developer": 0, "Engineer": 1, "Analyst": 2, "Designer": 3, "Techn  ician": 4, "Consultant": 5, "Adviser": 6, "Architect": 7, "Administrator": 8, "Strategist": 9}
        out_mapped = list(career_map.keys())[list(career_map.values()).index(out)]
        print(out_mapped)
        return redirect('/job_search/data=' + out_mapped)
    else:
        return redirect('/')

#Launch Website
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
    #from waitress import serve
    #serve(app, host="0.0.0.0", port=5000)