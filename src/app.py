from flask import Flask, request
from queries import db_add_workhours, db_delete_workhours, db_get_workhours_by_consult, db_update_workhours

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return {"index": True}


@app.route("/workhours", methods=["POST"])
def create_workhours():
    try:
        data = request.get_json()
        starttime = data["starttime"]
        endtime = data["endtime"]
        lunchbreak = data["lunchbreak"]
        consultname = data["consultname"]
        customername = data["customername"]

        db_add_workhours(starttime, endtime, lunchbreak, consultname, customername)
        return {"success": "added workhours for: %s" % consultname}
    except:
        return {"error": "error adding workhours"}
    
@app.route("/workhours/<int:id>", methods=["PUT"])
def update_workhours(id):
    try:
        data = request.get_json()
        starttime = data["starttime"]
        endtime = data["endtime"]
        lunchbreak = data["lunchbreak"]
        consultname = data["consultname"]
        customername = data["customername"]
        db_update_workhours(id, starttime, endtime, lunchbreak, consultname, customername)
        return {"success": "added workhours for: %s" % consultname}
    except:
        return {"error": "error adding workhours"}
    
@app.route("/workhours/<int:id>", methods=["DELETE"])
def delete_workhours(id):
    try:
        db_delete_workhours(id)
        return {"success": f"id: {id} was successfully deleted"}
    except:
        return {"error": "error deleting workhours"}
    
@app.route("/workhours/<consultname>", methods=["GET"])
def get_workhours_by_consult(consultname):
    try:
        workhours = db_get_workhours_by_consult(consultname)
        return workhours
    except:
        return {"error": "error with printing workhours"}

        