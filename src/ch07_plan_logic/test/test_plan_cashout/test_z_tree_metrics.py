from src.ch03_voice.group import awardunit_shop
from src.ch03_voice.voice import voiceunit_shop
from src.ch04_rope.rope import create_rope_from_labels
from src.ch06_keg.keg import kegunit_shop
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch07_plan_logic.test._util.ch07_examples import planunit_v001
from src.ref.keywords import ExampleStrs as exx


def test_PlanUnit_get_tree_metrics_Exists():
    # ESTABLISH
    zia_plan = planunit_shop(plan_name="Zia")

    # WHEN
    zia_plan_tree_metrics = zia_plan.get_tree_metrics()

    # THEN
    assert zia_plan_tree_metrics.label_count is not None
    assert zia_plan_tree_metrics.reason_contexts is not None
    assert zia_plan_tree_metrics.tree_level_count is not None
    assert zia_plan_tree_metrics.awardunits_metrics is not None


def test_PlanUnit_get_tree_metrics_get_keg_uid_max_GetsMaxKegUID():
    # ESTABLISH
    yao_plan = planunit_v001()

    # WHEN
    tree_metrics_x = yao_plan.get_tree_metrics()

    # THEN
    assert tree_metrics_x.uid_max == 279
    assert yao_plan.get_keg_uid_max() == 279


def test_PlanUnit_get_tree_metrics_SetsBoolean_all_keg_uids_are_unique():
    # ESTABLISH
    yao_plan = planunit_v001()

    # WHEN
    tree_metrics_x = yao_plan.get_tree_metrics()

    # THEN
    assert tree_metrics_x.all_keg_uids_are_unique is False
    assert len(tree_metrics_x.uid_dict) == 219


def test_PlanUnit_get_tree_set_all_keg_uids_unique():
    # ESTABLISH
    yao_plan = planunit_v001()
    tree_metrics_before = yao_plan.get_tree_metrics()
    assert len(tree_metrics_before.uid_dict) == 219

    # WHEN
    yao_plan.set_all_keg_uids_unique()

    # THEN
    tree_metrics_after = yao_plan.get_tree_metrics()
    # for uid, uid_count in tree_metrics_after.uid_dict.items():
    #     # print(f"{uid=} {uid_count=} {len(yao_plan.get_keg_dict())=}")
    #     print(f"{uid=} {uid_count=} ")
    assert len(tree_metrics_after.uid_dict) == 252
    assert tree_metrics_after.all_keg_uids_are_unique is True


def test_PlanUnit_set_all_keg_uids_unique_SetsUIDs():
    # ESTABLISH
    zia_plan = planunit_shop(plan_name=exx.zia)
    sports_str = "sports"
    zia_plan.set_l1_keg(kegunit_shop(exx.swim, uid=None))
    zia_plan.set_l1_keg(kegunit_shop(sports_str, uid=2))
    swim_rope = zia_plan.make_l1_rope(exx.swim)
    assert zia_plan.get_keg_obj(swim_rope).uid is None

    # WHEN
    zia_plan.set_all_keg_uids_unique()

    # THEN
    assert zia_plan.get_keg_obj(swim_rope).uid is not None


def test_PlanUnit_get_tree_metrics_ReturnsANone_pledge_KegRopeTerm():
    # ESTABLISH
    nia_str = "Nia"
    nia_plan = planunit_shop(nia_str, tally=10)
    wk = "wk"
    nia_plan.set_l1_keg(kegunit_shop(wk, star=40))
    tree_metrics_before = nia_plan.get_tree_metrics()

    # WHEN / THEN
    assert tree_metrics_before.last_evaluated_pledge_keg_rope is None


def test_PlanUnit_get_tree_metrics_Returns_pledge_KegRopeTerm():
    # ESTABLISH
    yao_plan = planunit_v001()
    yao_tree_metrics = yao_plan.get_tree_metrics()

    # WHEN / THEN
    traain_rope = create_rope_from_labels(
        [
            yao_plan.kegroot.keg_label,
            "ACME",
            "ACME Employee Responsiblities",
            "Know Abuse Deterrence and Reporting guildlines",
            "Accomplish Fall 2021 traaining",
        ]
    )
    assert yao_tree_metrics.last_evaluated_pledge_keg_rope == traain_rope


def test_PlanUnit_get_tree_metrics_TracksReasonsThatHaveNoFactreason_contexts():
    # ESTABLISH
    yao_planunit = planunit_v001()

    # WHEN
    yao_tree_metrics = yao_planunit.get_tree_metrics()

    # THEN
    print(f"{yao_tree_metrics.tree_level_count=}")
    print(f"{yao_tree_metrics.reason_contexts=}")
    assert yao_tree_metrics is not None
    reason_contexts_x = yao_tree_metrics.reason_contexts
    assert reason_contexts_x is not None
    assert len(reason_contexts_x) > 0


def test_PlanUnit_get_missing_fact_reason_contexts_ReturnsAllreason_contextsNotCoveredByFacts():
    # ESTABLISH
    yao_planunit = planunit_v001()
    missing_reason_contexts = yao_planunit.get_missing_fact_reason_contexts()
    assert missing_reason_contexts is not None
    print(f"{missing_reason_contexts=}")
    print(f"{len(missing_reason_contexts)=}")
    assert len(missing_reason_contexts) == 11

    yao_planunit.add_fact(
        yao_planunit.make_l1_rope("jour_minute"),
        fact_state=yao_planunit.make_l1_rope("jour_minute"),
        fact_lower=0,
        fact_upper=1439,
    )

    # WHEN
    missing_reason_contexts = yao_planunit.get_missing_fact_reason_contexts()

    # THEN
    assert len(missing_reason_contexts) == 11


def test_PlanUnit_3AdvocatesNokegunit_shop():
    # ESTABLISH

    zia_planunit = planunit_shop("Zia")
    yao_voiceunit = voiceunit_shop(voice_name=exx.yao)
    sue_voiceunit = voiceunit_shop(voice_name=exx.sue)
    zia_voiceunit = voiceunit_shop(voice_name=exx.zia)
    # print(f"{yao=}")
    zia_planunit.set_voiceunit(yao_voiceunit)
    zia_planunit.set_voiceunit(sue_voiceunit)
    zia_planunit.set_voiceunit(zia_voiceunit)
    zia_planunit.kegroot.set_awardunit(awardunit_shop(exx.yao, give_force=10))
    zia_planunit.kegroot.set_awardunit(awardunit_shop(exx.sue, give_force=10))
    zia_planunit.kegroot.set_awardunit(awardunit_shop(exx.zia, give_force=10))

    # WHEN
    assert zia_planunit.get_awardunits_metrics() is not None
    voices_metrics = zia_planunit.get_awardunits_metrics()

    # THEN
    yao_awardunit = voices_metrics[exx.yao]
    sue_awardunit = voices_metrics[exx.sue]
    zia_awardunit = voices_metrics[exx.zia]
    assert yao_awardunit.awardee_title is not None
    assert sue_awardunit.awardee_title is not None
    assert zia_awardunit.awardee_title is not None
    assert yao_awardunit.awardee_title == exx.yao
    assert sue_awardunit.awardee_title == exx.sue
    assert zia_awardunit.awardee_title == exx.zia
