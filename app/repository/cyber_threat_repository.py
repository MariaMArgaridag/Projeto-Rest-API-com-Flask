class CyberThreatRepository:
    def __init__(self, db):
        self.db = db

    def create(self, country: str, year: int, attack_type: int, target_industry: int, financial_loss: float, affected_users: int, attack_source: int, security_vulnerability: int, defense_mechanism: int, resolution_time: int):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(
                """INSERT INTO global_cyber_threats
                (Country, Year, `Attack Type`, `Target Industry`, `Financial Loss (in Million $)`, `Number of Affected Users`,
                `Attack Source`, `Security Vulnerability Type`, `Defense Mechanism Used`, `Incident Resolution Time (in Hours)`)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (country, year, attack_type, target_industry, financial_loss, affected_users, attack_source, security_vulnerability, defense_mechanism, resolution_time)
            )

            conn.commit()

            return {
                "Id": cursor.lastrowid,
                "Country": country,
                "Year": year,
                "Attack Type": attack_type,
                "Target Industry": target_industry,
                "Financial Loss (in Million $)": financial_loss,
                "Number of Affected Users": affected_users,
                "Attack Source": attack_source,
                "Security Vulnerability Type": security_vulnerability,
                "Defense Mechanism Used": defense_mechanism,
                "Incident Resolution Time (in Hours)": resolution_time
            }
        except:
            return None

    def list(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                gct.Id,
                gct.Country,
                gct.Year,
                gct.`Financial Loss (in Million $)` AS financial_loss,
                gct.`Number of Affected Users` AS affected_users,
                gct.`Incident Resolution Time (in Hours)` AS resolution_time,
                atp.Id AS attack_type_id,
                atp.Type AS attack_type,
                ti.Id AS target_industry_id,
                ti.Industry AS target_industry,
                src.Id AS attack_source_id,
                src.Source AS attack_source,
                svt.Id AS vulnerability_id,
                svt.Vulnerability AS vulnerability,
                dm.Id AS defense_mechanism_id,
                dm.Mechanism AS defense_mechanism
            FROM global_cyber_threats gct
            JOIN Attack_Types atp
                ON atp.Id = gct.`Attack Type`
            JOIN Target_Industries ti
                ON ti.Id = gct.`Target Industry`
            JOIN Attack_Sources src
                ON src.Id = gct.`Attack Source`
            JOIN Security_Vulnerabilities svt
                ON svt.Id = gct.`Security Vulnerability Type`
            JOIN Defense_Mechanisms dm
                ON dm.Id = gct.`Defense Mechanism Used`;
            """)
        
        rows = cursor.fetchall()
        result = []

        for row in rows:
            result.append({
                "Id": row["Id"],
                "Country": row["Country"],
                "Year": row["Year"],
                "Financial Loss (in Million $)": row["financial_loss"],
                "Number of Affected Users": row["affected_users"],
                "Incident Resolution Time (in Hours)": row["resolution_time"],

                "Attack Type": {
                    "Id": row["attack_type_id"],
                    "Type": row["attack_type"]
                },
                "Target Industry": {
                    "Id": row["target_industry_id"],
                    "Industry": row["target_industry"]
                },
                "Attack Source": {
                    "Id": row["attack_source_id"],
                    "Source": row["attack_source"]
                },
                "Security Vulnerability Type": {
                    "Id": row["vulnerability_id"],
                    "Vulnerability": row["vulnerability"]
                },
                "Defense Mechanism Used": {
                    "Id": row["defense_mechanism_id"],
                    "Mechanism": row["defense_mechanism"]
                }
            })

        return result
    
    def get_by_id(self, id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                gct.Id,
                gct.Country,
                gct.Year,
                gct.`Financial Loss (in Million $)` AS financial_loss,
                gct.`Number of Affected Users` AS affected_users,
                gct.`Incident Resolution Time (in Hours)` AS resolution_time,
                atp.Id AS attack_type_id,
                atp.Type AS attack_type,
                ti.Id AS target_industry_id,
                ti.Industry AS target_industry,
                src.Id AS attack_source_id,
                src.Source AS attack_source,
                svt.Id AS vulnerability_id,
                svt.Vulnerability AS vulnerability,
                dm.Id AS defense_mechanism_id,
                dm.Mechanism AS defense_mechanism
            FROM global_cyber_threats gct
            JOIN Attack_Types atp
                ON atp.Id = gct.`Attack Type`
            JOIN Target_Industries ti
                ON ti.Id = gct.`Target Industry`
            JOIN Attack_Sources src
                ON src.Id = gct.`Attack Source`
            JOIN Security_Vulnerabilities svt
                ON svt.Id = gct.`Security Vulnerability Type`
            JOIN Defense_Mechanisms dm
                ON dm.Id = gct.`Defense Mechanism Used`
            WHERE gct.Id = %s
            """,
            (id,)
        )

        row = cursor.fetchone()

        if row is None:
            return None

        result = {
            "Id": row["Id"],
            "Country": row["Country"],
            "Year": row["Year"],
            "Financial Loss (in Million $)": row["financial_loss"],
            "Number of Affected Users": row["affected_users"],
            "Incident Resolution Time (in Hours)": row["resolution_time"],

            "Attack Type": {
                "Id": row["attack_type_id"],
                "Type": row["attack_type"]
            },
            "Target Industry": {
                "Id": row["target_industry_id"],
                "Industry": row["target_industry"]
            },
            "Attack Source": {
                "Id": row["attack_source_id"],
                "Source": row["attack_source"]
            },
            "Security Vulnerability Type": {
                "Id": row["vulnerability_id"],
                "Vulnerability": row["vulnerability"]
            },
            "Defense Mechanism Used": {
                "Id": row["defense_mechanism_id"],
                "Mechanism": row["defense_mechanism"]
            }
        }
        
        return result
    
    def update(
        self, id: int, country: str, year: int, attack_type: int, target_industry: int, financial_loss: float, affected_users: int,
        attack_source: int, security_vulnerability: int, defense_mechanism: int, resolution_time: int
    ):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            UPDATE global_cyber_threats
            SET
                Country = %s,
                Year = %s,
                `Attack Type` = %s,
                `Target Industry` = %s,
                `Financial Loss (in Million $)` = %s,
                `Number of Affected Users` = %s,
                `Attack Source` = %s,
                `Security Vulnerability Type` = %s,
                `Defense Mechanism Used` = %s,
                `Incident Resolution Time (in Hours)` = %s
            WHERE Id = %s
            """,
            (
                country,
                year,
                attack_type,
                target_industry,
                financial_loss,
                affected_users,
                attack_source,
                security_vulnerability,
                defense_mechanism,
                resolution_time,
                id
            )
        )

        conn.commit()

        return {
            "Id": id,
            "Country": country,
            "Year": year,
            "Attack Type": attack_type,
            "Target Industry": target_industry,
            "Financial Loss (in Million $)": financial_loss,
            "Number of Affected Users": affected_users,
            "Attack Source": attack_source,
            "Security Vulnerability Type": security_vulnerability,
            "Defense Mechanism Used": defense_mechanism,
            "Incident Resolution Time (in Hours)": resolution_time
        }
    
    def delete(self, id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "DELETE FROM global_cyber_threats WHERE id = %s",
            (id,)
        )

        if cursor.rowcount == 0:
            return False

        conn.commit()
        return True
    
    def attack_source_percentage(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                ats.Id AS attack_source_id,
                ats.Source AS attack_source,
                COUNT(gct.Id) AS total_attacks,
                COALESCE(
                    (
                        COUNT(gct.Id) /
                        NULLIF(
                            (SELECT COUNT(*) FROM global_cyber_threats),
                            0
                        )
                    ) * 100,
                    0
                ) AS percentage
            FROM global_cyber_threats gct
            RIGHT JOIN Attack_Sources ats
                ON ats.Id = gct.`Attack Source`
            GROUP BY ats.Id, ats.source
            ORDER BY percentage DESC
            """
        )

        rows = cursor.fetchall()
        result = []

        for row in rows:
            result.append({
                "Id": row["attack_source_id"],
                "Source": row["attack_source"],
                "Total": row["total_attacks"],
                "Percentage": float(row["percentage"])
            })

        return result

    def attack_type_percentage(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                atp.Id AS attack_type_id,
                atp.Type AS attack_type,
                COUNT(gct.Id) AS total_attacks,
                COALESCE(
                    (
                        COUNT(gct.Id) /
                        NULLIF(
                            (SELECT COUNT(*) FROM global_cyber_threats),
                            0
                        )
                    ) * 100,
                    0
                ) AS percentage
            FROM global_cyber_threats gct
            RIGHT JOIN Attack_Types atp
                ON atp.Id = gct.`Attack Type`
            GROUP BY atp.Id, atp.Type
            ORDER BY percentage DESC
            """
        )

        rows = cursor.fetchall()
        result = []

        for row in rows:
            result.append({
                "Id": row["attack_type_id"],
                "Type": row["attack_type"],
                "Total": row["total_attacks"],
                "Percentage": float(row["percentage"])
            })

        return result
    
    def defense_mechanism_percentage(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                dfm.Id AS defense_mechanism_id,
                dfm.Mechanism AS defense_mechanism,
                COUNT(gct.Id) AS total_attacks,
                COALESCE(
                    (
                        COUNT(gct.Id) /
                        NULLIF(
                            (SELECT COUNT(*) FROM global_cyber_threats),
                            0
                        )
                    ) * 100,
                    0
                ) AS percentage
            FROM global_cyber_threats gct
            RIGHT JOIN Defense_Mechanisms dfm
                ON dfm.Id = gct.`Defense Mechanism Used`
            GROUP BY dfm.Id, dfm.Mechanism
            ORDER BY percentage DESC
            """
        )

        rows = cursor.fetchall()
        result = []

        for row in rows:
            result.append({
                "Id": row["defense_mechanism_id"],
                "Defense": row["defense_mechanism"],
                "Total": row["total_attacks"],
                "Percentage": float(row["percentage"])
            })

        return result
    
    def security_vulnerability_percentage(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                scv.Id AS security_vulnerability_id,
                scv.Vulnerability AS security_vulnerability,
                COUNT(gct.Id) AS total_attacks,
                COALESCE(
                    (
                        COUNT(gct.Id) /
                        NULLIF(
                            (SELECT COUNT(*) FROM global_cyber_threats),
                            0
                        )
                    ) * 100,
                    0
                ) AS percentage
            FROM global_cyber_threats gct
            RIGHT JOIN Security_Vulnerabilities scv
                ON scv.Id = gct.`Security Vulnerability Type`
            GROUP BY scv.Id, scv.Vulnerability
            ORDER BY percentage DESC
            """
        )

        rows = cursor.fetchall()
        result = []

        for row in rows:
            result.append({
                "Id": row["security_vulnerability_id"],
                "Vulnerability": row["security_vulnerability"],
                "Total": row["total_attacks"],
                "Percentage": float(row["percentage"])
            })

        return result
    
    def target_industry_percentage(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                tgi.Id AS target_industry_id,
                tgi.Industry AS target_industry,
                COUNT(gct.Id) AS total_attacks,
                COALESCE(
                    (
                        COUNT(gct.Id) /
                        NULLIF(
                            (SELECT COUNT(*) FROM global_cyber_threats),
                            0
                        )
                    ) * 100,
                    0
                ) AS percentage
            FROM global_cyber_threats gct
            RIGHT JOIN Target_Industries tgi
                ON tgi.Id = gct.`Target Industry`
            GROUP BY tgi.Id, tgi.Industry
            ORDER BY percentage DESC
            """
        )

        rows = cursor.fetchall()
        result = []

        for row in rows:
            result.append({
                "Id": row["target_industry_id"],
                "Industry": row["target_industry"],
                "Total": row["total_attacks"],
                "Percentage": float(row["percentage"])
            })

        return result