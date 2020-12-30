from pytest import fixture


@fixture
def supply_AA_BB_CC():
    aa = 25
    bb = 35
    cc = 45
    return [aa, bb, cc]


@fixture
def supply_url():
    return "https://reqres.in/api"
