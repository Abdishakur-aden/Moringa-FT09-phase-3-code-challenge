from database.connection import get_db_connection
conn = get_db_connection()
cursor = conn.cursor()

class Author:    
    def __init__(self, id, name):
        self.id = id
        self.name = name        
        cursor.execute('INSERT INTO authors (name) VALUES (?)', (name,))
        self.id = cursor.lastrowid

    def __repr__(self):
        return f'<Author {self.name}>'

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise ValueError("ID must be an integer.")
        self._id = value

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        if hasattr(self, '_name'):
            raise AttributeError("Can't change the name of the author once set")
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Name must be a non-empty string.")
        self._name = name

    def articles(self):
        cursor.execute(
            '''
            SELECT articles.title
            FROM articles
            INNER JOIN authors
            ON articles.author_id = authors.id
            WHERE authors.id = ?
            ''',
            (self.id)
        )
        return cursor.fetchall()


    def magazines(self):
        cursor.execute(
            '''
            SELECT magazines.name
            FROM magazines
            INNER JOIN articles
            ON magazines.id = articles.magazine_id
            WHERE authors.id = ?
            ''',
            (self.id)
        )
        return cursor.fetchall()
