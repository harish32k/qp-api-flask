from flask import jsonify
from decimal import Decimal
import pymysql

#return_json is True by default , if set to false it returns a list of dictionaries for debugging
def query(querystr, return_json=True):

    #create connection object
    connection = pymysql.connect(host='cosc-skillup.cxgok3weok8n.ap-south-1.rds.amazonaws.com',
                                 user='admin',
                                 password='coscskillup',
                                 db='testapi',
                                 cursorclass=pymysql.cursors.DictCursor)
    
    #start connection, create cursor and execute query from cursor
    connection.begin()
    cursor = connection.cursor()
    cursor.execute(querystr)

    #convert any decimal values to strings using encode function defined at the bottom
    result = encode(cursor.fetchall())
    connection.commit() #commit the changes made
    
    #close the cursor and connection
    cursor.close()
    connection.close()
    
    
    if return_json == True:
        return jsonify(result) #convert the query result to JSON
    else:
        return result #returns non JSON format of the query result for debugging


#encode converts decimals to strings
def encode(data):

    #iterate through rows
    for row in data:
        for key, value in row.items():
            if isinstance(value, Decimal):
                row[key] = str(value)
    return data
