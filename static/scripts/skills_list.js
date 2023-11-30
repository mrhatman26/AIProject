console.log("skills_list.js loaded!");
skillsDropDown = document.getElementById("skills_list");
addButton = document.getElementById("add_skill_button");
selectedSkillsDiv = document.getElementById("selcted_skills");
selectedSkillsDiv.style.display = "none";
let selectableSkills = [];
let selectedSkills = [];
let br = document.createElement("br");
for (let l = 0; l < skillsDropDown.length; l++){
    selectableSkills.push(skillsDropDown.options[l].value);
}
console.log(selectableSkills);
addSkill = function(){
    var selectedSkill = skillsDropDown.value;
    if (selectedSkill != "Select Skills"){
        console.log("Button was clicked!");
        console.log("Current skill is " + selectedSkill);    
        for (var i = 0; i < skillsDropDown.length; i++){
            if (skillsDropDown.options[i].value == selectedSkill){
                selectedSkills.push(skillsDropDown.options[i].value);
                skillsDropDown.remove(i);
                console.log(selectedSkill + " has been removed from selected");
            }
        }
        if (selectedSkills.length >= 1){
            selectedSkillsDiv.innerHTML = "";
            selectedSkillsDiv.style.display = "inline-block"
            for (var i = 0; i < selectedSkills.length; i++){
                selectedSkillsDiv.append(selectedSkills[i]);
                selectedSkillsDiv.appendChild(br); //Does not work?
            }
        }
        else{
            selectedSkillsDiv.style.display = "none";
        }
    }
}

addButton.addEventListener("click", addSkill);