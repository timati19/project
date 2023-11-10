import datetime
import sqlite3
import PIL


class FaceTable:
    def __init__(self, db):
        self.db = db

    def get_faces(self):
        con = sqlite3.connect(self.db)
        cursor = con.cursor()
        cursor.execute(f'''
                            SELECT human, face FROM humans
                        ''')
        rows = cursor.fetchall()
        return rows

    def set_dates(self, ):


face = FaceTable('faces.db')
print(face.get_faces())
