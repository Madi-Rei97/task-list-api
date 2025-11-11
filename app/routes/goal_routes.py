from flask import Blueprint, abort, make_response, request
from app.models.goal import Goal
from ..db import db

bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

