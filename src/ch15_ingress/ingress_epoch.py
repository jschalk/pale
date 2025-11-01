from dataclasses import dataclass
from src.ch01_py.dict_toolbox import (
    get_0_if_None,
    get_empty_dict_if_None,
    get_str_in_sub_dict,
    set_modular_dict_values,
)
from src.ch04_rope.rope import (
    create_rope,
    create_rope_from_labels,
    get_all_rope_labels,
    get_parent_rope,
    get_tail_label,
)
from src.ch15_ingress._ref.ch15_semantic_types import EpochTime, FaceName, SparkInt


@dataclass
class EpochIngress:
    face_name: FaceName = None
    spark_num: SparkInt = None
    # otx2inx dict key 'otx_epoch_length', key can be None is only inx_epoch_diff is given
    # otx2inx dict value 'inx_epoch_diff'
    otx2inx: dict[EpochTime, EpochTime] = None

    def set_all_otx2inx(self, otx2inx: dict[EpochTime, EpochTime]):
        self.otx2inx = set_modular_dict_values(get_empty_dict_if_None(otx2inx))

    def set_otx2inx(self, epoch_length: EpochTime, inx_epoch_diff: EpochTime):
        self.otx2inx[epoch_length] = inx_epoch_diff
        self.otx2inx = set_modular_dict_values(get_empty_dict_if_None(self.otx2inx))

    def get_inx_value(self, otx_epoch_length: EpochTime) -> EpochTime:
        return self.otx2inx.get(otx_epoch_length)

    def otx2inx_exists(
        self, epoch_length: EpochTime, inx_epoch_diff: EpochTime
    ) -> bool:
        return self.otx2inx.get(epoch_length) == inx_epoch_diff

    def otx_exists(self, epoch_length: EpochTime) -> bool:
        return self.otx2inx.get(epoch_length) != None

    def del_otx2inx(self, epoch_length: EpochTime):
        self.otx2inx.pop(epoch_length)

    def reveal_inx(
        self, otx_epoch_length: EpochTime, otx_value: EpochTime
    ) -> EpochTime:
        inx_epoch_diff = self.get_inx_value(otx_epoch_length)
        if inx_epoch_diff:
            otx_value += inx_epoch_diff
        otx_value = otx_value % otx_epoch_length
        return otx_value

    def to_dict(self) -> dict:
        """Returns seralizable dictionary"""
        return {
            "face_name": self.face_name,
            "spark_num": self.spark_num,
            "otx2inx": self.otx2inx,
        }


def epochingress_shop(
    face_name: FaceName,
    spark_num: SparkInt = None,
    otx2inx: dict[EpochTime, EpochTime] = None,
):
    x_epochingress = EpochIngress(
        face_name=face_name, spark_num=get_0_if_None(spark_num)
    )
    x_epochingress.set_all_otx2inx(otx2inx)
    return x_epochingress


def get_epochingress_from_dict(x_dict: dict) -> EpochIngress:
    return epochingress_shop(
        face_name=x_dict.get("face_name"),
        spark_num=x_dict.get("spark_num"),
        otx2inx=x_dict.get("otx2inx"),
    )


class inherit_epochingressException(Exception):
    pass


def inherit_epochingress(new: EpochIngress, old: EpochIngress):
    if new.face_name != old.face_name:
        exception_str = "Core attrs in conflict"
        raise inherit_epochingressException(exception_str)
    if new.spark_num <= old.spark_num:
        exception_str = "older EpochIngress is not older"
        raise inherit_epochingressException(exception_str)
    for otx_epoch_length, inx_epoch_diff in old.otx2inx.items():
        if not new.otx_exists(otx_epoch_length):
            new.set_otx2inx(otx_epoch_length, inx_epoch_diff)
