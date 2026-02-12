# from src.ch00_py.dict_toolbox import get_from_nested_dict
from os import getcwd as os_getcwd
from os.path import exists as os_path_exists
from src.ch00_py.file_toolbox import create_path
from src.ch07_plan_logic.plan_config import (
    get_all_plan_calc_args,
    get_plan_calc_args_sqlite_datatype_dict,
    get_plan_calc_args_type_dict,
    get_plan_calc_dimen_args,
    get_plan_calc_dimens,
    get_plan_config_dict,
    max_tree_traverse_default,
    plan_config_path,
)
from src.ch07_plan_logic.plan_main import PartnerUnit, PlanUnit
from src.ref.keywords import Ch07Keywords as kw


def test_max_tree_traverse_default_ReturnsObj() -> str:
    # ESTABLISH / WHEN / THEN
    assert max_tree_traverse_default() == 20


def test_get_plan_config_dict_Exists():
    # ESTABLISH
    src_dir = create_path(os_getcwd(), "src")
    expected_dir = create_path(src_dir, "ch07_plan_logic")

    # WHEN
    config_path = plan_config_path()
    # THEN
    expected_path = create_path(expected_dir, "plan_config.json")
    assert config_path == expected_path
    assert os_path_exists(plan_config_path())


def test_get_plan_config_dict_ReturnsObj_CheckLevel0Keys():
    # ESTABLISH / WHEN
    plan_config = get_plan_config_dict()
    plan_config_keys = set(plan_config.keys())

    # THEN
    assert kw.planunit in plan_config_keys
    assert kw.plan_partnerunit in plan_config_keys
    assert kw.plan_partner_membership in plan_config_keys
    assert kw.plan_kegunit in plan_config_keys
    assert kw.plan_keg_awardunit in plan_config_keys
    assert kw.plan_keg_reasonunit in plan_config_keys
    assert kw.plan_keg_reason_caseunit in plan_config_keys
    assert kw.plan_keg_partyunit in plan_config_keys
    assert kw.plan_keg_healerunit in plan_config_keys
    assert kw.plan_keg_factunit in plan_config_keys
    assert kw.plan_groupunit in plan_config_keys
    assert len(get_plan_config_dict()) == 11


def test_get_plan_config_dict_ReturnsObj_CheckLevel1Keys():
    # ESTABLISH / WHEN
    plan_config = get_plan_config_dict()

    # THEN
    # sourcery skip: no-loop-in-tests
    for level1_key, attribute_dict in plan_config.items():
        attribute_keys = set(attribute_dict.keys())
        print(f"{level1_key=} {attribute_keys=}")
        assert "abbreviation" in attribute_keys
        assert kw.jkeys in attribute_keys
        assert kw.jvalues in attribute_keys
        assert len(attribute_keys) == 3


def test_get_plan_config_dict_ReturnsObj_Check_populate_by_cashout():
    # ESTABLISH / WHEN
    plan_config = get_plan_config_dict()

    # THEN
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    abbr_str = "abbreviation"
    for level1_key, attribute_dict in plan_config.items():
        for level2_key, fm_attribute_dict in attribute_dict.items():
            if level2_key != abbr_str:
                for fm_attr_key, fm_attr_value in fm_attribute_dict.items():
                    populate_by_cashout_value = fm_attr_value.get("populate_by_cashout")
                    assertion_fail_str = f"{fm_attr_key} Value must be Boolean {populate_by_cashout_value=}"
                    assert populate_by_cashout_value in [
                        True,
                        False,
                    ], assertion_fail_str


def test_get_plan_config_dict_ReturnsObj_CheckAbbreviations():
    # ESTABLISH / WHEN
    plan_config = get_plan_config_dict()

    # THEN
    plnunit_attribute = plan_config.get(kw.planunit)
    plnptnr_attribute = plan_config.get(kw.plan_partnerunit)
    plnmemb_attribute = plan_config.get(kw.plan_partner_membership)
    plnkegg_attribute = plan_config.get(kw.plan_kegunit)
    plnawar_attribute = plan_config.get(kw.plan_keg_awardunit)
    plnreas_attribute = plan_config.get(kw.plan_keg_reasonunit)
    plncase_attribute = plan_config.get(kw.plan_keg_reason_caseunit)
    plnlabo_attribute = plan_config.get(kw.plan_keg_partyunit)
    plnheal_attribute = plan_config.get(kw.plan_keg_healerunit)
    plnfact_attribute = plan_config.get(kw.plan_keg_factunit)
    plngrou_attribute = plan_config.get(kw.plan_groupunit)
    abbr_str = "abbreviation"
    assert plnunit_attribute.get(abbr_str) == kw.plnunit
    assert plnptnr_attribute.get(abbr_str) == kw.plnptnr
    assert plnmemb_attribute.get(abbr_str) == kw.plnmemb
    assert plnkegg_attribute.get(abbr_str) == kw.plnkegg
    assert plnawar_attribute.get(abbr_str) == kw.plnawar
    assert plnreas_attribute.get(abbr_str) == kw.plnreas
    assert plncase_attribute.get(abbr_str) == kw.plncase
    assert plnlabo_attribute.get(abbr_str) == kw.plnlabo
    assert plnheal_attribute.get(abbr_str) == kw.plnheal
    assert plnfact_attribute.get(abbr_str) == kw.plnfact
    assert plngrou_attribute.get(abbr_str) == kw.plngrou


def test_get_all_plan_calc_args_ReturnsObj():
    # ESTABLISH / WHEN
    all_plan_calc_args = get_all_plan_calc_args()

    # THEN
    assert all_plan_calc_args
    assert kw.stop_want in all_plan_calc_args
    assert kw.keg_rope in all_plan_calc_args
    assert kw.fund_give in all_plan_calc_args
    assert all_plan_calc_args.get(kw.fund_give) == {
        kw.plan_keg_awardunit,
        kw.plan_partner_membership,
        kw.plan_groupunit,
        kw.plan_partnerunit,
    }

    assert len(all_plan_calc_args) == 77


def test_get_plan_config_dict_ReturnsObj_CheckArgDataTypesKeysExist():
    # ESTABLISH / WHEN
    plan_config = get_plan_config_dict()

    # THEN
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for level1_key, attribute_dict in plan_config.items():
        for level2_key, fm_attribute_dict in attribute_dict.items():
            if level2_key in {kw.jkeys, kw.jvalues}:
                for level3_key, attr_dict in fm_attribute_dict.items():
                    print(
                        f"{level1_key=} {level2_key=} {level3_key=} {set(attr_dict.keys())=}"
                    )
                    assert set(attr_dict.keys()) == {
                        kw.class_type,
                        kw.sqlite_datatype,
                        kw.populate_by_cashout,
                    }


def test_get_plan_calc_dimens_ReturnsObj():
    # ESTABLISH / WHEN
    plan_calc_dimens = get_plan_calc_dimens()

    # THEN
    expected_plan_calc_dimens = {
        kw.planunit,
        kw.plan_partnerunit,
        kw.plan_partner_membership,
        kw.plan_kegunit,
        kw.plan_keg_awardunit,
        kw.plan_keg_reasonunit,
        kw.plan_keg_reason_caseunit,
        kw.plan_keg_partyunit,
        kw.plan_keg_healerunit,
        kw.plan_keg_factunit,
        kw.plan_groupunit,
    }
    assert plan_calc_dimens == expected_plan_calc_dimens
    assert plan_calc_dimens == set(get_plan_config_dict().keys())


def test_get_plan_calc_dimen_args_ReturnsObj():
    # ESTABLISH / WHEN
    plan_partnerunit_args = get_plan_calc_dimen_args(kw.plan_partnerunit)
    plan_kegunit_args = get_plan_calc_dimen_args(kw.plan_kegunit)
    plan_groupunit_args = get_plan_calc_dimen_args(kw.plan_groupunit)

    #  THEN
    print(f"          {plan_partnerunit_args=}")
    print("")
    print(f"{set(PartnerUnit().__dict__.keys())=}")
    # print(plan_partnerunit_args.difference(set(PartnerUnit().__dict__.keys())))
    # assert plan_partnerunit_args == set(PartnerUnit().__dict__.keys())
    assert plan_partnerunit_args == {
        kw.moment_rope,
        kw.plan_name,
        kw.credor_pool,
        kw.debtor_pool,
        kw.fund_agenda_give,
        kw.fund_agenda_take,
        kw.fund_agenda_ratio_give,
        kw.fund_agenda_ratio_take,
        kw.fund_give,
        kw.fund_take,
        kw.partner_cred_lumen,
        kw.partner_debt_lumen,
        kw.partner_name,
        kw.inallocable_partner_debt_lumen,
        kw.irrational_partner_debt_lumen,
        kw.groupmark,
    }
    assert plan_kegunit_args == {
        kw.moment_rope,
        kw.plan_name,
        kw.morph,
        kw.denom,
        kw.pledge,
        kw.close,
        kw.addin,
        kw.numor,
        kw.star,
        kw.stop_want,
        kw.gogo_calc,
        kw.stop_calc,
        kw.keg_active,
        kw.fund_onset,
        kw.fund_cease,
        kw.descendant_pledge_count,
        kw.all_partner_cred,
        kw.all_partner_debt,
        kw.healerunit_ratio,
        kw.tree_level,
        kw.task,
        kw.fund_grain,
        kw.fund_ratio,
        kw.range_evaluated,
        kw.problem_bool,
        kw.gogo_want,
        kw.keg_rope,
        kw.begin,
    }
    print(f"{plan_groupunit_args=}")
    assert plan_groupunit_args == {
        kw.moment_rope,
        kw.plan_name,
        kw.debtor_pool,
        kw.credor_pool,
        kw.fund_give,
        kw.group_title,
        kw.fund_agenda_give,
        kw.fund_agenda_take,
        kw.fund_take,
        kw.fund_grain,
    }


def g_class_type(
    config: dict[str, dict[str, dict]], key1: str, key2: str, key3: str
) -> str:
    dimen = config.get(key1)
    j_dict = dimen.get(key2)
    j_arg = j_dict.get(key3)
    return j_arg.get(kw.class_type)


def g_sqlitetype(
    config: dict[str, dict[str, dict]], key1: str, key2: str, key3: str
) -> str:
    dimen = config.get(key1)
    j_dict = dimen.get(key2)
    j_arg = j_dict.get(key3)
    return j_arg.get(kw.sqlite_datatype)


def g_popcashout(
    config: dict[str, dict[str, dict]], key1: str, key2: str, key3: str
) -> str:
    dimen = config.get(key1)
    j_dict = dimen.get(key2)
    j_arg = j_dict.get(key3)
    return j_arg.get(kw.populate_by_cashout)


def test_get_plan_config_dict_ReturnsObj_CheckArgDataTypesCorrect():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH / WHEN
    cfig = get_plan_config_dict()

    # THEN
    # for level1_key, attribute_dict in config.items():
    #     for level2_key, fm_attribute_dict in attribute_dict.items():
    #         if level2_key in {kw.jkeys, kw.jvalues}:
    #             for level3_key, attr_dict in fm_attribute_dict.items():
    #                 dimem = attribute_dict.get("abbreviation")
    #                 x_class_type = attr_dict.get(kw.class_type)
    #                 x_sqlite_datatype = attr_dict.get(kw.sqlite_datatype)
    #                 print(
    #                     f"""    assert g_class_type(config, {dimem}, {level2_key[0:2]}, "{level3_key}") == "{x_class_type}" """
    #                 )
    #                 print(
    #                     f"""    assert g_sqlitetype(config, {dimem}, {level2_key[0:2]}, "{level3_key}") == "{x_sqlite_datatype}" """
    #                 )

    jk = kw.jkeys
    jv = kw.jvalues
    plnunit = kw.planunit
    plnptnr = kw.plan_partnerunit
    plnmemb = kw.plan_partner_membership
    plnkegg = kw.plan_kegunit
    plnawar = kw.plan_keg_awardunit
    plnreas = kw.plan_keg_reasonunit
    plncase = kw.plan_keg_reason_caseunit
    plnlabo = kw.plan_keg_partyunit
    plnheal = kw.plan_keg_healerunit
    plnfact = kw.plan_keg_factunit
    plngrou = kw.plan_groupunit
    assert g_class_type(cfig, plnmemb, jk, kw.partner_name) == kw.NameTerm
    assert g_sqlitetype(cfig, plnmemb, jk, kw.partner_name) == "TEXT"
    assert g_popcashout(cfig, plnmemb, jk, kw.partner_name) == False

    assert g_class_type(cfig, plnmemb, jk, kw.group_title) == kw.TitleTerm
    assert g_sqlitetype(cfig, plnmemb, jk, kw.group_title) == "TEXT"
    assert g_popcashout(cfig, plnmemb, jk, kw.group_title) == False

    assert g_class_type(cfig, plnmemb, jv, kw.credor_pool) == "float"
    assert g_sqlitetype(cfig, plnmemb, jv, kw.credor_pool) == "REAL"
    assert g_popcashout(cfig, plnmemb, jv, kw.credor_pool) == True

    assert g_class_type(cfig, plnmemb, jv, kw.debtor_pool) == "float"
    assert g_sqlitetype(cfig, plnmemb, jv, kw.debtor_pool) == "REAL"
    assert g_popcashout(cfig, plnmemb, jv, kw.debtor_pool) == True

    assert g_class_type(cfig, plnmemb, jv, kw.fund_agenda_give) == "float"
    assert g_sqlitetype(cfig, plnmemb, jv, kw.fund_agenda_give) == "REAL"
    assert g_popcashout(cfig, plnmemb, jv, kw.fund_agenda_give) == True

    assert g_class_type(cfig, plnmemb, jv, kw.fund_agenda_ratio_give) == "float"
    assert g_sqlitetype(cfig, plnmemb, jv, kw.fund_agenda_ratio_give) == "REAL"
    assert g_popcashout(cfig, plnmemb, jv, kw.fund_agenda_ratio_give) == True

    assert g_class_type(cfig, plnmemb, jv, kw.fund_agenda_ratio_take) == "float"
    assert g_sqlitetype(cfig, plnmemb, jv, kw.fund_agenda_ratio_take) == "REAL"
    assert g_popcashout(cfig, plnmemb, jv, kw.fund_agenda_ratio_take) == True

    assert g_class_type(cfig, plnmemb, jv, kw.fund_agenda_take) == "float"
    assert g_sqlitetype(cfig, plnmemb, jv, kw.fund_agenda_take) == "REAL"
    assert g_popcashout(cfig, plnmemb, jv, kw.fund_agenda_take) == True

    assert g_class_type(cfig, plnmemb, jv, kw.fund_give) == "float"
    assert g_sqlitetype(cfig, plnmemb, jv, kw.fund_give) == "REAL"
    assert g_popcashout(cfig, plnmemb, jv, kw.fund_give) == True

    assert g_class_type(cfig, plnmemb, jv, kw.fund_take) == "float"
    assert g_sqlitetype(cfig, plnmemb, jv, kw.fund_take) == "REAL"
    assert g_popcashout(cfig, plnmemb, jv, kw.fund_take) == True

    assert g_class_type(cfig, plnmemb, jv, kw.group_cred_lumen) == "float"
    assert g_sqlitetype(cfig, plnmemb, jv, kw.group_cred_lumen) == "REAL"
    assert g_popcashout(cfig, plnmemb, jv, kw.group_cred_lumen) == False

    assert g_class_type(cfig, plnmemb, jv, kw.group_debt_lumen) == "float"
    assert g_sqlitetype(cfig, plnmemb, jv, kw.group_debt_lumen) == "REAL"
    assert g_popcashout(cfig, plnmemb, jv, kw.group_debt_lumen) == False

    assert g_class_type(cfig, plnptnr, jk, kw.partner_name) == kw.NameTerm
    assert g_sqlitetype(cfig, plnptnr, jk, kw.partner_name) == "TEXT"
    assert g_popcashout(cfig, plnptnr, jk, kw.partner_name) == False

    assert g_class_type(cfig, plnptnr, jv, kw.credor_pool) == "float"
    assert g_sqlitetype(cfig, plnptnr, jv, kw.credor_pool) == "REAL"
    assert g_popcashout(cfig, plnptnr, jv, kw.credor_pool) == True

    assert g_class_type(cfig, plnptnr, jv, kw.debtor_pool) == "float"
    assert g_sqlitetype(cfig, plnptnr, jv, kw.debtor_pool) == "REAL"
    assert g_popcashout(cfig, plnptnr, jv, kw.debtor_pool) == True

    assert g_class_type(cfig, plnptnr, jv, kw.fund_agenda_give) == "float"
    assert g_sqlitetype(cfig, plnptnr, jv, kw.fund_agenda_give) == "REAL"
    assert g_popcashout(cfig, plnptnr, jv, kw.fund_agenda_give) == True

    assert g_class_type(cfig, plnptnr, jv, kw.fund_agenda_ratio_give) == "float"
    assert g_sqlitetype(cfig, plnptnr, jv, kw.fund_agenda_ratio_give) == "REAL"
    assert g_popcashout(cfig, plnptnr, jv, kw.fund_agenda_ratio_give) == True

    assert g_class_type(cfig, plnptnr, jv, kw.fund_agenda_ratio_take) == "float"
    assert g_sqlitetype(cfig, plnptnr, jv, kw.fund_agenda_ratio_take) == "REAL"
    assert g_popcashout(cfig, plnptnr, jv, kw.fund_agenda_ratio_take) == True

    assert g_class_type(cfig, plnptnr, jv, kw.fund_agenda_take) == "float"
    assert g_sqlitetype(cfig, plnptnr, jv, kw.fund_agenda_take) == "REAL"
    assert g_popcashout(cfig, plnptnr, jv, kw.fund_agenda_take) == True

    assert g_class_type(cfig, plnptnr, jv, kw.fund_give) == "float"
    assert g_sqlitetype(cfig, plnptnr, jv, kw.fund_give) == "REAL"
    assert g_popcashout(cfig, plnptnr, jv, kw.fund_give) == True

    assert g_class_type(cfig, plnptnr, jv, kw.fund_take) == "float"
    assert g_sqlitetype(cfig, plnptnr, jv, kw.fund_take) == "REAL"
    assert g_popcashout(cfig, plnptnr, jv, kw.fund_take) == True

    assert g_class_type(cfig, plnptnr, jv, kw.inallocable_partner_debt_lumen) == "float"
    assert g_sqlitetype(cfig, plnptnr, jv, kw.inallocable_partner_debt_lumen) == "REAL"
    assert g_popcashout(cfig, plnptnr, jv, kw.inallocable_partner_debt_lumen) == True

    assert g_class_type(cfig, plnptnr, jv, kw.irrational_partner_debt_lumen) == "float"
    assert g_sqlitetype(cfig, plnptnr, jv, kw.irrational_partner_debt_lumen) == "REAL"
    assert g_popcashout(cfig, plnptnr, jv, kw.irrational_partner_debt_lumen) == True

    assert g_class_type(cfig, plnptnr, jv, kw.partner_cred_lumen) == "float"
    assert g_sqlitetype(cfig, plnptnr, jv, kw.partner_cred_lumen) == "REAL"
    assert g_popcashout(cfig, plnptnr, jv, kw.partner_cred_lumen) == False

    assert g_class_type(cfig, plnptnr, jv, kw.partner_debt_lumen) == "float"
    assert g_sqlitetype(cfig, plnptnr, jv, kw.partner_debt_lumen) == "REAL"
    assert g_popcashout(cfig, plnptnr, jv, kw.partner_debt_lumen) == False

    assert g_class_type(cfig, plngrou, jk, kw.group_title) == "TitleTerm"
    assert g_sqlitetype(cfig, plngrou, jk, kw.group_title) == "TEXT"
    assert g_popcashout(cfig, plngrou, jk, kw.group_title) == True

    assert g_class_type(cfig, plngrou, jv, kw.debtor_pool) == "float"
    assert g_sqlitetype(cfig, plngrou, jv, kw.debtor_pool) == "REAL"
    assert g_popcashout(cfig, plngrou, jv, kw.debtor_pool) == True

    assert g_class_type(cfig, plngrou, jv, kw.credor_pool) == "float"
    assert g_sqlitetype(cfig, plngrou, jv, kw.credor_pool) == "REAL"
    assert g_popcashout(cfig, plngrou, jv, kw.credor_pool) == True

    assert g_class_type(cfig, plngrou, jv, kw.fund_give) == "float"
    assert g_sqlitetype(cfig, plngrou, jv, kw.fund_give) == "REAL"
    assert g_popcashout(cfig, plngrou, jv, kw.fund_give) == True

    assert g_class_type(cfig, plngrou, jv, kw.fund_agenda_give) == "float"
    assert g_sqlitetype(cfig, plngrou, jv, kw.fund_agenda_give) == "REAL"
    assert g_popcashout(cfig, plngrou, jv, kw.fund_agenda_give) == True

    assert g_class_type(cfig, plngrou, jv, kw.fund_agenda_take) == "float"
    assert g_sqlitetype(cfig, plngrou, jv, kw.fund_agenda_take) == "REAL"
    assert g_popcashout(cfig, plngrou, jv, kw.fund_agenda_take) == True

    assert g_class_type(cfig, plngrou, jv, kw.fund_take) == "float"
    assert g_sqlitetype(cfig, plngrou, jv, kw.fund_take) == "REAL"
    assert g_popcashout(cfig, plngrou, jv, kw.fund_take) == True

    assert g_class_type(cfig, plngrou, jv, kw.fund_grain) == "float"
    assert g_sqlitetype(cfig, plngrou, jv, kw.fund_grain) == "REAL"
    assert g_popcashout(cfig, plngrou, jv, kw.fund_grain) == True

    assert g_class_type(cfig, plnawar, jk, kw.awardee_title) == kw.TitleTerm
    assert g_sqlitetype(cfig, plnawar, jk, kw.awardee_title) == "TEXT"
    assert g_popcashout(cfig, plnawar, jk, kw.awardee_title) == False

    assert g_class_type(cfig, plnawar, jk, kw.keg_rope) == kw.RopeTerm
    assert g_sqlitetype(cfig, plnawar, jk, kw.keg_rope) == "TEXT"
    assert g_popcashout(cfig, plnawar, jk, kw.keg_rope) == False

    assert g_class_type(cfig, plnawar, jv, kw.fund_give) == "float"
    assert g_sqlitetype(cfig, plnawar, jv, kw.fund_give) == "REAL"
    assert g_popcashout(cfig, plnawar, jv, kw.fund_give) == True

    assert g_class_type(cfig, plnawar, jv, kw.fund_take) == "float"
    assert g_sqlitetype(cfig, plnawar, jv, kw.fund_take) == "REAL"
    assert g_popcashout(cfig, plnawar, jv, kw.fund_take) == True

    assert g_class_type(cfig, plnawar, jv, kw.give_force) == "float"
    assert g_sqlitetype(cfig, plnawar, jv, kw.give_force) == "REAL"
    assert g_popcashout(cfig, plnawar, jv, kw.give_force) == False

    assert g_class_type(cfig, plnawar, jv, kw.take_force) == "float"
    assert g_sqlitetype(cfig, plnawar, jv, kw.take_force) == "REAL"
    assert g_popcashout(cfig, plnawar, jv, kw.take_force) == False

    assert g_class_type(cfig, plnfact, jk, kw.fact_context) == kw.RopeTerm
    assert g_sqlitetype(cfig, plnfact, jk, kw.fact_context) == "TEXT"
    assert g_popcashout(cfig, plnfact, jk, kw.fact_context) == False

    assert g_class_type(cfig, plnfact, jk, kw.keg_rope) == kw.RopeTerm
    assert g_sqlitetype(cfig, plnfact, jk, kw.keg_rope) == "TEXT"
    assert g_popcashout(cfig, plnfact, jk, kw.keg_rope) == False

    assert g_class_type(cfig, plnfact, jv, kw.fact_upper) == kw.FactNum
    assert g_sqlitetype(cfig, plnfact, jv, kw.fact_upper) == "REAL"
    assert g_popcashout(cfig, plnfact, jv, kw.fact_upper) == False

    assert g_class_type(cfig, plnfact, jv, kw.fact_lower) == kw.FactNum
    assert g_sqlitetype(cfig, plnfact, jv, kw.fact_lower) == "REAL"
    assert g_popcashout(cfig, plnfact, jv, kw.fact_lower) == False

    assert g_class_type(cfig, plnfact, jv, kw.fact_state) == kw.RopeTerm
    assert g_sqlitetype(cfig, plnfact, jv, kw.fact_state) == "TEXT"
    assert g_popcashout(cfig, plnfact, jv, kw.fact_state) == False

    assert g_class_type(cfig, plnheal, jk, kw.healer_name) == kw.NameTerm
    assert g_sqlitetype(cfig, plnheal, jk, kw.healer_name) == "TEXT"
    assert g_popcashout(cfig, plnheal, jk, kw.healer_name) == False

    assert g_class_type(cfig, plnheal, jk, kw.keg_rope) == kw.RopeTerm
    assert g_sqlitetype(cfig, plnheal, jk, kw.keg_rope) == "TEXT"
    assert g_popcashout(cfig, plnheal, jk, kw.keg_rope) == False

    assert g_class_type(cfig, plncase, jk, kw.reason_context) == kw.RopeTerm
    assert g_sqlitetype(cfig, plncase, jk, kw.reason_context) == "TEXT"
    assert g_popcashout(cfig, plncase, jk, kw.reason_context) == False

    assert g_class_type(cfig, plncase, jk, kw.reason_state) == kw.RopeTerm
    assert g_sqlitetype(cfig, plncase, jk, kw.reason_state) == "TEXT"
    assert g_popcashout(cfig, plncase, jk, kw.reason_state) == False

    assert g_class_type(cfig, plncase, jk, kw.keg_rope) == kw.RopeTerm
    assert g_sqlitetype(cfig, plncase, jk, kw.keg_rope) == "TEXT"
    assert g_popcashout(cfig, plncase, jk, kw.keg_rope) == False

    assert g_class_type(cfig, plncase, jv, kw.case_active) == "int"
    assert g_sqlitetype(cfig, plncase, jv, kw.case_active) == "INTEGER"
    assert g_popcashout(cfig, plncase, jv, kw.case_active) == True

    assert g_class_type(cfig, plncase, jv, kw.task) == "int"
    assert g_sqlitetype(cfig, plncase, jv, kw.task) == "INTEGER"
    assert g_popcashout(cfig, plncase, jv, kw.task) == True

    assert g_class_type(cfig, plncase, jv, kw.reason_divisor) == "int"
    assert g_sqlitetype(cfig, plncase, jv, kw.reason_divisor) == "INTEGER"
    assert g_popcashout(cfig, plncase, jv, kw.reason_divisor) == False

    assert g_class_type(cfig, plncase, jv, kw.reason_upper) == kw.ReasonNum
    assert g_sqlitetype(cfig, plncase, jv, kw.reason_upper) == "REAL"
    assert g_popcashout(cfig, plncase, jv, kw.reason_upper) == False

    assert g_class_type(cfig, plncase, jv, kw.reason_lower) == kw.ReasonNum
    assert g_sqlitetype(cfig, plncase, jv, kw.reason_lower) == "REAL"
    assert g_popcashout(cfig, plncase, jv, kw.reason_lower) == False

    assert g_class_type(cfig, plnreas, jk, kw.reason_context) == kw.RopeTerm
    assert g_sqlitetype(cfig, plnreas, jk, kw.reason_context) == "TEXT"
    assert g_popcashout(cfig, plnreas, jk, kw.reason_context) == False

    assert g_class_type(cfig, plnreas, jk, kw.keg_rope) == kw.RopeTerm
    assert g_sqlitetype(cfig, plnreas, jk, kw.keg_rope) == "TEXT"
    assert g_popcashout(cfig, plnreas, jk, kw.keg_rope) == False

    assert g_class_type(cfig, plnreas, jv, kw.parent_heir_active) == "int"
    assert g_sqlitetype(cfig, plnreas, jv, kw.parent_heir_active) == "INTEGER"
    assert g_popcashout(cfig, plnreas, jv, kw.parent_heir_active) == True

    assert g_class_type(cfig, plnreas, jv, kw.reason_active) == "int"
    assert g_sqlitetype(cfig, plnreas, jv, kw.reason_active) == "INTEGER"
    assert g_popcashout(cfig, plnreas, jv, kw.reason_active) == True

    assert g_class_type(cfig, plnreas, jv, kw.task) == "int"
    assert g_sqlitetype(cfig, plnreas, jv, kw.task) == "INTEGER"
    assert g_popcashout(cfig, plnreas, jv, kw.task) == True

    assert g_class_type(cfig, plnreas, jv, kw.active_requisite) == "bool"
    assert g_sqlitetype(cfig, plnreas, jv, kw.active_requisite) == "INTEGER"
    assert g_popcashout(cfig, plnreas, jv, kw.active_requisite) == False

    assert g_class_type(cfig, plnlabo, jk, kw.keg_rope) == kw.RopeTerm
    assert g_sqlitetype(cfig, plnlabo, jk, kw.keg_rope) == "TEXT"
    assert g_popcashout(cfig, plnlabo, jk, kw.keg_rope) == False

    assert g_class_type(cfig, plnlabo, jk, kw.party_title) == kw.TitleTerm
    assert g_sqlitetype(cfig, plnlabo, jk, kw.party_title) == "TEXT"
    assert g_popcashout(cfig, plnlabo, jk, kw.party_title) == False

    assert g_class_type(cfig, plnlabo, jv, kw.plan_name_is_labor) == "int"
    assert g_sqlitetype(cfig, plnlabo, jv, kw.plan_name_is_labor) == "INTEGER"
    assert g_popcashout(cfig, plnlabo, jv, kw.plan_name_is_labor) == True

    assert g_class_type(cfig, plnkegg, jv, kw.keg_active) == "int"
    assert g_sqlitetype(cfig, plnkegg, jv, kw.keg_active) == "INTEGER"
    assert g_popcashout(cfig, plnkegg, jv, kw.keg_active) == True

    assert g_class_type(cfig, plnkegg, jv, kw.all_partner_cred) == "int"
    assert g_sqlitetype(cfig, plnkegg, jv, kw.all_partner_cred) == "INTEGER"
    assert g_popcashout(cfig, plnkegg, jv, kw.all_partner_cred) == True

    assert g_class_type(cfig, plnkegg, jv, kw.all_partner_debt) == "int"
    assert g_sqlitetype(cfig, plnkegg, jv, kw.all_partner_debt) == "INTEGER"
    assert g_popcashout(cfig, plnkegg, jv, kw.all_partner_debt) == True

    assert g_class_type(cfig, plnkegg, jv, kw.descendant_pledge_count) == "int"
    assert g_sqlitetype(cfig, plnkegg, jv, kw.descendant_pledge_count) == "INTEGER"
    assert g_popcashout(cfig, plnkegg, jv, kw.descendant_pledge_count) == True

    assert g_class_type(cfig, plnkegg, jv, kw.fund_cease) == "float"
    assert g_sqlitetype(cfig, plnkegg, jv, kw.fund_cease) == "REAL"
    assert g_popcashout(cfig, plnkegg, jv, kw.fund_cease) == True

    assert g_class_type(cfig, plnkegg, jv, kw.fund_grain) == "float"
    assert g_sqlitetype(cfig, plnkegg, jv, kw.fund_grain) == "REAL"
    assert g_popcashout(cfig, plnkegg, jv, kw.fund_grain) == True

    assert g_class_type(cfig, plnkegg, jv, kw.fund_onset) == "float"
    assert g_sqlitetype(cfig, plnkegg, jv, kw.fund_onset) == "REAL"
    assert g_popcashout(cfig, plnkegg, jv, kw.fund_onset) == True

    assert g_class_type(cfig, plnkegg, jv, kw.fund_ratio) == "float"
    assert g_sqlitetype(cfig, plnkegg, jv, kw.fund_ratio) == "REAL"
    assert g_popcashout(cfig, plnkegg, jv, kw.fund_ratio) == True

    assert g_class_type(cfig, plnkegg, jv, kw.gogo_calc) == "float"
    assert g_sqlitetype(cfig, plnkegg, jv, kw.gogo_calc) == "REAL"
    assert g_popcashout(cfig, plnkegg, jv, kw.gogo_calc) == True

    assert g_class_type(cfig, plnkegg, jv, kw.healerunit_ratio) == "float"
    assert g_sqlitetype(cfig, plnkegg, jv, kw.healerunit_ratio) == "REAL"
    assert g_popcashout(cfig, plnkegg, jv, kw.healerunit_ratio) == True

    assert g_class_type(cfig, plnkegg, jv, kw.tree_level) == "int"
    assert g_sqlitetype(cfig, plnkegg, jv, kw.tree_level) == "INTEGER"
    assert g_popcashout(cfig, plnkegg, jv, kw.tree_level) == True

    assert g_class_type(cfig, plnkegg, jv, kw.range_evaluated) == "int"
    assert g_sqlitetype(cfig, plnkegg, jv, kw.range_evaluated) == "INTEGER"
    assert g_popcashout(cfig, plnkegg, jv, kw.range_evaluated) == True

    assert g_class_type(cfig, plnkegg, jv, kw.stop_calc) == "float"
    assert g_sqlitetype(cfig, plnkegg, jv, kw.stop_calc) == "REAL"
    assert g_popcashout(cfig, plnkegg, jv, kw.stop_calc) == True

    assert g_class_type(cfig, plnkegg, jv, kw.task) == "int"
    assert g_sqlitetype(cfig, plnkegg, jv, kw.task) == "INTEGER"
    assert g_popcashout(cfig, plnkegg, jv, kw.task) == True

    assert g_class_type(cfig, plnkegg, jv, kw.addin) == "float"
    assert g_sqlitetype(cfig, plnkegg, jv, kw.addin) == "REAL"
    assert g_popcashout(cfig, plnkegg, jv, kw.addin) == False

    assert g_class_type(cfig, plnkegg, jv, kw.begin) == "float"
    assert g_sqlitetype(cfig, plnkegg, jv, kw.begin) == "REAL"
    assert g_popcashout(cfig, plnkegg, jv, kw.begin) == False

    assert g_class_type(cfig, plnkegg, jv, kw.close) == "float"
    assert g_sqlitetype(cfig, plnkegg, jv, kw.close) == "REAL"
    assert g_popcashout(cfig, plnkegg, jv, kw.close) == False

    assert g_class_type(cfig, plnkegg, jv, kw.denom) == "int"
    assert g_sqlitetype(cfig, plnkegg, jv, kw.denom) == "INTEGER"
    assert g_popcashout(cfig, plnkegg, jv, kw.denom) == False

    assert g_class_type(cfig, plnkegg, jv, kw.gogo_want) == "float"
    assert g_sqlitetype(cfig, plnkegg, jv, kw.gogo_want) == "REAL"
    assert g_popcashout(cfig, plnkegg, jv, kw.gogo_want) == False

    assert g_class_type(cfig, plnkegg, jv, kw.star) == "int"
    assert g_sqlitetype(cfig, plnkegg, jv, kw.star) == "INTEGER"
    assert g_popcashout(cfig, plnkegg, jv, kw.star) == False

    assert g_class_type(cfig, plnkegg, jv, kw.morph) == "bool"
    assert g_sqlitetype(cfig, plnkegg, jv, kw.morph) == "INTEGER"
    assert g_popcashout(cfig, plnkegg, jv, kw.morph) == False

    assert g_class_type(cfig, plnkegg, jv, kw.numor) == "int"
    assert g_sqlitetype(cfig, plnkegg, jv, kw.numor) == "INTEGER"
    assert g_popcashout(cfig, plnkegg, jv, kw.numor) == False

    assert g_class_type(cfig, plnkegg, jv, kw.pledge) == "bool"
    assert g_sqlitetype(cfig, plnkegg, jv, kw.pledge) == "INTEGER"
    assert g_popcashout(cfig, plnkegg, jv, kw.pledge) == False

    assert g_class_type(cfig, plnkegg, jv, kw.problem_bool) == "bool"
    assert g_sqlitetype(cfig, plnkegg, jv, kw.problem_bool) == "INTEGER"
    assert g_popcashout(cfig, plnkegg, jv, kw.problem_bool) == False

    assert g_class_type(cfig, plnkegg, jv, kw.stop_want) == "float"
    assert g_sqlitetype(cfig, plnkegg, jv, kw.stop_want) == "REAL"
    assert g_popcashout(cfig, plnkegg, jv, kw.stop_want) == False

    assert g_class_type(cfig, plnunit, jv, "keeps_buildable") == "int"
    assert g_sqlitetype(cfig, plnunit, jv, "keeps_buildable") == "INTEGER"
    assert g_popcashout(cfig, plnunit, jv, "keeps_buildable") == True

    assert g_class_type(cfig, plnunit, jv, "keeps_justified") == "int"
    assert g_sqlitetype(cfig, plnunit, jv, "keeps_justified") == "INTEGER"
    assert g_popcashout(cfig, plnunit, jv, "keeps_justified") == True

    assert g_class_type(cfig, plnunit, jv, kw.offtrack_fund) == "float"
    assert g_sqlitetype(cfig, plnunit, jv, kw.offtrack_fund) == "REAL"
    assert g_popcashout(cfig, plnunit, jv, kw.offtrack_fund) == True

    assert g_class_type(cfig, plnunit, jv, kw.rational) == "bool"
    assert g_sqlitetype(cfig, plnunit, jv, kw.rational) == "INTEGER"
    assert g_popcashout(cfig, plnunit, jv, kw.rational) == True

    assert g_class_type(cfig, plnunit, jv, kw.sum_healerunit_kegs_fund_total) == "float"
    assert g_sqlitetype(cfig, plnunit, jv, kw.sum_healerunit_kegs_fund_total) == "REAL"
    assert g_popcashout(cfig, plnunit, jv, kw.sum_healerunit_kegs_fund_total) == True

    assert g_class_type(cfig, plnunit, jv, kw.tree_traverse_count) == "int"
    assert g_sqlitetype(cfig, plnunit, jv, kw.tree_traverse_count) == "INTEGER"
    assert g_popcashout(cfig, plnunit, jv, kw.tree_traverse_count) == True

    assert g_class_type(cfig, plnunit, jv, kw.credor_respect) == "float"
    assert g_sqlitetype(cfig, plnunit, jv, kw.credor_respect) == "REAL"
    assert g_popcashout(cfig, plnunit, jv, kw.credor_respect) == False

    assert g_class_type(cfig, plnunit, jv, kw.debtor_respect) == "float"
    assert g_sqlitetype(cfig, plnunit, jv, kw.debtor_respect) == "REAL"
    assert g_popcashout(cfig, plnunit, jv, kw.debtor_respect) == False

    assert g_class_type(cfig, plnunit, jv, kw.fund_grain) == "float"
    assert g_sqlitetype(cfig, plnunit, jv, kw.fund_grain) == "REAL"
    assert g_popcashout(cfig, plnunit, jv, kw.fund_grain) == False

    assert g_class_type(cfig, plnunit, jv, kw.fund_pool) == "float"
    assert g_sqlitetype(cfig, plnunit, jv, kw.fund_pool) == "REAL"
    assert g_popcashout(cfig, plnunit, jv, kw.fund_pool) == False

    assert g_class_type(cfig, plnunit, jv, kw.max_tree_traverse) == "int"
    assert g_sqlitetype(cfig, plnunit, jv, kw.max_tree_traverse) == "INTEGER"
    assert g_popcashout(cfig, plnunit, jv, kw.max_tree_traverse) == False

    assert g_class_type(cfig, plnunit, jv, kw.mana_grain) == "float"
    assert g_sqlitetype(cfig, plnunit, jv, kw.mana_grain) == "REAL"
    assert g_popcashout(cfig, plnunit, jv, kw.mana_grain) == False

    assert g_class_type(cfig, plnunit, jv, kw.respect_grain) == "float"
    assert g_sqlitetype(cfig, plnunit, jv, kw.respect_grain) == "REAL"
    assert g_popcashout(cfig, plnunit, jv, kw.respect_grain) == False


def test_get_plan_config_dict_ReturnsObj_EachArgHasOneClassType():
    # ESTABLISH
    plan_config_dict = get_plan_config_dict()
    all_args = {}
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for plan_calc_dimen, dimen_dict in plan_config_dict.items():
        for dimen_key, args_dict in dimen_dict.items():
            if dimen_key in {kw.jkeys, kw.jvalues}:
                for x_arg, arg_dict in args_dict.items():
                    arg_type = arg_dict.get(kw.class_type)
                    if all_args.get(x_arg) is None:
                        all_args[x_arg] = set()
                    all_args.get(x_arg).add(arg_type)

    # WHEN / THEN
    for x_arg, arg_types in all_args.items():
        # print(f"{x_arg=} {arg_types=}")
        assertion_failure_str = f"{x_arg=} {arg_types=}"
        assert len(arg_types) == 1, assertion_failure_str


def test_get_plan_config_dict_ReturnsObj_EachArgHasOne_sqlite_datatype():
    # ESTABLISH
    plan_config_dict = get_plan_config_dict()
    all_args = {}
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for plan_calc_dimen, dimen_dict in plan_config_dict.items():
        for dimen_key, args_dict in dimen_dict.items():
            if dimen_key in {kw.jkeys, kw.jvalues}:
                for x_arg, arg_dict in args_dict.items():
                    arg_type = arg_dict.get(kw.sqlite_datatype)
                    if all_args.get(x_arg) is None:
                        all_args[x_arg] = set()
                    all_args.get(x_arg).add(arg_type)

    for x_arg, arg_types in all_args.items():
        # print(f"{x_arg=} {arg_types=}")
        assertion_failure_str = f"{x_arg=} {arg_types=}"
        assert len(arg_types) == 1, assertion_failure_str

    # WHEN
    sqlite_datatype_dict = get_plan_calc_args_sqlite_datatype_dict()

    # THEN
    for x_arg, arg_types in all_args.items():
        # print(
        #     f"""assert plan_calc_args_type_dict.get("{x_arg}") == "{list(arg_types)[0]}" """
        # )
        # print(f""""{x_arg}": "{list(arg_types)[0]}",""")
        assert_failure_str = f""""{x_arg}": "{list(arg_types)[0]}","""
        assert list(arg_types)[0] == sqlite_datatype_dict.get(x_arg), assert_failure_str


def test_get_plan_calc_args_type_dict_ReturnsObj():
    # ESTABLISH
    plan_config_dict = get_plan_config_dict()
    all_args = {}
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for plan_calc_dimen, dimen_dict in plan_config_dict.items():
        for dimen_key, args_dict in dimen_dict.items():
            if dimen_key in {kw.jkeys, kw.jvalues}:
                for x_arg, arg_dict in args_dict.items():
                    arg_type = arg_dict.get(kw.class_type)
                    if all_args.get(x_arg) is None:
                        all_args[x_arg] = set()
                    all_args.get(x_arg).add(arg_type)

    # WHEN
    plan_calc_args_type_dict = get_plan_calc_args_type_dict()

    # THEN
    assert plan_calc_args_type_dict.get(kw.partner_name) == kw.NameTerm
    assert plan_calc_args_type_dict.get(kw.group_title) == kw.TitleTerm
    assert plan_calc_args_type_dict.get(kw.case_active) == "int"
    assert plan_calc_args_type_dict.get(kw.credor_pool) == "float"
    assert plan_calc_args_type_dict.get(kw.debtor_pool) == "float"
    assert plan_calc_args_type_dict.get(kw.fund_agenda_give) == "float"
    assert plan_calc_args_type_dict.get(kw.fund_agenda_ratio_give) == "float"
    assert plan_calc_args_type_dict.get(kw.fund_agenda_ratio_take) == "float"
    assert plan_calc_args_type_dict.get(kw.fund_agenda_take) == "float"
    assert plan_calc_args_type_dict.get(kw.fund_give) == "float"
    assert plan_calc_args_type_dict.get(kw.fund_take) == "float"
    assert plan_calc_args_type_dict.get(kw.group_cred_lumen) == "int"
    assert plan_calc_args_type_dict.get(kw.group_debt_lumen) == "int"
    assert plan_calc_args_type_dict.get(kw.inallocable_partner_debt_lumen) == "float"
    assert plan_calc_args_type_dict.get(kw.irrational_partner_debt_lumen) == "float"
    assert plan_calc_args_type_dict.get(kw.partner_cred_lumen) == "float"
    assert plan_calc_args_type_dict.get(kw.partner_debt_lumen) == "float"
    assert plan_calc_args_type_dict.get(kw.addin) == "float"
    assert plan_calc_args_type_dict.get(kw.begin) == "float"
    assert plan_calc_args_type_dict.get(kw.close) == "float"
    assert plan_calc_args_type_dict.get(kw.denom) == "int"
    assert plan_calc_args_type_dict.get(kw.gogo_want) == "float"
    assert plan_calc_args_type_dict.get(kw.star) == "int"
    assert plan_calc_args_type_dict.get(kw.morph) == "bool"
    assert plan_calc_args_type_dict.get(kw.numor) == "int"
    assert plan_calc_args_type_dict.get(kw.pledge) == "bool"
    assert plan_calc_args_type_dict.get(kw.problem_bool) == "bool"
    assert plan_calc_args_type_dict.get(kw.stop_want) == "float"
    assert plan_calc_args_type_dict.get(kw.awardee_title) == kw.TitleTerm
    assert plan_calc_args_type_dict.get(kw.keg_rope) == kw.RopeTerm
    assert plan_calc_args_type_dict.get(kw.give_force) == "float"
    assert plan_calc_args_type_dict.get(kw.take_force) == "float"
    assert plan_calc_args_type_dict.get(kw.reason_context) == kw.RopeTerm
    assert plan_calc_args_type_dict.get(kw.fact_upper) == kw.FactNum
    assert plan_calc_args_type_dict.get(kw.fact_lower) == kw.FactNum
    assert plan_calc_args_type_dict.get(kw.fact_state) == kw.RopeTerm
    assert plan_calc_args_type_dict.get(kw.healer_name) == kw.NameTerm
    assert plan_calc_args_type_dict.get(kw.reason_state) == kw.RopeTerm
    assert plan_calc_args_type_dict.get(kw.reason_active) == "int"
    assert plan_calc_args_type_dict.get(kw.task) == "int"
    assert plan_calc_args_type_dict.get(kw.reason_divisor) == "int"
    assert plan_calc_args_type_dict.get(kw.reason_upper) == kw.ReasonNum
    assert plan_calc_args_type_dict.get(kw.reason_lower) == kw.ReasonNum
    assert plan_calc_args_type_dict.get(kw.parent_heir_active) == "int"
    assert plan_calc_args_type_dict.get(kw.active_requisite) == "bool"
    assert plan_calc_args_type_dict.get(kw.party_title) == kw.TitleTerm
    assert plan_calc_args_type_dict.get(kw.plan_name_is_labor) == "int"
    assert plan_calc_args_type_dict.get(kw.keg_active) == "int"
    assert plan_calc_args_type_dict.get(kw.all_partner_cred) == "int"
    assert plan_calc_args_type_dict.get(kw.all_partner_debt) == "int"
    assert plan_calc_args_type_dict.get(kw.descendant_pledge_count) == "int"
    assert plan_calc_args_type_dict.get(kw.fund_cease) == "float"
    assert plan_calc_args_type_dict.get(kw.fund_onset) == "float"
    assert plan_calc_args_type_dict.get(kw.fund_ratio) == "float"
    assert plan_calc_args_type_dict.get(kw.gogo_calc) == "float"
    assert plan_calc_args_type_dict.get(kw.healerunit_ratio) == "float"
    assert plan_calc_args_type_dict.get(kw.tree_level) == "int"
    assert plan_calc_args_type_dict.get(kw.range_evaluated) == "int"
    assert plan_calc_args_type_dict.get(kw.stop_calc) == "float"
    assert plan_calc_args_type_dict.get(kw.keeps_buildable) == "int"
    assert plan_calc_args_type_dict.get(kw.keeps_justified) == "int"
    assert plan_calc_args_type_dict.get(kw.offtrack_fund) == "int"
    assert plan_calc_args_type_dict.get(kw.rational) == "bool"
    assert plan_calc_args_type_dict.get(kw.sum_healerunit_kegs_fund_total) == "float"
    assert plan_calc_args_type_dict.get(kw.tree_traverse_count) == "int"
    assert plan_calc_args_type_dict.get(kw.credor_respect) == "float"
    assert plan_calc_args_type_dict.get(kw.debtor_respect) == "float"
    assert plan_calc_args_type_dict.get(kw.fund_grain) == "float"
    assert plan_calc_args_type_dict.get(kw.fund_pool) == "float"
    assert plan_calc_args_type_dict.get(kw.max_tree_traverse) == "int"
    assert plan_calc_args_type_dict.get(kw.mana_grain) == "float"
    assert plan_calc_args_type_dict.get(kw.respect_grain) == "float"
    assert len(plan_calc_args_type_dict) == 72
