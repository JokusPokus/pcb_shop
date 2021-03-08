from django.db import models


# Constraints on the acceptable board dimensions.
# These might need to be updated according to JLCPCB's requirements.
MIN_DIM_X = 6
MAX_DIM_X = 400

MIN_DIM_Y = 6
MAX_DIM_Y = 500

# Maximum number of different designs
MAX_NUM_DESIGNS = 50


class Layer(models.model):
    LAYER_CHOICES = [
        (1, 1),
        (2, 2),
        (4, 4),
        (6, 6)
    ]
    DEFAULT_CHOICE = 2

    layerQuantity = models.IntegerField(
        choices=LAYER_CHOICES,
        default=DEFAULT_CHOICE
    )


class DeliveryFormat(models.model):
    pass


class Quantity(models.model):
    pass


class Thickness(models.model):
    pass


class Color(models.model):
    pass


class SurfaceFinish(models.model):
    pass


class CopperWeight(models.model):
    pass


class GoldFingers(models.model):
    pass


class Chamfered45(models.model):
    pass


class ConfirmProdFile(models.model):
    pass


class FlyingProbeTest(models.model):
    pass


class CastellatedHoles(models.model):
    pass


class RemoveOrderNum(models.model):
    pass
