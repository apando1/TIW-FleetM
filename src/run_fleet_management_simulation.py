# Import the necessary libraries and modules.
import os
import sys
import json
import time
import logging
import subprocess
from typing import Dict

# Add the path to the src directory to the system path.
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

# Import the necessary classes.
from fleet_management.graph import Graph
from fleet_management.agents import Agents
from fleet_management.task_management import TaskManagement
from fleet_management.task_assignment import TaskAssignment
from fleet_management.fleet_management import FleetManagement

def setup_logging(log_file_path: str) -> logging.Logger:
    """
    Configure the logging setup.

    :param log_file_path: The path to the logging file.
    :return: The logging object.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename=log_file_path,
        filemode='a'
    )
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logging.getLogger('').addHandler(console_handler)
    logging.getLogger('matplotlib').setLevel(logging.WARNING)
    return logging.getLogger(__name__)

class ConfigManager:
    """
    Class handles loading and managing configurations.
    """
    def __init__(self, config_paths: Dict[str, str]):
        self.config_data = self._load_json(config_paths['config'])
        self.lif_data = self._load_json(config_paths['lif'])
        self.agents_initialization_data = self._load_json(config_paths['agents_initialization'])
        self.transportation_tasks_data = self._load_json(config_paths['transportation_tasks'])

    @staticmethod
    def _load_json(path: str) -> dict:
        """
        Loads a JSON file from the given path.
        
        :param path: The path to the JSON file.
        :return: The JSON data.
        """
        try:
            with open(path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            logging.error(f"File not found: {path}")
            sys.exit(1)
        except json.JSONDecodeError:
            logging.error(f"Invalid JSON format in file: {path}")
            sys.exit(1)

def run_simulation(config_manager: ConfigManager, logging: logging.Logger):
    """
    Run the fleet management simulation.
    
    :param config_manager: The configuration manager object.
    :param logger: The logging object.
    """
    # Start the agent simulation.
    agent_simulation_path = "src/mobile_robot_simulation/dist/agent_simulation.exe"
    try:
        subprocess.Popen([agent_simulation_path])
        # Wait for the agent simulation to start.
        time.sleep(10)
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to execute {agent_simulation_path}: {e}")
        sys.exit(1)

    # Initialize the objects of the fleet manager.
    graph = Graph(lif_data=config_manager.lif_data)
    agents_object = Agents(config_data=config_manager.config_data, logging=logging) 
    task_management = TaskManagement()
    task_assignment = TaskAssignment()
    fleet_management = FleetManagement(agents_object=agents_object)

    # Run the simulation for the specified time.
    time.sleep(config_manager.config_data["simulation_run_time"])

def main():
    """
    Main function to set up and start the simulation.
    """
    # Logging setup.
    logging = setup_logging("data/output_files/logging_file.log")

    # Configuration paths.
    config_paths = {
        "config": "data/input_files/config_file.json",
        "lif": "data/input_files/LIF_Example.json",
        "agents_initialization": "data/input_files/AgentsInitialization_Example.json",
        "transportation_tasks": "data/input_files/TransportationTasks_Example.json",
    }

    # Load configurations.
    config_manager = ConfigManager(config_paths)

    # Run the simulation.
    run_simulation(config_manager, logging)

if __name__ == "__main__":
    main()
