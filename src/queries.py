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

# delete row from workhours table
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
        
# Update daily workhours for a consult
def update_workhours(id, starttime=None, endtime=None, lunchbreak=None, consultname=None, customername=None):
    query_parts = ["UPDATE workhours SET"]
    query_params = {"id": id}

    # Dynamically add each parameter to the query if it's provided
    if starttime is not None:
        query_parts.append("starttime = to_timestamp(%(starttime)s, 'DD-MM-YYYY HH24:MI'),")
        query_params["starttime"] = starttime
    if endtime is not None:
        query_parts.append("endtime = to_timestamp(%(endtime)s, 'DD-MM-YYYY HH24:MI'),")
        query_params["endtime"] = endtime
    if lunchbreak is not None:
        query_parts.append("lunchbreak = %(lunchbreak)s,")
        query_params["lunchbreak"] = lunchbreak
    if consultname is not None:
        query_parts.append("consultname = %(consultname)s,")
        query_params["consultname"] = consultname
    if customername is not None:
        query_parts.append("customername = %(customername)s,")
        query_params["customername"] = customername

    # Remove the trailing comma from the last added parameter
    if query_parts[-1].endswith(','):
        query_parts[-1] = query_parts[-1][:-1]

    # Add the WHERE clause
    query_parts.append("WHERE id = %(id)s")

    # Combine all parts of the query
    query = sql.SQL(" ").join(map(sql.SQL, query_parts))

    # Execute the query
    con = connect()
    if con is not None:
        cursor = con.cursor()
        cursor.execute(query, query_params)
        con.commit()
        cursor.close()
        con.close()
