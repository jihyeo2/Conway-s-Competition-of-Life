# Conway's Game of Competition | Project 2 for GT CS3300, Fall '23

## Install Guide

### Prerequisites

Hardware:
* Any Windows, MacOS, or Linux machine capable of installing python 3.11 and docker

Software:
* Python 3.11 (along with the accompanying install of pip)
* Docker
* git (optional)

### Necessary Libraries

Using a general package manager (such as apt-get or brew)

* xorg 21.1.9
* xinit 1.4.2

Using pip

* fastapi==0.104.1
* tzlocal==5.2
* uvicorn>=0.24.0
* pygame==2.5.2
* requests==2.31.0
* numpy==1.26.1

### Download Instructions

To play online:
* Visit the application hosted on Google Cloud Platform at the URL: TODO deploy onto GCP and put link here.

To play, test, or develop locally:
* By downloading from GitHub releases:
    * TODO make GitHub release and put instructions for downloading the release.
* By cloning from GitHub (requires git):
    * In a terminal, clone the GitHub repository.
        * `git clone https://github.com/jihyeo2/Conway-s-Competition-of-Life.git`

### Build and Installation Instructions

None!

### Run Instructions

To run ```backend```:

* Make sure python3.11 is installed
* `cd backend`
* `pip install -r requirements.txt`
* `uvicorn src.api.api:app --host 0.0.0.0 --port 3301`

To run ```frontend```:

* Make sure Python3.11 is installed
* Make sure Docker is installed and is up and running
* Make sure xorg and xinit are installed
    * If they are not, perform the following commands:
        * For Linux:

            ```
            sudo apt-get update
            sudo apt-get install xorg
            sudo apt-get install xinit
            ```

        * For Mac:
            ```
            brew update
            brew install xorg-server
            brew install xinit
            ```
* Navigate to the repository
    ```
    cd frontend
    pip install -r requirements.txt
    docker build -t ccol .
    docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --name ccol ccol
    ```
* In another terminal window, navigate to the repository
    * For Windows:
        ```
        cd frontend/src
        python main.py
        ```
    * For Mac/Linux:
        ```
        cd frontend/src
        python3 main.py
        ```

### Troubleshooting

* When running `python main.py`
    * `ModuleNotFoundError: No module named 'pygame'`
        * Caused by pygame not being installed. Ensure that `pip install -r requirements.txt` has been run in the `~/frontend` directory. If you are using a python virtual environment when installing these dependencies, ensure this virtual environment is active when running `main.py`.
    * `ConnectionRefusedError: [Errno 61] Connection refused`
        * Caused by the frontend being unable to query the backend. Ensure that the instructions to run the backend have been followed before attempting to run the frontend.
* When running `python3 api.py`
    * `ModuleNotFoundError: No module named 'src'`
        * Caused by attempting to run the backend using python3 instead of uvicorn. Ensure that the backend is run using the instruction `uvicorn src.api.api:app --host 0.0.0.0 --port 3301` from the `~/backend` directory.

### FAQ
* Why are xorg and xinit required?
    * They are required to install and run pygame, the frontend display client of the application.
* Should I download from GitHub releases or clone the repository?
    * Either is okay!
* Why are there no build or install steps?
    * As this is a python application dependent only on python libraries, once the code is on your computer and python installed, you need only run the backend then frontend and python will interpret and run the program.
* Why do I have to run two different `python` files?
    * One is to initialize the backend server which handles the multiplayer connections and tracking the state of the game, while the other is to initialize a frontend instance that a user can use to connect to the backend and play the game.
