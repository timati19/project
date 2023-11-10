class FaceTable:
    def __init__(self, db):
        import sqlite3
        self.db = db
        self.con = sqlite3.connect(self.db)
        self.cursor = self.con.cursor()

    def get_faces(self):
        self.cursor.execute(f'''
                            SELECT id, face, human face FROM humans
                        ''')
        rows = self.cursor.fetchall()
        return rows

    def set_date(self, id):
        import datetime as dt
        query = self.cursor.execute(f'''
                                    select in_date, out_date from humans where id = {id}
                                ''').fetchall()
        print(query)
        if not query[0][0]:
            self.cursor.execute(f'''
                                update humans set in_date = '{dt.datetime.now().strftime("%H:%M")}' 
                                where id = '{id}'
                                ''').fetchall()
            self.con.commit()
            return

        if not query[0][1]:
            self.cursor.execute(f'''
                                update humans set out_date = '{dt.datetime.now().strftime("%H:%M")}' 
                                where id = '{id}'
                                ''').fetchall()
            self.con.commit()
            return
        self.cursor.execute(f'''
                                        update humans set in_date = '{dt.datetime.now().strftime("%H:%M")}', out_date = ''
                                        where id = '{id}'
                                        ''').fetchall()
        self.con.commit()
