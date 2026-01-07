from flask import Flask
from flasgger import Swagger
from app.controller.attack_type_controller import attack_type_bp
from app.controller.cyber_threat_controller import cyber_threat_bp
from app.controller.defense_mechanism_controller import defense_mechanism_bp
from app.controller.security_vulnerability_controller import security_vulnerability_bp
from app.controller.target_industry_controller import target_industry_bp

app = Flask(__name__)
Swagger(app)

app.register_blueprint(attack_type_bp)
app.register_blueprint(cyber_threat_bp)
app.register_blueprint(defense_mechanism_bp)
app.register_blueprint(security_vulnerability_bp)
app.register_blueprint(target_industry_bp)


@app.get("/")
def root():
    return "OK"

if __name__ == "__main__":
    app.run(debug=True)