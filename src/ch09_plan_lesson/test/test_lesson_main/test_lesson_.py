from pytest import raises as pytest_raises
from src.ch00_py.dict_toolbox import get_json_from_dict
from src.ch02_partner.partner import partnerunit_shop
from src.ch07_plan_logic.plan_main import get_default_rope, planunit_shop
from src.ch08_plan_atom.atom_main import planatom_shop
from src.ch09_plan_lesson._ref.ch09_semantic_types import FaceName, default_knot_if_None
from src.ch09_plan_lesson.delta import plandelta_shop
from src.ch09_plan_lesson.lesson_main import (
    LessonUnit,
    get_init_lesson_id_if_None,
    get_lessonunit_from_dict,
    init_lesson_id,
    lessonunit_shop,
)
from src.ch09_plan_lesson.test._util.ch09_examples import (
    get_atom_example_kegunit_sports,
    get_plandelta_sue_example,
)
from src.ref.keywords import Ch09Keywords as kw, ExampleStrs as exx


def test_FaceName_Exists():
    # ESTABLISH / WHEN / THEN
    assert FaceName() == ""
    assert FaceName("cuisine") == "cuisine"


def test_init_lesson_id_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert init_lesson_id() == 0


def test_get_init_lesson_id_if_None_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_init_lesson_id_if_None() == init_lesson_id()
    assert get_init_lesson_id_if_None(None) == init_lesson_id()
    assert get_init_lesson_id_if_None(1) == 1


def test_LessonUnit_Exists():
    # ESTABLISH / WHEN
    x_lessonunit = LessonUnit()

    # THEN
    assert not x_lessonunit.face_name
    assert not x_lessonunit.moment_rope
    assert not x_lessonunit.plan_name
    assert not x_lessonunit._lesson_id
    assert not x_lessonunit._plandelta
    assert not x_lessonunit._delta_start
    assert not x_lessonunit.lessons_dir
    assert not x_lessonunit.atoms_dir
    assert not x_lessonunit.spark_num


def test_lessonunit_shop_ReturnsObjEstablishWithEmptyArgs():
    # ESTABLISH

    # WHEN
    bob_lessonunit = lessonunit_shop(plan_name=exx.bob)

    # THEN
    assert not bob_lessonunit.face_name
    assert bob_lessonunit.moment_rope == get_default_rope()
    assert bob_lessonunit.plan_name == exx.bob
    assert bob_lessonunit._lesson_id == 0
    assert bob_lessonunit._plandelta == plandelta_shop()
    assert bob_lessonunit._delta_start == 0
    assert not bob_lessonunit.lessons_dir
    assert not bob_lessonunit.atoms_dir
    assert not bob_lessonunit.spark_num


def test_lessonunit_shop_ReturnsObjEstablishWithNonEmptyArgs():
    # ESTABLISH
    bob_lesson_id = 13
    bob_plandelta = get_plandelta_sue_example()
    bob_delta_start = 6
    bob_lessons_dir = "exampletext7"
    bob_atoms_dir = "exampletext9"
    amy45_str = "amy45"
    amy45_e5_spark_num = 5

    # WHEN
    bob_lessonunit = lessonunit_shop(
        face_name=exx.sue,
        plan_name=exx.bob,
        moment_rope=amy45_str,
        _lesson_id=bob_lesson_id,
        _plandelta=bob_plandelta,
        _delta_start=bob_delta_start,
        lessons_dir=bob_lessons_dir,
        atoms_dir=bob_atoms_dir,
        spark_num=amy45_e5_spark_num,
    )

    # THEN
    assert bob_lessonunit.face_name == exx.sue
    assert bob_lessonunit.plan_name == exx.bob
    assert bob_lessonunit.moment_rope == amy45_str
    assert bob_lessonunit._lesson_id == bob_lesson_id
    assert bob_lessonunit._plandelta == bob_plandelta
    assert bob_lessonunit._delta_start == bob_delta_start
    assert bob_lessonunit.lessons_dir == bob_lessons_dir
    assert bob_lessonunit.atoms_dir == bob_atoms_dir
    assert bob_lessonunit.spark_num == amy45_e5_spark_num


def test_lessonunit_shop_ReturnsObjEstablishWithSomeArgs_v1():
    # ESTABLISH

    # WHEN
    bob_lessonunit = lessonunit_shop(plan_name=exx.bob, face_name=exx.yao)

    # THEN
    assert bob_lessonunit.plan_name == exx.bob
    assert bob_lessonunit.face_name == exx.yao


def test_LessonUnit_set_face_SetsAttribute():
    # ESTABLISH
    bob_lessonunit = lessonunit_shop(plan_name=exx.bob)
    assert bob_lessonunit.face_name is None
    assert bob_lessonunit.face_name != exx.sue

    # WHEN
    bob_lessonunit.set_face(exx.sue)

    # THEN
    assert bob_lessonunit.face_name == exx.sue


def test_LessonUnit_del_face_SetsAttribute():
    # ESTABLISH
    bob_lessonunit = lessonunit_shop(plan_name=exx.bob)
    bob_lessonunit.set_face(exx.yao)
    assert bob_lessonunit.face_name == exx.yao

    # WHEN
    bob_lessonunit.del_face()

    # THEN
    assert bob_lessonunit.face_name != exx.yao
    assert bob_lessonunit.face_name is None


def test_LessonUnit_set_plandelta_SetsAttribute():
    # ESTABLISH
    bob_lessonunit = lessonunit_shop(plan_name=exx.bob)
    assert bob_lessonunit._plandelta == plandelta_shop()

    # WHEN
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(get_atom_example_kegunit_sports())
    bob_lessonunit.set_plandelta(x_plandelta)

    # THEN
    assert bob_lessonunit._plandelta == x_plandelta


def test_LessonUnit_set_delta_start_SetsAttribute():
    # ESTABLISH
    bob_lessonunit = lessonunit_shop(exx.bob)
    assert bob_lessonunit._delta_start == 0

    # WHEN
    x_delta_start = 11
    bob_lessonunit.set_delta_start(x_delta_start)

    # THEN
    assert bob_lessonunit._delta_start == x_delta_start


def test_LessonUnit_planatom_exists_ReturnsObj():
    # ESTABLISH
    x_plandelta = plandelta_shop()
    bob_lessonunit = lessonunit_shop(plan_name=exx.bob)
    bob_lessonunit.set_plandelta(x_plandelta)

    # WHEN
    sports_planatom = get_atom_example_kegunit_sports()

    # THEN
    assert bob_lessonunit.planatom_exists(sports_planatom) is False

    # WHEN
    x_plandelta.set_planatom(sports_planatom)
    bob_lessonunit.set_plandelta(x_plandelta)

    # THEN
    assert bob_lessonunit.planatom_exists(sports_planatom)


def test_LessonUnit_del_plandelta_SetsAttribute():
    # ESTABLISH
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(get_atom_example_kegunit_sports())
    bob_lessonunit = lessonunit_shop(plan_name=exx.bob, _plandelta=x_plandelta)
    assert bob_lessonunit._plandelta != plandelta_shop()
    assert bob_lessonunit._plandelta == x_plandelta

    # WHEN
    bob_lessonunit.del_plandelta()

    # THEN
    assert bob_lessonunit._plandelta == plandelta_shop()


def test_LessonUnit_get_step_dict_ReturnsObj_Simple():
    # ESTABLISH
    amy45_str = "amy45"
    amy45_e5_int = 5
    bob_lessonunit = lessonunit_shop(
        moment_rope=amy45_str, plan_name=exx.bob, spark_num=amy45_e5_int
    )
    bob_lessonunit.set_face(exx.sue)

    # WHEN
    x_dict = bob_lessonunit.get_step_dict()

    # THEN
    assert x_dict.get(kw.moment_rope) is not None
    assert x_dict.get(kw.moment_rope) == amy45_str
    assert x_dict.get(kw.plan_name) is not None
    assert x_dict.get(kw.plan_name) == exx.bob
    assert x_dict.get(kw.face_name) is not None
    assert x_dict.get(kw.face_name) == exx.sue
    assert x_dict.get(kw.spark_num) is not None
    assert x_dict.get(kw.spark_num) == amy45_e5_int

    delta_str = "delta"
    assert x_dict.get(delta_str) is not None
    assert x_dict.get(delta_str) == plandelta_shop().get_ordered_planatoms()
    assert x_dict.get(delta_str) == {}


def test_LessonUnit_get_step_dict_ReturnsObj_WithPlanDeltaPopulated():
    # ESTABLISH
    sue_plandelta = get_plandelta_sue_example()
    bob_lessonunit = lessonunit_shop(exx.bob, _plandelta=sue_plandelta)

    # WHEN
    x_dict = bob_lessonunit.get_step_dict()

    # THEN
    delta_str = "delta"
    assert x_dict.get(delta_str) is not None
    assert x_dict.get(delta_str) == sue_plandelta.get_ordered_planatoms()
    sue_planatoms_dict = x_dict.get(delta_str)
    print(f"{len(sue_plandelta.get_sorted_planatoms())=}")
    print(f"{sue_planatoms_dict.keys()=}")
    # print(f"{sue_planatoms_dict.get(0)=}")
    assert sue_planatoms_dict.get(2) is None
    assert sue_planatoms_dict.get(0) is not None
    assert sue_planatoms_dict.get(1) is not None


def test_LessonUnit_get_step_dict_ReturnsObj_delta_start():
    # ESTABLISH
    sue_plandelta = get_plandelta_sue_example()
    x_delta_start = 7
    bob_lessonunit = lessonunit_shop(
        exx.bob, _plandelta=sue_plandelta, _delta_start=x_delta_start
    )

    # WHEN
    step_dict = bob_lessonunit.get_step_dict()

    # THEN
    delta_str = "delta"
    assert step_dict.get(delta_str) is not None
    assert step_dict.get(delta_str) == sue_plandelta.get_ordered_planatoms(
        x_delta_start
    )
    sue_planatoms_dict = step_dict.get(delta_str)
    print(f"{len(sue_plandelta.get_sorted_planatoms())=}")
    print(f"{sue_planatoms_dict.keys()=}")
    # print(f"{sue_planatoms_dict.get(0)=}")
    assert sue_planatoms_dict.get(x_delta_start + 2) is None
    assert sue_planatoms_dict.get(x_delta_start + 0) is not None
    assert sue_planatoms_dict.get(x_delta_start + 1) is not None


def test_LessonUnit_get_serializable_step_dict_ReturnsObj_Simple():
    # ESTABLISH
    amy45_str = "amy45"
    amy45_e5_int = 5
    bob_lessonunit = lessonunit_shop(
        moment_rope=amy45_str, plan_name=exx.bob, spark_num=amy45_e5_int
    )
    bob_lessonunit.set_face(exx.sue)

    # WHEN
    total_dict = bob_lessonunit.get_serializable_step_dict()

    # THEN
    assert total_dict.get(kw.moment_rope) is not None
    assert total_dict.get(kw.moment_rope) == amy45_str
    assert total_dict.get(kw.plan_name) is not None
    assert total_dict.get(kw.plan_name) == exx.bob
    assert total_dict.get(kw.face_name) is not None
    assert total_dict.get(kw.face_name) == exx.sue
    assert total_dict.get(kw.spark_num) is not None
    assert total_dict.get(kw.spark_num) == amy45_e5_int
    delta_str = "delta"
    assert total_dict.get(delta_str) == {}


def test_LessonUnit_get_serializable_step_dict_ReturnsObj_Scenario0_WithPlanDeltaPopulated():
    # ESTABLISH
    sue_plandelta = get_plandelta_sue_example()
    bob_lessonunit = lessonunit_shop(exx.bob, _plandelta=sue_plandelta)

    # WHEN
    total_dict = bob_lessonunit.get_serializable_step_dict()

    # THEN
    print(f"{total_dict=}")
    delta_str = "delta"
    assert total_dict.get(delta_str) is not None
    assert total_dict.get(delta_str) == sue_plandelta.get_ordered_dict()


def test_LessonUnit_get_serializable_step_dict_ReturnsObj_Scenario1_WithPlanDeltaPopulated():
    # ESTABLISH
    sue_plandelta = get_plandelta_sue_example()
    bob_lessonunit = lessonunit_shop(exx.bob, _plandelta=sue_plandelta)

    # WHEN
    generated_dict = bob_lessonunit.get_serializable_step_dict()

    # THEN
    assert generated_dict
    print("generated_json")
    print(generated_dict)
    expected_json = """{
  "delta": {
    "0": {
      "crud": "DELETE", 
      "dimen": "plan_partnerunit", 
      "jkeys": {"partner_name": "Sue"}, 
      "jvalues": {}
    }, 
    "1": {
      "crud": "UPDATE", 
      "dimen": "planunit", 
      "jkeys": {}, 
      "jvalues": {"credor_respect": 77}
    }
  }, 
  "face_name": null, 
  "moment_rope": ";YY;", 
  "plan_name": "Bob", 
  "spark_num": null
}"""
    assert get_json_from_dict(generated_dict) == expected_json


def test_get_lessonunit_from_dict_ReturnsObj_WithPlanDeltaPopulated():
    # ESTABLISH
    sue_plandelta = get_plandelta_sue_example()
    bob_lessonunit = lessonunit_shop(exx.bob, _plandelta=sue_plandelta, spark_num=778)

    # WHEN
    generated_bob_lessonunit = get_lessonunit_from_dict(
        bob_lessonunit.get_serializable_step_dict()
    )

    # THEN
    assert generated_bob_lessonunit
    assert generated_bob_lessonunit.face_name == bob_lessonunit.face_name
    assert generated_bob_lessonunit.spark_num == bob_lessonunit.spark_num
    assert generated_bob_lessonunit.moment_rope == bob_lessonunit.moment_rope
    assert generated_bob_lessonunit._plandelta == bob_lessonunit._plandelta
    assert generated_bob_lessonunit == bob_lessonunit


def test_LessonUnit_get_delta_atom_numbers_ReturnsObj():
    # ESTABLISH
    sue_plandelta = get_plandelta_sue_example()
    x_delta_start = 7
    bob_lessonunit = lessonunit_shop(exx.bob)
    bob_lessonunit.set_plandelta(sue_plandelta)
    bob_lessonunit.set_delta_start(x_delta_start)
    bob_lessonunit.set_face(exx.yao)
    x_dict = bob_lessonunit.get_step_dict()

    # WHEN
    x_delta_atom_numbers = bob_lessonunit.get_delta_atom_numbers(x_dict)
    # THEN
    assert x_delta_atom_numbers == [x_delta_start, x_delta_start + 1]


def test_LessonUnit_get_deltametric_dict_ReturnsObj():
    # ESTABLISH
    spark5_int = 5550
    sue_plandelta = get_plandelta_sue_example()
    x_delta_start = 7
    bob_lessonunit = lessonunit_shop(exx.bob)
    bob_lessonunit.set_plandelta(sue_plandelta)
    bob_lessonunit.set_delta_start(x_delta_start)
    bob_lessonunit.set_face(exx.yao)
    bob_lessonunit.spark_num = spark5_int

    # WHEN
    x_dict = bob_lessonunit.get_deltametric_dict()

    # THEN
    assert x_dict.get(kw.plan_name) is not None
    assert x_dict.get(kw.plan_name) == exx.bob
    assert x_dict.get(kw.face_name) is not None
    assert x_dict.get(kw.face_name) == exx.yao
    assert x_dict.get(kw.spark_num) is not None
    assert x_dict.get(kw.spark_num) == spark5_int

    delta_atom_numbers_str = "delta_atom_numbers"
    assert x_dict.get(delta_atom_numbers_str) is not None
    assert x_dict.get(delta_atom_numbers_str) == [7, 8]

    delta_min_str = "delta_min"
    assert x_dict.get(delta_min_str) is None
    delta_max_str = "delta_max"
    assert x_dict.get(delta_max_str) is None


def test_LessonUnit_add_p_planatom_Sets_PlanUnit_partnerunits():
    # ESTABLISH
    bob_lessonunit = lessonunit_shop(exx.bob)
    bob_partner_cred_lumen = 55
    bob_partner_debt_lumen = 66
    bob_partnerunit = partnerunit_shop(
        exx.bob, bob_partner_cred_lumen, bob_partner_debt_lumen
    )
    cw_str = kw.partner_cred_lumen
    dw_str = kw.partner_debt_lumen
    print(f"{bob_partnerunit.to_dict()=}")
    bob_required_dict = {
        kw.partner_name: bob_partnerunit.to_dict().get(kw.partner_name)
    }
    bob_optional_dict = {cw_str: bob_partnerunit.to_dict().get(cw_str)}
    bob_optional_dict[dw_str] = bob_partnerunit.to_dict().get(dw_str)
    print(f"{bob_required_dict=}")
    assert bob_lessonunit._plandelta.planatoms == {}

    # WHEN
    bob_lessonunit.add_p_planatom(
        dimen=kw.plan_partnerunit,
        crud_str=kw.INSERT,
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )

    # THEN
    assert len(bob_lessonunit._plandelta.planatoms) == 1
    assert (
        bob_lessonunit._plandelta.planatoms.get(kw.INSERT)
        .get(kw.plan_partnerunit)
        .get(exx.bob)
        is not None
    )


def test_LessonUnit_get_edited_plan_ReturnsObj_PlanUnit_insert_partner():
    # ESTABLISH
    sue_lessonunit = lessonunit_shop(exx.sue)

    before_sue_planunit = planunit_shop(exx.sue)
    before_sue_planunit.add_partnerunit(exx.yao)
    assert before_sue_planunit.partner_exists(exx.yao)
    assert before_sue_planunit.partner_exists(exx.zia) is False
    dimen = kw.plan_partnerunit
    x_planatom = planatom_shop(dimen, kw.INSERT)
    x_planatom.set_jkey(kw.partner_name, exx.zia)
    x_partner_cred_lumen = 55
    x_partner_debt_lumen = 66
    x_planatom.set_jvalue("partner_cred_lumen", x_partner_cred_lumen)
    x_planatom.set_jvalue("partner_debt_lumen", x_partner_debt_lumen)
    sue_lessonunit._plandelta.set_planatom(x_planatom)
    print(f"{sue_lessonunit._plandelta.planatoms.keys()=}")

    # WHEN
    after_sue_planunit = sue_lessonunit.get_lesson_edited_plan(before_sue_planunit)

    # THEN
    yao_partnerunit = after_sue_planunit.get_partner(exx.yao)
    zia_partnerunit = after_sue_planunit.get_partner(exx.zia)
    assert yao_partnerunit is not None
    assert zia_partnerunit is not None
    assert zia_partnerunit.partner_cred_lumen == x_partner_cred_lumen
    assert zia_partnerunit.partner_debt_lumen == x_partner_debt_lumen


def test_LessonUnit_get_edited_plan_RaisesErrorWhenlessonAttrsAndPlanAttrsAreNotTheSame():
    # ESTABLISH
    xia_str = "Xia"
    bob_lessonunit = lessonunit_shop(exx.yao, xia_str, moment_rope=exx.a23)
    before_sue_planunit = planunit_shop(exx.sue, moment_rope=exx.a23)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        bob_lessonunit.get_lesson_edited_plan(before_sue_planunit)
    assertion_failure_str = f"lesson plan conflict {exx.a23} != {exx.a23} or Yao != Sue"
    assert str(excinfo.value) == assertion_failure_str


def test_LessonUnit_is_empty_ReturnsObj():
    # ESTABLISH
    bob_lessonunit = lessonunit_shop(exx.bob)
    bob_partner_cred_lumen = 55
    bob_partner_debt_lumen = 66
    bob_partnerunit = partnerunit_shop(
        exx.bob, bob_partner_cred_lumen, bob_partner_debt_lumen
    )
    cw_str = kw.partner_cred_lumen
    dw_str = kw.partner_debt_lumen
    print(f"{bob_partnerunit.to_dict()=}")
    bob_required_dict = {
        kw.partner_name: bob_partnerunit.to_dict().get(kw.partner_name)
    }
    bob_optional_dict = {cw_str: bob_partnerunit.to_dict().get(cw_str)}
    bob_optional_dict[dw_str] = bob_partnerunit.to_dict().get(dw_str)
    print(f"{bob_required_dict=}")
    assert bob_lessonunit._plandelta.planatoms == {}
    assert bob_lessonunit.is_empty()

    # WHEN
    bob_lessonunit.add_p_planatom(
        dimen=kw.plan_partnerunit,
        crud_str=kw.INSERT,
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )

    # THEN
    assert len(bob_lessonunit._plandelta.planatoms) == 1
    assert bob_lessonunit.is_empty() is False

    # WHEN
    bob_lessonunit._plandelta.planatoms = {}

    # THEN
    assert bob_lessonunit.is_empty()

    # Test for UPDATE_str operation
    bob_lessonunit_update = lessonunit_shop(exx.bob)
    bob_lessonunit_update.add_p_planatom(
        dimen=kw.plan_partnerunit,
        crud_str=kw.UPDATE,
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )
    assert len(bob_lessonunit_update._plandelta.planatoms) == 1
    assert bob_lessonunit_update.is_empty() is False

    # Test for DELETE_str operation
    bob_lessonunit_delete = lessonunit_shop(exx.bob)
    bob_lessonunit_delete.add_p_planatom(
        dimen=kw.plan_partnerunit,
        crud_str=kw.DELETE,
        jkeys=bob_required_dict,
        jvalues={},
    )
    assert len(bob_lessonunit_delete._plandelta.planatoms) == 1
    assert bob_lessonunit_delete.is_empty() is False
