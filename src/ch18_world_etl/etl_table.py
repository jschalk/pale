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
    idea_dimen_or_abbv7: str, stage0: str, stage1: str, put_del: str = None
) -> str:
    """
    stage0 must be one: 's', 'h', 'job'
    stage1 must be one: 'raw', 'agg', 'vld'
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
    if stage0 in {"s", "h", "job"}:
        tablename = f"{tablename}_{stage0}"
    if stage1 is None:
        return tablename
    if stage1 not in {"raw", "agg", "vld"}:
        raise prime_tablenameException(f"'{stage1}' is not a valid stage")

    return f"{tablename}_{put_del}_{stage1}" if put_del else f"{tablename}_{stage1}"


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
        return {"face_name", "otx_knot", "inx_knot", "unknown_str"}
    x_config = get_idea_config_dict().get(x_dimen)
    columns = set(x_config.get("jkeys").keys())
    columns.update(set(x_config.get("jvalues").keys()))
    return columns


def get_del_dimen_columns_set(x_dimen: str) -> set[str]:
    x_config = get_idea_config_dict().get(x_dimen)
    columns_set = set(x_config.get("jkeys").keys())
    columns_list = get_default_sorted_list(columns_set)
    columns_list[-1] = get_delete_key_name(columns_list[-1])
    return set(columns_list)


def get_trlcore_columns(x_dimen: str, stage0: str, stage1: str) -> set[str]:
    columns = get_all_dimen_columns_set(x_dimen)
    if (stage0, stage1) == ("s", "raw"):
        columns.add("source_dimen")
        columns.add("error_message")
    # elif (stage0, stage1) in [("s", "agg"), ("s", "vld")]:
    #     pass
    return columns


def get_translate_columns(x_dimen: str, stage0: str, stage1: str) -> set[str]:
    columns = get_all_dimen_columns_set(x_dimen)
    if (stage0, stage1) == ("s", "raw"):
        columns.add("idea_number")
        columns.add("error_message")
    elif (stage0, stage1) == ("s", "agg"):
        columns.add("error_message")
    elif (stage0, stage1) == ("s", "vld"):
        columns.remove("otx_knot")
        columns.remove("inx_knot")
        columns.remove("unknown_str")
    return columns


def get_moment_columns(x_dimen: str, stage0: str, stage1: str) -> set[str]:
    columns = get_all_dimen_columns_set(x_dimen)
    if (stage0, stage1) == ("s", "raw"):
        columns.add("idea_number")
        columns.add("error_message")
    elif (stage0, stage1) == ("s", "agg"):
        columns.add("error_message")
    elif (stage0, stage1) == ("h", "raw"):
        columns = find_set_otx_inx_args(columns)
        columns.add("error_message")
    elif (stage0, stage1) == ("h", "vld"):
        columns.remove("spark_num")
        columns.remove("face_name")
    # if (stage0, stage1) == ("s", "vld"):
    #   pass
    return columns


def get_belief_columns(
    x_dimen: str, stage0: str, stage1: str, put_del: str
) -> set[str]:
    columns = set()
    if put_del == "put":
        columns = get_all_dimen_columns_set(x_dimen)
    elif put_del == "del":
        columns = get_del_dimen_columns_set(x_dimen)

    if (stage0, stage1, put_del) == ("s", "raw", "put"):
        columns.add("idea_number")
        columns.add("error_message")
    elif (stage0, stage1, put_del) == ("s", "raw", "del"):
        columns.add("idea_number")
    elif (stage0, stage1) == ("s", "agg"):
        columns.add("error_message")
    elif (stage0, stage1) == ("h", "raw"):
        columns = find_set_otx_inx_args(columns)
        columns.add("translate_spark_num")
    # elif (stage0, stage1, put_del) == ("s", "vld", "put"):
    #     pass
    # elif (stage0, stage1, put_del) == ("s", "vld", "del"):
    #     pass
    # elif (stage0, stage1, put_del) == ("h", "vld", "put"):
    #     pass
    # elif (stage0, stage1, put_del) == ("h", "vld", "del"):
    #     pass
    return columns


def create_tlr_core_prime_table_sqlstr(x_dimen: str, stage0: str, stage1: str) -> str:
    tablename = create_prime_tablename(x_dimen, stage0, stage1)
    columns = get_trlcore_columns(x_dimen, stage0, stage1)
    return get_sorted_typed_create_table_sqlstr(tablename, columns)


def create_tlr_prime_table_sqlstr(x_dimen: str, stage0: str, stage1: str) -> str:
    tablename = create_prime_tablename(x_dimen, stage0, stage1)
    columns = get_translate_columns(x_dimen, stage0, stage1)
    return get_sorted_typed_create_table_sqlstr(tablename, columns)


def create_mmt_prime_table_sqlstr(x_dimen: str, stage0: str, stage1: str) -> str:
    tablename = create_prime_tablename(x_dimen, stage0, stage1)
    columns = get_moment_columns(x_dimen, stage0, stage1)
    return get_sorted_typed_create_table_sqlstr(tablename, columns)


def create_prime_table_sqlstr(
    x_dimen: str, stage0: str, stage1: str, put_del: str
) -> str:
    tablename = create_prime_tablename(x_dimen, stage0, stage1, put_del)
    columns = get_belief_columns(x_dimen, stage0, stage1, put_del)
    return get_sorted_typed_create_table_sqlstr(tablename, columns)


def get_sorted_typed_create_table_sqlstr(tablename: str, columns: list[str]) -> str:
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())
