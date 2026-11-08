"""Numerical Gauss linking integral for oriented closed polygonal curves."""
import math


def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])


def curve(points):
    if not isinstance(points,(list,tuple)) or not 3 <= len(points) <= 2000:
        raise ValueError('A curve requires 3 to 2000 vertices')
    result=[]
    for p in points:
        if not isinstance(p,(list,tuple)) or len(p)!=3:
            raise ValueError('Curve vertices must have three coordinates')
        try:
            p=tuple(float(v) for v in p)
        except (TypeError,ValueError) as exc:
            raise ValueError('Coordinates must be finite numbers') from exc
        if not all(math.isfinite(v) for v in p):
            raise ValueError('Coordinates must be finite numbers')
        result.append(p)
    if result[0]==result[-1]: result.pop()
    if len(result)<3 or any(result[i]==result[(i+1)%len(result)] for i in range(len(result))):
        raise ValueError('Curve requires three vertices and nonzero edges')
    return result


def segment_distance(p,q,r,s):
    # Minimize squared distance on [0,1]^2: interior stationary point and boundaries.
    u,v,w=sub(q,p),sub(s,r),sub(p,r)
    a,b,c,d,e=dot(u,u),dot(u,v),dot(v,v),dot(u,w),dot(v,w)
    clamp=lambda t:max(0.0,min(1.0,t))
    candidates=[(0,clamp(e/c)),(1,clamp((e+b)/c)),(clamp(-d/a),0),(clamp((b-d)/a),1)]
    denominator=a*c-b*b
    if denominator>1e-14*a*c:
        t,z=(b*e-c*d)/denominator,(a*e-b*d)/denominator
        if 0<=t<=1 and 0<=z<=1: candidates.append((t,z))
    return math.sqrt(min(sum((w[i]+t*u[i]-z*v[i])**2 for i in range(3)) for t,z in candidates))


def linking_number(first, second, subdivisions=8, tolerance=1e-9):
    """Midpoint quadrature estimate. Never round this into a certified invariant.

    Curves close implicitly; reject intersections/near contacts at tolerance.
    Orientation reversal of one curve reverses the sign.
    """
    if type(subdivisions) is not int or not 1<=subdivisions<=32:
        raise ValueError('subdivisions must be an integer from 1 to 32')
    if not math.isfinite(tolerance) or tolerance<=0:
        raise ValueError('tolerance must be positive and finite')
    curves=[curve(first),curve(second)]
    if len(curves[0])*len(curves[1])*subdivisions**2 > 2_000_000:
        raise ValueError('Quadrature exceeds two million sample pairs')
    edges=[[(p,ps[(i+1)%len(ps)]) for i,p in enumerate(ps)] for ps in curves]
    for es in edges:
        for i,(p,q) in enumerate(es):
            for j in range(i+1,len(es)):
                if j==i+1 or (i==0 and j==len(es)-1): continue
                if segment_distance(p,q,*es[j])<=tolerance:
                    raise ValueError('Curve self-intersects or has near contact')
    minimum=min(segment_distance(p,q,r,s) for p,q in edges[0] for r,s in edges[1])
    if minimum<=tolerance:
        raise ValueError('Curves intersect or have near contact')
    samples=[]
    for es in edges:
        parts=[]
        for p,q in es:
            delta=tuple(v/subdivisions for v in sub(q,p))
            for i in range(subdivisions):
                parts.append((tuple(p[j]+(i+0.5)*delta[j] for j in range(3)),delta))
        samples.append(parts)
    total=0.0
    for p,dp in samples[0]:
        for q,dq in samples[1]:
            difference=sub(p,q)
            total+=dot(difference,cross(dp,dq))/dot(difference,difference)**1.5
    return {'estimate':total/(4*math.pi),'minimum_separation':minimum,
            'subdivisions':subdivisions,'method':'midpoint Gauss integral; convergence must be checked'}
