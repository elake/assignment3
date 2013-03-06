"""
Plotting program from Michael Blouin

For anybody else who would like to visualize the route that your algorithm is
generating, here is a quick function I threw together that will print out a
path given as a list of (lat, lon) tuples in the format taken by this
site:http://www.multiplottr.com/

You then just copy and paste the output of the script into the "Batch
Addresses" box nearer the bottom of the site and it will create a Google map
with the path you generated.

"""

def generate_map(path):

    """
    Formats a path into a form that is easily visualized on the multiplottr.com
    website.

    Simply paste the output of the function into the "Bulk Addresses" box and
    hit submit.

    """

    print("{}, {} |Start|GREEN|Endpoints".format(path[0][0], path[0][1]))

    for p in range(1, len(path) - 1):
        print("{}, {} |Waypoint {}|BLUE|Waypoints".format(path[p][0], path[p][1], p))

    print("{}, {} |Destionation|RED|Endpoints".format(path[-1][0], path[-1][1]))
    print("{}, {} |BLUE|LINE1|".format(path[0][0], path[0][1]))

    for p in path[1:-1]:
        print("{}, {} |BLUE|LINE1|".format(p[0], p[1]))

    print("{}, {} |BLUE|LINE1|".format(path[-1][0], path[-1][1]))
    print("{}, {} |15|CENTER".format((path[0][0]+path[-1][0])/2, (path[0][1]+path[-1][1])/2))

if __name__ == "__main__":
    import sample_path
    # print(sample_path.path) 
    generate_map(sample_path.path) 
