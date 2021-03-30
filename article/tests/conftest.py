import pytest


@pytest.fixture()
def valid_board_data() -> Dict:
    return {
        "dimensionX": 100,
        "dimensionY": 100,
        "gerberFileName": "gerber.zip",
        "gerberHash": "blablub123",
        "differentDesigns": 1,
        "layers": 3,
        "deliveryFormat": "Single PCB",
        "thickness": 1.6,
        "color": "Red",
        "surfaceFinish": "no",
        "copperWeight": 2,
        "goldFingers": "no",
        "castellatedHoles": "no",
        "removeOrderNum": "yes",
        "confirmProdFile": "yes",
        "flyingProbeTest": "no"
    }