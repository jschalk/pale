from plotly.graph_objects import Figure as plotly_Figure


def conditional_fig_show(fig: plotly_Figure, graphics_bool: bool):
    if graphics_bool:
        fig.show()


def add_simp_rect(fig: plotly_Figure, x0, y0, x1, y1, display_str, x_color=None):
    if x_color is None:
        x_color = "LightSeaGreen"
    line_dict = dict(color=x_color, width=4)
    fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, line=line_dict)
    add_01rect(fig, x0, y1, display_str)


def add_direc_rect(fig: plotly_Figure, x0, y0, x1, y1, display_str):
    line_dict = dict(color="LightSeaGreen", width=2, dash="dot")
    fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, line=line_dict)
    add_01rect(fig, x0, y1, display_str)


def add_01rect(fig, x0, y0, text):
    x_margin = 0.2
    fig.add_annotation(
        x=x0 + x_margin, y=y0 - x_margin, text=text, showarrow=False, align="left"
    )


def add_keep__rect(
    fig: plotly_Figure, x0, y0, x1, y1, text1=None, text2=None, text3=None, text4=None
):
    line_dict = dict(color="LightSeaGreen", width=2, dash="dot")
    fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, line=line_dict)
    add_01rect(fig, x0 + 0.5, y1, text1)
    add_01rect(fig, x0 + 0.5, y1 - 0.2, text2)
    add_01rect(fig, x0 + 0.5, y1 - 0.4, text3)
    add_01rect(fig, x0 + 0.5, y1 - 0.6, text4)


def add_2_curve(fig: plotly_Figure, path: str, color: str):
    fig.add_shape(dict(type="path", path=path, line_color=color))


def add_rect_arrow(fig: plotly_Figure, x0, y0, ax0, ay0, color=None):
    if color is None:
        color = "black"
    fig.add_annotation(
        x=x0,  # arrows' head
        y=y0,  # arrows' head
        ax=ax0,  # arrows' tail
        ay=ay0,  # arrows' tail
        xref="x",
        yref="y",
        axref="x",
        ayref="y",
        text="",  # arrow only
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=3,
        arrowcolor=color,
    )
