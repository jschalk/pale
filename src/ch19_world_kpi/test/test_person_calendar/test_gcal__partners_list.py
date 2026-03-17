from src.ch07_person_logic.person_main import personunit_shop
from src.ch13_time.test._util.ch13_examples import Ch13ExampleStrs as wx
from src.ch19_world_kpi.gcalendar import gcal_readable_percent, get_gcal_partners_str
from src.ref.keywords import Ch19Keywords as kw, ExampleStrs as exx


def test_get_gcal_partners_str_ReturnsObj_Scenario1_TwoPartners():
    # ESTABLISH
    bob_person = personunit_shop(wx.Bob, wx.root_rope)
    bob_person.add_partnerunit(exx.bob, 2)
    bob_person.add_partnerunit(exx.sue, 1)
    casa_rope = bob_person.make_l1_rope(exx.casa)
    clean_rope = bob_person.make_rope(casa_rope, exx.clean)
    bob_person.add_plan(clean_rope, 1, pledge=True)
    bob_person.conpute()

    # WHEN
    gcal_partners_str = get_gcal_partners_str(bob_person)

    # THEN
    assert gcal_partners_str
    expected_gcal_partners_str = f"""Person Partners
16.67% {exx.bob}
-16.67% {exx.sue}"""
    assert gcal_partners_str == expected_gcal_partners_str


def test_get_gcal_partners_str_ReturnsObj_Scenario2_TwoPartnersCorrectOrder():
    # ESTABLISH
    bob_person = personunit_shop(wx.Bob, wx.root_rope)
    bob_person.add_partnerunit(exx.bob, 1)
    bob_person.add_partnerunit(exx.sue, 2)
    casa_rope = bob_person.make_l1_rope(exx.casa)
    clean_rope = bob_person.make_rope(casa_rope, exx.clean)
    bob_person.add_plan(clean_rope, 1, pledge=True)
    bob_person.conpute()

    # WHEN
    gcal_partners_str = get_gcal_partners_str(bob_person)

    # THEN
    assert gcal_partners_str
    expected_gcal_partners_str = f"""Person Partners
16.67% {exx.sue}
-16.67% {exx.bob}"""
    assert gcal_partners_str == expected_gcal_partners_str
