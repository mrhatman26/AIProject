console.log("skills_list.js loaded!");
let skillsDropDown = document.getElementById("skills_list");
let addButton = document.getElementById("add_skill_button");
let resetButton = document.getElementById("reset_skills_button");
let submitButton = document.getElementById("submit_skills_button");
let selectedSkillsDiv = document.getElementById("selcted_skills");
let hiddenAIAnswer = document.getElementById("hidden_ai_answer")
hiddenAIAnswer.style.display = "None";
let errorMessage = document.getElementById("skills_error");
errorMessage.style.display = "none";
errorMessage.style.color = "rgb(255, 0, 0)";
selectedSkillsDiv.style.display = "none";
let selectableSkills = [];
let selectedSkills = [];
let br = document.createElement("br");
let resultShown = false
for (let l = 0; l < skillsDropDown.length; l++){
    selectableSkills.push(skillsDropDown.options[l].value);
}
if (!window.location.href.includes("None")){
    console.log("AI Answer given, disabling buttons and showing answer...");
    submitButton.disabled = true;
    addButton.disabled = true;
    let response = window.location.href.split('=')[1];
    responseText = document.createElement("p");
    responseText.innerHTML = "Your recommended job type is: " + response;
    selectedSkillsDiv.appendChild(responseText);
    selectedSkillsDiv.style.display = "block";
    selectedSkillsDiv.style.fontSize = "28px";
    resultShown = true;
}
console.log(selectableSkills);
function addSkill(){ //This function adds the currently selected skill from the drop down to the selectedSkills array and also displays that array.
    var selectedSkill = skillsDropDown.value;
    console.log("selectedSkill is " + selectedSkill);
    if (selectedSkill != "Select Skills" && selectedSkill != "No More Options"){ //If the current skill is NOT the default option, continue.
        console.log("Button was clicked!");
        console.log("Current skill is " + selectedSkill);
        for (var i = 0; i < skillsDropDown.length; i++){ //Go through the skillsDropDown
            if (skillsDropDown.options[i].value == selectedSkill){ //If the selectedSkill is in the drop down's array, remove the option from the array and add it to the selectedSkills array.
                var noMoreOption = document.createElement('option')
                noMoreOption.value = "No More Options";
                noMoreOption.innerHTML = noMoreOption.value;
                noMoreOption.selected = true;
                selectedSkills.push(skillsDropDown.options[i].value);
                skillsDropDown.remove(i);
                console.log(skillsDropDown.length);
                if (skillsDropDown.length < 2){ //If there are no more options in the drop down, show "No More Options" instead.
                    skillsDropDown.appendChild(noMoreOption);
                }
                if (selectedSkills.length > 9){ //If there is 10 selected options, warn the user that they have selected the maximum and remove all options from the drop down and replace it with "No More Options";
                    errorMessage.innerHTML = "Maximum skills selected!";
                    errorMessage.style.display = "block";
                    for (var l = 0; l < skillsDropDown.length; l++){
                        skillsDropDown.remove(l);
                    }
                    skillsDropDown.appendChild(noMoreOption);
                }
                console.log(selectedSkill + " has been removed from selected");
            }
        }
        if (selectedSkills.length >= 1){ //If the selectedSkills array has elements:
            selectedSkillsDiv.innerHTML = "";
            selectedSkillsDiv.style.display = "block"; //Display the selectedSkillsDiv.
            /*Removes, sort of, duplicates from the selectedSkills array.
            This is necessary for some reason because the values of "Problem Solver" OR "Problem Solving" get added twice.
            But it is only those two values.
            How does that make any sense? (╯°□°)╯︵ ┻━┻*/
            for (var i = 1; i < selectedSkills.length; i++){ 
                if (selectedSkills[i] == selectedSkills[i - 1]){
                    selectedSkills.splice(i, 1);
                }
            }
            for (var i = 0; i < selectedSkills.length; i++){ //Add add the selectedSkills options to it one by one.
                selectedSkillElement = document.createElement('p');
                selectedSkillElement.innerHTML = (i + 1) + ". "  + selectedSkills[i];
                selectedSkillsDiv.appendChild(selectedSkillElement);
            }
            console.log(selectedSkills);
        }
        else{
            selectedSkillsDiv.style.display = "none"; //If the selectedSkills array is empty, hide the div.
        }
    }
}

function resetSkills(){ //Resets the skills drop down and removes all selected skills, hides the errorMessage and hide the selected skills divider.
    window.location.href = '/job_search/data="None"'
}

function submitSkills(){
    if (selectedSkills.length >= 1){
        submitButton.disabled = true;
        console.log("Sending skills data to Python Flask");
        let skillsString = "";
        for (var i = 0; i < selectedSkills.length; i++){
            console.log("Current skill is " + selectedSkills[i])
            if (skillsString === ""){
                skillsString = selectedSkills[i];
            }
            else{
                skillsString = skillsString + "+" + selectedSkills[i];
            }
        }
        skillsString = "/process/skills_data=" + skillsString;
        window.location.href = skillsString;
    }
    else{
        errorMessage.innerHTML = "You haven't selected any skills!";
        errorMessage.style.display = "block";
    }
}

addButton.addEventListener("click", addSkill);
resetButton.addEventListener("click", resetSkills);
submitButton.addEventListener("click", submitSkills);