LC = 23.0
def HM(h): return min(1, max(0, 25/h))
def VM(v): return max(0, 1 - 0.003*abs(v-75))
def DM(d): return max(0, 0.82 + (4.5/d))
def AM(a): return max(0, 1 - 0.0032*a)
def FM(freq):
    f = max(0.2, min(freq, 6))
    return max(0.3, 1.3 - 0.15*f)
def CM(c): return max(0.7, min(c, 1.0))
def compute_niosh(weight, h, v, d, a, f, c):
    rwl = LC * HM(h) * VM(v) * DM(d) * AM(a) * FM(f) * CM(c)
    rwl = max(0.1, rwl)
    li = weight / rwl
    return round(li, 2), round(rwl, 1)
