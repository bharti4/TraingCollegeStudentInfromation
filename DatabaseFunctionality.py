import mysql.connector

DbName = None
connection = None
class RecordNotFoundError(Exception):
    pass
# create database if not exist
def createDatabase(Dbname):
        global DbName
        global connection
        DbName = Dbname
        try:
            connection = mysql.connector.connect(
                host='localhost',
                port='3306',
                user='root'
            )
            mycursor = connection.cursor()

            # Check if the database exists before creating it
            mycursor.execute(f"SHOW DATABASES LIKE '{DbName}'")
            result = mycursor.fetchall()

            if not result:
                mycursor.execute(f"CREATE DATABASE {DbName}")
                #QMessageBox.information(self, "Success :", "Database Created Successfully")
                #print("Success")
        except Exception as error:
            #QMessageBox.information(self, "Error :", str(error))
            print("Failed")

# create  table if not exist

def createTable(tableName, columsStr):
        global DbName
        global connection
        try:
            connection = connectTodatabase()
            if connection:
                mycursor = connection.cursor()
                #query = f"CREATE TABLE  {tableName} , ({columsStr})"
                mycursor.execute(f"CREATE TABLE IF NOT EXISTS  {tableName}  ({columsStr})")
                connection.commit()
        except Exception as error:
            #QMessageBox.information(self, "Error :", str(error))
            print(str(error))
def connectTodatabase():
        global DbName
        global connection
        connection = mysql.connector.connect(
            host='localhost',
            port='3306',
            user='root',
            database=f"{DbName}"
        )
        return connection


def insertData(table_name, columnList , valuesList):
    try:
        connection = connectTodatabase()
        if connection:
            cursor = connection.cursor()

            # Constructing the INSERT query dynamically
            #placeholders = ', '.join(['%s' for _ in valuesList])
            placeholders = creatingPlaceholderString(valuesList)
            query = f"INSERT INTO {table_name} ({', '.join(columnList)}) VALUES ({placeholders})"

            # Executing the INSERT query
            cursor.execute(query, tuple(valuesList))

            connection.commit()
            connection.close()
            print("Data inserted successfully.")


    except Exception as e:
        # Catch the exception and re-raise it
        raise e
#Fetch all data
def fetch(tableName):
    try:
        connection = connectTodatabase()
        if connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {tableName}")
            rows = cursor.fetchall()
            connection.commit()
            connection.close()
            return rows

    except Exception as e:
        # Catch the exception and re-raise it
        raise e

# Fetch column data selectively
def fetchwithConditioaColumn(tableName,conditionColumnList , valuesList):

    try:
        connection = connectTodatabase()
        if connection:
            cursor = connection.cursor()

            # Constructing the Select placeholder dynamically

            placeholders=creatingPlaceholderString(valuesList)

            #placeholders = .join([f"{column} = %s" for column in conditionColumnList])

            placeholdersList = []

            # Loop through each item in the valuesList
            for column in conditionColumnList:
                # Add a placeholder '%s' to the placeholders_list
                placeholdersList.append(f"{column} = %s")

            # Join the placeholders_list with ', ' between elements
            placeholders = ' AND '.join(placeholdersList)


            query = f"SELECT * FROM {tableName} WHERE {placeholders}"

            # Executing the select query
            cursor.execute(query, tuple(valuesList))
            rows = cursor.fetchall()
            connection.commit()
            connection.close()
            return rows
    except Exception as e:
        # Catch the exception and re-raise it
        raise e
#retrive selective column from table
def load_data(tableName,columns_to_retrieve):
    try:
        connection = connectTodatabase()
        if connection:
            cursor = connection.cursor()
            columns_str = ', '.join(columns_to_retrieve)
            query = f"SELECT {columns_str} FROM {tableName}"
            cursor.execute(query)
            data = cursor.fetchall()
            return data
    except Exception as e:
        # Catch the exception and re-raise it
        raise e
def close():
       global connection
       if connection:
           connection.close()
           print("Connection closed.")

#Delete the row from table tableName with specified columName = columnVale
def remove(tableName, columnName,columnValue):
    try:
        connection = connectTodatabase()
        if connection:
            cursor = connection.cursor()
            cursor.execute(f"DELETE FROM {tableName} WHERE {columnName}= %s", (columnValue,))

            connection.commit()
            connection.close()
    except Exception as e:
        # Catch the exception and re-raise it
        raise e

def update(tableName, columnList , valuesList,conditionColumn,conditionValue):
    try:
        connection = connectTodatabase()
        if connection:
            cursor = connection.cursor()
            # Check if the record exists before updating
            cursor.execute(f"SELECT * FROM {tableName} WHERE {conditionColumn} = %s", (conditionValue,))
            if cursor.fetchone() is None:
                raise RecordNotFoundError(f"Record with {conditionColumn} = {conditionValue} not found.")

            # Construct the UPDATE query dynamically
            set_clause = ', '.join([f"{col} = %s" for col in columnList])
            valuesList.append(conditionValue)
            query = f"UPDATE  {tableName} SET {set_clause} WHERE {conditionColumn} = %s"

            # Executing the  query
            cursor.execute(query, tuple(valuesList))

            connection.commit()
            connection.close()
            print("Data Updated successfully.")
    except Exception as e:
        # Catch the exception and re-raise it
        raise e
def close():
       global connection
       if connection:
           connection.close()
           print("Connection closed.")


def creatingPlaceholderString(valuesList):
    # Create an empty list to hold the placeholders
    placeholdersList = []

    # Loop through each item in the valuesList
    for _ in valuesList:
        # Add a placeholder '%s' to the placeholders_list
        placeholdersList.append('%s')

    # Join the placeholders_list with ', ' between elements
    placeholders = ', '.join(placeholdersList)
    return placeholders