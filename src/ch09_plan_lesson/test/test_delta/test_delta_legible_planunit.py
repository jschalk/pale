from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch08_plan_atom.atom_main import planatom_shop
from src.ch09_plan_lesson.delta import plandelta_shop
from src.ch09_plan_lesson.legible import create_legible_list
from src.ref.keywords import Ch09Keywords as kw


def test_create_legible_list_ReturnsObjEstablishWithEmptyPlanDelta():
    # ESTABLISH / WHEN
    x_plandelta = plandelta_shop()
    sue_plan = planunit_shop("Sue")

    # THEN
    assert create_legible_list(x_plandelta, sue_plan) == []


def test_create_legible_list_ReturnsObjEstablishWithPlanUpdate_credor_respect():
    # ESTABLISH
    dimen = kw.planunit
    credor_respect_int = 71
    credor_respect_planatom = planatom_shop(dimen, kw.UPDATE)
    credor_respect_planatom.set_arg(kw.credor_respect, credor_respect_int)

    print(f"{credor_respect_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(credor_respect_planatom)
    sue_plan = planunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"{sue_plan.plan_name}'s credor pool is now {credor_respect_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithPlanUpdate_debtor_respect():
    # ESTABLISH
    dimen = kw.planunit
    partner_debtor_pool_int = 78
    partner_debtor_pool_planatom = planatom_shop(dimen, kw.UPDATE)
    partner_debtor_pool_planatom.set_arg(kw.debtor_respect, partner_debtor_pool_int)

    print(f"{partner_debtor_pool_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(partner_debtor_pool_planatom)
    sue_plan = planunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"{sue_plan.plan_name}'s debtor pool is now {partner_debtor_pool_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithPlanUpdate_credor_respect_Equal_debtor_respect():
    # ESTABLISH
    x_plandelta = plandelta_shop()
    dimen = kw.planunit
    partner_pool_int = 83
    planunit_planatom = planatom_shop(dimen, kw.UPDATE)
    planunit_planatom.set_arg(kw.credor_respect, partner_pool_int)
    planunit_planatom.set_arg(kw.debtor_respect, partner_pool_int)
    x_plandelta.set_planatom(planunit_planatom)
    sue_plan = planunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"{sue_plan.plan_name}'s total pool is now {partner_pool_int}"
    assert len(legible_list) == 1
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithPlanUpdate_max_tree_traverse():
    # ESTABLISH
    dimen = kw.planunit
    max_tree_traverse_str = kw.max_tree_traverse
    max_tree_traverse_int = 71
    max_tree_traverse_planatom = planatom_shop(dimen, kw.UPDATE)
    max_tree_traverse_planatom.set_arg(max_tree_traverse_str, max_tree_traverse_int)

    print(f"{max_tree_traverse_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(max_tree_traverse_planatom)
    sue_plan = planunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"{sue_plan.plan_name}'s maximum number of Plan evaluations set to {max_tree_traverse_int}"
    assert legible_list[0] == x_str
