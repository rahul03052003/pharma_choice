import mysql.connector

class Database:
    def dbconnection(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="pharma_choice_db"
        )