from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch08_plan_atom.atom_main import planatom_shop
from src.ch09_plan_lesson.delta import plandelta_shop
from src.ch09_plan_lesson.legible import create_legible_list
from src.ref.keywords import Ch09Keywords as kw, ExampleStrs as exx


def test_create_legible_list_ReturnsObj_voiceunit_INSERT():
    # ESTABLISH
    dimen = kw.plan_voiceunit
    voice_cred_lumen_value = 81
    voice_debt_lumen_value = 43
    yao_planatom = planatom_shop(dimen, kw.INSERT)
    yao_planatom.set_arg(kw.voice_name, exx.yao)
    yao_planatom.set_arg(kw.voice_cred_lumen, voice_cred_lumen_value)
    yao_planatom.set_arg(kw.voice_debt_lumen, voice_debt_lumen_value)
    # print(f"{yao_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(yao_planatom)
    sue_plan = planunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"{exx.yao} was added with {voice_cred_lumen_value} score credit and {voice_debt_lumen_value} score debt"
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_voiceunit_INSERT_score():
    # ESTABLISH
    dimen = kw.plan_voiceunit
    voice_cred_lumen_value = 81
    voice_debt_lumen_value = 43
    yao_planatom = planatom_shop(dimen, kw.INSERT)
    yao_planatom.set_arg(kw.voice_name, exx.yao)
    yao_planatom.set_arg(kw.voice_cred_lumen, voice_cred_lumen_value)
    yao_planatom.set_arg(kw.voice_debt_lumen, voice_debt_lumen_value)
    # print(f"{yao_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(yao_planatom)
    sue_plan = planunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"{exx.yao} was added with {voice_cred_lumen_value} score credit and {voice_debt_lumen_value} score debt"
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_voiceunit_UPDATE_voice_cred_lumen_voice_debt_lumen():
    # ESTABLISH
    dimen = kw.plan_voiceunit
    voice_cred_lumen_value = 81
    voice_debt_lumen_value = 43
    yao_planatom = planatom_shop(dimen, kw.UPDATE)
    yao_planatom.set_arg(kw.voice_name, exx.yao)
    yao_planatom.set_arg(kw.voice_cred_lumen, voice_cred_lumen_value)
    yao_planatom.set_arg(kw.voice_debt_lumen, voice_debt_lumen_value)
    # print(f"{yao_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(yao_planatom)
    sue_plan = planunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"{exx.yao} now has {voice_cred_lumen_value} score credit and {voice_debt_lumen_value} score debt."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_voiceunit_UPDATE_voice_cred_lumen():
    # ESTABLISH
    dimen = kw.plan_voiceunit
    voice_cred_lumen_value = 81
    yao_planatom = planatom_shop(dimen, kw.UPDATE)
    yao_planatom.set_arg(kw.voice_name, exx.yao)
    yao_planatom.set_arg(kw.voice_cred_lumen, voice_cred_lumen_value)
    # print(f"{yao_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(yao_planatom)
    sue_plan = planunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"{exx.yao} now has {voice_cred_lumen_value} score credit."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_voiceunit_UPDATE_voice_debt_lumen():
    # ESTABLISH
    dimen = kw.plan_voiceunit
    voice_debt_lumen_value = 43
    yao_planatom = planatom_shop(dimen, kw.UPDATE)
    yao_planatom.set_arg(kw.voice_name, exx.yao)
    yao_planatom.set_arg(kw.voice_debt_lumen, voice_debt_lumen_value)
    # print(f"{yao_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(yao_planatom)
    sue_plan = planunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"{exx.yao} now has {voice_debt_lumen_value} score debt."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_voiceunit_DELETE():
    # ESTABLISH
    dimen = kw.plan_voiceunit
    yao_planatom = planatom_shop(dimen, kw.DELETE)
    yao_planatom.set_arg(kw.voice_name, exx.yao)
    # print(f"{yao_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(yao_planatom)
    sue_plan = planunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"{exx.yao} was removed from score voices."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
