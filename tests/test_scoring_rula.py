from app.scoring.rula_reba import compute_rula_full
def test_rula_low_band():
    score = compute_rula_full(dict(upper_arm=1, lower_arm_band=1, wrist=1, wrist_twist=1, neck=1, trunk=1, legs=1, muscle_use=0, force_load=0))
    assert 1 <= score <= 3
