import sqlite3

class db_manager:
    def __init__(self, database):
        self.database = database

    def create_tables(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
                    
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ogrenciler(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ogrenci_id INTEGER NOT NULL,
                ogrenci_name TEXT NOT NULL
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS testler(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_id INTEGER NOT NULL,
                sinif TEXT NOT NULL,
                ders TEXT NOT NULL,
                tarih TEXT NOT NULL,
                kitap TEXT NOT NULL,
                sayfalar TEXT NOT NULL,
                cevaplar TEXT
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ogrenci_cevaplari(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_id INTEGER NOT NULL,
                ogrenci_name TEXT NOT NULL,
                cevaplar TEXT NOT NULL,
                puan INTEGER
            );
            """
        )
        
        conn.commit()
        conn.close()  
        
    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)
            conn.commit()

    def __select_data(self, sql, data=tuple()):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()

    def ogrenci_ekle(self, ogrenci_id, ogrenci_name):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO ogrenciler (ogrenci_id, ogrenci_name) VALUES (?, ?)",
                (ogrenci_id, ogrenci_name)
            )
            conn.commit()

    def get_homeworks(self, sinif):
        conn = sqlite3.connect(self.database)
        cur = conn.cursor()
        cur.execute(
            "SELECT test_id, ders, tarih, kitap, sayfalar, cevaplar FROM testler WHERE sinif = ? ORDER BY id DESC",
            (sinif,)
        )
        data = cur.fetchall()
        conn.close()
        return data        

    def odev_yukle(self, testid, deger1, deger2, deger3, deger4, deger5, deger6):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO testler(test_id, sinif, ders, tarih, kitap, sayfalar, cevaplar)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (testid, deger1, deger2, deger3, deger4, deger5, deger6)
            )
            conn.commit()

    def get_test_by_id(self, test_id):
        conn = sqlite3.connect(self.database)
        cur = conn.cursor()
        cur.execute("SELECT * FROM testler WHERE test_id = ?", (test_id,))
        test = cur.fetchone()
        conn.close()
        return test

    def ogrenci_cevabi_ekle(self, test_id, ogrenci_adi, cevaplar, puan):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO ogrenci_cevaplari(test_id, ogrenci_name, cevaplar, puan)
                VALUES (?, ?, ?, ?)
            """, (test_id, ogrenci_adi, cevaplar, puan))
            conn.commit()


    def get_ogrenci_cevaplari(self, test_id):
        conn = sqlite3.connect(self.database)
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM ogrenci_cevaplari WHERE test_id=?",
            (test_id,)
        )
        data = cur.fetchall()
        conn.close()
        return data        

if __name__ == '__main__':
    manager = db_manager("odevler.db")
    manager.create_tables()