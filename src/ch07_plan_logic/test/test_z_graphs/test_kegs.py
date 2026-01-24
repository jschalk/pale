from src.ch07_plan_logic.plan_graphic import (
    display_kegtree,
    planunit_graph0,
    planunit_graph1,
    planunit_graph2,
    planunit_graph3,
    planunit_graph4,
)
from src.ch07_plan_logic.test._util.ch07_examples import (
    get_planunit_with_4_levels,
    get_planunit_with_4_levels_and_2reasons,
    get_planunit_x1_3levels_1reason_1facts,
)
from src.ref.keywords import Ch07Keywords as kw


def test_planunit_graph_Showsgraph0PlanGraph(graphics_bool):
    # ESTABLISH / WHEN / THEN
    display_kegtree(get_planunit_with_4_levels(), graphics_bool)
    display_kegtree(get_planunit_with_4_levels_and_2reasons(), kw.task, graphics_bool)
    display_kegtree(get_planunit_x1_3levels_1reason_1facts(), graphics_bool)
    planunit_graph0(graphics_bool)
    planunit_graph1(graphics_bool)
    planunit_graph2(graphics_bool)
    planunit_graph3(graphics_bool)
    planunit_graph4(graphics_bool)
