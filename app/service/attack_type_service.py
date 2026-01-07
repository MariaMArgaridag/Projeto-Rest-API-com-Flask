class AttackTypeService:
    def __init__(self, repository):
        self.repo = repository

    def create(self, type: str):
        return self.repo.create(type)

    def list(self):
        return self.repo.list()

    def get_by_id(self, id: int):
        return self.repo.get_by_id(id)
    
    def update(self, id: int, type: str):
        return self.repo.update(id, type)
    
    def delete(self, id: int):
        return self.repo.delete(id)