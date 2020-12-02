import pymysql
from config import DB_PASSWORD
from FoodTypes import *

# connection = pymysql.connect(
#     host='localhost',
#     user='root',
#     password=DB_PASSWORD,
#     db='food_rescuer',
#     charset='utf8',
#     cursorclass=pymysql.cursors.DictCursor
# )


def add_donator(cursor, args, table_name):
    donator = args[0]
    try:
        columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in donator.keys())
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in donator.values())
        query = "INSERT into %s (%s) VALUES (%s);" % (table_name, columns, values)
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        print("Error while adding new donator", e)


def add_receiver(cursor, args, table_name):
    receiver = args[0]
    try:
        columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in receiver.keys())
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in receiver.values())
        query = "INSERT into %s (%s) VALUES (%s);" % (table_name, columns, values)
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        print("Error while adding new receiver", e)


def add_location(cursor, args, table_name):
    location = args[0]
    try:
        columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in location.keys())
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in location.values())
        query = "INSERT into %s (%s) VALUES (%s);" % (table_name, columns, values)
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        print("Error while adding new location", e)


def add_food(cursor, args, table_name):
    food = args[0]
    try:
        columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in food.keys())
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in food.values())
        query = "INSERT into %s (%s) VALUES (%s);" % (table_name, columns, values)
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        print("Error while adding new food", e)


def get_max_id(table_name):
    try:
        with connection.cursor() as cursor:
            query = f'select max(id) as id from {table_name} '
            cursor.execute(query)
            res = cursor.fetchall()
            return res[0]['id']
    except Exception as err:
        print("500 - Internal error", err)


def add_food_type(cursor, args, table_name):
    food_id = args[0]
    type = args[1]
    type_id = food_type.index(type) + 1
    obj = {'id': '0', 'type_id': type_id, 'food_id': food_id}
    try:
        columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in obj.keys())
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in obj.values())
        query = "INSERT into %s (%s) VALUES (%s);" % (table_name, columns, values)
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        print("Error while adding new food type", e)


def add_receiver_food_type(cursor, args, table_name):
    receiver_id = args[0]
    type = args[1]
    type_id = food_type.index(type) + 1
    obj = {'id': '0', 'type_id': type_id, 'receiver_id': receiver_id}
    try:
        columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in obj.keys())
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in obj.values())
        query = "INSERT into %s (%s) VALUES (%s);" % (table_name, columns, values)
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        print("Error while adding new receiver food type", e)


def main_db(action, *args):
    try:
        with connection.cursor() as cursor:
            if action == 'add_donator':
                add_donator(cursor, args, 'donator')
            elif action == 'add_receiver':
                receiver = args[0]
                food_types = receiver['food_types']
                del receiver['food_types']
                add_receiver(cursor, (receiver,), 'receiver')
                for type_ in food_types:
                    add_receiver_food_type(cursor, (receiver['id'], type_), 'receiver_types')
            elif action == 'add_location':
                add_location(cursor, args, 'location')
            elif action == 'add_food':
                food = args[0]
                food_types = food['food_types']
                del food['food_types']
                add_food(cursor, (food,), 'food')
                food_id = get_max_id('food')
                for type_ in food_types:
                    add_food_type(cursor, (food_id, type_), 'food_types')
            else:
                print("Invalid option")
    except Exception as err:
        print("500 - Internal error", err)


if __name__ == '__main__':
    main_db('add_location', {'id': '0', 'longitude': 34, 'latitude': 35})
    main_db('add_location', {'id': '0', 'longitude': 35, 'latitude': 37})
    main_db('add_location', {'id': '0', 'longitude': 36, 'latitude': 38})
    main_db('add_location', {'id': '0', 'longitude': 37, 'latitude': 39})

    main_db('add_receiver', {'id': 1, 'location_id': 1, 'food_types': ['Halal', 'Other']})
    main_db('add_receiver', {'id': 2, 'location_id': 3, 'food_types': ['Kosher', 'Vegan']})
    main_db('add_receiver', {'id': 3, 'location_id': 2, 'food_types': ['Halal']})

    main_db('add_donator',
            {'id': 1, 'user_name': 'donator1', 'location_id': 4, 'donation_count': 1, 'donation_level': 0.5})

    main_db('add_food', {'id': '0', 'donator_id': 1, 'location_id': 1, 'available': 1,
                         'number_of_servings': 2, 'expiration_date': 3, 'description': 'blabla',
                         'food_types': ['Halal', 'Kosher', 'Other']})
