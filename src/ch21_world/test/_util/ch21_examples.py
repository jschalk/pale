from pandas import DataFrame as pandas_DataFrame
from src.ch04_rope.rope import create_rope, create_rope_from_labels as init_rope
from src.ch07_person_logic.person_main import PersonUnit, personunit_shop
from src.ch13_time.epoch_main import add_epoch_planunit
from src.ref.keywords import Ch21Keywords as kw, ExampleStrs as exx


def br00013_example() -> pandas_DataFrame:
    """All rows valid. pledge=True throughout. Covers varied names."""

    h1_mop = init_rope(["herenow1", "family", exx.casa, exx.clean, exx.mop])
    h1_tools = init_rope(["herenow1", "family", exx.casa, exx.clean, exx.scrub])
    h7_mop = init_rope(["herenow7", "family", exx.casa, exx.clean, exx.mop])
    h7_grocery = init_rope(["herenow7", "family", exx.casa, exx.clean, "grocery"])
    h7_brush = init_rope(["herenow7", "family", exx.casa, exx.clean, "brush"])

    data = [
        (0, exx.sue, exx.zia, exx.hn1, h1_mop, 1, True),
        (0, exx.sue, exx.yao, exx.hn1, h1_tools, 2, True),
        (2, exx.yao, exx.yao, exx.hn7, h7_mop, 8, True),
        (3, exx.sue, exx.sue, exx.hn7, h7_grocery, 3, True),
        (4, exx.zia, exx.xio, exx.hn7, h7_brush, 1, True),
    ]
    cols = [
        kw.spark_num,
        kw.face_name,
        kw.person_name,
        kw.moment_rope,
        kw.plan_rope,
        kw.star,
        kw.pledge,
    ]
    return pandas_DataFrame(data, columns=cols)
