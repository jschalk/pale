from src.ch16_rose.map import epochmap_shop
from src.ch16_rose.rose_main import roseunit_shop
from src.ref.keywords import ExampleStrs as exx


def test_RoseUnit_set_epochmap_SetsAttr():
    # ESTABLISH
    sue_otx_epoch_length = None
    sue_inx_epoch_diff = 6
    sue_roseunit = roseunit_shop(exx.sue)
    sue_epochmap = epochmap_shop(exx.sue, 0)
    sue_epochmap.set_otx2inx(sue_otx_epoch_length, sue_inx_epoch_diff)
    assert sue_roseunit.epochmap != sue_epochmap

    # WHEN
    sue_roseunit.set_epochmap(sue_epochmap)

    # THEN
    assert sue_roseunit.epochmap == sue_epochmap


def test_RoseUnit_get_epochmap_ReturnsObj():
    # ESTABLISH
    sue_roseunit = roseunit_shop(exx.sue)
    sue_spark_num = 31
    sue_otx_time = 9
    sue_inx_time = 6
    sue_epoch_diff = sue_otx_time - sue_inx_time
    otx2inx = {None: sue_epoch_diff}
    static_sue_epochmap = epochmap_shop(exx.sue, sue_spark_num, otx2inx)
    sue_roseunit.set_epochmap(static_sue_epochmap)

    # WHEN
    gen_x_epochmap = sue_roseunit.get_epochmap()

    # THEN
    assert gen_x_epochmap == static_sue_epochmap


def test_RoseUnit_get_inx_epoch_ReturnsObj():
    # ESTABLISH
    sue_roseunit = roseunit_shop(exx.sue)
    sue_spark_num = 31
    sue_epoch_diff = 10
    otx2inx = {None: sue_epoch_diff}
    static_sue_epochmap = epochmap_shop(exx.sue, sue_spark_num, otx2inx)
    assert sue_roseunit._get_otx_epoch_diff(None) is None

    # WHEN
    sue_roseunit.set_epochmap(static_sue_epochmap)

    # THEN
    assert sue_roseunit._get_otx_epoch_diff(None) == sue_epoch_diff


def test_RoseUnit_set_epoch_SetsAttr():
    # ESTABLISH
    sue_roseunit = roseunit_shop(exx.sue)
    sue_epoch_diff = 10
    assert sue_roseunit._get_otx_epoch_diff(None) is None

    # WHEN
    sue_roseunit.set_epoch(None, sue_epoch_diff)

    # THEN
    assert sue_roseunit._get_otx_epoch_diff(None) == sue_epoch_diff


def test_RoseUnit_epoch_exists_ReturnsObj():
    # ESTABLISH
    sue_roseunit = roseunit_shop(exx.sue)
    sue_epoch_diff = 10
    assert not sue_roseunit.epoch_exists(None)

    # WHEN
    sue_roseunit.set_epoch(None, sue_epoch_diff)

    # THEN
    assert sue_roseunit.epoch_exists(None)


def test_RoseUnit_del_epoch_ReturnsObj():
    # ESTABLISH
    sue_roseunit = roseunit_shop(exx.sue)
    sue_epoch1_length = 111
    sue_epoch1_diff = 11
    sue_epoch2_length = 222
    sue_epoch2_diff = 22
    sue_roseunit.set_epoch(sue_epoch1_length, sue_epoch1_diff)
    sue_roseunit.set_epoch(sue_epoch2_length, sue_epoch2_diff)
    assert sue_roseunit.epoch_exists(sue_epoch1_length)
    assert sue_roseunit.epoch_exists(sue_epoch2_length)

    # WHEN
    sue_roseunit.del_epoch(sue_epoch1_length)

    # THEN
    assert not sue_roseunit.epoch_exists(sue_epoch1_length)
    assert sue_roseunit.epoch_exists(sue_epoch2_length)
