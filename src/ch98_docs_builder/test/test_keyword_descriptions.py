from src.ch00_py.keyword_class_builder import get_keywords_src_config
from src.ch07_plan_logic.plan_config import get_all_plan_calc_args
from src.ch14_moment.moment_config import get_moment_config_args
from src.ch15_nabu.nabu_config import get_nabu_args, get_nabuable_args
from src.ch16_translate.translate_config import get_translate_config_args
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
    print(f"{description_keywords.difference(config_keywords)=}")
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

    trllabe_args = get_translate_config_args(kw.translate_label)
    trlname_args = get_translate_config_args(kw.translate_name)
    trlrope_args = get_translate_config_args(kw.translate_rope)
    trltitl_args = get_translate_config_args(kw.translate_title)

    mmtbudd_args = get_moment_config_args(kw.moment_budunit)
    mmthour_args = get_moment_config_args(kw.moment_epoch_hour)
    mmtmont_args = get_moment_config_args(kw.moment_epoch_month)
    mmtweek_args = get_moment_config_args(kw.moment_epoch_weekday)
    mmtpayy_args = get_moment_config_args(kw.moment_paybook)
    mmtoffi_args = get_moment_config_args(kw.moment_timeoffi)
    mmtunit_args = get_moment_config_args(kw.momentunit)
    nabu_args = get_nabu_args()
    nabuable_args = get_nabuable_args()

    all_plan_calc_args = get_all_plan_calc_args()
    # print(f"{plan_config_args.keys()=}")

    # THEN
    for keyword, desc in get_keywords_description().items():
        if keyword in ch_dict:
            assert desc == get_chxx_ref_blurb(ch_dict, keyword)
        # print(f"{keyword=} {desc=}")

        check_plan_desc_str(plan_args, keyword, desc, "Plan")
        check_plan_desc_str(keg_args, keyword, desc, "Keg")
        check_plan_desc_str(reason_args, keyword, desc, "Reason")
        check_plan_desc_str(case_args, keyword, desc, "Case")
        check_plan_desc_str(fact_args, keyword, desc, "Fact")
        check_plan_desc_str(award_args, keyword, desc, "Award")
        check_plan_desc_str(party_args, keyword, desc, "Labor")
        check_plan_desc_str(healer_args, keyword, desc, "Healer")
        check_plan_desc_str(person_args, keyword, desc, "Person")
        check_plan_desc_str(member_args, keyword, desc, "Member")
        check_translate_desc_str(trllabe_args, keyword, desc, kw.translate_label)
        check_translate_desc_str(trlname_args, keyword, desc, kw.translate_name)
        check_translate_desc_str(trlrope_args, keyword, desc, kw.translate_rope)
        check_translate_desc_str(trltitl_args, keyword, desc, kw.translate_title)
        check_mmtunit_desc_str(mmtbudd_args, keyword, desc, "bud")
        check_mmtunit_desc_str(mmthour_args, keyword, desc, kw.mmthour)
        check_mmtunit_desc_str(mmtmont_args, keyword, desc, kw.mmtmont)
        check_mmtunit_desc_str(mmtweek_args, keyword, desc, kw.mmtweek)
        check_mmtunit_desc_str(mmtpayy_args, keyword, desc, kw.paybook)
        check_mmtunit_desc_str(mmtoffi_args, keyword, desc, kw.offi_time)
        check_mmtunit_desc_str(mmtunit_args, keyword, desc, "Moment")
        check_mmtunit_desc_str(nabu_args, keyword, desc, kw.nabu)
        check_mmtunit_desc_str(nabuable_args, keyword, desc, "Nabuable")


def check_plan_desc_str(
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


def check_mmtunit_desc_str(
    config_args: dict, keyword: str, description: str, src_label: str
):
    if keyword in config_args:
        # keyword_config = config_args.get(keyword)
        assert_fail_str = f"{keyword=} {description=} "
        # print(f"{keyword} {assert_fail_str=}")
        assert f", {src_label} arg" in description, assert_fail_str


def check_translate_desc_str(
    config_args: dict, keyword: str, description: str, src_label: str
):
    if keyword in config_args:
        assert_fail_str = f"{keyword=} {description=} "
        # print(f"{keyword} {assert_fail_str=}")
        assert f", {src_label.upper()} arg" in description, assert_fail_str
