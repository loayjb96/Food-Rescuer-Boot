import pymysql
from config import DB_PASSWORD

connection = pymysql.connect(
    host='localhost',
    user='root',
    password=DB_PASSWORD,
    db='sql_in_python',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
)


def add_donator(cursor, donator, table_name):
    try:
        columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in donator.keys())
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in donator.values())
        query = "INSERT into %s (%s) VALUES (%s);" % (table_name, columns, values)
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        print("Error while adding new donator", e)


def main_db(action, *args):
    try:
        with connection.cursor() as cursor:
            if action == 'add_donator':
                add_donator(cursor, args, 'donator')

    except Exception as err:
        print("500 - Internal error", err)
