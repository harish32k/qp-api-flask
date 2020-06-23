from flask_restful import Resource, reqparse
import pymysql

#AdminTimeTable class is to interact with the Timetable table.
class AdminTimeTable(Resource):
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('request_no', type=int, help="request_no cannot be left blank!")
        data = parser.parse_args()
        #create query string
        qstr = f""" SELECT * FROM timetable where request_no = { data['request_no'] };"""
        try:
            return query(qstr)
        except:
            return {
                "message" : "There was an error connecting to the timetable table while retrieving."
            }, 500

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('b_id', type=int, required=True, help="b_id cannot be left blank!")
        #parser.add_argument('d_id', type=int, required=True, help="d_id cannot be left blank!")
        parser.add_argument('s_code', type=str, required=True, help="s_code cannot be left blank!")
        parser.add_argument('exam_type', type=str, required=True, help="exam_type cannot be left blank!")
        parser.add_argument('subtype', type=str, required=True, help="subtype cannot be left blank!")

        parser.add_argument('start_at', type=str, required=True, help="start_at cannot be left blank!")
        parser.add_argument('end_at', type=str, required=True, help="end_at cannot be left blank!")
        parser.add_argument('date', type=str, required=True, help="date cannot be left blank!")
        parser.add_argument('year', type=int, required=True, help="year cannot be left blank!")
        parser.add_argument('sem_no', type=int, required=True, help="sem_no cannot be left blank!")
        parser.add_argument('subject_name', type=str, required=True, help="subject_name cannot be left blank!")
        data = parser.parse_args()
        try:
            connection = pymysql.connect(host='localhost',
                                        user='harish',
                                        password='',
                                        db='testapi',
                                        cursorclass=pymysql.cursors.DictCursor)
            
            #start connection, create cursor and execute query from cursor
            connection.begin()
            cursor = connection.cursor()

            qstr = f""" 
            INSERT INTO subject (s_code, subject_name)
            SELECT * FROM (SELECT '{data['s_code']}', '{data['subject_name']}') as temp
            WHERE NOT EXISTS (
                SELECT s_code FROM subject WHERE s_code = '{data['s_code']}'
            ) LIMIT 1;
            """

            cursor.execute(qstr)

            qstr = f""" 
            INSERT INTO details (start_at, end_at, date, year, sem_no)
            SELECT * FROM (SELECT '{data['start_at']}', '{data['end_at']}', '{data['date']}', '{data['year']}' , '{data['sem_no']}') as temp
            WHERE NOT EXISTS (
                SELECT d_id FROM details WHERE 
                start_at = '{data['start_at']}' AND
                end_at = '{data['end_at']}' AND
                date = '{data['date']}' AND
                year = '{data['year']}' AND
                sem_no = '{data['sem_no']}'
            ) LIMIT 1;
            """

            cursor.execute(qstr)

            qstr = f""" 
            INSERT INTO timetable (b_id, d_id, s_code, exam_type, subtype) 
            values('{data['b_id']}', 

                    (SELECT d_id FROM details WHERE 
                        start_at = '{data['start_at']}' AND
                        end_at = '{data['end_at']}' AND
                        date = '{data['date']}' AND
                        year = '{data['year']}' AND
                        sem_no = '{data['sem_no']}'),

                        '{data['s_code']}', 
                        '{data['exam_type']}', 
                        '{data['subtype']}');
            """

            cursor.execute(qstr)
            
            connection.commit() #commit the changes made
            
            #close the cursor and connection
            cursor.close()
            connection.close()

        except (pymysql.err.InternalError, pymysql.err.ProgrammingError, pymysql.err.IntegrityError) as e:
            return {
                "message" : "MySQL error: " + str(e)
            }, 500
        except Exception as e:
            return {
                "message" : "There was an error connecting to the requests table while inserting." + str(e)
            }, 500
        
        return {
            "message" : "Succesfully inserted"
        }, 200