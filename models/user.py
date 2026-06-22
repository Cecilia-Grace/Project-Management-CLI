import uuid

class User:
    def __init__(self, username, email, id=None):
        self.id = id or str(uuid.uuid4())[:6]
        self.username = username
        self.email = email
        
        
    def to_dict(self):
        return self.__dict__
    
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)
    
    
    def __str__(self):
        return f"👤 User ID: [{self.id}] | User Name: {self.username} | User Email: {self.email}"
    
    
