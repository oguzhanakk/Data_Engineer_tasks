import pypyodbc

db = pypyodbc.connect(
        'Driver={SQL Server};' #constant
        'Server=DESKTOP-QBD9D63;' #variable
        'Database=SqlEgitimDb;' #variable
        'Trusted_Connection=True;' #constant
    )
cursor=db.cursor()

def adding_data(table_name,name,surname,age,job):
    cursor.execute("insert into {} values('{}','{}',{},'{}')".format(table_name,name,surname,age,job))
    cursor.commit()

def pulling_data(table_name):
    cursor.execute('SELECT * FROM {}'.format(table_name))
    list = cursor.fetchall()
    for i in list:
        print(i)

    db.close()

def update_data(table_name,column,old_data,new_data):
    cursor.execute("Update {} set {} = '{}' where {} = '{}'".format(table_name,column,new_data,column,old_data))
    cursor.commit()

def delete_data(table_name,column,data):
    cursor.execute("Delete from {} where {} = '{}'".format(table_name,column,data))
    cursor.commit()

pulling_data("Tablo")

"""
cursor.execute("SELECT * FROM Sayfa Where İsim = 'Oguzhan' and Yaş = 22")
list = cursor.fetchall()
print(list)
"""