import math
def hav(a,b):
 r=6371.; p1,p2=math.radians(a[0]),math.radians(b[0]); dp=math.radians(b[0]-a[0]); dl=math.radians(b[1]-a[1]); x=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2; return 2*r*math.asin(math.sqrt(x))
def nn(points,depot=0):
 u=set(range(len(points))); u.remove(depot); route=[depot]
 while u: n=min(u,key=lambda i:hav(points[route[-1]],points[i])); route.append(n); u.remove(n)
 return route+[depot]
def dist(p,r): return sum(hav(p[r[i]],p[r[i+1]]) for i in range(len(r)-1))
def optimize(points):
 try:
  from ortools.constraint_solver import pywrapcp,routing_enums_pb2
  n=len(points); mat=[[int(hav(a,b)*1000) for b in points] for a in points]; m=pywrapcp.RoutingIndexManager(n,1,0); routing=pywrapcp.RoutingModel(m)
  cb=routing.RegisterTransitCallback(lambda i,j:mat[m.IndexToNode(i)][m.IndexToNode(j)]); routing.SetArcCostEvaluatorOfAllVehicles(cb); s=pywrapcp.DefaultRoutingSearchParameters(); s.first_solution_strategy=routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC; sol=routing.SolveWithParameters(s)
  if sol:
   r=[]; i=routing.Start(0)
   while not routing.IsEnd(i): r.append(m.IndexToNode(i)); i=sol.Value(routing.NextVar(i))
   r.append(m.IndexToNode(i)); return r,'OR-Tools'
 except Exception: pass
 return nn(points),'Nearest-neighbor fallback'
