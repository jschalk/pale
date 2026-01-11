from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from src.ch01_allot.allot import allot_scale
from src.ch04_rope.rope import get_ancestor_ropes, get_first_label_from_rope
from src.ch06_keg.keg import KegUnit
from src.ch07_plan_logic.plan_main import PersonUnit, PlanUnit
from src.ch09_plan_lesson.lesson_filehandler import LessonFileHandler, open_gut_file
from src.ch10_plan_listen._ref.ch10_semantic_types import PlanName, RopeTerm
from src.ch10_plan_listen.basis_plan import (
    create_empty_plan_from_plan,
    create_listen_basis,
)
from src.ch10_plan_listen.keep_tool import (
    get_duty_plan,
    get_perspective_plan,
    get_vision_plan,
    open_job_file,
    rj_speaker_plan,
    save_job_file,
    save_vision_plan,
    vision_file_exists,
)


class Missing_debtor_respectException(Exception):
    pass


def generate_perspective_agenda(perspective_plan: PlanUnit) -> list[KegUnit]:
    for x_factunit in perspective_plan.kegroot.factunits.values():
        x_factunit.set_fact_state_to_fact_context()
    return list(perspective_plan.get_agenda_dict().values())


def _ingest_perspective_agenda(listener: PlanUnit, agenda: list[KegUnit]) -> PlanUnit:
    debtor_respect = listener.debtor_respect
    ingest_list = generate_ingest_list(agenda, debtor_respect, listener.respect_grain)
    for ingest_kegunit in ingest_list:
        _ingest_single_kegunit(listener, ingest_kegunit)
    return listener


def _allocate_irrational_person_debt_lumen(
    listener: PlanUnit, speaker_plan_name: PlanName
) -> PlanUnit:
    speaker_personunit = listener.get_person(speaker_plan_name)
    speaker_person_debt_lumen = speaker_personunit.person_debt_lumen
    speaker_personunit.add_irrational_person_debt_lumen(speaker_person_debt_lumen)
    return listener


def _allocate_inallocable_person_debt_lumen(
    listener: PlanUnit, speaker_plan_name: PlanName
) -> PlanUnit:
    speaker_personunit = listener.get_person(speaker_plan_name)
    speaker_personunit.add_inallocable_person_debt_lumen(
        speaker_personunit.person_debt_lumen
    )
    return listener


def generate_ingest_list(
    keg_list: list[KegUnit], debtor_respect: float, respect_grain: float
) -> list[KegUnit]:
    keg_ledger = {x_keg.get_keg_rope(): x_keg.star for x_keg in keg_list}
    star_allot = allot_scale(keg_ledger, debtor_respect, respect_grain)
    for x_kegunit in keg_list:
        x_kegunit.star = star_allot.get(x_kegunit.get_keg_rope())
    return keg_list


def _ingest_single_kegunit(listener: PlanUnit, ingest_kegunit: KegUnit):
    star_data = _create_star_data(listener, ingest_kegunit.get_keg_rope())

    if listener.keg_exists(ingest_kegunit.get_keg_rope()) is False:
        x_parent_rope = ingest_kegunit.parent_rope
        listener.set_keg_obj(ingest_kegunit, x_parent_rope, create_missing_kegs=True)

    _add_and_replace_kegunit_stars(
        listener=listener,
        replace_star_list=star_data.replace_star_list,
        add_to_star_list=star_data.add_to_star_list,
        x_star=ingest_kegunit.star,
    )


@dataclass
class starReplaceOrAddData:
    add_to_star_list: list = None
    replace_star_list: list = None


def _create_star_data(listener: PlanUnit, x_rope: RopeTerm) -> list:
    star_data = starReplaceOrAddData()
    star_data.add_to_star_list = []
    star_data.replace_star_list = []
    ancestor_ropes = get_ancestor_ropes(x_rope, listener.knot)
    root_rope = get_first_label_from_rope(x_rope, listener.knot)
    for ancestor_rope in ancestor_ropes:
        if ancestor_rope != root_rope:
            if listener.keg_exists(ancestor_rope):
                star_data.add_to_star_list.append(ancestor_rope)
            else:
                star_data.replace_star_list.append(ancestor_rope)
    return star_data


def _add_and_replace_kegunit_stars(
    listener: PlanUnit,
    replace_star_list: list[RopeTerm],
    add_to_star_list: list[RopeTerm],
    x_star: float,
) -> None:
    for keg_rope in replace_star_list:
        listener.edit_keg_attr(keg_rope, star=x_star)
    for keg_rope in add_to_star_list:
        x_kegunit = listener.get_keg_obj(keg_rope)
        x_kegunit.star += x_star


def get_debtors_roll(x_duty: PlanUnit) -> list[PersonUnit]:
    return [
        x_personunit
        for x_personunit in x_duty.persons.values()
        if x_personunit.person_debt_lumen != 0
    ]


def get_ordered_debtors_roll(x_plan: PlanUnit) -> list[PersonUnit]:
    persons_ordered_list = get_debtors_roll(x_plan)
    persons_ordered_list.sort(
        key=lambda x: (x.person_debt_lumen, x.person_name), reverse=True
    )
    return persons_ordered_list


def migrate_all_facts(src_listener: PlanUnit, dst_listener: PlanUnit):
    for x_factunit in src_listener.kegroot.factunits.values():
        fact_context_rope = x_factunit.fact_context
        fact_state_rope = x_factunit.fact_state
        if dst_listener.keg_exists(fact_context_rope) is False:
            reason_context_keg = src_listener.get_keg_obj(fact_context_rope)
            dst_listener.set_keg_obj(reason_context_keg, reason_context_keg.parent_rope)
        if dst_listener.keg_exists(fact_state_rope) is False:
            fact_state_keg = src_listener.get_keg_obj(fact_state_rope)
            dst_listener.set_keg_obj(fact_state_keg, fact_state_keg.parent_rope)
        dst_listener.add_fact(fact_context_rope, fact_state_rope)


def listen_to_speaker_fact(
    listener: PlanUnit,
    speaker: PlanUnit,
    missing_fact_reason_contexts: list[RopeTerm] = None,
) -> PlanUnit:
    if missing_fact_reason_contexts is None:
        missing_fact_reason_contexts = list(listener.get_missing_fact_reason_contexts())
    for missing_fact_reason_context in missing_fact_reason_contexts:
        x_factunit = speaker.get_fact(missing_fact_reason_context)
        if x_factunit is not None:
            listener.add_fact(
                fact_context=x_factunit.fact_context,
                fact_state=x_factunit.fact_state,
                fact_lower=x_factunit.fact_lower,
                fact_upper=x_factunit.fact_upper,
                create_missing_kegs=True,
            )


def listen_to_speaker_agenda(listener: PlanUnit, speaker: PlanUnit) -> PlanUnit:
    if listener.person_exists(speaker.plan_name) is False:
        raise Missing_debtor_respectException(
            f"listener '{listener.plan_name}' plan is assumed to have {speaker.plan_name} personunit."
        )
    perspective_plan = get_perspective_plan(speaker, listener.plan_name)
    if perspective_plan.rational is False:
        return _allocate_irrational_person_debt_lumen(listener, speaker.plan_name)
    if listener.debtor_respect is None:
        return _allocate_inallocable_person_debt_lumen(listener, speaker.plan_name)
    if listener.plan_name != speaker.plan_name:
        agenda = generate_perspective_agenda(perspective_plan)
    else:
        agenda = list(perspective_plan.get_all_pledges().values())
    if len(agenda) == 0:
        return _allocate_inallocable_person_debt_lumen(listener, speaker.plan_name)
    return _ingest_perspective_agenda(listener, agenda)


def listen_to_agendas_create_init_job_from_guts(
    moment_mstr_dir: str, listener_job: PlanUnit
):
    moment_label = listener_job.moment_label
    for x_personunit in get_ordered_debtors_roll(listener_job):
        speaker_id = x_personunit.person_name
        speaker_gut = open_gut_file(moment_mstr_dir, moment_label, speaker_id)
        if speaker_gut is None:
            speaker_gut = create_empty_plan_from_plan(listener_job, speaker_id)
        if speaker_gut:
            listen_to_speaker_agenda(listener_job, speaker_gut)


def listen_to_agendas_jobs_into_job(moment_mstr_dir: str, listener_job: PlanUnit):
    moment_label = listener_job.moment_label
    for x_personunit in get_ordered_debtors_roll(listener_job):
        speaker_id = x_personunit.person_name
        speaker_job = open_job_file(moment_mstr_dir, moment_label, speaker_id)
        if speaker_job is None:
            speaker_job = create_empty_plan_from_plan(listener_job, speaker_id)
        listen_to_speaker_agenda(listener_job, speaker_job)


def listen_to_agendas_duty_vision(
    listener_vision: PlanUnit,
    healer_lessonfilehandler: LessonFileHandler,
    healer_keep_rope: RopeTerm,
):
    listener_id = listener_vision.plan_name
    for x_personunit in get_ordered_debtors_roll(listener_vision):
        if x_personunit.person_name == listener_id:
            listener_duty = get_duty_plan(
                moment_mstr_dir=healer_lessonfilehandler.moment_mstr_dir,
                plan_name=healer_lessonfilehandler.plan_name,
                moment_label=healer_lessonfilehandler.moment_label,
                keep_rope=healer_keep_rope,
                knot=healer_lessonfilehandler.knot,
                duty_plan_name=listener_id,
            )
            listen_to_speaker_agenda(listener_vision, listener_duty)
        else:
            speaker_id = x_personunit.person_name
            healer_name = healer_lessonfilehandler.plan_name
            speaker_vision = rj_speaker_plan(
                healer_lessonfilehandler.moment_mstr_dir,
                healer_lessonfilehandler.moment_label,
                healer_keep_rope,
                healer_lessonfilehandler.knot,
                healer_name,
                speaker_id,
            )
            if speaker_vision is None:
                speaker_vision = create_empty_plan_from_plan(
                    listener_vision, speaker_id
                )
            listen_to_speaker_agenda(listener_vision, speaker_vision)


def listen_to_facts_duty_vision(
    new_vision: PlanUnit,
    healer_lessonfilehandler: LessonFileHandler,
    healer_keep_rope: RopeTerm,
):
    duty = get_duty_plan(
        moment_mstr_dir=healer_lessonfilehandler.moment_mstr_dir,
        plan_name=healer_lessonfilehandler.plan_name,
        moment_label=healer_lessonfilehandler.moment_label,
        keep_rope=healer_keep_rope,
        knot=healer_lessonfilehandler.knot,
        duty_plan_name=new_vision.plan_name,
    )
    migrate_all_facts(duty, new_vision)
    for x_personunit in get_ordered_debtors_roll(new_vision):
        if x_personunit.person_name != new_vision.plan_name:
            speaker_vision = get_vision_plan(
                healer_lessonfilehandler.moment_mstr_dir,
                healer_lessonfilehandler.plan_name,
                healer_lessonfilehandler.moment_label,
                healer_keep_rope,
                healer_lessonfilehandler.knot,
                x_personunit.person_name,
            )
            if speaker_vision is not None:
                listen_to_speaker_fact(new_vision, speaker_vision)


def listen_to_facts_gut_job(moment_mstr_dir: str, new_job: PlanUnit):
    moment_label = new_job.moment_label
    old_job = open_job_file(moment_mstr_dir, moment_label, new_job.plan_name)
    for x_personunit in get_ordered_debtors_roll(old_job):
        speaker_id = x_personunit.person_name
        speaker_job = open_job_file(moment_mstr_dir, moment_label, speaker_id)
        if speaker_job is not None:
            listen_to_speaker_fact(new_job, speaker_job)


def listen_to_debtors_roll_jobs_into_job(
    moment_mstr_dir: str, moment_label: str, plan_name: PlanName
) -> PlanUnit:
    old_job = open_job_file(moment_mstr_dir, moment_label, plan_name)
    new_job = create_listen_basis(old_job)
    if old_job.debtor_respect is None:
        return new_job
    listen_to_agendas_jobs_into_job(moment_mstr_dir, new_job)
    listen_to_facts_gut_job(moment_mstr_dir, new_job)
    return new_job


def listen_to_debtors_roll_duty_vision(
    healer_lessonfilehandler: LessonFileHandler,
    listener_id: PlanName,
    healer_keep_rope: RopeTerm,
) -> PlanUnit:
    duty = get_duty_plan(
        moment_mstr_dir=healer_lessonfilehandler.moment_mstr_dir,
        plan_name=healer_lessonfilehandler.plan_name,
        moment_label=healer_lessonfilehandler.moment_label,
        keep_rope=healer_keep_rope,
        knot=healer_lessonfilehandler.knot,
        duty_plan_name=listener_id,
    )
    new_duty = create_listen_basis(duty)
    if duty.debtor_respect is None:
        return new_duty
    listen_to_agendas_duty_vision(new_duty, healer_lessonfilehandler, healer_keep_rope)
    listen_to_facts_duty_vision(new_duty, healer_lessonfilehandler, healer_keep_rope)
    return new_duty


def listen_to_plan_visions(
    listener_lessonfilehandler: LessonFileHandler, healer_keep_rope: RopeTerm
) -> None:
    gut = open_gut_file(
        listener_lessonfilehandler.moment_mstr_dir,
        listener_lessonfilehandler.moment_label,
        listener_lessonfilehandler.plan_name,
    )
    new_job = create_listen_basis(gut)
    pre_job_dict = new_job.to_dict()
    gut.cashout()
    new_job.cashout()

    for x_healer_name, keep_dict in gut._healers_dict.items():
        listener_id = listener_lessonfilehandler.plan_name
        healer_lessonfilehandler = copy_deepcopy(listener_lessonfilehandler)
        healer_lessonfilehandler.plan_name = x_healer_name
        fact_state_keep_visions_and_listen(
            listener_id,
            keep_dict,
            healer_lessonfilehandler,
            new_job,
            healer_keep_rope=healer_keep_rope,
        )

    if new_job.to_dict() == pre_job_dict:
        agenda = list(gut.get_agenda_dict().values())
        _ingest_perspective_agenda(new_job, agenda)
        listen_to_speaker_fact(new_job, gut)

    save_job_file(listener_lessonfilehandler.moment_mstr_dir, new_job)


def fact_state_keep_visions_and_listen(
    listener_id: PlanName,
    keep_dict: dict[RopeTerm],
    healer_lessonfilehandler: LessonFileHandler,
    new_job: PlanUnit,
    healer_keep_rope: RopeTerm,
):
    for keep_path in keep_dict:
        healer_keep_rope = keep_path
        fact_state_keep_vision_and_listen(
            listener_id, healer_lessonfilehandler, new_job, healer_keep_rope
        )


def fact_state_keep_vision_and_listen(
    listener_plan_name: PlanName,
    healer_lessonfilehandler: LessonFileHandler,
    new_job: PlanUnit,
    healer_keep_rope: RopeTerm,
):
    listener_id = listener_plan_name
    if vision_file_exists(
        healer_lessonfilehandler.moment_mstr_dir,
        healer_lessonfilehandler.plan_name,
        healer_lessonfilehandler.moment_label,
        healer_keep_rope,
        healer_lessonfilehandler.knot,
        listener_id,
    ):
        keep_vision = get_vision_plan(
            healer_lessonfilehandler.moment_mstr_dir,
            healer_lessonfilehandler.plan_name,
            healer_lessonfilehandler.moment_label,
            healer_keep_rope,
            healer_lessonfilehandler.knot,
            listener_id,
        )
    else:
        keep_vision = create_empty_plan_from_plan(new_job, new_job.plan_name)
    listen_to_vision_agenda(new_job, keep_vision)


def listen_to_vision_agenda(listener: PlanUnit, vision: PlanUnit):
    for x_keg in vision._keg_dict.values():
        if listener.keg_exists(x_keg.get_keg_rope()) is False:
            listener.set_keg_obj(x_keg, x_keg.parent_rope)
        if listener.get_fact(x_keg.get_keg_rope()) is False:
            listener.set_keg_obj(x_keg, x_keg.parent_rope)
    for x_fact_rope, x_fact_unit in vision.kegroot.factunits.items():
        listener.kegroot.set_factunit(x_fact_unit)
    listener.cashout()


def create_vision_file_from_duty_file(
    healer_lessonfilehandler: LessonFileHandler,
    plan_name: PlanName,
    healer_keep_rope: RopeTerm,
):
    x_vision = listen_to_debtors_roll_duty_vision(
        healer_lessonfilehandler,
        listener_id=plan_name,
        healer_keep_rope=healer_keep_rope,
    )
    save_vision_plan(
        healer_lessonfilehandler.moment_mstr_dir,
        healer_lessonfilehandler.plan_name,
        healer_lessonfilehandler.moment_label,
        healer_keep_rope,
        healer_lessonfilehandler.knot,
        x_vision,
    )
