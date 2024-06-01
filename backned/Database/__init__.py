import sqlalchemy
from sqlalchemy import URL


class Database:
    def __init__(self):
        self.url_object = URL.create(
            "mysql+pymysql",
            username="virakran",
            password="edgar2003",
            host="127.0.0.1",
            database="viraran_db",
        )
        self.engine = sqlalchemy.create_engine(
            url=self.url_object,
            echo=True
        )
        self.connection = self.engine.connect()
        self.metadata = sqlalchemy.MetaData()
        self.metadata.reflect(self.engine)


d = Database()