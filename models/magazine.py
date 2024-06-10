from database.connection import get_db_connection


class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name 
        self.category = category 

    def __repr__(self):
        return f"<Magazine {self.name}>"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Name must be a type str")
        if not (2 <= len(value) <= 16):
            raise ValueError("Name must be between 2 and 16 characters, inclusive")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str):
            raise ValueError("Category must be a type str")
        if len(value) == 0:
            raise ValueError("Category must be longer than 0 characters")
        self._category = value

    def articles(self):
        from models.article import Article  

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT articles.id, articles.title, articles.content, articles.author_id, articles.magazine_id "
            "FROM articles "
            "WHERE articles.magazine_id = ?",
            (self.id,),
        )
        articles_data = cursor.fetchall()
        conn.close()
        articles = [
            Article(
                row["id"],
                row["title"],
                row["content"],
                row["author_id"],
                row["magazine_id"],
            )
            for row in articles_data
        ]
        return articles

    def contributors(self):
        from models.author import Author  

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT authors.id, authors.name FROM authors "
            "JOIN articles ON authors.id = articles.author_id "
            "WHERE articles.magazine_id = ? "
            "GROUP BY authors.id, authors.name "
            "HAVING COUNT(articles.id) > 2",
            (self.id,),
        )
        authors_data = cursor.fetchall()
        conn.close()
        authors = [Author(row["id"], row["name"]) for row in authors_data]
        return authors

    def article_titles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT articles.title FROM articles " "WHERE articles.magazine_id = ?",
            (self.id,),
        )
        titles = cursor.fetchall()
        conn.close()
        return [title["title"] for title in titles] if titles else None

    def contributing_authors(self):
        from models.author import Author 

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT authors.id, authors.name FROM authors "
            "JOIN articles ON authors.id = articles.author_id "
            "WHERE articles.magazine_id = ? "
            "GROUP BY authors.id, authors.name "
            "HAVING COUNT(articles.id) > 2",
            (self.id,),
        )
        authors_data = cursor.fetchall()
        conn.close()
        return (
            [Author(row["id"], row["name"]) for row in authors_data]
            if authors_data
            else None
        )
