from sqlite3 import connect as sqlite3_connect
from src.ch00_py.db_toolbox import get_row_count, get_table_columns
from src.ch14_moment.moment_config import get_moment_dimens
from src.ch15_nabu.nabu_config import get_nabu_dimens
from src.ch17_idea.idea_config import get_default_sorted_list, get_idea_config_dict
from src.ch18_world_etl.etl_config import get_dimen_abbv7
from src.ch18_world_etl.etl_main import etl_heard_raw_tables_to_heard_vld_tables
from src.ch18_world_etl.etl_sqlstr import (
    create_prime_tablename as prime_tbl,
    create_sound_and_heard_tables,
    get_insert_heard_vld_sqlstrs,
)
from src.ref.keywords import Ch18Keywords as kw, ExampleStrs as exx


def test_get_insert_heard_vld_sqlstrs_ReturnsObj_CheckMomentDimen():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    insert_heard_vld_sqlstrs = get_insert_heard_vld_sqlstrs()

    # THEN
    gen_heard_vld_tablenames = set(insert_heard_vld_sqlstrs.keys())
    moment_dimes = get_moment_dimens()
    moment_vld_tablenames = {prime_tbl(dimen, "h", "vld") for dimen in moment_dimes}
    # print(f"{gen_heard_vld_tablenames=}")
    # print(f"     {get_moment_dimens()=}")
    assert moment_vld_tablenames.issubset(gen_heard_vld_tablenames)
    idea_config = get_idea_config_dict({kw.moment})
    with sqlite3_connect(":memory:") as moment_db_conn:
        cursor = moment_db_conn.cursor()
        create_sound_and_heard_tables(cursor)

        for x_dimen in idea_config:
            # print(f"{x_dimen} checking...")
            raw_tablename = prime_tbl(x_dimen, "h", "raw")
            vld_tablename = prime_tbl(x_dimen, "h", "vld")
            raw_columns = get_table_columns(cursor, raw_tablename)
            vld_columns = get_table_columns(cursor, vld_tablename)
            raw_columns = {raw_col for raw_col in raw_columns if raw_col[-3:] != "otx"}
            raw_columns.remove(f"{kw.face_name}_inx")
            raw_columns.remove(kw.spark_num)
            raw_columns.remove(kw.error_message)
            raw_columns = get_default_sorted_list(raw_columns)

            raw_columns_str = ", ".join(raw_columns)
            vld_columns_str = ", ".join(vld_columns)
            # print(f"{raw_columns_str=}")
            # print(f"{vld_columns_str=}")
            expected_table2table_vld_insert_sqlstr = f"""
INSERT INTO {vld_tablename} ({vld_columns_str})
SELECT {raw_columns_str}
FROM {raw_tablename}
GROUP BY {raw_columns_str}
"""
            dimen_abbv7 = get_dimen_abbv7(x_dimen)
            # print(f'"{x_dimen}": {dimen_abbv7.upper()}_HEARD_VLD_INSERT_SQLSTR,')
            print(
                f'{dimen_abbv7.upper()}_HEARD_VLD_INSERT_SQLSTR = """{expected_table2table_vld_insert_sqlstr}"""'
            )
            gen_sqlstr = insert_heard_vld_sqlstrs.get(vld_tablename)
            assert gen_sqlstr == expected_table2table_vld_insert_sqlstr


def test_get_insert_heard_vld_sqlstrs_ReturnsObj_PlanDimensRequired():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    plan_dimens_config = get_idea_config_dict({kw.plan})

    # WHEN
    insert_heard_vld_sqlstrs = get_insert_heard_vld_sqlstrs()

    # THEN
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_heard_tables(cursor)

        for plan_dimen in plan_dimens_config:
            # print(f"{plan_dimen=}")
            h_raw_put_tablename = prime_tbl(plan_dimen, "h", "raw", "put")
            h_raw_del_tablename = prime_tbl(plan_dimen, "h", "raw", "del")
            h_vld_put_tablename = prime_tbl(plan_dimen, "h", "vld", "put")
            h_vld_del_tablename = prime_tbl(plan_dimen, "h", "vld", "del")
            h_raw_put_cols = get_table_columns(cursor, h_raw_put_tablename)
            h_raw_del_cols = get_table_columns(cursor, h_raw_del_tablename)
            h_vld_put_cols = get_table_columns(cursor, h_vld_put_tablename)
            h_vld_del_cols = get_table_columns(cursor, h_vld_del_tablename)
            h_raw_put_cols = {col for col in h_raw_put_cols if col[-3:] != "otx"}
            h_raw_del_cols = {col for col in h_raw_del_cols if col[-3:] != "otx"}
            h_raw_put_cols = get_default_sorted_list(h_raw_put_cols)
            h_raw_del_cols = get_default_sorted_list(h_raw_del_cols)
            h_raw_put_columns_str = ", ".join(h_raw_put_cols)
            h_raw_put_cols.remove(kw.translate_spark_num)
            h_raw_del_cols.remove(kw.translate_spark_num)
            h_raw_put_columns_str = ", ".join(h_raw_put_cols)
            h_raw_del_columns_str = ", ".join(h_raw_del_cols)
            h_vld_put_columns_str = ", ".join(h_vld_put_cols)
            h_vld_del_columns_str = ", ".join(h_vld_del_cols)
            expected_vld_put_insert_sqlstr = f"""
INSERT INTO {h_vld_put_tablename} ({h_vld_put_columns_str})
SELECT {h_raw_put_columns_str}
FROM {h_raw_put_tablename}
GROUP BY {h_raw_put_columns_str}
"""
            expected_vld_del_insert_sqlstr = f"""
INSERT INTO {h_vld_del_tablename} ({h_vld_del_columns_str})
SELECT {h_raw_del_columns_str}
FROM {h_raw_del_tablename}
GROUP BY {h_raw_del_columns_str}
"""
            abbv7 = get_dimen_abbv7(plan_dimen)
            put_sqlstr_ref = f"INSERT_{abbv7.upper()}_HEARD_VLD_PUT_SQLSTR"
            del_sqlstr_ref = f"INSERT_{abbv7.upper()}_HEARD_VLD_DEL_SQLSTR"
            print(f'{put_sqlstr_ref}= """{expected_vld_put_insert_sqlstr}"""')
            print(f'{del_sqlstr_ref}= """{expected_vld_del_insert_sqlstr}"""')
            # print(f"'{h_vld_put_tablename}': {put_sqlstr_ref},")
            # print(f"'{h_vld_del_tablename}': {del_sqlstr_ref},")
            insert_h_vld_put_sqlstr = insert_heard_vld_sqlstrs.get(h_vld_put_tablename)
            insert_h_vld_del_sqlstr = insert_heard_vld_sqlstrs.get(h_vld_del_tablename)
            assert insert_h_vld_put_sqlstr == expected_vld_put_insert_sqlstr
            assert insert_h_vld_del_sqlstr == expected_vld_del_insert_sqlstr


def test_get_insert_heard_vld_sqlstrs_ReturnsObj_PopulatesTable_Scenario0():
    # ESTABLISH
    yao_inx = "Yaoito"
    spark1 = 1
    spark2 = 2
    spark5 = 5
    spark7 = 7
    x44_credit = 44
    x55_credit = 55
    x22_debt = 22
    x66_debt = 66

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        plnprsn_h_raw_put_tablename = prime_tbl(kw.plan_personunit, "h", "raw", "put")
        print(f"{get_table_columns(cursor, plnprsn_h_raw_put_tablename)=}")
        insert_into_clause = f"""INSERT INTO {plnprsn_h_raw_put_tablename} (
  {kw.spark_num}
, {kw.face_name}_inx
, {kw.moment_rope}_inx
, {kw.plan_name}_inx
, {kw.person_name}_inx
, {kw.person_cred_lumen}
, {kw.person_debt_lumen}
)
VALUES
  ({spark1}, '{exx.sue}', '{exx.a23}','{exx.yao}', '{yao_inx}', {x44_credit}, {x22_debt})
, ({spark2}, '{exx.yao}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x22_debt})
, ({spark5}, '{exx.sue}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x22_debt})
, ({spark7}, '{exx.bob}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x66_debt})
, ({spark7}, '{exx.bob}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x66_debt})
;
"""
        cursor.execute(insert_into_clause)
        assert get_row_count(cursor, plnprsn_h_raw_put_tablename) == 5
        plnprsn_h_vld_put_tablename = prime_tbl(kw.plan_personunit, "h", "vld", "put")
        assert get_row_count(cursor, plnprsn_h_vld_put_tablename) == 0

        # WHEN
        sqlstr = get_insert_heard_vld_sqlstrs().get(plnprsn_h_vld_put_tablename)
        print(sqlstr)
        cursor.execute(sqlstr)

        # THEN
        assert get_row_count(cursor, plnprsn_h_vld_put_tablename) == 4
        select_sqlstr = f"""SELECT {kw.spark_num}
, {kw.face_name}
, {kw.moment_rope}
, {kw.plan_name}
, {kw.person_name}
, {kw.person_cred_lumen}
, {kw.person_debt_lumen}
FROM {plnprsn_h_vld_put_tablename}
"""
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (spark1, exx.sue, exx.a23, exx.yao, yao_inx, 44.0, 22.0),
            (spark2, exx.yao, exx.a23, exx.bob, exx.bob, 55.0, 22.0),
            (spark5, exx.sue, exx.a23, exx.bob, exx.bob, 55.0, 22.0),
            (spark7, exx.bob, exx.a23, exx.bob, exx.bob, 55.0, 66.0),
        ]


def test_etl_heard_raw_tables_to_heard_vld_tables_PopulatesTable_Scenario0():
    # ESTABLISH
    yao_inx = "Yaoito"
    spark1 = 1
    spark2 = 2
    spark5 = 5
    spark7 = 7
    x44_credit = 44
    x55_credit = 55
    x22_debt = 22
    x66_debt = 66

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        plnprsn_h_raw_put_tablename = prime_tbl(kw.plan_personunit, "h", "raw", "put")
        print(f"{get_table_columns(cursor, plnprsn_h_raw_put_tablename)=}")
        insert_into_clause = f"""INSERT INTO {plnprsn_h_raw_put_tablename} (
  {kw.spark_num}
, {kw.face_name}_inx
, {kw.moment_rope}_inx
, {kw.plan_name}_inx
, {kw.person_name}_inx
, {kw.person_cred_lumen}
, {kw.person_debt_lumen}
)
VALUES
  ({spark1}, '{exx.sue}', '{exx.a23}','{exx.yao}', '{yao_inx}', {x44_credit}, {x22_debt})
, ({spark2}, '{exx.yao}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x22_debt})
, ({spark5}, '{exx.sue}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x22_debt})
, ({spark7}, '{exx.bob}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x66_debt})
, ({spark7}, '{exx.bob}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x66_debt})
;
"""
        cursor.execute(insert_into_clause)
        assert get_row_count(cursor, plnprsn_h_raw_put_tablename) == 5
        plnprsn_h_vld_put_tablename = prime_tbl(kw.plan_personunit, "h", "vld", "put")
        assert get_row_count(cursor, plnprsn_h_vld_put_tablename) == 0

        # WHEN
        etl_heard_raw_tables_to_heard_vld_tables(cursor)

        # THEN
        assert get_row_count(cursor, plnprsn_h_vld_put_tablename) == 4
        select_sqlstr = f"""SELECT {kw.spark_num}
, {kw.face_name}
, {kw.moment_rope}
, {kw.plan_name}
, {kw.person_name}
, {kw.person_cred_lumen}
, {kw.person_debt_lumen}
FROM {plnprsn_h_vld_put_tablename}
"""
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (spark1, exx.sue, exx.a23, exx.yao, yao_inx, 44.0, 22.0),
            (spark2, exx.yao, exx.a23, exx.bob, exx.bob, 55.0, 22.0),
            (spark5, exx.sue, exx.a23, exx.bob, exx.bob, 55.0, 22.0),
            (spark7, exx.bob, exx.a23, exx.bob, exx.bob, 55.0, 66.0),
        ]
