from database.setup import create_tables
from database.connection import get_db_connection
from models.article import Article
from models.author import Author
from models.magazine import Magazine


def create_author(cursor, name):
    cursor.execute("INSERT INTO authors (name) VALUES (?)", (name,))
    return cursor.lastrowid


def create_magazine(cursor, name, category):
    cursor.execute(
        "INSERT INTO magazines (name, category) VALUES (?, ?)", (name, category)
    )
    return cursor.lastrowid


def create_article(cursor, title, content, author_id, magazine_id):
    cursor.execute(
        "INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
        (title, content, author_id, magazine_id),
    )
    return cursor.lastrowid


def get_author_of_article(cursor, article_id):
    cursor.execute(
        "SELECT authors.id, authors.name FROM authors "
        "JOIN articles ON authors.id = articles.author_id "
        "WHERE articles.id = ?",
        (article_id,),
    )
    author_data = cursor.fetchone()
    return Author(author_data["id"], author_data["name"]) if author_data else None


def get_magazine_of_article(cursor, article_id):
    cursor.execute(
        "SELECT magazines.id, magazines.name, magazines.category FROM magazines "
        "JOIN articles ON magazines.id = articles.magazine_id "
        "WHERE articles.id = ?",
        (article_id,),
    )
    magazine_data = cursor.fetchone()
    return (
        Magazine(magazine_data["id"], magazine_data["name"], magazine_data["category"])
        if magazine_data
        else None
    )


def get_articles_of_author(cursor, author_id):
    cursor.execute("SELECT * FROM articles WHERE author_id = ?", (author_id,))
    articles_data = cursor.fetchall()
    return [
        Article(
            row["id"],
            row["title"],
            row["content"],
            row["author_id"],
            row["magazine_id"],
        )
        for row in articles_data
    ]


def get_articles_of_magazine(cursor, magazine_id):
    cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (magazine_id,))
    articles_data = cursor.fetchall()
    return [
        Article(
            row["id"],
            row["title"],
            row["content"],
            row["author_id"],
            row["magazine_id"],
        )
        for row in articles_data
    ]


def get_authors_of_magazine(cursor, magazine_id):
    cursor.execute(
        "SELECT DISTINCT authors.id, authors.name FROM authors "
        "JOIN articles ON authors.id = articles.author_id "
        "WHERE articles.magazine_id = ?",
        (magazine_id,),
    )
    authors_data = cursor.fetchall()
    return [Author(row["id"], row["name"]) for row in authors_data]


def get_article_titles_of_magazine(cursor, magazine_id):
    cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (magazine_id,))
    titles = cursor.fetchall()
    return [title["title"] for title in titles] if titles else None


def get_magazines_of_author(cursor, author_id):
    cursor.execute(
        "SELECT DISTINCT magazines.id, magazines.name, magazines.category FROM magazines "
        "JOIN articles ON magazines.id = articles.magazine_id "
        "WHERE articles.author_id = ?",
        (author_id,),
    )
    magazines_data = cursor.fetchall()
    return [Magazine(row["id"], row["name"], row["category"]) for row in magazines_data]


def get_contributing_authors(cursor, magazine_id):
    cursor.execute(
        "SELECT authors.id, authors.name FROM authors "
        "JOIN articles ON authors.id = articles.author_id "
        "WHERE articles.magazine_id = ? "
        "GROUP BY authors.id, authors.name "
        "HAVING COUNT(articles.id) > 2",
        (magazine_id,),
    )
    authors_data = cursor.fetchall()
    return (
        [Author(row["id"], row["name"]) for row in authors_data]
        if authors_data
        else None
    )


def main():
    # Initialize the database and create tables
    create_tables()

    # Collect user input
    author_name = input("Enter author's name: ")
    magazine_name = input("Enter magazine name: ")
    magazine_category = input("Enter magazine category: ")
    article_title = input("Enter article title: ")
    article_content = input("Enter article content: ")

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create an author
    cursor.execute("INSERT INTO authors (name) VALUES (?)", (author_name,))
    author_id = cursor.lastrowid  # Use this to fetch the id of the newly created author

    # Create a magazine
    cursor.execute(
        "INSERT INTO magazines (name, category) VALUES (?,?)",
        (magazine_name, magazine_category),
    )
    magazine_id = (
        cursor.lastrowid
    )  # Use this to fetch the id of the newly created magazine

    # Create an article
    cursor.execute(
        "INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
        (article_title, article_content, author_id, magazine_id),
    )

    conn.commit()

    # Query the database for inserted records.
    cursor.execute("SELECT * FROM magazines")
    magazines = cursor.fetchall()

    cursor.execute("SELECT * FROM authors")
    authors = cursor.fetchall()

    cursor.execute("SELECT * FROM articles")
    articles = cursor.fetchall()

    # Display results
    print("\nMagazines:")
    for magazine in magazines:
        print(Magazine(magazine["id"], magazine["name"], magazine["category"]))

    print("\nAuthors:")
    for author in authors:
        print(Author(author["id"], author["name"]))

    print("\nArticles:")
    for article in articles:
        print(
            Article(
                article["id"],
                article["title"],
                article["content"],
                article["author_id"],
                article["magazine_id"],
            )
        )

    # CLI loop
    while True:
        print("\nOptions:")
        print("1. Get Author of Article")
        print("2. Get Magazine of Article")
        print("3. Get Articles of Author")
        print("4. Get Articles of Magazine")
        print("5. Get Authors of Magazine")
        print("6. Get Article Titles of Magazine")
        print("7. Get Magazines of Author")
        print("8. Get Contributing Authors")
        print("9. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            article_id = int(input("Enter article ID: "))
            author = get_author_of_article(cursor, article_id)
            print(author)
        elif choice == "2":
            article_id = int(input("Enter article ID: "))
            magazine = get_magazine_of_article(cursor, article_id)
            print(magazine)
        elif choice == "3":
            author_id = int(input("Enter author ID: "))
            articles = get_articles_of_author(cursor, author_id)
            for article in articles:
                print(article)
        elif choice == "4":
            magazine_id = int(input("Enter magazine ID: "))
            articles = get_articles_of_magazine(cursor, magazine_id)
            for article in articles:
                print(article)
        elif choice == "5":
            magazine_id = int(input("Enter magazine ID: "))
            authors = get_authors_of_magazine(cursor, magazine_id)
            for author in authors:
                print(author)
        elif choice == "6":
            magazine_id = int(input("Enter magazine ID: "))
            titles = get_article_titles_of_magazine(cursor, magazine_id)
            for title in titles:
                print(title)
        elif choice == "7":
            author_id = int(input("Enter author ID: "))
            magazines = get_magazines_of_author(cursor, author_id)
            for magazine in magazines:
                print(magazine)
        elif choice == "8":
            magazine_id = int(input("Enter magazine ID: "))
            authors = get_contributing_authors(cursor, magazine_id)
            if authors:
                for author in authors:
                    print(author)
            else:
                print("No authors have more than 2 articles in this magazine.")
        elif choice == "9":
            break
        else:
            print("Invalid choice, please select again.")

        conn.commit()

    conn.close()


if __name__ == "__main__":
    main()
