# from src.ch15_ingress.map_epoch import epochingress_shop
# from src.ref.keywords import ExampleStrs as exx


# def test_IngressUnit_set_epochingress_SetsAttr():
#     # ESTABLISH
#     sue_otx_epoch_length = None
#     sue_inx_epoch_diff = 6
#     sue_ingressunit = ingressunit_shop(exx.sue)
#     sue_epochingress = epochingress_shop(exx.sue, 0)
#     sue_epochingress.set_otx2inx(sue_otx_epoch_length, sue_inx_epoch_diff)
#     assert sue_ingressunit.epochingress != sue_epochingress

#     # WHEN
#     sue_ingressunit.set_epochingress(sue_epochingress)

#     # THEN
#     assert sue_ingressunit.epochingress == sue_epochingress


# def test_IngressUnit_get_epochingress_ReturnsObj():
#     # ESTABLISH
#     sue_ingressunit = ingressunit_shop(exx.sue)
#     sue_spark_num = 31
#     sue_otx_time = 9
#     sue_inx_time = 6
#     sue_epoch_diff = sue_otx_time - sue_inx_time
#     otx2inx = {None: sue_epoch_diff}
#     static_sue_epochingress = epochingress_shop(exx.sue, sue_spark_num, otx2inx)
#     sue_ingressunit.set_epochingress(static_sue_epochingress)

#     # WHEN
#     gen_x_epochingress = sue_ingressunit.get_epochingress()

#     # THEN
#     assert gen_x_epochingress == static_sue_epochingress


# def test_IngressUnit_get_inx_epoch_ReturnsObj():
#     # ESTABLISH
#     sue_ingressunit = ingressunit_shop(exx.sue)
#     sue_spark_num = 31
#     sue_epoch_diff = 10
#     otx2inx = {None: sue_epoch_diff}
#     static_sue_epochingress = epochingress_shop(exx.sue, sue_spark_num, otx2inx)
#     assert sue_ingressunit._get_otx_epoch_diff(None) is None

#     # WHEN
#     sue_ingressunit.set_epochingress(static_sue_epochingress)

#     # THEN
#     assert sue_ingressunit._get_otx_epoch_diff(None) == sue_epoch_diff


# def test_IngressUnit_set_epoch_SetsAttr():
#     # ESTABLISH
#     sue_ingressunit = ingressunit_shop(exx.sue)
#     sue_epoch_diff = 10
#     assert sue_ingressunit._get_otx_epoch_diff(None) is None

#     # WHEN
#     sue_ingressunit.set_epoch(None, sue_epoch_diff)

#     # THEN
#     assert sue_ingressunit._get_otx_epoch_diff(None) == sue_epoch_diff


# def test_IngressUnit_epoch_exists_ReturnsObj():
#     # ESTABLISH
#     sue_ingressunit = ingressunit_shop(exx.sue)
#     sue_epoch_diff = 10
#     assert not sue_ingressunit.epoch_exists(None)

#     # WHEN
#     sue_ingressunit.set_epoch(None, sue_epoch_diff)

#     # THEN
#     assert sue_ingressunit.epoch_exists(None)


# def test_IngressUnit_del_epoch_ReturnsObj():
#     # ESTABLISH
#     sue_ingressunit = ingressunit_shop(exx.sue)
#     sue_epoch1_length = 111
#     sue_epoch1_diff = 11
#     sue_epoch2_length = 222
#     sue_epoch2_diff = 22
#     sue_ingressunit.set_epoch(sue_epoch1_length, sue_epoch1_diff)
#     sue_ingressunit.set_epoch(sue_epoch2_length, sue_epoch2_diff)
#     assert sue_ingressunit.epoch_exists(sue_epoch1_length)
#     assert sue_ingressunit.epoch_exists(sue_epoch2_length)

#     # WHEN
#     sue_ingressunit.del_epoch(sue_epoch1_length)

#     # THEN
#     assert not sue_ingressunit.epoch_exists(sue_epoch1_length)
#     assert sue_ingressunit.epoch_exists(sue_epoch2_length)


# from other file

# def test_IngressUnit_set_otx2inx_SetsAttr_Scenario3_EpochTime():
#     # ESTABLISH
#     sue_ingressunit = ingressunit_shop(exx.sue)
#     sue_epoch_diff = 10
#     assert sue_ingressunit._get_otx_epoch_diff(None) is None

#     # WHEN
#     sue_ingressunit.set_otx2inx(kw.EpochTime, None, sue_epoch_diff)

#     # THEN
#     assert sue_ingressunit._get_otx_epoch_diff(None) == sue_epoch_diff


# def test_IngressUnit_otx2inx_exists_ReturnsObj_Scenario1_EpochTime():
#     # ESTABLISH
#     sue_ingressunit = ingressunit_shop(exx.sue)
#     sue_epoch0_diff = 10
#     sue_epoch1_diff = 11
#     assert not sue_ingressunit.otx2inx_exists(kw.EpochTime, None, sue_epoch0_diff)
#     assert not sue_ingressunit.otx2inx_exists(kw.EpochTime, None, sue_epoch1_diff)

#     # WHEN
#     sue_ingressunit.set_otx2inx(kw.EpochTime, None, sue_epoch0_diff)

#     # THEN
#     assert sue_ingressunit.otx2inx_exists(kw.EpochTime, None, sue_epoch0_diff)
#     assert not sue_ingressunit.otx2inx_exists(kw.EpochTime, None, sue_epoch1_diff)


# def test_IngressUnit_get_inx_value_ReturnsObj_Scenario1_EpochTerm():
#     # ESTABLISH
#     sue_epoch_diff = 10
#     sue_ingressunit = ingressunit_shop(exx.sue)
#     assert sue_ingressunit.get_inx_value(kw.EpochTime, None) != sue_epoch_diff

#     # WHEN
#     sue_ingressunit.set_otx2inx(kw.EpochTime, None, sue_epoch_diff)

#     # THEN
#     assert sue_ingressunit.get_inx_value(kw.EpochTime, None) == sue_epoch_diff


# def test_IngressUnit_del_otx2inx_ReturnsObj_Scenario1_EpochTime():
#     # ESTABLISH
#     sue_ingressunit = ingressunit_shop(exx.sue)
#     sue_epoch0_diff = 10
#     sue_epoch1_diff = 11
#     sue_ingressunit.set_otx2inx(kw.EpochTime, None, sue_epoch0_diff)
#     assert sue_ingressunit.otx2inx_exists(kw.EpochTime, None, sue_epoch0_diff)
#     assert not sue_ingressunit.otx2inx_exists(kw.EpochTime, None, sue_epoch1_diff)

#     # WHEN
#     sue_ingressunit.del_otx2inx(kw.EpochTime, None)

#     # THEN
#     assert not sue_ingressunit.otx2inx_exists(kw.EpochTime, None, sue_epoch0_diff)
#     assert not sue_ingressunit.otx2inx_exists(kw.EpochTime, None, sue_epoch1_diff)
