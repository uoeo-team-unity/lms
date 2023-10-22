import pytest


@pytest.mark.usefixtures("wipe_feature_switch_table")
class TestFeatureSwitch:
    def test_toggle_hacker_mode_on(self, client) -> None:
        # Given the hacker_mode feature is off
        response = client.post("/feature_switch/hacker_mode", json={"active": 0})
        assert response.status_code == 200
        assert response.get_json() == {"message": "Hacker mode turned off"}

        # When I turn the hacker_mode feature on
        response = client.post("/feature_switch/hacker_mode", json={"active": 1})

        # Then the response should indicate that hacker_mode is now on
        assert response.status_code == 200
        assert response.get_json() == {"message": "Hacker mode turned on"}

    def test_toggle_hacker_mode_off(self, client) -> None:
        # Given the hacker_mode feature is on
        response = client.post("/feature_switch/hacker_mode", json={"active": 1})
        assert response.status_code == 200
        assert response.get_json() == {"message": "Hacker mode turned on"}

        # When I turn the hacker_mode feature off
        response = client.post("/feature_switch/hacker_mode", json={"active": 0})

        # Then the response should indicate that hacker_mode is now off
        assert response.status_code == 200
        assert response.get_json() == {"message": "Hacker mode turned off"}
