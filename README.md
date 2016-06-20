Tutorial on modeling and performance analysis of Slotted ALOHA protocol. 
The source code contains numerical calculation for different models.
- SlottedAlohaTutorial.pdf - tutorial slides
- basic.py 
	Basic model: no retransmission, poisson arrival rate. Plots throughput, collisions and idle slots
- mchain.py
	Markov chain model, with retransmission probability as a parameter.
- stability.py
	Additions for markov chain model, plots backlog and throughput and illustrates stability concerns

Models and notations according to the only reference:
Bertsekas, Dimitri, and Robert Gallager. "Data networks", 1987
