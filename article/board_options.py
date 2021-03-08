from django.db import models


# Constraints on the acceptable option values (as discussed on the Miro Board).
# These might need to be updated according to JLCPCB's requirements.

OPTIONS = {
    # Numeric constraints

    "dim_x": {
        "min": 6,
        "max": 400,
        "default": 100
    },

    "dim_y": {
        "min": 6,
        "max": 500,
        "default": 100
    },

    # Categorical constraints

    "num_designs": {
        "choices": [
            (1, 1)
        ],
        "default": 1
    },

    "layers": {
        "choices": [
            (1, 1),
            (2, 2),
        ],
        "default": 2
    },

    "delivery_format": {
        "choices": [
            ("single_pcb", "Single PCB"),
        ],
        "default": "single_pcb"
    },

    "thickness": {
        "choices": [
            (0.4, 0.4),
            (0.6, 0.6),
            (0.8, 0.8),
            (1.0, 1.0),
            (1.2, 1.2),
            (1.6, 1.6),
            (2.0, 2.0)
        ],
        "default": 1.6
    },

    "color": {
        "choices": [
            ("green", "green"),
            ("red", "red"),
            ("yellow", "yellow"),
            ("blue", "blue"),
            ("white", "white"),
            ("black", "black"),
        ],
        "default": "green"
    },

    "surface_finish": {
        "choices": [
            ("hasl_with_lead", "HASL(with lead)"),
            ("lead_free_hasl", "LeadFree HASL-RoHS"),
            ("enig-rohs", "ENIG-RoHS")
        ],
        "default": "hasl_with_lead"
    },

    "copper_weight": {
        "choices": [
            (1, "1 oz"),
            (2, "2 oz")
        ],
        "default": 1
    },

    "gold_fingers": {
        "choices": [
            ("no", "No"),
            ("yes", "Yes")
        ],
        "default": "no"
    },

    "castellated_holes": {
        "choices": [
            ("no", "No"),
        ],
        "default": "no"
    },

    "remove_order_num": {
        "choices": [
            ("no", "No"),
        ],
        "default": "no"
    },

    "confirm_prod_file": {
        "choices": [
            ("no", "No"),
        ],
        "default": "no"
    },

    "flying_probe_test": {
        "choices": [
            ("fully_test", "Fully test")
        ],
        "default": "fully_test"
    },
}
