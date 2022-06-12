firebase.auth().onAuthStateChanged(user => {
    if (user) {
        this.user = user;

        //username.innerHTML = user.displayName;
        UserID = firebase.auth().currentUser.uid;
        console.log(UserID);
        firebase.database().ref('users/' + UserID + '/accessLevel/').once('value', (snap) => {
            var role = snap.val();
            console.log(role);
            document.getElementById("AccessLevel").innerHTML = role;
        });
        firebase.database().ref('users/' + UserID + '/name/').once('value', (snap) => {
            var name = snap.val();
            console.log(name);
            document.getElementById("name").innerHTML = name;
        });
    }
    else {
        console.log("User not signed in");
    }
});

var newWindow;

function openWindow() {
    newWindow = window.open('addUser/addUser.html', '_blank', 'location=yes,height=570,width=520,scrollbars=yes,status=yes');
    /* firebase.auth().createUserWithEmailAndPassword("abc@gmail.com", "12345678").then((userCredential) => {
        var user = userCredential.user;
        console.log(user);
    }).catch((error) => {
        var errorCode = error.code;
        var errorMessage = error.message;
    }); */
}

function closeWindow() {
    newWindow.close();
}