from sqlite3 import Cursor as sqlite3_Cursor
from src.ch01_py.dict_toolbox import set_in_nested_dict
from src.ch11_bud.bud_main import MomentLabel
from src.ch18_world_etl.etl_sqlstr import get_moment_heard_select1_sqlstrs


def get_moment_dict_from_heard_tables(
    cursor: sqlite3_Cursor, moment_label: MomentLabel
) -> dict:
    fu1_sqlstrs = get_moment_heard_select1_sqlstrs(moment_label)
    return get_moment_dict_from_sqlstrs(cursor, fu1_sqlstrs, moment_label)


def get_moment_dict_from_sqlstrs(
    cursor: sqlite3_Cursor, fu1_sqlstrs: dict[str, str], moment_label: MomentLabel
) -> dict:
    cursor.execute(fu1_sqlstrs.get("momentunit"))
    momentunit_row = cursor.fetchone()
    if not momentunit_row:
        return None  # momentunit not found

    epoch_label = momentunit_row[1]
    c400_number = momentunit_row[2]
    yr1_jan1_offset = momentunit_row[3]
    monthday_index = momentunit_row[4]

    moment_dict: dict[str, any] = {"moment_label": momentunit_row[0], "epoch": {}}
    if (
        epoch_label is not None
        and c400_number is not None
        and yr1_jan1_offset is not None
        and monthday_index is not None
    ):
        if epoch_label:
            moment_dict["epoch"]["epoch_label"] = epoch_label
        if c400_number:
            moment_dict["epoch"]["c400_number"] = c400_number
        if yr1_jan1_offset:
            moment_dict["epoch"]["yr1_jan1_offset"] = yr1_jan1_offset
        if monthday_index:
            moment_dict["epoch"]["monthday_index"] = monthday_index

    if fund_grain := momentunit_row[5]:
        moment_dict["fund_grain"] = fund_grain
    if mana_grain := momentunit_row[6]:
        moment_dict["mana_grain"] = mana_grain
    if respect_grain := momentunit_row[7]:
        moment_dict["respect_grain"] = respect_grain
    if knot := momentunit_row[8]:
        moment_dict["knot"] = knot

    cursor.execute(fu1_sqlstrs.get("moment_paybook"))
    _set_moment_dict_mmtpayy(cursor, moment_dict, moment_label)

    cursor.execute(fu1_sqlstrs.get("moment_budunit"))
    _set_moment_dict_momentbud(cursor, moment_dict)

    cursor.execute(fu1_sqlstrs.get("moment_epoch_hour"))
    _set_moment_dict_mmthour(cursor, moment_dict)

    cursor.execute(fu1_sqlstrs.get("moment_epoch_month"))
    _set_moment_dict_mmtmont(cursor, moment_dict)

    cursor.execute(fu1_sqlstrs.get("moment_epoch_weekday"))
    _set_moment_dict_mmtweek(cursor, moment_dict)

    cursor.execute(fu1_sqlstrs.get("moment_timeoffi"))
    _set_moment_dict_timeoffi(cursor, moment_dict)
    return moment_dict


def _set_moment_dict_mmtpayy(
    cursor: sqlite3_Cursor, moment_dict: dict, x_moment_label: str
):
    tranunits_dict = {}
    for mmtpayy_row in cursor.fetchall():
        row_moment_label = mmtpayy_row[0]
        row_plan_name = mmtpayy_row[1]
        row_person_name = mmtpayy_row[2]
        row_tran_time = mmtpayy_row[3]
        row_amount = mmtpayy_row[4]
        keylist = [row_plan_name, row_person_name, row_tran_time]
        set_in_nested_dict(tranunits_dict, keylist, row_amount)
    paybook_dict = {"moment_label": x_moment_label, "tranunits": tranunits_dict}
    moment_dict["paybook"] = paybook_dict


def _set_moment_dict_momentbud(cursor: sqlite3_Cursor, moment_dict: dict):
    planbudhistorys_dict = {}
    for mmtpayy_row in cursor.fetchall():
        row_moment_label = mmtpayy_row[0]
        row_plan_name = mmtpayy_row[1]
        row_bud_time = mmtpayy_row[2]
        row_quota = mmtpayy_row[3]
        row_celldepth = mmtpayy_row[4]
        plan_keylist = [row_plan_name, "plan_name"]
        set_in_nested_dict(planbudhistorys_dict, plan_keylist, row_plan_name)
        keylist = [row_plan_name, "buds", row_bud_time]
        bud_epochtime_dict = {
            "bud_time": row_bud_time,
            "quota": row_quota,
            "celldepth": row_celldepth,
        }
        set_in_nested_dict(planbudhistorys_dict, keylist, bud_epochtime_dict)
    moment_dict["planbudhistorys"] = planbudhistorys_dict


def _set_moment_dict_mmthour(cursor: sqlite3_Cursor, moment_dict: dict):
    hours_config_list = []
    for mmtpayy_row in cursor.fetchall():
        row_moment_label = mmtpayy_row[0]
        row_cumulative_minute = mmtpayy_row[1]
        row_hour_label = mmtpayy_row[2]
        hours_config_list.append([row_hour_label, row_cumulative_minute])
    if hours_config_list:
        moment_dict["epoch"]["hours_config"] = hours_config_list


def _set_moment_dict_mmtmont(cursor: sqlite3_Cursor, moment_dict: dict):
    months_config_list = []
    for mmtpayy_row in cursor.fetchall():
        row_moment_label = mmtpayy_row[0]
        row_cumulative_day = mmtpayy_row[1]
        row_month_label = mmtpayy_row[2]
        months_config_list.append([row_month_label, row_cumulative_day])
    if months_config_list:
        moment_dict["epoch"]["months_config"] = months_config_list


def _set_moment_dict_mmtweek(cursor: sqlite3_Cursor, moment_dict: dict):
    weekday_dict = {}
    for mmtpayy_row in cursor.fetchall():
        row_moment_label = mmtpayy_row[0]
        row_weekday_order = mmtpayy_row[1]
        row_weekday_label = mmtpayy_row[2]
        weekday_dict[row_weekday_order] = row_weekday_label
    weekday_config_list = [weekday_dict[key] for key in sorted(weekday_dict.keys())]
    if weekday_dict:
        moment_dict["epoch"]["weekdays_config"] = weekday_config_list


def _set_moment_dict_timeoffi(cursor: sqlite3_Cursor, moment_dict: dict):
    offi_times_set = set()
    for mmtpayy_row in cursor.fetchall():
        row_moment_label = mmtpayy_row[0]
        row_offi_time = mmtpayy_row[1]
        offi_times_set.add(row_offi_time)
    moment_dict["offi_times"] = list(offi_times_set)
