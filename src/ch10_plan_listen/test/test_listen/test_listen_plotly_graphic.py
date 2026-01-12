from src.ch10_plan_listen.test._util.ch10_examples import get_fund_breakdown_plan
from src.ch10_plan_listen.test.test_listen.listen_graphic import (
    fund_graph13,
    get_listen_structures0_fig,
    get_listen_structures1_fig,
    get_listen_structures2_fig,
    get_listen_structures3_fig,
)
from src.ref.keywords import Ch10Keywords as kw


def test_listen_structures0_ShowsGraphs(graphics_bool):
    # ESTABLISH / WHEN / THEN
    get_listen_structures0_fig(graphics_bool)
    get_listen_structures1_fig(graphics_bool)
    get_listen_structures2_fig(graphics_bool)
    get_listen_structures3_fig(graphics_bool)


def test_fund_graph_ShowsGraph(graphics_bool):
    # ESTABLISH / WHEN
    x_planunit = get_fund_breakdown_plan()

    # THEN
    fund_graph13(x_planunit, kw.task, graphics_bool)
