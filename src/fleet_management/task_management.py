# Import required libraries and modules.

class TaskManagement:
    """
    Class for managing the tasks.
    """
    # TODO: Implement the task management algorithm.
    # Load JSON file
    # Organize tasks
    # Track status 

    def __init__(self) -> None:
        """
        Initialize the task management object.
        """
        ##Attributes and loading of file containing tasks
        #Store the tasks loaded from the file
        self.tasks = self.load_tasks("C:\Alex\Master\2024-5 WS\Industrial Mobile Robotics Lab\Practice\Fleet Management\fleet-management-simulation\data\input_files\TransportationTasks_Example.json")
        # Initialize the status of all tasks to "pending"
        self.task_status = {task["transportationTaskId"]: "pending" for task in self.tasks} 
    
    def load_tasks(self, task_file: str) -> list:
        # Load transportation tasks from a JSON file
        # Reads tasks from the file and handle error (file not found or invalid JSON).
        try:
            with open(task_file, 'r') as file: # Read mode
                data = json.load(file)
                return data["transportationTasks"] #return list of tasks
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(f"Error loading tasks: {e}")
            return [] 
            

    def get_next_task(self) -> dict:
        # Get the next available task for assignment
        # Return The next pending task or None if no tasks are available.

        for task_id, status in self.task_status.items():
            if status == "pending": # Iterate through task's status to find the first pending task.
                return next(task for task in self.tasks if task["transportationTaskId"] == task_id) 
                #Returns the corresponding task from self.tasks.
        return None 
    
    def update_task_status(self, task_id: str, status: str) -> None:
        # Update the status of a task.
        # task_id: The ID of the task to update.
        # status: The new status of the task.
        
        if task_id in self.task_status:
            self.task_status[task_id] = status

