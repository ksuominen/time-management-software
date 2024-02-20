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


def add_workhours(starttime, endtime, lunchbreak, consultname, customername):
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

def delete_workhours(id):
    query = sql.SQL(
        "DELETE FROM workhours WHERE id = %s"
    )
    con = connect()
    if con is not None:
        cursor = con.cursor()
        cursor.execute(query,(id,))
        con.commit()
        cursor.close()
        con.close()



# add_workhours("19-02-2024 08:00", "19-02-2024 17:30", 30, "Jasper", "Finnair")
delete_workhours(3)