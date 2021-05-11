from kivy.app import App
from kivy.graphics import Rectangle 
from kivy.graphics import Color
from kivy.graphics import Line 
from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty, ObjectProperty, NumericProperty, DictProperty
from kivy.uix.button import Button 
from kivy.uix.label import Label 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from simulator import BGPSimulator, Node

import math

#Define our different screens
class WelcomeScreen(Screen):
    pass

# fixed node is just a node that doesn't move - used for simulator screen
class FixedNode(Widget):
    node_name = StringProperty()
    plinks = ListProperty()
    pclinks = ListProperty()

class NodeG(Widget):
    node_name = StringProperty()
    #links = ListProperty()
    plinks = ListProperty()
    pclinks = ListProperty()

    # if mouse touch down is on me, claim the touch - so it won't affect any other nodes that the touch down might also be touching
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            return True

    # if touch_move, check if you own the touch, if you do, move the node with the touch_move
    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            if touch.grab_current is self:
                self.center = touch.pos
                for link in self.plinks:
                        link.points[0] = link.nodes[0].center_x
                        link.points[1] = link.nodes[0].center_y
                        link.points[2] = link.nodes[1].center_x
                        link.points[3] = link.nodes[1]. center_y
                for link in self.pclinks:
                        link.points[0] = link.nodes[0].center_x
                        link.points[1] = link.nodes[0].center_y
                        link.points[2] = link.nodes[1].center_x
                        link.points[3] = link.nodes[1]. center_y
                        link.custIndicator.update_pos(link)
            return True

    # on touch_up unclaim the touch
    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            return True


class PeerLink(Widget):
    points = ListProperty()
    nodes = ListProperty()

# Widget for dot that indicates customer in p-c link
class CustIndicator(Widget):
    # update the position of the dot to match where the arrow line is as best as possible
    def update_pos(self, link):
        if link.nodes[1].center_x != link.nodes[0].center_x:
            m = (float) (link.nodes[1].center_y - link.nodes[0].center_y) / (float) (link.nodes[1].center_x - link.nodes[0].center_x)
            if (link.nodes[1].center_y - link.nodes[0].center_y) < 0:
                # then customer is below provider
                if (link.nodes[1].center_x - link.nodes[0].center_x) < 0:
                    # then customer is left of provider
                    x = link.nodes[1].center_x + (25.0 * math.sqrt(1/(1+(m*m))))
                    y = link.nodes[1].center_y + (m * 25.0 * math.sqrt(1/(1+(m*m))))
                elif (link.nodes[1].center_x - link.nodes[0].center_x) > 0:
                    # then customer is right of provider
                    x = link.nodes[1].center_x - (25.0 * math.sqrt(1/(1+(m*m))))
                    y = link.nodes[1].center_y - (m * 25.0 * math.sqrt(1/(1+(m*m))))
            elif (link.nodes[1].center_y - link.nodes[0].center_y) > 0:
                # then customer is above provider
                if (link.nodes[1].center_x - link.nodes[0].center_x) < 0:
                    # then customer is left of provider
                    x = link.nodes[1].center_x + (25.0 * math.sqrt(1/(1+(m*m))))
                    y = link.nodes[1].center_y + (m * 25.0 * math.sqrt(1/(1+(m*m))))
                elif (link.nodes[1].center_x - link.nodes[0].center_x) > 0:
                    # then customer is right of provider
                    x = link.nodes[1].center_x - (25.0 * math.sqrt(1/(1+(m*m))))
                    y = link.nodes[1].center_y - (m * 25.0 * math.sqrt(1/(1+(m*m))))
            elif (link.nodes[1].center_y - link.nodes[0].center_y) == 0:
                # then customer is at same height as provider
                if (link.nodes[1].center_x - link.nodes[0].center_x) < 0:
                    # then customer is left of provider
                    x = link.nodes[1].center_x + (25.0 * math.sqrt(1/(1+(m*m))))
                    y = link.nodes[1].center_y - (m * 25.0 * math.sqrt(1/(1+(m*m))))
                elif (link.nodes[1].center_x - link.nodes[0].center_x) > 0:
                    # then customer is right of provider
                    x = link.nodes[1].center_x - (25.0 * math.sqrt(1/(1+(m*m))))
                    y = link.nodes[1].center_y - (m * 25.0 * math.sqrt(1/(1+(m*m))))
        else:
            if (link.nodes[1].center_y - link.nodes[0].center_y) < 0:
                # then customer is below provider
                y = link.nodes[1].center_y + 25.0
                x = link.nodes[1].center_x
            elif (link.nodes[1].center_y - link.nodes[0].center_y) > 0:
                # then customer is above provider
                y = link.nodes[1].center_y - 25.0
                x = link.nodes[1].center_x
        self.pos = (x,y)

class PCLink(Widget):
    points = ListProperty()
    cust_pos = ObjectProperty(None)
    nodes = ListProperty()
    custIndicator = ObjectProperty(None)

class NetworkCanvas(Widget):
    node_count = NumericProperty(0)
    # dictionary of all nodes on canvas
    node_widgets = DictProperty()
    # list of all canvas links
    plinks = ListProperty()
    pclinks = ListProperty()

    def add_node(self, nodeName):
        # id = nodeName + "__" + str(self.node_count)
        err, ok = sim.add_node(nodeName)
        if not ok:
            print(err)
            return

        temp_node = NodeG()
        temp_node.center = self.center
        # temp_node.node_id = id
        temp_node.node_name = nodeName
        
        self.add_widget(temp_node)
        self.node_widgets[nodeName] = temp_node
        self.node_count = self.node_count + 1

    def add_fixed_node(self, node):
        temp_node = FixedNode()
        temp_node.center = node.center 
        temp_node.node_name = node.node_name

        self.node_widgets[temp_node.node_name] = temp_node
        self.node_count = self.node_count + 1
        self.add_widget(temp_node)

    def delete_node(self, nodeName):
        # delete node from underlying simulator
        err, ok = sim.delete_node(nodeName)
        if not ok:
            print(err)
            return

        # delete any links connected to the node 
        # remove link from other node's link list and from canvas
        for link in self.node_widgets[nodeName].plinks:
            self.remove_widget(link)
            self.plinks.remove(link)
            for node in link.nodes:
                if node.node_name != nodeName:
                    node.plinks.remove(link)

        for link in self.node_widgets[nodeName].pclinks:
            self.remove_widget(link)
            self.pclinks.remove(link)
            for node in link.nodes:
                if node.node_name != nodeName:
                    node.pclinks.remove(link)

        # delete node from canvas
        self.remove_widget(self.node_widgets[nodeName])

        # delete node from simulator GUI 
        self.node_widgets.pop(nodeName)
        self.node_count = self.node_count - 1

    def add_peer_link(self, p1, p2, mod_sim=True, color=Color(204/255,204/255,204/255)):
        if (mod_sim):
            err, ok = sim.add_peer_link(p1, p2)
            if not ok:
                print(err)
                return

        temp_peer_link = PeerLink()

        temp_peer_link.canvas.before.add(color)

        # add the node link to each peer's link list
        self.node_widgets[p1].plinks.append(temp_peer_link)
        self.node_widgets[p2].plinks.append(temp_peer_link)

        # add peer nodes to the link's node list
        temp_peer_link.nodes.append(self.node_widgets[p1])
        temp_peer_link.nodes.append(self.node_widgets[p2])

        temp_peer_link.points.append(self.node_widgets[p1].center_x)
        temp_peer_link.points.append(self.node_widgets[p1].center_y)
        temp_peer_link.points.append(self.node_widgets[p2].center_x)
        temp_peer_link.points.append(self.node_widgets[p2].center_y)

        self.plinks.append(temp_peer_link)
        self.add_widget(temp_peer_link)
        return temp_peer_link

    def add_pc_link(self, p, c, mod_sim=True, color=Color(150/255,150/255,150/255)):
        if (mod_sim):
            err, ok = sim.add_pc_link(p,c)
            if not ok:
                print(err)
                return

        temp_pc_link = PCLink()
        temp_pc_link.canvas.before.add(color)


        # add the node link to each node's link list
        self.node_widgets[p].pclinks.append(temp_pc_link)
        self.node_widgets[c].pclinks.append(temp_pc_link)

        # add provider and customer nodes to the link's node list
        temp_pc_link.nodes.append(self.node_widgets[p])
        temp_pc_link.nodes.append(self.node_widgets[c])

        #c = self.node_widgets[c].pos

        # with temp_pc_link.canvas.after:
        #     Color(rgb=(0,0,1))
        #     Line(ellipse=(pos=(self.node_widgets[c].pos), size=(10,10)))

        temp_pc_link.custIndicator.update_pos(temp_pc_link)

        temp_pc_link.points.append(self.node_widgets[c].center_x)
        temp_pc_link.points.append(self.node_widgets[c].center_y)

        temp_pc_link.points.append(self.node_widgets[p].center_x)
        temp_pc_link.points.append(self.node_widgets[p].center_y)

        self.pclinks.append(temp_pc_link)
        self.add_widget(temp_pc_link)
        return temp_pc_link

    def clear(self):
        for key in self.node_widgets:
            # clear all nodes and links from the network canvas    
            for link in self.node_widgets[key].plinks:
                self.remove_widget(link)
            for link in self.node_widgets[key].pclinks:
                self.remove_widget(link)
            self.remove_widget(self.node_widgets[key])


        # remove all nodes from the network canvas's node dictionary
        self.node_widgets.clear()

        # remove all the links from the network canvas's link lists
        self.pclinks.clear()
        self.plinks.clear()
        self.node_count = 0


class SetupScreen(Screen):
    network_canvas = ObjectProperty(None)
    peerlink = ObjectProperty(None)
    pclink = ObjectProperty(None)
    node_name = ObjectProperty(None)
    delete_node_name = ObjectProperty(None)

    def add_nodes(self, nodes):
        node_list = nodes.strip()
        node_list = node_list.split()
        for node in node_list:
            self.network_canvas.add_node(node)

    def delete_nodes(self, nodes):
        node_list = nodes.strip()
        node_list = node_list.split()
        for node in node_list:
            self.network_canvas.delete_node(node)

    # parse link info input
    def add_peer_relationship(self):
        rel = self.peerlink.text
        rel = rel.strip()
        rel = rel.split()
        if len(rel) != 3:
            print("Incorrect peer relationship format")
            return
        p1 = rel[0]
        p2 = rel[2]
        self.network_canvas.add_peer_link(p1,p2)
    
    # parse link info input
    def add_pc_relationship(self):
        rel = self.pclink.text
        rel = rel.strip()
        rel = rel.split()
        if len(rel) != 3:
            print("Incorrect pc relationship format")
            return
        p = rel[0]
        c = rel[2]
        self.network_canvas.add_pc_link(p,c)

    def reset_text_inputs(self):
        self.pclink.text = "p -> c"
        self.peerlink.text = "p = p"
        self.node_name.text = ""
        self.delete_node_name.text = ""


    def populate_sim_screen(self):
        # self.parent.sim_screen.network_canvas = self.network_canvas <--- this does not work unfortunately
        for key in self.network_canvas.node_widgets:
            self.parent.sim_screen.final_network_canvas.add_fixed_node(self.network_canvas.node_widgets[key])

        for link in self.network_canvas.plinks:
            self.parent.sim_screen.final_network_canvas.add_peer_link(link.nodes[0].node_name, link.nodes[1].node_name, False)
        
        for link in self.network_canvas.pclinks:
            self.parent.sim_screen.final_network_canvas.add_pc_link(link.nodes[0].node_name, link.nodes[1].node_name, False)


class SimulationScreen(Screen):
    dest_node = ObjectProperty(None)
    results = ObjectProperty(None)
    final_network_canvas = ObjectProperty(None)
    final_route_links = ListProperty()

    # To show the results, instead of changing the color of chosen paths, I just draw over them in black
    def simulate(self):
        self.results.text = ""
        for link in self.final_route_links:
            self.final_network_canvas.remove_widget(link)
        self.final_route_links.clear()
        dest = self.dest_node.text.strip()
        err, ok = sim.simulate(dest)
        if not ok:
            self.results.text = err
            return
        self.results.text = str(sim)
        for node in sim.nodes:
            # node is node_name
            if sim.nodes[node].finalRoute is not None:
                if len(sim.nodes[node].finalRoute.path) == 1:
                    continue
                node2 = sim.nodes[node].finalRoute.path[1]
                if sim.nodes[node].finalRoute.path[1] in sim.nodes[node].providers:
                    self.final_route_links.append(self.final_network_canvas.add_pc_link(node2, node, False, Color(0,0,0)))
                elif sim.nodes[node].finalRoute.path[1] in sim.nodes[node].customers:
                    self.final_route_links.append(self.final_network_canvas.add_pc_link(node, node2, False, Color(0,0,0)))
                elif sim.nodes[node].finalRoute.path[1] in sim.nodes[node].peers:
                    self.final_route_links.append(self.final_network_canvas.add_peer_link(node, node2, False, Color(0,0,0)))


    def edit_network(self):
        self.final_network_canvas.clear()
        self.results.text = ""
    
    def start_over(self):
        sim.clear()
        self.results.text = ""
        self.dest_node.text = ""
        self.parent.setup.reset_text_inputs()
        self.final_network_canvas.clear()
        self.parent.setup.network_canvas.clear()
        
class WindowManager(ScreenManager):
    setup = ObjectProperty(None)
    sim_screen = ObjectProperty(None)

kv = Builder.load_file("simulatorGUI.kv")
sim = BGPSimulator()

class BGPStudyBuddyApp(App):
    def build(self):
        return kv

if __name__ == '__main__':
    BGPStudyBuddyApp().run()