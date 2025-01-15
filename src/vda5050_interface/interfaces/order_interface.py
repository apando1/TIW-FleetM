import json
from vda5050_interface.mqtt_clients.mqtt_publisher import MQTTPublisher

class OrderInterface:
    def __init__(self, config_data:dict, logging:object, order_topic:str, agentId:str) -> None:
        """
        Initialize the OrderInterface class.

        :param config_data: Data from the configuration file.
        :param logging: Logging object.
        :param order_topic: MQTT topic for the order messages.
        :param agentId: The ID of the agent.
        """
        self.config_data = config_data
        self.order_topic = order_topic
        self.logging = logging
        self.agentId = agentId
        self.mqtt_publisher = MQTTPublisher(config_data=config_data, channel=order_topic,
                                            client_id=f'order_publisher_agent_{self.agentId}', logging=self.logging)

    def generate_order_message(self) -> None:
        """
        Generate the VDA5050 order message.
        """
        # TODO: Implement the automatic generation of the order message.

        # Load the example order message.
        order_msg_path = "data/input_files/OrderMessage_Example.json"
        with open(order_msg_path, 'r') as order_msg_file:
            order_msg = json.load(order_msg_file)

        # Publish the order message.
        self.mqtt_publisher.publish(order_msg, qos=0)



    def generate_order_message(self) -> None:
    # Generate the VDA5050 order message dynamically and publish it.
    # Dynamically create the order message based on the current task or agent
    order_msg = {
        "headerId": 1,
        "timestamp": "2024-11-29T14:49:32.4926Z",  # You can replace this with the current time
        "version": "V2.1.0",
        "manufacturer": "IFL",
        "serialNumber": f"IFL_{self.agentId}",
        "orderId": str(self.agentId),  # Use agentId or other unique identifiers
        "orderUpdateId": 0,
        "nodes": [
            {
                "nodeId": f"N{self.agentId}",  # Example: Dynamically set nodeId
                "sequenceId": 1,
                "released": True,
                "nodePosition": {
                    "x": 1,
                    "y": 2,
                    "mapId": "Map_1"
                },
                "actions": [
                    {
                        "actionType": "pick",
                        "actionId": f"{self.agentId}-action-pick",
                        "blockingType": "HARD"
                    }
                ]
            }
        ],
        "edges": [
            {
                "edgeId": "E1",
                "sequenceId": 2,
                "released": True,
                "startNodeId": "N1",
                "endNodeId": "N3",
                "actions": []
            }
        ]
    }

    # Publish the order message using MQTT publisher
    self.mqtt_publisher.publish(order_msg, qos=0)
    self.logging.info(f"Order message generated and published for agent {self.agentId}.") 


    def state_callback(self, client, userdata, msg) -> None:
        """
        Callback function for the MQTT message that updates the agent's state.
        
        :param client: MQTT client.
        :param userdata: User data.
        :param msg: Message.
        """
        self.logging.info(f"Client {self.mqtt_subscriber_state.client_id} received message from topic {msg.topic}.")
        
        # Parse the state message (assuming JSON format)
        state_msg = json.loads(msg.payload.decode("utf-8"))
        
        # Example: Update the agent's state based on the message content
        if "state" in state_msg:
            self.currentState = state_msg["state"]
            self.logging.info(f"Updated agent {self.agentId} state to {self.currentState}")
        
        if "nodeId" in state_msg:
            self.currentNode = state_msg["nodeId"]
            self.logging.info(f"Agent {self.agentId} is at node {self.currentNode}")
        
        if "taskId" in state_msg:
            self.currentTask = state_msg["taskId"]
            self.logging.info(f"Agent {self.agentId} is performing task {self.currentTask}")
        
        # Additional state attributes can be updated here if necessary