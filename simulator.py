# Gao-Rexford 
# 1. Route export: don't export routes learned from a peer or provider to another peer or provider
# 2. Global topology: provider-customer path is acyclic i.e. my customer's customer is not my provider 
# 3. Route selection: prefer routes through customers over routes through peers and providers
# Gauranteed to converge to unique stable solution
import sys
import queue

sys.path.append(".")

from common import EventType, Event, Route


class Node:
    def __init__(self, sim, name):
        self.sim = sim # The simulator that this node belongs to
        self.name = name # String representing the node's name - must be unique
        self.providers = [] # list of provider node names
        self.customers = [] # list of customer node names
        self.peers = [] # list of peer node names
        self.providerRoutes = {} # dictionary of routes that each provider is taking - key is string (provider node name), value is route
        self.customerRoutes = {} # dictionary of routes that each customer is taking - key is string (customer node name), value is route
        self.peerRoutes = {} # dictionary of routes that each peer is taking - key is string (peer node name), value is route
        self.finalRoute = None
        # self.routingPolicies = ? # for future, could be used to allow for preference functions
        # self.preferences = ? # for future, could be used to allow for preference functions
    
    # print node as a string
    def __str__(self):
        node_string = "Name: " + self.name + "\n"
        node_string += "Providers:\n"  
        for provider in self.providers:
            node_string += provider + "\n"
        node_string += "Customers:\n"
        for customer in self.customers:
            node_string += customer + "\n"
        node_string += "Peers:\n"
        for peer in self.peers:
            node_string += peer + "\n"
        node_string += "Provider routes:\n" + str(self.providerRoutes) + "\n"
        node_string += "Customer routes:\n" + str(self.customerRoutes) + "\n"
        node_string += "Peer routes:\n" + str(self.peerRoutes) + "\n"
        node_string += "Final route\n" + str(self.finalRoute) + "\n"
        return node_string

    # clear all routing tables
    def clear_tables(self):
        self.providerRoutes.clear()
        self.customerRoutes.clear()
        self.peerRoutes.clear()
        self.finalRoute = None

    # add a provider relationship to this node
    def addProvider(self, provider):
        self.providers.append(provider)

    # delete a provider relationship from this node
    def deleteProvider(self, provider):
        self.providers.remove(provider)
    
    # set route that provider node is using
    def updateProviderRoute(self, provider, route):
        self.providerRoutes[provider] = route

    # remove provider route from provider routes dictionary
    def deleteProviderRoute(self, provider):
        self.providerRoutes.pop(provider, None)

    # add a customer relationship to this node
    def addCustomer(self, customer):
        self.customers.append(customer)
    
    def deleteCustomer(self, customer):
        self.customers.remove(customer)

    # set route that customer node is using
    def updateCustomerRoute(self, customer, route):
        self.customerRoutes[customer] = route

    # remove customer route from customer routes dictionary
    def deleteCustomerRoute(self, customer):
        self.customerRoutes.pop(customer, None)

    # add a peer relationship to this node
    def addPeer(self, peer):
        self.peers.append(peer)

    def deletePeer(self, peer):
        self.peers.remove(peer)

    # set route that peer node is using
    def updatePeerRoute(self, peer, route):
        self.peerRoutes[peer] = route

    # remove peer route from peer routes dictionary
    def deletePeerRoute(self, peer):
        self.peerRoutes.pop(peer, None)

    # choose the best route out of the provided list of routes
    # choosePreferredRoute should never be called with an empty list
    def choosePreferredRoute(self, routes):
        # first check preference value
        # for now they are all equal
        # next find paths with shortest length
        shortestRoutes = []
        bestRoute = None
        for route in routes:
            if len(shortestRoutes) == 0:
                shortestRoutes.append(route)
                continue
            if len(route.path) < len(shortestRoutes[0].path):
                shortestRoutes = []
                shortestRoutes.append(route)
            elif len(route.path) == len(shortestRoutes[0].path):
                shortestRoutes.append(route)
        bestRoute = shortestRoutes[0]
        if len(shortestRoutes) > 1:
            # choose path with lowest next hop cost - don't have these values
            # choose route with lowest peer address
            for route in shortestRoutes:
                if route.path[1] < bestRoute.path[1]:
                    bestRoute = route
        # they all have unique names so this will result in one final route
        return bestRoute # might need to return shallow copy if doesn't do that already

    # start decision process to choose final route out of customer routes or peer and provider routes
    def chooseFinalRoute(self):
        # prefer customer path over peer and provider
        oldFinalRoute = self.finalRoute
        if self.customerRoutes: # will return false if the list is empty
            self.finalRoute = self.choosePreferredRoute(list(self.customerRoutes.values())) 
        elif self.peerRoutes or self.providerRoutes:
            self.finalRoute = self.choosePreferredRoute(list(self.peerRoutes.values()) + list(self.providerRoutes.values()))
        if self.finalRoute != oldFinalRoute:
            print("announcing best path")
            self.announceBestPath()
        else:
            print("old final route is")
            print(oldFinalRoute)


    # announce a new best route to appropriate neighbors based on the route
    def announceBestPath(self):
        finalRoute = self.finalRoute
        nextHop = finalRoute.path[1]
        if nextHop in self.providers:
            # only announce to customers
            # add announce route event to queue
            for customer in self.customers:
                announceEvent = Event(EventType.ROUTE_ADVERTISE, self.name, customer, finalRoute)
                self.sim.q.put(announceEvent)
        elif nextHop in self.peers:
            # only announce to customers
            # add announce route event to queue
            for customer in self.customers:
                announceEvent = Event(EventType.ROUTE_ADVERTISE, self.name, customer, finalRoute)
                self.sim.q.put(announceEvent)
        elif nextHop in self.customers:
            # announce to providers, customers, peers
            # add announce route event to queue
            for customer in self.customers:
                announceEvent = Event(EventType.ROUTE_ADVERTISE, self.name, customer, finalRoute)
                self.sim.q.put(announceEvent)
            for provider in self.providers:
                announceEvent = Event(EventType.ROUTE_ADVERTISE, self.name, provider, finalRoute)
                self.sim.q.put(announceEvent)
            for peer in self.peers:
                announceEvent = Event(EventType.ROUTE_ADVERTISE, self.name, peer, finalRoute)
                self.sim.q.put(announceEvent)

    # handle route advertisement message events - these are the only types of events implemented so far
    def handleEvent(self, event):
        # first check if you are in the route
        if event.route.checkPath(self.name):
            src = event.sourceNode # src is who announcement is coming from
            # delete any existing route you have stored for src peer/provider/customer
            if src in self.providers:
                self.deleteProviderRoute(src)
            elif src in self.customers:
                self.deleteCustomerRoute(src)
            elif src in self.peers:
                self.deletePeerRoute(src)
            # ignore/disregard new route with you in it
            # need to re-choose final route since routes changed
            self.chooseFinalRoute()
            return
        if event.eventType == EventType.ROUTE_ADVERTISE:
            src = event.sourceNode # src is who announcement is coming from
            meList = [self.name]
            newPath = meList + event.route.path
            newRoute = Route(event.route.dest, newPath)
            if src in self.providers:
                self.updateProviderRoute(src, newRoute)
            elif src in self.customers:
                self.updateCustomerRoute(src, newRoute)
            elif src in self.peers:
                self.updatePeerRoute(src, newRoute)
            # need to re-choose final route since routes changed
            self.chooseFinalRoute()
            return

class BGPSimulator:
    def __init__(self):
        self.numNodes = 0 # number of nodes in the network
        self.nodes = {} # dictionary with node name (string) as index and node (Node()) as value - stores all network nodes 
        self.q = queue.Queue() # queue of upcoming events 
        self.log = [] # in-order log of past events
        
    def __str__(self):
        sim_string = "Number of nodes: " + str(self.numNodes) + "\n"
        sim_string = sim_string + "Nodes:\n- - - - - - - - - - - - - -\n"
        for node in self.nodes.values():
            sim_string += str(node)
            sim_string += "- - - - - - - - - - - - - -\n"
        sim_string = sim_string + "Log: \n- - - - - - - - - - - - - -\n"
        for log_entry in self.log:
            sim_string += str(log_entry)
            sim_string += "- - - - - - - - - - - - - -\n"
        return sim_string

    def reset(self):
        nodes = list(self.nodes.values())
        for node in nodes:
            node.clear_tables()
        self.log = []

    def clear(self):
        self.reset()
        self.nodes = {}
        self.numNodes = 0
        self.q = queue.Queue()


    # returns false if unsuccessful - making sure that each new node has a unique name
    def add_node(self, nodeName):
        # check that node name is unique
        if nodeName in self.nodes:
            error = "Failed to add node \'" + nodeName + "' because node with that name already exists\n"
            return error, False
        new_node = Node(self, nodeName)
        self.nodes[nodeName] = new_node
        self.numNodes = self.numNodes + 1
        return "", True

    def delete_node(self, nodeName):
        if not nodeName in self.nodes:
            return "Couldn't delete node because it does not exist in network", False
        # delete node from relationship with other nodes
        for provider in self.nodes[nodeName].providers:
            self.nodes[provider].deleteCustomer(nodeName)
        for customer in self.nodes[nodeName].customers:
            self.nodes[customer].deleteProvider(nodeName)
        for peer in self.nodes[nodeName].peers:
            self.nodes[peer].deletePeer(nodeName)
        self.nodes.pop(nodeName)
        self.numNodes = self.numNodes - 1
        return "", True

    def add_peer_link(self, p1, p2):
        if not p1 in self.nodes:
            return "Couldn't add peer link because node not in network\n", False
        if not p2 in self.nodes:
            return "Couldn't add peer link because node not in network\n", False
        self.nodes[p1].addPeer(p2)
        self.nodes[p2].addPeer(p1)
        return "", True

    def add_pc_link(self, p, c):
        if not p in self.nodes:
            return "Couldn't add pc link because provider node not in network\n", False
        if not c in self.nodes:
            return "Couldn't add link because customer node not in network\n", False
        self.nodes[p].addCustomer(c)
        self.nodes[c].addProvider(p)
        return "", True

    def simulate(self, destination):
        # clear any previous simulations
        self.reset()
        if not destination in self.nodes:
            return "Couldn't simulate because destination node not in network", False
        dest_node_name = destination # dest_node is just name of dest node

        # give dest node a final route
        dest_node = self.nodes[dest_node_name]
        dest_route = Route(dest_node_name, [dest_node_name])
        dest_node.finalRoute = dest_route


        # announce dest_node's route to all its neighbors
        for provider in self.nodes[dest_node_name].providers:
            # add announce route event to queue
            announceEvent = Event(EventType.ROUTE_ADVERTISE, dest_node_name, provider, dest_route)
            self.q.put(announceEvent)
        for peer in self.nodes[dest_node_name].peers:
            # add announce route event to queue
            announceEvent = Event(EventType.ROUTE_ADVERTISE, dest_node_name, peer, dest_route)
            self.q.put(announceEvent)
        for customer in self.nodes[dest_node_name].customers:
            # add announce route event to queue
            announceEvent = Event(EventType.ROUTE_ADVERTISE, dest_node_name, customer, dest_route)
            self.q.put(announceEvent)

        count = 0

        # go through queue events
        while(not self.q.empty()):
            print("we got an event")
            qEvent = self.q.get()
            self.nodes[qEvent.destNode].handleEvent(qEvent) 
            self.log.append(qEvent)
            count = count+1
            if count > 10000:
                return "Event queue took too long to empty, might have route oscillation", False
        return "", True
        


# input format: filename.txt - ignore this
def main():

    # create and initialize BGPSimulator object
    sim = BGPSimulator()

    # take in and process user input (file name)
    file_name = sys.argv[1]  # [0] is the script name (.py file name)

    # will change input format later (GUI)
    input_file = open(file_name, 'r')

    # get contents of file and set up simulator
    count = 0
    for line in input_file:
        stripped_line = line.strip()
        print(stripped_line)
        if count == 0:
            sim.numNodes = int(stripped_line)
        elif count >= 1 and count <= sim.numNodes: # better to just make a num_nodes variable? or no?
            # create a new node and add to node list for sim
            new_node = Node(sim, stripped_line)
            sim.nodes[stripped_line] = new_node
        elif count > sim.numNodes:
            # add node relationship to sim
            relation = stripped_line.split()
            if relation[1] == "=":
                # peer
                peer1 = relation[0]
                peer2 = relation[2]

                sim.nodes[peer1].addPeer(peer2)
                sim.nodes[peer2].addPeer(peer1)
            elif relation[1] == "->":
                # provider customer
                provider = relation[0]
                customer = relation[2]

                sim.nodes[provider].addCustomer(customer)
                sim.nodes[customer].addProvider(provider)
            else:
                # error
                print("incorrect relationship type, see input_format.txt")
                exit()
        count+=1

    
            

if __name__ == "__main__":
    main()