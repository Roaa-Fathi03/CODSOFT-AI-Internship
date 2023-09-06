import pandas as pd
import re

movies = pd.read_csv("movies.csv")
m_ratings = pd.read_csv("ratings.csv")

books = pd.read_csv("books.txt")
b_ratings = pd.read_csv("books-ratings.txt")


def format_movies_title(title):
    title = re.sub("[^a-zA-Z' ]", "", title)
    return title.strip().lower()  # Strip spaces and convert to lowercase


def format_books_title(title):
    title = re.sub("[^a-zA-Z ]", "", title)
    return title.strip().lower()


movies["clean_title"] = movies["title"].apply(format_movies_title)
books["clean_title"] = books["title"].apply(format_movies_title)


def find_similar_movies(movie_id):
    # finds people favorite movies that liked the same book you liked too and gets their full record
    similar_users = m_ratings[(m_ratings["movieId"] == movie_id) & (m_ratings["rating"] > 4)]["userId"].unique()
    similar_user_recs = m_ratings[(m_ratings["userId"].isin(similar_users)) & (m_ratings["rating"] > 4)]["movieId"]
    similar_user_recs = similar_user_recs.value_counts() / len(similar_users)

    similar_user_recs = similar_user_recs[similar_user_recs > .10]
    all_users = m_ratings[(m_ratings["movieId"].isin(similar_user_recs.index)) & (m_ratings["rating"] > 4)]
    all_user_recs = all_users["movieId"].value_counts() / len(all_users["userId"].unique())
    rec_percentages = pd.concat([similar_user_recs, all_user_recs], axis=1)
    rec_percentages.columns = ["similar", "all"] # create two col with names similar and all

    # checks if they liked a movie because they have same taste not a movie everyone likes
    rec_percentages["score"] = rec_percentages["similar"] / rec_percentages["all"]
    rec_percentages = rec_percentages.sort_values("score", ascending=False)

    return rec_percentages.head(10).merge(movies, left_index=True, right_on="movieId")[["score", "title", "genres"]]


def find_similar_books(book_id):
    # finds people favorite books that liked the same book you liked too and gets their full record
    similar_users = b_ratings[(b_ratings["bookId"] == book_id) & (b_ratings["rating"] > 4)]["userId"].unique()
    similar_user_recs = b_ratings[(b_ratings["userId"].isin(similar_users)) & (b_ratings["rating"] > 4)]["bookId"]
    similar_user_recs = similar_user_recs.value_counts() / len(similar_users)

    similar_user_recs = similar_user_recs[similar_user_recs > .10]
    all_users = b_ratings[(b_ratings["bookId"].isin(similar_user_recs.index)) & (b_ratings["rating"] > 4)]
    all_user_recs = all_users["bookId"].value_counts() / len(all_users["userId"].unique())
    rec_percentages = pd.concat([similar_user_recs, all_user_recs], axis=1)
    rec_percentages.columns = ["similar", "all"]  # create two col with names similar and all

    # checks if they liked a book because they have same taste not a book everyone likes
    rec_percentages["score"] = rec_percentages["similar"] / rec_percentages["all"]
    rec_percentages = rec_percentages.sort_values("score", ascending=False)

    return rec_percentages.head(11).merge(books, left_index=True, right_on="bookId")[["score", "title", "genres"]]


def display_top_recommendations(item_name, top_recommendations):
    if len(top_recommendations) > 1:
        print(f"Since You liked ** {item_name} ** then these are top recommendations for you: \n")
        i = 1
        while i < len(top_recommendations):
            print(f"=============== recommendation # {i} ===============")
            ith_title = top_recommendations.iloc[i]["title"]
            ith_genres = top_recommendations.iloc[i]["genres"]
            print("Title: ", ith_title)
            print("Genres: ", ith_genres)
            i += 1
    else:
        print("Sorry, No recommendations match this item.\n")


def recommendation_system():
    choice = None
    while True:
        print("\n========= Welcome to our Recommendation system =========== ")
        print("Choose from the list:\n"
              "1. Movie recommendations.\n"
              "2. Books recommendations.\n"
              "3. End\n")
        try:
            choice = int(input("Enter 1, 2 or 3: "))
            if choice == 1:  # we generate 9 recommendations for movies because we have a big dataset
                movie_name = str(input("\nEnter a movie name: ")).lower().strip()
                if movie_name in movies["clean_title"].values:
                    desired_movie = movies[movies["clean_title"] == movie_name]
                    movie_id = desired_movie["movieId"].values[0]
                    movie_title = desired_movie["title"].values[0]
                    top_10_recommendations = find_similar_movies(movie_id)
                    display_top_recommendations(movie_title, top_10_recommendations)
                else:
                    print("this movie is not in our system")

            elif choice == 2:  # we generate fewer recommendations for books because we have a smaller dataset
                book_name = str(input("\nEnter a book name: ")).lower().strip()
                if book_name in books["clean_title"].values:
                    desired_book = books[books["clean_title"] == book_name]
                    book_id = desired_book["bookId"].values[0]
                    book_title = desired_book["title"].values[0]
                    top_recommendations = find_similar_books(book_id)
                    display_top_recommendations(book_title, top_recommendations)
                else:
                    print("this book is not in our system")

            elif choice == 3:
                print("Thanks for choosing us.\n")
                break
            else:
                print("Please enter a valid number. \n")

        except ValueError:
            print("Enter a numeric data.\n")


recommendation_system()
