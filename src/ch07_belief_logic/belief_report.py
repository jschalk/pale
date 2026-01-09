from pandas import DataFrame
from src.ch04_rope.rope import RopeTerm
from src.ch07_belief_logic.belief_main import BeliefUnit


def get_belief_voiceunits_dataframe(x_belief: BeliefUnit) -> DataFrame:
    if x_belief.voices == {}:
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
    x_voiceunits_list = list(x_belief.get_voiceunits_dict(all_attrs=True).values())
    return DataFrame(x_voiceunits_list)


def get_belief_agenda_dataframe(
    x_belief: BeliefUnit, reason_context: RopeTerm = None
) -> DataFrame:
    agenda_dict = x_belief.get_agenda_dict(necessary_reason_context=reason_context)
    if agenda_dict == {}:
        return DataFrame(
            columns=[
                "belief_name",
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
            "belief_name": x_belief.belief_name,
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
