from pytest import raises as pytest_raises
from src.ch03_person.group import membership_shop
from src.ch03_person.person import personunit_shop
from src.ref.keywords import ExampleStrs as exx


def test_PersonUnit_set_membership_SetsAttr_memberships():
    # ESTABLISH
    run_group_cred_lumen = 66
    run_group_debt_lumen = 85
    yao_personunit = personunit_shop(exx.yao)
    assert yao_personunit.memberships == {}

    # WHEN
    yao_personunit.set_membership(
        membership_shop(exx.run, run_group_cred_lumen, run_group_debt_lumen)
    )

    # THEN
    assert len(yao_personunit.memberships) == 1
    run_membership = yao_personunit.memberships.get(exx.run)
    assert run_membership.group_title == exx.run
    assert run_membership.group_cred_lumen == run_group_cred_lumen
    assert run_membership.group_debt_lumen == run_group_debt_lumen
    assert run_membership.person_name == exx.yao


def test_PersonUnit_set_membership_SetsMultipleAttr():
    # ESTABLISH
    fly_str = ";fly"
    run_membership = membership_shop(exx.run, group_cred_lumen=13, group_debt_lumen=7)
    fly_membership = membership_shop(fly_str, group_cred_lumen=23, group_debt_lumen=5)
    yao_personunit = personunit_shop(exx.yao)
    assert yao_personunit.memberships == {}

    # WHEN
    yao_personunit.set_membership(run_membership)
    yao_personunit.set_membership(fly_membership)

    # THEN
    yao_memberships = {
        run_membership.group_title: run_membership,
        fly_membership.group_title: fly_membership,
    }
    assert yao_personunit.memberships == yao_memberships


def test_PersonUnit_set_membership_RaisesErrorIf_group_titleIsPersonNameAndNotPersonUnit_person_name():
    # ESTABLISH
    yao_personunit = personunit_shop(exx.yao)
    bob_membership = membership_shop(exx.bob)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        yao_personunit.set_membership(bob_membership)

    # THEN
    assertion_fail_str = (
        f"PersonUnit with person_name='{exx.yao}' cannot have link to '{exx.bob}'."
    )
    assert str(excinfo.value) == assertion_fail_str


def test_PersonUnit_get_membership_ReturnsObj():
    # ESTABLISH
    fly_str = ";fly"
    yao_personunit = personunit_shop(exx.yao)
    yao_personunit.set_membership(membership_shop(exx.run, 13, 7))
    yao_personunit.set_membership(membership_shop(fly_str, 23, 5))

    # WHEN / THEN
    assert yao_personunit.get_membership(exx.run) is not None
    assert yao_personunit.get_membership(fly_str) is not None
    climb_str = ",climbers"
    assert yao_personunit.get_membership(climb_str) is None


def test_membership_exists_ReturnsObj():
    # ESTABLISH
    fly_str = ";fly"
    yao_personunit = personunit_shop(exx.yao)
    yao_personunit.set_membership(membership_shop(exx.run, 13, 7))
    yao_personunit.set_membership(membership_shop(fly_str, 23, 5))

    # WHEN / THEN
    assert yao_personunit.membership_exists(exx.run)
    assert yao_personunit.membership_exists(fly_str)
    climb_str = ",climbers"
    assert yao_personunit.membership_exists(climb_str) is False


def test_memberships_exist_ReturnsObj():
    # ESTABLISH
    fly_str = ";fly"
    yao_personunit = personunit_shop(exx.yao)
    assert not yao_personunit.memberships_exist()

    # WHEN
    yao_personunit.set_membership(membership_shop(exx.run))
    # THEN
    assert yao_personunit.memberships_exist()

    # WHEN
    yao_personunit.set_membership(membership_shop(fly_str))
    # THEN
    assert yao_personunit.memberships_exist()

    # WHEN
    yao_personunit.delete_membership(fly_str)
    # THEN
    assert yao_personunit.memberships_exist()

    # WHEN
    yao_personunit.delete_membership(exx.run)
    # THEN
    assert not yao_personunit.memberships_exist()


def test_PersonUnit_del_membership_SetsAttr():
    # ESTABLISH
    fly_str = ";fly"
    run_membership = membership_shop(exx.run)
    fly_membership = membership_shop(fly_str)
    yao_memberships = {
        run_membership.group_title: run_membership,
        fly_membership.group_title: fly_membership,
    }
    yao_personunit = personunit_shop(exx.yao)
    yao_personunit.set_membership(run_membership)
    yao_personunit.set_membership(fly_membership)
    assert len(yao_personunit.memberships) == 2
    assert yao_personunit.memberships == yao_memberships

    # WHEN
    yao_personunit.delete_membership(exx.run)

    # THEN
    assert len(yao_personunit.memberships) == 1
    assert yao_personunit.memberships.get(exx.run) is None


def test_PersonUnit_clear_memberships_SetsAttr():
    # ESTABLISH
    fly_str = ";fly"
    run_membership = membership_shop(exx.run)
    fly_membership = membership_shop(fly_str)
    yao_memberships = {
        run_membership.group_title: run_membership,
        fly_membership.group_title: fly_membership,
    }
    yao_personunit = personunit_shop(exx.yao)
    yao_personunit.set_membership(run_membership)
    yao_personunit.set_membership(fly_membership)
    assert len(yao_personunit.memberships) == 2
    assert yao_personunit.memberships == yao_memberships

    # WHEN
    yao_personunit.clear_memberships()

    # THEN
    assert len(yao_personunit.memberships) == 0
    assert yao_personunit.memberships.get(exx.run) is None


def test_PersonUnit_add_membership_SetsAttr():
    # ESTABLISH
    run_group_cred_lumen = 78
    run_group_debt_lumen = 99
    yao_personunit = personunit_shop(exx.yao)
    assert yao_personunit.get_membership(exx.run) is None

    # WHEN
    yao_personunit.add_membership(exx.run, run_group_cred_lumen, run_group_debt_lumen)

    # THEN
    assert yao_personunit.get_membership(exx.run) is not None
    run_membership = yao_personunit.get_membership(exx.run)
    assert run_membership.group_cred_lumen == run_group_cred_lumen
    assert run_membership.group_debt_lumen == run_group_debt_lumen


def test_PersonUnit_set_credor_pool_SetAttr():
    # ESTABLISH
    bob_personunit = personunit_shop(exx.bob)
    assert bob_personunit.credor_pool == 0

    # WHEN
    bob_credor_pool = 51
    bob_personunit.set_credor_pool(bob_credor_pool)

    # THEN
    assert bob_personunit.credor_pool == bob_credor_pool


def test_PersonUnit_set_debtor_pool_SetAttr():
    # ESTABLISH
    bob_personunit = personunit_shop(exx.bob)
    assert bob_personunit.debtor_pool == 0

    # WHEN
    bob_debtor_pool = 51
    bob_personunit.set_debtor_pool(bob_debtor_pool)

    # THEN
    assert bob_personunit.debtor_pool == bob_debtor_pool


def test_PersonUnit_set_credor_pool_Sets_memberships():
    # ESTABLISH
    ohio_str = ";Ohio"
    iowa_str = ";Iowa"
    sue_group_cred_lumen = 1
    yao_group_cred_lumen = 4
    bob_personunit = personunit_shop(exx.bob)
    bob_personunit.add_membership(ohio_str, sue_group_cred_lumen)
    bob_personunit.add_membership(iowa_str, yao_group_cred_lumen)
    assert bob_personunit.credor_pool == 0
    sue_membership = bob_personunit.get_membership(ohio_str)
    yao_membership = bob_personunit.get_membership(iowa_str)
    assert sue_membership.credor_pool == 0
    assert yao_membership.credor_pool == 0

    # WHEN
    bob_credor_pool = 51
    bob_personunit.set_credor_pool(bob_credor_pool)

    # THEN
    assert bob_personunit.credor_pool == bob_credor_pool
    assert sue_membership.credor_pool == 10
    assert yao_membership.credor_pool == 41


def test_PersonUnit_set_debtor_pool_Sets_memberships():
    # ESTABLISH
    ohio_str = ";Ohio"
    iowa_str = ";Iowa"
    sue_group_debt_lumen = 1
    yao_group_debt_lumen = 4
    bob_personunit = personunit_shop(exx.bob)
    bob_personunit.add_membership(ohio_str, 2, sue_group_debt_lumen)
    bob_personunit.add_membership(iowa_str, 2, yao_group_debt_lumen)
    assert bob_personunit.debtor_pool == 0
    sue_membership = bob_personunit.get_membership(ohio_str)
    yao_membership = bob_personunit.get_membership(iowa_str)
    assert sue_membership.debtor_pool == 0
    assert yao_membership.debtor_pool == 0

    # WHEN
    bob_debtor_pool = 54
    bob_personunit.set_debtor_pool(bob_debtor_pool)

    # THEN
    assert bob_personunit.debtor_pool == bob_debtor_pool
    assert sue_membership.debtor_pool == 11
    assert yao_membership.debtor_pool == 43
