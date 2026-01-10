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
from src.ch06_keg.healer import healerunit_shop
from src.ch06_keg.keg import kegunit_shop
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch18_world_etl.etl_sqlstr import create_sound_and_heard_tables
from src.ch18_world_etl.obj2db_plan import (
    ObjKeysHolder,
    insert_h_agg_obj,
    insert_h_agg_plnawar,
    insert_h_agg_plncase,
    insert_h_agg_plnfact,
    insert_h_agg_plngrou,
    insert_h_agg_plnheal,
    insert_h_agg_plnkegg,
    insert_h_agg_plnlabo,
    insert_h_agg_plnmemb,
    insert_h_agg_plnreas,
    insert_h_agg_plnunit,
    insert_h_agg_plnvoce,
)
from src.ch18_world_etl.test._util.ch18_env import temp_dir_setup
from src.ref.keywords import Ch18Keywords as kw, ExampleStrs as exx


def test_insert_h_agg_plnunit_CreatesTableRowsFor_planunit_h_agg():
    # sourcery skip: extract-method
    # ESTABLISH
    x_spark_num = 77
    x_face_name = exx.yao
    # TODO replace all exx.a23 references in tests to exx.a23
    x_moment_label = exx.a23
    x_plan_name = "Sue"
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
    sue_plan.credor_respect = x_credor_respect
    sue_plan.debtor_respect = x_debtor_respect

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_heard_tables(cursor)
        x_table_name = "planunit_h_put_agg"
        assert get_row_count(cursor, x_table_name) == 0
        objkeysholder = ObjKeysHolder(x_spark_num, x_face_name)

        # WHEN
        insert_h_agg_plnunit(cursor, objkeysholder, sue_plan)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            x_spark_num,
            x_face_name,
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
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_h_agg_plnkegg_CreatesTableRowsFor_plnkegg_h_agg():
    # sourcery skip: extract-method
    # ESTABLISH
    x_spark_num = 77
    x_face_name = exx.yao
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

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_heard_tables(cursor)
        x_table_name = "plan_kegunit_h_put_agg"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(
            spark_num=x_spark_num,
            face_name=x_face_name,
            moment_label=x_moment_label,
            plan_name=x_plan_name,
        )

        # WHEN
        insert_h_agg_plnkegg(cursor, x_objkeysholder, x_keg)

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
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_h_agg_plnreas_CreatesTableRowsFor_plnreas_h_agg():
    # sourcery skip: extract-method
    # ESTABLISH
    x_spark_num = 77
    x_face_name = exx.yao
    x_moment_label = 1
    x_plan_name = 2
    x_rope = 3
    x_reason_context = 4
    x_active_requisite = 5
    x_reasonheir = reasonheir_shop(reason_context=x_reason_context)
    x_reasonheir.reason_context = x_reason_context
    x_reasonheir.active_requisite = x_active_requisite

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_heard_tables(cursor)
        x_table_name = "plan_keg_reasonunit_h_put_agg"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(
            spark_num=x_spark_num,
            face_name=x_face_name,
            moment_label=x_moment_label,
            plan_name=x_plan_name,
            rope=x_rope,
        )

        # WHEN
        insert_h_agg_plnreas(cursor, x_objkeysholder, x_reasonheir)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            x_spark_num,
            x_face_name,
            str(x_moment_label),
            str(x_plan_name),
            str(x_rope),
            str(x_reason_context),
            x_active_requisite,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_h_agg_plncase_CreatesTableRowsFor_plncase_h_agg():
    # sourcery skip: extract-method
    # ESTABLISH
    x_spark_num = 77
    x_face_name = exx.yao
    x_moment_label = 1
    x_plan_name = 2
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
        x_table_name = "plan_keg_reason_caseunit_h_put_agg"
        print(
            f"{get_table_columns(cursor, x_table_name)=} {len(get_table_columns(cursor, x_table_name))=}"
        )
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(
            spark_num=x_spark_num,
            face_name=x_face_name,
            moment_label=x_moment_label,
            plan_name=x_plan_name,
            rope=x_rope,
            reason_context=x_reason_context,
        )

        # WHEN
        insert_h_agg_plncase(cursor, x_objkeysholder, x_caseunit)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            x_spark_num,
            x_face_name,
            str(x_moment_label),
            str(x_plan_name),
            str(x_rope),
            str(x_reason_context),
            str(x_reason_state),
            x_reason_lower_otx,
            x_reason_lower_inx,
            x_reason_upper_otx,
            x_reason_upper_inx,
            x_reason_divisor,
            None,
            None,
            None,
            None,
        )
        expected_data = [expected_row1]
        assert len(rows[0]) == len(expected_data[0])
        assert rows == expected_data


# def test_insert_h_agg_plnmemb_CreatesTableRowsFor_plnmemb_h_agg():
#     # sourcery skip: extract-method
#     # ESTABLISH
#     # x_args = get_plan_calc_dimen_args("plan_voice_membership")
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
#     x_plan_name = 2
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
#         x_table_name = "plan_voice_membership_h_put_agg"
#         assert get_row_count(cursor, x_table_name) == 0
#         x_objkeysholder = ObjKeysHolder(spark_num=x_spark_num, face_name=x_face_name, moment_label=x_moment_label, plan_name=x_plan_name)

#         # WHEN
#         insert_h_agg_plnmemb(cursor, x_objkeysholder, x_membership)

#         # THEN
#         assert get_row_count(cursor, x_table_name) == 1
#         select_sqlstr = f"SELECT * FROM {x_table_name};"
#         cursor.execute(select_sqlstr)
#         rows = cursor.fetchall()
#         expected_row1 = (
#             x_spark_num,
#             x_face_name,
#             str(x_moment_label),
#             str(x_plan_name),
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


# def test_insert_h_agg_plnvoce_CreatesTableRowsFor_plnvoce_h_agg():
#     # sourcery skip: extract-method
#     # ESTABLISH
#     # x_args = get_plan_calc_dimen_args("plan_voiceunit")
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
#     x_plan_name = 2
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
#         x_table_name = "plan_voiceunit_h_put_agg"
#         assert get_row_count(cursor, x_table_name) == 0
#         x_objkeysholder = ObjKeysHolder(spark_num=x_spark_num, face_name=x_face_name, moment_label=x_moment_label, plan_name=x_plan_name)

#         # WHEN
#         insert_h_agg_plnvoce(cursor, x_objkeysholder, x_voice)

#         # THEN
#         assert get_row_count(cursor, x_table_name) == 1
#         select_sqlstr = f"SELECT * FROM {x_table_name};"
#         cursor.execute(select_sqlstr)
#         rows = cursor.fetchall()
#         expected_row1 = (
#             x_spark_num,
#             x_face_name,
#             str(x_moment_label),
#             str(x_plan_name),
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


# def test_insert_h_agg_plngrou_CreatesTableRowsFor_plngrou_h_agg():
#     # sourcery skip: extract-method
#     # ESTABLISH
#     # x_args = get_plan_calc_dimen_args("plan_groupunit")
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
#     x_plan_name = 2
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
#         x_table_name = "plan_groupunit_h_put_agg"
#         assert get_row_count(cursor, x_table_name) == 0
#         x_objkeysholder = ObjKeysHolder(spark_num=x_spark_num, face_name=x_face_name, moment_label=x_moment_label, plan_name=x_plan_name)

#         # WHEN
#         insert_h_agg_plngrou(cursor, x_objkeysholder, x_group)

#         # THEN
#         assert get_row_count(cursor, x_table_name) == 1
#         select_sqlstr = f"SELECT * FROM {x_table_name};"
#         cursor.execute(select_sqlstr)
#         rows = cursor.fetchall()
#         expected_row1 = (
#             x_spark_num,
#             x_face_name,
#             str(x_moment_label),
#             str(x_plan_name),
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


# def test_insert_h_agg_plnawar_CreatesTableRowsFor_plnawar_h_agg():
#     # sourcery skip: extract-method
#     # ESTABLISH
#     # x_args = get_plan_calc_dimen_args("plan_keg_awardunit")
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
#     x_plan_name = 2
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
#         x_table_name = "plan_keg_awardunit_h_put_agg"
#         assert get_row_count(cursor, x_table_name) == 0
#         x_objkeysholder = ObjKeysHolder(spark_num=x_spark_num, face_name=x_face_name, moment_label=x_moment_label, plan_name=x_plan_name, rope=x_rope)

#         # WHEN
#         insert_h_agg_plnawar(cursor, x_objkeysholder, x_awardheir)

#         # THEN
#         assert get_row_count(cursor, x_table_name) == 1
#         select_sqlstr = f"SELECT * FROM {x_table_name};"
#         cursor.execute(select_sqlstr)
#         rows = cursor.fetchall()
#         expected_row1 = (
#             x_spark_num,
#             x_face_name,
#             str(x_moment_label),
#             str(x_plan_name),
#             str(x_rope),
#             str(x_awardee_title),
#             x_give_force,
#             x_take_force,
#             x_fund_give,
#             x_fund_take,
#         )
#         expected_data = [expected_row1]
#         assert rows == expected_data


def test_insert_h_agg_plnfact_CreatesTableRowsFor_plnfact_h_agg():
    # sourcery skip: extract-method
    # ESTABLISH
    x_spark_num = 77
    x_face_name = exx.yao
    x_moment_label = 1
    x_plan_name = 2
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
        x_table_name = "plan_keg_factunit_h_put_agg"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(
            spark_num=x_spark_num,
            face_name=x_face_name,
            moment_label=x_moment_label,
            plan_name=x_plan_name,
            rope=x_rope,
        )

        # WHEN
        insert_h_agg_plnfact(cursor, x_objkeysholder, x_factheir)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            x_spark_num,
            x_face_name,
            str(x_moment_label),
            str(x_plan_name),
            str(x_rope),
            str(x_reason_context),
            str(x_fact_state),
            x_fact_lower_otx,
            x_fact_lower_inx,
            x_fact_upper_otx,
            x_fact_upper_inx,
            None,
            None,
            None,
            None,
        )
        expected_data = [expected_row1]
        assert len(rows[0]) == len(expected_data[0])
        print(rows[0])
        print(expected_data[0])
        assert rows == expected_data


# def test_insert_h_agg_plnheal_CreatesTableRowsFor_plnheal_h_agg():
#     # sourcery skip: extract-method
#     # ESTABLISH
#     # x_args = get_plan_calc_dimen_args("plan_keg_healerunit")
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
#     x_plan_name = 2
#     x_rope = 3
#     x_healerunit = healerunit_shop()
#     x_healerunit.set_healer_name(exx.bob)
#     x_healerunit.set_healer_name(exx.sue)

#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_sound_and_heard_tables(cursor)
#         x_table_name = "plan_keg_healerunit_h_put_agg"
#         assert get_row_count(cursor, x_table_name) == 0
#         x_objkeysholder = ObjKeysHolder(spark_num=x_spark_num, face_name=x_face_name, moment_label=x_moment_label, plan_name=x_plan_name, rope=x_rope)

#         # WHEN
#         insert_h_agg_plnheal(cursor, x_objkeysholder, x_healerunit)

#         # THEN
#         assert get_row_count(cursor, x_table_name) == 2
#         select_sqlstr = f"SELECT * FROM {x_table_name};"
#         cursor.execute(select_sqlstr)
#         rows = cursor.fetchall()
#         expected_row1 = (
#             x_spark_num,
#             x_face_name,
#             str(x_moment_label),
#             str(x_plan_name),
#             str(x_rope),
#             exx.bob,
#         )
#         expected_row2 = (
#             str(x_moment_label),
#             str(x_plan_name),
#             str(x_rope),
#             exx.sue,
#         )
#         expected_data = [expected_row1, expected_row2]
#         assert rows == expected_data


# def test_insert_h_agg_plnlabo_CreatesTableRowsFor_plnlabo_h_agg():
#     # sourcery skip: extract-method
#     # ESTABLISH
#     # x_args = get_plan_calc_dimen_args("plan_keg_partyunit")
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
#     x_plan_name = 2
#     x_rope = 3
#     x__plan_name_is_labor = 5
#     x_laborheir = laborheir_shop()
#     x_laborheir.plan_name_is_labor = x__plan_name_is_labor
#     bob_solo_bool = 6
#     sue_solo_bool = 7
#     bob_partyheir = partyheir_shop(exx.bob, bob_solo_bool)
#     sue_partyheir = partyheir_shop(exx.sue, sue_solo_bool)
#     x_laborheir.partys = {exx.bob: bob_partyheir, exx.sue: sue_partyheir}

#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_sound_and_heard_tables(cursor)
#         x_table_name = "plan_keg_partyunit_h_put_agg"
#         assert get_row_count(cursor, x_table_name) == 0
#         x_objkeysholder = ObjKeysHolder(spark_num=x_spark_num, face_name=x_face_name, moment_label=x_moment_label, plan_name=x_plan_name, rope=x_rope)

#         # WHEN
#         insert_h_agg_plnlabo(cursor, x_objkeysholder, x_laborheir)

#         # THEN
#         assert get_row_count(cursor, x_table_name) == 2
#         select_sqlstr = f"SELECT * FROM {x_table_name};"
#         cursor.execute(select_sqlstr)
#         rows = cursor.fetchall()
#         expected_row1 = (
#             x_spark_num,
#             x_face_name,
#             str(x_moment_label),
#             str(x_plan_name),
#             str(x_rope),
#             exx.bob,
#             bob_solo_bool,
#             x__plan_name_is_labor,
#         )
#         expected_row2 = (
#             str(x_moment_label),
#             str(x_plan_name),
#             str(x_rope),
#             exx.sue,
#             sue_solo_bool,
#             x__plan_name_is_labor,
#         )
#         expected_data = [expected_row1, expected_row2]
#         assert rows == expected_data


def test_insert_h_agg_obj_CreatesTableRows_Scenario0_ReasonNumRelevantTables():
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
        create_sound_and_heard_tables(cursor)
        plnfact_h_agg_table = f"{kw.plan_keg_factunit}_h_put_agg"
        plncase_h_agg_table = f"{kw.plan_keg_reason_caseunit}_h_put_agg"
        plnreas_h_agg_table = f"{kw.plan_keg_reasonunit}_h_put_agg"
        plnkegg_h_agg_table = f"{kw.plan_kegunit}_h_put_agg"
        plnunit_h_agg_table = f"{kw.planunit}_h_put_agg"
        assert get_row_count(cursor, plnunit_h_agg_table) == 0
        assert get_row_count(cursor, plnkegg_h_agg_table) == 0
        assert get_row_count(cursor, plnfact_h_agg_table) == 0
        assert get_row_count(cursor, plnreas_h_agg_table) == 0
        assert get_row_count(cursor, plncase_h_agg_table) == 0

        # WHEN
        spark7 = 7
        insert_h_agg_obj(cursor, sue_plan, spark7, face_name=exx.yao)

        # THEN
        assert get_row_count(cursor, plnunit_h_agg_table) == 1
        assert get_row_count(cursor, plnkegg_h_agg_table) == 5
        assert get_row_count(cursor, plnfact_h_agg_table) == 1
        assert get_row_count(cursor, plnreas_h_agg_table) == 1
        assert get_row_count(cursor, plncase_h_agg_table) == 1
        select_case_sqlstr = (
            f"""SELECT spark_num, face_name, moment_label FROM {plncase_h_agg_table};"""
        )
        cursor.execute(select_case_sqlstr)
        assert cursor.fetchall() == [(spark7, exx.yao, exx.a23)]


# def test_insert_h_agg_obj_CreatesTableRows_Scenario1_AllTables():
#     # sourcery skip: extract-method
#     # ESTABLISH
#     sue_plan = planunit_shop(exx.sue, exx.a23)
#     sue_plan.add_voiceunit(exx.sue)
#     sue_plan.add_voiceunit(exx.bob)
#     sue_plan.get_voice(exx.bob).add_membership(exx.run)
#     casa_rope = sue_plan.make_l1_rope("casa")
#     situation_rope = sue_plan.make_l1_rope(kw.reason_active)
#     clean_rope = sue_plan.make_rope(situation_rope, "clean")
#     dirty_rope = sue_plan.make_rope(situation_rope, "dirty")
#     sue_plan.add_keg(casa_rope)
#     sue_plan.add_keg(clean_rope)
#     sue_plan.add_keg(dirty_rope)
#     sue_plan.edit_keg_attr(
#         casa_rope, reason_context=situation_rope, reason_case=dirty_rope
#     )
#     sue_plan.edit_keg_attr(casa_rope, awardunit=awardunit_shop(exx.run))
#     sue_plan.edit_keg_attr(casa_rope, healerunit=healerunit_shop({exx.bob}))
#     casa_laborunit = laborunit_shop()
#     casa_laborunit.add_party(exx.sue, True)
#     sue_plan.edit_keg_attr(casa_rope, laborunit=casa_laborunit)
#     sue_plan.add_fact(situation_rope, clean_rope)

#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_sound_and_heard_tables(cursor)
#         plnmemb_h_agg_table = f"{kw.plan_voice_membership}_h_put_agg"
#         plnvoce_h_agg_table = f"{kw.plan_voiceunit}_h_put_agg"
#         plngrou_h_agg_table = f"{kw.plan_groupunit}_h_put_agg"
#         plnawar_h_agg_table = f"{kw.plan_keg_awardunit}_h_put_agg"
#         plnfact_h_agg_table = f"{kw.plan_keg_factunit}_h_put_agg"
#         plnheal_h_agg_table = f"{kw.plan_keg_healerunit}_h_put_agg"
#         plncase_h_agg_table = f"{kw.plan_keg_reason_caseunit}_h_put_agg"
#         plnreas_h_agg_table = f"{kw.plan_keg_reasonunit}_h_put_agg"
#         plnlabo_h_agg_table = f"{kw.plan_keg_partyunit}_h_put_agg"
#         plnkegg_h_agg_table = f"{kw.plan_kegunit}_h_put_agg"
#         plnunit_h_agg_table = f"{kw.planunit}_h_put_agg"
#         assert get_row_count(cursor, plnunit_h_agg_table) == 0
#         assert get_row_count(cursor, plnkegg_h_agg_table) == 0
#         assert get_row_count(cursor, plnvoce_h_agg_table) == 0
#         assert get_row_count(cursor, plnmemb_h_agg_table) == 0
#         assert get_row_count(cursor, plngrou_h_agg_table) == 0
#         assert get_row_count(cursor, plnawar_h_agg_table) == 0
#         assert get_row_count(cursor, plnfact_h_agg_table) == 0
#         assert get_row_count(cursor, plnheal_h_agg_table) == 0
#         assert get_row_count(cursor, plnreas_h_agg_table) == 0
#         assert get_row_count(cursor, plncase_h_agg_table) == 0
#         assert get_row_count(cursor, plnlabo_h_agg_table) == 0

#         # WHEN
#         insert_h_agg_obj(cursor, sue_plan)

#         # THEN
#         assert get_row_count(cursor, plnunit_h_agg_table) == 1
#         assert get_row_count(cursor, plnkegg_h_agg_table) == 5
#         assert get_row_count(cursor, plnvoce_h_agg_table) == 2
#         assert get_row_count(cursor, plnmemb_h_agg_table) == 3
#         assert get_row_count(cursor, plngrou_h_agg_table) == 3
#         assert get_row_count(cursor, plnawar_h_agg_table) == 1
#         assert get_row_count(cursor, plnfact_h_agg_table) == 1
#         assert get_row_count(cursor, plnheal_h_agg_table) == 1
#         assert get_row_count(cursor, plnreas_h_agg_table) == 1
#         assert get_row_count(cursor, plncase_h_agg_table) == 1
#         assert get_row_count(cursor, plnlabo_h_agg_table) == 1
