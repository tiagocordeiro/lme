from lme.prices import date_range_builder


def test_date_range_period_returns_type():
    periodo = date_range_builder()
    assert type(periodo) == dict


def test_date_range_period_returns_content():
    periodo = date_range_builder()
    assert 'inicio' in periodo
