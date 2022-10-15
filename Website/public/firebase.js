// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyA3sxz8LTLgtvdkvBAaLvZO7gBLqzuLM_A",
    authDomain: "rudra-x.firebaseapp.com",
    databaseURL: "https://rudra-x-default-rtdb.firebaseio.com",
    projectId: "rudra-x",
    storageBucket: "rudra-x.appspot.com",
    messagingSenderId: "825213372220",
    appId: "1:825213372220:web:8f22d587cfc44237848039",

    clientId: "825213372220-91aurkmepobjc9pahjd8c8m3ftkbmp71.apps.googleusercontent.com",

    scopes: [
        "email",
        "profile"
    ]
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

firebase.auth().onAuthStateChanged(user => {
    if (user) {
        this.user = user;

        //username.innerHTML = user.uid;
        //username = user.uid;
        console.log(user.uid);
        console.log("xyz");
        const displayName = user.displayName;
        const email = user.email;
        const photoURL = user.photoURL;

        console.log("Name: " + displayName);
        console.log("email: " + email);
        console.log("photoURL: " + photoURL);
    }
    else {
        console.log("abc")
    }
});