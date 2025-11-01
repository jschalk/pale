# from src.ch15_forge.map_epoch import epochforge_shop
# from src.ref.keywords import ExampleStrs as exx


# def test_ForgeUnit_set_epochforge_SetsAttr():
#     # ESTABLISH
#     sue_otx_epoch_length = None
#     sue_inx_epoch_diff = 6
#     sue_forgeunit = forgeunit_shop(exx.sue)
#     sue_epochforge = epochforge_shop(exx.sue, 0)
#     sue_epochforge.set_otx2inx(sue_otx_epoch_length, sue_inx_epoch_diff)
#     assert sue_forgeunit.epochforge != sue_epochforge

#     # WHEN
#     sue_forgeunit.set_epochforge(sue_epochforge)

#     # THEN
#     assert sue_forgeunit.epochforge == sue_epochforge


# def test_ForgeUnit_get_epochforge_ReturnsObj():
#     # ESTABLISH
#     sue_forgeunit = forgeunit_shop(exx.sue)
#     sue_spark_num = 31
#     sue_otx_time = 9
#     sue_inx_time = 6
#     sue_epoch_diff = sue_otx_time - sue_inx_time
#     otx2inx = {None: sue_epoch_diff}
#     static_sue_epochforge = epochforge_shop(exx.sue, sue_spark_num, otx2inx)
#     sue_forgeunit.set_epochforge(static_sue_epochforge)

#     # WHEN
#     gen_x_epochforge = sue_forgeunit.get_epochforge()

#     # THEN
#     assert gen_x_epochforge == static_sue_epochforge


# def test_ForgeUnit_get_inx_epoch_ReturnsObj():
#     # ESTABLISH
#     sue_forgeunit = forgeunit_shop(exx.sue)
#     sue_spark_num = 31
#     sue_epoch_diff = 10
#     otx2inx = {None: sue_epoch_diff}
#     static_sue_epochforge = epochforge_shop(exx.sue, sue_spark_num, otx2inx)
#     assert sue_forgeunit._get_otx_epoch_diff(None) is None

#     # WHEN
#     sue_forgeunit.set_epochforge(static_sue_epochforge)

#     # THEN
#     assert sue_forgeunit._get_otx_epoch_diff(None) == sue_epoch_diff


# def test_ForgeUnit_set_epoch_SetsAttr():
#     # ESTABLISH
#     sue_forgeunit = forgeunit_shop(exx.sue)
#     sue_epoch_diff = 10
#     assert sue_forgeunit._get_otx_epoch_diff(None) is None

#     # WHEN
#     sue_forgeunit.set_epoch(None, sue_epoch_diff)

#     # THEN
#     assert sue_forgeunit._get_otx_epoch_diff(None) == sue_epoch_diff


# def test_ForgeUnit_epoch_exists_ReturnsObj():
#     # ESTABLISH
#     sue_forgeunit = forgeunit_shop(exx.sue)
#     sue_epoch_diff = 10
#     assert not sue_forgeunit.epoch_exists(None)

#     # WHEN
#     sue_forgeunit.set_epoch(None, sue_epoch_diff)

#     # THEN
#     assert sue_forgeunit.epoch_exists(None)


# def test_ForgeUnit_del_epoch_ReturnsObj():
#     # ESTABLISH
#     sue_forgeunit = forgeunit_shop(exx.sue)
#     sue_epoch1_length = 111
#     sue_epoch1_diff = 11
#     sue_epoch2_length = 222
#     sue_epoch2_diff = 22
#     sue_forgeunit.set_epoch(sue_epoch1_length, sue_epoch1_diff)
#     sue_forgeunit.set_epoch(sue_epoch2_length, sue_epoch2_diff)
#     assert sue_forgeunit.epoch_exists(sue_epoch1_length)
#     assert sue_forgeunit.epoch_exists(sue_epoch2_length)

#     # WHEN
#     sue_forgeunit.del_epoch(sue_epoch1_length)

#     # THEN
#     assert not sue_forgeunit.epoch_exists(sue_epoch1_length)
#     assert sue_forgeunit.epoch_exists(sue_epoch2_length)


# from other file

# def test_ForgeUnit_set_otx2inx_SetsAttr_Scenario3_EpochTime():
#     # ESTABLISH
#     sue_forgeunit = forgeunit_shop(exx.sue)
#     sue_epoch_diff = 10
#     assert sue_forgeunit._get_otx_epoch_diff(None) is None

#     # WHEN
#     sue_forgeunit.set_otx2inx(kw.EpochTime, None, sue_epoch_diff)

#     # THEN
#     assert sue_forgeunit._get_otx_epoch_diff(None) == sue_epoch_diff


# def test_ForgeUnit_otx2inx_exists_ReturnsObj_Scenario1_EpochTime():
#     # ESTABLISH
#     sue_forgeunit = forgeunit_shop(exx.sue)
#     sue_epoch0_diff = 10
#     sue_epoch1_diff = 11
#     assert not sue_forgeunit.otx2inx_exists(kw.EpochTime, None, sue_epoch0_diff)
#     assert not sue_forgeunit.otx2inx_exists(kw.EpochTime, None, sue_epoch1_diff)

#     # WHEN
#     sue_forgeunit.set_otx2inx(kw.EpochTime, None, sue_epoch0_diff)

#     # THEN
#     assert sue_forgeunit.otx2inx_exists(kw.EpochTime, None, sue_epoch0_diff)
#     assert not sue_forgeunit.otx2inx_exists(kw.EpochTime, None, sue_epoch1_diff)


# def test_ForgeUnit_get_inx_value_ReturnsObj_Scenario1_EpochTerm():
#     # ESTABLISH
#     sue_epoch_diff = 10
#     sue_forgeunit = forgeunit_shop(exx.sue)
#     assert sue_forgeunit.get_inx_value(kw.EpochTime, None) != sue_epoch_diff

#     # WHEN
#     sue_forgeunit.set_otx2inx(kw.EpochTime, None, sue_epoch_diff)

#     # THEN
#     assert sue_forgeunit.get_inx_value(kw.EpochTime, None) == sue_epoch_diff


# def test_ForgeUnit_del_otx2inx_ReturnsObj_Scenario1_EpochTime():
#     # ESTABLISH
#     sue_forgeunit = forgeunit_shop(exx.sue)
#     sue_epoch0_diff = 10
#     sue_epoch1_diff = 11
#     sue_forgeunit.set_otx2inx(kw.EpochTime, None, sue_epoch0_diff)
#     assert sue_forgeunit.otx2inx_exists(kw.EpochTime, None, sue_epoch0_diff)
#     assert not sue_forgeunit.otx2inx_exists(kw.EpochTime, None, sue_epoch1_diff)

#     # WHEN
#     sue_forgeunit.del_otx2inx(kw.EpochTime, None)

#     # THEN
#     assert not sue_forgeunit.otx2inx_exists(kw.EpochTime, None, sue_epoch0_diff)
#     assert not sue_forgeunit.otx2inx_exists(kw.EpochTime, None, sue_epoch1_diff)
