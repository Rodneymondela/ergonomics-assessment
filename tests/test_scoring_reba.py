from app.scoring.rula_reba import compute_reba_full
def test_reba_basic():
    score = compute_reba_full(dict(trunk=1, neck=1, legs=1, upper_arm=1, lower_arm=1, wrist=1, coupling=0, load=0, activity_static=0, activity_repeat=0, activity_rapid=0))
    assert 1 <= score <= 15
