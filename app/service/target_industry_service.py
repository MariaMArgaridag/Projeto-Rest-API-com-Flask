class TargetIndustryService:
    def __init__(self, repository):
        self.repo = repository

    def create(self, industry: str):
        return self.repo.create(industry)

    def list(self):
        return self.repo.list()

    def get_by_id(self, id: int):
        return self.repo.get_by_id(id)
    
    def update(self, id: int, industry: str):
        return self.repo.update(id, industry)
    
    def delete(self, id: int):
        return self.repo.delete(id)