import uuid

class Task:
    def __init__(self,  project_id, task_title, status="To Do", assigned_to=None, id=None):
        self.id = id or str(uuid.uuid4())[:6]
        self.task_title = task_title
        self.status = status
        self.assigned_to = assigned_to          #links to the user that owns the task
        self.project_id = project_id            #links to the project that owns the task
        
        
    def to_dict(self):
        return self.__dict__
    
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)
    
    
    def __str__(self):
        return f"📝 Task ID: [{self.id}] | Task Title: {self.task_title} | Status: {self.status} | Assigned To: {self.assigned_to}"
    
    
