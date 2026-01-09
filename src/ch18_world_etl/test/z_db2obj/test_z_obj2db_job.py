from sqlite3 import connect as sqlite3_connect
from src.ch01_py.db_toolbox import get_row_count
from src.ch03_voice.group import (
    awardheir_shop,
    awardunit_shop,
    groupunit_shop,
    membership_shop,
)
from src.ch03_voice.labor import laborheir_shop, laborunit_shop, partyheir_shop
from src.ch03_voice.voice import voiceunit_shop
from src.ch04_rope.rope import create_rope
from src.ch05_reason.reason_main import caseunit_shop, factheir_shop, reasonheir_shop
from src.ch06_keg.healer import healerunit_shop
from src.ch06_keg.keg import kegunit_shop
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch18_world_etl.etl_sqlstr import create_job_tables
from src.ch18_world_etl.obj2db_plan import (
    ObjKeysHolder,
    insert_job_blfawar,
    insert_job_blfcase,
    insert_job_blffact,
    insert_job_blfgrou,
    insert_job_blfheal,
    insert_job_blfkegg,
    insert_job_blflabo,
    insert_job_blfmemb,
    insert_job_blfreas,
    insert_job_blfunit,
    insert_job_blfvoce,
    insert_job_obj,
)
from src.ch18_world_etl.test._util.ch18_env import temp_dir_setup
from src.ref.keywords import Ch18Keywords as kw, ExampleStrs as exx


def test_ObjKeysHolder_Exists():
    # ESTABLISH / WHEN
    x_objkeyholder = ObjKeysHolder()

    # THEN
    assert not x_objkeyholder.moment_label
    assert not x_objkeyholder.plan_name
    assert not x_objkeyholder.rope
    assert not x_objkeyholder.reason_context
    assert not x_objkeyholder.voice_name
    assert not x_objkeyholder.membership
    assert not x_objkeyholder.group_title
    assert not x_objkeyholder.fact_rope


def test_insert_job_blfunit_CreatesTableRowsFor_planunit_job():
    # sourcery skip: extract-method
    # ESTABLISH
    x_moment_label = exx.a23
    x_plan_name = "Sue"
    x_keeps_buildable = 99
    x_keeps_justified = 77
    x_offtrack_fund = 55.5
    x_rational = 92
    x_sum_healerunit_kegs_fund_total = 66.6
    x_tree_traverse_count = 7
    x_credor_respect = 88.2
    x_debtor_respect = 88.4
    x_fund_grain = 3.0
    x_fund_pool = 3000.0
    x_max_tree_traverse = 22
    x_mana_grain = 4.0
    x_respect_grain = 0.2
    x_tally = 6
    sue_plan = planunit_shop(x_plan_name, moment_label=x_moment_label)
    sue_plan.fund_pool = x_fund_pool
    sue_plan.fund_grain = x_fund_grain
    sue_plan.mana_grain = x_mana_grain
    sue_plan.tally = x_tally
    sue_plan.respect_grain = x_respect_grain
    sue_plan.max_tree_traverse = x_max_tree_traverse
    sue_plan.keeps_buildable = x_keeps_buildable
    sue_plan.keeps_justified = x_keeps_justified
    sue_plan.offtrack_fund = x_offtrack_fund
    sue_plan.rational = x_rational
    sue_plan.sum_healerunit_kegs_fund_total = x_sum_healerunit_kegs_fund_total
    sue_plan.tree_traverse_count = x_tree_traverse_count
    sue_plan.credor_respect = x_credor_respect
    sue_plan.debtor_respect = x_debtor_respect

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "planunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        objkeysholder = ObjKeysHolder()

        # WHEN
        insert_job_blfunit(cursor, objkeysholder, sue_plan)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            x_moment_label,
            x_plan_name,
            x_credor_respect,
            x_debtor_respect,
            x_fund_pool,
            x_max_tree_traverse,
            x_tally,
            x_fund_grain,
            x_mana_grain,
            x_respect_grain,
            x_rational,
            x_keeps_justified,
            x_offtrack_fund,
            x_sum_healerunit_kegs_fund_total,
            x_keeps_buildable,
            x_tree_traverse_count,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_job_blfkegg_CreatesTableRowsFor_blfkegg_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_plan_calc_dimen_args("plan_kegunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_keg.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""            x_{x_arg},""")
    # print("")
    x_moment_label = exx.a23
    x_plan_name = 2
    casa_rope = create_rope(x_moment_label, "casa")
    x_parent_rope = casa_rope
    x_keg_label = "clean"
    x_begin = 5.0
    x_close = 6.0
    x_addin = 7.0
    x_numor = 8
    x_denom = 9
    x_morph = 10
    x_gogo_want = 11.0
    x_stop_want = 12.0
    x_star = 13
    x_pledge = 14
    x_problem_bool = 15
    x_active = 16
    x_task = 17
    x_fund_grain = 18.0
    x_fund_onset = 19.0
    x_fund_cease = 20.0
    x_fund_ratio = 21.0
    x_gogo_calc = 22.0
    x_stop_calc = 23.0
    x_level = 24
    x_range_evaluated = 25
    x_descendant_pledge_count = 26
    x_healerunit_ratio = 27.0
    x_all_voice_cred = 28
    x_all_voice_debt = 29
    x_keg = kegunit_shop(exx.casa)
    x_keg.parent_rope = x_parent_rope
    x_keg.keg_label = x_keg_label
    x_keg.begin = x_begin
    x_keg.close = x_close
    x_keg.addin = x_addin
    x_keg.numor = x_numor
    x_keg.denom = x_denom
    x_keg.morph = x_morph
    x_keg.gogo_want = x_gogo_want
    x_keg.stop_want = x_stop_want
    x_keg.star = x_star
    x_keg.pledge = x_pledge
    x_keg.problem_bool = x_problem_bool
    x_keg.keg_active = x_active
    x_keg.task = x_task
    x_keg.fund_grain = x_fund_grain
    x_keg.fund_onset = x_fund_onset
    x_keg.fund_cease = x_fund_cease
    x_keg.fund_ratio = x_fund_ratio
    x_keg.gogo_calc = x_gogo_calc
    x_keg.stop_calc = x_stop_calc
    x_keg.tree_level = x_level
    x_keg.range_evaluated = x_range_evaluated
    x_keg.descendant_pledge_count = x_descendant_pledge_count
    x_keg.healerunit_ratio = x_healerunit_ratio
    x_keg.all_voice_cred = x_all_voice_cred
    x_keg.all_voice_debt = x_all_voice_debt
    x_keg.begin = x_begin
    x_keg.close = x_close
    x_keg.addin = x_addin
    x_keg.numor = x_numor
    x_keg.denom = x_denom
    x_keg.morph = x_morph
    x_keg.gogo_want = x_gogo_want
    x_keg.stop_want = x_stop_want
    x_keg.star = x_star
    x_keg.pledge = x_pledge
    x_keg.problem_bool = x_problem_bool
    x_keg.keg_active = x_active
    x_keg.task = x_task
    x_keg.fund_grain = x_fund_grain
    x_keg.fund_onset = x_fund_onset
    x_keg.fund_cease = x_fund_cease
    x_keg.fund_ratio = x_fund_ratio
    x_keg.gogo_calc = x_gogo_calc
    x_keg.stop_calc = x_stop_calc
    x_keg.tree_level = x_level
    x_keg.range_evaluated = x_range_evaluated
    x_keg.descendant_pledge_count = x_descendant_pledge_count
    x_keg.healerunit_ratio = x_healerunit_ratio
    x_keg.all_voice_cred = x_all_voice_cred
    x_keg.all_voice_debt = x_all_voice_debt

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "plan_kegunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(
            moment_label=x_moment_label, plan_name=x_plan_name
        )

        # WHEN
        insert_job_blfkegg(cursor, x_objkeysholder, x_keg)

        # THEN
        clean_rope = create_rope(casa_rope, "clean")
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            None,
            str(x_plan_name),
            clean_rope,
            x_begin,
            x_close,
            x_addin,
            x_numor,
            x_denom,
            x_morph,
            x_gogo_want,
            x_stop_want,
            x_star,
            x_pledge,
            x_problem_bool,
            x_fund_grain,
            x_active,
            x_task,
            x_fund_onset,
            x_fund_cease,
            x_fund_ratio,
            x_gogo_calc,
            x_stop_calc,
            x_level,
            x_range_evaluated,
            x_descendant_pledge_count,
            x_healerunit_ratio,
            x_all_voice_cred,
            x_all_voice_debt,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_job_blfreas_CreatesTableRowsFor_blfreas_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_plan_calc_dimen_args("plan_keg_reasonunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_reasonunit.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""            x_{x_arg},""")
    # print("")

    x_moment_label = 1
    x_plan_name = 2
    x_rope = 3
    x_reason_context = 4
    x_active_requisite = 5
    x_task = 6
    x_reason_active = 7
    x__heir_active = 8
    x_reasonheir = reasonheir_shop(reason_context=x_reason_context)
    x_reasonheir.reason_context = x_reason_context
    x_reasonheir.active_requisite = x_active_requisite
    x_reasonheir.task = x_task
    x_reasonheir.reason_active = x_reason_active
    x_reasonheir.parent_heir_active = x__heir_active

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "plan_keg_reasonunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(
            moment_label=x_moment_label, plan_name=x_plan_name, rope=x_rope
        )

        # WHEN
        insert_job_blfreas(cursor, x_objkeysholder, x_reasonheir)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_moment_label),
            str(x_plan_name),
            str(x_rope),
            str(x_reason_context),
            x_active_requisite,
            x_task,
            x_reason_active,
            x__heir_active,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_job_blfcase_CreatesTableRowsFor_blfcase_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_plan_calc_dimen_args("plan_keg_reason_caseunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_caseunit.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""            x_{x_arg},""")

    x_moment_label = 1
    x_plan_name = 2
    x_rope = 3
    x_reason_context = 4
    x_reason_state = 5
    x_reason_lower = 7.0
    x_reason_upper = 6.0
    x_reason_divisor = 8
    x_task = 9
    x_case_active = 10
    x_caseunit = caseunit_shop(reason_state=x_reason_state)
    x_caseunit.reason_state = x_reason_state
    x_caseunit.reason_lower = x_reason_lower
    x_caseunit.reason_upper = x_reason_upper
    x_caseunit.reason_divisor = x_reason_divisor
    x_caseunit.task = x_task
    x_caseunit.case_active = x_case_active

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "plan_keg_reason_caseunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(
            moment_label=x_moment_label,
            plan_name=x_plan_name,
            rope=x_rope,
            reason_context=x_reason_context,
        )

        # WHEN
        insert_job_blfcase(cursor, x_objkeysholder, x_caseunit)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_moment_label),
            str(x_plan_name),
            str(x_rope),
            str(x_reason_context),
            str(x_reason_state),
            x_reason_lower,
            x_reason_upper,
            x_reason_divisor,
            x_task,
            x_case_active,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_job_blfmemb_CreatesTableRowsFor_blfmemb_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_plan_calc_dimen_args("plan_voice_membership")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_membership.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""            x_{x_arg},""")

    x_moment_label = 1
    x_plan_name = 2
    x_voice_name = 3
    x_group_title = 4
    x_group_cred_lumen = 5.0
    x_group_debt_lumen = 6.0
    x_credor_pool = 7.0
    x_debtor_pool = 8.0
    x_fund_give = 9.0
    x_fund_take = 10.0
    x_fund_agenda_give = 11.0
    x_fund_agenda_take = 12.0
    x_fund_agenda_ratio_give = 13.0
    x_fund_agenda_ratio_take = 14.0
    x_membership = membership_shop(x_group_title)
    x_membership.voice_name = x_voice_name
    x_membership.group_cred_lumen = x_group_cred_lumen
    x_membership.group_debt_lumen = x_group_debt_lumen
    x_membership.credor_pool = x_credor_pool
    x_membership.debtor_pool = x_debtor_pool
    x_membership.fund_give = x_fund_give
    x_membership.fund_take = x_fund_take
    x_membership.fund_agenda_give = x_fund_agenda_give
    x_membership.fund_agenda_take = x_fund_agenda_take
    x_membership.fund_agenda_ratio_give = x_fund_agenda_ratio_give
    x_membership.fund_agenda_ratio_take = x_fund_agenda_ratio_take

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "plan_voice_membership_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(
            moment_label=x_moment_label, plan_name=x_plan_name
        )

        # WHEN
        insert_job_blfmemb(cursor, x_objkeysholder, x_membership)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_moment_label),
            str(x_plan_name),
            str(x_voice_name),
            str(x_group_title),
            x_group_cred_lumen,
            x_group_debt_lumen,
            x_credor_pool,
            x_debtor_pool,
            x_fund_give,
            x_fund_take,
            x_fund_agenda_give,
            x_fund_agenda_take,
            x_fund_agenda_ratio_give,
            x_fund_agenda_ratio_take,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_job_blfvoce_CreatesTableRowsFor_blfvoce_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_plan_calc_dimen_args("plan_voiceunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_voice.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""            x_{x_arg},""")

    x_moment_label = 1
    x_plan_name = 2
    x_voice_name = 3
    x_voice_cred_lumen = 4
    x_voice_debt_lumen = 5
    x_credor_pool = 6
    x_debtor_pool = 7
    x_fund_give = 8
    x_fund_take = 9
    x_fund_agenda_give = 10
    x_fund_agenda_take = 11
    x_fund_agenda_ratio_give = 12
    x_fund_agenda_ratio_take = 13
    x_inallocable_voice_debt_lumen = 14
    x_irrational_voice_debt_lumen = 15
    x_groupmark = 16
    x_voice = voiceunit_shop(x_voice_name)
    x_voice.voice_name = x_voice_name
    x_voice.voice_cred_lumen = x_voice_cred_lumen
    x_voice.voice_debt_lumen = x_voice_debt_lumen
    x_voice.credor_pool = x_credor_pool
    x_voice.debtor_pool = x_debtor_pool
    x_voice.fund_give = x_fund_give
    x_voice.fund_take = x_fund_take
    x_voice.fund_agenda_give = x_fund_agenda_give
    x_voice.fund_agenda_take = x_fund_agenda_take
    x_voice.fund_agenda_ratio_give = x_fund_agenda_ratio_give
    x_voice.fund_agenda_ratio_take = x_fund_agenda_ratio_take
    x_voice.inallocable_voice_debt_lumen = x_inallocable_voice_debt_lumen
    x_voice.irrational_voice_debt_lumen = x_irrational_voice_debt_lumen
    x_voice.groupmark = x_groupmark

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "plan_voiceunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(
            moment_label=x_moment_label, plan_name=x_plan_name
        )

        # WHEN
        insert_job_blfvoce(cursor, x_objkeysholder, x_voice)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_moment_label),
            str(x_plan_name),
            str(x_voice_name),
            x_voice_cred_lumen,
            x_voice_debt_lumen,
            str(x_groupmark),
            x_credor_pool,
            x_debtor_pool,
            x_fund_give,
            x_fund_take,
            x_fund_agenda_give,
            x_fund_agenda_take,
            x_fund_agenda_ratio_give,
            x_fund_agenda_ratio_take,
            x_inallocable_voice_debt_lumen,
            x_irrational_voice_debt_lumen,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_job_blfgrou_CreatesTableRowsFor_blfgrou_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_plan_calc_dimen_args("plan_groupunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_group.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""            x_{x_arg},""")

    x_moment_label = 1
    x_plan_name = 2
    x_group_title = 3
    x_fund_grain = 4
    x_credor_pool = 6
    x_debtor_pool = 7
    x_fund_give = 8
    x_fund_take = 9
    x_fund_agenda_give = 10
    x_fund_agenda_take = 11
    x_group = groupunit_shop(x_group_title)
    x_group.group_title = x_group_title
    x_group.fund_grain = x_fund_grain
    x_group.credor_pool = x_credor_pool
    x_group.debtor_pool = x_debtor_pool
    x_group.fund_give = x_fund_give
    x_group.fund_take = x_fund_take
    x_group.fund_agenda_give = x_fund_agenda_give
    x_group.fund_agenda_take = x_fund_agenda_take

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "plan_groupunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(
            moment_label=x_moment_label, plan_name=x_plan_name
        )

        # WHEN
        insert_job_blfgrou(cursor, x_objkeysholder, x_group)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_moment_label),
            str(x_plan_name),
            str(x_group_title),
            x_fund_grain,
            x_credor_pool,
            x_debtor_pool,
            x_fund_give,
            x_fund_take,
            x_fund_agenda_give,
            x_fund_agenda_take,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_job_blfawar_CreatesTableRowsFor_blfawar_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_plan_calc_dimen_args("plan_keg_awardunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_awardheir.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""            x_{x_arg},""")

    x_moment_label = 1
    x_plan_name = 2
    x_rope = 3
    x_awardee_title = 4
    x_give_force = 5
    x_take_force = 6
    x_fund_give = 7
    x_fund_take = 8
    x_awardheir = awardheir_shop(x_awardee_title)
    x_awardheir.awardee_title = x_awardee_title
    x_awardheir.give_force = x_give_force
    x_awardheir.take_force = x_take_force
    x_awardheir.fund_give = x_fund_give
    x_awardheir.fund_take = x_fund_take

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "plan_keg_awardunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(
            moment_label=x_moment_label, plan_name=x_plan_name, rope=x_rope
        )

        # WHEN
        insert_job_blfawar(cursor, x_objkeysholder, x_awardheir)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_moment_label),
            str(x_plan_name),
            str(x_rope),
            str(x_awardee_title),
            x_give_force,
            x_take_force,
            x_fund_give,
            x_fund_take,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_job_blffact_CreatesTableRowsFor_blffact_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_plan_calc_dimen_args("plan_keg_factunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_factheir.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""            x_{x_arg},""")

    x_moment_label = 1
    x_plan_name = 2
    x_rope = 3
    x_reason_context = 4
    x_fact_state = 5
    x_fact_lower = 6
    x_fact_upper = 7
    x_factheir = factheir_shop()
    x_factheir.fact_context = x_reason_context
    x_factheir.fact_state = x_fact_state
    x_factheir.fact_lower = x_fact_lower
    x_factheir.fact_upper = x_fact_upper

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "plan_keg_factunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(
            moment_label=x_moment_label, plan_name=x_plan_name, rope=x_rope
        )

        # WHEN
        insert_job_blffact(cursor, x_objkeysholder, x_factheir)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_moment_label),
            str(x_plan_name),
            str(x_rope),
            str(x_reason_context),
            str(x_fact_state),
            x_fact_lower,
            x_fact_upper,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_job_blfheal_CreatesTableRowsFor_blfheal_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_plan_calc_dimen_args("plan_keg_healerunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_healerunit.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""            x_{x_arg},""")

    x_moment_label = 1
    x_plan_name = 2
    x_rope = 3
    x_healerunit = healerunit_shop()
    x_healerunit.set_healer_name(exx.bob)
    x_healerunit.set_healer_name(exx.sue)

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "plan_keg_healerunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(
            moment_label=x_moment_label, plan_name=x_plan_name, rope=x_rope
        )

        # WHEN
        insert_job_blfheal(cursor, x_objkeysholder, x_healerunit)

        # THEN
        assert get_row_count(cursor, x_table_name) == 2
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_moment_label),
            str(x_plan_name),
            str(x_rope),
            exx.bob,
        )
        expected_row2 = (
            str(x_moment_label),
            str(x_plan_name),
            str(x_rope),
            exx.sue,
        )
        expected_data = [expected_row1, expected_row2]
        assert rows == expected_data


def test_insert_job_blflabo_CreatesTableRowsFor_blflabo_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_plan_calc_dimen_args("plan_keg_partyunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_laborheir.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""            x_{x_arg},""")

    x_moment_label = 1
    x_plan_name = 2
    x_rope = 3
    x__plan_name_is_labor = 5
    x_laborheir = laborheir_shop()
    x_laborheir.plan_name_is_labor = x__plan_name_is_labor
    bob_solo_bool = 6
    sue_solo_bool = 7
    bob_partyheir = partyheir_shop(exx.bob, bob_solo_bool)
    sue_partyheir = partyheir_shop(exx.sue, sue_solo_bool)
    x_laborheir.partys = {exx.bob: bob_partyheir, exx.sue: sue_partyheir}

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "plan_keg_partyunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(
            moment_label=x_moment_label, plan_name=x_plan_name, rope=x_rope
        )

        # WHEN
        insert_job_blflabo(cursor, x_objkeysholder, x_laborheir)

        # THEN
        assert get_row_count(cursor, x_table_name) == 2
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_moment_label),
            str(x_plan_name),
            str(x_rope),
            exx.bob,
            bob_solo_bool,
            x__plan_name_is_labor,
        )
        expected_row2 = (
            str(x_moment_label),
            str(x_plan_name),
            str(x_rope),
            exx.sue,
            sue_solo_bool,
            x__plan_name_is_labor,
        )
        expected_data = [expected_row1, expected_row2]
        assert rows == expected_data


def test_insert_job_obj_CreatesTableRows_Scenario0():
    # sourcery skip: extract-method
    # ESTABLISH
    sue_plan = planunit_shop(exx.sue, exx.a23)
    sue_plan.add_voiceunit(exx.sue)
    sue_plan.add_voiceunit(exx.bob)
    sue_plan.get_voice(exx.bob).add_membership(exx.run)
    casa_rope = sue_plan.make_l1_rope("casa")
    situation_rope = sue_plan.make_l1_rope(kw.reason_active)
    clean_rope = sue_plan.make_rope(situation_rope, "clean")
    dirty_rope = sue_plan.make_rope(situation_rope, "dirty")
    sue_plan.add_keg(casa_rope)
    sue_plan.add_keg(clean_rope)
    sue_plan.add_keg(dirty_rope)
    sue_plan.edit_keg_attr(
        casa_rope, reason_context=situation_rope, reason_case=dirty_rope
    )
    sue_plan.edit_keg_attr(casa_rope, awardunit=awardunit_shop(exx.run))
    sue_plan.edit_keg_attr(casa_rope, healerunit=healerunit_shop({exx.bob}))
    casa_laborunit = laborunit_shop()
    casa_laborunit.add_party(exx.sue, True)
    sue_plan.edit_keg_attr(casa_rope, laborunit=casa_laborunit)
    sue_plan.add_fact(situation_rope, clean_rope)

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        blfmemb_job_table = f"{kw.plan_voice_membership}_job"
        blfvoce_job_table = f"{kw.plan_voiceunit}_job"
        blfgrou_job_table = f"{kw.plan_groupunit}_job"
        blfawar_job_table = f"{kw.plan_keg_awardunit}_job"
        blffact_job_table = f"{kw.plan_keg_factunit}_job"
        blfheal_job_table = f"{kw.plan_keg_healerunit}_job"
        blfcase_job_table = f"{kw.plan_keg_reason_caseunit}_job"
        blfreas_job_table = f"{kw.plan_keg_reasonunit}_job"
        blflabo_job_table = f"{kw.plan_keg_partyunit}_job"
        blfkegg_job_table = f"{kw.plan_kegunit}_job"
        blfunit_job_table = f"{kw.planunit}_job"
        assert get_row_count(cursor, blfunit_job_table) == 0
        assert get_row_count(cursor, blfkegg_job_table) == 0
        assert get_row_count(cursor, blfvoce_job_table) == 0
        assert get_row_count(cursor, blfmemb_job_table) == 0
        assert get_row_count(cursor, blfgrou_job_table) == 0
        assert get_row_count(cursor, blfawar_job_table) == 0
        assert get_row_count(cursor, blffact_job_table) == 0
        assert get_row_count(cursor, blfheal_job_table) == 0
        assert get_row_count(cursor, blfreas_job_table) == 0
        assert get_row_count(cursor, blfcase_job_table) == 0
        assert get_row_count(cursor, blflabo_job_table) == 0

        # WHEN
        insert_job_obj(cursor, sue_plan)

        # THEN
        assert get_row_count(cursor, blfunit_job_table) == 1
        assert get_row_count(cursor, blfkegg_job_table) == 5
        assert get_row_count(cursor, blfvoce_job_table) == 2
        assert get_row_count(cursor, blfmemb_job_table) == 3
        assert get_row_count(cursor, blfgrou_job_table) == 3
        assert get_row_count(cursor, blfawar_job_table) == 1
        assert get_row_count(cursor, blffact_job_table) == 1
        assert get_row_count(cursor, blfheal_job_table) == 1
        assert get_row_count(cursor, blfreas_job_table) == 1
        assert get_row_count(cursor, blfcase_job_table) == 1
        assert get_row_count(cursor, blflabo_job_table) == 1
