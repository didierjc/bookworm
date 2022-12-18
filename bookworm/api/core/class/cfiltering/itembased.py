class ItemBasedCF():
    def __init__(self, users, obj, ratings, k=10, max_rating=5.0, **kwargs) -> None:
        self.users = users
        self.users = self.users.reset_index()
        self.users = self.users.drop(columns=['index'])

        self.obj = obj

        self.ratings = ratings
        self.ratings = self.ratings.reset_index()
        self.ratings = self.ratings.drop(columns=['userId'])

        self.k = k
        self.max_rating = max_rating

        self.frequencies = {}
        self.deviations = {}

    def prepare_data(self):
        user_indices = list(self.ratings.index.values)

        users_ratings = []

        try:
            for user_index in user_indices:
                rated_book_indices = list(self.ratings.iloc[user_index].to_numpy().nonzero()[0])
                users_ratings.append({user_index: dict(self.ratings[self.ratings.columns[rated_book_indices]].iloc[user_index])})
        except Exception as e:
            print(e)
    
        self.users_ratings = users_ratings
        
        return self.users_ratings
