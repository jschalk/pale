from src.ch04_rope.rope import default_knot_if_None
from src.ch08_belief_atom.atom_config import (
    get_all_belief_dimen_delete_keys,
    get_atom_args_class_types,
)
from src.ch15_moment.moment_config import get_moment_args_class_types
from src.ch16_rose.map import (
    epochmap_shop,
    labelmap_shop,
    namemap_shop,
    ropemap_shop,
    titlemap_shop,
)
from src.ch16_rose.rose_config import (
    default_unknown_str_if_None,
    find_set_otx_inx_args,
    get_rose_args_class_types,
    get_rose_epochtime_args,
    get_rose_labelterm_args,
    get_rose_nameterm_args,
    get_rose_ropeterm_args,
    get_rose_titleterm_args,
    get_roseable_args,
    get_roseable_number_class_types,
    get_roseable_term_class_types,
    roseable_class_types,
)
from src.ch16_rose.rose_term import RoseUnit, roseunit_shop
from src.ref.keywords import Ch16Keywords as kw, ExampleStrs as exx


def test_get_rose_args_class_types_ReturnsObj():
    # ESTABLISH / WHEN
    rose_args_class_types = get_rose_args_class_types()

    # THEN
    assert rose_args_class_types.get(kw.voice_name) == kw.NameTerm
    assert rose_args_class_types.get(kw.addin) == "float"
    assert rose_args_class_types.get(kw.amount) == "float"
    assert rose_args_class_types.get(kw.awardee_title) == kw.TitleTerm
    assert rose_args_class_types.get(kw.reason_context) == kw.RopeTerm
    assert rose_args_class_types.get(kw.active_requisite) == "bool"
    assert rose_args_class_types.get(kw.begin) == "float"
    assert rose_args_class_types.get(kw.c400_number) == "int"
    assert rose_args_class_types.get(kw.close) == "float"
    assert rose_args_class_types.get(kw.voice_cred_lumen) == "float"
    assert rose_args_class_types.get(kw.group_cred_lumen) == "float"
    assert rose_args_class_types.get(kw.credor_respect) == "float"
    assert rose_args_class_types.get(kw.cumulative_day) == "int"
    assert rose_args_class_types.get(kw.cumulative_minute) == "int"
    assert rose_args_class_types.get(kw.voice_debt_lumen) == "float"
    assert rose_args_class_types.get(kw.group_debt_lumen) == "float"
    assert rose_args_class_types.get(kw.debtor_respect) == "float"
    assert rose_args_class_types.get(kw.denom) == "int"
    assert rose_args_class_types.get(kw.reason_divisor) == "int"
    assert rose_args_class_types.get(kw.face_name) == kw.NameTerm
    assert rose_args_class_types.get(kw.fact_context) == kw.RopeTerm
    assert rose_args_class_types.get(kw.moment_label) == kw.LabelTerm
    assert rose_args_class_types.get(kw.fact_upper) == kw.ContextNum
    assert rose_args_class_types.get(kw.fact_lower) == kw.ContextNum
    assert rose_args_class_types.get(kw.fund_grain) == "float"
    assert rose_args_class_types.get(kw.fund_pool) == "float"
    assert rose_args_class_types.get(kw.give_force) == "float"
    assert rose_args_class_types.get(kw.gogo_want) == "float"
    assert rose_args_class_types.get(kw.group_title) == kw.TitleTerm
    assert rose_args_class_types.get(kw.healer_name) == kw.NameTerm
    assert rose_args_class_types.get(kw.hour_label) == kw.LabelTerm
    assert rose_args_class_types.get(kw.star) == "int"
    assert rose_args_class_types.get(kw.max_tree_traverse) == "int"
    assert rose_args_class_types.get(kw.month_label) == kw.LabelTerm
    assert rose_args_class_types.get(kw.monthday_index) == "int"
    assert rose_args_class_types.get(kw.morph) == "bool"
    assert rose_args_class_types.get(kw.reason_state) == kw.RopeTerm
    assert rose_args_class_types.get(kw.reason_upper) == kw.ContextNum
    assert rose_args_class_types.get(kw.numor) == "int"
    assert rose_args_class_types.get(kw.offi_time) == kw.EpochTime
    assert rose_args_class_types.get(kw.belief_name) == kw.NameTerm
    assert rose_args_class_types.get(kw.reason_lower) == kw.ContextNum
    assert rose_args_class_types.get(kw.mana_grain) == "float"
    assert rose_args_class_types.get(kw.fact_state) == kw.RopeTerm
    assert rose_args_class_types.get(kw.pledge) == "bool"
    assert rose_args_class_types.get(kw.problem_bool) == "bool"
    assert rose_args_class_types.get(kw.quota) == "int"
    assert rose_args_class_types.get(kw.respect_grain) == "float"
    assert rose_args_class_types.get(kw.plan_rope) == kw.RopeTerm
    assert rose_args_class_types.get(kw.celldepth) == "int"
    assert rose_args_class_types.get(kw.stop_want) == "float"
    assert rose_args_class_types.get(kw.take_force) == "float"
    assert rose_args_class_types.get(kw.tally) == "int"
    assert rose_args_class_types.get(kw.party_title) == kw.TitleTerm
    assert rose_args_class_types.get(kw.bud_time) == kw.EpochTime
    assert rose_args_class_types.get(kw.tran_time) == kw.EpochTime
    assert rose_args_class_types.get(kw.epoch_label) == kw.LabelTerm
    assert rose_args_class_types.get(kw.weekday_label) == kw.LabelTerm
    assert rose_args_class_types.get(kw.weekday_order) == "int"
    assert rose_args_class_types.get(kw.knot) == "str"
    assert rose_args_class_types.get(kw.yr1_jan1_offset) == "int"
    assert rose_args_class_types.get(kw.solo) == "int"

    # make sure it rose_arg_class_types has all moment and all atom args
    rose_args = set(rose_args_class_types.keys())
    atom_args = set(get_atom_args_class_types().keys())
    moment_args = set(get_moment_args_class_types().keys())
    assert atom_args.issubset(rose_args)
    assert moment_args.issubset(rose_args)
    assert atom_args & (moment_args) == {
        kw.voice_name,
        kw.fund_grain,
        kw.mana_grain,
        kw.respect_grain,
    }
    assert atom_args.union(moment_args) != rose_args
    assert atom_args.union(moment_args).union({kw.face_name}) == rose_args
    assert check_class_types_are_correct()
    # assert rose_args_class_types.keys() == get_atom_args_dimen_mapping().keys()
    # assert all_atom_args_class_types_are_correct(x_class_types)


def check_class_types_are_correct() -> bool:
    rose_args_class_types = get_rose_args_class_types()
    atom_args_class_types = get_atom_args_class_types()
    moment_args_class_types = get_moment_args_class_types()
    for rose_arg, rose_type in rose_args_class_types.items():
        print(f"check {rose_arg=} {rose_type=}")
        if atom_args_class_types.get(rose_arg) not in [None, rose_type]:
            print(f"{rose_arg=} {rose_type=} {atom_args_class_types.get(rose_arg)=}")
            return False
        if moment_args_class_types.get(rose_arg) not in [None, rose_type]:
            print(f"{rose_arg=} {rose_type=} {moment_args_class_types.get(rose_arg)=}")
            return False
    return True


def test_roseable_class_types_ReturnsObj():
    # ESTABLISH / WHEN
    x_roseable_class_types = roseable_class_types()

    # THEN
    assert len(x_roseable_class_types) == 5
    assert x_roseable_class_types == {
        kw.EpochTime,
        kw.NameTerm,
        kw.TitleTerm,
        kw.LabelTerm,
        kw.RopeTerm,
    }
    print(f"{set(get_atom_args_class_types().values())=}")
    all_atom_class_types = set(get_atom_args_class_types().values())
    all_atom_class_types.add(kw.LabelTerm)
    all_atom_class_types.add(kw.EpochTime)
    x_cL_tyep = set(all_atom_class_types) & (x_roseable_class_types)
    assert x_cL_tyep == x_roseable_class_types


def test_get_roseable_number_class_types_ReturnsObj():
    # ESTABLISH / WHEN
    x_number_class_types = get_roseable_number_class_types()

    # THEN
    assert len(x_number_class_types) == 1
    assert x_number_class_types == {kw.EpochTime}
    assert x_number_class_types.issubset(roseable_class_types())


def test_get_roseable_term_class_types_ReturnsObj():
    # ESTABLISH / WHEN
    x_term_class_types = get_roseable_term_class_types()

    # THEN
    assert len(x_term_class_types) == 4
    assert x_term_class_types == {
        kw.NameTerm,
        kw.TitleTerm,
        kw.LabelTerm,
        kw.RopeTerm,
    }
    assert x_term_class_types.issubset(roseable_class_types())
    assert x_term_class_types.isdisjoint(get_roseable_number_class_types())
    number_class_types = get_roseable_number_class_types()
    assert x_term_class_types.intersection(number_class_types) == set()


def test_get_roseable_args_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    print(f"{roseable_class_types()=}")
    all_rose_args = set(get_rose_args_class_types().keys())
    print(f"{get_roseable_args().difference(all_rose_args)}")
    assert get_roseable_args().issubset(all_rose_args)
    static_get_roseable_args = {
        x_arg
        for x_arg, class_type in get_rose_args_class_types().items()
        if class_type in roseable_class_types()
    }
    assert get_roseable_args() == static_get_roseable_args

    assert len(get_roseable_args()) == 20
    assert get_roseable_args() == {
        kw.awardee_title,
        kw.belief_name,
        kw.bud_time,
        kw.epoch_label,
        kw.face_name,
        kw.fact_context,
        kw.fact_state,
        kw.group_title,
        kw.healer_name,
        kw.hour_label,
        kw.moment_label,
        kw.month_label,
        kw.offi_time,
        kw.plan_rope,
        kw.party_title,
        kw.reason_context,
        kw.reason_state,
        kw.tran_time,
        kw.voice_name,
        kw.weekday_label,
    }


def test_find_set_otx_inx_args_ReturnsObj_Scenario0_All_roseable_args():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    roseable_args = get_roseable_args()

    # WHEN
    otx_inx_args = find_set_otx_inx_args(roseable_args)

    # THEN
    expected_otx_inx_args = set()
    for roseable_arg in roseable_args:
        expected_otx_inx_args.add(f"{roseable_arg}_otx")
        expected_otx_inx_args.add(f"{roseable_arg}_inx")
    print(f"{otx_inx_args=}")
    assert otx_inx_args == expected_otx_inx_args


def test_find_set_otx_inx_args_ReturnsObj_Scenario1_belief_dimen_delete_keys():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    belief_dimen_delete_keys = get_all_belief_dimen_delete_keys()

    # WHEN
    otx_inx_args = find_set_otx_inx_args(belief_dimen_delete_keys)

    # THEN
    expected_otx_inx_args = set()
    for roseable_arg in belief_dimen_delete_keys:
        expected_otx_inx_args.add(f"{roseable_arg}_otx")
        expected_otx_inx_args.add(f"{roseable_arg}_inx")
    print(f"{otx_inx_args=}")
    assert otx_inx_args == expected_otx_inx_args


def test_find_set_otx_inx_args_ReturnsObj_Scenario2_OtherArgsAreUntouched():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    run_str = "run"
    given_belief_dimen_delete_keys = get_all_belief_dimen_delete_keys()
    given_belief_dimen_delete_keys.add(run_str)

    # WHEN
    otx_inx_args = find_set_otx_inx_args(given_belief_dimen_delete_keys)

    # THEN
    expected_otx_inx_args = set()
    for roseable_arg in get_all_belief_dimen_delete_keys():
        expected_otx_inx_args.add(f"{roseable_arg}_otx")
        expected_otx_inx_args.add(f"{roseable_arg}_inx")
    expected_otx_inx_args.add(run_str)
    print(f"{otx_inx_args=}")
    assert otx_inx_args == expected_otx_inx_args


def test_find_set_otx_inx_args_ReturnsObj_Scenario3_PartialSets():
    # ESTABLISH
    healer_name_ERASE_str = f"{kw.healer_name}_ERASE"
    run_str = "run"
    given_belief_dimen_delete_keys = {run_str, healer_name_ERASE_str}

    # WHEN
    otx_inx_args = find_set_otx_inx_args(given_belief_dimen_delete_keys)

    # THEN
    healer_name_ERASE_str = f"{kw.healer_name}_ERASE"
    expected_otx_inx_args = {
        f"{healer_name_ERASE_str}_otx",
        f"{healer_name_ERASE_str}_inx",
        run_str,
    }
    print(f"{otx_inx_args=}")
    assert otx_inx_args == expected_otx_inx_args


def test_get_rose_nameterm_args_ReturnsObj():
    # ESTABLISH / WHEN
    rose_NameTerm_args = get_rose_nameterm_args()

    # THEN
    assert rose_NameTerm_args == {
        kw.voice_name,
        kw.face_name,
        kw.healer_name,
        kw.belief_name,
    }
    expected_args = {
        x_arg
        for x_arg, class_type in get_rose_args_class_types().items()
        if class_type == kw.NameTerm
    }
    assert rose_NameTerm_args == expected_args


def test_get_rose_titleterm_args_ReturnsObj():
    # ESTABLISH / WHEN
    rose_TitleTerm_args = get_rose_titleterm_args()

    # THEN
    assert rose_TitleTerm_args == {
        kw.awardee_title,
        kw.group_title,
        kw.party_title,
    }
    expected_args = {
        x_arg
        for x_arg, class_type in get_rose_args_class_types().items()
        if class_type == kw.TitleTerm
    }
    assert rose_TitleTerm_args == expected_args


def test_get_rose_labelterm_args_ReturnsObj():
    # ESTABLISH / WHEN
    rose_LabelTerm_args = get_rose_labelterm_args()

    # THEN
    assert rose_LabelTerm_args == {
        kw.moment_label,
        kw.hour_label,
        kw.month_label,
        kw.epoch_label,
        kw.weekday_label,
    }
    expected_args = {
        x_arg
        for x_arg, class_type in get_rose_args_class_types().items()
        if class_type == kw.LabelTerm
    }
    assert rose_LabelTerm_args == expected_args


def test_get_rose_ropeterm_args_ReturnsObj():
    # ESTABLISH / WHEN
    rose_RopeTerm_args = get_rose_ropeterm_args()

    # THEN
    assert rose_RopeTerm_args == {
        kw.fact_state,
        kw.fact_context,
        kw.plan_rope,
        kw.reason_context,
        kw.reason_state,
    }
    expected_args = {
        x_arg
        for x_arg, class_type in get_rose_args_class_types().items()
        if class_type == kw.RopeTerm
    }
    assert rose_RopeTerm_args == expected_args


def test_get_rose_epochtime_args_ReturnsObj():
    # ESTABLISH / WHEN
    rose_EpochTime_args = get_rose_epochtime_args()

    # THEN
    assert rose_EpochTime_args == {kw.bud_time, kw.offi_time, kw.tran_time}
    expected_args = {
        x_arg
        for x_arg, class_type in get_rose_args_class_types().items()
        if class_type == kw.EpochTime
    }
    assert rose_EpochTime_args == expected_args


def test_RoseUnit_Exists():
    # ESTABLISH
    x_roseunit = RoseUnit()

    # WHEN / THEN
    assert not x_roseunit.face_name
    assert not x_roseunit.spark_num
    assert not x_roseunit.titlemap
    assert not x_roseunit.namemap
    assert not x_roseunit.labelmap
    assert not x_roseunit.ropemap
    assert not x_roseunit.epochmap
    assert not x_roseunit.unknown_str
    assert not x_roseunit.otx_knot
    assert not x_roseunit.inx_knot
    assert set(x_roseunit.__dict__.keys()) == {
        kw.face_name,
        kw.spark_num,
        kw.titlemap,
        kw.namemap,
        kw.labelmap,
        kw.ropemap,
        kw.epochmap,
        kw.unknown_str,
        kw.otx_knot,
        kw.inx_knot,
    }


def test_roseunit_shop_ReturnsObj_Scenario0():
    # ESTABLISH

    # WHEN
    sue_roseunit = roseunit_shop(exx.sue)

    # THEN
    assert sue_roseunit.face_name == exx.sue
    assert sue_roseunit.spark_num == 0
    assert sue_roseunit.unknown_str == default_unknown_str_if_None()
    assert sue_roseunit.otx_knot == default_knot_if_None()
    assert sue_roseunit.inx_knot == default_knot_if_None()
    assert sue_roseunit.titlemap == titlemap_shop(face_name=exx.sue)
    assert sue_roseunit.namemap == namemap_shop(face_name=exx.sue)
    assert sue_roseunit.labelmap == labelmap_shop(face_name=exx.sue)
    assert sue_roseunit.ropemap == ropemap_shop(face_name=exx.sue)
    assert sue_roseunit.epochmap == epochmap_shop(exx.sue)
    assert sue_roseunit.namemap.spark_num == 0
    assert sue_roseunit.namemap.unknown_str == default_unknown_str_if_None()
    assert sue_roseunit.namemap.otx_knot == default_knot_if_None()
    assert sue_roseunit.namemap.inx_knot == default_knot_if_None()
    assert sue_roseunit.titlemap.spark_num == 0
    assert sue_roseunit.titlemap.unknown_str == default_unknown_str_if_None()
    assert sue_roseunit.titlemap.otx_knot == default_knot_if_None()
    assert sue_roseunit.titlemap.inx_knot == default_knot_if_None()
    assert sue_roseunit.labelmap.spark_num == 0
    assert sue_roseunit.labelmap.unknown_str == default_unknown_str_if_None()
    assert sue_roseunit.labelmap.otx_knot == default_knot_if_None()
    assert sue_roseunit.labelmap.inx_knot == default_knot_if_None()
    assert sue_roseunit.ropemap.spark_num == 0
    assert sue_roseunit.ropemap.unknown_str == default_unknown_str_if_None()
    assert sue_roseunit.ropemap.otx_knot == default_knot_if_None()
    assert sue_roseunit.ropemap.inx_knot == default_knot_if_None()


def test_roseunit_shop_ReturnsObj_Scenario1():
    # ESTABLISH
    five_spark_num = 5
    y_uk = "UnknownTerm"
    slash_otx_knot = "/"
    colon_inx_knot = ":"
    sue_epoch_length = 600

    # WHEN
    sue_roseunit = roseunit_shop(
        face_name=exx.sue,
        spark_num=five_spark_num,
        otx_knot=slash_otx_knot,
        inx_knot=colon_inx_knot,
        unknown_str=y_uk,
    )

    # THEN
    assert sue_roseunit.spark_num == five_spark_num
    assert sue_roseunit.unknown_str == y_uk
    assert sue_roseunit.otx_knot == slash_otx_knot
    assert sue_roseunit.inx_knot == colon_inx_knot

    # x_titlemap = titlemap_shop(
    #     slash_otx_knot, colon_inx_knot, {}, y_uk, exx.sue, five_spark_num
    # )
    # x_namemap = namemap_shop(
    #     slash_otx_knot, colon_inx_knot, {}, y_uk, exx.sue, five_spark_num
    # )
    # x_ropemap = ropemap_shop(
    #     slash_otx_knot, colon_inx_knot, None, {}, y_uk, exx.sue, five_spark_num
    # )
    # assert sue_roseunit.titlemap == x_titlemap
    # assert sue_roseunit.namemap == x_namemap
    # assert sue_roseunit.ropemap == x_ropemap

    assert sue_roseunit.namemap.face_name == exx.sue
    assert sue_roseunit.namemap.spark_num == five_spark_num
    assert sue_roseunit.namemap.unknown_str == y_uk
    assert sue_roseunit.namemap.otx_knot == slash_otx_knot
    assert sue_roseunit.namemap.inx_knot == colon_inx_knot
    assert sue_roseunit.titlemap.face_name == exx.sue
    assert sue_roseunit.titlemap.spark_num == five_spark_num
    assert sue_roseunit.titlemap.unknown_str == y_uk
    assert sue_roseunit.titlemap.otx_knot == slash_otx_knot
    assert sue_roseunit.titlemap.inx_knot == colon_inx_knot
    assert sue_roseunit.labelmap.face_name == exx.sue
    assert sue_roseunit.labelmap.spark_num == five_spark_num
    assert sue_roseunit.labelmap.unknown_str == y_uk
    assert sue_roseunit.labelmap.otx_knot == slash_otx_knot
    assert sue_roseunit.labelmap.inx_knot == colon_inx_knot
    assert sue_roseunit.ropemap.face_name == exx.sue
    assert sue_roseunit.ropemap.spark_num == five_spark_num
    assert sue_roseunit.ropemap.unknown_str == y_uk
    assert sue_roseunit.ropemap.otx_knot == slash_otx_knot
    assert sue_roseunit.ropemap.inx_knot == colon_inx_knot


def test_roseunit_shop_ReturnsObj_Scenario2_RoseCoreAttrAreDefaultWhenGiven_float_nan():
    # ESTABLISH
    spark7 = 7
    x_nan = float("nan")

    # WHEN
    x_roseunit = roseunit_shop(
        face_name=exx.bob,
        spark_num=spark7,
        unknown_str=x_nan,
        otx_knot=x_nan,
        inx_knot=x_nan,
    )

    # THEN
    assert x_roseunit.face_name == exx.bob
    assert x_roseunit.spark_num == spark7
    assert x_roseunit.unknown_str == default_unknown_str_if_None()
    assert x_roseunit.otx_knot == default_knot_if_None()
    assert x_roseunit.inx_knot == default_knot_if_None()
