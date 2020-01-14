from flask import Flask, render_template, request, redirect, url_for
from data import *

app = Flask(__name__)



@app.errorhandler(404)
def page_not_found(e):
    """
    Upon reciving an unrecognizable url, this function renders a premade error page, displaying that the url is not found.
    """
    return render_template("pagenotfound.html")

@app.route("/")
def index():
    """
    Firstly loads the database to then set a variable ("project_new") to fetch the latest project. Then renders the index.html page along with the newest project.
    """
    db = load("database.json")
    project_new = get_project(db, len(db))
    return render_template("index.html", proj = project_new)

@app.route("/projects", methods=['GET'])
def projects():
    """
    Loads the database and then applies the search function on the database from the data module, along with the get techniques function. Then renders the project.html page with the new filterd database and the techniques.
    """
    db = load("database.json")
    pick_techs = get_techniques(db)
    filtered = search(db, request.args.get('sorting'), request.args.get('sort'),request.args.getlist('techniques'), request.args.get('inp_for_search'), request.args.getlist('categories'))
    return render_template("projects.html", proj = filtered, pick_techs = pick_techs)

@app.route("/techniques", methods=['GET'])
def techniques():
    """
    Loads the database and then fetches all the techniques with the funciton get_techniques from the data module. Then filter the database according to the technique parameters applied by the user. Afterwards the function renders the techniques.html page with the techniques and the projects filtered to the techniques.
    """
    db  = load("database.json")
    pick_techs = get_techniques(db)
    tech_list = filter_techniques(db, request.args.getlist('tech_values'))
    return render_template("techniques.html", pick_techs = pick_techs ,tech_list = tech_list)

@app.route("/project/<int:project_id>")
def project_page(project_id):
    """
    Retrieves the project id and then renders the projectid.html page along with the correct projct data according to it's id.
    """
    db = load("database.json")
    try:
        get_proj = get_project(db, project_id)
        return render_template("projectid.html", project = get_proj)
    except:
        return render_template("pagenotfound.html")


if __name__ == "__main__":
    app.run(debug=True)
