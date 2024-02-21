from config import config
import psycopg2
from psycopg2 import sql


def connect():
    con = None
    try:
        con = psycopg2.connect(**config())
        return con
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# Add daily workhours for a consult
def db_add_workhours(starttime, endtime, lunchbreak, consultname, customername):
    query = sql.SQL(
        "INSERT INTO workhours (starttime, endtime, lunchbreak, consultname, customername) VALUES (to_timestamp(%(starttime)s, 'dd-mm-yyyy hh24:mi'), to_timestamp(%(endtime)s, 'dd-mm-yyyy hh24:mi'), %(lunchbreak)s, %(consultname)s, %(customername)s)"
    )
    con = connect()
    if con is not None:
        cursor = con.cursor()
        cursor.execute(
            query,
            {
                "starttime": starttime,
                "endtime": endtime,
                "lunchbreak": lunchbreak,
                "consultname": consultname,
                "customername": customername,
            },
        )
        con.commit()
        cursor.close()
        con.close()

# Update daily workhours for a consult
def db_update_workhours(id, starttime, endtime, lunchbreak, consultname, customername):
    query = sql.SQL(
        ''' UPDATE workhours 
            SET starttime = %s, endtime = %s, lunchbreak = %s, consultname = %s, customername = %s 
            WHERE id = %s;
        '''
    )
    con = connect()
    if con is not None:
        cursor = con.cursor()
        cursor.execute(
            query, (starttime, endtime, lunchbreak, consultname, customername, id)
        )
        con.commit()
        cursor.close()
        con.close()