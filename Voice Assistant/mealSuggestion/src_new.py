import pandas as pd
import numpy as np
from IPython.core.interactiveshell import InteractiveShell
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from IPython.display import display
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate(
    'C:/Users/Utkarsha 1/Downloads/rudra-x-firebase-adminsdk-e2s77-2a7119b4c9.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://rudra-x-default-rtdb.firebaseio.com/'
})

# Reading from DB
ref_Liked = db.reference('Meal Suggestion/Liked meals/')
print(ref_Liked.get())

# Reading from DB
ref_Previous= db.reference('Meal Suggestion/Previous meals/')
print(ref_Previous.get())

# Reading from DB
ref_Foodlog = db.reference('Meal Suggestion/Food log/')
print(ref_Foodlog.get())


InteractiveShell.ast_node_interactivity = "all"


df1 = pd.read_csv('./db/food.csv')
df1.columns = ['food_id', 'title', 'canteen_id', 'num_orders', 'avg_rating', 'num_rating', 'category', 'tags', 'user_rating']
orders = pd.read_csv('./db/orders.csv')
orders.columns = ['order_id','food_id','canteen_id','user_id']

# updates user's orders by inserting a new row every time user makes an order
def insert_row_in_orders(title="",orders=orders):

    idx=(df1.loc[df1['title'] == title]).index

    upper_row = pd.DataFrame({'order_id':[0],'food_id':[idx[0]],'canteen_id':[1],'user_id':[1]}, index =[0])
    return pd.concat([upper_row, orders]).reset_index(drop = True)

# updates values of number of orders everytime user orders an old dish or if the food is not in database creates values for ratings, number of people who rated and number of orders for user
def avg_rating(user_rating, m =""):
    
    idx=(df1.loc[df1['title'] == m]).index

    # checks if food has already been rated by the user. If yes then only num_order value is updated 
    if df1.loc[idx[0],'user_rating']==0:
        df1.loc[idx,'user_rating']= user_rating
        df1.loc[idx,'avg_rating']= ((df1.loc[idx,'num_rating'].multiply(df1.loc[idx,'avg_rating']))+user_rating)/df1.loc[idx,'num_rating']+1
        df1.loc[idx,'num_rating']= df1.loc[idx,'num_rating'] + 1
    df1.loc[idx,'num_orders']= df1.loc[idx,'num_orders'] + 1
    
    return "none"

# inserts a new row at the top of our existing food dataframe for any food value given by the user that did not exist before. Returns concanted dataframe food. Index of new row is not required to be 0 and can be adjusted at any index position  
def insert_row(user_rating,category="",title="",df1=df1):

    top_row = pd.DataFrame({'food_id':[0],'title':[title],'canteen_id':[1], 'num_orders':[1], 'avg_rating':[user_rating], 'num_rating':[1], 'category':[category], 'tags':['healthy'], 'user_rating':[user_rating]}, index =[0])
    return pd.concat([top_row, df1]).reset_index(drop = True)

# checks if food name asked by user exists in the food dataframe
def check_foodname(user_rating,category="",title="",df1=df1):
    
    # if it exists
    if title in df1['title'].values:
        # checks user rating and updates ratings and order values in food dataframe
        avg_rating(user_rating,title)
    else: 
        # if it does not
        df1=insert_row(user_rating,category,title)
        # food_id is reset to match previous order(i.e. index 0 is 1, index 1 is 2....)
        df1['food_id']=df1['food_id']+1
    return df1

# checks if food name asked by user exists in the food dataframe. Rating and category passed in the case that it does not and a new row needs to be created 
user_rating=ref_Foodlog.get()
category=ref_Foodlog.get()
foodname=ref_Foodlog.get()
confirmation=ref_Foodlog.get()

answer=confirmation["meal1"]
para1=user_rating["meal1"]
para2=category["meal1"]
para3=foodname["meal1"]

df1=check_foodname(para1,para2,para3)

def confirm_order(answer):
    answer=answer.lower()
    bool(answer=="yes")
    return bool

print("\nDid you order the previous asked menu?\n")

confirm_order(answer)

# inserts a new row everytime user makes an order in the orders dataframe. check_foodname function needs to be passed first in case food value does not exist so that a food_id is created

if bool==answer:
    orders=insert_row_in_orders(para3)

# order_id is reset to match previous order(i.e. index 0 is 1, index 1 is 2....)
    orders['order_id']=orders['order_id']+1

# updates new dataframe to food.csv
df1.to_csv('./db/food.csv',index=False)
# updates new dataframe to orders.csv
orders.to_csv('./db/orders.csv', index=False)


# TODO: clean data

# creating combined string for each item
def create_soup(x): 
    tags = x['tags'].lower().split(', ')
    tags.extend(x['title'].lower().split())
    tags.extend(x['category'].lower().split())
    return " ".join(sorted(set(tags), key=tags.index))


df1['title'] = df1['title'].str.lower()
df1['combined'] = df1.apply(create_soup, axis=1)

# create the count matrix from CountVectorizer
count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(df1['combined'])

# compute the Cosine Similarity matrix based on the count_matrix
cosine_sim = cosine_similarity(count_matrix, count_matrix)

# returns index from food name or title column in food dataframe
indices_from_title = pd.Series(df1.index, index=df1['title'])
# returns index from food_id in food dataframe
indices_from_food_id = pd.Series(df1.index, index=df1['food_id'])

# function that takes in food title or food id as input and outputs most similar dishes 
def get_recommendations(title="", cosine_sim=cosine_sim, idx=-1):
    # get the index of the item that matches the title
    if idx == -1 and title != "":
        idx = indices_from_title[title]

    # get the pairwsie similarity scores of all dishes with that dish
    sim_scores = list(enumerate(cosine_sim[idx]))

    # sort the dishes based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # get the scores of the 10 most similar dishes
    sim_scores = sim_scores[1:3]

    # get the food indices
    food_indices = [i[0] for i in sim_scores]

    # return the top 10 most similar dishes
    return food_indices

foodname=ref_Liked.get()
title=foodname["meal1"]

df2= df1.loc[get_recommendations(title)]

matrix1 = df2.to_numpy()
a= display(matrix1[0][1])
b= display(matrix1[1][1])


# fetch few past orders of a user, based on which personalized recommendations are to be made
def get_latest_user_orders(user_id, orders, num_orders=3):
    counter = num_orders
    order_indices = []

    for index, row in orders[['user_id']].iterrows():
        if row.user_id == user_id:
            counter = counter - 1
            order_indices.append(index)
        if counter == 0:
            break

    return order_indices

# utility function that returns a DataFrame given the food_indices to be recommended
def get_recomms_df(food_indices, df1, columns, comment):
    row = 0
    df = pd.DataFrame(columns=columns)

    for i in food_indices:
        df.loc[row] = df1[['title', 'canteen_id']].loc[i]
        df.loc[row].comment = comment
        row = row + 1
    
    return df

# return food_indices for accomplishing personalized recommendation using Count Vectorizer
def personalised_recomms(orders, df1, user_id, columns, comment="based on your past orders"):
    order_indices = get_latest_user_orders(user_id, orders)

    food_ids = []
    food_indices = []
    recomm_indices = []

    for i in order_indices:
        food_ids.append(orders.loc[i].food_id)
    for i in food_ids:
        food_indices.append(indices_from_food_id[i])
    for i in food_indices:
        recomm_indices.extend(get_recommendations(idx=i))

    return get_recomms_df(set(recomm_indices), df1, columns, comment)

# utility function to get the home canteen given a user id
def get_user_home_canteen(users, user_id):
    for index, row in users[['user_id']].iterrows():
        if row.user_id == user_id:
            return users.loc[index].home_canteen
    return -1


orders = pd.read_csv('./db/orders.csv')
new_and_specials = pd.read_csv('./db/new_and_specials.csv')
users = pd.read_csv('./db/users.csv')

columns = ['title', 'canteen_id', 'comment']
current_user = 1
current_canteen = get_user_home_canteen(users, current_user)

# to get recommendations based on past orders

df=personalised_recomms(orders, df1, current_user, columns)

matrix1 = df.to_numpy()
print("\nBased on your previous orders..\n")
c= display(matrix1[0][0])
d= display(matrix1[1][0])


ref_Liked.update({
    'Liked meals': {
        "meal1": a,
        "meal2": b
    }
})

if bool==answer:

    ref_Foodlog.update({
        'Food log': {
            "meal1": para3,
            "meal2": b
       }
    })

ref_Previous.update({
    'Previous meals': {
        "meal1": c,
        "meal2": d
    }
})