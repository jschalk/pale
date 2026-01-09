from src.ch01_py.plotly_toolbox import conditional_fig_show
from src.ch08_plan_atom.atom_graphic import planatom_periodic_table0

# from src.ch07_plan_logic.test._util.example_plans import (
#     planunit_v001_with_large_agenda,
#     get_planunit_with_4_levels,
#     get_planunit_with_4_levels_and_2reasons,
#     get_planunit_x1_3levels_1reason_1facts,
# )
# from src.ch07_plan_logic.plan import planunit_shop


def test_planatom_periodic_table0_ShowsGraph0(graphics_bool):
    # ESTABLISH / WHEN
    planatom_periodic_table0_fig = planatom_periodic_table0()

    # THEN
    conditional_fig_show(planatom_periodic_table0_fig, graphics_bool)
