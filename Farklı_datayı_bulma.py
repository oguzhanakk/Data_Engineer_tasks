import pypyodbc

db = pypyodbc.connect(
        'Driver={SQL Server};' #constant
        'Server=DESKTOP-QBD9D63;' #variable
        'Database=SqlEgitimDb;' #variable
        'Trusted_Connection=True;' #constant
    )
cursor=db.cursor()

cursor.execute('SELECT * FROM tumykvbirlesim')
list = cursor.fetchall()

for i in range(0,100):
    print(list[0][i])

db.close()