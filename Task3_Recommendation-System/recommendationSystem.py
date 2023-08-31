import pandas as pd
import re

movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")


def format_title(title):
    title = re.sub("[^a-zA-Z ]", "", title)
    return title.strip().lower()  # Strip spaces and convert to lowercase


movies["clean_title"] = movies["title"].apply(format_title)


def find_similar_movies(movie_id):
    similar_users = ratings[(ratings["movieId"] == movie_id) & (ratings["rating"] > 4)]["userId"].unique()
    similar_user_recs = ratings[(ratings["userId"].isin(similar_users)) & (ratings["rating"] > 4)]["movieId"]
    similar_user_recs = similar_user_recs.value_counts() / len(similar_users)

    similar_user_recs = similar_user_recs[similar_user_recs > .10]
    all_users = ratings[(ratings["movieId"].isin(similar_user_recs.index)) & (ratings["rating"] > 4)]
    all_user_recs = all_users["movieId"].value_counts() / len(all_users["userId"].unique())
    rec_percentages = pd.concat([similar_user_recs, all_user_recs], axis=1)
    rec_percentages.columns = ["similar", "all"]

    rec_percentages["score"] = rec_percentages["similar"] / rec_percentages["all"]
    rec_percentages = rec_percentages.sort_values("score", ascending=False)
    return rec_percentages.head(10).merge(movies, left_index=True, right_on="movieId")[["score", "title", "genres"]]


def display_top_recommendations(movie_title, top_10_recommendations):
    print(f"Since You liked {movie_title} movie then these are top 10 recommendations for you: \n")
    for i in range(0, 10):
        print(f"=============== recommendation # {i + 1} ===============")
        ith_title = top_10_recommendations.iloc[i]["title"]
        ith_genres = top_10_recommendations.iloc[i]["genres"]
        print("Title: ", ith_title)
        print("Genres: ", ith_genres)
        # print(top_10_recommendations.iloc[i])


def recommendation_system():
    print("========= Welcome to our Recommendation system =========== ")
    movie_name = str(input("Enter a movie name: ")).lower().strip()
    if movie_name in movies["clean_title"].values:
        desired_movie = movies[movies["clean_title"] == movie_name]
        movie_id = desired_movie["movieId"].values[0]
        movie_title = desired_movie["title"].values[0]
        top_10_recommendations = find_similar_movies(movie_id)
        display_top_recommendations(movie_title, top_10_recommendations)
    else:
        print("this movie is not in our system")


recommendation_system()
