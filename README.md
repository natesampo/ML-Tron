# PercepTRON
We hate losing at Tron. To remedy this, we  developed an evolutionary machine learning algorithm to lose Tron for us. 

## What a NEAT algorithm

NeuroEvolution of Augmenting Topologies (NEAT) is an algorithm for evolving sparse neural nets. NEAT evolves neural networks by randomly adding nodes, adding edges, and perturbing edge weights. More fit networks will replicate while less fit networks will drop out of the population.

NEAT encourages diverse networks and thorough exploration of the solution space by a method known as speciation. A genetic distance metric is defined, and sufficiently similar networks are designated to be part of the same species. Through a type of explicit fitness sharing, species are penalized for having large populations. This stops a single species from subsuming the entire population, and forces the algorithm to explore a wider solution space. This aids in avoiding local minima.

## Learning how to not die

As inputs, our network used the presence or absence of dangerous tiles in the entire playing grid. As outputs, the network could move the character in any of the four cardinal directions, with the restriction that a player cannot turn 180 degrees in a single move.

Additionally, we started the network with full connections between the outputs and the four cells immediately adjacent to the player, such that it could learn early on to avoid moves that lead to immediate death. Models were also given access to the relative X and Y position of the opposing player, so aggressive or cowardly tactics could emerge. The remainder of the network was initialized empty for the NEAT algorithm to populate with edges, intermediary nodes, and some semblance of self-preservation.

Each generation, individual models are assigned fitness based on matches with four other models. This fitness value is awarded based on the number of squares the model successfully fills with its color, rewarding strategies that can effectively avoid obstacles for long periods of time and punishing strategies that immediately race toward the nearest hazard and die.

## Results

Results were mixed.

A. For a single-player game and a set spawning location, our model could find an optimal strategy. In this situation, it learns to fill all available tiles on the board.

B. For a competitive game with random spawning location, agents would often learn probabilistic or cooperative strategies, such as proceeding in one direction while filling as many squares as possible. This indicates that there wasn’t sufficient reward for winning the game, so agents just learned to get a high number of squares filled on average, but the strategies perform poorly against humans.

C. We modified the simulation to incentivize killing the other player by giving the victor a percentage  of the remaining empty tiles. After a bit of training, the bot seemed to develop  higher-level strategies, like attempting to enclose the opponent and avoiding certain “greedy” survival routes.

## Bibliography

NEAT algorithm: Stanley et al, “Evolving Neural Networks through Augmenting Topologies”

