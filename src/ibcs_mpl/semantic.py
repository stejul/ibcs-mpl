from ibcs_mpl.types import Impact


def impact_from_value(value: float) -> Impact:
    if value > 0:
        return Impact.POSITIVE
    if value < 0:
        return Impact.NEGATIVE
    return Impact.NEUTRAL
