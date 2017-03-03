import mlbgame


def test_statmap_idmap():
    assert isinstance(mlbgame.statmap.idmap, dict)
    assert len(mlbgame.statmap.idmap) >= 50
    assert 'ab' in mlbgame.statmap.idmap
