import json
import operator

def load(filename):
    """
    Loads data from a JSON file (filename) and returns a list of all projects in the database sorted after number. Parameters: filename (JSON file that contains all the information), Returns: list of dictionaries.
    """
    try:
        with open(filename, "r") as f:
            projects = list(json.load(f))
            projects.sort(key=operator.itemgetter("project_id"))
        return projects
    except:
        print("Could not load database")
        return None

def get_project_count(db):
    """
    Retrieves the number of projects in the project list. Parameters: db (a list returned by the load function).
    """
    return len(db)

def get_project(db, id):
    """
    Fetches the project with the specified id from the specified list, if the project id is not present it returns None. Parameters: db (list returned by load function), id (The id of the wanted project). Returns: Dict containing all the project data for the specified project, or None.
    """
    try:
        for dict in db:
            if int(dict["project_id"]) == int(id):
                return dict
    except:
        ("Could not get projects")
        return None


def get_techniques(db):
    """
    Fetches a list of all the techniques used in the projects in lexicographical order. Parameters: db (list returned by load function). Returns: list containing all techniques used in db.
    """
    try:
        tech_list = []
        techs = []
        for x in db:
            tech_list.append(x["techniques_used"])
        for lst in tech_list:
            for item in lst:
                if item not in techs:
                    techs.append(item)
                    techs.sort()
        return techs
    except:
        print("Could not get techniques")
        return None

def get_technique_stats(db):
    """
    Collects and returns statistics for all the techniques used. Imports all the techniques with the get_techniques function and returns the project id and project name for all projects that use that technique. This function does that for all the techniques in the in get_techniques. Parameters: db  (list returned by load function). Returns: a dict with each technique as a key and all the projects that use that techniques as a list of dicts.
    """
    tech_stats = {}
    data = get_techniques(db)
    for item in data:
        tech_stats.update({item: []})
    for tech_used in data:
        for projects in db:
            if tech_used in projects["techniques_used"]:
                tech_stats[tech_used].append({"id": projects["project_id"], "name": projects["project_name"]})
    return tech_stats

def search(db, sort_by=None, sort_order="asc", techniques=None, search=None, search_fields=None):
    """
    Search function that organizes all the functions in the data.py to accurately search in the database with a string, by techniques, in certain search fields, sorted by categories and in ascending or descending order. The function is able to search with all these, none or just some of them. The default values of the parameters is None except for sort_order that is descending. Parameters: db (list returned by load function), sort_by (search field to sort by), sort_order (ascending('asc') or descending('desc')), techniques (a list of techniques), search (search string), search_fields (search field to search in).
    """
    db1 = filter_techniques(db, techniques)
    db2 = searching(db1, search, search_fields)
    db3 = sort_by_param(db2, sort_by, sort_order)
    return db3

def sort_by_param(db, sort_by, sort_order):
    """
    Sorting by parameters.
    """
    try:
        if sort_order == "desc":
            db.sort(key=operator.itemgetter(sort_by), reverse= True)
            return db
        elif sort_order == "asc" or sort_order == None:
            db.sort(key=operator.itemgetter(sort_by), reverse= False)
            return db
    except:
        return db
def filter_techniques(db, techniques):
    """
    Returns a database filtered after certain techniques.
    """
    try:
        if techniques == []:
            return db
        else:
            filtered = []
            for filtering in db:
                if filtering_techs(filtering["techniques_used"], techniques) == True:
                    filtered.append(filtering)
                else:
                    filtered = filtered
            return filtered
    except:
        prin("Could not filter techniques")
        return db

def filtering_techs(tech_used, techniques):
    """
    Returns a bool depending on if all specified techniques were used in a project.
    """
    for i in techniques:
        if i in tech_used:
            continue
        else:
            return False
    return True

def searching(db, search, search_fields):
    """
    Uses a string to find matching text in database according to search fields. Returns dictionarie.
    """
    try:
        result = []
        for i in db:
            if search_fields != []:
                for t in search_fields:
                    if search.lower() in str(i[t]).lower():
                        if i not in result:
                            result.append(i)
            else:
                for x in i:
                    if search.lower() in str(i[x]).lower():
                        if i not in result:
                            result.append(i)
        return result
    except:
        print("could not search")
        return db
