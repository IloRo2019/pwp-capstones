class TomeRaterExceptions(Exception):
    pass


class UserAlreadyExists(TomeRaterExceptions):
    pass


class NonUniqueISBN(TomeRaterExceptions):
    pass


class NotValidEmail(TomeRaterExceptions):
    pass



class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print("Email for {} has been updated to {}".format(self.name, self.email))

    def __repr__(self):
        return "User {}, email: {}, books read: {}".format(self.name, self.email, len(self.books))

    def __eq__(self, other_user):
        if self.email == other_user.email and self.name == other_user.name:
            return True
        else:
            return False

    def read_book(self, book, rating=None):
        self.books[book] = rating

    def get_average_rating(self):
        nominator = 0
        denominator = 0
        for i in self.books.values():
            if i != None:
                nominator += i
                denominator += 1
        if denominator !=0:
            return nominator/denominator


class Books(object):

    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.rating = []

    def __eq__(self, other):
        if self.title == other.title and self.isbn == other.isbn:
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.title, self.isbn))

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        print("ISBN for {} has been updated to {}".format(self.title, self.isbn))

    def set_rating (self, rating):
        if 0 <= rating <= 4:
            self.rating.append(rating)
            #print("Thank you for submitting your rating")
        else:
            print("Invalid Rating")

    def get_average_rating(self):
        nominator = 0
        denominator = 0
        for i in self.rating:
            if i != None:
                nominator += i
                denominator += 1
        if denominator != 0:
            return nominator / denominator


class Fiction(Books):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def __repr__(self):
        return ("{title} by {author}".format(title = self.title, author = self.author))

    def get_author(self):
        return self.author


class Non_Fiction(Books):
    def __init__(self, title, subject, level, isbn):
        super().__init__( title, isbn)
        self.subject = subject
        self.level = level

    def __repr__(self):
        return ("{title}, a {level} manual on {subject}".format(title = self.title,
                                                               level = self.level,
                                                               subject = self.subject))

    def get_subject(self):
        return self.subject
    def get_level(self):
        return self.level


class TomeRater():
    def __init__(self):
        self.books = {} #key: book object value: number of users that have read it
        self.users = {} #key: email value:user object
        self.isbn = []

    def create_book(self, title, isbn):
        try:
            if isbn in self.isbn:
                raise NonUniqueISBN

            new_book = Books(title, isbn)
            self.isbn.append(isbn)

            return new_book

        except NonUniqueISBN:
            print("ISBN {} is already taken. Book {} has not been added. Please provide different number".format(isbn, title))

    # def create_user(self, name, email):
    #     new_user = User(name, email)
    #     return new_user

    def create_user(self, name, email):
        try:
            if email in self.users:
                raise UserAlreadyExists
            elif email.count('@') != 1 or email[-4:] not in list(('.com', '.edu', '.org')):
                raise NotValidEmail
            else:
                new_user = User(name, email)
                return new_user
        except UserAlreadyExists:
            print ("Given email {} already exists. Please enter different email".format(email))
        except NotValidEmail:
            print("Given email {} is incorrect. Please enter different email".format(email))

    def create_novel(self, title, author, isbn):

        new_novel = Fiction(title, author, isbn)
        return new_novel

    def create_non_fiction (self, title, subject, level, isbn):
        new_manual = Non_Fiction(title, subject, level, isbn)
        return new_manual

    def add_user (self, name, email, user_books=None):
        self.users[email] = self.create_user(name=name, email=email)
        if user_books==None:
            pass
        else:
            for item in user_books:
                self.add_book_to_user(email=email, book=item, rating=None)

    def add_book_to_user(self,  book, email, rating=None):
        if email in self.users:
            user_found = self.users[email]
            user_found.read_book(book= book, rating=rating)
            if rating != None:
                book.set_rating(rating)
        else:
          print("No user with such email: {email}".format(email=email))

        if book in self.books:
            self.books[book] += 1
        else:
            self.books[book] = 1

    def print_catalog(self):
        for i in self.books:
            print(str(i))

    def print_users(self):
        for i in self.users.values():
            print(str(i))

    def most_positive_user(self):
        best_rating_ever = 0
        for probably_most_positive in self.users.values():
            if best_rating_ever < probably_most_positive.get_average_rating():
                best_rating_ever = probably_most_positive.get_average_rating()
                most_positive_user = probably_most_positive
        return "Most positive is {} with average rating:{}".format(most_positive_user,best_rating_ever)

    def highest_rated_book(self):
        best_book_rating  = 0
        for book_rated in self.books.keys():
            if best_book_rating < book_rated.get_average_rating():
                best_book_rating = book_rated.get_average_rating()
                best_book = book_rated
        return best_book

    def most_read_book(self):
        read_cnt = 0
        for k, v in self.books.items():
            if read_cnt < v:
                read_cnt = v
                most_read_book = k
        return "Most read book {}".format(most_read_book)


