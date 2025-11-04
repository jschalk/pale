from copy import copy as copy_copy
from os import getcwd as os_getcwd
from src.ch01_py.db_toolbox import get_create_table_sqlstr
from src.ch01_py.dict_toolbox import get_empty_set_if_None, get_from_nested_dict
from src.ch01_py.file_toolbox import create_path, open_json
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
    "NABEPOC",
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
        "nabu_epochtime": "NABEPOC",
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
        "NABEPOC": "nabu_epochtime",
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


def etl_dimen_config_path() -> str:
    "Returns path: ch18_world_etl/etl_dimen_config.json"
    src_dir = create_path(os_getcwd(), "src")
    chapter_dir = create_path(src_dir, "ch18_world_etl")
    return create_path(chapter_dir, "etl_dimen_config.json")


def etl_dimen_config_dict() -> dict:
    return open_json(etl_dimen_config_path())


def get_all_dimen_columns_set(x_dimen: str) -> set[str]:
    if x_dimen == "translate_core":
        translate_core_dict = etl_dimen_config_dict().get("translate_core")
        return set(translate_core_dict.get("override_columns"))
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


def get_prime_columns(x_dimen: str, table_keylist: list[str]) -> set[str]:
    """Given dimen and config_keylist (ala ["s", "agg", put_del] )
    Return list of columns for that prime table"""
    columns = get_all_dimen_columns_set(x_dimen)
    if table_keylist[-1] == "del":
        columns = get_del_dimen_columns_set(x_dimen)

    if x_dimen == "translate_core":
        idea_category = "translate_core"
    elif x_dimen.find("translate") == 0:
        idea_category = "translate"
    elif x_dimen.find("nabu") == 0:
        idea_category = "nabu"
    elif x_dimen.find("moment") == 0:
        idea_category = "moment"
    elif x_dimen.find("belief") == 0:
        idea_category = "belief"
    config_keylist = [idea_category, "stages", *table_keylist]

    etl_dimen_config = etl_dimen_config_dict()
    otx_keylist = copy_copy(config_keylist)
    otx_keylist.append("set_otx_inx_args")
    if get_from_nested_dict(etl_dimen_config, otx_keylist, True):
        columns = find_set_otx_inx_args(columns)

    update_keylist = copy_copy(config_keylist)
    update_keylist.append("add")
    update_cols = get_from_nested_dict(etl_dimen_config, update_keylist, True)
    columns.update(get_empty_set_if_None(update_cols))

    update_keylist = copy_copy(config_keylist)
    update_keylist.append("remove")
    remove_cols = get_from_nested_dict(etl_dimen_config, update_keylist, True)
    columns -= set(get_empty_set_if_None(remove_cols))

    return columns


def create_prime_table_sqlstr(
    x_dimen: str, stage0: str, stage1: str, put_del: str = None
) -> str:
    tablename = create_prime_tablename(x_dimen, stage0, stage1, put_del)
    table_keylist = [stage0, stage1, put_del] if put_del else [stage0, stage1]
    columns = get_default_sorted_list(get_prime_columns(x_dimen, table_keylist))
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())
