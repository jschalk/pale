from src.ch00_py.plotly_toolbox import conditional_fig_show
from src.ch07_plan_logic.plan_graphic import (
    display_kegtree,
    fund_graph0,
    get_plan_agenda_plotly_fig,
    get_plan_partners_plotly_fig,
)
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch07_plan_logic.test._util.ch07_examples import (
    get_planunit_laundry_example1,
    get_planunit_with_4_levels,
    get_planunit_with_4_levels_and_2reasons,
    get_planunit_x1_3levels_1reason_1facts,
    planunit_v001_with_large_agenda,
)
from src.ref.keywords import Ch07Keywords as kw, ExampleStrs as exx


def test_display_kegtree_Scenario0(graphics_bool):
    # ESTABLISH
    # a_plan = get_1label_plan()
    # a_plan = get_2label_plan()
    # a_plan = get_3label_plan()
    # a_plan = get_5labelHG_plan()
    # a_plan = get_7labelJroot_plan()
    a_plan = get_planunit_with_4_levels()
    # a_plan = planunit_v001()
    a_plan.cashout()
    print(f"Plan {a_plan.kegroot.keg_label}: Labels ({len(a_plan._keg_dict)})")

    # WHEN / THEN
    x_fig = display_kegtree(a_plan, graphics_bool)


def test_display_kegtree_Scenario1_shows_tasks(graphics_bool):
    # ESTABLISH
    # a_plan = get_1label_plan()
    # a_plan = get_2label_plan()
    # a_plan = get_3label_plan()
    # a_plan = get_5labelHG_plan()
    # a_plan = get_7labelJroot_plan()
    a_plan = get_planunit_laundry_example1()
    # a_plan = planunit_v001()
    a_plan.cashout()
    print(f"Plan {a_plan.kegroot.keg_label}: Labels ({len(a_plan._keg_dict)})")

    # WHEN / THEN
    display_kegtree(a_plan, mode=kw.task, graphics_bool=graphics_bool)


def test_get_plan_partners_plotly_fig_DisplaysInfo(graphics_bool):
    # ESTABLISH
    luca_plan = planunit_shop()
    luca_plan.set_credor_respect(500)
    luca_plan.set_debtor_respect(400)
    yao_partner_cred_lumen = 66
    yao_partner_debt_lumen = 77
    luca_plan.add_partnerunit(exx.yao, yao_partner_cred_lumen, yao_partner_debt_lumen)
    sue_partner_cred_lumen = 434
    sue_partner_debt_lumen = 323
    luca_plan.add_partnerunit(exx.sue, sue_partner_cred_lumen, sue_partner_debt_lumen)

    # WHEN
    x_fig = get_plan_partners_plotly_fig(luca_plan)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_plan_agenda_plotly_fig_DisplaysInfo(graphics_bool):
    # ESTABLISH
    yao_plan = planunit_v001_with_large_agenda()
    assert len(yao_plan.get_agenda_dict()) == 69

    # WHEN
    x_fig = get_plan_agenda_plotly_fig(yao_plan)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_PlanUnit_fund_flow(graphics_bool):
    # ESTABLISH
    sue_plan = planunit_shop(plan_name="Sue")
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    cat_str = "cat situation"
    cat_rope = sue_plan.make_rope(casa_rope, cat_str)
    hun_n_str = "not hungry"
    hun_n_rope = sue_plan.make_rope(cat_rope, hun_n_str)
    hun_y_str = "hungry"
    hun_y_rope = sue_plan.make_rope(cat_rope, hun_y_str)
    clean_str = "cleaning"
    clean_rope = sue_plan.make_rope(casa_rope, clean_str)
    sweep_str = "sweep floor"
    sweep_rope = sue_plan.make_rope(clean_rope, sweep_str)
    dish_str = "clean dishes"
    dish_rope = sue_plan.make_rope(clean_rope, dish_str)
    sue_plan.add_keg(casa_rope, star=30)
    sue_plan.add_keg(cat_rope, star=30)
    sue_plan.add_keg(hun_n_rope, star=30)
    sue_plan.add_keg(hun_y_rope, star=30)
    sue_plan.add_keg(clean_rope, star=30)
    sue_plan.add_keg(sweep_rope, star=30, pledge=True)
    sue_plan.add_keg(dish_rope, star=30, pledge=True)
    dinner_str = "cat have dinner"
    dinner_rope = sue_plan.make_l1_rope(dinner_str)
    sue_plan.add_keg(dinner_rope, star=30, pledge=True)

    # WHEN / THEN
    fund_graph0(sue_plan, kw.task, graphics_bool)
