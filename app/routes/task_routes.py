from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from ..db import db
from .route_utilities import validate_model

bp = Blueprint("task_bp", __name__, url_prefix="/task")

# POST
@bp.post("")
def create_task():
    request_body = request.get_json()

    try:
        new_task = Task.from_dict(request_body)
        
    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))

    db.session.add(new_task)
    db.session.commit()

    return new_task.to_dict(), 201

# GET
@bp.get("")
def get_all_tasks():
    query = db.select(Task)

    title_param = request.args.get("title")
    if title_param:
        query = query.where(Task.title.ilike(f"%{title_param}%"))

    description_param = request.args.get("description")
    if description_param:
        query = query.where(Task.description.ilike(f"%{description_param}%"))

    query = query.order_by(Task.id)
    task = db.session.scalars(query)

    tasks_response = []
    for task in task:
        tasks_response.append(task.to_dict())
    return tasks_response

@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    return task.to_dict()

# PUT
@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

# DELETE
@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(task_id)
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")
