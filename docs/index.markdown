---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
---

# Introduction/Background

## Context and Significance

Conway’s Game of Life is an automated game played on a board of “cells,” or pixels. Before the game begins, the user is able to select any number of cells to be marked as “alive” with their uniquely assigned color. The user may then launch the game. The following rules will then apply across a series of rounds: any live cell with fewer than two live neighbors dies, any live cell with two or three live neighbors survives, any live cell with more than three live neighbors dies, and any dead cell with exactly three live neighbors becomes a live cell. Beautiful patterns are able to emerge as a result, with the live and dead cells shifting and changing either until all cells are dead, or some cells enter a repeated pattern of liveness.

Our product is a multiplayer variation of this game, one in which each player is able to select additional live cells in between rounds. The additional rules are as follows: each player is able to denote a set number of cells as live before the game begins; players each have their own set of live cells denoted by color; when a dead cell is to become alive, the player with two or more of the neighboring live cells gains that live cell as part of their set; if a dead cell is to become alive but its three neighboring live cells are all of different sets, then the cell remains dead; players with no live cells at the end of a round are “eliminated”; and each player yet to be eliminated is able to mark a new cell as live after each round.

There will also be the addition of the “food” mechanic: before the game begins, a set of predetermined cells will be marked as food, with collisions between live cells and food cells allowing the colliding player to denote additional cells as live after the round. Players are unable to denote cells adjacent to food as live, and instead must collide with food via propagation from selections from previous rounds. The player who has collected the most food by the end of the game will be declared winner. A statistics screen containing information such as: total food eaten, total cells collided with, maximum simultaneous live cells, etc… will be shown at the end of the game.

In terms of implementation, a pygame display client will be used for the user interface, and a FastAPI server will allow multiple players to make requests to the server to affect the grid.


## Project Scope

The scope of this project is limited only to a deployed backend server for unifying the display among each player and frontend display for allowing users to play the game. The rules were set in stone before development began, and no updates would be made without clear need. Moreover, our four Minimum Marketable Features were decided well in advance, and no additions would be made to these without the completion of the first four. This would ensure that our team would have bitesize quantities of work culminating in a complete Minimum Viable Product.

## Project Management

The project management structure for this project entailed assigning each member ownership over distinct portions of the project. This was chosen to ensure that there would always be one primary point of contact with complete knowledge over any given component of the project. The breakdown is shown below:

- Backend Lead: Pranav Devarinti
- Frontend Lead: Andrew Woo
- Testing Lead: Nishant Baglodi
- Frontend-Backend Connection Lead: Julie Oh
- Documentation and Deployment Lead: Kevin Mankowski
- Presentation Lead: Chris Reid

There was no single lead for the team as it was deemed that a more democratic approach would suit the smaller size of the team. Each lead was tasked with ensuring that their component was being completed and integrated in a timely manner.

# Literature Review

## Related Work

1. [MIT Lecture on Conway's Game of Life](https://web.mit.edu/sp.268/www/2010/lifeSlides.pdf)
2. [Implementation of Conway's Game of Life](https://playgameoflife.com/)
3. [Implementation of Patterns in Conway's Game of Life](https://conwaylife.com/)
4. [Multiplayer Implementation of Conway's Game of Life](http://lifecompetes.com/)
5. [2-Player Implementation of Conway's Game of Life](https://www.dcs.bbk.ac.uk/~gr/software/p2life/p2life-old.asp)

## Analysis

In reviewing the existing literature in determining the feasability of our idea, reference [1] was used in getting the team members up to speed on the rules and context of Conway's Game of Life. This resource goes over the rules of the game in detail, the history of Conway's Game of Life, and some of the many repeating patterns possible.

Then, reference [2] was found and used to help members of the team visually understand the rules of the game. From this, the team agreed that a multiplayer implementation with corresponding additions to the rules would be feasible as an idea. This application became our largest inspiration, and our goal would be to achieve the same look and feel but with these new additions. However, our team had to first verify that although Conway's Game of Life was first conceptualized in 1970, no modern functional multiplayer implementation was currently available.

References [3], [4], and [5] were found while verifying that no multiplayer implementations were currently usable. Reference [3] is very similar to reference [2], but adds preset iterations of the game highlighting some of the possible repeating patterns. Reference [4] is a modern multiplayer implementation of Conway's Game of Life, but is not currently functional. As such, it seemed that a current hole in the market existed due to the server behind this implementation not accepting requests. However, it's multiplayer rules were still visible, and appeared very similar to those of our team, so the decision was made to add the additional functionality of the food mechanic to our implementation. Reference [5] is a 2-player implementation of Conway's Game of Life. However, it is dated to the point that the only browsers successfuly able to use the application are Netscape and Firefox.

After this research, it was clear to our team that no modern multiplayer version of this game was available, and the decision was made to proceed with the idea.

# Software Technologies

## Python3.11

Used for the entirety of the source code of our project. It was chosen as all developers had prior experience with the language, it's extensive libraries would allow for a backend server and frontend display client written in one language, and it's popularity which would ensure adequate resources in development, testing, and deployment.

## FastAPI

Used for the backend server. It was chosen due to it simplicity in providing endpoints to the frontend server.

## PyGame

Used for the frontend display client. It was chosen due to being the most popular frontend game display library for the Python language.

## PyTest

Used for the entirety of the testing within our source code. It was chosen due to being one of the most prolific python testing libraries, meaning that many resources would be available in team members learning and using the library. Moreover, it could be used to achieve both white box and black box testing, as well as unit testing and integration testing. As these were key testing goals in our development process, PyTest was chosen.

## Postman

Used for the testing of backend endpoints. This was necessary for testing the FastAPI server during development, which was essential in ensuring that the multiplayer functionality was implemented correctly. It was chosen due to each team member having sufficient experience with the tool such that no learning would be required for its use.

## Google Cloud Platform

Used for the deployment of the backend FastAPI server. This was necessary to allow for players on different machines to play with one another, which was crucial in our goal of implementing a multiplayer spin on Conway's Game of Life. Google Cloud Platform was chosen due to each team member having prior experience in deployments via the platform.

## GitHub / Git

Used for version control during the development process. This was necessary to ensure that team members could work in a cohesive manner and on the same version of the application, with conflicts able to be handled seamlessly during merge conflicts. GitHub and Git were chosen due to each team member having ample prior experience in version control using the tools.

# Project Lifecycle

## Stages

### Topic

Multiplayer twist on Conway’s Game of Life (difference is player’s compete by having the most ‘food’ eaten)

### Minimum Marketable Feature 1: Conway’s Game of Life

The direct neighbors to a given pixel affect how it will evolve in the next time step; no neighbors could mean death by solitude, too many neighbors could mean death by overpopulation, enough neighbors could spawn a new pixel.

### Minimum Marketable Feature 2: Multiplayer

- Multiplayer functionality with different players having different colors
- A game lobby waits until enough players join, then the game starts
- Players who come into close contact with each other could have pixels die off

### Minimum Marketable Feature 3: Additional Mechanics
- Added food system
- Food has a random chance of spawning
- Players are able to gather it by collision over the course of rounds
- Board wraps around

### Minimum Marketable Feature 4: Statistics
- Backend server tracks statistics of the players throughout a game
- At the end of the game, the frontend will query a backend endpoint for the statistics


## Progress Report

Report included an introduction/background of Conway’s Game of Life, software technologies we used, our software output/purpose and the conclusion of our game which aligns with our project purpose and goals.

## Code

Clearly written out Release notes for:
1. Detailing all new software features, enhancements, and improvements made
2. Clear documentation of all bug fixes and isues addressed since the last release, with descriptions and resolutions. Identification of all known bug fixes, defects, and missing functionalities in this release, along with planned future improvements
3. Comprehensive documentation of the required software and hardware configurations that the customer must have before installation
4. Clear documentation of all third-party software or libraries that must be installed for the software to function correctly
5. Clear and detailed instructions on how the customers can access and download the project or software, including any steps required for building from source code
6. Comprehensive steps and directories required for the installation process, including configuration and setup, as well as clear instructions on how to run the software
7. A comprehensive section addressing common errors during installation and usage, providing corrective actions with clear troubleshooting steps. FAQs included


## Presentation and Demo

Were able to deliver a working twist on Conway’s Game of Life with frontend and background from technologies used and implemented correctly. Given this was our key milestone being able to present our background and tools used, then followed by a wonderful demo from our team.

## Peer Evaluation

All team members have submitted peer evaluations discussing everyone's roll in the project and opinions on how the project came to completion.


# Requirements

## Minimum Marketable Features

### Multiplayer

We add multiplayer functionality to Conway’s game of life. Users should be able to play with their friends!

### Modified Rules and Objective

In order to make this game competitive, we modify the rules to include a food mechanic. The objective is to collect as much food as possible by the end of the game.

### Statistics Board

Players should be able to see some stats about their gameplay at the end of the game.

## Functional Requirements

From these MMFs, we were able to generate a list of functional requirements and nonfunctional requirements that together allow us to create a good user experience.

### Lobby Joining

Players must be able to join a lobby before the game starts.

### Display

The game (when loaded into) must display a grid and run at 30fps (minimum on a GTX 1070 / i5-8700 setup running Ubuntu 20.04 LTS).

### Selection

The user must be able to select various regions on the grid to add / remove cells. He must also have some way to send changes or have them automatically be sent to the server.

### Multiplayer

Changes that a single player makes should propagate to all players.

### Rules

At a specified server-side tick, the game should update. When this update occurs, player cells and empty space should evolve according to the rules of Conway's game of life. Food cells should behave as empty space, but be added to the player's stats the first time a player occupies a space with them.

The game should end after a specified period of time and player statistics should be displayed.

### Stats

At the end of a game, a player’s statistics should be displayed. These stats must include total food eaten and all stats shown must be accurate.

## Non Functional Requirements

### Speed

The game must be able to operate in a playable condition. We define this in two different ways. Locally, it should be able to run without server side lag > 200ms. Since the cloud introduces additional problems out of our control, this is instead raised to a server-side response time >2 seconds.

### Proactive Error Avoidance

Measures need to be taken to prevent server side internal errors. For example two users attempting to join with the same username, or change the same squares must be anticipated in order to prevent unexpected server behavior and possible bugs.

## Prioritization

Our team decided to prioritize these requirements first by dependency. Items like the user stats are dependent on the game first functioning. From there, we prioritized items by figuring out what could be developed in parallel and then attempting to make those portions in parallel. The lists above are displayed in the rough order that we attempted to make the game in (some items were worked on in parallel by different sub-teams).


# Design

## System Architecture: Monolithic Client-Server

Our game is built on a monolithic client-server architecture, adopting a 2-tier design where a single server entity handles all server-side functionalities. This organization consists of a server which provides a set of services upon API calls to specific endpoints and clients.

![Component Diagram](./fig1.png)
Figure 1. Component Diagram

## Design Decisions & Reflection

### Game Logic

#### Centralized game instance

To maintain control over the game shared by multiple clients, we followed the Singleton Design pattern, allowing only one game instance. For better coherence, we further separated internal and external methods for classes. External methods, such as ‘update_board()’ and ‘spawn_food()’, are reserved for client interactions, while internal methods, such as ‘_get_cell_neighbors()’ and ‘_contesting_players()’ are called when internally handling requests received from client interactions.

#### Abstract Classes

Leveraging the Decorator Design pattern, we employed python’s abstract classes, methods, and properties to define game objects with their attributes and behaviors. Specific implementations were then dynamically added to classes through wrapping. This approach enhanced the scalability of our game logic, laying a foundation that allows the seamless incorporation of future features without encountering conflicts.

![Design Class Diagram](./fig2.png)
Figure 2. Design Class Diagram

#### Shared Classes

While designing the game logic, we prioritized the creation of shared objects to ensure coherent integration of frontend and backend. This decision not only enhanced the extensibility of our game but effectively minimized potential conflicts or discrepancies from both ends.

#### Independent Cell Evolution Behaviors

In implementing automated cell evolution upon user inputs, we utilized the Strategy Design Pattern and defined concrete strategies for cell behaviors. Concrete strategies include random spawn, birth, death, and food consumption. This modular approach enables the game to dynamically decide evolutionary cell behaviors, facilitating extensibility of our game.

### Implementation
Game States & Components
Following the initial implementation, we conducted a comprehensive code refactoring to enable the generation of appropriate display contents corresponding to different game states. Additionally, we meticulously defined separate GUI components within our game, ensuring their easy reusability. This strategic compartmentalization not only elevated the overall user experience but also established a groundwork that facilitates future development.

### Integration

#### Communication Protocol

We decided to use HTTP instead of web sockets for networking due to its inherent advantages in simplicity and compatibility. HTTP, being a stateless protocol, eliminates the need for persistent connections between the game server and client instances. Therefore, connections are rather made upon requests, ensuring better response time and more stable connection between entities.

#### Synchronization

A notable challenge emerged when we tried to synchronize the clocks between the server and client. To address this, we added thread locks with a controlled update period respectively for the server and client. This approach enabled the game to provide uniform updates to all players.

# Testing

## Test Strategy

Our testing strategy started with reviewing our functional and non-functional requirements to highlight what features the existing code was supposed to provide and formulate possible edge cases that could test the boundaries of the code. Both white box and black box testing were implemented to provide cases that depended on the inner workings of the code as well as cases that formulated as broader functionality concepts.

### White box

To cover white box testing, we looked at the structure of how a game started. This process involved creating settings for the game that described the board size, creating a lobby using those settings, creating players with name and color attributes, adding them to the lobby, and then starting the game. We’d then make sure that the game’s board and players showed accurate information. Afterwards, we tested that players’ pixel placements accurately updated the game’s backing board. White box testing mainly covered the start_game() and update_board() functions.

### Black box

For black box testing to cover general game functionality, we thought of general mechanics that we’d expect to see the game properly execute. For example, there were several cases of pixel evolution that we thought of; after placing these pixels and executing a time step, we expected to see a certain pixel configuration depending on the initial configuration. Other examples of game mechanics/functionality included food generation and player statistics. Black box testing involved the previously mentioned start_game() and update_board() functions for basic game initialization and progress, but also tested functions involving game mechanics such as step(), spawn_food(), and get_statistics().

## Tools Used

### pytest

pytest was used as an easy way to run all our tests using Python. The simplicity of following a naming convention for test functions and then running the pytest command within the appropriate directory automatically ran all tests and showed which ones failed. In addition, flags such as -v (verbose, used to show more details about the tests) and -s (disables output capturing, allows for passed tests to still show output if print is used) were helpful.

## Test Cases

### Initialization

The initialization tests covered the board setup, creating multiple instances of lobbies with different settings (ex. board sizes and player count) and ensuring that after a game was started from that lobby, all game configurations were as expected. One important case we made sure to test was trying to add a player with the same name/color as an existing player, as we needed to make sure that all players were unique. As the structure of our program changed (lobby was implemented later), the tests also updated to ensure that the new structure was still functional.

### Board Update

Board update tests initialized a game and then attempted to place pixels to see if they properly updated the internal game board. In addition, players placing pixels on the same coordinate was tested to ensure that the game logic would recognize this was an illegal move and prevent the second player from overriding the first player’s pixel.

### Food Generation

Food generation tests initialized a game, placed player pixels, then generated food with varying spawn rates. Afterwards, the board was checked to ensure that food was generated properly (spawn rate of 100% required all non-player pixels be food, 50% spawn rate required at least 1 food be generated) and that food generation didn’t override player pixels.

### Time Steps

Time step tests initialized a game, placed player pixels in a certain configuration, then executed a time step to ensure pixel evolution was behaving as expected. Configurations tested included a single lone pixel, 2 pixels next to each other, 3 pixels connected in L-shape, and 2 different players placing multiple pixels close to each other (this specific test had 2 timesteps; one for verifying evolution behavior when multiple players contest the same area, and another for ensuring further evolution occurred as expected).

### Player Stats

Player stats tests initialized a game, placed player pixels, spawned food, underwent time steps, and then checked player statistics to make sure cells created, food captured, and contested areas were all accurate. Different tests changed food spawning, player pixel placement with respect to food, and player pixel placement with respect to other players.

## Impact on Development:

Testing was very important in the development process to ensure that new game logic design worked as intended and that the game structure wasn’t too complex to follow. One fault in the code that was found through testing was pixel evolution for 2 pixels directly next to each other. The expected behavior for this was for the pixels to disappear after a timestep occurred; however, the program incorrectly kept both pixels alive. Another example of a fault was within the player statistics system; the food that a player evolved to capture was not being shown within the player’s statistics, revealing a condition in the game logic where food was searched for in an array that was defined as only including player pixels, not food pixels. Extensive testing of edge cases provided the final product to avoid obvious bugs with the game’s backing logic.
