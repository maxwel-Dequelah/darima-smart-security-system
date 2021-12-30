import mysql.connector



config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'security'
}

database = mysql.connector.connect(**config)
print(database)

mycursor = database.cursor()

mycursor.execute("CREATE DATABASE security")
print('db created')


