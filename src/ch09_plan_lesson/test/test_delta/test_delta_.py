from pytest import raises as pytest_raises
from src.ch03_person.person import personunit_shop
from src.ch04_rope.rope import create_rope, to_rope
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch08_plan_atom.atom_main import planatom_shop
from src.ch09_plan_lesson.delta import (
    PlanDelta,
    get_plandelta_from_ordered_dict,
    plan_built_from_delta_is_valid,
    plandelta_shop,
)
from src.ch09_plan_lesson.test._util.ch09_examples import get_plandelta_example1
from src.ref.keywords import Ch09Keywords as kw, ExampleStrs as exx


def test_PlanDelta_Exists():
    # ESTABLISH / WHEN
    x_plandelta = PlanDelta()

    # THEN
    assert x_plandelta.planatoms is None
    assert x_plandelta._plan_build_validated is None


def test_plandelta_shop_ReturnsObj():
    # ESTABLISH / WHEN
    ex1_plandelta = plandelta_shop()

    # THEN
    assert ex1_plandelta.planatoms == {}
    assert ex1_plandelta._plan_build_validated is False


def test_PlanDelta_set_planatom_Sets_PlanUnitSimpleAttrs():
    # ESTABLISH
    ex1_plandelta = plandelta_shop()
    attribute_value = 55
    dimen = kw.planunit
    opt1_arg = kw.tally
    jvalues = {opt1_arg: attribute_value}
    jkeys = {}
    plan_star_planatom = planatom_shop(
        dimen,
        kw.UPDATE,
        jkeys=jkeys,
        jvalues=jvalues,
    )
    assert ex1_plandelta.planatoms == {}
    assert plan_star_planatom.atom_order is None

    # WHEN
    ex1_plandelta.set_planatom(plan_star_planatom)

    # THEN
    assert len(ex1_plandelta.planatoms) == 1
    x_update_dict = ex1_plandelta.planatoms.get(kw.UPDATE)
    # print(f"{x_update_dict=}")
    x_dimen_planatom = x_update_dict.get(dimen)
    print(f"{x_dimen_planatom=}")
    assert x_dimen_planatom == plan_star_planatom
    assert plan_star_planatom.atom_order is not None


def test_PlanDelta_set_planatom_RaisesErrorWhen_is_valid_IsFalse():
    # ESTABLISH
    ex1_plandelta = plandelta_shop()
    x_dimen = kw.plan_personunit
    plan_star_planatom = planatom_shop(x_dimen, kw.UPDATE)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        ex1_plandelta.set_planatom(plan_star_planatom)

    # THEN
    exception_str = f"""'{x_dimen}' UPDATE PlanAtom is invalid
                x_planatom.is_jkeys_valid()=False
                x_planatom.is_jvalues_valid()=True"""
    assert str(excinfo.value) == exception_str


def test_ChangUnit_c_planatom_exists_ReturnsObj_plan_personunit_str():
    # ESTABLISH
    x_plandelta = plandelta_shop()
    bob_planatom = planatom_shop(kw.plan_personunit, kw.INSERT)
    bob_planatom.set_arg(kw.person_name, exx.bob)
    assert not x_plandelta.c_planatom_exists(bob_planatom)

    # WHEN
    x_plandelta.set_planatom(bob_planatom)

    # THEN
    assert x_plandelta.c_planatom_exists(bob_planatom)


def test_ChangUnit_c_planatom_exists_ReturnsObj_plan_person_membership_str():
    # ESTABLISH
    iowa_str = ";Iowa"
    x_plandelta = plandelta_shop()
    bob_iowa_planatom = planatom_shop(kw.plan_person_membership, kw.INSERT)
    bob_iowa_planatom.set_arg(kw.group_title, iowa_str)
    bob_iowa_planatom.set_arg(kw.person_name, exx.bob)
    assert not x_plandelta.c_planatom_exists(bob_iowa_planatom)

    # WHEN
    x_plandelta.set_planatom(bob_iowa_planatom)

    # THEN
    assert x_plandelta.c_planatom_exists(bob_iowa_planatom)


def test_PlanDelta_get_atom_ReturnsObj():
    # ESTABLISH
    ex1_plandelta = plandelta_shop()
    opt_arg1 = kw.tally
    opt_value = 55
    planunit_planatom = planatom_shop(kw.planunit, kw.UPDATE)
    planunit_planatom.set_jvalue(x_key=opt_arg1, x_value=opt_value)
    ex1_plandelta.set_planatom(planunit_planatom)

    # WHEN
    gen_planatom = ex1_plandelta.get_planatom(kw.UPDATE, dimen=kw.planunit, jkeys=[])

    # THEN
    assert gen_planatom == planunit_planatom


def test_PlanDelta_add_planatom_Sets_PlanUnitSimpleAttrs():
    # ESTABLISH
    ex1_plandelta = plandelta_shop()
    assert ex1_plandelta.planatoms == {}

    # WHEN
    op2_arg = kw.tally
    op2_value = 55
    jkeys = {}
    jvalues = {op2_arg: op2_value}
    ex1_plandelta.add_planatom(
        kw.planunit,
        kw.UPDATE,
        jkeys,
        jvalues=jvalues,
    )

    # THEN
    assert len(ex1_plandelta.planatoms) == 1
    x_update_dict = ex1_plandelta.planatoms.get(kw.UPDATE)
    x_planatom = x_update_dict.get(kw.planunit)
    assert x_planatom is not None
    assert x_planatom.dimen == kw.planunit


def test_PlanDelta_add_planatom_Sets_PlanUnit_personunits():
    # ESTABLISH
    ex1_plandelta = plandelta_shop()
    assert ex1_plandelta.planatoms == {}

    # WHEN
    bob_person_cred_lumen = 55
    bob_person_debt_lumen = 66
    bob_personunit = personunit_shop(
        exx.bob, bob_person_cred_lumen, bob_person_debt_lumen
    )
    cw_str = kw.person_cred_lumen
    dw_str = kw.person_debt_lumen
    print(f"{bob_personunit.to_dict()=}")
    bob_required_dict = {kw.person_name: bob_personunit.to_dict().get(kw.person_name)}
    bob_optional_dict = {cw_str: bob_personunit.to_dict().get(cw_str)}
    bob_optional_dict[dw_str] = bob_personunit.to_dict().get(dw_str)
    print(f"{bob_required_dict=}")
    personunit_str = kw.plan_personunit
    ex1_plandelta.add_planatom(
        dimen=personunit_str,
        crud_str=kw.INSERT,
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )
    # THEN
    assert len(ex1_plandelta.planatoms) == 1
    assert (
        ex1_plandelta.planatoms.get(kw.INSERT).get(personunit_str).get(exx.bob)
        is not None
    )


def test_PlanDelta_get_crud_planatoms_list_ReturnsObj():
    # ESTABLISH
    ex1_plandelta = get_plandelta_example1()
    assert len(ex1_plandelta.planatoms.get(kw.UPDATE).keys()) == 1
    assert ex1_plandelta.planatoms.get(kw.INSERT) is None
    assert len(ex1_plandelta.planatoms.get(kw.DELETE).keys()) == 1

    # WHEN
    sue_atom_order_dict = ex1_plandelta._get_crud_planatoms_list()

    # THEN
    assert len(sue_atom_order_dict) == 2
    print(f"{sue_atom_order_dict.keys()=}")
    # print(f"{sue_atom_order_dict.get(kw.UPDATE)=}")
    assert len(sue_atom_order_dict.get(kw.UPDATE)) == 1
    assert len(sue_atom_order_dict.get(kw.DELETE)) == 1
    # for crud_str, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_str=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.dimen=}")


def test_PlanDelta_get_dimen_sorted_planatoms_list_ReturnsObj_Scenario0_rope():
    # ESTABLISH
    ex1_plandelta = get_plandelta_example1()
    update_dict = ex1_plandelta.planatoms.get(kw.UPDATE)
    assert len(update_dict.keys()) == 1
    print(f"{update_dict.keys()=}")
    assert ex1_plandelta.planatoms.get(kw.INSERT) is None
    delete_dict = ex1_plandelta.planatoms.get(kw.DELETE)
    assert len(delete_dict.keys()) == 1

    # WHEN
    sue_atoms_list = ex1_plandelta.get_dimen_sorted_planatoms_list()

    # THEN
    assert len(sue_atoms_list) == 2
    assert sue_atoms_list[0] == update_dict.get(kw.planunit)
    z_atom = sue_atoms_list[1]
    print(f"{z_atom=}")
    print(delete_dict.get(kw.plan_personunit).keys())
    zia_personunit_delete = delete_dict.get(kw.plan_personunit).get("Zia")
    assert sue_atoms_list[1] == zia_personunit_delete


# def test_PlanDelta_add_planatom_Sets_PlanUnit_max_tree_traverse():
#     # ESTABLISH
#     ex1_plandelta = plandelta_shop(get_sue_rope())
#     assert ex1_plandelta.planatoms == {}

#     # WHEN
#     opt2_value = 55
#     dimen = kw.planunit
#     opt2_arg = kw.star
#     star_planatom = planatom_shop(dimen, kw.UPDATE)
#     star_planatom.set_jvalue(opt2_arg, opt2_value)
#     ex1_plandelta.set_planatom(star_planatom)
#     # THEN
#     assert len(ex1_plandelta.planatoms.get(kw.UPDATE).keys()) == 1
#     sue_planunit_dict = ex1_plandelta.planatoms.get(kw.UPDATE)
#     sue_star_planatom = sue_planunit_dict.get(dimen)
#     print(f"{sue_star_planatom=}")
#     assert star_planatom == sue_star_planatom

#     # WHEN
#     new2_value = 66
#     x_attribute = kw.max_tree_traverse
#     jkeys = {x_attribute: new2_value}
#     x_planatom = planatom_shop(x_attribute, kw.UPDATE, None, jkeys)
#     ex1_plandelta.set_planatom(x_planatom)
#     # THEN
#     print(f"{ex1_plandelta.planatoms.keys()=}")
#     print(f"{ex1_plandelta.planatoms.get(kw.UPDATE).keys()=}")
#     assert len(ex1_plandelta.planatoms.get(kw.UPDATE).keys()) == 2
#     assert x_planatom == ex1_plandelta.planatoms.get(kw.UPDATE).get(x_attribute)

#     # WHEN
#     new3_value = 77
#     x_attribute = kw.credor_respect
#     jkeys = {x_attribute: new3_value}
#     x_planatom = planatom_shop(x_attribute, kw.UPDATE, None, jkeys)
#     ex1_plandelta.set_planatom(x_planatom)
#     # THEN
#     assert len(ex1_plandelta.planatoms.get(kw.UPDATE).keys()) == 3
#     assert x_planatom == ex1_plandelta.planatoms.get(kw.UPDATE).get(x_attribute)

#     # WHEN
#     new4_value = 88
#     x_attribute = kw.debtor_respect
#     jkeys = {x_attribute: new4_value}
#     x_planatom = planatom_shop(x_attribute, kw.UPDATE, None, jkeys)
#     ex1_plandelta.set_planatom(x_planatom)
#     # THEN
#     assert len(ex1_plandelta.planatoms.get(kw.UPDATE).keys()) == 4
#     assert x_planatom == ex1_plandelta.planatoms.get(kw.UPDATE).get(x_attribute)


def test_PlanDelta_get_sorted_planatoms_ReturnsObj():
    # ESTABLISH
    ex1_plandelta = get_plandelta_example1()
    update_dict = ex1_plandelta.planatoms.get(kw.UPDATE)
    assert len(update_dict.keys()) == 1
    assert update_dict.get(kw.planunit) is not None
    print(f"atom_order 28 {ex1_plandelta.planatoms.get(kw.UPDATE).keys()=}")
    delete_dict = ex1_plandelta.planatoms.get(kw.DELETE)
    assert len(delete_dict.keys()) == 1
    assert delete_dict.get(kw.plan_personunit) is not None
    print(f"atom_order 26 {ex1_plandelta.planatoms.get(kw.DELETE).keys()=}")

    # WHEN
    sue_atom_order_list = ex1_plandelta.get_sorted_planatoms()

    # THEN
    assert len(sue_atom_order_list) == 2
    print(delete_dict.get(kw.plan_personunit).keys())
    zia_personunit_delete = delete_dict.get(kw.plan_personunit).get("Zia")
    # for planatom in sue_atom_order_list:
    #     print(f"{planatom.atom_order=}")
    assert sue_atom_order_list[0] == zia_personunit_delete
    assert sue_atom_order_list[1] == update_dict.get(kw.planunit)
    # for crud_str, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_str=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.dimen=}")


def test_PlanDelta_get_sorted_planatoms_ReturnsObj_KegUnitsSorted():
    # ESTABLISH
    x_moment_label = exx.a23
    root_rope = to_rope(x_moment_label)
    sports_str = "sports"
    sports_rope = create_rope(x_moment_label, sports_str)
    knee_str = "knee"
    knee_rope = create_rope(x_moment_label, knee_str)
    x_dimen = kw.plan_kegunit
    sports_insert_kegunit_planatom = planatom_shop(x_dimen, kw.INSERT)
    sports_insert_kegunit_planatom.set_jkey(kw.keg_rope, sports_rope)
    knee_insert_kegunit_planatom = planatom_shop(x_dimen, kw.INSERT)
    knee_insert_kegunit_planatom.set_jkey(kw.keg_rope, knee_rope)
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(knee_insert_kegunit_planatom)
    x_plandelta.set_planatom(sports_insert_kegunit_planatom)

    # WHEN
    x_atom_order_list = x_plandelta.get_sorted_planatoms()

    # THEN
    assert len(x_atom_order_list) == 2
    # for planatom in x_atom_order_list:
    #     print(f"{planatom.jkeys=}")
    assert x_atom_order_list[0] == knee_insert_kegunit_planatom
    assert x_atom_order_list[1] == sports_insert_kegunit_planatom
    # for crud_str, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_str=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.dimen=}")


def test_PlanDelta_get_sorted_planatoms_ReturnsObj_Rope_Sorted():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    x_moment_label = exx.a23
    sports_str = "sports"
    sports_rope = create_rope(x_moment_label, sports_str)
    knee_str = "knee"
    knee_rope = create_rope(sports_rope, knee_str)
    x_dimen = kw.plan_keg_awardunit
    swimmers_str = ",Swimmers"
    sports_awardunit_planatom = planatom_shop(x_dimen, kw.INSERT)
    sports_awardunit_planatom.set_jkey(kw.awardee_title, swimmers_str)
    sports_awardunit_planatom.set_jkey(kw.keg_rope, sports_rope)
    knee_awardunit_planatom = planatom_shop(x_dimen, kw.INSERT)
    knee_awardunit_planatom.set_jkey(kw.awardee_title, swimmers_str)
    knee_awardunit_planatom.set_jkey(kw.keg_rope, knee_rope)
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(knee_awardunit_planatom)
    x_plandelta.set_planatom(sports_awardunit_planatom)

    # WHEN
    x_atom_order_list = x_plandelta.get_sorted_planatoms()

    # THEN
    assert len(x_atom_order_list) == 2
    # for planatom in x_atom_order_list:
    #     print(f"{planatom.jkeys=}")
    assert x_atom_order_list[0] == sports_awardunit_planatom
    assert x_atom_order_list[1] == knee_awardunit_planatom
    # for crud_str, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_str=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.dimen=}")


def test_plan_built_from_delta_is_valid_ReturnsObjEstablishWithNoPlan_Scenario1():
    # ESTABLISH
    sue_plandelta = plandelta_shop()

    x_planatom = planatom_shop(kw.planunit, kw.UPDATE)
    x_attribute = kw.credor_respect
    x_planatom.set_jvalue(x_attribute, 100)
    sue_plandelta.set_planatom(x_planatom)

    dimen = kw.plan_personunit
    x_planatom = planatom_shop(dimen, kw.INSERT)
    x_planatom.set_arg(kw.person_name, exx.zia)
    x_planatom.set_arg(kw.person_cred_lumen, "70 is the number")
    sue_plandelta.set_planatom(x_planatom)
    print(f"{sue_plandelta=}")

    # WHEN / THEN
    assert plan_built_from_delta_is_valid(sue_plandelta) is False


def test_plan_built_from_delta_is_valid_ReturnsObjEstablishWithNoPlan_Scenario2():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_plandelta = plandelta_shop()
    dimen = kw.plan_personunit
    # WHEN
    x_planatom = planatom_shop(dimen, kw.INSERT)
    x_planatom.set_arg(kw.person_name, exx.yao)
    x_planatom.set_arg(kw.person_cred_lumen, 30)
    sue_plandelta.set_planatom(x_planatom)

    # THEN
    assert plan_built_from_delta_is_valid(sue_plandelta)

    # WHEN
    x_planatom = planatom_shop(dimen, kw.INSERT)
    x_planatom.set_arg(kw.person_name, exx.bob)
    x_planatom.set_arg(kw.person_cred_lumen, "70 is the number")
    sue_plandelta.set_planatom(x_planatom)

    # THEN
    assert plan_built_from_delta_is_valid(sue_plandelta) is False


def test_PlanDelta_get_ordered_planatoms_ReturnsObj_EstablishWithNoStartingNumber():
    # sourcery skip: extract-duplicate-method, inline-immediately-returned-variable, move-assign-in-block
    # ESTABLISH
    sue_plandelta = plandelta_shop()
    pool_planatom = planatom_shop(kw.planunit, kw.UPDATE)
    pool_attribute = kw.credor_respect
    pool_planatom.set_jvalue(pool_attribute, 100)
    sue_plandelta.set_planatom(pool_planatom)
    dimen = kw.plan_personunit
    zia_planatom = planatom_shop(dimen, kw.INSERT)
    zia_planatom.set_arg(kw.person_name, exx.zia)
    zia_planatom.set_arg(kw.person_cred_lumen, 70)
    sue_plandelta.set_planatom(zia_planatom)
    sue_plan = planunit_shop(exx.sue)
    sue_plan.set_credor_respect(100)
    yao_planatom = planatom_shop(dimen, kw.INSERT)
    yao_planatom.set_arg(kw.person_name, exx.yao)
    yao_planatom.set_arg(kw.person_cred_lumen, 30)
    sue_plandelta.set_planatom(yao_planatom)

    sue_plan = planunit_shop(exx.sue)
    assert plan_built_from_delta_is_valid(sue_plandelta, sue_plan)

    # WHEN
    plandelta_dict = sue_plandelta.get_ordered_planatoms()

    # THEN
    # delta_zia = plandelta_dict.get(0)
    # delta_yao = plandelta_dict.get(1)
    # delta_pool = plandelta_dict.get(2)
    # assert delta_zia == zia_planatom
    # assert delta_yao == yao_planatom
    # assert delta_pool == pool_planatom
    assert plandelta_dict.get(0) == zia_planatom
    assert plandelta_dict.get(1) == yao_planatom
    assert plandelta_dict.get(2) == pool_planatom


def test_PlanDelta_get_ordered_planatoms_ReturnsObj_EstablishWithStartingNumber():
    # sourcery skip: extract-duplicate-method, inline-immediately-returned-variable, move-assign-in-block
    # ESTABLISH
    sue_plandelta = plandelta_shop()
    pool_planatom = planatom_shop(kw.planunit, kw.UPDATE)
    pool_attribute = kw.credor_respect
    pool_planatom.set_jvalue(pool_attribute, 100)
    sue_plandelta.set_planatom(pool_planatom)
    dimen = kw.plan_personunit
    zia_planatom = planatom_shop(dimen, kw.INSERT)
    zia_planatom.set_arg(kw.person_name, exx.zia)
    zia_planatom.set_arg(kw.person_cred_lumen, 70)
    sue_plandelta.set_planatom(zia_planatom)
    sue_plan = planunit_shop(exx.sue)
    sue_plan.set_credor_respect(100)
    yao_planatom = planatom_shop(dimen, kw.INSERT)
    yao_planatom.set_arg(kw.person_name, exx.yao)
    yao_planatom.set_arg(kw.person_cred_lumen, 30)
    sue_plandelta.set_planatom(yao_planatom)

    sue_plan = planunit_shop(exx.sue)
    assert plan_built_from_delta_is_valid(sue_plandelta, sue_plan)

    # WHEN
    plandelta_dict = sue_plandelta.get_ordered_planatoms(5)

    # THEN
    # delta_zia = plandelta_dict.get(0)
    # delta_yao = plandelta_dict.get(1)
    # delta_pool = plandelta_dict.get(2)
    # assert delta_zia == zia_planatom
    # assert delta_yao == yao_planatom
    # assert delta_pool == pool_planatom
    assert plandelta_dict.get(5) == zia_planatom
    assert plandelta_dict.get(6) == yao_planatom
    assert plandelta_dict.get(7) == pool_planatom


def test_PlanDelta_get_ordered_dict_ReturnsObj_Scenario0_EstablishWithStartingNumber():
    # sourcery skip: extract-duplicate-method, inline-immediately-returned-variable, move-assign-in-block
    # ESTABLISH
    sue_plandelta = plandelta_shop()
    pool_planatom = planatom_shop(kw.planunit, kw.UPDATE)
    pool_attribute = kw.credor_respect
    pool_planatom.set_jvalue(pool_attribute, 100)
    sue_plandelta.set_planatom(pool_planatom)
    dimen = kw.plan_personunit
    zia_planatom = planatom_shop(dimen, kw.INSERT)
    zia_planatom.set_arg(kw.person_name, exx.zia)
    zia_planatom.set_arg(kw.person_cred_lumen, 70)
    sue_plandelta.set_planatom(zia_planatom)
    sue_plan = planunit_shop(exx.sue)
    sue_plan.set_credor_respect(100)
    yao_planatom = planatom_shop(dimen, kw.INSERT)
    yao_planatom.set_arg(kw.person_name, exx.yao)
    yao_planatom.set_arg(kw.person_cred_lumen, 30)
    sue_plandelta.set_planatom(yao_planatom)

    sue_plan = planunit_shop(exx.sue)
    assert plan_built_from_delta_is_valid(sue_plandelta, sue_plan)

    # WHEN
    plandelta_dict = sue_plandelta.get_ordered_dict(5)

    # THEN
    # delta_zia = plandelta_dict.get(0)
    # delta_yao = plandelta_dict.get(1)
    # delta_pool = plandelta_dict.get(2)
    # assert delta_zia == zia_planatom
    # assert delta_yao == yao_planatom
    # assert delta_pool == pool_planatom
    assert plandelta_dict.get(5) == zia_planatom.to_dict()
    assert plandelta_dict.get(6) == yao_planatom.to_dict()
    assert plandelta_dict.get(7) == pool_planatom.to_dict()


def test_PlanDelta_get_ordered_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_plandelta = plandelta_shop()
    pool_planatom = planatom_shop(kw.planunit, kw.UPDATE)
    pool_attribute = kw.credor_respect
    pool_planatom.set_jvalue(pool_attribute, 100)
    sue_plandelta.set_planatom(pool_planatom)
    dimen = kw.plan_personunit
    zia_planatom = planatom_shop(dimen, kw.INSERT)
    zia_planatom.set_arg(kw.person_name, exx.zia)
    zia_planatom.set_arg(kw.person_cred_lumen, 70)
    sue_plandelta.set_planatom(zia_planatom)
    yao_planatom = planatom_shop(dimen, kw.INSERT)
    yao_planatom.set_arg(kw.person_name, exx.yao)
    yao_planatom.set_arg(kw.person_cred_lumen, 30)
    sue_plandelta.set_planatom(yao_planatom)

    # WHEN
    delta_start_int = 5
    plandelta_ordered_dict = sue_plandelta.get_ordered_dict(delta_start_int)

    # THEN
    assert plandelta_ordered_dict


def test_get_plandelta_from_ordered_dict_ReturnsObj():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    expected_plandelta = plandelta_shop()
    pool_planatom = planatom_shop(kw.planunit, kw.UPDATE)
    pool_attribute = kw.credor_respect
    pool_planatom.set_jvalue(pool_attribute, 100)
    expected_plandelta.set_planatom(pool_planatom)
    dimen = kw.plan_personunit
    zia_planatom = planatom_shop(dimen, kw.INSERT)
    zia_planatom.set_arg(kw.person_name, exx.zia)
    zia_planatom.set_arg(kw.person_cred_lumen, 70)
    expected_plandelta.set_planatom(zia_planatom)
    sue_plan = planunit_shop(exx.sue)
    sue_plan.set_credor_respect(100)
    yao_planatom = planatom_shop(dimen, kw.INSERT)
    yao_planatom.set_arg(kw.person_name, exx.yao)
    yao_planatom.set_arg(kw.person_cred_lumen, 30)
    expected_plandelta.set_planatom(yao_planatom)
    plandelta_dict = expected_plandelta.get_ordered_dict(5)

    # WHEN
    generated_plandelta = get_plandelta_from_ordered_dict(plandelta_dict)

    # THEN
    # delta_zia = plandelta_dict.get(0)
    # delta_yao = plandelta_dict.get(1)
    # delta_pool = plandelta_dict.get(2)
    # assert delta_zia == zia_planatom
    # assert delta_yao == yao_planatom
    # assert delta_pool == pool_planatom
    # assert plandelta_dict.get(5) == zia_planatom.to_dict()
    # assert plandelta_dict.get(6) == yao_planatom.to_dict()
    # assert plandelta_dict.get(7) == pool_planatom.to_dict()
    assert generated_plandelta == expected_plandelta


def test_PlanDelta_c_planatom_exists_ReturnsObj():
    # ESTABLISH
    x_plandelta = plandelta_shop()

    # WHEN / THEN
    dimen = kw.plan_personunit
    zia_planatom = planatom_shop(dimen, kw.INSERT)
    zia_planatom.set_arg(kw.person_name, exx.zia)
    zia_planatom.set_arg(kw.person_cred_lumen, 70)
    assert x_plandelta.c_planatom_exists(zia_planatom) is False

    # WHEN
    x_plandelta.set_planatom(zia_planatom)

    # THEN
    assert x_plandelta.c_planatom_exists(zia_planatom)


def test_PlanDelta_is_empty_ReturnsObj():
    # ESTABLISH
    x_plandelta = plandelta_shop()

    # WHEN / THEN
    dimen = kw.plan_personunit
    zia_planatom = planatom_shop(dimen, kw.INSERT)
    zia_planatom.set_arg(kw.person_name, exx.zia)
    zia_planatom.set_arg(kw.person_cred_lumen, 70)
    assert x_plandelta.atoms_empty()

    # WHEN
    x_plandelta.set_planatom(zia_planatom)

    # THEN
    assert x_plandelta.atoms_empty() is False
