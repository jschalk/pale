from dataclasses import dataclass
from src.ch06_keg.keg import KegUnit


@dataclass
class RangeAttrHolder:
    begin: float = None
    close: float = None
    addin: float = None
    denom: int = None
    numor: int = None
    morph: bool = None
    gogo_want: float = None
    stop_want: float = None
    gogo_calc: float = None
    stop_calc: float = None


def get_range_attrs(x_keg: KegUnit) -> RangeAttrHolder:
    return RangeAttrHolder(
        begin=x_keg.begin,
        close=x_keg.close,
        addin=x_keg.addin,
        denom=x_keg.denom,
        numor=x_keg.numor,
        morph=x_keg.morph,
        gogo_want=x_keg.gogo_want,
        stop_want=x_keg.stop_want,
        gogo_calc=x_keg.gogo_calc,
        stop_calc=x_keg.stop_calc,
    )
