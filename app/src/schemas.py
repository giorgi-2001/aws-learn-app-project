class QueryParams:
    def __init__(self, name: str | None = None):
        self.name = name
    
    def to_dict(self):
        data = {"name": self.name}
        return {key: value for key, value in data.items() if value}
    
    def model_dump(self):
        return self.to_dict()