from flask import Blueprint, jsonify, request

from .feature_switch_model import FeatureSwitch

feature_switch_domain = Blueprint("feature_switch", __name__, url_prefix="/feature_switch")


@feature_switch_domain.post("/hacker_mode")
def update_hacker_mode():
    data = request.get_json()
    active = data.get("active")

    if active not in {0, 1}:
        return jsonify({"message": "Invalid value for active. Please use 1 to turn on and 0 to turn off."}), 400

    feature = FeatureSwitch.find_by(name="hacker_mode")
    if feature is None:
        feature = FeatureSwitch.create(name="hacker_mode", active=active)
    else:
        feature.set_value(active)

    status = "on" if active else "off"
    return jsonify({"message": f"Hacker mode turned {status}"}), 200
