from src.ch07_person_logic.person_main import personunit_shop
from src.ch08_person_atom.atom_main import personatom_shop
from src.ch09_person_lesson.delta import persondelta_shop
from src.ch09_person_lesson.legible import create_legible_list
from src.ref.keywords import Ch09Keywords as kw, ExampleStrs as exx


def test_create_legible_list_ReturnsObj_partnerunit_INSERT():
    # ESTABLISH
    dimen = kw.person_partnerunit
    partner_cred_lumen_value = 81
    partner_debt_lumen_value = 43
    yao_personatom = personatom_shop(dimen, kw.INSERT)
    yao_personatom.set_arg(kw.partner_name, exx.yao)
    yao_personatom.set_arg(kw.partner_cred_lumen, partner_cred_lumen_value)
    yao_personatom.set_arg(kw.partner_debt_lumen, partner_debt_lumen_value)
    # print(f"{yao_personatom=}")
    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(yao_personatom)
    sue_person = personunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_persondelta, sue_person)

    # THEN
    x_str = f"{exx.yao} was added with {partner_cred_lumen_value} score credit and {partner_debt_lumen_value} score debt"
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_partnerunit_INSERT_score():
    # ESTABLISH
    dimen = kw.person_partnerunit
    partner_cred_lumen_value = 81
    partner_debt_lumen_value = 43
    yao_personatom = personatom_shop(dimen, kw.INSERT)
    yao_personatom.set_arg(kw.partner_name, exx.yao)
    yao_personatom.set_arg(kw.partner_cred_lumen, partner_cred_lumen_value)
    yao_personatom.set_arg(kw.partner_debt_lumen, partner_debt_lumen_value)
    # print(f"{yao_personatom=}")
    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(yao_personatom)
    sue_person = personunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_persondelta, sue_person)

    # THEN
    x_str = f"{exx.yao} was added with {partner_cred_lumen_value} score credit and {partner_debt_lumen_value} score debt"
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_partnerunit_UPDATE_partner_cred_lumen_partner_debt_lumen():
    # ESTABLISH
    dimen = kw.person_partnerunit
    partner_cred_lumen_value = 81
    partner_debt_lumen_value = 43
    yao_personatom = personatom_shop(dimen, kw.UPDATE)
    yao_personatom.set_arg(kw.partner_name, exx.yao)
    yao_personatom.set_arg(kw.partner_cred_lumen, partner_cred_lumen_value)
    yao_personatom.set_arg(kw.partner_debt_lumen, partner_debt_lumen_value)
    # print(f"{yao_personatom=}")
    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(yao_personatom)
    sue_person = personunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_persondelta, sue_person)

    # THEN
    x_str = f"{exx.yao} now has {partner_cred_lumen_value} score credit and {partner_debt_lumen_value} score debt."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_partnerunit_UPDATE_partner_cred_lumen():
    # ESTABLISH
    dimen = kw.person_partnerunit
    partner_cred_lumen_value = 81
    yao_personatom = personatom_shop(dimen, kw.UPDATE)
    yao_personatom.set_arg(kw.partner_name, exx.yao)
    yao_personatom.set_arg(kw.partner_cred_lumen, partner_cred_lumen_value)
    # print(f"{yao_personatom=}")
    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(yao_personatom)
    sue_person = personunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_persondelta, sue_person)

    # THEN
    x_str = f"{exx.yao} now has {partner_cred_lumen_value} score credit."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_partnerunit_UPDATE_partner_debt_lumen():
    # ESTABLISH
    dimen = kw.person_partnerunit
    partner_debt_lumen_value = 43
    yao_personatom = personatom_shop(dimen, kw.UPDATE)
    yao_personatom.set_arg(kw.partner_name, exx.yao)
    yao_personatom.set_arg(kw.partner_debt_lumen, partner_debt_lumen_value)
    # print(f"{yao_personatom=}")
    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(yao_personatom)
    sue_person = personunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_persondelta, sue_person)

    # THEN
    x_str = f"{exx.yao} now has {partner_debt_lumen_value} score debt."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_partnerunit_DELETE():
    # ESTABLISH
    dimen = kw.person_partnerunit
    yao_personatom = personatom_shop(dimen, kw.DELETE)
    yao_personatom.set_arg(kw.partner_name, exx.yao)
    # print(f"{yao_personatom=}")
    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(yao_personatom)
    sue_person = personunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_persondelta, sue_person)

    # THEN
    x_str = f"{exx.yao} was removed from score partners."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
