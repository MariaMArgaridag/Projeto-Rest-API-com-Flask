class CyberThreatService:
    def __init__(self, repository):
        self.repo = repository

    def create(self, country: str, year: int, attack_type: int, target_industry: int, financial_loss: float, affected_users: int, attack_source: int, security_vulnerability: int, defense_mechanism: int, resolution_time: int):
        return self.repo.create(country, year, attack_type, target_industry, financial_loss, affected_users, attack_source, security_vulnerability, defense_mechanism, resolution_time)

    def list(self):
        return self.repo.list()

    def get_by_id(self, id: int):
        return self.repo.get_by_id(id)
    
    def update(
        self,
        id: int,
        country: str | None,
        year: int | None,
        attack_type: int | None,
        target_industry: int | None,
        financial_loss: float | None,
        affected_users: int | None,
        attack_source: int | None,
        security_vulnerability: int | None,
        defense_mechanism: int | None,
        resolution_time: int | None
    ):
        current = self.repo.get_by_id(id)

        if current is None:
            return None

        country = country if country is not None else current["Country"]
        year = year if year is not None else current["Year"]
        attack_type = attack_type if attack_type is not None else current["Attack Type"]["id"]
        target_industry = target_industry if target_industry is not None else current["Target Industry"]["id"]
        financial_loss = financial_loss if financial_loss is not None else current["Financial Loss (in Million $)"]
        affected_users = affected_users if affected_users is not None else current["Number of Affected Users"]
        attack_source = attack_source if attack_source is not None else current["Attack Source"]["id"]
        security_vulnerability = (
            security_vulnerability
            if security_vulnerability is not None
            else current["Security Vulnerability Type"]["id"]
        )
        defense_mechanism = (
            defense_mechanism
            if defense_mechanism is not None
            else current["Defense Mechanism Used"]["id"]
        )
        resolution_time = (
            resolution_time
            if resolution_time is not None
            else current["Incident Resolution Time (in Hours)"]
        )

        return self.repo.update(
            id,
            country,
            year,
            attack_type,
            target_industry,
            financial_loss,
            affected_users,
            attack_source,
            security_vulnerability,
            defense_mechanism,
            resolution_time
        )
    
    def delete(self, id: int):
        return self.repo.delete(id)
    
    def attack_source_percentage(self):
        return self.repo.attack_source_percentage()
    
    def attack_type_percentage(self):
        return self.repo.attack_type_percentage()
    
    def defense_mechanism_percentage(self):
        return self.repo.defense_mechanism_percentage()
    
    def security_vulnerability_percentage(self):
        return self.repo.security_vulnerability_percentage()
    
    def target_industry_percentage(self):
        return self.repo.target_industry_percentage()