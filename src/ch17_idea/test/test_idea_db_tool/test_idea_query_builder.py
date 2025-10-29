from sqlite3 import connect as sqlite3_connect
from src.ch17_idea.idea_config import get_idea_config_dict
from src.ch17_idea.idea_db_tool import (
    create_idea_sorted_table,
    get_default_sorted_list,
    get_idea_into_dimen_raw_query,
)
from src.ref.keywords import Ch17Keywords as kw


def test_get_idea_into_dimen_raw_query_ReturnsObj_Scenario0_belief_plan_partyunit():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        idea_number = "br000XX"
        idea_cols = [
            kw.spark_num,
            kw.face_name,
            kw.moment_label,
            kw.plan_rope,
            kw.party_title,
            kw.belief_name,
            kw.voice_name,
            kw.amount,
        ]
        blrlabo_cat = "belief_plan_partyunit"
        src_table = f"{idea_number}_raw"
        dst_table = f"{blrlabo_cat}_raw"
        idea_config = get_idea_config_dict()
        blrlabo_config = idea_config.get(blrlabo_cat)
        print(f"{blrlabo_cat=}")
        print(f"{blrlabo_config=}")
        blrlabo_jkeys = blrlabo_config.get(kw.jkeys)
        blrlabo_jvals = blrlabo_config.get(kw.jvalues)
        blrlabo_args = set(blrlabo_jkeys.keys()).union(set(blrlabo_jvals.keys()))
        blrlabo_args = get_default_sorted_list(blrlabo_args)
        print(f"{blrlabo_jkeys=}")
        print(f"{blrlabo_jvals=}")
        create_idea_sorted_table(conn, src_table, idea_cols)
        create_idea_sorted_table(conn, dst_table, blrlabo_args)

        # WHEN
        gen_sqlstr = get_idea_into_dimen_raw_query(
            conn, idea_number, blrlabo_cat, blrlabo_jkeys
        )

        # THEN
        columns_str = f"{kw.spark_num}, {kw.face_name}, {kw.moment_label}, {kw.belief_name}, {kw.plan_rope}, {kw.party_title}"
        expected_sqlstr = f"""INSERT INTO {blrlabo_cat}_raw ({kw.idea_number}, {columns_str})
SELECT '{idea_number}' as {kw.idea_number}, {columns_str}
FROM {idea_number}_raw
WHERE {kw.spark_num} IS NOT NULL AND {kw.face_name} IS NOT NULL AND {kw.moment_label} IS NOT NULL AND {kw.belief_name} IS NOT NULL AND {kw.plan_rope} IS NOT NULL AND {kw.party_title} IS NOT NULL
GROUP BY {columns_str}
;
"""
        print("")
        print(gen_sqlstr)
        print(expected_sqlstr)
        assert gen_sqlstr == expected_sqlstr


def test_get_idea_into_dimen_raw_query_ReturnsObj_Scenario1_belief_voiceunit():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        idea_number = "br000XX"
        idea_cols = [
            kw.spark_num,
            kw.face_name,
            kw.moment_label,
            kw.plan_rope,
            kw.party_title,
            kw.belief_name,
            kw.voice_name,
            kw.voice_cred_lumen,
            kw.voice_debt_lumen,
            kw.amount,
        ]
        src_table = f"{idea_number}_raw"
        blfvoce_table = f"{kw.belief_voiceunit}_raw"
        idea_config = get_idea_config_dict()
        blfvoce_config = idea_config.get(kw.belief_voiceunit)
        blfvoce_jkeys = blfvoce_config.get(kw.jkeys)
        blfvoce_jvals = blfvoce_config.get(kw.jvalues)
        blfvoce_args = set(blfvoce_jkeys.keys()).union(set(blfvoce_jvals.keys()))
        print(f"{blfvoce_jkeys=}")
        print(f"{blfvoce_jvals=}")
        create_idea_sorted_table(conn, src_table, idea_cols)
        create_idea_sorted_table(conn, blfvoce_table, list(blfvoce_args))

        # WHEN
        gen_sqlstr = get_idea_into_dimen_raw_query(
            conn, idea_number, kw.belief_voiceunit, blfvoce_jkeys
        )

        # THEN
        columns_str = "spark_num, face_name, moment_label, belief_name, voice_name, voice_cred_lumen, voice_debt_lumen"
        expected_sqlstr = f"""INSERT INTO {kw.belief_voiceunit}_raw (idea_number, {columns_str})
SELECT '{idea_number}' as idea_number, {columns_str}
FROM {idea_number}_raw
WHERE spark_num IS NOT NULL AND face_name IS NOT NULL AND moment_label IS NOT NULL AND belief_name IS NOT NULL AND voice_name IS NOT NULL
GROUP BY {columns_str}
;
"""
        print("")
        print(gen_sqlstr)
        print(expected_sqlstr)

        assert gen_sqlstr == expected_sqlstr


def test_get_idea_into_dimen_raw_query_ReturnsObj_Scenario2_belief_voiceunit():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        idea_number = "br000XX"
        idea_cols = [
            kw.spark_num,
            kw.face_name,
            kw.moment_label,
            kw.plan_rope,
            kw.party_title,
            kw.belief_name,
            kw.voice_name,
            kw.voice_cred_lumen,
            kw.amount,
        ]
        src_table = f"{idea_number}_raw"
        blfvoce_table = f"{kw.belief_voiceunit}_raw"
        idea_config = get_idea_config_dict()
        blfvoce_config = idea_config.get(kw.belief_voiceunit)
        blfvoce_jkeys = blfvoce_config.get(kw.jkeys)
        blfvoce_jvals = blfvoce_config.get(kw.jvalues)
        blfvoce_args = set(blfvoce_jkeys.keys()).union(set(blfvoce_jvals.keys()))
        print(f"{blfvoce_jkeys=}")
        print(f"{blfvoce_jvals=}")
        create_idea_sorted_table(conn, src_table, idea_cols)
        create_idea_sorted_table(conn, blfvoce_table, list(blfvoce_args))

        # WHEN
        gen_sqlstr = get_idea_into_dimen_raw_query(
            conn, idea_number, kw.belief_voiceunit, blfvoce_jkeys
        )

        # THEN
        columns_str = "spark_num, face_name, moment_label, belief_name, voice_name, voice_cred_lumen"
        expected_sqlstr = f"""INSERT INTO {kw.belief_voiceunit}_raw (idea_number, {columns_str})
SELECT '{idea_number}' as idea_number, {columns_str}
FROM {idea_number}_raw
WHERE spark_num IS NOT NULL AND face_name IS NOT NULL AND moment_label IS NOT NULL AND belief_name IS NOT NULL AND voice_name IS NOT NULL
GROUP BY {columns_str}
;
"""
        print("generated:")
        print(gen_sqlstr)
        print(expected_sqlstr)

        assert gen_sqlstr == expected_sqlstr
