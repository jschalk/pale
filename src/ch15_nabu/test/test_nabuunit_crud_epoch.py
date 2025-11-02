# from src.ch15_nabu.map_epoch import epochnabu_shop
# from src.ref.keywords import ExampleStrs as exx


# def test_NabuUnit_set_epochnabu_SetsAttr():
#     # ESTABLISH
#     sue_otx_epoch_length = None
#     sue_inx_epoch_diff = 6
#     sue_nabuunit = nabuunit_shop(exx.sue)
#     sue_epochnabu = epochnabu_shop(exx.sue, 0)
#     sue_epochnabu.set_otx2inx(sue_otx_epoch_length, sue_inx_epoch_diff)
#     assert sue_nabuunit.epochnabu != sue_epochnabu

#     # WHEN
#     sue_nabuunit.set_epochnabu(sue_epochnabu)

#     # THEN
#     assert sue_nabuunit.epochnabu == sue_epochnabu


# def test_NabuUnit_get_epochnabu_ReturnsObj():
#     # ESTABLISH
#     sue_nabuunit = nabuunit_shop(exx.sue)
#     sue_spark_num = 31
#     sue_otx_time = 9
#     sue_inx_time = 6
#     sue_epoch_diff = sue_otx_time - sue_inx_time
#     otx2inx = {None: sue_epoch_diff}
#     static_sue_epochnabu = epochnabu_shop(exx.sue, sue_spark_num, otx2inx)
#     sue_nabuunit.set_epochnabu(static_sue_epochnabu)

#     # WHEN
#     gen_x_epochnabu = sue_nabuunit.get_epochnabu()

#     # THEN
#     assert gen_x_epochnabu == static_sue_epochnabu


# def test_NabuUnit_get_inx_epoch_ReturnsObj():
#     # ESTABLISH
#     sue_nabuunit = nabuunit_shop(exx.sue)
#     sue_spark_num = 31
#     sue_epoch_diff = 10
#     otx2inx = {None: sue_epoch_diff}
#     static_sue_epochnabu = epochnabu_shop(exx.sue, sue_spark_num, otx2inx)
#     assert sue_nabuunit._get_otx_epoch_diff(None) is None

#     # WHEN
#     sue_nabuunit.set_epochnabu(static_sue_epochnabu)

#     # THEN
#     assert sue_nabuunit._get_otx_epoch_diff(None) == sue_epoch_diff


# def test_NabuUnit_set_epoch_SetsAttr():
#     # ESTABLISH
#     sue_nabuunit = nabuunit_shop(exx.sue)
#     sue_epoch_diff = 10
#     assert sue_nabuunit._get_otx_epoch_diff(None) is None

#     # WHEN
#     sue_nabuunit.set_epoch(None, sue_epoch_diff)

#     # THEN
#     assert sue_nabuunit._get_otx_epoch_diff(None) == sue_epoch_diff


# def test_NabuUnit_epoch_exists_ReturnsObj():
#     # ESTABLISH
#     sue_nabuunit = nabuunit_shop(exx.sue)
#     sue_epoch_diff = 10
#     assert not sue_nabuunit.epoch_exists(None)

#     # WHEN
#     sue_nabuunit.set_epoch(None, sue_epoch_diff)

#     # THEN
#     assert sue_nabuunit.epoch_exists(None)


# def test_NabuUnit_del_epoch_ReturnsObj():
#     # ESTABLISH
#     sue_nabuunit = nabuunit_shop(exx.sue)
#     sue_epoch1_length = 111
#     sue_epoch1_diff = 11
#     sue_epoch2_length = 222
#     sue_epoch2_diff = 22
#     sue_nabuunit.set_epoch(sue_epoch1_length, sue_epoch1_diff)
#     sue_nabuunit.set_epoch(sue_epoch2_length, sue_epoch2_diff)
#     assert sue_nabuunit.epoch_exists(sue_epoch1_length)
#     assert sue_nabuunit.epoch_exists(sue_epoch2_length)

#     # WHEN
#     sue_nabuunit.del_epoch(sue_epoch1_length)

#     # THEN
#     assert not sue_nabuunit.epoch_exists(sue_epoch1_length)
#     assert sue_nabuunit.epoch_exists(sue_epoch2_length)


# from other file

# def test_NabuUnit_set_otx2inx_SetsAttr_Scenario3_EpochTime():
#     # ESTABLISH
#     sue_nabuunit = nabuunit_shop(exx.sue)
#     sue_epoch_diff = 10
#     assert sue_nabuunit._get_otx_epoch_diff(None) is None

#     # WHEN
#     sue_nabuunit.set_otx2inx(kw.EpochTime, None, sue_epoch_diff)

#     # THEN
#     assert sue_nabuunit._get_otx_epoch_diff(None) == sue_epoch_diff


# def test_NabuUnit_otx2inx_exists_ReturnsObj_Scenario1_EpochTime():
#     # ESTABLISH
#     sue_nabuunit = nabuunit_shop(exx.sue)
#     sue_epoch0_diff = 10
#     sue_epoch1_diff = 11
#     assert not sue_nabuunit.otx2inx_exists(kw.EpochTime, None, sue_epoch0_diff)
#     assert not sue_nabuunit.otx2inx_exists(kw.EpochTime, None, sue_epoch1_diff)

#     # WHEN
#     sue_nabuunit.set_otx2inx(kw.EpochTime, None, sue_epoch0_diff)

#     # THEN
#     assert sue_nabuunit.otx2inx_exists(kw.EpochTime, None, sue_epoch0_diff)
#     assert not sue_nabuunit.otx2inx_exists(kw.EpochTime, None, sue_epoch1_diff)


# def test_NabuUnit_get_inx_value_ReturnsObj_Scenario1_EpochTerm():
#     # ESTABLISH
#     sue_epoch_diff = 10
#     sue_nabuunit = nabuunit_shop(exx.sue)
#     assert sue_nabuunit.get_inx_value(kw.EpochTime, None) != sue_epoch_diff

#     # WHEN
#     sue_nabuunit.set_otx2inx(kw.EpochTime, None, sue_epoch_diff)

#     # THEN
#     assert sue_nabuunit.get_inx_value(kw.EpochTime, None) == sue_epoch_diff


# def test_NabuUnit_del_otx2inx_ReturnsObj_Scenario1_EpochTime():
#     # ESTABLISH
#     sue_nabuunit = nabuunit_shop(exx.sue)
#     sue_epoch0_diff = 10
#     sue_epoch1_diff = 11
#     sue_nabuunit.set_otx2inx(kw.EpochTime, None, sue_epoch0_diff)
#     assert sue_nabuunit.otx2inx_exists(kw.EpochTime, None, sue_epoch0_diff)
#     assert not sue_nabuunit.otx2inx_exists(kw.EpochTime, None, sue_epoch1_diff)

#     # WHEN
#     sue_nabuunit.del_otx2inx(kw.EpochTime, None)

#     # THEN
#     assert not sue_nabuunit.otx2inx_exists(kw.EpochTime, None, sue_epoch0_diff)
#     assert not sue_nabuunit.otx2inx_exists(kw.EpochTime, None, sue_epoch1_diff)
