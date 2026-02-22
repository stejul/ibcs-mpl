from ibcs_mpl.theme_profiles import get_theme_profile


def test_get_theme_profile_dashboard() -> None:
    t = get_theme_profile("dashboard")
    assert t.title_size == 11
    assert t.label_size == 8
