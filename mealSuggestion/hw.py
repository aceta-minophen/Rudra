
from firebase import Firebase

config = {
    "apiKey": "AIzaSyA3sxz8LTLgtvdkvBAaLvZO7gBLqzuLM_A",
    "authDomain": "rudra-x.firebaseapp.com",
    "databaseURL": "https://rudra-x-default-rtdb.firebaseio.com",
    "storageBucket": "rudra-x.appspot.com"
}

firebase = Firebase(config)

db1 = firebase.database()

# Reading from DB
ref = db1.child('Meal Suggestion/Food log/')
meal = ref.child("meal1").get()
print(meal.val())
