var subjectObject = {
    "Head": {
    },
    "Leader": {
        "Task1": ["subtask1", "subtask2", "subtask3"],
        "Task2": ["subtask4", "subtask5", "subtask6"]
    },
    "Member": {
        "Task1": ["subtask1", "subtask2", "subtask3"],
        "Task2": ["subtask4", "subtask5", "subtask6"]
    }
}
window.onload = function () {
    var subjectSel = document.getElementById("role");
    var topicSel = document.getElementById("tasks");
    var chapterSel = document.getElementById("subtasks");
    for (var x in subjectObject) {
        subjectSel.options[subjectSel.options.length] = new Option(x, x);
    }
    subjectSel.onchange = function () {
        //empty Chapters- and Topics- dropdowns
        chapterSel.length = 1;
        topicSel.length = 1;
        //display correct values
        for (var y in subjectObject[this.value]) {
            topicSel.options[topicSel.options.length] = new Option(y, y);
        }
    }
    topicSel.onchange = function () {
        //empty Chapters dropdown
        chapterSel.length = 1;
        //display correct values
        var z = subjectObject[subjectSel.value][this.value];
        for (var i = 0; i < z.length; i++) {
            chapterSel.options[chapterSel.options.length] = new Option(z[i], z[i]);
        }
    }
}

var name = document.querySelector("#name").value;
var role = document.querySelector("#role").value;
var tasks = document.querySelector("#tasks").value;

console.log(name);
console.log(role);
console.log(tasks);

function createUser() {
    console.log(name);
    console.log(role);
    console.log(tasks);
    //window.close();
    /* firebase.auth().createUserWithEmailAndPassword("abc@gmail.com", "12345678").then((userCredential) => {
        var user = userCredential.user;
        console.log(user);
    }).catch((error) => {
        var errorCode = error.code;
        var errorMessage = error.message;
    }); */
}

document
    .getElementById('newUserForm')
    .addEventListener('submit', formSubmit);

function formSubmit(e) {
    e.preventDefault();
    var name = document.querySelector("#name");
    var role = document.querySelector("#role");
    var tasks = document.querySelector("#tasks");
    console.log(name);
    console.log(role);
    console.log(tasks);
}