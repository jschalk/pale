from src.ch04_rope.rope import RopeTerm, create_rope_from_labels
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch12_keep._ref.ch12_semantic_types import PersonName, PlanName
from src.ch12_keep.rivercycle import get_patientledger
from src.ref.keywords import ExampleStrs as exx


def get_nation_texas_rope() -> RopeTerm:
    naton_str = "nation"
    usa_str = "usa"
    texas_str = "texas"
    return create_rope_from_labels([naton_str, usa_str, texas_str])


def example_yao_patientledger() -> dict[str, float]:
    yao_person_cred_lumen = 7
    bob_person_cred_lumen = 3
    zia_person_cred_lumen = 10
    yao_plan = planunit_shop(exx.yao)
    yao_plan.add_personunit(exx.yao, yao_person_cred_lumen)
    yao_plan.add_personunit(exx.bob, bob_person_cred_lumen)
    yao_plan.add_personunit(exx.zia, zia_person_cred_lumen)
    return get_patientledger(yao_plan)


def example_bob_patientledger() -> dict[str, float]:
    yao_person_cred_lumen = 1
    bob_person_cred_lumen = 7
    zia_person_cred_lumen = 42
    bob_plan = planunit_shop(exx.bob)
    bob_plan.add_personunit(exx.yao, yao_person_cred_lumen)
    bob_plan.add_personunit(exx.bob, bob_person_cred_lumen)
    bob_plan.add_personunit(exx.zia, zia_person_cred_lumen)
    return get_patientledger(bob_plan)


def example_zia_patientledger() -> dict[str, float]:
    yao_person_cred_lumen = 89
    bob_person_cred_lumen = 150
    zia_person_cred_lumen = 61
    zia_plan = planunit_shop(exx.zia)
    zia_plan.add_personunit(exx.yao, yao_person_cred_lumen)
    zia_plan.add_personunit(exx.bob, bob_person_cred_lumen)
    zia_plan.add_personunit(exx.zia, zia_person_cred_lumen)
    return get_patientledger(zia_plan)


def example_yao_bob_zia_patientledgers() -> dict[PlanName : dict[PersonName, float]]:
    return {
        exx.yao: example_yao_patientledger,
        exx.bob: example_bob_patientledger,
        exx.zia: example_zia_patientledger,
    }


def example_yao_bob_zia_need_dues() -> dict[PersonName, float]:
    yao_sum = sum(example_yao_patientledger().values())
    bob_sum = sum(example_bob_patientledger().values())
    zia_sum = sum(example_zia_patientledger().values())

    return {
        exx.yao: yao_sum - 60000,
        exx.bob: bob_sum - 500000,
        exx.zia: zia_sum - 4000,
    }
