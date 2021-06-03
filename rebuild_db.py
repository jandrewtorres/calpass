import data.db_access as dba
import json
from pathlib import Path


courses = json.load(Path('scraper/courses.json').open('r'))
profs = json.load(Path('scraper/profs.json').open('r'))
dba.build_db(courses, profs, dbpath='course_database')