import uuid
from datetime import datetime, date

class Project:
    def __init__(self, project_title, user_id, due_date, project_description="", id=None):
        self.id = id or str(uuid.uuid4())[:6]
        self.project_title = project_title
        self.user_id = user_id          #links to the user that owns the project
        
        if isinstance(due_date, (date, datetime)):
            self.due_date = due_date.strftime("%Y-%m-%d") 
        elif isinstance(due_date, str):
            try:
                parsed_date = datetime.strptime(due_date.strip(), "%Y-%m-%d")
                self.due_date = parsed_date.strftime("%Y-%m-%d")
            except ValueError:
                self.due_date = "No deadline"
            
        self.project_description = project_description
        
        
    def to_dict(self):
        return self.__dict__
    
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)
    
    
    def __str__(self):
        return f"📁 Project ID: [{self.id}] | Project Title: {self.project_title} | Project Owner ID: {self.user_id} | Due Date: {self.due_date} | Project Description: {self.project_description}"
    
    
