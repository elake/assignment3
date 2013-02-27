import digraph


# Read text file into python
infile = open("edmonton-roads-digraph.txt", "r")
vertices = {}
edges = []
#edges holds edges plus street names
#digraphEdges hold edges suitable for digraph
digraphEdges = []
for line in infile:
    line = line.rstrip()
    fields = line.split(",")
    
    type = fields.pop(0)

    if type == "E":
        (start, stop, name) = fields
        name = name.strip('"')
        stop = int(stop)
        start = int(start)
        edges.append((start, stop, name))
        digraphEdges.append((start, stop))
    if type == "V":
        (name, lon, lat) = fields
        vertices[int(name)] = [float(lon),float(lat)]
edmonton = digraph.Digraph(digraphEdges)

def edgecost(e):
    x1, y1 = vertices[e[0]]
    x2, y2 = vertices[e[1]]
    return eucDist(x1, y1, x2, y2)

def least_cost_path(G, start, dest, cost):
    todo = {start: 0}
    parent = {}
    visited = set()
    while todo and dest not in visited:
        cur = min(todo, key=todo.get)
        c = todo[cur]
        todo.pop(cur)
        visited.add(cur)
        for n in G.adj_to(cur):
            if n in visited: continue
            if n not in todo or ( c + cost((cur,n)) < todo[n] ):
                todo[n] = c + cost((cur,n))
                parent[n] = cur
    if dest in visited:
        path = []
        while start not in path:
            path.insert(0, parent[cur])
            cur = parent[cur]
        return path
    else:
        return None     

def eucDist(x1, y1, x2, y2):
    cost = ((x1-x2)**2 + (y1-y2)**2)**0.5
    return cost

def nearestVertex(x, y):
    # 100 degrees is arbitrarily large
    dist = 100
    for v in vertices.items():
        if eucDist(x, y, v[1][0], v[1][1]) < dist:
            closest = v[0]
            dist = eucDist(x, y, v[1][0], v[1][1])
    return closest

while 1:
    trip = input('Awaiting input:').split(" ")
    x1, y1, x2, y2 = trip
    least_cost_path(edmonton, nearestVertex(x1, y1),
                    nearestVertex(x2, y2), edgecost)
    
