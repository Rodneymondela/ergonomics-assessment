from flask import Blueprint
bp = Blueprint('jobs', __name__, template_folder='../../templates/jobs')
from . import routes  # noqa
