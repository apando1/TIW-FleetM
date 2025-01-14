# Import necessary libraries and modules.
import json
from vda5050_interface.mqtt_clients.mqtt_subscriber import MQTTSubscriber
from vda5050_interface.interfaces.order_interface import OrderInterface

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
        self.agent = Agent(config_data=config_data, logging=logging)


class Agent:
    """
    Class representing a digital twin of an agent.
    """
    # TODO: Initialize the agent based on the AgentsInitialitation data and define necessary attributes.

    def __init__(self, config_data, logging) -> None:
        """
        Initialize the digital twin agent object.

        :param config_data: Data from the configuration file.
        :param logging: Logging object.
        """
        self.logging = logging
        self.mqtt_subscriber_state = MQTTSubscriber(config_data=config_data, logging=self.logging, on_message=self.state_callback,
                                                    channel="IMRL/fleet_management/agent_1/state", client_id='state_subscriber_agent_1')
        self.order_interface = OrderInterface(config_data=config_data, logging=self.logging,
                                              order_topic="IMRL/fleet_management/agent_1/order", agentId="1")
    
    def state_callback(self, client, userdata, msg) -> None:
        """
        Callback function for the MQTT message.

        :param client: MQTT client.
        :param userdata: User data.
        :param msg: Message.
        """
        self.logging.info(f"Client {self.mqtt_subscriber_state.client_id} received message from topic `{msg.topic}`.")  # `{msg.payload.decode()}`

        # TODO: Load the state message automatically.
