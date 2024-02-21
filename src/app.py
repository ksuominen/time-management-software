from flask import Flask, request
from queries import add_workhours, delete_workhours, get_workhours_by_consult

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return {"index": True}


@app.route("/workhours", methods=["POST"])
def create_workhour():
    try:
        data = request.get_json()
        starttime = data["starttime"]
        endtime = data["endtime"]
        lunchbreak = data["lunchbreak"]
        consultname = data["consultname"]
        customername = data["customername"]
        add_workhours(starttime, endtime, lunchbreak, consultname, customername)
        return {"success": "added workhours for: %s" % consultname}
    except:
        return {"error": "error adding workhours"}
    
@app.route("/workhours/<int:id>", methods=["DELETE"])
def delete_workhour(id):
    try:
        delete_workhours(id)
        return {"success": f"id: {id} was successfully deleted"}
    except:
        return {"error": "error deleting workhours"}
    
@app.route("/workhours/<consultname>", methods=["GET"])
def get_workhour_by_consult(consultname):
    try:
        workhours = get_workhours_by_consult(consultname)
        return workhours
    except:
        return {"error": "error with printing workhours"}

        