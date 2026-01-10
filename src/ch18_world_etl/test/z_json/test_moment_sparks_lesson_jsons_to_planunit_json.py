from os.path import exists as os_path_exists
from src.ch01_py.file_toolbox import create_path, open_json, save_json
from src.ch07_plan_logic.plan_main import get_planunit_from_dict, planunit_shop
from src.ch09_plan_lesson.lesson_main import get_lessonunit_from_dict, lessonunit_shop
from src.ch11_bud._ref.ch11_path import (
    create_plan_spark_dir_path,
    create_spark_all_lesson_path,
    create_spark_expressed_lesson_path,
)
from src.ch18_world_etl.etl_main import (
    etl_spark_lesson_json_to_spark_inherited_planunits,
)
from src.ch18_world_etl.test._util.ch18_env import get_temp_dir, temp_dir_setup
from src.ref.keywords import Ch18Keywords as kw, ExampleStrs as exx


def test_etl_spark_lesson_json_to_spark_inherited_planunits_SetsFiles_plan_json(
    temp_dir_setup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    yao_inx = "Yaoe"
    spark3 = 3
    spark7 = 7
    credit44 = 44
    credit77 = 77
    credit88 = 88
    moment_mstr_dir = get_temp_dir()
    a23_bob_e3_dir = create_plan_spark_dir_path(
        moment_mstr_dir, exx.a23, bob_inx, spark3
    )
    a23_bob_e7_dir = create_plan_spark_dir_path(
        moment_mstr_dir, exx.a23, bob_inx, spark7
    )
    a23_bob_e3_lesson = lessonunit_shop(bob_inx, None, exx.a23, spark_num=spark3)
    a23_bob_e7_lesson = lessonunit_shop(bob_inx, None, exx.a23, spark_num=spark7)
    plnvoce_dimen = kw.plan_voiceunit
    bob_jkeys = {kw.voice_name: bob_inx}
    bob_jvalues = {kw.voice_cred_lumen: credit77, kw.voice_debt_lumen: None}
    yao_jkeys = {kw.voice_name: yao_inx}
    yao_jvalues = {kw.voice_cred_lumen: credit44, kw.voice_debt_lumen: None}
    a23_bob_e3_lesson.add_p_planatom(plnvoce_dimen, kw.INSERT, bob_jkeys, bob_jvalues)
    a23_bob_e3_lesson.add_p_planatom(plnvoce_dimen, kw.INSERT, yao_jkeys, yao_jvalues)
    sue_jkeys = {kw.voice_name: sue_inx}
    sue_jvalues = {kw.voice_cred_lumen: credit88, kw.voice_debt_lumen: None}
    a23_bob_e7_lesson.add_p_planatom(plnvoce_dimen, kw.INSERT, bob_jkeys, bob_jvalues)
    a23_bob_e7_lesson.add_p_planatom(plnvoce_dimen, kw.INSERT, sue_jkeys, sue_jvalues)
    e3_all_lesson_path = create_spark_all_lesson_path(
        moment_mstr_dir, exx.a23, bob_inx, spark3
    )
    e7_all_lesson_path = create_spark_all_lesson_path(
        moment_mstr_dir, exx.a23, bob_inx, spark7
    )
    save_json(e3_all_lesson_path, None, a23_bob_e3_lesson.get_serializable_step_dict())
    save_json(e7_all_lesson_path, None, a23_bob_e7_lesson.get_serializable_step_dict())
    assert os_path_exists(e3_all_lesson_path)
    assert os_path_exists(e7_all_lesson_path)
    plan_filename = "plan.json"
    e3_plan_path = create_path(a23_bob_e3_dir, plan_filename)
    e7_plan_path = create_path(a23_bob_e7_dir, plan_filename)
    assert os_path_exists(e3_plan_path) is False
    assert os_path_exists(e7_plan_path) is False

    # WHEN
    etl_spark_lesson_json_to_spark_inherited_planunits(moment_mstr_dir)

    # THEN
    assert os_path_exists(e3_plan_path)
    assert os_path_exists(e7_plan_path)
    expected_e3_bob_plan = planunit_shop(bob_inx, exx.a23)
    expected_e7_bob_plan = planunit_shop(bob_inx, exx.a23)
    expected_e3_bob_plan.add_voiceunit(bob_inx, credit77)
    expected_e3_bob_plan.add_voiceunit(yao_inx, credit44)
    expected_e7_bob_plan.add_voiceunit(bob_inx, credit77)
    expected_e7_bob_plan.add_voiceunit(sue_inx, credit88)
    expected_e7_bob_plan.add_voiceunit(yao_inx, credit44)
    generated_e3_plan = get_planunit_from_dict(open_json(e3_plan_path))
    generated_e7_plan = get_planunit_from_dict(open_json(e7_plan_path))
    assert generated_e3_plan.voices == expected_e3_bob_plan.voices
    assert generated_e3_plan == expected_e3_bob_plan
    assert generated_e3_plan.to_dict() == expected_e3_bob_plan.to_dict()
    assert generated_e7_plan.voices == expected_e7_bob_plan.voices
    assert generated_e7_plan.to_dict() == expected_e7_bob_plan.to_dict()


def test_etl_spark_lesson_json_to_spark_inherited_planunits_SetsFiles_expressed_lesson(
    temp_dir_setup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    yao_inx = "Yaoe"
    xia_inx = "Xia"
    spark3 = 3
    spark7 = 7
    credit44 = 44
    credit77 = 77
    credit88 = 88
    moment_mstr_dir = get_temp_dir()
    a23_bob_e3_lesson = lessonunit_shop(bob_inx, xia_inx, exx.a23, spark_num=spark3)
    a23_bob_e7_lesson = lessonunit_shop(bob_inx, xia_inx, exx.a23, spark_num=spark7)
    plnvoce_dimen = kw.plan_voiceunit
    bob_jkeys = {kw.voice_name: bob_inx}
    bob_jvalues = {kw.voice_cred_lumen: credit77}
    yao_jkeys = {kw.voice_name: yao_inx}
    yao_jvalues = {kw.voice_cred_lumen: credit44}
    a23_bob_e3_lesson.add_p_planatom(plnvoce_dimen, kw.INSERT, bob_jkeys, bob_jvalues)
    a23_bob_e3_lesson.add_p_planatom(plnvoce_dimen, kw.INSERT, yao_jkeys, yao_jvalues)
    sue_jkeys = {kw.voice_name: sue_inx}
    sue_jvalues = {kw.voice_cred_lumen: credit88}
    a23_bob_e7_lesson.add_p_planatom(plnvoce_dimen, kw.INSERT, bob_jkeys, bob_jvalues)
    a23_bob_e7_lesson.add_p_planatom(plnvoce_dimen, kw.INSERT, sue_jkeys, sue_jvalues)
    a23_bob_e3_all_lesson_path = create_spark_all_lesson_path(
        moment_mstr_dir, exx.a23, bob_inx, spark3
    )
    a23_bob_e7_all_lesson_path = create_spark_all_lesson_path(
        moment_mstr_dir, exx.a23, bob_inx, spark7
    )
    save_json(
        a23_bob_e3_all_lesson_path, None, a23_bob_e3_lesson.get_serializable_step_dict()
    )
    save_json(
        a23_bob_e7_all_lesson_path, None, a23_bob_e7_lesson.get_serializable_step_dict()
    )
    e3_expressed_lesson_path = create_spark_expressed_lesson_path(
        moment_mstr_dir, exx.a23, bob_inx, spark3
    )
    e7_expressed_lesson_path = create_spark_expressed_lesson_path(
        moment_mstr_dir, exx.a23, bob_inx, spark7
    )
    assert os_path_exists(a23_bob_e3_all_lesson_path)
    assert os_path_exists(a23_bob_e7_all_lesson_path)
    assert os_path_exists(e3_expressed_lesson_path) is False
    assert os_path_exists(e7_expressed_lesson_path) is False

    # WHEN
    etl_spark_lesson_json_to_spark_inherited_planunits(moment_mstr_dir)

    # THEN
    assert os_path_exists(e3_expressed_lesson_path)
    assert os_path_exists(e7_expressed_lesson_path)
    gen_e3_express_lesson = get_lessonunit_from_dict(
        open_json(e3_expressed_lesson_path)
    )
    gen_e7_express_lesson = get_lessonunit_from_dict(
        open_json(e7_expressed_lesson_path)
    )
    expected_e3_bob_lesson = lessonunit_shop(
        bob_inx, xia_inx, exx.a23, spark_num=spark3
    )
    expected_e7_bob_lesson = lessonunit_shop(
        bob_inx, xia_inx, exx.a23, spark_num=spark7
    )
    expected_e3_bob_lesson.add_p_planatom(
        plnvoce_dimen, kw.INSERT, bob_jkeys, bob_jvalues
    )
    expected_e3_bob_lesson.add_p_planatom(
        plnvoce_dimen, kw.INSERT, yao_jkeys, yao_jvalues
    )
    expected_e7_bob_lesson.add_p_planatom(
        plnvoce_dimen, kw.INSERT, sue_jkeys, sue_jvalues
    )
    assert expected_e3_bob_lesson == a23_bob_e3_lesson
    assert expected_e7_bob_lesson._plandelta != a23_bob_e7_lesson._plandelta
    assert expected_e7_bob_lesson != a23_bob_e7_lesson
    # expected_e3_bob_lesson.add_p_planatom()
    # expected_e3_bob_lesson.add_p_planatom()
    # expected_e7_bob_lesson.add_p_planatom()
    # expected_e7_bob_lesson.add_p_planatom()
    # expected_e7_bob_lesson.add_p_planatom()
    assert gen_e3_express_lesson == expected_e3_bob_lesson
    gen_e7_express_delta = gen_e7_express_lesson._plandelta
    expected_e7_delta = expected_e7_bob_lesson._plandelta
    assert gen_e7_express_delta.planatoms == expected_e7_delta.planatoms
    assert gen_e7_express_lesson._plandelta == expected_e7_bob_lesson._plandelta
    assert gen_e7_express_lesson == expected_e7_bob_lesson
