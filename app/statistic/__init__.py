from flask import Blueprint

statistic = Blueprint('statistic', __name__)

from . import views, api_for_chart