from sqlite3 import connect as sqlite3_connect
from src.ch17_idea.idea_config import get_idea_config_dict
from src.ch17_idea.idea_db_tool import (
    create_idea_sorted_table,
    get_default_sorted_list,
    get_idea_into_dimen_raw_query,
)
from src.ref.keywords import Ch17Keywords as kw


def test_get_idea_into_dimen_raw_query_ReturnsObj_Scenario0_plan_keg_partyunit():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        idea_number = "br000XX"
        idea_cols = [
            kw.spark_num,
            kw.face_name,
            kw.moment_label,
            kw.keg_rope,
            kw.party_title,
            kw.plan_name,
            kw.person_name,
            kw.amount,
        ]
        plnlabo_cat = "plan_keg_partyunit"
        src_table = f"{idea_number}_raw"
        dst_table = f"{plnlabo_cat}_raw"
        idea_config = get_idea_config_dict()
        plnlabo_config = idea_config.get(plnlabo_cat)
        print(f"{plnlabo_cat=}")
        print(f"{plnlabo_config=}")
        plnlabo_jkeys = plnlabo_config.get(kw.jkeys)
        plnlabo_jvals = plnlabo_config.get(kw.jvalues)
        plnlabo_args = set(plnlabo_jkeys.keys()).union(set(plnlabo_jvals.keys()))
        plnlabo_args = get_default_sorted_list(plnlabo_args)
        print(f"{plnlabo_jkeys=}")
        print(f"{plnlabo_jvals=}")
        create_idea_sorted_table(conn, src_table, idea_cols)
        create_idea_sorted_table(conn, dst_table, plnlabo_args)

        # WHEN
        gen_sqlstr = get_idea_into_dimen_raw_query(
            conn, idea_number, plnlabo_cat, plnlabo_jkeys
        )

        # THEN
        columns_str = f"{kw.spark_num}, {kw.face_name}, {kw.moment_label}, {kw.plan_name}, {kw.keg_rope}, {kw.party_title}"
        expected_sqlstr = f"""INSERT INTO {plnlabo_cat}_raw ({kw.idea_number}, {columns_str})
SELECT '{idea_number}' as {kw.idea_number}, {columns_str}
FROM {idea_number}_raw
WHERE {kw.spark_num} IS NOT NULL AND {kw.face_name} IS NOT NULL AND {kw.moment_label} IS NOT NULL AND {kw.plan_name} IS NOT NULL AND {kw.keg_rope} IS NOT NULL AND {kw.party_title} IS NOT NULL
GROUP BY {columns_str}
;
"""
        print("")
        print(gen_sqlstr)
        print(expected_sqlstr)
        assert gen_sqlstr == expected_sqlstr


def test_get_idea_into_dimen_raw_query_ReturnsObj_Scenario1_plan_personunit():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        idea_number = "br000XX"
        idea_cols = [
            kw.spark_num,
            kw.face_name,
            kw.moment_label,
            kw.keg_rope,
            kw.party_title,
            kw.plan_name,
            kw.person_name,
            kw.person_cred_lumen,
            kw.person_debt_lumen,
            kw.amount,
        ]
        src_table = f"{idea_number}_raw"
        plnprsn_table = f"{kw.plan_personunit}_raw"
        idea_config = get_idea_config_dict()
        plnprsn_config = idea_config.get(kw.plan_personunit)
        plnprsn_jkeys = plnprsn_config.get(kw.jkeys)
        plnprsn_jvals = plnprsn_config.get(kw.jvalues)
        plnprsn_args = set(plnprsn_jkeys.keys()).union(set(plnprsn_jvals.keys()))
        print(f"{plnprsn_jkeys=}")
        print(f"{plnprsn_jvals=}")
        create_idea_sorted_table(conn, src_table, idea_cols)
        create_idea_sorted_table(conn, plnprsn_table, list(plnprsn_args))

        # WHEN
        gen_sqlstr = get_idea_into_dimen_raw_query(
            conn, idea_number, kw.plan_personunit, plnprsn_jkeys
        )

        # THEN
        columns_str = "spark_num, face_name, moment_label, plan_name, person_name, person_cred_lumen, person_debt_lumen"
        expected_sqlstr = f"""INSERT INTO {kw.plan_personunit}_raw (idea_number, {columns_str})
SELECT '{idea_number}' as idea_number, {columns_str}
FROM {idea_number}_raw
WHERE spark_num IS NOT NULL AND face_name IS NOT NULL AND moment_label IS NOT NULL AND plan_name IS NOT NULL AND person_name IS NOT NULL
GROUP BY {columns_str}
;
"""
        print("")
        print(gen_sqlstr)
        print(expected_sqlstr)

        assert gen_sqlstr == expected_sqlstr


def test_get_idea_into_dimen_raw_query_ReturnsObj_Scenario2_plan_personunit():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        idea_number = "br000XX"
        idea_cols = [
            kw.spark_num,
            kw.face_name,
            kw.moment_label,
            kw.keg_rope,
            kw.party_title,
            kw.plan_name,
            kw.person_name,
            kw.person_cred_lumen,
            kw.amount,
        ]
        src_table = f"{idea_number}_raw"
        plnprsn_table = f"{kw.plan_personunit}_raw"
        idea_config = get_idea_config_dict()
        plnprsn_config = idea_config.get(kw.plan_personunit)
        plnprsn_jkeys = plnprsn_config.get(kw.jkeys)
        plnprsn_jvals = plnprsn_config.get(kw.jvalues)
        plnprsn_args = set(plnprsn_jkeys.keys()).union(set(plnprsn_jvals.keys()))
        print(f"{plnprsn_jkeys=}")
        print(f"{plnprsn_jvals=}")
        create_idea_sorted_table(conn, src_table, idea_cols)
        create_idea_sorted_table(conn, plnprsn_table, list(plnprsn_args))

        # WHEN
        gen_sqlstr = get_idea_into_dimen_raw_query(
            conn, idea_number, kw.plan_personunit, plnprsn_jkeys
        )

        # THEN
        columns_str = "spark_num, face_name, moment_label, plan_name, person_name, person_cred_lumen"
        expected_sqlstr = f"""INSERT INTO {kw.plan_personunit}_raw (idea_number, {columns_str})
SELECT '{idea_number}' as idea_number, {columns_str}
FROM {idea_number}_raw
WHERE spark_num IS NOT NULL AND face_name IS NOT NULL AND moment_label IS NOT NULL AND plan_name IS NOT NULL AND person_name IS NOT NULL
GROUP BY {columns_str}
;
"""
        print("generated:")
        print(gen_sqlstr)
        print(expected_sqlstr)

        assert gen_sqlstr == expected_sqlstr
