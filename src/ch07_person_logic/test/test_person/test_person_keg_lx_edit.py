from pytest import raises as pytest_raises
from src.ch06_keg.keg import kegunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ch07_person_logic.test._util.ch07_examples import (
    get_personunit_with_4_levels_and_2reasons_2facts,
)
from src.ref.keywords import ExampleStrs as exx


def test_PersonUnit_edit_keg_label_FailsWhenKegDoesNotExist():
    # ESTABLISH
    yao_person = personunit_shop("Yao")

    casa_rope = yao_person.make_l1_rope(exx.casa)
    yao_person.set_l1_keg(kegunit_shop(exx.casa))
    yao_person.set_keg_obj(kegunit_shop(exx.swim), parent_rope=casa_rope)

    # WHEN / THEN
    no_keg_rope = yao_person.make_l1_rope("bees")
    with pytest_raises(Exception) as excinfo:
        yao_person.edit_keg_label(old_rope=no_keg_rope, new_keg_label="birds")
    assert str(excinfo.value) == f"Keg old_rope='{no_keg_rope}' does not exist"


def test_PersonUnit_find_replace_rope_Modifies_kids_Scenario1():
    # ESTABLISH Keg with kids that will be different
    yao_person = personunit_shop(exx.yao)

    casa_old_str = "casa"
    old_casa_rope = yao_person.make_l1_rope(casa_old_str)
    bloomers_str = "bloomers"
    old_bloomers_rope = yao_person.make_rope(old_casa_rope, bloomers_str)
    tulips_str = "tulips"
    old_tulips_rope = yao_person.make_rope(old_bloomers_rope, tulips_str)
    old_red_rope = yao_person.make_rope(old_tulips_rope, exx.red)

    yao_person.set_l1_keg(kegunit_shop(casa_old_str))
    yao_person.set_keg_obj(kegunit_shop(bloomers_str), parent_rope=old_casa_rope)
    yao_person.set_keg_obj(kegunit_shop(tulips_str), parent_rope=old_bloomers_rope)
    yao_person.set_keg_obj(kegunit_shop(exx.red), parent_rope=old_tulips_rope)
    r_keg_tulips = yao_person.get_keg_obj(old_tulips_rope)
    r_keg_bloomers = yao_person.get_keg_obj(old_bloomers_rope)

    assert r_keg_bloomers.kids.get(tulips_str)
    assert r_keg_tulips.parent_rope == old_bloomers_rope
    assert r_keg_tulips.kids.get(exx.red)
    r_keg_red = r_keg_tulips.kids.get(exx.red)
    assert r_keg_red.parent_rope == old_tulips_rope

    # WHEN
    new_casa_str = "casita"
    new_casa_rope = yao_person.make_l1_rope(new_casa_str)
    yao_person.edit_keg_label(old_rope=old_casa_rope, new_keg_label=new_casa_str)

    # THEN
    assert yao_person.kegroot.kids.get(new_casa_str) is not None
    assert yao_person.kegroot.kids.get(casa_old_str) is None

    assert r_keg_bloomers.parent_rope == new_casa_rope
    assert r_keg_bloomers.kids.get(tulips_str) is not None

    r_keg_tulips = r_keg_bloomers.kids.get(tulips_str)
    new_bloomers_rope = yao_person.make_rope(new_casa_rope, bloomers_str)
    assert r_keg_tulips.parent_rope == new_bloomers_rope
    assert r_keg_tulips.kids.get(exx.red) is not None
    r_keg_red = r_keg_tulips.kids.get(exx.red)
    new_tulips_rope = yao_person.make_rope(new_bloomers_rope, tulips_str)
    assert r_keg_red.parent_rope == new_tulips_rope


def test_person_edit_keg_label_Modifies_factunits():
    # ESTABLISH person with factunits that will be different
    yao_person = personunit_shop(exx.yao)

    casa_rope = yao_person.make_l1_rope(exx.casa)
    bloomers_str = "bloomers"
    bloomers_rope = yao_person.make_rope(casa_rope, bloomers_str)
    tulips_str = "tulips"
    tulips_rope = yao_person.make_rope(bloomers_rope, tulips_str)
    old_water_str = "water"
    old_water_rope = yao_person.make_l1_rope(old_water_str)
    rain_str = "rain"
    old_rain_rope = yao_person.make_rope(old_water_rope, rain_str)

    yao_person.set_l1_keg(kegunit_shop(exx.casa))
    yao_person.set_keg_obj(kegunit_shop(tulips_str), parent_rope=bloomers_rope)
    yao_person.set_keg_obj(kegunit_shop(rain_str), parent_rope=old_water_rope)
    yao_person.add_fact(fact_context=old_water_rope, fact_state=old_rain_rope)

    keg_x = yao_person.get_keg_obj(tulips_rope)
    assert yao_person.kegroot.factunits[old_water_rope] is not None
    old_water_rain_factunit = yao_person.kegroot.factunits[old_water_rope]
    assert old_water_rain_factunit.fact_context == old_water_rope
    assert old_water_rain_factunit.fact_state == old_rain_rope

    # WHEN
    new_water_str = "h2o"
    new_water_rope = yao_person.make_l1_rope(new_water_str)
    yao_person.set_l1_keg(kegunit_shop(new_water_str))
    assert yao_person.kegroot.factunits.get(new_water_rope) is None
    yao_person.edit_keg_label(old_rope=old_water_rope, new_keg_label=new_water_str)

    # THEN
    assert yao_person.kegroot.factunits.get(old_water_rope) is None
    assert yao_person.kegroot.factunits.get(new_water_rope) is not None
    new_water_rain_factunit = yao_person.kegroot.factunits[new_water_rope]
    assert new_water_rain_factunit.fact_context == new_water_rope
    new_rain_rope = yao_person.make_rope(new_water_rope, rain_str)
    assert new_water_rain_factunit.fact_state == new_rain_rope

    assert yao_person.kegroot.factunits.get(new_water_rope)
    x_factunit = yao_person.kegroot.factunits.get(new_water_rope)
    # for factunit_key, x_factunit in yao_person.kegroot.factunits.items():
    #     assert factunit_key == new_water_rope
    assert x_factunit.fact_context == new_water_rope
    assert x_factunit.fact_state == new_rain_rope


def test_person_edit_keg_label_ModifiesKegReasonUnitsScenario1():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_person = get_personunit_with_4_levels_and_2reasons_2facts()
    old_sem_jour_str = "sem_jours"
    old_sem_jour_rope = sue_person.make_l1_rope(old_sem_jour_str)
    old_wed_rope = sue_person.make_rope(old_sem_jour_rope, exx.wed)
    casa_keg = sue_person.get_keg_obj(sue_person.make_l1_rope("casa"))
    # casa_wk_reason = reasonunit_shop(sem_jour, cases={wed_case.reason_state: wed_case})
    # nation_reason = reasonunit_shop(nation, cases={usa_case.reason_state: usa_case})
    assert len(casa_keg.reasonunits) == 2
    assert casa_keg.reasonunits.get(old_sem_jour_rope) is not None
    wed_keg = sue_person.get_keg_obj(old_sem_jour_rope)
    casa_sem_jour_reason = casa_keg.reasonunits.get(old_sem_jour_rope)
    assert casa_sem_jour_reason.cases.get(old_wed_rope) is not None
    assert casa_sem_jour_reason.cases.get(old_wed_rope).reason_state == old_wed_rope
    new_sem_jour_str = "jours des sem"
    new_sem_jour_rope = sue_person.make_l1_rope(new_sem_jour_str)
    new_wed_rope = sue_person.make_rope(new_sem_jour_rope, exx.wed)
    assert casa_keg.reasonunits.get(new_sem_jour_str) is None

    # WHEN
    # for key_x, x_reason in casa_keg.reasonunits.items():
    #     print(f"Before {key_x=} {x_reason.reason_context=}")
    print(f"before {wed_keg.keg_label=}")
    print(f"before {wed_keg.parent_rope=}")
    sue_person.edit_keg_label(
        old_rope=old_sem_jour_rope, new_keg_label=new_sem_jour_str
    )
    # for key_x, x_reason in casa_keg.reasonunits.items():
    #     print(f"after {key_x=} {x_reason.reason_context=}")
    print(f"after  {wed_keg.keg_label=}")
    print(f"after  {wed_keg.parent_rope=}")

    # THEN
    assert casa_keg.reasonunits.get(new_sem_jour_rope) is not None
    assert casa_keg.reasonunits.get(old_sem_jour_rope) is None
    casa_sem_jour_reason = casa_keg.reasonunits.get(new_sem_jour_rope)
    assert casa_sem_jour_reason.cases.get(new_wed_rope) is not None
    assert casa_sem_jour_reason.cases.get(new_wed_rope).reason_state == new_wed_rope
    assert len(casa_keg.reasonunits) == 2


def test_person_set_person_name_ModifiesBoth():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels_and_2reasons_2facts()
    assert sue_person.person_name == "Sue"
    # mid_keg_label1 = "Yao"
    # sue_person.edit_keg_label(old_rope=old_keg_label, new_keg_label=mid_keg_label1)
    # assert sue_person.person_name == old_keg_label
    # assert sue_person.kegroot.keg_label == mid_keg_label1

    # WHEN
    sue_person.set_person_name(new_person_name=exx.bob)

    # THEN
    assert sue_person.person_name == exx.bob


def test_person_edit_keg_label_RaisesErrorIfknotIsInLabel():
    # ESTABLISH
    sue_person = get_personunit_with_4_levels_and_2reasons_2facts()
    old_sem_jour_str = "sem_jours"
    old_sem_jour_rope = sue_person.make_l1_rope(old_sem_jour_str)

    # WHEN / THEN
    new_sem_jour_str = "jours; des wk"
    with pytest_raises(Exception) as excinfo:
        sue_person.edit_keg_label(
            old_rope=old_sem_jour_rope, new_keg_label=new_sem_jour_str
        )
    assert (
        str(excinfo.value)
        == f"Cannot modify '{old_sem_jour_rope}' because new_keg_label {new_sem_jour_str} contains knot {sue_person.knot}"
    )
