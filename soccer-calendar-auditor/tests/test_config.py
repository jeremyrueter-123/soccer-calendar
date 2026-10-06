from config import SOURCES


def test_maryland_scope_has_31_teams():
    assert len(SOURCES) == 31
    assert len({(s['team'], s['gender']) for s in SOURCES}) == 31
    assert not any(s['team'] == 'Catholic' for s in SOURCES)


def test_maryland_scope_is_complete():
    expected = {
        ('Maryland', 'Men'), ('Maryland', 'Women'),
        ('UMBC', 'Men'), ('UMBC', 'Women'),
        ("Mount St. Mary's", 'Men'), ("Mount St. Mary's", 'Women'),
        ('Loyola', 'Men'), ('Loyola', 'Women'),
        ('Navy', 'Men'), ('Navy', 'Women'),
        ('Towson', 'Women'),
        ('Frostburg State', 'Men'), ('Frostburg State', 'Women'),
        ('Johns Hopkins', 'Men'), ('Johns Hopkins', 'Women'),
        ('McDaniel', 'Men'), ('McDaniel', 'Women'),
        ('Washington College', 'Men'), ('Washington College', 'Women'),
        ('Salisbury', 'Men'), ('Salisbury', 'Women'),
        ('Goucher', 'Men'), ('Goucher', 'Women'),
        ('Hood', 'Men'), ('Hood', 'Women'),
        ('Stevenson', 'Men'), ('Stevenson', 'Women'),
        ('Notre Dame (MD)', 'Men'), ('Notre Dame (MD)', 'Women'),
        ("St. Mary's", 'Men'), ("St. Mary's", 'Women'),
    }
    assert {(s['team'], s['gender']) for s in SOURCES} == expected
