from src.ch00_py.keyword_class_builder import get_keywords_src_config
from src.ch07_plan_logic.plan_config import get_all_plan_calc_args
from src.ch98_docs_builder.keyword_description_builder import (
    get_chxx_prefix_path_dict,
    get_chxx_ref_blurb,
    get_keywords_description,
    get_plan_dimen_config,
)
from src.ref.keywords import Ch98Keywords as kw


def test_get_keywords_description_ReturnsObj_HasAllkeywords():
    # ESTABLISH / WHEN
    keywords_description = get_keywords_description()

    # THEN
    assert keywords_description
    keywords_config = get_keywords_src_config()

    description_keywords = set(keywords_description.keys())
    config_keywords = set(keywords_config.keys())
    print(f"{config_keywords.difference(description_keywords)=}")
    assert keywords_description.keys() == keywords_config.keys()
    for keyword, description in keywords_description.items():
        assert description, keyword


def test_get_keywords_description_ReturnsObj_CheckDescriptions():
    # ESTABLISH / WHEN
    ch_dict = get_chxx_prefix_path_dict()
    plan_args = get_plan_dimen_config(kw.planunit)
    keg_args = get_plan_dimen_config(kw.plan_kegunit)
    reason_args = get_plan_dimen_config(kw.plan_keg_reasonunit)
    case_args = get_plan_dimen_config(kw.plan_keg_reason_caseunit)
    fact_args = get_plan_dimen_config(kw.plan_keg_factunit)
    award_args = get_plan_dimen_config(kw.plan_keg_awardunit)
    party_args = get_plan_dimen_config(kw.plan_keg_partyunit)
    healer_args = get_plan_dimen_config(kw.plan_keg_healerunit)
    person_args = get_plan_dimen_config(kw.plan_personunit)
    member_args = get_plan_dimen_config(kw.plan_person_membership)

    all_plan_calc_args = get_all_plan_calc_args()
    # print(f"{plan_config_args.keys()=}")

    # THEN
    for keyword, description in get_keywords_description().items():
        if keyword in ch_dict:
            assert description == get_chxx_ref_blurb(ch_dict, keyword)
        # print(f"{keyword=} {description=}")

        check_descriptions_str(plan_args, keyword, description, "Plan")
        check_descriptions_str(keg_args, keyword, description, "Keg")
        check_descriptions_str(reason_args, keyword, description, "Reason")
        check_descriptions_str(case_args, keyword, description, "Case")
        check_descriptions_str(fact_args, keyword, description, "Fact")
        check_descriptions_str(award_args, keyword, description, "Award")
        check_descriptions_str(party_args, keyword, description, "Labor")
        check_descriptions_str(healer_args, keyword, description, "Healer")
        check_descriptions_str(person_args, keyword, description, "Person")
        check_descriptions_str(member_args, keyword, description, "Member")


def check_descriptions_str(
    config_args: dict, keyword: str, description: str, src_label: str
):
    if keyword in config_args:
        keyword_config = config_args.get(keyword)
        populate_by_cashout_value = keyword_config.get(kw.populate_by_cashout)
        assert_fail_str = f"{keyword=} {description=} {populate_by_cashout_value=} "
        # print(f"{keyword} {assert_fail_str=}")
        cashout_str = f", {src_label} {kw.cashout}"
        seed_str = f", {src_label} seed"
        if keyword_config.get(kw.populate_by_cashout):
            assert cashout_str in description, assert_fail_str
            assert seed_str not in description, assert_fail_str
        else:
            assert seed_str in description, assert_fail_str
            assert cashout_str not in description, assert_fail_str
