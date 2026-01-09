from src.ch03_voice.voice import voiceunit_shop
from src.ch08_plan_atom.atom_main import PlanAtom, planatom_shop
from src.ref.keywords import Ch08Keywords as kw, ExampleStrs as exx


def test_PlanAtom_Exists():
    # ESTABLISH / WHEN
    x_planatom = PlanAtom()

    # THEN
    assert not x_planatom.dimen
    assert not x_planatom.crud_str
    assert not x_planatom.jkeys
    assert not x_planatom.jvalues
    assert not x_planatom.atom_order


def test_planatom_shop_ReturnsObj():
    # ESTABLISH
    bob_voice_cred_lumen = 55
    bob_voice_debt_lumen = 66
    bob_voiceunit = voiceunit_shop(exx.bob, bob_voice_cred_lumen, bob_voice_debt_lumen)
    cw_str = "_voice_cred_lumen"
    dw_str = "_voice_debt_lumen"
    bob_required_dict = {kw.voice_name: "huh"}
    bob_optional_dict = {cw_str: bob_voiceunit.to_dict().get(cw_str)}
    bob_optional_dict[dw_str] = bob_voiceunit.to_dict().get(dw_str)
    voiceunit_str = kw.plan_voiceunit

    # WHEN
    x_planatom = planatom_shop(
        dimen=voiceunit_str,
        crud_str=kw.INSERT,
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )

    # THEN
    print(f"{x_planatom=}")
    assert x_planatom.dimen == voiceunit_str
    assert x_planatom.crud_str == kw.INSERT
    assert x_planatom.jkeys == bob_required_dict
    assert x_planatom.jvalues == bob_optional_dict


def test_PlanAtom_set_jkey_SetsAttr():
    # ESTABLISH
    voiceunit_str = kw.plan_voiceunit
    voiceunit_planatom = planatom_shop(voiceunit_str, kw.INSERT)
    assert voiceunit_planatom.jkeys == {}

    # WHEN
    voiceunit_planatom.set_jkey(x_key=kw.voice_name, x_value=exx.bob)

    # THEN
    assert voiceunit_planatom.jkeys == {kw.voice_name: exx.bob}


def test_PlanAtom_set_jvalue_SetsAttr():
    # ESTABLISH
    voiceunit_str = kw.plan_voiceunit
    voiceunit_planatom = planatom_shop(voiceunit_str, kw.INSERT)
    assert voiceunit_planatom.jvalues == {}

    # WHEN
    voiceunit_planatom.set_jvalue(x_key=kw.voice_name, x_value=exx.bob)

    # THEN
    assert voiceunit_planatom.jvalues == {kw.voice_name: exx.bob}


def test_PlanAtom_get_value_ReturnsObj_Scenario0():
    # ESTABLISH
    voiceunit_str = kw.plan_voiceunit
    voiceunit_planatom = planatom_shop(voiceunit_str, kw.INSERT)
    voiceunit_planatom.set_jkey(x_key=kw.voice_name, x_value=exx.bob)

    # WHEN / THEN
    assert voiceunit_planatom.get_value(kw.voice_name) == exx.bob


def test_PlanAtom_is_jvalues_valid_ReturnsBoolean():
    # ESTABLISH / WHEN
    voiceunit_str = kw.plan_voiceunit
    bob_insert_planatom = planatom_shop(voiceunit_str, crud_str=kw.INSERT)
    assert bob_insert_planatom.is_jvalues_valid()

    # WHEN
    bob_insert_planatom.set_jvalue(kw.voice_cred_lumen, 55)
    # THEN
    assert len(bob_insert_planatom.jvalues) == 1
    assert bob_insert_planatom.is_jvalues_valid()

    # WHEN
    bob_insert_planatom.set_jvalue(kw.voice_debt_lumen, 66)
    # THEN
    assert len(bob_insert_planatom.jvalues) == 2
    assert bob_insert_planatom.is_jvalues_valid()

    # WHEN
    bob_insert_planatom.set_jvalue("x_x_x", 77)
    # THEN
    assert len(bob_insert_planatom.jvalues) == 3
    assert bob_insert_planatom.is_jvalues_valid() is False


def test_PlanAtom_is_valid_ReturnsBoolean_VoiceUnit_INSERT():
    # ESTABLISH
    bob_voice_cred_lumen = 55
    bob_voice_debt_lumen = 66
    bob_voiceunit = voiceunit_shop(exx.bob, bob_voice_cred_lumen, bob_voice_debt_lumen)
    voiceunit_str = kw.plan_voiceunit

    # WHEN
    bob_insert_planatom = planatom_shop(voiceunit_str, crud_str=kw.INSERT)

    # THEN
    assert bob_insert_planatom.is_jkeys_valid() is False
    assert bob_insert_planatom.is_jvalues_valid()
    assert bob_insert_planatom.is_valid() is False

    # WHEN
    bob_insert_planatom.set_jvalue("x_x_x", 12)

    # THEN
    assert bob_insert_planatom.is_jkeys_valid() is False
    assert bob_insert_planatom.is_jvalues_valid() is False
    assert bob_insert_planatom.is_valid() is False

    # WHEN
    bob_insert_planatom.set_jkey(kw.voice_name, exx.bob)

    # THEN
    assert bob_insert_planatom.is_jkeys_valid()
    assert bob_insert_planatom.is_jvalues_valid() is False
    assert bob_insert_planatom.is_valid() is False

    # WHEN
    bob_insert_planatom.jvalues = {}
    cw_str = kw.voice_cred_lumen
    dw_str = kw.voice_debt_lumen
    bob_insert_planatom.set_jvalue(cw_str, bob_voiceunit.to_dict().get(cw_str))
    bob_insert_planatom.set_jvalue(dw_str, bob_voiceunit.to_dict().get(dw_str))

    # THEN
    assert bob_insert_planatom.is_jkeys_valid()
    assert bob_insert_planatom.is_jvalues_valid()
    assert bob_insert_planatom.is_valid()

    # WHEN
    bob_insert_planatom.crud_str = None

    # THEN
    assert bob_insert_planatom.is_jkeys_valid() is False
    assert bob_insert_planatom.is_valid() is False

    # WHEN
    bob_insert_planatom.crud_str = kw.INSERT

    # THEN
    assert bob_insert_planatom.is_jkeys_valid()
    assert bob_insert_planatom.is_valid()


def test_PlanAtom_get_value_ReturnsObj_Scenario1():
    # ESTABLISH
    bob_voice_cred_lumen = 55
    bob_voice_debt_lumen = 66
    bob_voiceunit = voiceunit_shop(exx.bob, bob_voice_cred_lumen, bob_voice_debt_lumen)
    voiceunit_str = kw.plan_voiceunit
    bob_insert_planatom = planatom_shop(voiceunit_str, kw.INSERT)
    cw_str = kw.voice_cred_lumen
    dw_str = kw.voice_debt_lumen
    print(f"{bob_voiceunit.to_dict()=}")
    # bob_voiceunit_dict = {kw.voice_name: bob_voiceunit.to_dict().get(kw.voice_name)}
    # print(f"{bob_voiceunit_dict=}")
    bob_insert_planatom.set_jkey(kw.voice_name, exx.bob)
    bob_insert_planatom.set_jvalue(cw_str, bob_voiceunit.to_dict().get(cw_str))
    bob_insert_planatom.set_jvalue(dw_str, bob_voiceunit.to_dict().get(dw_str))
    assert bob_insert_planatom.is_valid()

    # WHEN / THEN
    assert bob_insert_planatom.get_value(cw_str) == bob_voice_cred_lumen
    assert bob_insert_planatom.get_value(dw_str) == bob_voice_debt_lumen


def test_PlanAtom_is_valid_ReturnsBoolean_VoiceUnit_DELETE():
    # ESTABLISH
    voiceunit_str = kw.plan_voiceunit
    delete_str = kw.DELETE

    # WHEN
    bob_delete_planatom = planatom_shop(voiceunit_str, crud_str=delete_str)

    # THEN
    assert bob_delete_planatom.is_jkeys_valid() is False
    assert bob_delete_planatom.is_valid() is False

    # WHEN
    bob_delete_planatom.set_jkey(kw.voice_name, exx.bob)

    # THEN
    assert bob_delete_planatom.is_jkeys_valid()
    assert bob_delete_planatom.is_valid()


def test_PlanAtom_is_valid_ReturnsBoolean_planunit():
    # ESTABLISH / WHEN
    bob_update_planatom = planatom_shop(kw.planunit, kw.INSERT)

    # THEN
    assert bob_update_planatom.is_jkeys_valid()
    assert bob_update_planatom.is_valid() is False

    # WHEN
    bob_update_planatom.set_jvalue(kw.max_tree_traverse, 14)

    # THEN
    assert bob_update_planatom.is_jkeys_valid()
    assert bob_update_planatom.is_valid()


def test_PlanAtom_set_atom_order_SetsAttr():
    # ESTABLISH
    bob_voice_cred_lumen = 55
    bob_voice_debt_lumen = 66
    voiceunit_str = kw.plan_voiceunit
    bob_insert_planatom = planatom_shop(voiceunit_str, kw.INSERT)
    cw_str = kw.voice_cred_lumen
    dw_str = kw.voice_debt_lumen
    bob_insert_planatom.set_jkey(kw.voice_name, exx.bob)
    bob_insert_planatom.set_jvalue(cw_str, bob_voice_cred_lumen)
    bob_insert_planatom.set_jvalue(dw_str, bob_voice_debt_lumen)
    assert bob_insert_planatom.is_valid()

    # WHEN / THEN
    assert bob_insert_planatom.get_value(cw_str) == bob_voice_cred_lumen
    assert bob_insert_planatom.get_value(dw_str) == bob_voice_debt_lumen


def test_PlanAtom_set_arg_SetsAny_jkey_jvalue():
    # ESTABLISH
    bob_voice_cred_lumen = 55
    bob_voice_debt_lumen = 66
    voiceunit_str = kw.plan_voiceunit
    bob_insert_planatom = planatom_shop(voiceunit_str, kw.INSERT)
    cw_str = kw.voice_cred_lumen
    dw_str = kw.voice_debt_lumen

    # WHEN
    bob_insert_planatom.set_arg(kw.voice_name, exx.bob)
    bob_insert_planatom.set_arg(cw_str, bob_voice_cred_lumen)
    bob_insert_planatom.set_arg(dw_str, bob_voice_debt_lumen)

    # THEN
    assert bob_insert_planatom.get_value(kw.voice_name) == exx.bob
    assert bob_insert_planatom.get_value(cw_str) == bob_voice_cred_lumen
    assert bob_insert_planatom.get_value(dw_str) == bob_voice_debt_lumen
    assert bob_insert_planatom.get_value(kw.voice_name) == exx.bob
    assert bob_insert_planatom.is_valid()


def test_PlanAtom_get_nesting_order_args_ReturnsObj_plan_voiceunit():
    # ESTABLISH
    sue_insert_planatom = planatom_shop(kw.plan_voiceunit, kw.INSERT)
    sue_insert_planatom.set_arg(kw.voice_name, exx.sue)
    print(f"{sue_insert_planatom.jkeys=}")

    # WHEN / THEN
    ordered_jkeys = [exx.sue]
    assert sue_insert_planatom.get_nesting_order_args() == ordered_jkeys


def test_PlanAtom_get_nesting_order_args_ReturnsObj_plan_voice_membership():
    # ESTABLISH
    iowa_str = ";Iowa"
    sue_insert_planatom = planatom_shop(kw.plan_voice_membership, kw.INSERT)
    sue_insert_planatom.set_arg(kw.group_title, iowa_str)
    sue_insert_planatom.set_arg(kw.voice_name, exx.sue)
    print(f"{sue_insert_planatom.jkeys=}")

    # WHEN / THEN
    ordered_jkeys = [exx.sue, iowa_str]
    assert sue_insert_planatom.get_nesting_order_args() == ordered_jkeys
