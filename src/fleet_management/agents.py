# Import necessary libraries and modules.
import json
from vda5050_interface.mqtt_clients.mqtt_subscriber import MQTTSubscriber
from vda5050_interface.interfaces.order_interface import OrderInterface

class Agent:
    """
    Class representing a digital twin of an agent.
    """
    # TODO: Initialize the agent based on the AgentsInitialitation data and define necessary attributes.

    def __init__(self, agent_data, logging) -> None:
        # Initializaition based on AgentsInitialization file
        """
        Initialize the digital twin agent object.

        :param config_data: Data from the configuration file.
        :param logging: Logging object.
        """
        # Attributes
        self.logging = logging # log messages during the agent's lifecycle.
        self.agentId = agent_data["agentId"] # identifier for the agent
        self.stateTopic = agent_data["stateTopic"] # MQTT topic where agent's state updates is published
        self.orderTopic = agent_data["orderTopic"] # MQTT topic where agent receives orders
        self.agentPosition = agent_data["agentPosition"]  # Position of agent {x, y, theta}
        self.agentVelocity = agent_data["agentVelocity"] # Velocity of agent
        self.agentRotationVelocity = agent_data["agentRotationVelocity"] # Rotation velocity of agent
        #Extra attributes
        self.currentState = None  # agent's current state (e.g., idle, moving)
        self.currentNode = None  # Current node at which is the agent
        self.currentTask = None  # Current task assigned to agent
    
        # MQTT Suscribers for state and order
        # Agent suscribes to stateTopic to receive state updates
        self.mqtt_subscriber_state = MQTTSubscriber(config_data=config_data, logging=self.logging, on_message=self.state_callback,
                                                    channel="IMRL/fleet_management/agent_1/state", client_id='state_subscriber_agent_1')
        # agent uses the this orderInterface to receive orderTopic
        self.order_interface = OrderInterface(config_data=config_data, logging=self.logging,
                                              order_topic="IMRL/fleet_management/agent_1/order", agentId="1")
    
    # to handle incoming MQTT messages
    # When the agent receives a state update, this method is triggered
    def state_callback(self, client, userdata, msg) -> None:
        """
        Callback function for the MQTT message.

        :param client: MQTT client.
        :param userdata: User data.
        :param msg: Message.
        """
        self.logging.info(f"Client {self.mqtt_subscriber_state.client_id} received message from topic {msg.topic}.")
        # stated is logged and agent's state is updated 
        # TODO: Parse and update the agent's state based on the message

    # def update_task(self, task) -> None:
    #     """
    #     Assign a new task to the agent.

    #     :param task: The task to assign.
    #     """
    #     self.current_task = task
    #     self.logging.info(f"Agent {self.agent_id} assigned task: {task}")


# To handle all agents (digital twins)
class Agents:
    """
    Class representing the digital twins of the agents controlled by the fleet manager.
    """
    # TODO: Initialize all agents based on the AgentsInitialitation data.

    def __init__(self, config_data, logging) -> None:
        """
        Initialize the Agents object.

        :param config_data: Data from the configuration file.
        :param logging: Logging object.
        """
        self.agents = []  # List to store agent objects
        self.logging = logging

        # in case key is missing
        # if "agents_initialization" not in config_data:
        #     self.logging.error("Missing 'agents_initialization' in config data.")
        #     sys.exit(1)

        # extracts the initialization data of agents from file
        agents_initialization_data = config_data["agents_initialization"]
        
        # for each agent in the agents_initialization_data
        # is created a new Agent and added to self.agents
        for agent_data in agents_initialization_data["agents"]:
            agent = Agent(agent_data=agent_data, logging=self.logging)
            self.agents.append(agent)
            self.logging.info(f"Initialized agent {agent.agentId} at position {agent.agentPosition}")

    # Retrieve an agent by its agentId
    def get_agent_by_id(self, agent_id: str) -> Agent: #  parameter is the ID of the agent and returns Agent or None
        """
        Retrieve an agent by its ID.

        :param agent_id: The ID of the agent.
        :return: The corresponding Agent object.
        """
        # Searches for an agent by its agentId. 
        # If one is found, returns the agent.
        for agent in self.agents:
            if agent.agentId == agent_id:
                return agent
        self.logging.error(f"Agent with ID {agent_id} not found.")
        return None
        # If not, it logs an error and returns None.
    
    
    # def update_agent_task(self, agent_id, task):
    #     """
    #     Update the task for a specific agent.

    #     :param agent_id: The ID of the agent.
    #     :param task: The task to assign.
    #     """
    #     agent = self.get_agent(agent_id)
    #     if agent:
    #         agent.update_task(task)
    #     else:
    #         self.logging.warning(f"Agent {agent_id} not found.")


