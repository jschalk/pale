from pandas import DataFrame
from src.ch04_rope.rope import RopeTerm
from src.ch07_person_logic.person_main import PersonUnit


def get_person_partnerunits_dataframe(x_person: PersonUnit) -> DataFrame:
    if x_person.partners == {}:
        return DataFrame(
            columns=[
                "partner_name",
                "partner_cred_lumen",
                "partner_debt_lumen",
                "fund_give",
                "fund_take",
                "fund_agenda_give",
                "fund_agenda_take",
                "fund_agenda_ratio_give",
                "fund_agenda_ratio_take",
            ]
        )
    x_partnerunits_list = list(x_person.get_partnerunits_dict(all_attrs=True).values())
    return DataFrame(x_partnerunits_list)


def get_person_agenda_dataframe(
    x_person: PersonUnit, reason_context: RopeTerm = None
) -> DataFrame:
    agenda_dict = x_person.get_agenda_dict(necessary_reason_context=reason_context)
    if agenda_dict == {}:
        return DataFrame(
            columns=[
                "person_name",
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
            "person_name": x_person.person_name,
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
