from pytest import raises as pytest_raises
from src.ch05_reason.reason_main import factunit_shop
from src.ch06_keg.keg import kegunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch07_belief_logic.test._util.ch07_examples import get_beliefunit_with_4_levels
from src.ref.keywords import ExampleStrs as exx


def test_BeliefUnit_set_fact_ModifiesAttr_1():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    sem_jour_rope = sue_belief.make_l1_rope("sem_jours")
    sun_rope = sue_belief.make_rope(sem_jour_rope, "Sun")
    sun_belief_fact = factunit_shop(fact_context=sem_jour_rope, fact_state=sun_rope)
    print(sun_belief_fact)
    x_kegroot = sue_belief.kegroot
    x_kegroot.factunits = {sun_belief_fact.fact_context: sun_belief_fact}
    assert x_kegroot.factunits is not None
    x_kegroot.factunits = {}
    assert not x_kegroot.factunits

    # ESTABLISH
    sue_belief.add_fact(fact_context=sem_jour_rope, fact_state=sun_rope)

    # THEN
    assert x_kegroot.factunits == {sun_belief_fact.fact_context: sun_belief_fact}

    # ESTABLISH
    x_kegroot.factunits = {}
    assert not x_kegroot.factunits
    usa_wk_rope = sue_belief.make_l1_rope("nation")
    usa_wk_fact = factunit_shop(
        usa_wk_rope, usa_wk_rope, fact_lower=608, fact_upper=610
    )
    x_kegroot.factunits = {usa_wk_fact.fact_context: usa_wk_fact}

    x_kegroot.factunits = {}
    assert not x_kegroot.factunits

    # WHEN
    sue_belief.add_fact(
        fact_context=usa_wk_rope, fact_state=usa_wk_rope, fact_lower=608, fact_upper=610
    )

    # THEN
    assert x_kegroot.factunits is not None
    assert x_kegroot.factunits == {usa_wk_fact.fact_context: usa_wk_fact}


def test_BeliefUnit_set_fact_ModifiesAttr_2():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    sem_jour_rope = sue_belief.make_l1_rope("sem_jours")
    sun_rope = sue_belief.make_rope(sem_jour_rope, "Sun")

    # WHEN
    sue_belief.add_fact(fact_context=sem_jour_rope, fact_state=sun_rope)

    # THEN
    sun_belief_fact = factunit_shop(fact_context=sem_jour_rope, fact_state=sun_rope)
    x_kegroot = sue_belief.kegroot
    assert x_kegroot.factunits == {sun_belief_fact.fact_context: sun_belief_fact}


def test_BeliefUnit_set_fact_ModifiesAttrWhen_fact_state_IsNone():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    sem_jour_rope = sue_belief.make_l1_rope("sem_jours")

    # WHEN
    sue_belief.add_fact(fact_context=sem_jour_rope, fact_lower=5, fact_upper=7)

    # THEN
    sun_belief_fact = factunit_shop(sem_jour_rope, sem_jour_rope, 5, 7)
    x_kegroot = sue_belief.kegroot
    assert x_kegroot.factunits == {sun_belief_fact.fact_context: sun_belief_fact}


def test_BeliefUnit_set_fact_ModifiesAttrWhen_reason_lower_IsNone():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    sem_jour_rope = sue_belief.make_l1_rope("sem_jours")
    sue_belief.add_fact(fact_context=sem_jour_rope, fact_lower=5, fact_upper=7)
    x_kegroot = sue_belief.kegroot
    x7_factunit = factunit_shop(sem_jour_rope, sem_jour_rope, 5, 7)
    assert x_kegroot.factunits.get(sem_jour_rope) == x7_factunit

    # WHEN
    sue_belief.add_fact(fact_context=sem_jour_rope, fact_upper=10)

    # THEN
    x10_factunit = factunit_shop(sem_jour_rope, sem_jour_rope, 5, 10)
    assert x_kegroot.factunits.get(sem_jour_rope) == x10_factunit


def test_BeliefUnit_set_fact_FailsToCreateWhenreason_contextAndFactAreDifferenctAndFactKegIsNot_RangeRoot():
    # ESTABLISH
    bob_belief = beliefunit_shop("Bob")
    ziet_str = "ziet"
    ziet_keg = kegunit_shop(ziet_str, begin=0, close=140)
    bob_belief.set_l1_keg(ziet_keg)
    ziet_rope = bob_belief.make_l1_rope(ziet_str)
    a1st = "age1st"
    a1st_rope = bob_belief.make_rope(ziet_rope, a1st)
    a1st_keg = kegunit_shop(a1st, begin=0, close=20)
    bob_belief.set_keg_obj(a1st_keg, parent_rope=ziet_rope)
    a1e1st_str = "a1_era1st"
    a1e1st_keg = kegunit_shop(a1e1st_str, begin=20, close=30)
    bob_belief.set_keg_obj(a1e1st_keg, parent_rope=a1st_rope)
    a1e1_rope = bob_belief.make_rope(a1st_rope, a1e1st_str)
    assert bob_belief.kegroot.factunits in (None, {})

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        bob_belief.add_fact(
            fact_context=a1e1_rope, fact_state=a1e1_rope, fact_lower=20, fact_upper=23
        )
    x_str = f"Non rangeroot fact:{a1e1_rope} can only be set by rangeroot fact"
    assert str(excinfo.value) == x_str


def test_BeliefUnit_del_fact_ModifiesAttr():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    sem_jour_rope = sue_belief.make_l1_rope("sem_jours")
    sun_rope = sue_belief.make_rope(sem_jour_rope, "Sun")
    sue_belief.add_fact(fact_context=sem_jour_rope, fact_state=sun_rope)
    sun_belief_fact = factunit_shop(fact_context=sem_jour_rope, fact_state=sun_rope)
    x_kegroot = sue_belief.kegroot
    assert x_kegroot.factunits == {sun_belief_fact.fact_context: sun_belief_fact}

    # WHEN
    sue_belief.del_fact(fact_context=sem_jour_rope)

    # THEN
    assert x_kegroot.factunits == {}


def test_BeliefUnit_get_fact_ReturnsFactUnit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    situations_str = "situations"
    situations_rope = sue_belief.make_l1_rope(situations_str)
    climate_str = "climate"
    climate_rope = sue_belief.make_rope(situations_rope, climate_str)
    sue_belief.add_fact(situations_rope, climate_rope, create_missing_kegs=True)

    # WHEN
    generated_situations_reason_context = sue_belief.get_fact(situations_rope)

    # THEN
    static_situations_reason_context = sue_belief.kegroot.factunits.get(situations_rope)
    assert generated_situations_reason_context == static_situations_reason_context


def test_BeliefUnit_get_rangeroot_factunits_ReturnsObj_Scenario0():
    # ESTABLISH a single ranged fact
    sue_belief = beliefunit_shop("Sue")
    ziet_str = "ziet"
    ziet_keg = kegunit_shop(ziet_str, begin=0, close=140)
    sue_belief.set_l1_keg(ziet_keg)

    clean_keg = kegunit_shop(exx.clean, pledge=True)
    sue_belief.set_l1_keg(clean_keg)
    c_rope = sue_belief.make_l1_rope(exx.clean)
    ziet_rope = sue_belief.make_l1_rope(ziet_str)
    # sue_belief.edit_keg_attr(c_rope, reason_context=ziet_rope, reason_case=ziet_rope, reason_lower=5, reason_upper=10)

    sue_belief.add_fact(
        fact_context=ziet_rope, fact_state=ziet_rope, fact_lower=5, fact_upper=10
    )
    print(f"Establish a single ranged fact {sue_belief.kegroot.factunits=}")
    assert len(sue_belief.kegroot.factunits) == 1

    # WHEN / THEN
    assert len(sue_belief._get_rangeroot_factunits()) == 1

    # WHEN one ranged fact added
    place_str = "place_x"
    place_keg = kegunit_shop(place_str, begin=600, close=800)
    sue_belief.set_l1_keg(place_keg)
    place_rope = sue_belief.make_l1_rope(place_str)
    sue_belief.add_fact(
        fact_context=place_rope, fact_state=place_rope, fact_lower=5, fact_upper=10
    )
    print(f"When one ranged fact added {sue_belief.kegroot.factunits=}")
    assert len(sue_belief.kegroot.factunits) == 2

    # THEN
    assert len(sue_belief._get_rangeroot_factunits()) == 2

    # WHEN one non-ranged_fact added
    mood = "mood_x"
    sue_belief.set_l1_keg(kegunit_shop(mood))
    m_rope = sue_belief.make_l1_rope(mood)
    sue_belief.add_fact(fact_context=m_rope, fact_state=m_rope)
    print(f"When one non-ranged_fact added {sue_belief.kegroot.factunits=}")
    assert len(sue_belief.kegroot.factunits) == 3

    # THEN
    assert len(sue_belief._get_rangeroot_factunits()) == 2


def test_BeliefUnit_get_rangeroot_factunits_ReturnsObj_Scenario1():
    # ESTABLISH a two ranged facts where one is "rangeroot" get_root_ranged_facts returns one "rangeroot" fact
    sue_belief = beliefunit_shop("Sue")
    ziet_str = "ziet"
    sue_belief.set_l1_keg(kegunit_shop(ziet_str, begin=0, close=140))
    ziet_rope = sue_belief.make_l1_rope(ziet_str)
    mood_x = "mood_x"
    sue_belief.set_l1_keg(kegunit_shop(mood_x))
    m_x_rope = sue_belief.make_l1_rope(mood_x)
    happy = "happy"
    sad = "Sad"
    sue_belief.set_keg_obj(kegunit_shop(happy), parent_rope=m_x_rope)
    sue_belief.set_keg_obj(kegunit_shop(sad), parent_rope=m_x_rope)
    sue_belief.add_fact(
        fact_context=ziet_rope, fact_state=ziet_rope, fact_lower=5, fact_upper=10
    )
    sue_belief.add_fact(
        fact_context=m_x_rope, fact_state=sue_belief.make_rope(m_x_rope, happy)
    )
    print(
        f"Establish a root ranged fact and non-range fact:\n{sue_belief.kegroot.factunits=}"
    )
    assert len(sue_belief.kegroot.factunits) == 2

    # WHEN / THEN
    assert len(sue_belief._get_rangeroot_factunits()) == 1
    assert sue_belief._get_rangeroot_factunits()[0].fact_context == ziet_rope


def test_BeliefUnit_set_fact_create_missing_kegs_Createsreason_contextAndFact():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    situations_str = "situations"
    situations_rope = sue_belief.make_l1_rope(situations_str)
    climate_str = "climate"
    climate_rope = sue_belief.make_rope(situations_rope, climate_str)
    assert sue_belief.kegroot.get_kid(situations_str) is None

    # WHEN
    sue_belief.add_fact(situations_rope, climate_rope, create_missing_kegs=True)

    # THEN
    assert sue_belief.kegroot.get_kid(situations_str) is not None
    assert sue_belief.get_keg_obj(situations_rope) is not None
    assert sue_belief.get_keg_obj(climate_rope) is not None
