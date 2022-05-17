import os
from flask import request, render_template, redirect, url_for
from flask_cors import cross_origin
from server import app


def start_debug():
    os.environ["FLASK_DEBUG"] = "1"


def stop_debug():
    os.environ["FLASK_DEBUG"] = "0"


@app.errorhandler(403)
def forbidden_error(error=None):
    return redirect(url_for('error', status=403))


@app.errorhandler(404)
@app.errorhandler(405)
def not_found_error(error=None):
    return redirect(url_for('error', status=404))


@app.errorhandler(500)
def internal_error(error=None):
    return redirect(url_for('error', status=500))


@app.route("/error")
@cross_origin()
def error():
    status = request.args.get('status')
    return render_template(status + '.html'), status
