from config import config
import psycopg2
from psycopg2 import sql
from datetime import datetime


def connect():
    con = None
    try:
        con = psycopg2.connect(**config())
        return con
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def validate_user_input(starttime, endtime, lunchbreak, consultname, customername):
    try:
        starttime_ob = datetime.strptime(starttime, "%Y-%m-%d %H:%M")
    except ValueError:
        return {
            "error": "Incorrect date format for starttime, should be YYYY-MM-DD hh:mm"
        }

    try:
        endtime_ob = datetime.strptime(endtime, "%Y-%m-%d %H:%M")
    except ValueError:
        return {
            "error": "Incorrect date format for endtime, should be YYYY-MM-DD hh:mm"
        }
    if starttime_ob > endtime_ob:
        return {"error": "Endtime cannot be before starttime"}
    now = datetime.now()
    if datetime.date(starttime_ob) > datetime.date(now):
        return {"error": "startdate in the future"}

    if datetime.date(endtime_ob) > datetime.date(now):
        return {"error": "enddate in the future"}
    if datetime.date(starttime_ob) != datetime.date(endtime_ob):
        return {"error": "startime and endtime must be on the same date"}
    if not isinstance(lunchbreak, int) or not (30 <= lunchbreak and 120 >= lunchbreak):
        return {"error": "lunchbreak must to be an integer between 30 and 120"}
    if not isinstance(consultname, str) or len(consultname) > 100 or consultname == "":
        return {
            "error": "consult name must be a string of max 100 characters and must not be empty"
        }
    if (
        not isinstance(customername, str)
        or len(customername) > 100
        or customername == ""
    ):
        return {
            "error": "customer name must be a string of max 100 characters and must not be empty"
        }
    else:
        return "everything ok"


# Add daily workhours for a consult


def db_add_workhours(starttime, endtime, lunchbreak, consultname, customername):
    val = validate_user_input(starttime, endtime, lunchbreak, consultname, customername)
    if val != "everything ok":
        return val

    query = sql.SQL(
        "INSERT INTO workhours (starttime, endtime, lunchbreak, consultname, customername) VALUES (to_timestamp(%(starttime)s, 'yyyy-mm-dd hh24:mi'), to_timestamp(%(endtime)s, 'yyyy-mm-dd hh24:mi'), %(lunchbreak)s, %(consultname)s, %(customername)s)"
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
        return {"success": "added workhours for: %s" % consultname}
    return {"error": "problems with connection"}


# Delete row from workhours table
def db_delete_workhours(id):
    query = sql.SQL("DELETE FROM workhours WHERE id = %s")
    con = connect()
    if con is not None:
        cursor = con.cursor()
        cursor.execute(query, (id,))
        con.commit()
        cursor.close()
        con.close()


# Update daily workhours for a consult
def db_update_workhours(id, starttime, endtime, lunchbreak, consultname, customername):
    val = validate_user_input(starttime, endtime, lunchbreak, consultname, customername)
    if val != "everything ok":
        return val

    query = sql.SQL(
        """ UPDATE workhours 
            SET starttime = %s, endtime = %s, lunchbreak = %s, consultname = %s, customername = %s 
            WHERE id = %s;
        """
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
        return {"success": "updated workhours for: %s" % consultname}
    return {"error": "problems with connection"}


def db_get_workhours_by_consult(consultname):
    query = sql.SQL("SELECT * FROM workhours WHERE consultname = %s")
    con = connect()
    if con is not None:
        cursor = con.cursor()
        cursor.execute(query, (consultname,))
        data = cursor.fetchall()
        cursor.close()
        con.close()
    return data
