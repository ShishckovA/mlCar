from pygame.math import Vector2
def vect(v1, v2):
    return v1.x * v2.y - v2.x * v1.y

def my_key(v):
    return v.x, v.y

def intersectTwoSegments(s1, s2):
    return intersectTwoSegments1(s1.A, s1.B, s2.A, s2.B)

def intersectTwoSegments1(A, B, C, D):
    dir1 = B - A
    dir2 = D - C

    if vect(dir1, dir2):
        t1 = (vect(C, dir2) - vect(A, dir2)) / vect(dir1, dir2)
        t2 = (vect(A, dir1) - vect(C, dir1)) / vect(dir2, dir1)
        if 0 <= t1 <= 1 and 0 <= t2 <= 1:
            return A + dir1 * t1
        else:
            return None
    else:
        if vect(B - A, D - C) or vect(D - A, C - B):
            return None
        else:
            A, B = min(A, B, key = my_key), max(A, B, key = my_key)
            C, D = min(C, D, key = my_key), max(C, D, key = my_key)
            if my_key(B) < my_key(C) or my_key(D) < my_key(A):
                return None
            else:
                firs = max(A, C, key=my_key)
                return firs
