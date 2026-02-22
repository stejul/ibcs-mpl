from ibcs_mpl.types import Pt
import matplotlib.figure


def pt_to_fig_x(fig: matplotlib.figure.Figure, pt: Pt) -> float:
    """Convert points to figure-coordinate delta in X direction"""
    inches = pt / 72.0
    fig_w_in = fig.get_size_inches()[0]

    return inches / fig_w_in

def pt_to_fig_y(fig: matplotlib.figure.Figure, pt: Pt) -> float:
    """Convert points to figure-coordinate delta in Y direction"""
    inches = pt / 72.0
    fig_h_in = fig.get_size_inches()[1]

    return inches / fig_h_in
