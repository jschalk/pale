from pandas import DataFrame, concat as pandas_concat
from plotly.graph_objects import Figure as plotly_Figure, Table as plotly_Table
from src.ch07_plan_logic.plan_report import (
    get_plan_agenda_dataframe,
    get_plan_personunits_dataframe,
)
from src.ch09_plan_lesson.lasso import lassounit_shop
from src.ch09_plan_lesson.lesson_filehandler import open_gut_file
from src.ch10_plan_listen.keep_tool import open_job_file
from src.ch14_moment.moment_main import MomentUnit


def get_moment_guts_persons_dataframe(x_moment: MomentUnit) -> DataFrame:
    # get list of all plan paths
    moment_plan_names = x_moment._get_plan_dir_names()
    # for all plans get gut
    gut_dfs = []
    for plan_name in moment_plan_names:
        moment_lasso = lassounit_shop(x_moment.moment_rope)
        gut_plan = open_gut_file(x_moment.moment_mstr_dir, moment_lasso, plan_name)
        gut_plan.cashout()
        df = get_plan_personunits_dataframe(gut_plan)
        df.insert(0, "plan_name", gut_plan.plan_name)
        gut_dfs.append(df)
    return pandas_concat(gut_dfs, ignore_index=True)


def get_moment_guts_persons_plotly_fig(x_moment: MomentUnit) -> plotly_Figure:
    column_header_list = [
        "plan_name",
        "person_name",
        "person_cred_lumen",
        "person_debt_lumen",
        "fund_give",
        "fund_take",
        "fund_agenda_give",
        "fund_agenda_take",
    ]
    df = get_moment_guts_persons_dataframe(x_moment)
    header_dict = dict(values=column_header_list, fill_color="powderblue", align="left")
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.plan_name,
                df.person_name,
                df.person_cred_lumen,
                df.person_debt_lumen,
                df.fund_give,
                df.fund_take,
                df.fund_agenda_give,
                df.fund_agenda_take,
            ],
            fill_color="lavender",
            align="left",
        ),
    )

    fig = plotly_Figure(data=[x_table])
    fig_label = f"moment '{x_moment.moment_rope}', gut persons metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_label, title_font_size=20)

    return fig


def get_moment_jobs_persons_dataframe(x_moment: MomentUnit) -> DataFrame:
    # get list of all plan paths
    moment_plan_names = x_moment._get_plan_dir_names()
    # for all plans get gut
    job_dfs = []
    for plan_name in moment_plan_names:
        moment_lasso = lassounit_shop(x_moment.moment_rope, x_moment.knot)
        job = open_job_file(x_moment.moment_mstr_dir, moment_lasso, plan_name)
        job.cashout()
        job_df = get_plan_personunits_dataframe(job)
        job_df.insert(0, "plan_name", job.plan_name)
        job_dfs.append(job_df)
    return pandas_concat(job_dfs, ignore_index=True)


def get_moment_jobs_persons_plotly_fig(x_moment: MomentUnit) -> plotly_Figure:
    column_header_list = [
        "plan_name",
        "person_name",
        "person_cred_lumen",
        "person_debt_lumen",
        "fund_give",
        "fund_take",
        "fund_agenda_give",
        "fund_agenda_take",
    ]
    df = get_moment_jobs_persons_dataframe(x_moment)
    header_dict = dict(values=column_header_list, fill_color="powderblue", align="left")
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.plan_name,
                df.person_name,
                df.person_cred_lumen,
                df.person_debt_lumen,
                df.fund_give,
                df.fund_take,
                df.fund_agenda_give,
                df.fund_agenda_take,
            ],
            fill_color="lavender",
            align="left",
        ),
    )

    fig = plotly_Figure(data=[x_table])
    fig_label = f"moment '{x_moment.moment_rope}', job persons metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_label, title_font_size=20)
    return fig


def get_moment_guts_agenda_dataframe(x_moment: MomentUnit) -> DataFrame:
    # get list of all plan paths
    moment_plan_names = x_moment._get_plan_dir_names()
    # for all plans get gut
    gut_dfs = []
    for plan_name in moment_plan_names:
        moment_lasso = lassounit_shop(x_moment.moment_rope, x_moment.knot)
        gut_plan = open_gut_file(x_moment.moment_mstr_dir, moment_lasso, plan_name)
        gut_plan.cashout()
        df = get_plan_agenda_dataframe(gut_plan)
        gut_dfs.append(df)
    return pandas_concat(gut_dfs, ignore_index=True)


def get_moment_guts_agenda_plotly_fig(x_moment: MomentUnit) -> plotly_Figure:
    column_header_list = [
        "plan_name",
        "fund_ratio",
        "keg_label",
        "parent_rope",
        "begin",
        "close",
        "addin",
        "denom",
        "numor",
        "morph",
    ]
    df = get_moment_guts_agenda_dataframe(x_moment)
    header_dict = dict(values=column_header_list, fill_color="powderblue", align="left")
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.plan_name,
                df.fund_ratio,
                df.keg_label,
                df.parent_rope,
                df.begin,
                df.close,
                df.addin,
                df.denom,
                df.numor,
                df.morph,
            ],
            fill_color="lavender",
            align="left",
        ),
    )

    fig = plotly_Figure(data=[x_table])
    fig_label = f"moment '{x_moment.moment_rope}', gut agenda metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_label, title_font_size=20)
    return fig


def get_moment_jobs_agenda_dataframe(x_moment: MomentUnit) -> DataFrame:
    # get list of all plan paths
    job_dfs = []
    for x_plan_name in x_moment._get_plan_dir_names():
        moment_lasso = lassounit_shop(x_moment.moment_rope, x_moment.knot)
        job = open_job_file(x_moment.moment_mstr_dir, moment_lasso, x_plan_name)
        job.cashout()
        job_df = get_plan_agenda_dataframe(job)
        job_dfs.append(job_df)
    return pandas_concat(job_dfs, ignore_index=True)


def get_moment_jobs_agenda_plotly_fig(x_moment: MomentUnit) -> plotly_Figure:
    column_header_list = [
        "plan_name",
        "fund_ratio",
        "keg_label",
        "parent_rope",
        "begin",
        "close",
        "addin",
        "denom",
        "numor",
        "morph",
    ]
    df = get_moment_jobs_agenda_dataframe(x_moment)
    header_dict = dict(values=column_header_list, fill_color="powderblue", align="left")
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.plan_name,
                df.fund_ratio,
                df.keg_label,
                df.parent_rope,
                df.begin,
                df.close,
                df.addin,
                df.denom,
                df.numor,
                df.morph,
            ],
            fill_color="lavender",
            align="left",
        ),
    )

    fig = plotly_Figure(data=[x_table])
    fig_label = f"moment '{x_moment.moment_rope}', job agenda metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_label, title_font_size=20)
    return fig
