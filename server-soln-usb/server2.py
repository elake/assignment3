import digraph


def cost_distance(e):
    '''
    edge cost function for an edge composed of two vertices; returns the 
    Euclidean distance between the two vertices in 100,000ths of degrees
    '''
    x1, y1 = vertices[e[0]]
    x2, y2 = vertices[e[1]]
    if 0: # For testing int vs float distance returns
        return int(eucDist(x1, y1, x2, y2))
    return eucDist(x1, y1, x2, y2)

def least_cost_path(G, start, dest, cost):
    '''
    implementation of Dijkstra's algorithm, written in majority by Dr. Jim
    Hoover though the path traceback was written by Eldon Lake
    The first two tests were taken from a discussion forum post by Dr.
    Michael Bowling
    Tests:
    >>> G = digraph.Digraph([(0, 1), (1, 2), (3, 4), (0, 2), (2, 4)])
    >>> least_cost_path(G, 0, 4, lambda e: 1)
    [0, 2, 4]
    >>> least_cost_path(G, 0, 4, lambda e: (e[0] - e[1]) ** 2)
    [0, 1, 2, 4]
    >>> G = digraph.Digraph([(0, 1), (1, 2), (2, 6), (3, 4), (0, 6)])
    >>> least_cost_path(G, 0, 6, lambda e: 1)
    [0, 6]
    >>> least_cost_path(G, 0, 0, lambda e: 1)
    [0]
    >>> least_cost_path(G, 0, 4, lambda e: 1) is None
    True
    >>> least_cost_path(G, 5, 6, lambda e: (e[0] - e[1]) ** 2) is None
    True
    >>> least_cost_path(G, 9, 11, lambda e: (e[0] - e[1]) ** 2) is None
    True
    >>> G = digraph.Digraph([(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)])
    >>> least_cost_path(G, 0, 3, lambda e: e[0])
    [0, 1, 3]
    >>> G = digraph.Digraph([(1, 3), (1, 2), (2, 6), (3, 9), (6, 9)])
    >>> least_cost_path(G, 1, 9, lambda e: e[1] - e[0] + 1)
    [1, 3, 9]
    >>> G = digraph.Digraph()
    >>> least_cost_path(G, 1, 21, lambda e: 1) == None
    True
    >>> G.add_edge((1, 3))
    >>> least_cost_path(G, 1, 13, lambda e: 1) == None
    True
    >>> least_cost_path(G, 3, 1, lambda e: 1) == None
    True
    >>> least_cost_path(G, 1, 3, lambda e: 1)
    [1, 3]
    >>> G.add_edge((3, 1))
    >>> least_cost_path(G, 3, 1, lambda e: 1)
    [3, 1]
    >>> G.add_vertex(4)
    >>> least_cost_path(G, 4, 1, lambda e: 1) == least_cost_path(G, 4, 3, lambda e: 1) == None
    True
    >>> G.add_edge((4, 5))
    >>> least_cost_path(G, 4, 5, lambda e: 1)
    [4, 5]
    >>> G.add_edge((5, 1))
    >>> least_cost_path(G, 4, 1, lambda e: 1)
    [4, 5, 1]
    '''
    todo = {start: 0}
    parent = {}
    visited = set()
    # Return empty list if start or dest cannot be found
    if start not in G.vertices() or dest not in G.vertices():
        return []
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
        return []     

def eucDist(x1, y1, x2, y2):
    '''
    Euclidean distance between (x1, y1) and (x2, y2)
    Tests:
    >>> eucDist(0, 0, 4, 3)
    5.0
    >>> eucDist(0, 0, 68, 285)
    293.0
    >>> eucDist(0, 0, 0, 0)
    0.0
    >>> eucDist(45, 900, 65, 150)
    750.2666192761077
    >>> {eucDist(i, i, i, i) for i in range(100)} == {0}
    True
    >>> {(eucDist(i, i, j, j) == eucDist(j, j, i, i)) for i in range(100) for j in range(100)} == {True}
    True
    '''
    cost = ((x1-x2)**2 + (y1-y2)**2)**0.5
    return cost

def nearestVertex(x, y):
    '''
    Finds the vertex nearest the inputted coordinates
    '''
    dist = float("inf") # start at infinity
    for v in vertices.items(): # look through the vertices for a match
        if eucDist(x, y, v[1][0], v[1][1]) < dist: # search for the closest
            closest = v[0] # analogous to "min"
            dist = eucDist(x, y, v[1][0], v[1][1]) 
    return closest

if 1:
    import doctest
    doctest.testmod()
    
    # Read text file into python
    infile = open("edmonton-roads-digraph.txt", "r")
    vertices = {}
    edges = []
    # edges holds edges plus street names
    # digraphEdges hold edges suitable for digraph
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
            edges.append((start, stop, name)) # put name param. in our edges
            digraphEdges.append((start, stop)) # exclude name for the digraph

        if type == "V": # the type is a vertex
            (name, lon, lat) = fields # the fields of a vertex given by the vid
            # or vertex id, as an integer and lon and lat in degrees as floats
            # multiply by 100000 to turn degrees into 100000ths
            vertices[int(name)] = [int(float(lon)*100000), 
                                   int(float(lat)*100000)]

    # make a digraph of digraph edges, vertices will be filled in automatically
    edmonton = digraph.Digraph(digraphEdges) 

# Test path example at the end of page 2 in assignment3.pdf
correct_path = [314088878, 314088877, 629239018, 314089059,
                314089060, 629239023, 629239027, 629239028]
our_path = least_cost_path(edmonton, nearestVertex(5365488, -11333914),
                nearestVertex(5364727, -11335890), cost_distance)
if correct_path != our_path:
    print("Example path failed!")

def handle_client(request):
    trip = request.split(" ") 
    x1, y1, x2, y2 = trip # get the coords from the incoming request
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to ints

    path = least_cost_path(edmonton, nearestVertex(x1, y1),
                           nearestVertex(x2, y2), cost_distance) # find path
    # convert the path into a list:
    lines = [] 
    for v in path:
            lines.append(str(vertices[v][0])+" "+str(vertices[v][1]))
    
    # print(len(lines)) # for testing
    return lines

# for manually manipulating the server:
if __name__ == "__main__":
    while 1: # continuously wait for input
        trip = input('Awaiting input:').split(" ")
        x1, y1, x2, y2 = trip
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        path = least_cost_path(edmonton, nearestVertex(x1, y1),
                        nearestVertex(x2, y2), cost_distance)
        print(len(path))
        for v in path:
            print(vertices[v][0], vertices[v][1])
    
