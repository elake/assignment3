import digraph


# Read text file into python
infile = open("edmonton-roads-digraph.txt", "r")
vertices = {}
edges = []
#edges holds edges plus street names
#digraphEdges hold edges suitable for digraph
digraphEdges = []
for line in infile: # remove the endline character
    line = line.rstrip() # split the parameters of the csv
    fields = line.split(",")
    
    type = fields.pop(0) # vertex or edge indicator (hopefully)

    if type == "E": # the type is an edge
        (start, stop, name) = fields # remaining unpopped fields
        name = name.strip('"') # remove the quotes from the name field
        stop = int(stop) # integer-ize the stop and start fields; 
        start = int(start)
        edges.append((start, stop, name)) # put the name param. in our edges
        digraphEdges.append((start, stop)) # exclude the name for the digraph
    if type == "V": # the type is a vertex
        (name, lon, lat) = fields # the fields of a vertex given by the vid, or
        # vertex id, as an integer and lon and lat in degrees as floats
        # multiply by 100000 to turn degrees into 100000ths
        vertices[int(name)] = [int(float(lon)*100000), int(float(lat)*100000)]

# make a digraph of our digraph edges, vertices will be filled in automatically
edmonton = digraph.Digraph(digraphEdges) 

def edgecost(e):
    '''
    edge cost function for an edge composed of two vertices; returns the 
    Euclidean distance between the two vertices in 100,000ths of degrees
    '''
    x1, y1 = vertices[e[0]]
    x2, y2 = vertices[e[1]]
    return eucDist(x1, y1, x2, y2)

def least_cost_path(G, start, dest, cost):
    '''
    implementation of Dijkstra's algorithm, written in majority by Dr. Jim
    Hoover though the path traceback was written by Eldon Lake
    '''
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
    if dest in visited: # this means we found dest in the above search
        path = [dest] # include dest in path to start, work from its parent
        while start not in path:
            path.insert(0, parent[cur]) # insert the parents at the beginning
            cur = parent[cur] # ascend to the parent of cur
        return path
    else: # we did not find dest in our search, return None as specified
        return None     

def eucDist(x1, y1, x2, y2):
    '''
    Euclidean distance between (x1, y1) and (x2, y2)
    '''
    cost = ((x1-x2)**2 + (y1-y2)**2)**0.5
    return cost

def nearestVertex(x, y):
    # 100 degrees is arbitrarily large, no such distance possible
    dist = 100
    for v in vertices.items(): # look through the vertices for a match
        if eucDist(x, y, v[1][0], v[1][1]) < dist: # search for the closest
            closest = v[0] # analogous to "min"
            dist = eucDist(x, y, v[1][0], v[1][1]) 
    return closest

while 1: # continuously wait for input
    trip = input('Awaiting input:').split(" ")
    x1, y1, x2, y2 = trip
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    path = least_cost_path(edmonton, nearestVertex(x1, y1),
                    nearestVertex(x2, y2), edgecost)
    print(len(path))
    for v in path:
        print(vertices[v])
