from inspect import getdoc as inspect_getdoc
from platform import system as platform_system
from src.ch00_py.file_toolbox import create_path
from src.ch11_bud._ref.ch11_path import (
    BUDUNIT_FILENAME,
    CELL_MANDATE_FILENAME,
    CELLNODE_FILENAME,
    MOMENT_FILENAME,
    PLANSPARK_FILENAME,
    PLANTIME_FILENAME,
    SPARK_ALL_LESSON_FILENAME,
    SPARK_EXPRESSED_LESSON_FILENAME,
    create_bud_dir_path,
    create_buds_dir_path,
    create_budunit_json_path,
    create_cell_dir_path,
    create_cell_json_path,
    create_cell_person_mandate_ledger_path,
    create_plan_spark_dir_path,
    create_planspark_path,
    create_plantime_path,
    create_spark_all_lesson_path,
    create_spark_expressed_lesson_path,
)
from src.ch11_bud.test._util.ch11_env import get_temp_dir
from src.ref.keywords import Ch11Keywords as kw, ExampleStrs as exx


def test_create_buds_dir_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()

    # WHEN
    buds_dir = create_buds_dir_path(x_moment_mstr_dir, exx.a23, exx.sue)

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    amy23_dir = create_path(x_moments_dir, exx.a23)
    plans_dir = create_path(amy23_dir, "plans")
    sue_dir = create_path(plans_dir, exx.sue)
    expected_buds_dir = create_path(sue_dir, "buds")
    assert buds_dir == expected_buds_dir


def test_create_bud_dir_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    epochtime7 = 7

    # WHEN
    generated_epochtime_dir = create_bud_dir_path(
        x_moment_mstr_dir, exx.a23, exx.sue, epochtime7
    )

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    amy23_dir = create_path(x_moments_dir, exx.a23)
    plans_dir = create_path(amy23_dir, "plans")
    sue_dir = create_path(plans_dir, exx.sue)
    buds_dir = create_path(sue_dir, "buds")
    expected_epochtime_dir = create_path(buds_dir, epochtime7)
    assert generated_epochtime_dir == expected_epochtime_dir


def test_create_budunit_json_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    epochtime7 = 7

    # WHEN
    gen_bud_path = create_budunit_json_path(
        x_moment_mstr_dir, exx.a23, exx.sue, epochtime7
    )

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    amy23_dir = create_path(x_moments_dir, exx.a23)
    plans_dir = create_path(amy23_dir, "plans")
    sue_dir = create_path(plans_dir, exx.sue)
    buds_dir = create_path(sue_dir, "buds")
    epochtime_dir = create_path(buds_dir, epochtime7)
    expected_bud_path_dir = create_path(epochtime_dir, BUDUNIT_FILENAME)
    assert gen_bud_path == expected_bud_path_dir


def test_create_plantime_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    epochtime7 = 7

    # WHEN
    gen_plantime_path = create_plantime_path(
        x_moment_mstr_dir, exx.a23, exx.sue, epochtime7
    )

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    amy23_dir = create_path(x_moments_dir, exx.a23)
    plans_dir = create_path(amy23_dir, "plans")
    sue_dir = create_path(plans_dir, exx.sue)
    buds_dir = create_path(sue_dir, "buds")
    epochtime_dir = create_path(buds_dir, epochtime7)
    expected_plantime_path_dir = create_path(epochtime_dir, PLANTIME_FILENAME)
    assert gen_plantime_path == expected_plantime_path_dir


def test_create_cell_dir_path_ReturnsObj_Scenario0_No_bud_ancestors():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    tp7 = 7

    # WHEN
    gen_cell_dir = create_cell_dir_path(x_moment_mstr_dir, exx.a23, exx.sue, tp7, [])

    # THEN
    epochtime_dir = create_bud_dir_path(x_moment_mstr_dir, exx.a23, exx.sue, tp7)
    assert gen_cell_dir == epochtime_dir


def test_create_cell_dir_path_ReturnsObj_Scenario1_One_bud_ancestors():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    tp7 = 7
    x_bud_ancestors = [exx.yao]

    # WHEN
    gen_cell_dir = create_cell_dir_path(
        x_moment_mstr_dir, exx.a23, exx.sue, tp7, bud_ancestors=x_bud_ancestors
    )

    # THEN
    epochtime_dir = create_bud_dir_path(x_moment_mstr_dir, exx.a23, exx.sue, tp7)
    tp_yao_dir = create_path(epochtime_dir, exx.yao)
    assert gen_cell_dir == tp_yao_dir


def test_create_cell_dir_path_ReturnsObj_Scenario2_Three_bud_ancestors():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    tp7 = 7
    x_bud_ancestors = [exx.yao, exx.bob, exx.zia]

    # WHEN
    gen_bud_celldepth_dir_path = create_cell_dir_path(
        x_moment_mstr_dir, exx.a23, exx.sue, tp7, bud_ancestors=x_bud_ancestors
    )

    # THEN
    epochtime_dir = create_bud_dir_path(x_moment_mstr_dir, exx.a23, exx.sue, tp7)
    tp_yao_dir = create_path(epochtime_dir, exx.yao)
    tp_yao_bob_dir = create_path(tp_yao_dir, exx.bob)
    expected_tp_yao_bob_zia_dir = create_path(tp_yao_bob_dir, exx.zia)
    assert gen_bud_celldepth_dir_path == expected_tp_yao_bob_zia_dir


def test_create_cell_json_path_ReturnsObj_Scenario0_Empty_bud_ancestors():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    epochtime7 = 7

    # WHEN
    gen_cell_json_path = create_cell_json_path(
        x_moment_mstr_dir, exx.a23, exx.sue, epochtime7
    )

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    amy23_dir = create_path(x_moments_dir, exx.a23)
    plans_dir = create_path(amy23_dir, "plans")
    sue_dir = create_path(plans_dir, exx.sue)
    buds_dir = create_path(sue_dir, "buds")
    epochtime_dir = create_path(buds_dir, epochtime7)
    expected_cell_json_path = create_path(epochtime_dir, CELLNODE_FILENAME)
    assert gen_cell_json_path == expected_cell_json_path


def test_create_cell_json_path_ReturnsObj_Scenario1_Three_bud_ancestors():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    tp7 = 7
    bud_ancestors = [exx.yao, exx.bob]

    # WHEN
    gen_cell_json_path = create_cell_json_path(
        x_moment_mstr_dir, exx.a23, exx.sue, tp7, bud_ancestors=bud_ancestors
    )

    # THEN
    epochtime_dir = create_bud_dir_path(x_moment_mstr_dir, exx.a23, exx.sue, tp7)
    tp_yao_dir = create_path(epochtime_dir, exx.yao)
    tp_yao_bob_dir = create_path(tp_yao_dir, exx.bob)
    expected_cell_json_path = create_path(tp_yao_bob_dir, CELLNODE_FILENAME)
    assert gen_cell_json_path == expected_cell_json_path


def test_create_cell_person_mandate_ledger_path_ReturnsObj_Scenario1_Three_bud_ancestors():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    tp7 = 7
    bud_ancestors = [exx.yao, exx.bob]

    # WHEN
    gen_cell_json_path = create_cell_person_mandate_ledger_path(
        x_moment_mstr_dir, exx.a23, exx.sue, tp7, bud_ancestors=bud_ancestors
    )

    # THEN
    epochtime_dir = create_bud_dir_path(x_moment_mstr_dir, exx.a23, exx.sue, tp7)
    tp_yao_dir = create_path(epochtime_dir, exx.yao)
    tp_yao_bob_dir = create_path(tp_yao_dir, exx.bob)
    expected_cell_json_path = create_path(tp_yao_bob_dir, CELL_MANDATE_FILENAME)
    assert gen_cell_json_path == expected_cell_json_path


def test_create_plan_spark_dir_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    spark3 = 3

    # WHEN
    gen_a23_e3_dir_path = create_plan_spark_dir_path(
        x_moment_mstr_dir, exx.a23, exx.bob, spark3
    )

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    a23_dir = create_path(x_moments_dir, exx.a23)
    a23_plans_dir = create_path(a23_dir, "plans")
    a23_bob_dir = create_path(a23_plans_dir, exx.bob)
    a23_sparks_dir = create_path(a23_bob_dir, "sparks")
    expected_a23_bob_e3_dir = create_path(a23_sparks_dir, spark3)
    assert gen_a23_e3_dir_path == expected_a23_bob_e3_dir


def test_create_planspark_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    spark3 = 3

    # WHEN
    gen_a23_e3_plan_path = create_planspark_path(
        x_moment_mstr_dir, exx.a23, exx.bob, spark3
    )

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    a23_dir = create_path(x_moments_dir, exx.a23)
    a23_plans_dir = create_path(a23_dir, "plans")
    a23_bob_dir = create_path(a23_plans_dir, exx.bob)
    a23_sparks_dir = create_path(a23_bob_dir, "sparks")
    a23_bob_e3_dir = create_path(a23_sparks_dir, spark3)
    expected_a23_bob_e3_plan_path = create_path(a23_bob_e3_dir, PLANSPARK_FILENAME)
    assert gen_a23_e3_plan_path == expected_a23_bob_e3_plan_path


def test_create_spark_all_lesson_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    spark3 = 3

    # WHEN
    gen_a23_e3_plan_path = create_spark_all_lesson_path(
        x_moment_mstr_dir, exx.a23, exx.bob, spark3
    )

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    a23_dir = create_path(x_moments_dir, exx.a23)
    a23_plans_dir = create_path(a23_dir, "plans")
    a23_bob_dir = create_path(a23_plans_dir, exx.bob)
    a23_sparks_dir = create_path(a23_bob_dir, "sparks")
    a23_bob_e3_dir = create_path(a23_sparks_dir, spark3)
    expected_a23_bob_e3_all_lesson_path = create_path(
        a23_bob_e3_dir, SPARK_ALL_LESSON_FILENAME
    )
    assert gen_a23_e3_plan_path == expected_a23_bob_e3_all_lesson_path


def test_create_spark_expressed_lesson_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    spark3 = 3

    # WHEN
    gen_a23_e3_plan_path = create_spark_expressed_lesson_path(
        x_moment_mstr_dir, exx.a23, exx.bob, spark3
    )

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    a23_dir = create_path(x_moments_dir, exx.a23)
    a23_plans_dir = create_path(a23_dir, "plans")
    a23_bob_dir = create_path(a23_plans_dir, exx.bob)
    a23_sparks_dir = create_path(a23_bob_dir, "sparks")
    a23_bob_e3_dir = create_path(a23_sparks_dir, spark3)
    expected_a23_bob_e3_expressed_lesson_path = create_path(
        a23_bob_e3_dir, SPARK_EXPRESSED_LESSON_FILENAME
    )
    assert gen_a23_e3_plan_path == expected_a23_bob_e3_expressed_lesson_path


LINUX_OS = platform_system() == "Linux"


def test_create_buds_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_buds_dir_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=kw.moment_label,
        plan_name=kw.plan_name,
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_buds_dir_path) == doc_str


def test_create_bud_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_bud_dir_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=kw.moment_label,
        plan_name=kw.plan_name,
        bud_time=kw.bud_time,
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_bud_dir_path) == doc_str


def test_create_cell_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_cell_dir_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=kw.moment_label,
        plan_name=kw.plan_name,
        bud_time=kw.bud_time,
        bud_ancestors=["ledger_plan1", "ledger_plan2", "ledger_plan3"],
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_cell_dir_path) == doc_str


def test_create_cell_json_path_HasDocString():
    # ESTABLISH
    doc_str = create_cell_json_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=kw.moment_label,
        plan_name=kw.plan_name,
        bud_time=kw.bud_time,
        bud_ancestors=["ledger_plan1", "ledger_plan2", "ledger_plan3"],
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_cell_json_path) == doc_str


def test_create_cell_person_mandate_ledger_path_HasDocString():
    # ESTABLISH
    doc_str = create_cell_person_mandate_ledger_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=kw.moment_label,
        plan_name=kw.plan_name,
        bud_time=kw.bud_time,
        bud_ancestors=["ledger_plan1", "ledger_plan2", "ledger_plan3"],
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_cell_person_mandate_ledger_path) == doc_str


def test_create_budunit_json_path_HasDocString():
    # ESTABLISH
    doc_str = create_budunit_json_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=kw.moment_label,
        plan_name=kw.plan_name,
        bud_time=kw.bud_time,
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_budunit_json_path) == doc_str


def test_create_plantime_path_HasDocString():
    # ESTABLISH
    doc_str = create_plantime_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=kw.moment_label,
        plan_name=kw.plan_name,
        bud_time=kw.bud_time,
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_plantime_path) == doc_str


def test_create_plan_spark_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_plan_spark_dir_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=kw.moment_label,
        plan_name=kw.plan_name,
        spark_num=kw.spark_num,
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_plan_spark_dir_path) == doc_str


def test_create_planspark_path_HasDocString():
    # ESTABLISH
    doc_str = create_planspark_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=kw.moment_label,
        plan_name=kw.plan_name,
        spark_num=kw.spark_num,
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_planspark_path) == doc_str


def test_create_spark_all_lesson_path_HasDocString():
    # ESTABLISH
    doc_str = create_spark_all_lesson_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=kw.moment_label,
        plan_name=kw.plan_name,
        spark_num=kw.spark_num,
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_spark_all_lesson_path) == doc_str


def test_create_spark_expressed_lesson_path_HasDocString():
    # ESTABLISH
    doc_str = create_spark_expressed_lesson_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=kw.moment_label,
        plan_name=kw.plan_name,
        spark_num=kw.spark_num,
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_spark_expressed_lesson_path) == doc_str
