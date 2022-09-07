import sqlite3 as sq

class Data_user:
    def __init__(self, ID=None, name=None):
        self.ID = ID
        self.name = name
        self.connect_data_user()
        self.creat_data_base()

    def creat_data_base(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
        user_name TEXT,
        ID INTEGER,
        SUM_MONEY FLOAT,
        SUM_Purchases INTEGER)
        """)

    def connect_data_user(self):
        self.con = sq.connect('Data_base.db')
        self.cur = self.con.cursor()

    def edit_summa_amount(self,total_money,summ):
        user = self.cur.execute("""SELECT SUM_Purchases,SUM_MONEY FROM users WHERE ID=?""",(self.ID,)).fetchone()
        money = user[1]-total_money
        summ = user[0]+summ
        if money <0:
            return 'Не хватает денег.'
        else:
            self.cur.execute(f"""UPDATE users SET SUM_MONEY = ? WHERE ID = {self.ID} """,(money,))
            self.cur.execute(f"""UPDATE users SET SUM_Purchases = ? WHERE ID ={self.ID} """,(summ,))
            self.con.commit()
            return True



    def get_info_user_table(self):
        data = self.cur.execute("""SELECT * FROM users WHERE ID =?""", (self.ID,))
        data = data.fetchone()
        if data is None:
            self.reg_new_user()
            return self.get_info_user_table()
        return data

    def reg_new_user(self):
        num = self.cur.execute("""SELECT ID FROM users WHERE ID =?""", (self.ID,))
        check_fetcnone = num.fetchone()
        if check_fetcnone == None:
            result = self.cur.execute("""INSERT INTO users VALUES(?,?,?,?)""", (self.name, self.ID, 0.0, 0,))
            self.con.commit()
            return result
        else:
            print(f'пользователь с ID {self.ID} уже существует')

    def add_money_user(self, money):
        old_money = self.cur.execute("""SELECT SUM_MONEY FROM users WHERE ID =?""", (self.ID,))
        old_money = old_money.fetchone()
        new_money = money + float(*old_money)
        self.cur.execute("""UPDATE users SET SUM_MONEY = ?""", (new_money,))
        self.con.commit()


class Magazine:
    def __init__(self, data=None,type_name=None,name=None):
        self.data = data
        self.name = name
        self.type_name = type_name
        self.connect_to_magazine()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS magazine(
        type_name TEXT,
        name TEXT,
        image TEXT,
        SUMMA INTEGER)
        """)
        self.con.commit()

    def get_info_from_magazine(self):
        many_subjects = self.cur.execute("""SELECT * FROM magazine WHERE type_name=?""", (self.type_name,))

        return many_subjects
    def get_info_name_subject(self):
        sub = self.cur.execute("""SELECT * FROM magazine WHERE name =?""",(self.data[1],)).fetchone()
        if sub is not None and str(sub).lower() != str(self.data[1]).lower():
            return False
        else:
            return True
    def add_subject_in_magazine(self):
        check = self.get_info_name_subject()
        if check:
            try:
                self.cur.execute("""INSERT INTO magazine VALUES(?,?,?,?)""",(tuple(self.data)))
                return True
            except:
                return 'Ошибка записи новых данных'
            finally:
                self.con.commit()
        else:
            return 'Продукт уже такой создан'
    def buy(self):
        sub = self.cur.execute("""SELECT SUMMA FROM magazine WHERE name =?""", (*self.name,)).fetchone()
        return sub

    def connect_to_magazine(self):
        self.con = sq.connect("Data_base.db")
        self.cur = self.con.cursor()
