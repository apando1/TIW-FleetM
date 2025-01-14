# Fleet Management Simulation

## Project Setup Guide


### Creating a Virtual Environment with `conda`

- Conda manages both Python and non-Python packages, such as libraries for R, C, or system-level dependencies. It's a package manager and environment manager.
- Conda creates isolated environments that include Python itself. Useful for maintaining multiple Python versions.
- Conda performs automatic dependency resolution.

####  Required Tools and Installation

1. **Anaconda or Miniconda**:

    - Download [Anaconda](https://www.anaconda.com/) (full distribution) or [Miniconda](https://docs.anaconda.com/miniconda/) (minimal version).
    - Install the software based on the instructions for your operating system.
    - Verify the installation in the Anaconda/Miniconda Prompt:

        ```
        conda --version
        ```

#### Steps to Create a Virtual Environment with `conda` without using an `environment.yml`

1. **Create a new environment**:
    ```
    conda create -n my_env_name python=3.x
    ```

    Replace `my_env_name` with the desired name of the new virtual environment.

    Replace `3.x` with the desired Python version (e.g., 3.12).

2. **Activate the environment**:
    ```
    conda activate my_env_name
    ```

3. **Install packages**: Inside the active environment, install Python or system-level packages:
    ```
    conda install package_name
    ```

    Alternatively, you can also use pip inside the environment:
    ```
    pip install package_name
    ```

5. **Deactivate the environment**:
    ```
    conda deactivate
    ```

6. **Delete the environment**:
    ```
    conda remove --name my_env_name --all
    ```

#### Steps to Create a Virtual Environment with `conda` using an `environment.yml`

- The `environment.yml` file is used to recreate or share a Conda environment, including both Python and system-level dependencies.

1. **Export a Conda environment**:
    ```
    conda env export > environment.yml
    ```

2. **Create an environment from an `environment.yml`**:
    ```
    conda env create -n my_env_name -f environment.yml
    ```

    Navigate to the location where the `environment.yml` file is located.

    Replace `my_env_name` with the desired name of the new virtual environment.

3. **Update an existing environment**:
    ```
    conda env update -f environment.yml
    ```

### Creating a Virtual Environment with `pip`

- Pip manages only Python packages from the Python Package Index (PyPI).
- Pip relies on venv or virtualenv for environment management, requiring separate tools to isolate Python versions.
- Pip resolves dependencies but may require manual intervention to fix conflicts.

#### Required Tools and Installation

1. **Python**:

    - `pip` comes bundled with Python. Make sure Python is installed:

        - **Windows**: Download Python from the [official website](https://www.python.org/downloads/) and install it. During installation, check the box for **"Add Python to PATH"**.
        - **Linux/Mac**: Verify if Python is installed:
            ```
            python3 --version
            ```

            If not, install it using:

            - **Linux**: `sudo apt install python3`
            - **macOS**: `brew install python3` (if Homebrew is installed).

2. **Virtual Environment Module**:

    - Python's `venv` module is included by default.


#### Steps to Create a Virtual Environment with `pip` without using a `requirements.txt`

1. **Create a new environment**:

    ```
    python -m venv my_env_name
    ```

    Replace `my_env_name` with the desired name of the new virtual environment.

2. **Activate the environment**:

    - **Windows**:
        ```
        my_env_name\Scripts\activate
        ```

    - **Linux/macOS**:
        ```
        source my_env_name/bin/activate
        ```

3. **Install packages**: Inside the active environment, install required packages:
    ```
    pip install package_name
    ```

4. **Deactivate the environment**:
    ```
    deactivate
    ```

5. **Delete the environment**: Simply delete the `my_env_name` folder.

#### Steps to Create a Virtual Environment with `pip` using a `requirements.txt`

- The `requirements.txt` file is used to list Python package dependencies for environments managed with `pip`.

1. **Export installed packages to `requirements.txt`**: Command can also be used in Conda environments:
    ```
    pip freeze > requirements.txt
    ```

2. **Create an environment using `requirements.txt`**:

    - First, create and activate a virtual environment as described above.
    - Then install the dependencies:

        ```
        pip install -r requirements.txt
        ```


### Setting up MQTT

#### MQTT (Message Queuing Telemetry Transport)

1. **Install an MQTT broker (e.g., `mosquitto`)**:

    - **Linux**:
        ```
        sudo apt update
        sudo apt install mosquitto mosquitto-clients
        ```

    - **macOS** (with Homebrew):
        ```
        brew install mosquitto
        ```

    - **Windows**: Download and install Mosquitto from [Eclipse Mosquitto](https://mosquitto.org/).

2. **Run the Mosquitto broker**: The Mosquitto folder (e.g.: `C:\Program Files\mosquitto`) may have to be added manually to the system PATH beforehand.
    ```
    mosquitto
    ```

3. **Verify MQTT setup**:

    - Subscribe to the topic:
        ```
        mosquitto_sub -h localhost -t test/topic
        ```

    - Publish a test message to the topic (in a second terminal):
        ```
        mosquitto_pub -h localhost -t test/topic -m "Hello MQTT"
        ```


### Setting up VS Code

1. **Install VS Code**:

    - **Windows**: 
    Download the installer from [Visual Studio Code](https://code.visualstudio.com/), run the installer and follow the steps (check options like "Add to PATH").

    - **Linux**:
        ```
        sudo apt update
        sudo apt install code
        ```

    - **macOS** (with Homebrew):
        ```
        brew install --cask visual-studio-code
        ```

2. **Install extensions**:

    - Open VS Code and click on the Extensions Icon (left sidebar).
    - Search for and install commonly used extensions, e.g. Python.


### Setting up Git

1. **Install Git**:

- **Windows**:
    - Download and install Git from the [official website](https://git-scm.com/).
    - During installation:
        - Choose a text editor (default is Vim; you can select VS Code or another editor).
        - Select default branch name (e.g., main).
        - Set other options as per your preference (e.g., Git Bash for command-line use).

- **Linux**:
    ```
    sudo apt update
    sudo apt install git
    ```

- **macOS** (with Homebrew):
    ```
    brew install git
    ```

2. **Configure Git**:

    After installation, configure your user identity and preferences in the Git Bash:

    - **Set user name and email**:
        ```
        git config --global user.name "Your Name"
        git config --global user.email "your.email@example.com"
        ```
        These will appear in your commits.

    - **View your configuration**:
        ```
        git config --list
        ```