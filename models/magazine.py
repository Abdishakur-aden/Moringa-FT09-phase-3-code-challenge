from database.connection import get_db_connection
conn = get_db_connection()
cursor = conn.cursor()

class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category
        cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (name, category))
        self.id = cursor.lastrowid

    def __repr__(self):
        return f'<Magazine {self.name}>'
    
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise ValueError("ID must be an integer")
        self._id = value

    @property
    def name(self):
        cursor.execute('SELECT name FROM magazines WHERE id = ?', (self._id,))
        self._name = cursor.fetchone()[0]
        return self._name
    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise ValueError("Name must be a string between 2 and 16 characters")
        if not (2 <= len(name) <= 16):
            raise ValueError("Name must be between 2 and 16 characters")
        cursor.execute('UPDATE magazines SET name = ? WHERE id = ?', (name, self._id))
        self._name = name

    @property
    def category(self):
        cursor.execute('SELECT category FROM magazines WHERE id = ?', (self._id,))
        self._category = cursor.fetchone()[0]
        return self._category
    @category.setter
    def category(self, category):
        if not isinstance(category, str):
            raise ValueError("Category must be a string")
        if not len(category) > 0:
            raise ValueError("Category must be longer than 0 characters")
        cursor.execute('UPDATE magazines SET category = ? WHERE id = ?', (category, self._id))
        self._category = category

    def articles(self):
        cursor.execute(
            '''
            SELECT articles.title
            FROM articles
            INNER JOIN magazines
            ON articles.magazine_id = magazines.id
            WHERE magazines.id = ?
            ''',
            (self._id)
        )
        return cursor.fetchall()
    
    def contributors(self):
        cursor.execute(
            '''
            SELECT authors.name
            FROM authors
            INNER JOIN articles
            ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            ''',
            (self._id)
        )
        return cursor.fetchall()