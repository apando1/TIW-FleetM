# Import necessary libraries and modules.

class Graph:
    """
    Class representing the graph, based on which the agents are controlled by the fleet manager.
    """
    # TODO: Model the graph based on the LIF data.

    def __init__(self, lif_data):
        # Define the dictionaries to store the data: nodes, edges, stations
        # Initializes the graph by calling _initialize_graph, 
        # which populates the dictionaries with the LIF data.
        
        self.nodes = {}
        self.edges = {}
        self.stations = {}
        self.initialize_graph(lif_data)
    
    def initialize_graph(self,lif_data): 
        #Extracts nodes, edges, and stations from the LIF data
        
        layout = lif_data["layouts"][0]  # Assumed a single layout

        # Process nodes.
        for node in layout["nodes"]: # iteration through all nodes in the file
            self.nodes[node["nodeId"]] = { #identifier of the node
                "position": node["nodePosition"], #x,y coordinates
                "vehicleTypes": [vt["vehicleTypeId"] for vt in node["vehicleTypeNodeProperties"]] #List of vehicleTypeId 
                #For loop, in case many types are possible
            }

        # Process edges.
        for edge in layout["edges"]:
            self.edges[edge["edgeId"]] = { #identifier of the edge
                "start": edge["startNodeId"], # nodes connected
                "end": edge["endNodeId"], # nodes connected
                "vehicleTypes": [ #List of vehicleTypeId and whether rotation is allowed
                    {
                        "vehicleTypeId": vt["vehicleTypeId"],
                        "rotationAllowed": vt["rotationAllowed"]
                    }
                    for vt in edge["vehicleTypeEdgeProperties"]
                ] #For loop, in case many types are possible
            }

        # Process stations.
        for station in layout["stations"]: 
            self.stations[station["stationId"]] = { #identifier of the station
                "interactionNodes": station["interactionNodeIds"], #nodes associated with station
                "position": station["stationPosition"] # x, y coordinates and rotation angle (theta) of station
            }

    def get_neighbors(self, node_id): 
        # Identifying all nodes directly connected to every node
        # Find and return neighboring nodes of a given node
        
        neighbors = []
        for edge in self.edges.values(): # Iterates over all edge dictionaries stored in self.edges
            if edge["start"] == node_id: # checking if the node is start of end of an edge
                neighbors.append(edge["end"]) #add the other node of the edge to the neighbors list
            elif edge["end"] == node_id:
                neighbors.append(edge["start"])
        return neighbors # To return the list of neighboring node IDs.
        
    def __repr__(self): 
        # Provide a summary of the graph
       
        return f"Graph(nodes={len(self.nodes)}, edges={len(self.edges)}, stations={len(self.stations)})"
    
