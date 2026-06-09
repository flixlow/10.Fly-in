*This project has been created as part of the 42 curriculum by flauweri.*

# Fly-in

## Description
Fly-in is a small simulator that plans and visualizes drone routes on a network of hubs and connections. The tool parses plain-text map descriptions, constructs a time-expanded network to model drone movement and hub/link capacities, computes feasible routes using a max-flow approach built on DFS-based path finding, and visualizes drone movements using Pygame. The goal is to demonstrate constrained routing, capacity management, and an interactive visual representation of the resulting schedules.

## Instructions
This project provides a Makefile with convenient targets to prepare and run the application.

Common targets:
- make map
  - Extract example maps from data/maps.tar.gz into the maps/ directory.
- make install
  - Ensures maps are installed and synchronizes the virtual environment / dependencies (project-specific sync command).
- make run
  - Builds prerequisites and runs the app: equivalent to "python3 -B -m src". You can pass an optional ARG to change runtime behavior: `make run ARG="--input maps/example_map.txt"`.
- make debug
  - Run the application under pdb: `make debug`
- make clean
  - Remove caches, virtualenv, and maps folder.
- make lint
  - Run linters and mypy checks.
- make lint-strict
  - Run stricter linting.

Examples:
- Prepare maps and run: make install && make run
- Run with a specific map: make run ARG="--input maps/example_map.txt"

## Resources
References and helpful links:
- Regex testing: https://regex101.com/
- Time-expanded networks & max flow: standard algorithm texts (e.g., CLRS)
- Pygame docs: https://www.pygame.org/docs/
- Pydantic docs: https://pydantic-docs.helpmanual.io/

AI usage
- AI-assisted for README, docstring

## Algorithm choices and implementation strategy
Overview:
- Time-expanded network: each hub is represented as a node per time step; two types of edges model waiting (stay in same hub) and movement (follow a connection) between consecutive time layers.
- Capacities:
  - Hub capacity: each hub has a max_drones value limiting how many drones can occupy it at a given time.
  - Link capacity: each connection has max_link_capacity to limit concurrent traversals.
- Node types:
  - Regular Node: represents hub at a time step.
  - ConnectionNode: used for special handling when a restricted zone requires using previous connection to move forward.
- Path finding & flow:
  - DFS-based augmenting path search finds one feasible path from start to end in the time-expanded graph while respecting capacities and zone rules.
  - For each found path, a blocking flow (the minimum residual capacity along the path) is applied to update edge and node passages.
  - The algorithm repeats until no more augmenting paths are available or the required number of drones is scheduled.
- Zones handling:
  - NORMAL, BLOCKED, RESTRICTED, PRIORITY are supported.
  - BLOCKED hubs are pruned from exploration.
  - RESTRICTED hubs are treated to ensure drones enter and exit respecting special connection constraints.
  - PRIORITY edges/hubs are considered first when sorting exploration edges.

Design rationale:
- Time expansion simplifies capacity and concurrency constraints by turning scheduling into a pure flow problem.
- DFS-based path search is simple and effective for the small to medium maps targeted by the project.
- The code is modular: parser, network builder, flow algorithm, and visualizer are separated to ease testing and extension.

## Visual representation features
- Based on Pygame, the visualizer:
  - Draws hubs and connections with scalable coordinates and padding to fit the window.
  - Uses themes (background, line, and text colors) loaded from assets/themes.json; press Space to cycle themes.
  - Shows drone icons moving along paths; time steps advance with arrow keys to inspect schedules.
  - Distinguishes restricted movement events (special coloring in console output).
- UX benefits:
  - Immediate visual feedback of schedule conflicts and capacity constraints.
  - Theme switching aids readability on different display environments.
  - Manual time control helps debugging and demonstration.

## Usage examples
- Prepare a map file in the maps directory (see example format in maps/).
- Start the app via Makefile: make install && make run
- Select a map, let the algorithm compute routes, then inspect movement in the visualizer.

## Project structure (high level)
- src/
  - parser.py : map parsing and validation
  - network.py : time-expanded network model
  - algo.py : DFS-based flow finder and path management
  - display.py : Pygame visualizer
  - output.py : textual step output
  - utils.py : data models (Hub, Connection, Map, etc.)

## Contributing
Report bugs or suggest improvements by opening issues or pull requests. Keep map format and semantics compatible with parser expectations.

---

If you need a sample README variation or an example map file to include in the repository, request it and it will be provided.

