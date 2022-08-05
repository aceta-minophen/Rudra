from operator import concat, index
from turtle import title
from unicodedata import category
import pandas as pd
import numpy as np
from IPython.core.interactiveshell import InteractiveShell
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from IPython.display import display
from tabulate import tabulate

InteractiveShell.ast_node_interactivity = "all"

df1 = pd.read_csv('./db/food.csv')
df1.columns = ['food_id', 'title', 'canteen_id', 'num_orders',
               'avg_rating', 'num_rating', 'category', 'tags', 'user_rating']


def avg_rating(user_rating, m=""):
    row = df1.index[(df1['title'] == m)].tolist()
    df1["avg_rating"] = df1.loc9(
        (["avg_rating"]*["num_rating"]+["user_rating"])/["num_rating+1"])[index == row]
    df1["num_rating"] = df1["num_rating"][index == row]+1

    return "none"


def new_row(user_rating, m=""):

    m = m.lower()

    if m not in df1['title'].unique():
        line = df2({"food_id": 1, "title": m, "canteen_id": 1, "num_orders": 1,
                   "avg_rating": user_rating, "num_rating": 1, "user_rating": user_rating}, index=[0])
        df2 = concat([df1.iloc[:], line, df1.iloc[:]]).reset_index(drop=True)

    else:
        avg_rating(user_rating)

    return "none"


new_row(3.5, "matar kulcha")


# TODO: clean data

def create_soup(x):
    tags = x['tags'].lower().split(', ')
    tags.extend(x['title'].lower().split())
    tags.extend(x['category'].lower().split())
    return " ".join(sorted(set(tags), key=tags.index))


df1['title'] = df1['title'].str.lower()
df1['combined'] = df1.apply(create_soup, axis=1)

count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(df1['combined'])


cosine_sim = cosine_similarity(count_matrix, count_matrix)

indices_from_title = pd.Series(df1.index, index=df1['title'])
indices_from_food_id = pd.Series(df1.index, index=df1['food_id'])


def get_recommendations(title="", cosine_sim=cosine_sim, idx=-1):

    if idx == -1 and title != "":
        idx = indices_from_title[title]

    sim_scores = list(enumerate(cosine_sim[idx]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    sim_scores = sim_scores[1:3]

    food_indices = [i[0] for i in sim_scores]

    return food_indices


df2 = df1.loc[get_recommendations(title="paneer tikka masala")]
matrix1 = df2.to_numpy()
a = display(matrix1[0][1])
b = display(matrix1[1][1])


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


def get_recomms_df(food_indices, df1, columns, comment):
    row = 0
    df = pd.DataFrame(columns=columns)

    for i in food_indices:
        df.loc[row] = df1[['title', 'canteen_id']].loc[i]
        df.loc[row].comment = comment
        row = row + 1
    matrix1 = df.to_numpy()
    print("\nBased on your previous orders..\n")
    c = display(matrix1[0][0])
    d = display(matrix1[1][0])
    return df


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


def get_user_home_canteen(users, user_id):
    for index, row in users[['user_id']].iterrows():
        if row.user_id == user_id:
            return users.loc[index].home_canteen
    return -1


orders = pd.read_csv('./db/orders.csv')
new_and_specials = pd.read_csv('./db/new_and_specials.csv')
users = pd.read_csv('./db/users.csv')

columns = ['title', 'canteen_id', 'comment']
current_user = 3
current_canteen = get_user_home_canteen(users, current_user)

personalised_recomms(orders, df1, current_user, columns)
