from flask import Flask, request
from queries import add_workhours

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
