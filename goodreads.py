from typing import List
import csv


class Review:
    all_reviews = dict()

    def __init__(self, review_id: str, book_id: str, user_id: str, rating: int, date: str, number_of_like: int) -> None:
        self.id = review_id
        self.book_id = book_id
        self.user_id = user_id
        self.rating = rating
        self.date = date
        self.number_of_likes = number_of_like
        if book_id in self.all_reviews:
            self.all_reviews[book_id].append(self)
        else:
            self.all_reviews[book_id] = [self]


class Book:
    def __init__(self, book_id: str, book_title: str, author_id: str, genre: str) -> None:
        self.id = book_id
        self.title = book_title
        self.author_id = author_id
        self.genre = genre
        self.number_of_likes = 0
        self.number_of_review = 0
        self.rating = 0


class SheffManager:
    def __init__(self) -> None:
        self._libraries = dict()

    def add_library(self, name: str, books: list) -> None:
        self._libraries[name] = books

    def get_library(self, library_name: str) -> list:
        return self._libraries[library_name]

    def fet_library_size(self, library_name: str) -> int:
        return len(self._libraries[library_name])


class User:
    def __init__(self, user_id: str, username: str, place_of_birth: str, member_since: str, favorite_authors: str,
                 favorite_genres: str, want_to_read: list, currently_reading: list, read: list) -> None:
        self.sheff_manager = SheffManager()
        self.user_id = user_id
        self.name = username
        self.place_of_birth = place_of_birth
        self.member_since = member_since
        self.favorite_authors = favorite_authors
        self.favorite_genres = favorite_genres
        self.sheff_manager.add_library("want_to_read", want_to_read)
        self.sheff_manager.add_library("currently_reading", currently_reading)
        self.sheff_manager.add_library("read", read)
        self.credit = 0
        self.total_likes = 0
        self.total_review = 0

    def get_size_of_library(self, library_name: str) -> int:
        return self.sheff_manager.fet_library_size(library_name)

    def get_library(self, library_name: str) -> list:
        return self.sheff_manager.get_library(library_name)


class Author:
    def __init__(self, author_id: str, author_name: str, gender: str, member_since: str, year_of_birth: str,
                 place_of_birth: str, genres: str) -> None:
        self.id = author_id
        self.name = author_name
        self.gender = gender
        self.member_since = member_since
        self.year_of_birth = year_of_birth
        self.place_of_birth = place_of_birth
        self.genres = genres
        self.books = list()


class UserManager:
    def __init__(self) -> None:
        self._all_users = dict()

    def add_user(self, user: User) -> None:
        self._all_users[user.user_id] = user

    def get_spec_library(self, user_id: str, library_name: str) -> list:
        return self._all_users[user_id].get_library(library_name)

    @staticmethod
    def calculate_credit(number_of_likes: int, number_of_reviews: int, number_of_user_reviews_likes: int,
                         number_of_user_reviews: int) -> float:
        credit = 1 / 2 * (
                    (number_of_user_reviews_likes / number_of_likes) + (number_of_user_reviews / number_of_reviews))
        return round(credit, 6)

    def credit(self, user_id: str, number_of_likes: int, number_of_reviews: int) -> float:
        credit = UserManager.calculate_credit(number_of_likes, number_of_reviews, self._all_users[user_id].total_likes,
                                              self._all_users[user_id].total_review)
        self._all_users[user_id].credit = credit
        return credit

    def update_review(self, username: str, numbers_of_likes: int):
        self._all_users[username].total_likes += numbers_of_likes
        self._all_users[username].total_review += 1

    def user_info(self, username: str) -> tuple:
        name = self._all_users[username].name
        place_of_birth = self._all_users[username].place_of_birth
        member_since = self._all_users[username].member_since
        favorite_genres = self._all_users[username].favorite_genres
        favorite_authors = self._all_users[username].favorite_authors
        number_of_books_in_read_shelf = self._all_users[username].get_size_of_library("read")
        number_of_books_in_want_to_read_shelf = self._all_users[username].get_size_of_library("want_to_read")
        number_of_books_in_currently_reading_shelf = self._all_users[username].get_size_of_library("currently_reading")
        return (name, place_of_birth, member_since, favorite_genres, favorite_authors, number_of_books_in_read_shelf,
                number_of_books_in_want_to_read_shelf, number_of_books_in_currently_reading_shelf)

    def _find_best_viewer(self):
        max_number_of_likes = 0
        for user_id in self._all_users:
            if self._all_users[user_id].total_likes > max_number_of_likes:
                max_number_of_likes = self._all_users[user_id].total_likes
                best_viewer = user_id
        return best_viewer, max_number_of_likes

    def best_reviewer_info(self) -> tuple:
        max_number_of_likes = 0
        best_viewer = None
        best_viewer, max_number_of_likes = self._find_best_viewer()
        name, place_of_birth, member_since, favorite_genres, favorite_authors, read_books_number, \
        want_to_read_book_number, currently_reading_book_number = self.user_info(best_viewer)
        return (best_viewer, name, place_of_birth, member_since, favorite_genres, favorite_authors,
                read_books_number, want_to_read_book_number, currently_reading_book_number, max_number_of_likes)


class AuthorsManager:
    all_authors = dict()

    def __init__(self) -> None:
        pass

    def author_info(self, authors_id: str) -> Author:
        return self.all_authors[authors_id]


class BooksManager:
    all_books = dict()

    def __init__(self) -> None:
        pass

    def book_info(self, book_id: str) -> Book:
        return self.all_books[book_id]


    @staticmethod
    def the_best_book() -> tuple:
        max_avg = 0
        best_book_id = None
        for book_id in Review.all_reviews:
            sum_of_rating = BooksManager.all_books[book_id].rating
            book_avrage_rating = Tools.caculate_avrage(sum_of_rating, len(Review.all_reviews[book_id]))
            if max_avg < book_avrage_rating:
                best_book_id = book_id
                max_avg = book_avrage_rating
        return best_book_id, max_avg




class Tools:
    def __init(self) -> None:
        pass

    @staticmethod
    def sort_books_with_key(books: list, genre: str):
        s = sorted(books, key=lambda x: (BooksManager.all_books[x].genre == genre, BooksManager.all_books[x].title))
        s = sorted(s, key=lambda x: (BooksManager.all_books[x].genre == genre), reverse=True)
        return s

    @staticmethod
    def caculate_avrage(sum_of_item: int, number_of_item: int) -> float:
        return sum_of_item / number_of_item


class GoodReads:
    def __init__(self) -> None:
        self.author_manager = AuthorsManager()
        self.user_manager = UserManager()
        self.book_manager = BooksManager()
        self.number_of_likes = 0
        self.number_of_review = 0
        self.rating = 0

    def add_user(self, user: User) -> None:
        self.user_manager.add_user(user)

    def author_info(self, authors_id: str) -> Author:
        return self.author_manager.author_info(authors_id)

    def book_info(self, book_id: str) -> Book:
        return self.book_manager.book_info(book_id)

    def user_sorted_shelf_with_genre(self, user_id: str, shelf_type: str, genre: str) -> list:
        books = self.user_manager.get_spec_library(user_id, shelf_type)
        sorted_books = Tools.sort_books_with_key(books, genre)
        return sorted_books

    def calculate_user_credit(self, user_id: str) -> float:
        return self.user_manager.credit(user_id, self.number_of_likes, self.number_of_review)

    def best_book(self) -> tuple:
        return self.book_manager.the_best_book()

    def review_update(self, username: str, book_id: str, number_of_likes: int, rating: int) -> None:
        self.number_of_likes += number_of_likes
        self.number_of_review += 1
        self.book_manager.all_books[book_id].number_of_review += 1
        self.book_manager.all_books[book_id].number_of_likes += number_of_likes
        self.book_manager.all_books[book_id].rating += rating
        self.user_manager.update_review(username, number_of_likes)

    def best_reviewer(self) -> tuple:
        return self.user_manager.best_reviewer_info()


class UserInterface:
    def __init__(self) -> None:
        self._good_reads = GoodReads()
        self._dispatch = {
            "show_author_info": self._show_author_info,
            "show_sorted_shelf": self._show_sorted_shelf,
            "credit": self._credit,
            "best_book": self._best_book,
            "best_reviewer": self._best_reviewer,
        }

    def _get_command(self) -> None:
        while True:
            order = input().split()
            self._dispatch[order[0]](order[1:])

    def _print_book(self, book_id: str) -> None:
        book_data = self._good_reads.book_info(book_id)
        print("id:", book_data.id, "Title:", book_data.title)

    def _print_author_data(self, author: Author) -> None:
        print("id:", author.id)
        print("Name:", author.name)
        print("Year of Birth:", author.year_of_birth)
        print("Place of Birth:", author.place_of_birth)
        print("Member Since:", author.member_since)
        print("Genres:", author.genres)
        print("Books:")
        for book in author.books:
            self._print_book(book)

    def _show_author_info(self, data: list) -> None:
        author_id = data[0]
        author_data = self._good_reads.author_info(author_id)
        self._print_author_data(author_data)

    def _show_sorted_shelf(self, data: list) -> None:
        user_id = data[0]
        shelf_type = data[1]
        genre = data[2]
        sorted_books = self._good_reads.user_sorted_shelf_with_genre(user_id, shelf_type, genre)
        for book_id in sorted_books:
            print("id:", BooksManager.all_books[book_id].id)
            print("Title:", BooksManager.all_books[book_id].title)
            print("Genre:", BooksManager.all_books[book_id].genre)
            author_id = BooksManager.all_books[book_id].author_id
            print("Author:", AuthorsManager.all_authors[author_id].name)
            print("***")

    def _credit(self, data: list) -> None:
        user_id = data[0]
        credit = self._good_reads.calculate_user_credit(user_id)
        print(credit)

    @staticmethod
    def _print_best_book_info(book_id: str, avg_rate):
        print("id:", BooksManager.all_books[book_id].id)
        print("Title:", BooksManager.all_books[book_id].title)
        print("Genre:", BooksManager.all_books[book_id].genre)
        author_id = BooksManager.all_books[book_id].author_id
        print("Author:", AuthorsManager.all_authors[author_id].name)
        print("Avrege Rating:", round(avg_rate, 2))

    def _best_book(self, data: list) -> None:
        best_book_id, avg_rate = self._good_reads.best_book()
        self._print_best_book_info(best_book_id, avg_rate)

    @staticmethod
    def _print_author_names_best_reviewer(authors: list) -> None:
        res = "Favorite Authors: "
        for author in authors:
            res += AuthorsManager.all_authors[author].name + ", "
        print(res[:-1])

    def _best_reviewer(self, data: list) -> None:
        book_id, name, place_of_birth, member_since, favorite_genres, favorite_authores, \
            read_books, want_to_read_books, currently_reading_books, number_of_likes = self._good_reads.best_reviewer()
        print("id:", book_id)
        print("Name:", name)
        print("Place of Birth:", place_of_birth)
        print("Member Since:", member_since)
        print("Favorite Genres:", favorite_genres.replace("$", ", "))
        self._print_author_names_best_reviewer(favorite_authores.split("$"))
        print("Number of Books in Read Shelf:", read_books)
        print("Number of Books in Want to Read Shelf:", want_to_read_books)
        print("Number of Books in Currently Reading Shels:", currently_reading_books)
        print("Number of Likes:", number_of_likes)

    @staticmethod
    def _read_author_data(filename: str) -> None:
        with open(filename) as author_file:
            csv_reader = csv.reader(author_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                i = 0
                if line_count != 0:
                    author_id = row[0]
                    name = row[1]
                    gender = row[2]
                    member_since = row[3]
                    year_of_birth = row[4]
                    place_of_birth = row[5]
                    genres = row[6]
                    AuthorsManager.all_authors[author_id] = Author(author_id, name, gender, member_since,
                                                                   year_of_birth, place_of_birth, genres)
                line_count += 1

    @staticmethod
    def _read_book_data(filename: str) -> None:
        with open(filename) as book_file:
            csv_reader = csv.reader(book_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                i = 0
                if line_count != 0:
                    book_id = row[0]
                    title = row[1]
                    author_id = row[2]
                    genre = row[3]
                    AuthorsManager.all_authors[author_id].books.append(book_id)
                    BooksManager.all_books[book_id] = Book(book_id, title, author_id, genre)
                line_count += 1

    def _read_user_data(self, filename: str) -> None:
        with open(filename) as user_file:
            csv_reader = csv.reader(user_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                i = 0
                if line_count != 0:
                    user_id = row[0]
                    name = row[1]
                    place_of_birth = row[2]
                    member_since = row[3]
                    favorite_authors = row[4]
                    favorite_genre = row[5]
                    want_to_read = row[6].split("$")
                    currently_reading = row[7].split("$")
                    read = row[8].split("$")
                    self._good_reads.add_user(User(user_id, name, place_of_birth, member_since, favorite_authors,
                                                   favorite_genre, want_to_read, currently_reading, read))
                line_count += 1

    def _read_review_data(self, filename: str) -> None:
        with open(filename) as review_file:
            csv_reader = csv.reader(review_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                i = 0
                if line_count != 0:
                    review_id = row[0]
                    book_id = row[1]
                    user_id = row[2]
                    rating = row[3]
                    date = row[4]
                    number_of_likes = row[5]
                    Review(review_id, book_id, user_id, int(rating), date, int(number_of_likes))
                    self._good_reads.review_update(user_id, book_id, int(number_of_likes), int(rating))
                line_count += 1

    def run(self) -> None:
        self._read_author_data("authors.csv")
        self._read_book_data("books.csv")
        self._read_user_data("users.csv")
        self._read_review_data("reviews.csv")
        self._get_command()


user_interface = UserInterface()
user_interface.run()
