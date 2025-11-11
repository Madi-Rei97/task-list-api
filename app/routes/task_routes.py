from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from ..db import db
from .route_utilities import (validate_model, create_model, 
                                get_models_with_filters)
from datetime import datetime

bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

# POST
@bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model(Task, request_body)

# GET
@bp.get("")
def get_all_tasks():
    return get_models_with_filters(Task, request.args)

@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    return task.to_dict()

# PUT
@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

# PATCH
@bp.patch("/<task_id>/mark_complete")
def mark_complete_task(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.now()
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete_task(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None
    db.session.commit()

    return Response(status=204, mimetype="application/json")

# DELETE
@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")
