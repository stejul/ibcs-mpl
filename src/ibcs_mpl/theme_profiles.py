from ibcs_mpl.theme import IBCSTheme


def default_profile() -> IBCSTheme:
    return IBCSTheme()


def print_bw_profile() -> IBCSTheme:
    return IBCSTheme(
        actual_dark="#1F1F1F",
        measured_light="#8C8C8C",
        variance_pos="#6E6E6E",
        variance_neg="#2B2B2B",
        variance_neu="#9A9A9A",
    )


def color_deficiency_safe_profile() -> IBCSTheme:
    return IBCSTheme(
        variance_pos="#007A7A",
        variance_neg="#C62828",
        variance_neu="#6E6E6E",
    )


def dashboard_profile() -> IBCSTheme:
    return IBCSTheme(
        font_size=9,
        title_size=11,
        label_size=8,
    )


def get_theme_profile(name: str) -> IBCSTheme:
    normalized = name.strip().lower()
    if normalized in {"default", "standard"}:
        return default_profile()
    if normalized in {"print", "bw", "black-white", "black_white"}:
        return print_bw_profile()
    if normalized in {"color-deficiency", "color_deficiency", "accessible", "cb-safe"}:
        return color_deficiency_safe_profile()
    if normalized in {"dashboard", "dash"}:
        return dashboard_profile()
    raise KeyError(f"Unknown theme profile: {name}")
