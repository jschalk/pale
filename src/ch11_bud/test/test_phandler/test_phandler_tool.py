from os.path import exists as os_path_exists
from pytest import raises as pytest_raises
from src.ch01_py.file_toolbox import create_path, open_json, set_dir
from src.ch04_rope.rope import create_rope
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch07_belief_logic.test._util.ch07_examples import (
    get_beliefunit_irrational_example,
    get_beliefunit_with_4_levels,
)
from src.ch10_belief_listen.keep_tool import (
    job_file_exists,
    open_job_file,
    save_job_file,
)
from src.ch11_bud._ref.ch11_path import (
    create_belief_spark_dir_path,
    create_beliefspark_path,
    create_belieftime_path,
    create_budunit_json_path,
    create_cell_dir_path,
    create_cell_json_path as node_path,
    create_cell_voice_mandate_ledger_path,
)
from src.ch11_bud.bud_filehandler import (
    belieftime_file_exists,
    bud_file_exists,
    cellunit_add_json_file,
    cellunit_get_from_dir,
    cellunit_save_to_dir,
    collect_belief_spark_dir_sets,
    create_cell_voice_mandate_ledger_json,
    get_beliefs_downhill_spark_nums,
    get_beliefspark_obj,
    get_epochtime_dirs,
    open_belief_file,
    open_belieftime_file,
    open_bud_file,
    save_arbitrary_beliefspark,
    save_belief_file,
    save_belieftime_file,
    save_bud_file,
)
from src.ch11_bud.cell_main import CELLNODE_QUOTA_DEFAULT, cellunit_shop
from src.ch11_bud.test._util.ch11_env import get_temp_dir, temp_dir_setup
from src.ch11_bud.test._util.ch11_examples import (
    example_casa_clean_factunit as clean_factunit,
    example_casa_dirty_factunit as dirty_factunit,
    example_sky_blue_factunit as sky_blue_factunit,
    get_budunit_55_example,
    get_budunit_invalid_example,
)
from src.ref.keywords import Ch11Keywords as kw, ExampleStrs as exx


def test_save_belief_file_SetsFile(temp_dir_setup):
    # ESTABLISH
    temp_dir = get_temp_dir()
    belief_filename = "belief.json"
    belief_path = create_path(temp_dir, belief_filename)
    sue_belief = beliefunit_shop(exx.sue)
    assert os_path_exists(belief_path) is False

    # WHEN
    save_belief_file(belief_path, None, sue_belief)

    # THEN
    assert os_path_exists(belief_path)


def test_open_belief_file_ReturnsObj_Scenario0_NoFile():
    # ESTABLISH
    temp_dir = get_temp_dir()
    belief_filename = "belief.json"
    belief_path = create_path(temp_dir, belief_filename)
    assert os_path_exists(belief_path) is False

    # WHEN
    gen_sue_belief = open_belief_file(belief_path)

    # THEN
    assert not gen_sue_belief


def test_open_belief_file_ReturnsObj_Scenario1_FileExists():
    # ESTABLISH
    temp_dir = get_temp_dir()
    belief_filename = "belief.json"
    belief_path = create_path(temp_dir, belief_filename)
    expected_sue_belief = beliefunit_shop(exx.sue)
    save_belief_file(belief_path, None, expected_sue_belief)
    assert os_path_exists(belief_path)

    # WHEN
    gen_sue_belief = open_belief_file(belief_path)

    # THEN
    assert gen_sue_belief == expected_sue_belief


def test_save_arbitrary_beliefspark_SetsFile_Scenario0(temp_dir_setup):
    # ESTABLISH
    moment_mstr_dir = get_temp_dir()
    spark5 = 5
    beliefspark_path = create_beliefspark_path(
        moment_mstr_dir, exx.a23, exx.sue, spark5
    )
    assert os_path_exists(beliefspark_path) is False

    # WHEN
    save_arbitrary_beliefspark(moment_mstr_dir, exx.a23, exx.sue, spark5)

    # THEN
    assert os_path_exists(beliefspark_path)
    expected_sue_belief = beliefunit_shop(exx.sue, exx.a23)
    assert open_belief_file(beliefspark_path).to_dict() == expected_sue_belief.to_dict()


def test_save_arbitrary_beliefspark_SetsFile_Scenario1_includes_facts(
    temp_dir_setup,
):
    # ESTABLISH
    moment_mstr_dir = get_temp_dir()
    spark5 = 5
    beliefspark_path = create_beliefspark_path(
        moment_mstr_dir, exx.a23, exx.sue, spark5
    )
    casa_rope = create_rope(exx.a23, "casa")
    clean_rope = create_rope(casa_rope, "clean")
    clean_fact_lower = 11
    clean_fact_upper = 16
    x_facts = [(casa_rope, clean_rope, clean_fact_lower, clean_fact_upper)]
    assert os_path_exists(beliefspark_path) is False

    # WHEN
    save_arbitrary_beliefspark(moment_mstr_dir, exx.a23, exx.sue, spark5, facts=x_facts)

    # THEN
    assert os_path_exists(beliefspark_path)
    expected_sue_belief = beliefunit_shop(exx.sue, exx.a23)
    expected_sue_belief.add_fact(
        casa_rope, clean_rope, clean_fact_lower, clean_fact_upper, True
    )
    gen_sue_belief = open_belief_file(beliefspark_path)
    assert (
        gen_sue_belief.get_kegroot_factunits_dict()
        == expected_sue_belief.get_kegroot_factunits_dict()
    )
    assert gen_sue_belief.to_dict() == expected_sue_belief.to_dict()


def test_get_beliefspark_obj_ReturnsObj_Scenario0_NoFile(temp_dir_setup):
    # ESTABLISH
    moment_mstr_dir = get_temp_dir()
    t3 = 3

    # WHEN / THEN
    assert get_beliefspark_obj(moment_mstr_dir, exx.a23, exx.sue, t3) is None


def test_get_beliefspark_obj_ReturnsObj_Scenario1_FileExists(temp_dir_setup):
    # ESTABLISH
    moment_mstr_dir = get_temp_dir()
    t3 = 3
    t3_json_path = create_beliefspark_path(moment_mstr_dir, exx.a23, exx.sue, t3)
    sue_belief = beliefunit_shop(exx.sue, exx.a23)
    casa_rope = sue_belief.make_l1_rope("casa")
    clean_rope = sue_belief.make_l1_rope("clean")
    dirty_rope = sue_belief.make_l1_rope("dirty")
    sue_belief.add_fact(casa_rope, dirty_rope, create_missing_kegs=True)
    save_belief_file(t3_json_path, None, sue_belief)

    # WHEN
    gen_a3_beliefspark = get_beliefspark_obj(moment_mstr_dir, exx.a23, exx.sue, t3)

    # THEN
    assert gen_a3_beliefspark == sue_belief


def test_collect_belief_spark_dir_sets_ReturnsObj_Scenario0_none(
    temp_dir_setup,
):
    # ESTABLISH
    moment_mstr_dir = get_temp_dir()
    # WHEN
    belief_sparks_sets = collect_belief_spark_dir_sets(moment_mstr_dir, exx.a23)
    # THEN
    assert belief_sparks_sets == {}


def test_collect_belief_spark_dir_sets_ReturnsObj_Scenario1_DirsExist(
    temp_dir_setup,
):
    # ESTABLISH
    moment_mstr_dir = get_temp_dir()
    spark1 = 1
    spark2 = 2
    bob1_dir = create_belief_spark_dir_path(moment_mstr_dir, exx.a23, exx.bob, spark1)
    bob2_dir = create_belief_spark_dir_path(moment_mstr_dir, exx.a23, exx.bob, spark2)
    print(f"  {bob1_dir=}")
    print(f"  {bob2_dir=}")
    set_dir(bob1_dir)
    set_dir(bob2_dir)

    # WHEN
    belief_sparks_sets = collect_belief_spark_dir_sets(moment_mstr_dir, exx.a23)

    # THEN
    assert belief_sparks_sets == {exx.bob: {spark1, spark2}}


def test_collect_belief_spark_dir_sets_ReturnsObj_Scenario2_DirsExist(
    temp_dir_setup,
):
    # ESTABLISH
    moment_mstr_dir = get_temp_dir()
    spark1 = 1
    spark2 = 2
    spark7 = 7
    bob1_dir = create_belief_spark_dir_path(moment_mstr_dir, exx.a23, exx.bob, spark1)
    bob2_dir = create_belief_spark_dir_path(moment_mstr_dir, exx.a23, exx.bob, spark2)
    sue2_dir = create_belief_spark_dir_path(moment_mstr_dir, exx.a23, exx.sue, spark2)
    sue7_dir = create_belief_spark_dir_path(moment_mstr_dir, exx.a23, exx.sue, spark7)
    set_dir(bob1_dir)
    set_dir(bob2_dir)
    set_dir(sue2_dir)
    set_dir(sue7_dir)

    # WHEN
    belief_sparks_sets = collect_belief_spark_dir_sets(moment_mstr_dir, exx.a23)

    # THEN
    assert belief_sparks_sets == {
        exx.bob: {spark1, spark2},
        exx.sue: {spark2, spark7},
    }


def test_get_beliefs_downhill_spark_nums_ReturnsObj_Scenario0_Empty():
    # ESTABLISH
    spark2 = 2
    belief_sparks_sets = {}
    downhill_spark_num = spark2
    downhill_beliefs = {exx.bob, exx.sue}

    # WHEN
    beliefs_downhill_spark_nums = get_beliefs_downhill_spark_nums(
        belief_sparks_sets, downhill_beliefs, downhill_spark_num
    )

    # THEN
    assert beliefs_downhill_spark_nums == {}


def test_get_beliefs_downhill_spark_nums_ReturnsObj_Scenario1_simple():
    # ESTABLISH
    spark1 = 1
    spark2 = 2
    spark7 = 7
    belief_sparks_sets = {exx.bob: {spark1, spark2}, exx.sue: {spark2, spark7}}
    downhill_spark_num = spark2
    downhill_beliefs = {exx.bob, exx.sue}

    # WHEN
    beliefs_downhill_spark_nums = get_beliefs_downhill_spark_nums(
        belief_sparks_sets, downhill_beliefs, downhill_spark_num
    )

    # THEN
    assert beliefs_downhill_spark_nums == {exx.bob: spark2, exx.sue: spark2}


def test_get_beliefs_downhill_spark_nums_ReturnsObj_Scenario2Empty_downhill_spark_num():
    # ESTABLISH
    spark1 = 1
    spark2 = 2
    spark7 = 7
    belief_sparks_sets = {
        exx.bob: {spark1, spark2},
        exx.sue: {spark2, spark7},
        exx.yao: {spark1, spark2, spark7},
    }
    downhill_beliefs = {exx.bob, exx.sue}

    # WHEN
    beliefs_downhill_spark_nums = get_beliefs_downhill_spark_nums(
        belief_sparks_sets, downhill_beliefs
    )

    # THEN
    assert beliefs_downhill_spark_nums == {exx.bob: spark2, exx.sue: spark7}


def test_get_beliefs_downhill_spark_nums_ReturnsObj_Scenario3Empty_downhill_beliefs():
    # ESTABLISH
    spark1 = 1
    spark2 = 2
    spark7 = 7
    belief_sparks_sets = {
        exx.bob: {spark1, spark2},
        exx.sue: {spark2, spark7},
        exx.yao: {spark1, spark2, spark7},
    }

    # WHEN
    beliefs_downhill_spark_nums = get_beliefs_downhill_spark_nums(belief_sparks_sets)

    # THEN
    assert beliefs_downhill_spark_nums == {
        exx.bob: spark2,
        exx.sue: spark7,
        exx.yao: spark7,
    }


def test_get_beliefs_downhill_spark_nums_ReturnsObj_Scenario4Empty_downhill_beliefs_Withdownhill_spark_num():
    # ESTABLISH
    spark1 = 1
    spark2 = 2
    spark7 = 7
    belief_sparks_sets = {
        exx.bob: {spark1, spark2},
        exx.sue: {spark2, spark7},
        exx.yao: {spark7},
    }
    downhill_spark_num = 2

    # WHEN
    beliefs_downhill_spark_nums = get_beliefs_downhill_spark_nums(
        belief_sparks_sets, ref_spark_num=downhill_spark_num
    )

    # THEN
    assert beliefs_downhill_spark_nums == {exx.bob: spark2, exx.sue: spark2}


def test_cellunit_add_json_file_SetsFile_Scenario0(temp_dir_setup):
    # ESTABLISH
    moment_mstr_dir = get_temp_dir()
    time7 = 777000
    sue7_cell_path = node_path(moment_mstr_dir, exx.a23, exx.sue, time7)
    spark3 = 3
    das = []
    quota500 = 500
    celldepth4 = 4
    mana_grain6 = 6
    assert os_path_exists(sue7_cell_path) is False

    # WHEN
    cellunit_add_json_file(
        moment_mstr_dir=moment_mstr_dir,
        moment_label=exx.a23,
        time_belief_name=exx.sue,
        bud_time=time7,
        quota=quota500,
        spark_num=spark3,
        celldepth=celldepth4,
        mana_grain=mana_grain6,
        bud_ancestors=das,
    )

    # THEN
    print(f"{sue7_cell_path=}")
    assert os_path_exists(sue7_cell_path)
    generated_cell_dict = open_json(sue7_cell_path)
    assert generated_cell_dict.get(kw.ancestors) == das
    assert generated_cell_dict.get(kw.spark_num) == spark3
    assert generated_cell_dict.get(kw.celldepth) == celldepth4
    assert generated_cell_dict.get(kw.bud_belief_name) == exx.sue
    assert generated_cell_dict.get(kw.mana_grain) == mana_grain6
    assert generated_cell_dict.get(kw.quota) == quota500


def test_cellunit_add_json_file_SetsFile_Scenario1_ManyParametersEmpty(
    temp_dir_setup,
):
    # ESTABLISH
    moment_mstr_dir = get_temp_dir()
    time7 = 777000
    das = [exx.bob, exx.sue]
    sue7_cell_path = node_path(moment_mstr_dir, exx.a23, exx.sue, time7, das)
    spark3 = 3
    assert os_path_exists(sue7_cell_path) is False

    # WHEN
    cellunit_add_json_file(
        moment_mstr_dir, exx.a23, exx.sue, time7, spark3, bud_ancestors=das
    )

    # THEN
    print(f"{sue7_cell_path=}")
    assert os_path_exists(sue7_cell_path)
    generated_cell_dict = open_json(sue7_cell_path)
    assert generated_cell_dict.get(kw.ancestors) == das
    assert generated_cell_dict.get(kw.spark_num) == spark3
    assert generated_cell_dict.get(kw.celldepth) == 0
    assert generated_cell_dict.get(kw.bud_belief_name) == exx.sue
    assert generated_cell_dict.get(kw.mana_grain) == 1
    assert generated_cell_dict.get(kw.quota) == CELLNODE_QUOTA_DEFAULT


def test_cellunit_get_from_dir_ReturnsObj_Scenario0_NoFileExists(temp_dir_setup):
    # ESTABLISH
    moment_mstr_dir = get_temp_dir()
    time7 = 777000
    das = [exx.bob, exx.sue]
    sue7_cell_path = node_path(moment_mstr_dir, exx.a23, exx.sue, time7, das)
    spark3 = 3
    assert os_path_exists(sue7_cell_path) is False
    cell_dir = create_cell_dir_path(
        moment_mstr_dir, exx.a23, exx.sue, time7, bud_ancestors=das
    )

    # WHEN / THEN
    assert cellunit_get_from_dir(cell_dir) is None


def test_cellunit_get_from_dir_ReturnsObj_Scenario1_FileExists(temp_dir_setup):
    # ESTABLISH
    moment_mstr_dir = get_temp_dir()
    time7 = 777000
    das = [exx.bob, exx.sue]
    sue7_cell_path = node_path(moment_mstr_dir, exx.a23, exx.sue, time7, das)
    spark3 = 3
    assert os_path_exists(sue7_cell_path) is False
    cellunit_add_json_file(
        moment_mstr_dir, exx.a23, exx.sue, time7, spark3, bud_ancestors=das
    )
    cell_dir = create_cell_dir_path(
        moment_mstr_dir, exx.a23, exx.sue, time7, bud_ancestors=das
    )

    # WHEN
    gen_cellunit = cellunit_get_from_dir(cell_dir)

    # THEN
    expected_cellunit = cellunit_shop(exx.sue, ancestors=das, spark_num=spark3)
    assert gen_cellunit == expected_cellunit


def test_cellunit_save_to_dir_ReturnsObj_Scenario0(temp_dir_setup):
    # ESTABLISH
    moment_mstr_dir = get_temp_dir()
    time7 = 777000
    das = [exx.bob, exx.sue]
    sue7_cell_path = node_path(moment_mstr_dir, exx.a23, exx.sue, time7, das)
    spark3 = 3
    sue_cell = cellunit_shop(exx.sue, ancestors=das, spark_num=spark3)
    cell_dir = create_cell_dir_path(moment_mstr_dir, exx.a23, exx.sue, time7, das)
    assert os_path_exists(sue7_cell_path) is False

    # WHEN
    cellunit_save_to_dir(cell_dir, sue_cell)

    # THEN
    assert os_path_exists(sue7_cell_path)
    assert cellunit_get_from_dir(cell_dir) == sue_cell


def test_create_cell_voice_mandate_ledger_json_CreatesFile_Scenario0_NoCellFile(
    temp_dir_setup,
):
    # ESTABLISH
    mstr_dir = get_temp_dir()
    sue_ancestors = [exx.sue]
    tp6 = 6
    sue_voice_mandate_ledger_path = create_cell_voice_mandate_ledger_path(
        mstr_dir, exx.a23, exx.bob, tp6, sue_ancestors
    )
    sue_cell_dir = create_cell_dir_path(mstr_dir, exx.a23, exx.bob, tp6, sue_ancestors)
    assert os_path_exists(sue_voice_mandate_ledger_path) is False

    # WHEN
    create_cell_voice_mandate_ledger_json(sue_cell_dir)

    # THEN
    assert os_path_exists(sue_voice_mandate_ledger_path) is False


def test_create_cell_voice_mandate_ledger_json_CreatesFile_Scenario1(
    temp_dir_setup,
):
    # ESTABLISH
    mstr_dir = get_temp_dir()
    sue_ancestors = [exx.sue]
    sue_spark7 = 7
    sue_celldepth3 = 3
    sue_mana_grain2 = 2
    sue_quota300 = 300
    sue_mandate = 444
    sue_belief = beliefunit_shop(exx.sue, exx.a23)
    sue_belief.add_voiceunit(exx.sue, 3, 5)
    sue_belief.add_voiceunit(exx.yao, 7, 2)
    clean_fact = clean_factunit()
    dirty_fact = dirty_factunit()
    sue_belief.add_keg(clean_fact.fact_state)
    sue_belief.add_keg(dirty_fact.fact_state)
    casa_rope = sue_belief.make_l1_rope("casa")
    mop_rope = sue_belief.make_rope(casa_rope, "mop")
    sue_belief.add_keg(mop_rope, 1, pledge=True)
    sue_belief.edit_reason(mop_rope, dirty_fact.fact_context, dirty_fact.fact_state)
    sue_belief.add_fact(
        dirty_fact.fact_context, dirty_fact.fact_state, create_missing_kegs=True
    )
    sky_blue_fact = sky_blue_factunit()
    sue_beliefspark_factunits = {clean_fact.fact_context: clean_fact}
    sue_found_factunits = {dirty_fact.fact_context: dirty_fact}
    sue_boss_factunits = {sky_blue_fact.fact_context: sky_blue_fact}
    sue_cell = cellunit_shop(
        bud_belief_name=exx.yao,
        ancestors=sue_ancestors,
        spark_num=sue_spark7,
        celldepth=sue_celldepth3,
        mana_grain=sue_mana_grain2,
        quota=sue_quota300,
        beliefadjust=sue_belief,
        beliefspark_facts=sue_beliefspark_factunits,
        found_facts=sue_found_factunits,
        boss_facts=sue_boss_factunits,
        mandate=sue_mandate,
    )
    sue_cell.reason_contexts = set()
    tp6 = 6
    sue_voice_mandate_ledger_path = create_cell_voice_mandate_ledger_path(
        mstr_dir, exx.a23, exx.bob, tp6, sue_ancestors
    )
    sue_cell_dir = create_cell_dir_path(mstr_dir, exx.a23, exx.bob, tp6, sue_ancestors)
    cellunit_save_to_dir(sue_cell_dir, sue_cell)
    assert os_path_exists(sue_voice_mandate_ledger_path) is False

    # WHEN
    create_cell_voice_mandate_ledger_json(sue_cell_dir)

    # THEN
    assert os_path_exists(sue_voice_mandate_ledger_path)
    assert open_json(sue_voice_mandate_ledger_path) == {exx.yao: 311, exx.sue: 133}


def test_save_valid_bud_file_Scenario0_SavesFile(temp_dir_setup):
    # ESTABLISH
    mstr_dir = get_temp_dir()
    t55_bud = get_budunit_55_example()
    t55_bud_time = t55_bud.bud_time
    t55_bud_path = create_budunit_json_path(mstr_dir, exx.a23, exx.yao, t55_bud_time)
    assert os_path_exists(t55_bud_path) is False

    # WHEN
    save_bud_file(mstr_dir, exx.a23, exx.yao, t55_bud)

    # THEN
    assert os_path_exists(t55_bud_path)


def test_save_valid_bud_file_Scenario1_RaisesError(temp_dir_setup):
    # ESTABLISH
    mstr_dir = get_temp_dir()
    invalid_bud = get_budunit_invalid_example()

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        save_bud_file(mstr_dir, exx.a23, exx.yao, invalid_bud)
    exception_str = (
        "magnitude cannot be calculated: debt_bud_voice_net=-5, cred_bud_voice_net=3"
    )
    assert str(excinfo.value) == exception_str


def test_bud_file_exists_ReturnsObj(temp_dir_setup):
    # ESTABLISH
    mstr_dir = get_temp_dir()
    t55_bud = get_budunit_55_example()
    assert not bud_file_exists(mstr_dir, exx.a23, exx.yao, t55_bud.bud_time)

    # WHEN
    save_bud_file(mstr_dir, exx.a23, exx.yao, t55_bud)

    # THEN
    assert bud_file_exists(mstr_dir, exx.a23, exx.yao, t55_bud.bud_time)


def test_open_bud_file_ReturnsObj_Scenario0_NoFileExists(temp_dir_setup):
    # ESTABLISH
    mstr_dir = get_temp_dir()
    t55_bud = get_budunit_55_example()
    t55_bud_time = t55_bud.bud_time
    assert not bud_file_exists(mstr_dir, exx.a23, exx.yao, t55_bud_time)

    # WHEN / THEN
    assert not open_bud_file(mstr_dir, exx.a23, exx.yao, t55_bud_time)


def test_open_bud_file_ReturnsObj_Scenario1_FileExists(temp_dir_setup):
    # ESTABLISH
    mstr_dir = get_temp_dir()
    t55_bud = get_budunit_55_example()
    t55_bud_time = t55_bud.bud_time
    save_bud_file(mstr_dir, exx.a23, exx.yao, t55_bud)
    assert bud_file_exists(mstr_dir, exx.a23, exx.yao, t55_bud_time)

    # WHEN / THEN
    assert open_bud_file(mstr_dir, exx.a23, exx.yao, t55_bud_time) == t55_bud


def test_save_belieftime_file_SavesFile(temp_dir_setup):
    # ESTABLISH
    mstr_dir = get_temp_dir()
    t55_belieftime = get_beliefunit_with_4_levels()
    t55_bud_time = 55
    t55_belieftime_path = create_belieftime_path(
        mstr_dir, exx.a23, exx.sue, t55_bud_time
    )
    print(f"{t55_belieftime.moment_label=}")
    print(f"               {mstr_dir=}")
    print(f"      {t55_belieftime_path=}")
    assert os_path_exists(t55_belieftime_path) is False

    # WHEN
    save_belieftime_file(mstr_dir, t55_belieftime, t55_bud_time)

    # THEN
    assert os_path_exists(t55_belieftime_path)


def test_save_belieftime_file_RaisesError(temp_dir_setup):
    # ESTABLISH
    mstr_dir = get_temp_dir()
    irrational_belieftime = get_beliefunit_irrational_example()
    t55_bud_time = 55

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        save_belieftime_file(mstr_dir, irrational_belieftime, t55_bud_time)
    exception_str = "BeliefTime could not be saved BeliefUnit.rational is False"
    assert str(excinfo.value) == exception_str


def test_belieftime_file_exists_ReturnsObj(temp_dir_setup):
    # ESTABLISH
    mstr_dir = get_temp_dir()
    t55_bud_time = 55
    assert belieftime_file_exists(mstr_dir, exx.a23, exx.sue, t55_bud_time) is False

    # WHEN
    t55_belieftime = get_beliefunit_with_4_levels()
    save_belieftime_file(mstr_dir, t55_belieftime, t55_bud_time)

    # THEN
    assert belieftime_file_exists(mstr_dir, exx.a23, exx.sue, t55_bud_time)


def test_open_belieftime_file_ReturnsObj_Scenario0_NoFileExists(
    temp_dir_setup,
):
    # ESTABLISH
    mstr_dir = get_temp_dir()
    t55_bud_time = 55
    assert not belieftime_file_exists(mstr_dir, exx.a23, exx.sue, t55_bud_time)

    # WHEN / THEN
    assert not open_belieftime_file(mstr_dir, exx.a23, exx.sue, t55_bud_time)


def test_open_belieftime_file_ReturnsObj_Scenario1_FileExists(temp_dir_setup):
    # ESTABLISH
    mstr_dir = get_temp_dir()
    t55_bud_time = 55
    t55_belieftime = get_beliefunit_with_4_levels()
    save_belieftime_file(mstr_dir, t55_belieftime, t55_bud_time)
    assert belieftime_file_exists(mstr_dir, exx.a23, exx.sue, t55_bud_time)

    # WHEN
    file_belieftime = open_belieftime_file(mstr_dir, exx.a23, exx.sue, t55_bud_time)

    # THEN
    assert file_belieftime.to_dict() == t55_belieftime.to_dict()


def test_get_epochtime_dirs_ReturnsObj_Scenario0(temp_dir_setup):
    # ESTABLISH
    mstr_dir = get_temp_dir()
    t55_bud_time = 55
    t77_bud_time = 77
    belieftime = get_beliefunit_with_4_levels()
    save_belieftime_file(mstr_dir, belieftime, t55_bud_time)
    save_belieftime_file(mstr_dir, belieftime, t77_bud_time)

    # WHEN
    epochtime_dirs = get_epochtime_dirs(mstr_dir, exx.a23, exx.sue)

    # THEN
    assert epochtime_dirs == [t55_bud_time, t77_bud_time]
