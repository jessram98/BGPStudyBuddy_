from enum import Enum

class EventType(Enum):
    ROUTE_ADVERTISE = 1
    ROUTE_WITHDRAW = 2

class Event:
    def __init__(self, eventType, source, dest, route):
        self.eventType = eventType # currently only support route_advertise event types
        self.sourceNode = source # string - source node is name of node that is doing announcing
        self.destNode = dest # string - destination node is name of node you are announcing to
        self.route = route # route object

    def __str__(self):
        string = ""
        if self.eventType == EventType.ROUTE_ADVERTISE:
            string += "Node " + self.sourceNode + " announced to node " + self.destNode + ": \n" + str(self.route) + "\n"
        elif self.eventType == EventType.ROUTE_WITHDRAW:
            pass
        return string

    def __repr__(self):
        return str(self)

class Route:
    def __init__(self, dest, path):
        self.dest = dest # the name of the end destination node of this path
        self.path = path # ordered list of names of ASes in path

    def __str__(self):
        string = "Route to node " + self.dest + ":\n" + str(self.path) + "\n"
        return string

    def __repr__(self):
        return str(self)

    # def addNode(self, node):
    #     self.path = [node] + self.path

    def nextHop(self):
        return self.path[0]

    # check if node is in path
    def checkPath(self, node):
        if node in self.path:
            return True
        return False

    
        