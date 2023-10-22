# Import necessary classes and functions from Flask
from flask import Blueprint, jsonify, request

# Import the FeatureSwitch model from the current package
from .feature_switch_model import FeatureSwitch

# Create a Flask Blueprint for grouping related views under the feature_switch domain
feature_switch_domain = Blueprint("feature_switch", __name__, url_prefix="/feature_switch")


# Define a route to update the hacker_mode feature switch
@feature_switch_domain.post("/hacker_mode")
def update_hacker_mode():
    # Parse JSON data from the request body
    data = request.get_json()
    # Retrieve the 'active' value from the parsed data
    active = data.get("active")

    # Validate that 'active' is either 0 or 1
    if active not in {0, 1}:
        # Return an error message and a 400 Bad Request status if validation fails
        return jsonify({"message": "Invalid value for active. Please use 1 to turn on and 0 to turn off."}), 400

    # Attempt to find an existing feature switch by name
    feature = FeatureSwitch.find_by(name="hacker_mode")
    # If the feature switch doesn't exist, create a new one
    if feature is None:
        feature = FeatureSwitch.create(name="hacker_mode", active=active)
    # If it does exist, update its value
    else:
        feature.set_value(active)

    # Determine the status message based on the 'active' value
    status = "on" if active else "off"
    # Return a success message with the updated status and a 200 OK status code
    return jsonify({"message": f"Hacker mode turned {status}"}), 200
