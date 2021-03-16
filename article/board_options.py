"""Constraints on the acceptable option values.
These might need to be updated according to the vendors' requirements.

All options are represented as dictionaries and should include either
NUMERIC or CATEGORICAL constraints on their values. Moreover, each option
has to define a default value.

NUMERIC constraints define, for example, a min and max value.

E.g.,
"dim_x": {
    "min": 6,
    "max": 400,
    "default": 100
}

CATEGORICAL constraints define a list of tuples labelled "choices",
where each tuple represents one selectable option. The first element
in each tuple is the actual value to be set on the model, and the second
element is the human-readable name.

E.g.,
"copper_weight": {
    "choices": [
        (1, "1 oz"),
        (2, "2 oz")
    ],
    "default": 1
}
"""
from django.db import models

OPTIONS = {
    "numeric": {
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
    },

    "categorical": {
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
}
