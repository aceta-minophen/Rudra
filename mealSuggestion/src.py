#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"


# # Lunchbox App ML Engine
#
# This is the Recommendation Engine that will be used in building the <b>Lunchbox App</b>, a platform for ordering food and keeping track of user expenditure and canteen sales. Regardless of whether or not this is actually implemented in all the canteens of <b>IIT Kanpur</b>, given the potential for frauds & cyber-attacks, I will complete the platform.
#
# Also, <b>I would be open-sourcing the app</b> so that any campus can implement a <b>cash-less & integrated system of ordering food</b> across their whole campus. After all, what good are IITs for if our canteens still keep track of student accounts on paper registers!

# ## Demographic Filtering
#
# Suggesting the users items that were well-received and are popular among the users, in general. Most trending items and items with the best rating rise to the top and get shortlisted for recommendation.

# In[2]:


# Importing db of food items across all canteens registered on the platform
df1 = pd.read_csv('./db/food.csv')
df1.columns = ['food_id', 'title', 'canteen_id', 'price', 'num_orders',
               'avg_rating', 'num_rating', 'category', 'tags']

df1


# In[3]:


# mean of average ratings of all items
C = df1['avg_rating'].mean()

# the minimum number of votes required to appear in recommendation list, i.e, 60th percentile among 'num_rating'
m = df1['num_rating'].quantile(0.60)

# items that qualify the criteria of minimum num of votes
q_items = df1.copy().loc[df1['num_rating'] >= m]

# Calculation of weighted rating based on the IMDB formula


def weighted_rating(x, m=m, C=C):
    v = x['num_rating']
    R = x['avg_rating']
    return (v/(v+m) * R) + (m/(m+v) * C)


# Applying weighted_rating to qualified items
q_items['score'] = q_items.apply(weighted_rating, axis=1)

# Shortlisting the top rated items and popular items
top_rated_items = q_items.sort_values('score', ascending=False)
pop_items = df1.sort_values('num_orders', ascending=False)


# In[4]:


# Display results of demographic filtering
top_rated_items[['title', 'num_rating', 'avg_rating', 'score']].head()
pop_items[['title', 'num_orders']].head()


# ## Content Based Filtering
#
# A bit more personalised recommendation. We will be analysing the past orders of the user and suggesting back those items which are similar.
#
# Also, since each person has a "home canteen", the user should be notified any new items included in the menu by the vendor.
#
# We will be using <b>Count Vectorizer</b> from <b>Scikit-Learn</b> to find similarity between items based on their title, category and tags. To bring all these properties of each item together we create a <b>"soup"</b> of tags. <b>"Soup"</b> is a processed string correspnding to each item, formed using constituent words of tags, tile and category.

# In[5]:


# TODO: clean data

# Creating soup string for each item
def create_soup(x):
    tags = x['tags'].lower().split(', ')
    tags.extend(x['title'].lower().split())
    tags.extend(x['category'].lower().split())
    return " ".join(sorted(set(tags), key=tags.index))


df1['title'] = df1['title'].str.lower()
df1['combined'] = df1.apply(create_soup, axis=1)
df1.head(30)


# In[6]:


df1['title'][1]


# In[7]:


# Import CountVectorizer and create the count matrix
count = CountVectorizer(stop_words='english')

# df1['combined']
count_matrix = count.fit_transform(df1['combined'])

# Compute the Cosine Similarity matrix based on the count_matrix
cosine_sim = cosine_similarity(count_matrix, count_matrix)

indices_from_title = pd.Series(df1.index, index=df1['title'])
indices_from_food_id = pd.Series(df1.index, index=df1['food_id'])


# In[8]:


# Function that takes in food title or food id as input and outputs most similar dishes
def get_recommendations(title="", cosine_sim=cosine_sim, idx=-1):
    # Get the index of the item that matches the title
    if idx == -1 and title != "":
        idx = indices_from_title[title]

    # Get the pairwsie similarity scores of all dishes with that dish
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the dishes based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar dishes
    sim_scores = sim_scores[1:3]

    # Get the food indices
    food_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar dishes
    return food_indices


# In[9]:


df1.loc[get_recommendations(title="paneer tikka masala")]


# We will now some functions, some of which are utility functions, others are actually the functions which will help get personalised recommendations for current user.

# In[10]:


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
        row = row+1
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

# fetch items from previously calculated top_rated_items list


def get_top_rated_items(top_rated_items, df1, columns, comment="top rated items across canteens"):
    food_indices = []

    for index, row in top_rated_items.iterrows():
        food_indices.append(
            indices_from_food_id[top_rated_items.loc[index].food_id])

    return get_recomms_df(food_indices, df1, columns, comment)

# fetch items from previously calculated pop_items list


def get_popular_items(pop_items, df1, columns, comment="most popular items across canteens"):
    food_indices = []

    for index, row in pop_items.iterrows():
        food_indices.append(indices_from_food_id[pop_items.loc[index].food_id])

    return get_recomms_df(food_indices, df1, columns, comment)


# ### After all the hard work, we finally get the recommendations

# In[11]:

orders = pd.read_csv('./db/orders.csv')
new_and_specials = pd.read_csv('./db/new_and_specials.csv')
users = pd.read_csv('./db/users.csv')

columns = ['title', 'canteen_id', 'comment']
current_user = 3
current_canteen = get_user_home_canteen(users, current_user)


personalised_recomms(orders, df1, current_user, columns)
get_top_rated_items(top_rated_items, df1, columns)
get_popular_items(pop_items, df1, columns).head(3)


# These are just simple algorithms to make personalised and even general recommendations to users. We can easily use collaborative filtering or incorporate neural networks to make our prediction even better. However, these are more computationally intensive methods. Kinda overkill, IMO! Let's build that app first!

# #### Star the repository and send in your PRs if you think the engine needs any improvement or helping me implement some more advanced features.
