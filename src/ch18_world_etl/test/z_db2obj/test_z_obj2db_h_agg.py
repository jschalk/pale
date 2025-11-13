from sqlite3 import connect as sqlite3_connect
from src.ch01_py.db_toolbox import get_row_count, get_table_columns
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
from src.ch06_plan.healer import healerunit_shop
from src.ch06_plan.plan import planunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch18_world_etl.etl_sqlstr import create_sound_and_heard_tables
from src.ch18_world_etl.obj2db_belief import (
    ObjKeysHolder,
    insert_h_agg_blfawar,
    insert_h_agg_blfcase,
    insert_h_agg_blffact,
    insert_h_agg_blfgrou,
    insert_h_agg_blfheal,
    insert_h_agg_blflabo,
    insert_h_agg_blfmemb,
    insert_h_agg_blfplan,
    insert_h_agg_blfreas,
    insert_h_agg_blfunit,
    insert_h_agg_blfvoce,
    insert_h_agg_obj,
)
from src.ch18_world_etl.test._util.ch18_env import temp_dir_setup
from src.ref.keywords import Ch18Keywords as kw, ExampleStrs as exx


def test_insert_h_agg_blfunit_CreatesTableRowsFor_beliefunit_h_agg():
    # sourcery skip: extract-method
    # ESTABLISH
    x_spark_num = 77
    x_face_name = exx.yao
    # TODO replace all "Amy23" references in tests to exx.a23
    x_moment_label = "Amy23"
    x_belief_name = "Sue"
    x_credor_respect = 88.2
    x_debtor_respect = 88.4
    x_fund_grain = 3.0
    x_fund_pool = 3000.0
    x_max_tree_traverse = 22
    x_mana_grain = 4.0
    x_respect_grain = 0.2
    x_tally = 6
    sue_belief = beliefunit_shop(x_belief_name, moment_label=x_moment_label)
    sue_belief.fund_pool = x_fund_pool
    sue_belief.fund_grain = x_fund_grain
    sue_belief.mana_grain = x_mana_grain
    sue_belief.tally = x_tally
    sue_belief.respect_grain = x_respect_grain
    sue_belief.max_tree_traverse = x_max_tree_traverse
    sue_belief.credor_respect = x_credor_respect
    sue_belief.debtor_respect = x_debtor_respect

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_heard_tables(cursor)
        x_table_name = "beliefunit_h_put_agg"
        assert get_row_count(cursor, x_table_name) == 0
        objkeysholder = ObjKeysHolder(x_spark_num, x_face_name)

        # WHEN
        insert_h_agg_blfunit(cursor, objkeysholder, sue_belief)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            x_spark_num,
            x_face_name,
            x_moment_label,
            x_belief_name,
            x_credor_respect,
            x_debtor_respect,
            x_fund_pool,
            x_max_tree_traverse,
            x_tally,
            x_fund_grain,
            x_mana_grain,
            x_respect_grain,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_h_agg_blfplan_CreatesTableRowsFor_blfplan_h_agg():
    # sourcery skip: extract-method
    # ESTABLISH
    x_spark_num = 77
    x_face_name = exx.yao
    x_moment_label = "Amy23"
    x_belief_name = 2
    casa_rope = create_rope(x_moment_label, "casa")
    x_parent_rope = casa_rope
    x_plan_label = "clean"
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
    x_plan = planunit_shop(exx.casa)
    x_plan.parent_rope = x_parent_rope
    x_plan.plan_label = x_plan_label
    x_plan.begin = x_begin
    x_plan.close = x_close
    x_plan.addin = x_addin
    x_plan.numor = x_numor
    x_plan.denom = x_denom
    x_plan.morph = x_morph
    x_plan.gogo_want = x_gogo_want
    x_plan.stop_want = x_stop_want
    x_plan.star = x_star
    x_plan.pledge = x_pledge
    x_plan.problem_bool = x_problem_bool
    x_plan.begin = x_begin
    x_plan.close = x_close
    x_plan.addin = x_addin
    x_plan.numor = x_numor
    x_plan.denom = x_denom
    x_plan.morph = x_morph
    x_plan.gogo_want = x_gogo_want
    x_plan.stop_want = x_stop_want
    x_plan.star = x_star
    x_plan.pledge = x_pledge
    x_plan.problem_bool = x_problem_bool

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_heard_tables(cursor)
        x_table_name = "belief_planunit_h_put_agg"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(
            spark_num=x_spark_num,
            face_name=x_face_name,
            moment_label=x_moment_label,
            belief_name=x_belief_name,
        )

        # WHEN
        insert_h_agg_blfplan(cursor, x_objkeysholder, x_plan)

        # THEN
        clean_rope = create_rope(casa_rope, "clean")
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            x_spark_num,
            x_face_name,
            None,
            str(x_belief_name),
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
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_h_agg_blfreas_CreatesTableRowsFor_blfreas_h_agg():
    # sourcery skip: extract-method
    # ESTABLISH
    x_spark_num = 77
    x_face_name = exx.yao
    x_moment_label = 1
    x_belief_name = 2
    x_rope = 3
    x_reason_context = 4
    x_active_requisite = 5
    x_reasonheir = reasonheir_shop(reason_context=x_reason_context)
    x_reasonheir.reason_context = x_reason_context
    x_reasonheir.active_requisite = x_active_requisite

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_heard_tables(cursor)
        x_table_name = "belief_plan_reasonunit_h_put_agg"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(
            spark_num=x_spark_num,
            face_name=x_face_name,
            moment_label=x_moment_label,
            belief_name=x_belief_name,
            rope=x_rope,
        )

        # WHEN
        insert_h_agg_blfreas(cursor, x_objkeysholder, x_reasonheir)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            x_spark_num,
            x_face_name,
            str(x_moment_label),
            str(x_belief_name),
            str(x_rope),
            str(x_reason_context),
            x_active_requisite,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_h_agg_blfcase_CreatesTableRowsFor_blfcase_h_agg():
    # sourcery skip: extract-method
    # ESTABLISH
    x_spark_num = 77
    x_face_name = exx.yao
    x_moment_label = 1
    x_belief_name = 2
    x_rope = 3
    x_reason_context = 4
    x_reason_state = 5
    x_reason_lower_otx = 7.0
    x_reason_upper_otx = 6.0
    x_reason_lower_inx = None
    x_reason_upper_inx = None
    x_reason_divisor = 8
    x_caseunit = caseunit_shop(reason_state=x_reason_state)
    x_caseunit.reason_state = x_reason_state
    x_caseunit.reason_lower = x_reason_lower_otx
    x_caseunit.reason_upper = x_reason_upper_otx
    x_caseunit.reason_divisor = x_reason_divisor

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_heard_tables(cursor)
        x_table_name = "belief_plan_reason_caseunit_h_put_agg"
        print(
            f"{get_table_columns(cursor, x_table_name)=} {len(get_table_columns(cursor, x_table_name))=}"
        )
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(
            spark_num=x_spark_num,
            face_name=x_face_name,
            moment_label=x_moment_label,
            belief_name=x_belief_name,
            rope=x_rope,
            reason_context=x_reason_context,
        )

        # WHEN
        insert_h_agg_blfcase(cursor, x_objkeysholder, x_caseunit)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            x_spark_num,
            x_face_name,
            str(x_moment_label),
            str(x_belief_name),
            str(x_rope),
            str(x_reason_context),
            str(x_reason_state),
            x_reason_lower_otx,
            x_reason_lower_inx,
            x_reason_upper_otx,
            x_reason_upper_inx,
            x_reason_divisor,
        )
        expected_data = [expected_row1]
        assert len(rows[0]) == len(expected_data[0])
        assert rows == expected_data


# def test_insert_h_agg_blfmemb_CreatesTableRowsFor_blfmemb_h_agg():
#     # sourcery skip: extract-method
#     # ESTABLISH
#     # x_args = get_belief_calc_dimen_args("belief_voice_membership")
#     # x_count = 0
#     # for x_arg in get_default_sorted_list(x_args):
#     #     x_count += 1
#     #     print(f"    x_{x_arg} = {x_count}")
#     # print("")
#     # for x_arg in get_default_sorted_list(x_args):
#     #     print(f"""    x_membership.{x_arg} = x_{x_arg}""")
#     # print("")
#     # for x_arg in get_default_sorted_list(x_args):
#     #     print(f"""            x_{x_arg},""")

#     x_spark_num = 77
#     x_face_name = exx.yao
#     x_moment_label = 1
#     x_belief_name = 2
#     x_voice_name = 3
#     x_group_title = 4
#     x_group_cred_lumen = 5.0
#     x_group_debt_lumen = 6.0
#     x_credor_pool = 7.0
#     x_debtor_pool = 8.0
#     x_fund_give = 9.0
#     x_fund_take = 10.0
#     x_fund_agenda_give = 11.0
#     x_fund_agenda_take = 12.0
#     x_fund_agenda_ratio_give = 13.0
#     x_fund_agenda_ratio_take = 14.0
#     x_membership = membership_shop(x_group_title)
#     x_membership.voice_name = x_voice_name
#     x_membership.group_cred_lumen = x_group_cred_lumen
#     x_membership.group_debt_lumen = x_group_debt_lumen
#     x_membership.credor_pool = x_credor_pool
#     x_membership.debtor_pool = x_debtor_pool
#     x_membership.fund_give = x_fund_give
#     x_membership.fund_take = x_fund_take
#     x_membership.fund_agenda_give = x_fund_agenda_give
#     x_membership.fund_agenda_take = x_fund_agenda_take
#     x_membership.fund_agenda_ratio_give = x_fund_agenda_ratio_give
#     x_membership.fund_agenda_ratio_take = x_fund_agenda_ratio_take

#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_sound_and_heard_tables(cursor)
#         x_table_name = "belief_voice_membership_h_put_agg"
#         assert get_row_count(cursor, x_table_name) == 0
#         x_objkeysholder = ObjKeysHolder(spark_num=x_spark_num, face_name=x_face_name, moment_label=x_moment_label, belief_name=x_belief_name)

#         # WHEN
#         insert_h_agg_blfmemb(cursor, x_objkeysholder, x_membership)

#         # THEN
#         assert get_row_count(cursor, x_table_name) == 1
#         select_sqlstr = f"SELECT * FROM {x_table_name};"
#         cursor.execute(select_sqlstr)
#         rows = cursor.fetchall()
#         expected_row1 = (
#             x_spark_num,
#             x_face_name,
#             str(x_moment_label),
#             str(x_belief_name),
#             str(x_voice_name),
#             str(x_group_title),
#             x_group_cred_lumen,
#             x_group_debt_lumen,
#             x_credor_pool,
#             x_debtor_pool,
#             x_fund_give,
#             x_fund_take,
#             x_fund_agenda_give,
#             x_fund_agenda_take,
#             x_fund_agenda_ratio_give,
#             x_fund_agenda_ratio_take,
#         )
#         expected_data = [expected_row1]
#         assert rows == expected_data


# def test_insert_h_agg_blfvoce_CreatesTableRowsFor_blfvoce_h_agg():
#     # sourcery skip: extract-method
#     # ESTABLISH
#     # x_args = get_belief_calc_dimen_args("belief_voiceunit")
#     # x_count = 0
#     # for x_arg in get_default_sorted_list(x_args):
#     #     x_count += 1
#     #     print(f"    x_{x_arg} = {x_count}")
#     # print("")
#     # for x_arg in get_default_sorted_list(x_args):
#     #     print(f"""    x_voice.{x_arg} = x_{x_arg}""")
#     # print("")
#     # for x_arg in get_default_sorted_list(x_args):
#     #     print(f"""            x_{x_arg},""")

#     x_spark_num = 77
#     x_face_name = exx.yao
#     x_moment_label = 1
#     x_belief_name = 2
#     x_voice_name = 3
#     x_voice_cred_lumen = 4
#     x_voice_debt_lumen = 5
#     x_credor_pool = 6
#     x_debtor_pool = 7
#     x_fund_give = 8
#     x_fund_take = 9
#     x_fund_agenda_give = 10
#     x_fund_agenda_take = 11
#     x_fund_agenda_ratio_give = 12
#     x_fund_agenda_ratio_take = 13
#     x_inallocable_voice_debt_lumen = 14
#     x_irrational_voice_debt_lumen = 15
#     x_groupmark = 16
#     x_voice = voiceunit_shop(x_voice_name)
#     x_voice.voice_name = x_voice_name
#     x_voice.voice_cred_lumen = x_voice_cred_lumen
#     x_voice.voice_debt_lumen = x_voice_debt_lumen
#     x_voice.credor_pool = x_credor_pool
#     x_voice.debtor_pool = x_debtor_pool
#     x_voice.fund_give = x_fund_give
#     x_voice.fund_take = x_fund_take
#     x_voice.fund_agenda_give = x_fund_agenda_give
#     x_voice.fund_agenda_take = x_fund_agenda_take
#     x_voice.fund_agenda_ratio_give = x_fund_agenda_ratio_give
#     x_voice.fund_agenda_ratio_take = x_fund_agenda_ratio_take
#     x_voice.inallocable_voice_debt_lumen = x_inallocable_voice_debt_lumen
#     x_voice.irrational_voice_debt_lumen = x_irrational_voice_debt_lumen
#     x_voice.groupmark = x_groupmark

#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_sound_and_heard_tables(cursor)
#         x_table_name = "belief_voiceunit_h_put_agg"
#         assert get_row_count(cursor, x_table_name) == 0
#         x_objkeysholder = ObjKeysHolder(spark_num=x_spark_num, face_name=x_face_name, moment_label=x_moment_label, belief_name=x_belief_name)

#         # WHEN
#         insert_h_agg_blfvoce(cursor, x_objkeysholder, x_voice)

#         # THEN
#         assert get_row_count(cursor, x_table_name) == 1
#         select_sqlstr = f"SELECT * FROM {x_table_name};"
#         cursor.execute(select_sqlstr)
#         rows = cursor.fetchall()
#         expected_row1 = (
#             x_spark_num,
#             x_face_name,
#             str(x_moment_label),
#             str(x_belief_name),
#             str(x_voice_name),
#             x_voice_cred_lumen,
#             x_voice_debt_lumen,
#             str(x_groupmark),
#             x_credor_pool,
#             x_debtor_pool,
#             x_fund_give,
#             x_fund_take,
#             x_fund_agenda_give,
#             x_fund_agenda_take,
#             x_fund_agenda_ratio_give,
#             x_fund_agenda_ratio_take,
#             x_inallocable_voice_debt_lumen,
#             x_irrational_voice_debt_lumen,
#         )
#         expected_data = [expected_row1]
#         assert rows == expected_data


# def test_insert_h_agg_blfgrou_CreatesTableRowsFor_blfgrou_h_agg():
#     # sourcery skip: extract-method
#     # ESTABLISH
#     # x_args = get_belief_calc_dimen_args("belief_groupunit")
#     # x_count = 0
#     # for x_arg in get_default_sorted_list(x_args):
#     #     x_count += 1
#     #     print(f"    x_{x_arg} = {x_count}")
#     # print("")
#     # for x_arg in get_default_sorted_list(x_args):
#     #     print(f"""    x_group.{x_arg} = x_{x_arg}""")
#     # print("")
#     # for x_arg in get_default_sorted_list(x_args):
#     #     print(f"""            x_{x_arg},""")

#     x_spark_num = 77
#     x_face_name = exx.yao
#     x_moment_label = 1
#     x_belief_name = 2
#     x_group_title = 3
#     x_fund_grain = 4
#     x_credor_pool = 6
#     x_debtor_pool = 7
#     x_fund_give = 8
#     x_fund_take = 9
#     x_fund_agenda_give = 10
#     x_fund_agenda_take = 11
#     x_group = groupunit_shop(x_group_title)
#     x_group.group_title = x_group_title
#     x_group.fund_grain = x_fund_grain
#     x_group.credor_pool = x_credor_pool
#     x_group.debtor_pool = x_debtor_pool
#     x_group.fund_give = x_fund_give
#     x_group.fund_take = x_fund_take
#     x_group.fund_agenda_give = x_fund_agenda_give
#     x_group.fund_agenda_take = x_fund_agenda_take

#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_sound_and_heard_tables(cursor)
#         x_table_name = "belief_groupunit_h_put_agg"
#         assert get_row_count(cursor, x_table_name) == 0
#         x_objkeysholder = ObjKeysHolder(spark_num=x_spark_num, face_name=x_face_name, moment_label=x_moment_label, belief_name=x_belief_name)

#         # WHEN
#         insert_h_agg_blfgrou(cursor, x_objkeysholder, x_group)

#         # THEN
#         assert get_row_count(cursor, x_table_name) == 1
#         select_sqlstr = f"SELECT * FROM {x_table_name};"
#         cursor.execute(select_sqlstr)
#         rows = cursor.fetchall()
#         expected_row1 = (
#             x_spark_num,
#             x_face_name,
#             str(x_moment_label),
#             str(x_belief_name),
#             str(x_group_title),
#             x_fund_grain,
#             x_credor_pool,
#             x_debtor_pool,
#             x_fund_give,
#             x_fund_take,
#             x_fund_agenda_give,
#             x_fund_agenda_take,
#         )
#         expected_data = [expected_row1]
#         assert rows == expected_data


# def test_insert_h_agg_blfawar_CreatesTableRowsFor_blfawar_h_agg():
#     # sourcery skip: extract-method
#     # ESTABLISH
#     # x_args = get_belief_calc_dimen_args("belief_plan_awardunit")
#     # x_count = 0
#     # for x_arg in get_default_sorted_list(x_args):
#     #     x_count += 1
#     #     print(f"    x_{x_arg} = {x_count}")
#     # print("")
#     # for x_arg in get_default_sorted_list(x_args):
#     #     print(f"""    x_awardheir.{x_arg} = x_{x_arg}""")
#     # print("")
#     # for x_arg in get_default_sorted_list(x_args):
#     #     print(f"""            x_{x_arg},""")

#     x_spark_num = 77
#     x_face_name = exx.yao
#     x_moment_label = 1
#     x_belief_name = 2
#     x_rope = 3
#     x_awardee_title = 4
#     x_give_force = 5
#     x_take_force = 6
#     x_fund_give = 7
#     x_fund_take = 8
#     x_awardheir = awardheir_shop(x_awardee_title)
#     x_awardheir.awardee_title = x_awardee_title
#     x_awardheir.give_force = x_give_force
#     x_awardheir.take_force = x_take_force
#     x_awardheir.fund_give = x_fund_give
#     x_awardheir.fund_take = x_fund_take

#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_sound_and_heard_tables(cursor)
#         x_table_name = "belief_plan_awardunit_h_put_agg"
#         assert get_row_count(cursor, x_table_name) == 0
#         x_objkeysholder = ObjKeysHolder(spark_num=x_spark_num, face_name=x_face_name, moment_label=x_moment_label, belief_name=x_belief_name, rope=x_rope)

#         # WHEN
#         insert_h_agg_blfawar(cursor, x_objkeysholder, x_awardheir)

#         # THEN
#         assert get_row_count(cursor, x_table_name) == 1
#         select_sqlstr = f"SELECT * FROM {x_table_name};"
#         cursor.execute(select_sqlstr)
#         rows = cursor.fetchall()
#         expected_row1 = (
#             x_spark_num,
#             x_face_name,
#             str(x_moment_label),
#             str(x_belief_name),
#             str(x_rope),
#             str(x_awardee_title),
#             x_give_force,
#             x_take_force,
#             x_fund_give,
#             x_fund_take,
#         )
#         expected_data = [expected_row1]
#         assert rows == expected_data


def test_insert_h_agg_blffact_CreatesTableRowsFor_blffact_h_agg():
    # sourcery skip: extract-method
    # ESTABLISH
    x_spark_num = 77
    x_face_name = exx.yao
    x_moment_label = 1
    x_belief_name = 2
    x_rope = 3
    x_reason_context = 4
    x_fact_state = 5
    x_fact_lower_otx = 6
    x_fact_upper_otx = 7
    x_fact_lower_inx = None
    x_fact_upper_inx = None
    x_factheir = factheir_shop()
    x_factheir.fact_context = x_reason_context
    x_factheir.fact_state = x_fact_state
    x_factheir.fact_lower = x_fact_lower_otx
    x_factheir.fact_upper = x_fact_upper_otx

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_heard_tables(cursor)
        x_table_name = "belief_plan_factunit_h_put_agg"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(
            spark_num=x_spark_num,
            face_name=x_face_name,
            moment_label=x_moment_label,
            belief_name=x_belief_name,
            rope=x_rope,
        )

        # WHEN
        insert_h_agg_blffact(cursor, x_objkeysholder, x_factheir)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            x_spark_num,
            x_face_name,
            str(x_moment_label),
            str(x_belief_name),
            str(x_rope),
            str(x_reason_context),
            str(x_fact_state),
            x_fact_lower_otx,
            x_fact_lower_inx,
            x_fact_upper_otx,
            x_fact_upper_inx,
        )
        expected_data = [expected_row1]
        assert len(rows[0]) == len(expected_data[0])
        print(rows[0])
        print(expected_data[0])
        assert rows == expected_data


# def test_insert_h_agg_blfheal_CreatesTableRowsFor_blfheal_h_agg():
#     # sourcery skip: extract-method
#     # ESTABLISH
#     # x_args = get_belief_calc_dimen_args("belief_plan_healerunit")
#     # x_count = 0
#     # for x_arg in get_default_sorted_list(x_args):
#     #     x_count += 1
#     #     print(f"    x_{x_arg} = {x_count}")
#     # print("")
#     # for x_arg in get_default_sorted_list(x_args):
#     #     print(f"""    x_healerunit.{x_arg} = x_{x_arg}""")
#     # print("")
#     # for x_arg in get_default_sorted_list(x_args):
#     #     print(f"""            x_{x_arg},""")

#     x_spark_num = 77
#     x_face_name = exx.yao
#     x_moment_label = 1
#     x_belief_name = 2
#     x_rope = 3
#     x_healerunit = healerunit_shop()
#     x_healerunit.set_healer_name(exx.bob)
#     x_healerunit.set_healer_name(exx.sue)

#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_sound_and_heard_tables(cursor)
#         x_table_name = "belief_plan_healerunit_h_put_agg"
#         assert get_row_count(cursor, x_table_name) == 0
#         x_objkeysholder = ObjKeysHolder(spark_num=x_spark_num, face_name=x_face_name, moment_label=x_moment_label, belief_name=x_belief_name, rope=x_rope)

#         # WHEN
#         insert_h_agg_blfheal(cursor, x_objkeysholder, x_healerunit)

#         # THEN
#         assert get_row_count(cursor, x_table_name) == 2
#         select_sqlstr = f"SELECT * FROM {x_table_name};"
#         cursor.execute(select_sqlstr)
#         rows = cursor.fetchall()
#         expected_row1 = (
#             x_spark_num,
#             x_face_name,
#             str(x_moment_label),
#             str(x_belief_name),
#             str(x_rope),
#             exx.bob,
#         )
#         expected_row2 = (
#             str(x_moment_label),
#             str(x_belief_name),
#             str(x_rope),
#             exx.sue,
#         )
#         expected_data = [expected_row1, expected_row2]
#         assert rows == expected_data


# def test_insert_h_agg_blflabo_CreatesTableRowsFor_blflabo_h_agg():
#     # sourcery skip: extract-method
#     # ESTABLISH
#     # x_args = get_belief_calc_dimen_args("belief_plan_partyunit")
#     # x_count = 0
#     # for x_arg in get_default_sorted_list(x_args):
#     #     x_count += 1
#     #     print(f"    x_{x_arg} = {x_count}")
#     # print("")
#     # for x_arg in get_default_sorted_list(x_args):
#     #     print(f"""    x_laborheir.{x_arg} = x_{x_arg}""")
#     # print("")
#     # for x_arg in get_default_sorted_list(x_args):
#     #     print(f"""            x_{x_arg},""")

#     x_spark_num = 77
#     x_face_name = exx.yao
#     x_moment_label = 1
#     x_belief_name = 2
#     x_rope = 3
#     x__belief_name_is_labor = 5
#     x_laborheir = laborheir_shop()
#     x_laborheir.belief_name_is_labor = x__belief_name_is_labor
#     bob_solo_bool = 6
#     sue_solo_bool = 7
#     bob_partyheir = partyheir_shop(exx.bob, bob_solo_bool)
#     sue_partyheir = partyheir_shop(exx.sue, sue_solo_bool)
#     x_laborheir.partys = {exx.bob: bob_partyheir, exx.sue: sue_partyheir}

#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_sound_and_heard_tables(cursor)
#         x_table_name = "belief_plan_partyunit_h_put_agg"
#         assert get_row_count(cursor, x_table_name) == 0
#         x_objkeysholder = ObjKeysHolder(spark_num=x_spark_num, face_name=x_face_name, moment_label=x_moment_label, belief_name=x_belief_name, rope=x_rope)

#         # WHEN
#         insert_h_agg_blflabo(cursor, x_objkeysholder, x_laborheir)

#         # THEN
#         assert get_row_count(cursor, x_table_name) == 2
#         select_sqlstr = f"SELECT * FROM {x_table_name};"
#         cursor.execute(select_sqlstr)
#         rows = cursor.fetchall()
#         expected_row1 = (
#             x_spark_num,
#             x_face_name,
#             str(x_moment_label),
#             str(x_belief_name),
#             str(x_rope),
#             exx.bob,
#             bob_solo_bool,
#             x__belief_name_is_labor,
#         )
#         expected_row2 = (
#             str(x_moment_label),
#             str(x_belief_name),
#             str(x_rope),
#             exx.sue,
#             sue_solo_bool,
#             x__belief_name_is_labor,
#         )
#         expected_data = [expected_row1, expected_row2]
#         assert rows == expected_data


def test_insert_h_agg_obj_CreatesTableRows_Scenario0_ContextNumRelevantTables():
    # sourcery skip: extract-method
    # ESTABLISH
    sue_belief = beliefunit_shop(exx.sue, exx.a23)
    sue_belief.add_voiceunit(exx.sue)
    sue_belief.add_voiceunit(exx.bob)
    sue_belief.get_voice(exx.bob).add_membership(exx.run)
    casa_rope = sue_belief.make_l1_rope("casa")
    situation_rope = sue_belief.make_l1_rope(kw.reason_active)
    clean_rope = sue_belief.make_rope(situation_rope, "clean")
    dirty_rope = sue_belief.make_rope(situation_rope, "dirty")
    sue_belief.add_plan(casa_rope)
    sue_belief.add_plan(clean_rope)
    sue_belief.add_plan(dirty_rope)
    sue_belief.edit_plan_attr(
        casa_rope, reason_context=situation_rope, reason_case=dirty_rope
    )
    sue_belief.edit_plan_attr(casa_rope, awardunit=awardunit_shop(exx.run))
    sue_belief.edit_plan_attr(casa_rope, healerunit=healerunit_shop({exx.bob}))
    casa_laborunit = laborunit_shop()
    casa_laborunit.add_party(exx.sue, True)
    sue_belief.edit_plan_attr(casa_rope, laborunit=casa_laborunit)
    sue_belief.add_fact(situation_rope, clean_rope)

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_heard_tables(cursor)
        blffact_h_agg_table = f"{kw.belief_plan_factunit}_h_put_agg"
        blfcase_h_agg_table = f"{kw.belief_plan_reason_caseunit}_h_put_agg"
        blfreas_h_agg_table = f"{kw.belief_plan_reasonunit}_h_put_agg"
        blfplan_h_agg_table = f"{kw.belief_planunit}_h_put_agg"
        blfunit_h_agg_table = f"{kw.beliefunit}_h_put_agg"
        assert get_row_count(cursor, blfunit_h_agg_table) == 0
        assert get_row_count(cursor, blfplan_h_agg_table) == 0
        assert get_row_count(cursor, blffact_h_agg_table) == 0
        assert get_row_count(cursor, blfreas_h_agg_table) == 0
        assert get_row_count(cursor, blfcase_h_agg_table) == 0

        # WHEN
        insert_h_agg_obj(cursor, sue_belief)

        # THEN
        assert get_row_count(cursor, blfunit_h_agg_table) == 1
        assert get_row_count(cursor, blfplan_h_agg_table) == 5
        assert get_row_count(cursor, blffact_h_agg_table) == 1
        assert get_row_count(cursor, blfreas_h_agg_table) == 1
        assert get_row_count(cursor, blfcase_h_agg_table) == 1


# def test_insert_h_agg_obj_CreatesTableRows_Scenario1_AllTables():
#     # sourcery skip: extract-method
#     # ESTABLISH
#     sue_belief = beliefunit_shop(exx.sue, exx.a23)
#     sue_belief.add_voiceunit(exx.sue)
#     sue_belief.add_voiceunit(exx.bob)
#     sue_belief.get_voice(exx.bob).add_membership(exx.run)
#     casa_rope = sue_belief.make_l1_rope("casa")
#     situation_rope = sue_belief.make_l1_rope(kw.reason_active)
#     clean_rope = sue_belief.make_rope(situation_rope, "clean")
#     dirty_rope = sue_belief.make_rope(situation_rope, "dirty")
#     sue_belief.add_plan(casa_rope)
#     sue_belief.add_plan(clean_rope)
#     sue_belief.add_plan(dirty_rope)
#     sue_belief.edit_plan_attr(
#         casa_rope, reason_context=situation_rope, reason_case=dirty_rope
#     )
#     sue_belief.edit_plan_attr(casa_rope, awardunit=awardunit_shop(exx.run))
#     sue_belief.edit_plan_attr(casa_rope, healerunit=healerunit_shop({exx.bob}))
#     casa_laborunit = laborunit_shop()
#     casa_laborunit.add_party(exx.sue, True)
#     sue_belief.edit_plan_attr(casa_rope, laborunit=casa_laborunit)
#     sue_belief.add_fact(situation_rope, clean_rope)

#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_sound_and_heard_tables(cursor)
#         blfmemb_h_agg_table = f"{kw.belief_voice_membership}_h_put_agg"
#         blfvoce_h_agg_table = f"{kw.belief_voiceunit}_h_put_agg"
#         blfgrou_h_agg_table = f"{kw.belief_groupunit}_h_put_agg"
#         blfawar_h_agg_table = f"{kw.belief_plan_awardunit}_h_put_agg"
#         blffact_h_agg_table = f"{kw.belief_plan_factunit}_h_put_agg"
#         blfheal_h_agg_table = f"{kw.belief_plan_healerunit}_h_put_agg"
#         blfcase_h_agg_table = f"{kw.belief_plan_reason_caseunit}_h_put_agg"
#         blfreas_h_agg_table = f"{kw.belief_plan_reasonunit}_h_put_agg"
#         blflabo_h_agg_table = f"{kw.belief_plan_partyunit}_h_put_agg"
#         blfplan_h_agg_table = f"{kw.belief_planunit}_h_put_agg"
#         blfunit_h_agg_table = f"{kw.beliefunit}_h_put_agg"
#         assert get_row_count(cursor, blfunit_h_agg_table) == 0
#         assert get_row_count(cursor, blfplan_h_agg_table) == 0
#         assert get_row_count(cursor, blfvoce_h_agg_table) == 0
#         assert get_row_count(cursor, blfmemb_h_agg_table) == 0
#         assert get_row_count(cursor, blfgrou_h_agg_table) == 0
#         assert get_row_count(cursor, blfawar_h_agg_table) == 0
#         assert get_row_count(cursor, blffact_h_agg_table) == 0
#         assert get_row_count(cursor, blfheal_h_agg_table) == 0
#         assert get_row_count(cursor, blfreas_h_agg_table) == 0
#         assert get_row_count(cursor, blfcase_h_agg_table) == 0
#         assert get_row_count(cursor, blflabo_h_agg_table) == 0

#         # WHEN
#         insert_h_agg_obj(cursor, sue_belief)

#         # THEN
#         assert get_row_count(cursor, blfunit_h_agg_table) == 1
#         assert get_row_count(cursor, blfplan_h_agg_table) == 5
#         assert get_row_count(cursor, blfvoce_h_agg_table) == 2
#         assert get_row_count(cursor, blfmemb_h_agg_table) == 3
#         assert get_row_count(cursor, blfgrou_h_agg_table) == 3
#         assert get_row_count(cursor, blfawar_h_agg_table) == 1
#         assert get_row_count(cursor, blffact_h_agg_table) == 1
#         assert get_row_count(cursor, blfheal_h_agg_table) == 1
#         assert get_row_count(cursor, blfreas_h_agg_table) == 1
#         assert get_row_count(cursor, blfcase_h_agg_table) == 1
#         assert get_row_count(cursor, blflabo_h_agg_table) == 1
