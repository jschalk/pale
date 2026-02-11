from src.ch04_rope.rope import RopeTerm, create_rope, create_rope_from_labels
from src.ch08_plan_atom.atom_main import PlanAtom, planatom_shop
from src.ch09_plan_lesson._ref.ch09_semantic_types import LabelTerm, MomentRope
from src.ch09_plan_lesson.delta import PlanDelta, plandelta_shop
from src.ch09_plan_lesson.lasso import LassoUnit, lassounit_shop
from src.ch09_plan_lesson.lesson_main import LessonUnit, lessonunit_shop
from src.ref.keywords import Ch09Keywords as kw, ExampleStrs as exx


def get_ch09_example_moment_rope() -> str:
    return ";FizzBuzz2;"


def get_ch09_example_moment_lasso() -> LassoUnit:
    return lassounit_shop(get_ch09_example_moment_rope())


def get_texas_rope() -> RopeTerm:
    moment_rope = get_ch09_example_moment_rope()
    nation_str = "nation"
    usa_str = "USA"
    texas_str = "Texas"
    return create_rope_from_labels([moment_rope, nation_str, usa_str, texas_str])


def get_atom_example_factunit_knee(first_label: LabelTerm = None) -> PlanAtom:
    if not first_label:
        first_label = exx.a23
    sports_str = "sports"
    sports_rope = create_rope(first_label, sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope(first_label, knee_str)
    knee_fact_lower = 7
    knee_fact_upper = 23
    x_dimen = kw.plan_keg_factunit
    insert_factunit_planatom = planatom_shop(x_dimen, kw.INSERT)
    insert_factunit_planatom.set_jkey(kw.keg_rope, ball_rope)
    insert_factunit_planatom.set_jkey(kw.fact_context, knee_rope)
    insert_factunit_planatom.set_jvalue(kw.fact_lower, knee_fact_lower)
    insert_factunit_planatom.set_jvalue(kw.fact_upper, knee_fact_upper)
    return insert_factunit_planatom


def get_atom_example_kegunit_sports(moment_rope: MomentRope = None) -> PlanAtom:
    if not moment_rope:
        moment_rope = exx.a23
    sports_str = "sports"
    sports_rope = create_rope(moment_rope, sports_str)
    insert_kegunit_planatom = planatom_shop(kw.plan_kegunit, kw.INSERT)
    insert_kegunit_planatom.set_jkey(kw.keg_rope, sports_rope)
    return insert_kegunit_planatom


def get_atom_example_kegunit_ball(moment_rope: MomentRope = None) -> PlanAtom:
    if not moment_rope:
        moment_rope = exx.a23
    sports_str = "sports"
    sports_rope = create_rope(moment_rope, sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    insert_kegunit_planatom = planatom_shop(kw.plan_kegunit, kw.INSERT)
    insert_kegunit_planatom.set_jkey(kw.keg_rope, ball_rope)
    return insert_kegunit_planatom


def get_atom_example_kegunit_knee(moment_rope: MomentRope = None) -> PlanAtom:
    if not moment_rope:
        moment_rope = exx.a23
    sports_str = "sports"
    sports_rope = create_rope(moment_rope, sports_str)
    knee_str = "knee"
    knee_begin = 1
    knee_close = 71
    begin_str = "begin"
    close_str = "close"
    knee_rope = create_rope(sports_rope, knee_str)
    insert_kegunit_planatom = planatom_shop(kw.plan_kegunit, crud_str=kw.INSERT)
    insert_kegunit_planatom.set_jkey(kw.keg_rope, knee_rope)
    insert_kegunit_planatom.set_jvalue(begin_str, knee_begin)
    insert_kegunit_planatom.set_jvalue(close_str, knee_close)
    return insert_kegunit_planatom


def get_plandelta_sue_example() -> PlanDelta:
    sue_plandelta = plandelta_shop()

    pool_planatom = planatom_shop(kw.planunit, kw.UPDATE)
    pool_attribute = kw.credor_respect
    pool_planatom.set_jvalue(pool_attribute, 77)
    sue_plandelta.set_planatom(pool_planatom)

    dimen = kw.plan_personunit
    sue_planatom = planatom_shop(dimen, kw.DELETE)
    sue_planatom.set_jkey(kw.person_name, exx.sue)
    sue_plandelta.set_planatom(sue_planatom)
    return sue_plandelta


def get_plandelta_example1() -> PlanDelta:
    sue_plandelta = plandelta_shop()

    x_planatom = planatom_shop(kw.planunit, kw.UPDATE)
    x_planatom.set_jvalue(kw.max_tree_traverse, 66)
    x_planatom.set_jvalue(kw.credor_respect, 77)
    x_planatom.set_jvalue(kw.debtor_respect, 88)
    sue_plandelta.set_planatom(x_planatom)

    x_planatom = planatom_shop(dimen=kw.plan_personunit, crud_str=kw.DELETE)
    x_planatom.set_jkey(kw.person_name, exx.zia)
    sue_plandelta.set_planatom(x_planatom)
    return sue_plandelta


def get_sue_lessonunit() -> LessonUnit:
    return lessonunit_shop(plan_name="Sue", _lesson_id=37, face_name="Yao")


def sue_1planatoms_lessonunit() -> LessonUnit:
    x_lessonunit = lessonunit_shop(plan_name="Sue", _lesson_id=53, face_name="Yao")
    x_lessonunit._plandelta.set_planatom(get_atom_example_kegunit_sports())
    return x_lessonunit


def sue_2planatoms_lessonunit() -> LessonUnit:
    x_lessonunit = lessonunit_shop(plan_name="Sue", _lesson_id=53, face_name="Yao")
    x_lessonunit._plandelta.set_planatom(get_atom_example_kegunit_knee())
    x_lessonunit._plandelta.set_planatom(get_atom_example_kegunit_sports())
    return x_lessonunit


def sue_3planatoms_lessonunit() -> LessonUnit:
    x_lessonunit = lessonunit_shop(plan_name="Sue", _lesson_id=37, face_name="Yao")
    x_lessonunit._plandelta.set_planatom(get_atom_example_factunit_knee())
    x_lessonunit._plandelta.set_planatom(get_atom_example_kegunit_ball())
    x_lessonunit._plandelta.set_planatom(get_atom_example_kegunit_knee())
    return x_lessonunit


def sue_4planatoms_lessonunit() -> LessonUnit:
    x_lessonunit = lessonunit_shop(plan_name="Sue", _lesson_id=47, face_name="Yao")
    x_lessonunit._plandelta.set_planatom(get_atom_example_factunit_knee())
    x_lessonunit._plandelta.set_planatom(get_atom_example_kegunit_ball())
    x_lessonunit._plandelta.set_planatom(get_atom_example_kegunit_knee())
    x_lessonunit._plandelta.set_planatom(get_atom_example_kegunit_sports())
    return x_lessonunit
