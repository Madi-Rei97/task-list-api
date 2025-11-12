from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from datetime import datetime
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from .goal import Goal
from sqlalchemy import ForeignKey

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    @classmethod
    def from_dict(cls, task_data):
        new_task = Task(title=task_data["title"],
                        description=task_data["description"],
                        completed_at=task_data["is_complete"] if "is_complete"
                        in task_data and task_data["is_complete"] != False 
                        else None)
        return new_task
    
    def to_dict(self):
        task_as_dict = {}
        task_as_dict["id"] = self.id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        task_as_dict["is_complete"] = (False if self.completed_at is None else
                                        self.completed_at)
        if self.goal_id:
            task_as_dict["goal_id"] = self.goal_id

        return task_as_dict