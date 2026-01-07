class DefenseMechanismService:
    def __init__(self, repository):
        self.repo = repository

    def create(self, mechanism: str):
        return self.repo.create(mechanism)

    def list(self):
        return self.repo.list()

    def get_by_id(self, id: int):
        return self.repo.get_by_id(id)
    
    def update(self, id: int, mechanism: str):
        return self.repo.update(id, mechanism)
    
    def delete(self, id: int):
        return self.repo.delete(id)