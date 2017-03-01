import pytest
import mlbgame


@pytest.fixture(scope='session')
def data():
    d = dict()
    d['ab'] = '3'
    d['batter_side'] = 'L'
    d['s_avg'] = '0.350'
    return d


def test_init_mlbgame_object(data):
    o = mlbgame.object.Object(data)

    assert isinstance(o, mlbgame.object.Object)

    assert o.ab == 3
    assert isinstance(o.ab, int)

    assert o.batter_side == 'L'
    assert isinstance(o.batter_side, str)

    assert o.s_avg == 0.350
    assert isinstance(o.s_avg, float)


if __name__ == '__main__':
    pass
