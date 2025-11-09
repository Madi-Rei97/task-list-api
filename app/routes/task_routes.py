from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from ..db import db

task_bp = Blueprint("task_bp", __name__, url_prefix="/task")

# POST
@task_bp.post("")
def create_task():
    request_body = request.get_json()
    title = request_body["title"]
    description = request_body["description"]
    completed_at = request_body["completed_at"]

    new_task = Task(title=title, description=description, 
                    completed_at=completed_at)
    db.session.add(new_task)
    db.session.commit()

    response = {
        "id": new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "completed_at": new_task.completed_at
    }
    return response, 201

# GET
@task_bp.get("")
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
        tasks_response.append(
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed_at": task.completed_at
            }
        )
    return tasks_response

@task_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_task(task_id)

    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed_at": task.completed_at
    }

# PUT
@task_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

# DELETE
@task_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_task(task_id)
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

# Validate Task
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        response = {"message": f"Task {task_id} invalid"}
        abort(make_response(response , 400))

    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)
    
    if not task:
        response = {"message": f"Task {task_id} not found"}
        abort(make_response(response, 404))

    return task
