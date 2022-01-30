import sqlite3

path_to_db = 'db//fucking_bot_db'
path_to_db33 = 'fucking_bot_db'

## formating

# Форматирование запроса с аргументами
def update_format_with_args(sql, parameters: dict):
    values = ", ".join([
        f"{item} = ?" for item in parameters
    ])
    sql = sql.replace("XXX", values)
    return sql, tuple(parameters.values())


# Форматирование запроса без аргументов
def get_format_args(sql, parameters: dict):
    sql += " AND ".join([
        f"{item} = ?" for item in parameters
    ])
    return sql, tuple(parameters.values())

######################################### БЛЯТЬ #############

# Добавление пользователя
def add_userx(user_id, user_login, user_name):
    with sqlite3.connect(path_to_db) as db:
        db.execute("INSERT INTO storage_users "
                   "(user_id, user_login, user_name) "
                   "VALUES (?, ?, ?)",
                   [user_id, user_login, user_name])
        db.commit()

#добавка прилы в бд
def add_apk(apk_packagename, apkname, status, metka, cookies, passw, fbappid, tg_id):
    with sqlite3.connect(path_to_db) as db:
        db.execute("INSERT INTO storage_apk"
                   "(package, disname, status, metka, cookies, pass, fbappid, tg_id_webmaster)"
                   "VALUES (?, ?, ?, ?, ?, ?,?,?)",
                   [apk_packagename, apkname, status, metka, cookies, passw, fbappid, tg_id])
        db.commit()
        print('commited')

"(id_pidorskiy TEXT, suka_packagename TEXT, suka_apkname TEXT, ebanyi_suka_rot_statusa TEXT, chto_za_ebanya_metka_a TEXT)  AND ebanyi_suka_rot_statusa=ACTIVE"

def get_all_apks_for_admin():
    sql = "SELECT * FROM storage_apk"
    with sqlite3.connect(path_to_db) as db:
        return db.execute(sql).fetchall()

def test_bd_test():
    with sqlite3.connect(path_to_db) as db:
        cur = db.cursor()
        cur.execute(f'DROP TABLE storage_apk')
        db.commit()

def check_if_apk_already_there(package):
    with sqlite3.connect(path_to_db) as db:
        cur = db.cursor()
        cur.execute(f'SELECT * FROM storage_apk WHERE package="{package}"')
        data = cur.fetchall()
        return len(data)

def get_active_apks_of_users(user_id):
    with sqlite3.connect(path_to_db) as db:
        all_apks = get_all_apks_for_admin()
        data = []
        for i in all_apks:
            if str(user_id) in str(i[-1]):
                data.append(i)
        print(data)
        return data

def get_special_package(package):
    with sqlite3.connect(path_to_db) as db:
        cur = db.cursor()
        cur.execute(f'SELECT * FROM storage_apk WHERE package="{package}"')
        data = cur.fetchall()
        print(data)
        return data[0]

def update_data_bd(package, userid):
    with sqlite3.connect(path_to_db) as db:
        cur = db.cursor()
        cur.execute(f'SELECT * FROM storage_apk WHERE package="{package}"')
        data = cur.fetchall()
        if len(data) != 1:
            print('there can not be more or less rows in the bd')
            return 0
        print(data)
        users_before = data[0][-1]
        print(users_before)
        users_after = str(users_before) +','+ str(userid.replace('\n', ','))
        print(users_after)
        cur.execute(f'UPDATE storage_apk SET tg_id_webmaster="{users_after}"')
        return 1


######################################### СОЗДАНИЕ БД #########################################
# Создание всех таблиц для БД
def create_bdx():
    with sqlite3.connect(path_to_db) as db:

        # Создание БД с хранением данных about users apks
        try:
            db.execute("CREATE TABLE storage_apk("
                       "package TEXT, disname TEXT, status TEXT, metka TEXT, cookies TEXT, pass TEXT, fbappid TEXT, tg_id_webmaster TEXT)")
            db.commit()
            print("DB was not found | Creating...")
        except Exception as e:
            print(e)


'package, disname, status, metka, cookies, pass, fbappid, tg_id_webmaster'


'''create_bdx()
print(get_active_apks_of_users('953941448'))

for i in get_all_apks_for_admin():
    print(i)

'package, apkname, status, metka, idwebov'
update_data_bd(0, 0)

#add_apk(953941448, 'boookofrathisisfine.androidappi', 'фывафыва', 'ACTIVE', 'metka123')
#add_apk('boookofrathisisfine.androidappi', 'фывафыва', 'ACTIVE', 'metka123', 'cookies', 'pass', '0123', 44)'''
'''
print(check_if_apk_already_there('com.dztall.ccr.android.admob'))
print(get_all_apks_for_admin())
get_active_apks_of_users(str(953941448))
drop_tables()
#'''