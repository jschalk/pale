from os import getcwd as os_getcwd
from src.ch01_py.dict_toolbox import get_from_nested_dict
from src.ch01_py.file_toolbox import create_path, open_json
from src.ch08_belief_atom.atom_config import get_all_belief_dimen_delete_keys


def rose_config_path() -> str:
    "Returns path: c16_rose/rose_config.json"
    src_dir = create_path(os_getcwd(), "src")
    chapter_dir = create_path(src_dir, "ch16_rose")
    return create_path(chapter_dir, "rose_config.json")


def get_rose_filename() -> str:
    return "rose.json"


def get_rose_config_dict() -> dict:
    return open_json(rose_config_path())


def get_rose_dimens() -> set[str]:
    return set(get_rose_config_dict().keys())


def default_unknown_str() -> str:
    return "UNKNOWN"


def default_unknown_str_if_None(unknown_str: any = None) -> str:
    if unknown_str != unknown_str:
        unknown_str = None
    if unknown_str is None:
        unknown_str = default_unknown_str()
    return unknown_str


def get_rose_config_jkeys(x_dimen: str) -> dict:
    jkeys_key_list = [x_dimen, "jkeys"]
    return get_from_nested_dict(get_rose_config_dict(), jkeys_key_list)


def get_rose_config_jvalues(x_dimen: str) -> dict:
    jvalues_key_list = [x_dimen, "jvalues"]
    return get_from_nested_dict(get_rose_config_dict(), jvalues_key_list)


def get_rose_config_args(x_dimen: str) -> dict[str, dict]:
    args_dict = get_rose_config_jkeys(x_dimen)
    args_dict.update(get_rose_config_jvalues(x_dimen))
    return args_dict


def get_rose_args_dimen_mapping() -> dict[str, str]:
    x_dict = {}
    for rose_dimen in get_rose_config_dict().keys():
        args_set = set(get_rose_config_args(rose_dimen))
        for x_arg in args_set:
            if x_dict.get(x_arg) is None:
                x_dict[x_arg] = {rose_dimen}
            else:
                x_dimen_set = x_dict.get(x_arg)
                x_dimen_set.add(rose_dimen)
                x_dict[x_arg] = x_dimen_set
    return x_dict


def get_rose_args_class_types() -> dict[str, str]:
    return {
        "active_requisite": "bool",
        "addin": "float",
        "amount": "float",
        "awardee_title": "TitleTerm",
        "begin": "float",
        "belief_name": "NameTerm",
        "bud_time": "EpochTime",
        "c400_number": "int",
        "celldepth": "int",
        "close": "float",
        "credor_respect": "float",
        "cumulative_day": "int",
        "cumulative_minute": "int",
        "debtor_respect": "float",
        "denom": "int",
        "epoch_label": "LabelTerm",
        "face_name": "NameTerm",
        "fact_context": "RopeTerm",
        "fact_state": "RopeTerm",
        "fact_upper": "ContextNum",
        "fact_lower": "ContextNum",
        "fund_grain": "float",
        "fund_pool": "float",
        "give_force": "float",
        "gogo_want": "float",
        "group_cred_lumen": "float",
        "group_debt_lumen": "float",
        "group_title": "TitleTerm",
        "healer_name": "NameTerm",
        "hour_label": "LabelTerm",
        "job_listen_rotations": "int",
        "knot": "str",
        "mana_grain": "float",
        "max_tree_traverse": "int",
        "moment_label": "LabelTerm",
        "month_label": "LabelTerm",
        "monthday_index": "int",
        "morph": "bool",
        "numor": "int",
        "offi_time": "EpochTime",
        "quota": "int",
        "party_title": "TitleTerm",
        "plan_rope": "RopeTerm",
        "pledge": "bool",
        "problem_bool": "bool",
        "reason_context": "RopeTerm",
        "reason_divisor": "int",
        "reason_lower": "ContextNum",
        "reason_upper": "ContextNum",
        "reason_state": "RopeTerm",
        "star": "int",
        "respect_grain": "float",
        "solo": "int",
        "stop_want": "float",
        "take_force": "float",
        "tally": "int",
        "tran_time": "EpochTime",
        "voice_name": "NameTerm",
        "voice_cred_lumen": "float",
        "voice_debt_lumen": "float",
        "weekday_label": "LabelTerm",
        "weekday_order": "int",
        "yr1_jan1_offset": "int",
    }


def get_quick_roses_column_ref() -> dict[str, set[str]]:
    """for each rose_config dimen contains the associated columns"""
    return {
        "rose_epoch": {"inx_epoch_diff", "otx_epoch_length"},
        "rose_title": {
            "inx_title",
            "otx_title",
            "inx_knot",
            "otx_knot",
            "unknown_str",
        },
        "rose_name": {
            "inx_name",
            "otx_name",
            "inx_knot",
            "otx_knot",
            "unknown_str",
        },
        "rose_label": {
            "inx_label",
            "otx_label",
            "inx_knot",
            "otx_knot",
            "unknown_str",
        },
        "rose_rope": {
            "inx_rope",
            "otx_rope",
            "inx_knot",
            "otx_knot",
            "unknown_str",
        },
    }


def roseable_class_types() -> set:
    return {"NameTerm", "TitleTerm", "LabelTerm", "RopeTerm", "EpochTime"}


def get_roseable_term_class_types() -> set:
    return {"NameTerm", "TitleTerm", "LabelTerm", "RopeTerm"}


def get_roseable_number_class_types() -> set:
    return {"EpochTime"}


def get_roseable_args() -> set:
    return {
        "awardee_title",
        "belief_name",
        "bud_time",
        "epoch_label",
        "face_name",
        "fact_context",
        "fact_state",
        "group_title",
        "healer_name",
        "hour_label",
        "moment_label",
        "month_label",
        "party_title",
        "plan_rope",
        "offi_time",
        "reason_context",
        "reason_state",
        "tran_time",
        "voice_name",
        "weekday_label",
    }


def find_set_otx_inx_args(args: set) -> set:
    """Receives set of args, returns a set with all "Roseable" args replaced with "_otx" and "_inx" """
    all_roseable = get_roseable_args()
    all_roseable.update(get_all_belief_dimen_delete_keys())
    transformed_args = set()
    for arg in args:
        if arg in all_roseable:
            transformed_args.add(f"{arg}_otx")
            transformed_args.add(f"{arg}_inx")
        else:
            transformed_args.add(arg)
    return transformed_args


def get_rose_nameterm_args() -> set[str]:
    return {
        "voice_name",
        "face_name",
        "healer_name",
        "belief_name",
    }


def get_rose_titleterm_args() -> set[str]:
    return {
        "awardee_title",
        "group_title",
        "party_title",
    }


def get_rose_labelterm_args() -> set[str]:
    return {
        "moment_label",
        "hour_label",
        "month_label",
        "epoch_label",
        "weekday_label",
    }


def get_rose_ropeterm_args() -> set[str]:
    return {
        "fact_state",
        "fact_context",
        "plan_rope",
        "reason_state",
        "reason_context",
    }


def get_rose_epochtime_args() -> set[str]:
    return {"bud_time", "offi_time", "tran_time"}
