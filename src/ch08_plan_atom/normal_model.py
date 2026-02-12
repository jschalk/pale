from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase


# Declare a base class
class Base(DeclarativeBase):
    pass


class PlanTable(Base):
    __tablename__ = "plan"
    keg_uid = Column(Integer, primary_key=True)
    max_tree_traverse = Column(Integer)
    credor_respect = Column(Float)
    debtor_respect = Column(Float)
    fund_pool = Column(Float)
    fund_grain = Column(Float)
    respect_grain = Column(Float)
    mana_grain = Column(Float)


class PartnerUnitTable(Base):
    __tablename__ = "partnerunit"
    keg_uid = Column(Integer, primary_key=True)
    partner_name = Column(String)
    partner_cred_lumen = Column(Float)
    partner_debt_lumen = Column(Float)


class MemberShipTable(Base):
    __tablename__ = "membership"
    keg_uid = Column(Integer, primary_key=True)
    group_title = Column(String)
    partner_name = Column(String)
    group_cred_lumen = Column(Float)
    group_debt_lumen = Column(Float)


class KegTable(Base):
    __tablename__ = "keg"
    keg_uid = Column(Integer, primary_key=True)
    keg_rope = Column(String)
    addin = Column(Float)
    begin = Column(Float)
    close = Column(Float)
    denom = Column(Integer)
    gogo_want = Column(Float)
    numor = Column(Integer)
    problem_bool = Column(Integer)
    morph = Column(Integer)
    star = Column(Integer)
    pledge = Column(Integer)
    stop_want = Column(Float)


class AwardUnitTable(Base):
    __tablename__ = "awardunit"
    keg_uid = Column(Integer, primary_key=True)
    awardee_title = Column(String)
    keg_rope = Column(String)
    give_force = Column(Float)
    take_force = Column(Float)


class ReasonTable(Base):
    __tablename__ = "reason"
    keg_uid = Column(Integer, primary_key=True)
    reason_context = Column(String)
    keg_rope = Column(String)
    active_requisite = Column(Integer)


class CaseTable(Base):
    __tablename__ = "case"
    keg_uid = Column(Integer, primary_key=True)
    reason_context = Column(String)
    reason_state = Column(String)
    keg_rope = Column(String)
    reason_divisor = Column(Integer)
    reason_upper = Column(Float)
    reason_lower = Column(Float)


class LaborLinkTable(Base):
    __tablename__ = "partyunit"
    keg_uid = Column(Integer, primary_key=True)
    party_title = Column(String)
    keg_rope = Column(String)
    solo = Column(Integer)


class HealerUnitTable(Base):
    __tablename__ = "healerunit"
    keg_uid = Column(Integer, primary_key=True)
    healer_name = Column(String)
    keg_rope = Column(String)


class FactTable(Base):
    __tablename__ = "fact"
    keg_uid = Column(Integer, primary_key=True)
    fact_context = Column(String)
    keg_rope = Column(String)
    fact_upper = Column(Float)
    fact_lower = Column(Float)
    fact_state = Column(String)
