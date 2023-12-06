# Hunter Bergstrom - Miniproject
## Installation
First, install the miniproject following:
- [NodeJS](https://nodejs.org/en/) (LTS recommended; go to 'Previous Releases' and install v18.19.0)
- [Docker](https://www.docker.com/)

Once you have installed these, run the command `npm i` to install the dependencies for the project. After that, open Docker. In the search bar on top, search for "mongo", pull the latest version, and then select "Run". Click on the optional settings and enter the container name as "minimongo". For host port, enter "27017". For host path, enter the path to this folder (the top-level miniproject folder), and for container path, enter "/data/db". After this, just run the container and the mongodb instance should be deployed. Finally, after all of this is set up, simply run the command `node app.js` to deploy this project, and navigate to `http://localhost:8888` in your browser to view it.

## Implementation
### Seed
This repository contains a seed file already called "seed.webgmex". By default, this seed will be available for the user to select when creating a new project in WebGME. However, if you would like to use your own seed, you can do so using the command `webgme new seed -f newSeed.webgmex newSeedName`.
### Visualizer
The visualizers folder has two parts: panels and widgets. The panels folder contains both the panel file (OthelloVizPanel) and the control file (OthelloVizControl). The panel file sets up the actual framework of the panel and its underlying functions. The control file is what actual controls the elements of the panel. It has the functions that will be called when updates are made to the board by interacting with it during the game. These are mainly handler functions that keep track of state and call the plugins included when they are needed. This also includes toolbar functions as well.
### Plugins
There are a few plugins that are used to update the state of the game as the user interacts with the board. They are as follows:
- BuildDescriptor: This plugin is written in python and creates a structured data structure in the form of a JSON object tht can be used to represent the model for visualization purposes.
- CreateGame: This plugin is written in python and simply creates a new game in the proper folder (/J) with the set start state.
- 

## Usage
After running this project and creating a new project in WebGME based on the supplied seed, an Othello game can be played. To do this, simply navigate to  