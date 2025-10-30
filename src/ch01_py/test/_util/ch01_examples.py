from enum import Enum
from src.ch01_py.file_toolbox import open_json


class CommonExampleStrs(str, Enum):
    bob = "Bob"
    sue = "Sue"
    SueZia = "SueZia"
    yao = "Yao"
    xio = "Xio"
    zia = "Zia"
    SueAndZia = "SueAndZia"
    casa = "casa"
    clean_str = "clean"
    dirtyness_str = "dirtyness"
    mop_str = "mop"
    slash_str = "/"
    swim = "swim"
    wk_str = "wk"
    wed_str = "Wed"

    def __str__(self):
        return self.value
