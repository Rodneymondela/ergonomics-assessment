from app.scoring.rula_reba import compute_rula_full, compute_reba_full
def test_rula_reba_ranges():
    rula = compute_rula_full(dict(upper_arm=1, lower_arm_band=1, wrist=1, wrist_twist=1, neck=1, trunk=1, legs=1, muscle_use=0, force_load=0))
    reba = compute_reba_full(dict(trunk=1, neck=1, legs=1, upper_arm=1, lower_arm=1, wrist=1, coupling=0, load=0, activity_static=0, activity_repeat=0, activity_rapid=0))
    assert 1 <= rula <= 7
    assert 1 <= reba <= 15
