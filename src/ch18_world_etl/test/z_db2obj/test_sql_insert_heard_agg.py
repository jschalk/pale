from sqlite3 import connect as sqlite3_connect
from src.ch01_py.db_toolbox import create_insert_query
from src.ch18_world_etl.etl_config import (
    etl_idea_category_config_dict as get_etl_config,
    get_prime_columns,
    remove_inx_columns,
    remove_staging_columns,
)
from src.ch18_world_etl.etl_sqlstr import create_sound_and_heard_tables
from src.ch18_world_etl.obj2db_plan import (
    create_plnawar_h_put_agg_insert_sqlstr,
    create_plncase_h_put_agg_insert_sqlstr,
    create_plnfact_h_put_agg_insert_sqlstr,
    create_plngrou_h_put_agg_insert_sqlstr,
    create_plnheal_h_put_agg_insert_sqlstr,
    create_plnkegg_h_put_agg_insert_sqlstr,
    create_plnlabo_h_put_agg_insert_sqlstr,
    create_plnmemb_h_put_agg_insert_sqlstr,
    create_plnprsn_h_put_agg_insert_sqlstr,
    create_plnreas_h_put_agg_insert_sqlstr,
    create_plnunit_h_put_agg_insert_sqlstr,
)
from src.ref.keywords import Ch18Keywords as kw, ExampleStrs as exx


def test_create_plnunit_h_put_agg_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_moment_label = exx.a23
    x_plan_name = "Sue"
    x_credor_respect = 88.2
    x_debtor_respect = 88.4
    x_fund_grain = 3
    x_fund_pool = 3000
    x_max_tree_traverse = 22
    x_mana_grain = 4
    x_respect_grain = 0.2
    x_tally = 6
    values_dict = {
        kw.spark_num: 77,
        kw.face_name: exx.yao,
        kw.moment_label: x_moment_label,
        kw.plan_name: x_plan_name,
        kw.credor_respect: x_credor_respect,
        kw.debtor_respect: x_debtor_respect,
        kw.fund_grain: x_fund_grain,
        kw.fund_pool: x_fund_pool,
        kw.max_tree_traverse: x_max_tree_traverse,
        kw.mana_grain: x_mana_grain,
        kw.respect_grain: x_respect_grain,
        kw.tally: x_tally,
    }
    etl_config = get_etl_config()
    plnunit = kw.planunit
    dst_columns = get_prime_columns(plnunit, ["h", "agg", "put"], etl_config)
    print(f"{dst_columns=}")
    # all args included in values dict
    assert dst_columns == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_plnunit_h_put_agg_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_heard_tables(cursor)
        table_name = "planunit_h_put_agg"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        # print(expected_sqlstr)
        # print("")
        print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


def test_create_plnkegg_h_put_agg_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_moment_label = exx.a23
    x_plan_name = "Sue"
    x_active = 1
    x_all_person_cred = 2
    x_all_person_debt = 3
    x_descendant_pledge_count = 4
    x_fund_cease = 5
    x_fund_grain = 6
    x_fund_onset = 7
    x_fund_ratio = 8
    x_gogo_calc = 9
    x_healerunit_ratio = 10
    x_tree_level = 11
    x_range_evaluated = 12
    x_stop_calc = 13
    x_task = 14
    x_addin = 15
    x_begin = 16
    x_close = 17
    x_denom = 18
    x_gogo_want = 19
    x_star = 21
    x_morph = 22
    x_numor = 23
    x_rope = 24
    x_pledge = 25
    x_problem_bool = 26
    x_stop_want = 27
    values_dict = {
        kw.spark_num: 77,
        kw.face_name: exx.yao,
        kw.moment_label: x_moment_label,
        kw.plan_name: x_plan_name,
        kw.addin: x_addin,
        kw.begin: x_begin,
        kw.close: x_close,
        kw.denom: x_denom,
        kw.gogo_want: x_gogo_want,
        kw.star: x_star,
        kw.morph: x_morph,
        kw.numor: x_numor,
        kw.keg_rope: x_rope,
        kw.pledge: x_pledge,
        kw.problem_bool: x_problem_bool,
        kw.stop_want: x_stop_want,
    }
    # all args included in values dict
    etl_config = get_etl_config()
    dimen = kw.plan_kegunit
    dst_columns = get_prime_columns(dimen, ["h", "agg", "put"], etl_config)
    print(f"{dst_columns=}")
    assert dst_columns == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_plnkegg_h_put_agg_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_heard_tables(cursor)
        table_name = "plan_kegunit_h_put_agg"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        # print(expected_sqlstr)
        # print("")
        print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


def test_create_plnreas_h_put_agg_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_moment_label = exx.a23
    x_plan_name = "Sue"
    x_rope = 1
    x_reason_context = 2
    x_active_requisite = 3
    values_dict = {
        kw.spark_num: 77,
        kw.face_name: exx.yao,
        kw.moment_label: x_moment_label,
        kw.plan_name: x_plan_name,
        kw.keg_rope: x_rope,
        kw.reason_context: x_reason_context,
        kw.active_requisite: x_active_requisite,
    }
    # all args included in values dict
    etl_config = get_etl_config()
    dimen = kw.plan_keg_reasonunit
    dst_columns = get_prime_columns(dimen, ["h", "agg", "put"], etl_config)
    print(f"{dst_columns=}")
    assert dst_columns == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_plnreas_h_put_agg_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_heard_tables(cursor)
        table_name = "plan_keg_reasonunit_h_put_agg"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        # print(expected_sqlstr)
        print("")
        print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


def test_create_plncase_h_put_agg_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_moment_label = exx.a23
    x_plan_name = "Sue"
    x_rope = 1
    x_reason_context = 2
    x_reason_state = 3
    x_reason_lower = 4
    x_reason_upper = 5
    x_reason_divisor = 6
    values_dict = {
        kw.spark_num: 77,
        kw.face_name: exx.yao,
        kw.moment_label: x_moment_label,
        kw.plan_name: x_plan_name,
        kw.keg_rope: x_rope,
        kw.reason_context: x_reason_context,
        kw.reason_state: x_reason_state,
        f"{kw.reason_lower}_otx": x_reason_lower,
        f"{kw.reason_upper}_otx": x_reason_upper,
        kw.reason_divisor: x_reason_divisor,
    }
    # all args included in values dict
    etl_config = get_etl_config()
    dimen = kw.plan_keg_reason_caseunit
    dst_columns = get_prime_columns(dimen, ["h", "agg", "put"], etl_config)
    dst_columns = remove_inx_columns(dst_columns)
    dst_columns = remove_staging_columns(dst_columns)
    print(f"{dst_columns=}")
    assert dst_columns == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_plncase_h_put_agg_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_heard_tables(cursor)
        table_name = "plan_keg_reason_caseunit_h_put_agg"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        # print(expected_sqlstr)
        print("")
        print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


# def test_create_plnawar_h_put_agg_insert_sqlstr_ReturnsObj():
#     # ESTABLISH
#     x_moment_label = exx.a23
#     x_plan_name = "Sue"
#     x_rope = 1
#     x_awardee_title = 2
#     x_give_force = 3
#     x_take_force = 4
#     x_fund_give = 5
#     x_fund_take = 6
#     values_dict = {
#         kw.spark_num: 77,
#         kw.face_name: exx.yao,
#         kw.moment_label: x_moment_label,
#         kw.plan_name: x_plan_name,
#         kw.keg_rope: x_rope,
#         kw.awardee_title: x_awardee_title,
#         kw.give_force: x_give_force,
#         kw.take_force: x_take_force,
#         kw.fund_give: x_fund_give,
#         kw.fund_take: x_fund_take,
#     }
#     all args included in values dict
#     etl_config = get_etl_config()
#     dimen = kw.planunit
#     dst_columns = get_prime_columns(dimen, ["h", "agg", "put"], etl_config)
#     print(f"{dst_columns=}")
#     assert dst_columns == set(values_dict.keys())

#     # WHEN
#     insert_sqlstr = create_plnawar_h_put_agg_insert_sqlstr(values_dict)

#     # THEN
#     assert insert_sqlstr
#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_sound_and_heard_tables(cursor)
#         table_name = "plan_keg_awardunit_h_put_agg"
#         expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
#         print("")
#         print(expected_sqlstr)
#         # print(insert_sqlstr)
#         assert insert_sqlstr == expected_sqlstr


def test_create_plnfact_h_put_agg_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_moment_label = exx.a23
    x_plan_name = "Sue"
    x_rope = 1
    x_fact_context = 2
    x_fact_state = 3
    x_fact_lower_otx = 4
    x_fact_upper_otx = 5
    values_dict = {
        kw.spark_num: 77,
        kw.face_name: exx.yao,
        kw.moment_label: x_moment_label,
        kw.plan_name: x_plan_name,
        kw.keg_rope: x_rope,
        kw.fact_context: x_fact_context,
        kw.fact_state: x_fact_state,
        f"{kw.fact_lower}_otx": x_fact_lower_otx,
        f"{kw.fact_upper}_otx": x_fact_upper_otx,
    }
    # all args included in values dict
    etl_config = get_etl_config()
    dimen = kw.plan_keg_factunit
    dst_columns = get_prime_columns(dimen, ["h", "agg", "put"], etl_config)
    dst_columns = remove_inx_columns(dst_columns)
    dst_columns = remove_staging_columns(dst_columns)
    print(f"{dst_columns=}")
    assert dst_columns == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_plnfact_h_put_agg_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_heard_tables(cursor)
        table_name = "plan_keg_factunit_h_put_agg"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        print("")
        print(expected_sqlstr)
        # print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


# def test_create_plnheal_h_put_agg_insert_sqlstr_ReturnsObj():
#     # ESTABLISH
#     x_moment_label = exx.a23
#     x_plan_name = "Sue"
#     x_rope = 1
#     x_healer_name = 2
#     values_dict = {
#         kw.spark_num: 77,
#         kw.face_name: exx.yao,
#         kw.moment_label: x_moment_label,
#         kw.plan_name: x_plan_name,
#         kw.keg_rope: x_rope,
#         kw.healer_name: x_healer_name,
#     }
#     all args included in values dict
#     etl_config = get_etl_config()
#     dimen = kw.planunit
#     dst_columns = get_prime_columns(dimen, ["h", "agg", "put"], etl_config)
#     print(f"{dst_columns=}")
#     assert dst_columns == set(values_dict.keys())

#     # WHEN
#     insert_sqlstr = create_plnheal_h_put_agg_insert_sqlstr(values_dict)

#     # THEN
#     assert insert_sqlstr
#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_sound_and_heard_tables(cursor)
#         table_name = "plan_keg_healerunit_h_put_agg"
#         expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
#         print("")
#         print(expected_sqlstr)
#         # print(insert_sqlstr)
#         assert insert_sqlstr == expected_sqlstr


# def test_create_plnlabo_h_put_agg_insert_sqlstr_ReturnsObj():
#     # ESTABLISH
#     x_moment_label = exx.a23
#     x_plan_name = "Sue"
#     x_rope = 1
#     x_party_title = 2
#     x_solo = 4
#     x__plan_name_is_labor = 3
#     values_dict = {
#         kw.spark_num: 77,
#         kw.face_name: exx.yao,
#         kw.moment_label: x_moment_label,
#         kw.plan_name: x_plan_name,
#         kw.keg_rope: x_rope,
#         kw.party_title: x_party_title,
#         kw.solo: x_solo,
#         kw.plan_name_is_labor: x__plan_name_is_labor,
#     }
#     all args included in values dict
#     etl_config = get_etl_config()
#     dimen = kw.planunit
#     dst_columns = get_prime_columns(dimen, ["h", "agg", "put"], etl_config)
#     print(f"{dst_columns=}")
#     assert dst_columns == set(values_dict.keys())

#     # WHEN
#     insert_sqlstr = create_plnlabo_h_put_agg_insert_sqlstr(values_dict)

#     # THEN
#     assert insert_sqlstr
#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_sound_and_heard_tables(cursor)
#         table_name = "plan_keg_partyunit_h_put_agg"
#         expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
#         print("")
#         print(expected_sqlstr)
#         print("")
#         print(insert_sqlstr)
#         assert insert_sqlstr == expected_sqlstr


# def test_create_plnprsn_h_put_agg_insert_sqlstr_ReturnsObj():
#     # ESTABLISH
#     x_moment_label = exx.a23
#     x_plan_name = "Sue"
#     x_person_name = 1
#     x_person_cred_lumen = 2
#     x_person_debt_lumen = 3
#     x_credor_pool = 4
#     x_debtor_pool = 5
#     x_fund_give = 6
#     x_fund_take = 7
#     x_fund_agenda_give = 8
#     x_fund_agenda_take = 9
#     x_fund_agenda_ratio_give = 10
#     x_fund_agenda_ratio_take = 11
#     x_inallocable_person_debt_lumen = 12
#     x_irrational_person_debt_lumen = 13
#     x_groupmark = 13
#     values_dict = {
#         kw.spark_num: 77,
#         kw.face_name: exx.yao,
#         kw.moment_label: x_moment_label,
#         kw.plan_name: x_plan_name,
#         kw.person_name: x_person_name,
#         kw.person_cred_lumen: x_person_cred_lumen,
#         kw.person_debt_lumen: x_person_debt_lumen,
#         kw.credor_pool: x_credor_pool,
#         kw.debtor_pool: x_debtor_pool,
#         kw.fund_give: x_fund_give,
#         kw.fund_take: x_fund_take,
#         kw.fund_agenda_give: x_fund_agenda_give,
#         kw.fund_agenda_take: x_fund_agenda_take,
#         kw.fund_agenda_ratio_give: x_fund_agenda_ratio_give,
#         kw.fund_agenda_ratio_take: x_fund_agenda_ratio_take,
#         kw.inallocable_person_debt_lumen: x_inallocable_person_debt_lumen,
#         kw.irrational_person_debt_lumen: x_irrational_person_debt_lumen,
#         kw.groupmark: x_groupmark,
#     }
#     all args included in values dict
#     etl_config = get_etl_config()
#     dimen = kw.planunit
#     dst_columns = get_prime_columns(dimen, ["h", "agg", "put"], etl_config)
#     print(f"{dst_columns=}")
#     assert dst_columns == set(values_dict.keys())

#     # WHEN
#     insert_sqlstr = create_plnprsn_h_put_agg_insert_sqlstr(values_dict)

#     # THEN
#     assert insert_sqlstr
#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_sound_and_heard_tables(cursor)
#         table_name = "plan_personunit_h_put_agg"
#         expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
#         print("")
#         print(expected_sqlstr)
#         # print(insert_sqlstr)
#         assert insert_sqlstr == expected_sqlstr


# def test_create_plnmemb_h_put_agg_insert_sqlstr_ReturnsObj():
#     # ESTABLISH
#     x_moment_label = exx.a23
#     x_plan_name = "Sue"
#     x_person_name = 1
#     x_group_title = 2
#     x_group_cred_lumen = 3
#     x_group_debt_lumen = 4
#     x_credor_pool = 5
#     x_debtor_pool = 6
#     x_fund_give = 7
#     x_fund_take = 8
#     x_fund_agenda_give = 9
#     x_fund_agenda_take = 10
#     x_fund_agenda_ratio_give = 11
#     x_fund_agenda_ratio_take = 12
#     values_dict = {
#         kw.spark_num: 77,
#         kw.face_name: exx.yao,
#         kw.moment_label: x_moment_label,
#         kw.plan_name: x_plan_name,
#         kw.person_name: x_person_name,
#         kw.group_title: x_group_title,
#         kw.group_cred_lumen: x_group_cred_lumen,
#         kw.group_debt_lumen: x_group_debt_lumen,
#         kw.credor_pool: x_credor_pool,
#         kw.debtor_pool: x_debtor_pool,
#         kw.fund_give: x_fund_give,
#         kw.fund_take: x_fund_take,
#         kw.fund_agenda_give: x_fund_agenda_give,
#         kw.fund_agenda_take: x_fund_agenda_take,
#         kw.fund_agenda_ratio_give: x_fund_agenda_ratio_give,
#         kw.fund_agenda_ratio_take: x_fund_agenda_ratio_take,
#     }
#     all args included in values dict
#     etl_config = get_etl_config()
#     dimen = kw.planunit
#     dst_columns = get_prime_columns(dimen, ["h", "agg", "put"], etl_config)
#     print(f"{dst_columns=}")
#     assert dst_columns == set(values_dict.keys())

#     # WHEN
#     insert_sqlstr = create_plnmemb_h_put_agg_insert_sqlstr(values_dict)

#     # THEN
#     assert insert_sqlstr
#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_sound_and_heard_tables(cursor)
#         table_name = "plan_person_membership_h_put_agg"
#         expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
#         print("")
#         print(expected_sqlstr)
#         # print(insert_sqlstr)
#         assert insert_sqlstr == expected_sqlstr


# def test_create_plngrou_h_put_agg_insert_sqlstr_ReturnsObj():
#     # ESTABLISH
#     x_moment_label = exx.a23
#     x_plan_name = "Sue"
#     x_group_title = 1
#     x_credor_pool = 2
#     x_debtor_pool = 3
#     x_fund_grain = 4
#     x_fund_give = 5
#     x_fund_take = 6
#     x_fund_agenda_give = 7
#     x_fund_agenda_take = 8
#     values_dict = {
#         kw.spark_num: 77,
#         kw.face_name: exx.yao,
#         kw.moment_label: x_moment_label,
#         kw.plan_name: x_plan_name,
#         kw.group_title: x_group_title,
#         kw.credor_pool: x_credor_pool,
#         kw.debtor_pool: x_debtor_pool,
#         kw.fund_grain: x_fund_grain,
#         kw.fund_give: x_fund_give,
#         kw.fund_take: x_fund_take,
#         kw.fund_agenda_give: x_fund_agenda_give,
#         kw.fund_agenda_take: x_fund_agenda_take,
#     }
#     all args included in values dict
#     etl_config = get_etl_config()
#     dimen = kw.planunit
#     dst_columns = get_prime_columns(dimen, ["h", "agg", "put"], etl_config)
#     print(f"{dst_columns=}")
#     assert dst_columns == set(values_dict.keys())

#     # WHEN
#     insert_sqlstr = create_plngrou_h_put_agg_insert_sqlstr(values_dict)

#     # THEN
#     assert insert_sqlstr
#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_sound_and_heard_tables(cursor)
#         table_name = "plan_groupunit_h_put_agg"
#         expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
#         print("")
#         print(expected_sqlstr)
#         # print(insert_sqlstr)
#         assert insert_sqlstr == expected_sqlstr
