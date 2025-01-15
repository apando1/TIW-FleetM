# Import required libraries and modules.

class TaskAssignment:
    """
    Class for assigning tasks to the agents.
    """
    # TODO: Implement the task assignment algorithm.
    # Logic for assigning tasks to robots

    def __init__(self) -> None:
        #Attributes
        # Manages robots
        self.agents = agents_object
        # Information about the map
        self.graph = graph_object

    def calculate_distance(self, start_node_id: str, end_node_id: str) -> float:
        # Calculate the shortest distance between two nodes using the graph structure
        # This assumes a simple breadth-first search (BFS) to find the shortest path
        from collections import deque

        visited = set() # To keep track of nodes already analyzed
        # A deque (double-ended queue) used to store nodes to explore, 
        # along with the cumulative distance to reach them.
        queue = deque([(start_node_id, 0)])  # (current_node, cumulative_distance)
        
        # loop runs as long as there are nodes to explore in the queue
        while queue:
            current_node, distance = queue.popleft()
            #Extract the current node and the cumulative distance from the front of the queue

            if current_node == end_node_id:
                return distance #If the current node is the final node, return the cumulative distance
                                

            if current_node not in visited: #If the current node hasn't been visited yet
                visited.add(current_node) #mark it as visited to prevent processing it again
                neighbors = self.graph.get_neighbors(current_node) #retrieve neighbors from graph
                #explore neighbors
                for neighbor in neighbors: # retrieve all nodes directly connected 
                    edge = next(
                        (
                            
                            #Identify the edge connecting the current node to its neighbor
                            # use of a generator that searches through the edges dictionary
                            e
                            for e in self.graph.edges.values()
                            if (e["start"] == current_node and e["end"] == neighbor)
                            or (e["start"] == neighbor and e["end"] == current_node)
                        ),
                        None,
                    )
                    #If an edge exists, add the neighbor to the queue and update cum distance
                    if edge:
                        queue.append((neighbor, distance + 1))  # Edge weight is 1 for simplicity

        return float("inf")  # Return infinity if no path is found
    
    def get_available_robot(self, start_station_id: str) -> dict:
        # Get the closest available robot to a station
        # start_station_id: The ID of the start station
        # return The closest available robot or None
        
        available_agents = [agent for agent in self.agents.get_available_agents()]
        if not available_agents:
            return None

        closest_agent = min(
            available_agents,
            key=lambda agent: self.calculate_distance(agent["position"], start_station_id)
        )
        return closest_agent

    def assign_task(self, task: dict) -> bool:
        # Assign a task to the closest available robot
        # task: The task to assign
        # Return True if the task was successfully assigned, False otherwise
        
        start_station = task["startStationId"]
        agent = self.get_available_robot(start_station)
        if agent:
            self.agents.assign_task(agent["id"], task)
            logging.info(f"Assigned task {task['transportationTaskId']} to agent {agent['id']}.")
            return True
        else:
            logging.warning(f"No available agent for task {task['transportationTaskId']}.")
            return False
