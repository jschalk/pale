from pandas import DataFrame
from src.ch04_rope.rope import RopeTerm
from src.ch07_plan_logic.plan_main import PlanUnit


def get_plan_voiceunits_dataframe(x_plan: PlanUnit) -> DataFrame:
    if x_plan.voices == {}:
        return DataFrame(
            columns=[
                "voice_name",
                "voice_cred_lumen",
                "voice_debt_lumen",
                "fund_give",
                "fund_take",
                "fund_agenda_give",
                "fund_agenda_take",
                "fund_agenda_ratio_give",
                "fund_agenda_ratio_take",
            ]
        )
    x_voiceunits_list = list(x_plan.get_voiceunits_dict(all_attrs=True).values())
    return DataFrame(x_voiceunits_list)


def get_plan_agenda_dataframe(
    x_plan: PlanUnit, reason_context: RopeTerm = None
) -> DataFrame:
    agenda_dict = x_plan.get_agenda_dict(necessary_reason_context=reason_context)
    if agenda_dict == {}:
        return DataFrame(
            columns=[
                "plan_name",
                "fund_ratio",
                "keg_label",
                "parent_rope",
                "begin",
                "close",
                "addin",
                "denom",
                "numor",
                "morph",
            ]
        )
    x_keg_list = []
    for x_keg in agenda_dict.values():
        keg_dict = {
            "plan_name": x_plan.plan_name,
            "fund_ratio": x_keg.fund_ratio,
            "keg_label": x_keg.keg_label,
            "parent_rope": x_keg.parent_rope,
            "begin": x_keg.begin,
            "close": x_keg.close,
            "addin": x_keg.addin,
            "denom": x_keg.denom,
            "numor": x_keg.numor,
            "morph": x_keg.morph,
        }
        x_keg_list.append(keg_dict)
    return DataFrame(x_keg_list)
