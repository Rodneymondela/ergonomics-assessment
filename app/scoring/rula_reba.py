from typing import Dict
RULA_TABLE_A = [
    [[1,2,2,3],[2,2,3,3],[2,3,3,4],[3,3,4,4],[4,4,4,5],[5,5,5,5]],
    [[2,2,3,3],[2,3,3,4],[3,3,4,4],[3,4,4,5],[4,4,5,5],[5,5,5,6]],
    [[2,3,3,4],[3,3,4,4],[3,4,4,5],[4,4,5,5],[4,5,5,6],[5,5,6,6]],
]
RULA_TABLE_B_LEGS12 = [
    [1,2,3,3,4,5],[2,2,3,4,5,5],[3,3,3,4,5,6],
    [3,4,4,5,6,6],[4,5,5,6,6,7],[5,5,6,6,7,7],
]
RULA_TABLE_B_LEGS34 = [
    [2,3,3,4,5,6],[3,3,4,5,6,6],[3,4,4,5,6,7],
    [4,5,5,6,7,7],[5,6,6,7,7,7],[6,6,7,7,7,7],
]
RULA_TABLE_C = [
    [1,2,3,3,4,5,6],[2,2,3,4,5,5,6],[3,3,3,4,5,6,7],
    [3,4,4,5,6,6,7],[4,5,5,6,6,7,7],[5,5,6,6,7,7,7],[6,6,7,7,7,7,7],
]
def _rula_a(upper:int, lower_band:int, wrist:int, twist:int)->int:
    base = RULA_TABLE_A[max(1,min(lower_band,3))-1][max(1,min(upper,6))-1][max(1,min(wrist,4))-1]
    return min(7, base + (1 if twist>=2 else 0))
def _rula_b(neck:int, trunk:int, legs:int)->int:
    table = RULA_TABLE_B_LEGS12 if legs in (1,2) else RULA_TABLE_B_LEGS34
    return table[max(1,min(neck,6))-1][max(1,min(trunk,6))-1]
def compute_rula_full(i: Dict[str,int]) -> int:
    A = _rula_a(i['upper_arm'], i['lower_arm_band'], i['wrist'], i.get('wrist_twist',1))
    B = _rula_b(i['neck'], i['trunk'], i['legs'])
    A_ = min(7, A + i.get('muscle_use',0) + i.get('force_load',0))
    B_ = min(7, B + i.get('muscle_use',0) + i.get('force_load',0))
    return RULA_TABLE_C[A_-1][B_-1]
REBA_TABLE_A_LEG1 = [[1,2,2],[2,3,3],[3,4,5],[4,5,6],[5,6,7]]
REBA_TABLE_A_LEG2 = [[2,3,3],[3,4,4],[4,5,6],[5,6,7],[6,7,8]]
REBA_TABLE_B_WRIST1 = [[1,2,2],[2,2,3],[3,3,4],[4,4,4],[5,5,5],[6,6,7]]
REBA_TABLE_B_WRIST2 = [[2,2,3],[2,3,3],[3,4,4],[4,4,5],[5,6,6],[6,7,7]]
REBA_TABLE_B_WRIST3 = [[2,3,3],[3,3,4],[4,4,5],[4,5,6],[6,6,7],[7,7,8]]
REBA_TABLE_C = [
 [1,1,1,2,3,3,4,5,6,7,7,8],
 [1,2,2,3,3,4,4,5,6,7,8,8],
 [2,2,3,3,4,4,5,6,7,8,8,9],
 [3,3,3,4,4,5,6,7,8,8,9,10],
 [3,4,4,4,5,6,7,8,8,9,10,11],
 [4,4,5,5,6,7,8,8,9,10,11,11],
 [4,5,5,6,7,8,8,9,10,11,11,12],
 [5,5,6,7,8,8,9,10,11,11,12,12],
 [6,6,7,8,8,9,10,11,11,12,12,13],
 [7,7,8,8,9,10,11,11,12,12,13,13],
 [7,8,8,9,10,11,11,12,12,13,13,14],
 [8,8,9,10,11,11,12,12,13,13,14,15],
]
def _reba_a(trunk:int, neck:int, legs:int)->int:
    t,n = max(1,min(trunk,5))-1, max(1,min(neck,3))-1
    tab = REBA_TABLE_A_LEG1 if legs==1 else REBA_TABLE_A_LEG2
    return tab[t][n]
def _reba_b(upper:int, lower:int, wrist:int)->int:
    u,l = max(1,min(upper,6))-1, max(1,min(lower,3))-1
    if wrist==1: return REBA_TABLE_B_WRIST1[u][l]
    if wrist==2: return REBA_TABLE_B_WRIST2[u][l]
    return REBA_TABLE_B_WRIST3[u][l]
def compute_reba_full(i: Dict[str,int])->int:
    A = _reba_a(i['trunk'], i['neck'], i['legs'])
    B = _reba_b(i['upper_arm'], i['lower_arm'], i['wrist'])
    A_ = min(12, A + i.get('load',0) + i.get('activity_static',0) + i.get('activity_repeat',0) + i.get('activity_rapid',0))
    B_ = min(12, B + i.get('coupling',0))
    return REBA_TABLE_C[A_-1][B_-1]
def risk_band(method:str, score:float)->dict:
    if method=='RULA':
        cat = 'Low' if score<=2 else 'Medium' if score<=4 else 'High'
    elif method=='REBA':
        cat = 'Low' if score<=3 else 'Medium' if score<=7 else 'High'
    else:
        cat = 'Medium'
    return {'method': method, 'category': cat, 'note': ''}
