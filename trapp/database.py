import mysql.connector
import connection as connection


class Database():

    def __init__(self):
        self.cnx = ''
        self.cursor = ''

    def connect(self):
        self.cnx = mysql.connector.connect(user=connection.u, password=connection.p, host=connection.h, database=connection.d)
        self.cursor = self.cnx.cursor(buffered=True)

    def disconnect(self):
        self.cursor.close()
        self.cnx.close()

    def query(self, query, params):
        self.cursor.execute(query, params)
        self.cnx.commit()
        return self.cursor

    def warnings(self):
        return self.cursor.fetchwarnings()
