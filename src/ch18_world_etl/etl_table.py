from src.ch01_py.db_toolbox import get_create_table_sqlstr
from src.ch08_belief_atom.atom_config import get_delete_key_name
from src.ch16_translate.translate_config import find_set_otx_inx_args
from src.ch17_idea.idea_config import (
    get_default_sorted_list,
    get_idea_config_dict,
    get_idea_sqlite_types,
)

ALL_DIMEN_ABBV7 = {
    "MMTPAYY",
    "MMTBUDD",
    "MMTHOUR",
    "MMTMONT",
    "MMTWEEK",
    "MMTOFFI",
    "MMTUNIT",
    "BLFMEMB",
    "BLFVOCE",
    "BLFAWAR",
    "BLFFACT",
    "BLFHEAL",
    "BLFCASE",
    "BLFREAS",
    "BLFLABO",
    "BLFPLAN",
    "BLFUNIT",
    "NBUEPCH",
    "TRLTITL",
    "TRLNAME",
    "TRLROPE",
    "TRLLABE",
}


def get_dimen_abbv7(dimen: str) -> str:
    return {
        "moment_paybook": "MMTPAYY",
        "moment_budunit": "MMTBUDD",
        "moment_epoch_hour": "MMTHOUR",
        "moment_epoch_month": "MMTMONT",
        "moment_epoch_weekday": "MMTWEEK",
        "moment_timeoffi": "MMTOFFI",
        "momentunit": "MMTUNIT",
        "belief_voice_membership": "BLFMEMB",
        "belief_voiceunit": "BLFVOCE",
        "belief_plan_awardunit": "BLFAWAR",
        "belief_plan_factunit": "BLFFACT",
        "belief_plan_healerunit": "BLFHEAL",
        "belief_plan_reason_caseunit": "BLFCASE",
        "belief_plan_reasonunit": "BLFREAS",
        "belief_plan_partyunit": "BLFLABO",
        "belief_planunit": "BLFPLAN",
        "beliefunit": "BLFUNIT",
        "nabu_epochtime": "NBUEPCH",
        "translate_title": "TRLTITL",
        "translate_name": "TRLNAME",
        "translate_rope": "TRLROPE",
        "translate_label": "TRLLABE",
        "translate_core": "TRLCORE",
    }.get(dimen)


class prime_tablenameException(Exception):
    pass


def create_prime_tablename(
    idea_dimen_or_abbv7: str, phase: str, stage: str, put_del: str = None
) -> str:
    """
    phase must be one: 's', 'h', 'job'
    stage must be one: 'raw', 'agg', 'vld'
    """

    abbv_references = {
        "MMTPAYY": "moment_paybook",
        "MMTBUDD": "moment_budunit",
        "MMTHOUR": "moment_epoch_hour",
        "MMTMONT": "moment_epoch_month",
        "MMTWEEK": "moment_epoch_weekday",
        "MMTOFFI": "moment_timeoffi",
        "MMTUNIT": "momentunit",
        "BLFMEMB": "belief_voice_membership",
        "BLFVOCE": "belief_voiceunit",
        "BLFAWAR": "belief_plan_awardunit",
        "BLFFACT": "belief_plan_factunit",
        "BLFGROU": "belief_groupunit",
        "BLFHEAL": "belief_plan_healerunit",
        "BLFCASE": "belief_plan_reason_caseunit",
        "BLFREAS": "belief_plan_reasonunit",
        "BLFLABO": "belief_plan_partyunit",
        "BLFPLAN": "belief_planunit",
        "BLFUNIT": "beliefunit",
        "NBUEPCH": "nabu_epochtime",
        "TRLTITL": "translate_title",
        "TRLNAME": "translate_name",
        "TRLROPE": "translate_rope",
        "TRLLABE": "translate_label",
        "TRLCORE": "translate_core",
    }
    tablename = idea_dimen_or_abbv7
    if abbv_references.get(idea_dimen_or_abbv7.upper()):
        tablename = abbv_references.get(idea_dimen_or_abbv7.upper())
    if phase in {"s", "h", "job"}:
        tablename = f"{tablename}_{phase}"
    if stage is None:
        return tablename
    if stage not in {"raw", "agg", "vld"}:
        raise prime_tablenameException(f"'{stage}' is not a valid stage")

    return f"{tablename}_{put_del}_{stage}" if put_del else f"{tablename}_{stage}"


BELIEF_PRIME_TABLENAMES = {
    "belief_plan_awardunit_sound_del_agg": "BLFAWAR_DEL_AGG",
    "belief_plan_awardunit_sound_del_raw": "BLFAWAR_DEL_RAW",
    "belief_plan_awardunit_sound_put_agg": "BLFAWAR_PUT_AGG",
    "belief_plan_awardunit_sound_put_raw": "BLFAWAR_PUT_RAW",
    "belief_plan_factunit_sound_del_agg": "BLFFACT_DEL_AGG",
    "belief_plan_factunit_sound_del_raw": "BLFFACT_DEL_RAW",
    "belief_plan_factunit_sound_put_agg": "BLFFACT_PUT_AGG",
    "belief_plan_factunit_sound_put_raw": "BLFFACT_PUT_RAW",
    "belief_plan_healerunit_sound_del_agg": "BLFHEAL_DEL_AGG",
    "belief_plan_healerunit_sound_del_raw": "BLFHEAL_DEL_RAW",
    "belief_plan_healerunit_sound_put_agg": "BLFHEAL_PUT_AGG",
    "belief_plan_healerunit_sound_put_raw": "BLFHEAL_PUT_RAW",
    "belief_plan_partyunit_sound_del_agg": "BLFLABO_DEL_AGG",
    "belief_plan_partyunit_sound_del_raw": "BLFLABO_DEL_RAW",
    "belief_plan_partyunit_sound_put_agg": "BLFLABO_PUT_AGG",
    "belief_plan_partyunit_sound_put_raw": "BLFLABO_PUT_RAW",
    "belief_plan_reason_caseunit_sound_del_agg": "BLFCASE_DEL_AGG",
    "belief_plan_reason_caseunit_sound_del_raw": "BLFCASE_DEL_RAW",
    "belief_plan_reason_caseunit_sound_put_agg": "BLFCASE_PUT_AGG",
    "belief_plan_reason_caseunit_sound_put_raw": "BLFCASE_PUT_RAW",
    "belief_plan_reasonunit_sound_del_agg": "BLFREAS_DEL_AGG",
    "belief_plan_reasonunit_sound_del_raw": "BLFREAS_DEL_RAW",
    "belief_plan_reasonunit_sound_put_agg": "BLFREAS_PUT_AGG",
    "belief_plan_reasonunit_sound_put_raw": "BLFREAS_PUT_RAW",
    "belief_planunit_sound_del_agg": "BLFPLAN_DEL_AGG",
    "belief_planunit_sound_del_raw": "BLFPLAN_DEL_RAW",
    "belief_planunit_sound_put_agg": "BLFPLAN_PUT_AGG",
    "belief_planunit_sound_put_raw": "BLFPLAN_PUT_RAW",
    "belief_voice_membership_sound_del_agg": "BLFMEMB_DEL_AGG",
    "belief_voice_membership_sound_del_raw": "BLFMEMB_DEL_RAW",
    "belief_voice_membership_sound_put_agg": "BLFMEMB_PUT_AGG",
    "belief_voice_membership_sound_put_raw": "BLFMEMB_PUT_RAW",
    "belief_voiceunit_sound_del_agg": "BLFVOCE_DEL_AGG",
    "belief_voiceunit_sound_del_raw": "BLFVOCE_DEL_RAW",
    "belief_voiceunit_sound_put_agg": "BLFVOCE_PUT_AGG",
    "belief_voiceunit_sound_put_raw": "BLFVOCE_PUT_RAW",
    "beliefunit_sound_del_agg": "BLFUNIT_DEL_AGG",
    "beliefunit_sound_del_raw": "BLFUNIT_DEL_RAW",
    "beliefunit_sound_put_agg": "BLFUNIT_PUT_AGG",
    "beliefunit_sound_put_raw": "BLFUNIT_PUT_RAW",
}


def get_all_dimen_columns_set(x_dimen: str) -> set[str]:
    if x_dimen == "translate_core":
        return {"spark_num", "face_name", "otx_knot", "inx_knot", "unknown_str"}
    x_config = get_idea_config_dict().get(x_dimen)
    columns = set(x_config.get("jkeys").keys())
    columns.update(set(x_config.get("jvalues").keys()))
    return columns


def get_del_dimen_columns_set(x_dimen: str) -> list[str]:
    x_config = get_idea_config_dict().get(x_dimen)
    columns_set = set(x_config.get("jkeys").keys())
    columns_list = get_default_sorted_list(columns_set)
    columns_list[-1] = get_delete_key_name(columns_list[-1])
    return set(columns_list)


def create_translate_sound_raw_table_sqlstr(x_dimen):
    tablename = create_prime_tablename(get_dimen_abbv7(x_dimen), "s", "raw")
    columns = get_all_dimen_columns_set(x_dimen)
    columns.add("idea_number")
    columns.add("error_message")
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_translate_sound_agg_table_sqlstr(x_dimen):
    tablename = create_prime_tablename(get_dimen_abbv7(x_dimen), "s", "agg")
    columns = get_all_dimen_columns_set(x_dimen)
    columns.add("error_message")
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_moment_sound_agg_table_sqlstr(x_dimen):
    tablename = create_prime_tablename(get_dimen_abbv7(x_dimen), "s", "agg")
    columns = get_all_dimen_columns_set(x_dimen)
    columns.add("error_message")
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_moment_sound_vld_table_sqlstr(x_dimen):
    tablename = create_prime_tablename(get_dimen_abbv7(x_dimen), "s", "vld")
    columns = get_all_dimen_columns_set(x_dimen)
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_translate_sound_vld_table_sqlstr(x_dimen):
    tablename = create_prime_tablename(get_dimen_abbv7(x_dimen), "s", "vld")
    columns = get_all_dimen_columns_set(x_dimen)
    columns.discard("otx_knot")
    columns.discard("inx_knot")
    columns.discard("unknown_str")
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_translate_core_raw_table_sqlstr(x_dimen):
    tablename = create_prime_tablename(get_dimen_abbv7(x_dimen), "s", "raw")
    columns = get_all_dimen_columns_set(x_dimen)
    columns.remove("spark_num")
    columns.add("source_dimen")
    columns.add("error_message")
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_translate_core_agg_table_sqlstr(x_dimen):
    tablename = create_prime_tablename(get_dimen_abbv7(x_dimen), "s", "agg")
    columns = get_all_dimen_columns_set(x_dimen)
    columns.remove("spark_num")
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_translate_core_vld_table_sqlstr(x_dimen):
    agg_tablename = create_prime_tablename(get_dimen_abbv7(x_dimen), "s", "agg")
    vld_tablename = create_prime_tablename(get_dimen_abbv7(x_dimen), "s", "vld")
    sqlstr = create_translate_core_agg_table_sqlstr(x_dimen)
    sqlstr = sqlstr.replace(agg_tablename, vld_tablename)
    return sqlstr


def create_moment_heard_raw_table_sqlstr(x_dimen):
    tablename = create_prime_tablename(get_dimen_abbv7(x_dimen), "h", "raw")
    columns = get_all_dimen_columns_set(x_dimen)
    columns = find_set_otx_inx_args(columns)
    columns.add("error_message")
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_moment_heard_vld_table_sqlstr(x_dimen: str):
    tablename = create_prime_tablename(get_dimen_abbv7(x_dimen), "h", "vld")
    columns = get_all_dimen_columns_set(x_dimen)
    columns.remove("spark_num")
    columns.remove("face_name")
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_belief_sound_put_raw_table_sqlstr(x_dimen: str) -> str:
    tablename = create_prime_tablename(get_dimen_abbv7(x_dimen), "s", "raw", "put")
    columns = get_all_dimen_columns_set(x_dimen)
    columns.add("idea_number")
    columns.add("error_message")
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_belief_sound_put_agg_table_sqlstr(x_dimen: str) -> str:
    tablename = create_prime_tablename(get_dimen_abbv7(x_dimen), "s", "agg", "put")
    columns = get_all_dimen_columns_set(x_dimen)
    columns.add("error_message")
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_belief_sound_put_vld_table_sqlstr(x_dimen: str) -> str:
    tablename = create_prime_tablename(get_dimen_abbv7(x_dimen), "s", "vld", "put")
    columns = get_all_dimen_columns_set(x_dimen)
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_belief_sound_del_raw_table_sqlstr(x_dimen: str) -> str:
    tablename = create_prime_tablename(get_dimen_abbv7(x_dimen), "s", "raw", "del")
    columns = get_del_dimen_columns_set(x_dimen)
    columns.add("idea_number")
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_belief_sound_del_agg_table_sqlstr(x_dimen: str) -> str:
    tablename = create_prime_tablename(get_dimen_abbv7(x_dimen), "s", "agg", "del")
    columns = get_del_dimen_columns_set(x_dimen)
    columns.add("error_message")
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_belief_sound_del_vld_table_sqlstr(x_dimen: str) -> str:
    tablename = create_prime_tablename(get_dimen_abbv7(x_dimen), "s", "vld", "del")
    columns = get_del_dimen_columns_set(x_dimen)
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_belief_heard_put_raw_table_sqlstr(x_dimen: str) -> str:
    tablename = create_prime_tablename(get_dimen_abbv7(x_dimen), "h", "raw", "put")
    columns = set()
    columns = get_all_dimen_columns_set(x_dimen)
    columns = find_set_otx_inx_args(columns)
    columns.add("translate_spark_num")
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_belief_heard_put_agg_table_sqlstr(x_dimen: str) -> str:
    tablename = create_prime_tablename(get_dimen_abbv7(x_dimen), "h", "vld", "put")
    columns = get_all_dimen_columns_set(x_dimen)
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_belief_heard_del_raw_table_sqlstr(x_dimen: str) -> str:
    tablename = create_prime_tablename(get_dimen_abbv7(x_dimen), "h", "raw", "del")
    columns = get_del_dimen_columns_set(x_dimen)
    columns = find_set_otx_inx_args(columns)
    columns.add("translate_spark_num")
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_belief_heard_del_agg_table_sqlstr(x_dimen: str) -> str:
    tablename = create_prime_tablename(get_dimen_abbv7(x_dimen), "h", "vld", "del")
    columns = get_del_dimen_columns_set(x_dimen)
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())
