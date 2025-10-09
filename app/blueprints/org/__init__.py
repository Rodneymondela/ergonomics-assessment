from flask import Blueprint
bp = Blueprint('org', __name__, template_folder='../../templates/org')
from . import routes  # noqa
