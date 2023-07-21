"""
Contains various recommondation implementations
all algorithms return a list of movieids
"""

import pandas as pd
import numpy as np
from utils import movie_ratings, titles, movies
import pickle


def recommend_random(k=3):
    return movies['title'].sample(k).to_list()

with open('nmf_model1.pkl','rb') as file:
    nmf_model = pickle.load(file)




def recommend_with_NMF(query, model=nmf_model, movie_title = titles, k=10):
    """
    Filters and recommends the top k movies for any given input query based on a trained NMF model. 
    Returns a list of k movie ids.
    """
    

    # 1. candidate generation
    print(nmf_model.feature_names_in_)
    print(titles)
    
    # 2. construct new_user-item dataframe given the query
    new_user_dataframe =  pd.DataFrame(query, columns=movie_title, index=["new_user"])
    new_user_dataframe_imputed = new_user_dataframe.fillna(movie_ratings.mean())
   
    # 3. scoring
    P_new_user_matrix = model.transform(new_user_dataframe_imputed)
    
    # calculate the score with the NMF model
    Q_matrix = model.components_
    R_hat_new_user_matrix = np.dot(P_new_user_matrix,Q_matrix)
    
    R_hat_new_user = pd.DataFrame(data=R_hat_new_user_matrix, columns=movie_title, index = ['new_user'])

    # 4. ranking
    sorted_list = R_hat_new_user.transpose().sort_values(by="new_user", ascending=False).index.to_list()
    rated_movies = list(query.keys())

    
    # filter out movies already seen by the user
    recommendations = [movie for movie in sorted_list if movie not in rated_movies]
    
    
    # return the top-k highest rated movie ids or titles

    return recommendations[:k]


def recommend_neighborhood(query, model, k=3):
    """
    Filters and recommends the top k movies for any given input query based on a trained nearest neighbors model. 
    Returns a list of k movie ids.
    """   
    pass
    

