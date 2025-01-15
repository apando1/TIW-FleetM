import logging
from collections import deque

class FleetManagement:
    """
    Class for managing the fleet of agents. Pathfinding with collision avoidance.
    """

    def __init__(self, agents_object, graph_object) -> None:
        """
        Initialize the fleet management object.

        :param agents_object: The agents object containing the digital twin agents.
        :param graph_object: The graph object representing the map.
        """
        self.agents = agents_object # Manages agents: positions and availability
        self.graph = graph_object # Manages the graph

    def find_path(self, start_node: str, end_node: str) -> list:
        """
        Find the shortest path between two nodes using BFS.

        :param start_node: The starting node ID.
        :param end_node: The ending node ID.
        :return: A list of node IDs representing the path from start to end.
        """
        visited = set()
        queue = deque([(start_node, [])])  # (current_node, path_so_far)

        while queue:
            current_node, path = queue.popleft()

            if current_node == end_node:
                return path + [current_node]

            if current_node not in visited:
                visited.add(current_node)
                neighbors = self.graph.get_neighbors(current_node)

                for neighbor in neighbors:
                    if neighbor not in visited:
                        queue.append((neighbor, path + [current_node]))

        logging.warning(f"No path found from {start_node} to {end_node}.")
        return []

    def execute_task(self, agent_id: str, task: dict) -> None:
        #Planning the path from the agent's current position to the task's start station.
        #Planning the path from the start station to the goal station.
        #Simulating the agent's movement along the combined path.

        """
        Execute a task by planning and following the path.

        :param agent_id: The ID of the agent executing the task.
        :param task: The task to execute.
        """
        start_station = task["startStationId"]
        goal_station = task["goalStationId"]

        # Get the agent's current position.
        agent_position = self.agents.get_agent_position(agent_id)

        # Plan path to the start station.
        path_to_start = self.find_path(agent_position, start_station)
        if not path_to_start:
            logging.error(f"Agent {agent_id} could not find a path to start station {start_station}.")
            return

        # Plan path from start to goal station.
        path_to_goal = self.find_path(start_station, goal_station)
        if not path_to_goal:
            logging.error(f"Agent {agent_id} could not find a path to goal station {goal_station}.")
            return

        # Combine paths.
        full_path = path_to_start + path_to_goal[1:]  # Avoid duplicating the start station.

        # Simulate the agent following the path.
        # Log the agent's movements and task completion.
        logging.info(f"Agent {agent_id} executing task {task['transportationTaskId']}.")
        for node in full_path:
            self.agents.update_agent_position(agent_id, node)
            logging.info(f"Agent {agent_id} moved to {node}.")

        logging.info(f"Agent {agent_id} completed task {task['transportationTaskId']}.")
    
    # Manages the execution of all tasks in the task list
    def run_fleet_management(self, tasks: list) -> None:
        """
        Run the fleet management process to execute all tasks.

        :param tasks: A list of tasks to execute.
        """
        #For each task, retrieve an available agent
        # If an agent is available, call execute_task
        # If no agent is available, log a warning
        for task in tasks:
            agent = self.agents.get_available_agents()[0]  # Get the first available agent.
            if agent:
                self.execute_task(agent["id"], task)
            else:
                logging.warning(f"No available agents for task {task['transportationTaskId']}.")
