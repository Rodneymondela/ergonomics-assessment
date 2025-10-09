from flask import Blueprint
bp = Blueprint('assessments', __name__, template_folder='../../templates/assessments')
from . import routes  # noqa
