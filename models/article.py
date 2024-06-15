from database.connection import get_db_connection
conn = get_db_connection()
cursor = conn.cursor()

class Article:
    def __init__(self, id, title, author_id, magazine_id):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id
        cursor.execute('INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?, ?)',
                   (title, author_id, magazine_id))

    def __repr__(self):
        return f'<Article {self.title}>'
    
    @property
    def title(self):
        cursor.execute('SELECT title FROM articles WHERE id = ?', (self.id,))
        self._title = cursor.fetchone()
        return self._title

    @title.setter
    def title(self, title):
        if not isinstance(title, str):
            raise ValueError("Title must be a string")
        if not 5 <= len(title) <= 50:
            raise ValueError("Title must be between 5 and 50 characters long")
        if not hasattr(self, '_title'):
            raise AttributeError("Can't change the title of the article once set")
        cursor.execute('UPDATE articles SET title = ? WHERE id = ?', (title, self.id))
        self._title = title

    def author_articles(self):
        cursor.execute(
            '''
            SELECT authors.name
            FROM authors
            INNER JOIN articles
            ON authors.id = articles.author_id
            WHERE articles.author_id = ?
            ''',
            (self.author_id)
        )
        return cursor.fetchone()

    def magazine_articles(self):
        cursor.execute(
            '''
            SELECT magazines.name
            FROM magazines
            INNER JOIN articles
            ON magazines.id = articles.magazine_id
            WHERE articles.magazine_id = ?
            ''',
            (self.magazine_id)
        )
        return cursor.fetchone()
