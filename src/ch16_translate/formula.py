from copy import copy as copy_copy
from dataclasses import dataclass
from src.ch01_py.dict_toolbox import (
    get_0_if_None,
    get_empty_dict_if_None,
    get_str_in_sub_dict,
    str_in_all_dict_keys,
    str_in_all_dict_values,
    str_in_dict,
    str_in_dict_keys,
    str_in_dict_values,
)
from src.ch04_rope.rope import (
    create_rope,
    create_rope_from_labels,
    get_all_rope_labels,
    get_parent_rope,
    get_tail_label,
)
from src.ch16_translate._ref.ch16_semantic_types import (
    EpochTime,
    FaceName,
    KnotTerm,
    LabelTerm,
    RopeTerm,
    SparkInt,
    default_knot_if_None,
)
from src.ch16_translate.translate_config import default_unknown_str_if_None


@dataclass
class EpochFormula:
    face_name: FaceName = None
    spark_num: SparkInt = None
    otx_time: EpochTime = None
    inx_time: EpochTime = None
    epoch_length_min: EpochTime = None

    def get_inx_value(self, otx_value: EpochTime) -> EpochTime:
        difference = get_0_if_None(self.inx_time) - get_0_if_None(self.otx_time)
        return (otx_value + difference) % self.epoch_length_min

    def to_dict(self) -> dict:
        """Returns seralizable dictionary"""
        return {
            "face_name": self.face_name,
            "spark_num": self.spark_num,
            "inx_time": self.inx_time,
            "otx_time": self.otx_time,
        }


def epochformula_shop(
    face_name: FaceName,
    spark_num: SparkInt = None,
    otx_time: EpochTime = None,
    inx_time: EpochTime = None,
    epoch_length_min: EpochTime = None,
):
    if epoch_length_min is None:
        epoch_length_min = 1472657760
    if otx_time:
        otx_time = get_0_if_None(otx_time) % epoch_length_min
    if inx_time:
        inx_time = get_0_if_None(inx_time) % epoch_length_min
    return EpochFormula(
        face_name=face_name,
        spark_num=get_0_if_None(spark_num),
        otx_time=otx_time,
        inx_time=inx_time,
        epoch_length_min=epoch_length_min,
    )


def get_epochformula_from_dict(x_dict: dict) -> EpochFormula:
    return epochformula_shop(
        face_name=x_dict.get("face_name"),
        spark_num=x_dict.get("spark_num"),
        otx_time=x_dict.get("otx_time"),
        inx_time=x_dict.get("inx_time"),
    )


class inherit_epochformulaException(Exception):
    pass


def inherit_epochformula(new: EpochFormula, old: EpochFormula):
    if new.epoch_length_min != old.epoch_length_min or new.face_name != old.face_name:
        exception_str = "Core attrs in conflict"
        raise inherit_epochformulaException(exception_str)
    if old.spark_num >= new.spark_num:
        raise inherit_epochformulaException("older EpochFormula is not older")
    if new.otx_time is None and old.otx_time is not None:
        new.otx_time = old.otx_time
    if new.inx_time is None and old.inx_time is not None:
        new.inx_time = old.inx_time
