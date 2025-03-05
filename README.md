# Shared Micromobility Demand and Recharging Simulation

This repository contains a multi-agent system (MAS) simulation project designed to model a shared micromobility fleet operating within a grid-based city. The simulation focuses on vehicle battery management, user demand, and recharging operations, offering insight into the dynamics of micromobility systems. The project is implemented using the Mesa Python framework and includes real-time visualization of key metrics.


## Overview

The goal of this project is to simulate the behavior of a shared micromobility fleet within an urban environment. Vehicles operate across a grid where they serve user requests, manage battery levels, and visit charging stations when necessary. The simulation includes two types of demand scenarios:
- **Random Demand:** Users appear randomly on the grid.
- **High-Demand Zones:** Users are generated with higher probability in specific areas.

This model helps analyze vehicle availability, user wait times, and overall system utilization, providing valuable insights into managing real-world micromobility services.

## Features

- **Multi-Agent Simulation:** Models vehicles, users, and charging stations as independent agents.
- **Dynamic User Demand:** Simulates both random user distribution and peak demand zones.
- **Battery Management:** Vehicles transition between states (Available, In Use, Needs Recharging, Recharging) based on battery levels.
- **Real-Time Visualization:** Uses CanvasGrid and ChartModules to monitor simulation metrics such as vehicle availability and wait times.
- **Flexible Configuration:** Key simulation parameters (grid size, battery depletion/recharge rates, user demand probability, etc.) are adjustable to test various scenarios.
