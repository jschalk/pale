from platform import system as platform_system
from pytest import raises as pytest_raises
from src.ch00_py.file_toolbox import create_path
from src.ch04_rope._ref.ch04_env import get_temp_dir
from src.ch04_rope._ref.ch04_semantic_types import default_knot_if_None
from src.ch04_rope.rope import (
    LassoUnit,
    RopeTerm,
    all_ropes_between,
    create_rope,
    create_rope_from_labels,
    default_knot_if_None,
    find_replace_rope_key_dict,
    get_all_rope_labels,
    get_ancestor_ropes,
    get_default_rope,
    get_first_label_from_rope,
    get_forefather_ropes,
    get_parent_rope,
    get_tail_label,
    is_heir_rope,
    is_labelterm,
    is_sub_rope,
    lassounit_shop,
    rebuild_rope,
    remove_knot_ends,
    replace_knot,
    rope_is_valid_dir_path,
    to_rope,
    validate_labelterm,
)
from src.ref.keywords import Ch04Keywords as kw, ExampleStrs as exx


def test_LassoUnit_Exists():
    # ESTABLISH / WHEN
    x_lasso = LassoUnit()

    # THEN
    assert not x_lasso.rope
    assert not x_lasso.knot
    assert set(x_lasso.__dict__.keys()) == {"rope", kw.knot}


def test_lassounit_shop_ReturnsObj_Scenario0_WithoutParameters():
    # ESTABLISH / WHEN
    x_lasso = lassounit_shop()

    # THEN
    assert x_lasso.rope == get_default_rope()
    assert x_lasso.knot == default_knot_if_None()


def test_lassounit_shop_ReturnsObj_Scenario1_WithParameters():
    # ESTABLISH
    slash_knot = "/"
    casa_rope = create_rope(exx.sue, exx.casa, slash_knot)

    # WHEN
    casa_lasso = lassounit_shop(casa_rope, slash_knot)

    # THEN
    assert casa_lasso.rope == casa_rope
    assert casa_lasso.knot == slash_knot


def test_lassounit_shop_ReturnsObj_Scenario2_RaisesErrorIfKnotNotAtPostionZeroOf_parent_rope():
    # ESTABLISH
    tulip_str = "tulip"
    semicolon_knot = ";"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        lassounit_shop(tulip_str, semicolon_knot)
    exception_str = (
        f"Rope '{tulip_str}' must have knot '{semicolon_knot}' at position 0 in string"
    )
    assert str(excinfo.value) == exception_str


def test_LassoUnit_make_path_ReturnsObj_Scenario0_SimpleRope():
    # ESTABLISH
    casa_rope = create_rope(exx.sue, exx.casa)
    casa_lasso = lassounit_shop(casa_rope)

    # WHEN
    casa_path = casa_lasso.make_path()

    # THEN
    assert casa_path
    expected_casa_path = create_path(exx.sue, exx.casa)
    assert casa_path == expected_casa_path
