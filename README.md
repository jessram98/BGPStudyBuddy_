# BGPStudyBuddy
Welcome to the BGP Study Buddy Github Repository!

# Set up
In order to use the simulator, you must have Python and Kivy downloaded. If you don't have Kivy, follow the instructions [here](https://kivy.org/doc/stable/gettingstarted/installation.html#install-python) to download Kivy. If you don't have Python, follow the instructions at the same link to download Python. You will need to have python before you can get Kivy.

Once your environment is set up with Python and Kivy dependencies, download the simulator files in this repository and save them in a file where you can access Kivy and Python.

# Starting the simulator
In order to start the simulator, run the following command: 
    python simulatorGUI.py

You should see a window pop up with the welcome screen displayed. It should look like this:

![Image of WelcomeScreen](https://github.com/jessram98/BGPStudyBuddy_/blob/e6a8f3b0fb48085f84937f1a74d667c1bfca934d/WelcomeScreen.png)

Click the 'Let's Get Started!' button at the bottom of the page to get started and enter the network setup page.

# Setting up the network
The network setup page looks like this: 

[NetworkSetup](https://github.com/jessram98/BGPStudyBuddy_/blob/c511cbff185eb64d15ddb5bdaf4b5c1c746395df/NetworkSetupScreen.png)

The pane on the left is where you can input network information. The pane on the right is where the graph visualiation appears.

To add a node, type the node name in the node name text field above the add node button. This name MUST be unique to names of any nodes already in the network. Once the name is in the text box, click add Node. The node is now in the network and should appear in the right pane. You can click the node around.

To add multiple nodes at once, input node names separated by one space each. It must be in this format to work.

Follow the same procedure for delete node.

To add peer links, write the node names in the peer link text field in the format displayed. The peer node names must be separated by a single equal sign and it MUST have spaces between the equal sign and the peer node names. For example, this is how you would add a peer link between nodes v and x:

    v = x
    
To add p-c links, follow the same procedure except instead of putting an equal sign between the provider and customer node, put an arrow like this one: ->  The provider node should be on the left side and the customer node should be on the right side.

Once all nodes and links have been added and you have clicked and dragged each node into the positions you would like, the network set up screen should look something like this:

[network screen 2](https://github.com/jessram98/BGPStudyBuddy_/blob/e94496ba0f711a22cec44a31f5a5fc34358a225f/NetworkSetupScreenWithNetwork.png)

Finally, click I'm done setting up to finalize your network.

# Simulation screen
Once you are done setting up the network and reach the simulation screen, should see your graph has transferred over to this screen, except the nodes are no longer click-and-draggable. It should look something like this:
[sim screen](https://github.com/jessram98/BGPStudyBuddy_/blob/a28a6e7c3b04ae61457917a6487ef3fdfb34e50a/SimulationScreenInit.png)

To start a simulation, enter the destination node name into the text field and click simulate. 

The screen should look like this once the simulation is complete:
[sim screen 2](https://github.com/jessram98/BGPStudyBuddy_/blob/e94496ba0f711a22cec44a31f5a5fc34358a225f/SimulationScreenResults.png)

The paths that are now black in the graph are the paths that were chosen by each node. If a node is not connected to a black path, that means it does not have a valid path to the destination node.

In the left pane, there is also a more detailed text-based version of the results. It contains information about each node. At the bottom of these results is a log showing the order of events that led up to the final result. 

The log should look like this: 
[log](https://github.com/jessram98/BGPStudyBuddy_/blob/e94496ba0f711a22cec44a31f5a5fc34358a225f/SimulationScreenWithResults.png)

You can keep putting new destination node values to see the different outcomes. Or you can go back and edit the network or completely start over by clicking one of the buttons in the left pane.


