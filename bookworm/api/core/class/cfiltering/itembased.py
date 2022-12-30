import pandas as pd
import numpy as np
import warnings
import surprise
import time
import sklearn
import re

from matplotlib import pyplot as plt
from sklearn.metrics.pairwise import sigmoid_kernel
from surprise.model_selection import cross_validate

warnings.filterwarnings("ignore", "FutureWarnings")


class ItemBasedCF:
    def __init__(self, users, obj, ratings, k=10, max_rating=5.0, **kwargs) -> None:
        self.users = users
        self.users = self.users.reset_index()
        self.users = self.users.drop(columns=["index"])

        self.obj = obj

        self.ratings = ratings
        self.ratings = self.ratings.reset_index()
        self.ratings = self.ratings.drop(columns=["userId"])

        self.k = k
        self.max_rating = max_rating

        self.frequencies = {}
        self.deviations = {}

    def prepare_data(self):
        user_indices = list(self.ratings.index.values)

        users_ratings = []

        try:
            for user_index in user_indices:
                rated_book_indices = list(
                    self.ratings.iloc[user_index].to_numpy().nonzero()[0]
                )
                users_ratings.append(
                    {
                        user_index: dict(
                            self.ratings[self.ratings.columns[rated_book_indices]].iloc[
                                user_index
                            ]
                        )
                    }
                )
        except Exception as e:
            print(e)

        self.users_ratings = users_ratings

        return self.users_ratings

    def create_similarity_matrix(self):
        num_users = len(self.users)
        similarity_array = np.array(
            [
                self.__compute_similarity(
                    self.ratings.iloc[i, :], self.ratings.iloc[j, :]
                )
                for i in range(num_users)
                for j in range(num_users)
            ]
        )
        similarity_matrix = pd.DataFrame(
            data=similarity_array.reshape(self.users.shape[0], self.users.shape[0])
        )

        return similarity_matrix

    # [PRIVATE METHODS]
    def __compute_similarity(self, x, y):
        return np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))
