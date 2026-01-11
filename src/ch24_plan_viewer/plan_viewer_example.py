from src.ch02_person.group import awardunit_shop
from src.ch03_labor.labor import laborunit_shop
from src.ch07_plan_logic.plan_main import PlanUnit, planunit_shop
from src.ch07_plan_logic.plan_tool import plan_keg_reason_caseunit_set_obj
from src.ch07_plan_logic.test._util.ch07_examples import get_planunit_irrational_example


def sue2_str() -> str:
    return "Sue"


def bob2_str() -> str:
    return "Bob"


def best_sport_str() -> str:
    return "best sport"


def best_soccer_str() -> str:
    return "The best sport is soccer"


def best_swim_str() -> str:
    return "The best sport is swimming"


def best_run_str() -> str:
    return "The best sport is running"


def play_str() -> str:
    return "playing"


def play_soccer_str() -> str:
    return "play soccer"


def play_swim_str() -> str:
    return "play swimming"


def play_run_str() -> str:
    return "play running"


def get_sue_planunit() -> PlanUnit:
    sue_plan = planunit_shop(sue2_str(), "accord23")
    sue_cred_lumen = 11
    sue_debt_lumen = 13
    bob_cred_lumen = 23
    bob_debt_lumen = 29
    sue_plan.add_personunit(sue2_str(), sue_cred_lumen, sue_debt_lumen)
    sue_plan.add_personunit(bob2_str(), bob_cred_lumen, bob_debt_lumen)
    sue_person = sue_plan.get_person(sue2_str())
    swim_str = ";swimmers"
    team_str = ";Team Administrator"
    sue_person.add_membership(swim_str, 77, 51)
    bob_person = sue_plan.get_person(bob2_str())
    bob_person.add_membership(swim_str, 12, 37)
    bob_person.add_membership(team_str, 51, 91)

    casa_rope = sue_plan.make_l1_rope("casa")
    clean_rope = sue_plan.make_rope(casa_rope, "clean")
    mop_rope = sue_plan.make_rope(clean_rope, "mop")
    mop_fancy_rope = sue_plan.make_rope(mop_rope, "use fancy mop")
    sweep_rope = sue_plan.make_rope(clean_rope, "sweep")
    tidi_rope = sue_plan.make_rope(casa_rope, "tidiness")
    dirty_rope = sue_plan.make_rope(tidi_rope, "dirty")
    tidy_rope = sue_plan.make_rope(tidi_rope, "tidy")
    sue_plan.add_keg(casa_rope, 3)
    sue_plan.add_keg(tidi_rope, 7)
    sue_plan.add_keg(dirty_rope, 1)
    sue_plan.add_keg(tidy_rope, 3)
    sue_plan.add_keg(clean_rope, 3)
    sue_plan.add_keg(mop_rope, 3, pledge=True)
    sue_plan.add_keg(mop_fancy_rope, 3, pledge=True)
    sue_plan.add_keg(sweep_rope, 3, pledge=True)
    sports_rope = sue_plan.make_l1_rope("sports")
    best_rope = sue_plan.make_rope(sports_rope, best_sport_str())
    best_soccer_rope = sue_plan.make_rope(best_rope, best_soccer_str())
    best_swim_rope = sue_plan.make_rope(best_rope, best_swim_str())
    best_run_rope = sue_plan.make_rope(best_rope, best_run_str())
    play_rope = sue_plan.make_rope(sports_rope, play_str())
    play_soccer_rope = sue_plan.make_rope(play_rope, play_soccer_str())
    play_swim_rope = sue_plan.make_rope(play_rope, play_swim_str())
    play_run_rope = sue_plan.make_rope(play_rope, play_run_str())
    sue_plan.add_keg(sports_rope, 5)
    sue_plan.add_keg(best_soccer_rope, 23)
    sue_plan.add_keg(best_swim_rope, 2)
    sue_plan.add_keg(best_run_rope, 23)
    sue_plan.add_keg(play_rope, 2)
    sue_plan.add_keg(play_soccer_rope, 11, pledge=True)
    sue_plan.add_keg(play_swim_rope, 55, pledge=True)
    sue_plan.add_keg(play_run_rope, 22, pledge=True)

    # Add some award links
    casa_administrator_awardunit = awardunit_shop("Administrator", 0.5, 0.2)
    casa_team_awardunit = awardunit_shop(team_str, 0.3, 0.1)
    casa_devloper_awardunit = awardunit_shop(sue2_str(), 1, 0.8)
    casa_jundevloper_awardunit = awardunit_shop("Bob", 0.7, 0.9)
    root_rope = sue_plan.kegroot.get_keg_rope()
    sue_plan.edit_keg_attr(root_rope, awardunit=casa_administrator_awardunit)
    sue_plan.edit_keg_attr(root_rope, awardunit=casa_team_awardunit)
    sue_plan.edit_keg_attr(casa_rope, awardunit=casa_devloper_awardunit)
    sue_plan.edit_keg_attr(casa_rope, awardunit=casa_jundevloper_awardunit)
    sue_plan.cashout()
    return sue_plan


def get_sue_plan_with_facts_and_reasons() -> PlanUnit:
    sue_plan = get_sue_planunit()
    casa_rope = sue_plan.make_l1_rope("casa")
    clean_rope = sue_plan.make_rope(casa_rope, "clean")
    mop_rope = sue_plan.make_rope(clean_rope, "mop")
    sweep_rope = sue_plan.make_rope(clean_rope, "sweep")
    tidi_rope = sue_plan.make_rope(casa_rope, "tidiness")
    dirty_rope = sue_plan.make_rope(tidi_rope, "dirty")
    tidy_rope = sue_plan.make_rope(tidi_rope, "tidy")
    sports_rope = sue_plan.make_l1_rope("sports")
    best_rope = sue_plan.make_rope(sports_rope, best_sport_str())
    best_soccer_rope = sue_plan.make_rope(best_rope, best_soccer_str())
    best_swim_rope = sue_plan.make_rope(best_rope, best_swim_str())
    best_run_rope = sue_plan.make_rope(best_rope, best_run_str())
    play_rope = sue_plan.make_rope(sports_rope, play_str())
    play_soccer_rope = sue_plan.make_rope(play_rope, play_soccer_str())
    play_swim_rope = sue_plan.make_rope(play_rope, play_swim_str())
    play_run_rope = sue_plan.make_rope(play_rope, play_run_str())
    sue_plan.add_fact(tidi_rope, dirty_rope, 4, 8)
    sue_plan.add_fact(best_rope, best_soccer_rope, 1, 7)
    mop_laborunit = laborunit_shop()
    mop_laborunit.add_party(sue2_str())
    mop_laborunit.add_party(bob2_str(), True)
    sue_plan.edit_keg_attr(mop_rope, laborunit=mop_laborunit)
    # add reasons to mop_keg, sweep_keg, play_soccer_keg, keg_swim_keg, play_run_keg
    x_keg = "keg_rope"
    x_context = "reason_context"
    x_state = "reason_state"
    tidi_dirty_jkeys = {x_keg: mop_rope, x_context: tidi_rope, x_state: dirty_rope}
    swwep_dirty_jkeys = {x_keg: sweep_rope, x_context: tidi_rope, x_state: dirty_rope}
    soccer_soccer_jkeys = {
        x_keg: play_soccer_rope,
        x_context: best_rope,
        x_state: best_soccer_rope,
    }
    soccer_run_jkeys = {
        x_keg: play_soccer_rope,
        x_context: best_rope,
        x_state: best_run_rope,
    }
    soccer_tidy_jkeys = {
        x_keg: play_soccer_rope,
        x_context: tidi_rope,
        x_state: tidy_rope,
    }
    swim_swim_jkeys = {
        x_keg: play_swim_rope,
        x_context: best_rope,
        x_state: best_swim_rope,
    }
    swim_tidy_jkeys = {x_keg: play_swim_rope, x_context: tidi_rope, x_state: tidy_rope}
    run_run_jkeys = {
        x_keg: play_run_rope,
        x_context: best_rope,
        x_state: best_run_rope,
    }
    plan_keg_reason_caseunit_set_obj(sue_plan, tidi_dirty_jkeys)
    plan_keg_reason_caseunit_set_obj(sue_plan, swwep_dirty_jkeys)
    plan_keg_reason_caseunit_set_obj(sue_plan, soccer_soccer_jkeys)
    plan_keg_reason_caseunit_set_obj(sue_plan, soccer_run_jkeys)
    plan_keg_reason_caseunit_set_obj(sue_plan, soccer_tidy_jkeys)
    plan_keg_reason_caseunit_set_obj(sue_plan, swim_swim_jkeys)
    plan_keg_reason_caseunit_set_obj(sue_plan, swim_tidy_jkeys)
    plan_keg_reason_caseunit_set_obj(sue_plan, run_run_jkeys)
    sue_plan.cashout()
    return sue_plan
