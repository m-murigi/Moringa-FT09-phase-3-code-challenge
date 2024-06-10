from database.connection import get_db_connection


class Author:
    def __init__(self, id, name):
        self._id = id
        self._name = name

    def __repr__(self):
        return f"<Author {self.name}>"

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise ValueError("id must be an integer")
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("name must be a string")
        if hasattr(self, "_name") and self._name is not None:
            raise AttributeError("name cannot be changed after it is set")
        if len(value) == 0:
            raise ValueError("Name must be longer than 0 characters")
        self._name = value  # Set the instance variable

    def magazines(self):
        from models.magazine import Magazine  # Local import

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT DISTINCT magazines.id, magazines.name, magazines.category FROM magazines "
            "JOIN articles ON magazines.id = articles.magazine_id "
            "WHERE articles.author_id = ?",
            (self.id,),
        )
        magazines_data = cursor.fetchall()
        conn.close()
        magazines = [
            Magazine(row["id"], row["name"], row["category"]) for row in magazines_data
        ]
        return magazines

    def articles(self):
        from models.article import Article  # Local import

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT articles.id, articles.title, articles.content, articles.author_id, articles.magazine_id "
            "FROM articles "
            "WHERE articles.author_id = ?",
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
