

from haversine import haversine
import pandas as pd

latitude_longitude = pd.read_csv("nodes.csv")

def haversine_distance(currNode):
    [currLat, currLon] = latitude_longitude[latitude_longitude["id"] == currNode].iloc[0][ ["lat", "lon"] ]
    #[desLat,destLon] = latitude_longitude[latitude_longitude["id"] == destNode].iloc[0][["lat","lon"]]
    curr = (currLat, currLon)

    dest = (17.5473641,78.5724988)
    return haversine(curr, dest)






import networkx as nx
path1 = pd.read_csv("edges.csv")
path1= path1[["source", "target", "length"]]
path = path1.drop_duplicates()
graph_using = nx.Graph
g = nx.from_pandas_edgelist(path,source="source",target="target", edge_attr="length", create_using=graph_using)

import heapq
def create_path(cameFrom, current):
    path = [current]
    while current in cameFrom.keys():
        current = cameFrom[current]
        path.insert(0, current)
    return path
def AStar(srcNode, destNode):
    set = []
    cameFrom = {}
    cameFrom[srcNode] = None
    cost = {}
    cost[srcNode] = 0
    f = {}
    f[srcNode] = 0
    g_n = {}
    g_n[srcNode] = 0
    heapq.heappush(set, (srcNode, f))
    i = 0
    while len(set) > 0:
        currentNode = heapq.heappop(set)
        print(i)
        i = i + 1
        if currentNode[0] == destNode:
            return create_path(cameFrom, currentNode[0])



        neighbourData = list(g.neighbors(currentNode[0]))


        for item in neighbourData:
            # distance = length of edge between currentNode & neighbourNode
            # neighbourNode is osm id of the node
            neighbourNode = item
            distance = g[currentNode[0]][neighbourNode]["length"]

            # if neighbourNode has not been visited before
            if neighbourNode not in cameFrom:

                # cost = distance from srcNode to neighbourNode through currentNode i.e. tentative gScore of neighbourNode
                cost[neighbourNode] = g_n[currentNode[0]] + distance

                # if we have a neighbour that has been visited already by some other path
                # and we are visiting it again via some new path, we check which path is optimum
                if cost[neighbourNode] < g_n.get(neighbourNode, float("inf")):
                    # if true then this path is better one than the previous
                    # so we update everything
                    cameFrom[neighbourNode] = currentNode[0]
                    g_n[neighbourNode] = cost[neighbourNode]
                    f[neighbourNode] = g_n[neighbourNode] + haversine_distance(
                        neighbourNode
                    )
                    if neighbourNode not in set:
                        heapq.heappush(set, (neighbourNode, f))

    # return openSet: it is empty, so destination was never reached. [Failure]
    return set


# In[ ]:


# osm id of source node
srcNode = 5711258337
# osm ide of destination node
destNode = 7065632060
# call to aStar
print("fin")
route = AStar(srcNode, destNode)
route.pop(0)

# popping the None


# if path not found, inform the user
if len(route) == 0:
    print(f"Fatal Error: Path doesn't exist")


# In[6]:

print('fin2')
# aStar function return list(route) which contains osm id's so we need to obtain lat lons from latlonData for each osm id
latlonRoute = []
for node in route:
    [lat, lon] = latitude_longitude[latitude_longitude["id"] == node].iloc[0][["lat", "lon"]]
    latlonRoute.append((lat, lon))

# to find meanLat and meanLon so as to display middle location on map
from statistics import mean

meanLat = mean(point[0] for point in latlonRoute)
meanLon = mean(point[1] for point in latlonRoute)
print("fin")

import gmplot

routeLats, routeLons = zip(*latlonRoute)
gmap = gmplot.GoogleMapPlotter(meanLat, meanLon, 13)
# uncomment the foloowing line to make a scatter plot the nodes along thr route
# gmap.scatter(routeLats, routeLons, '#FF0000', size = 50, marker = False )
gmap.plot(routeLats, routeLons, "cornflowerblue", edge_width=3.0)
gmap.draw("route.html")
