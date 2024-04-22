**Cloning and Beyond: A Quantum Solution to Duplicate Code** 

Quantum computers are becoming a reality. They have the potential to accelerate many computationally complex processes, and also to find better results in 
complex solution landscapes. However, the kinds of problems which these computers are currently a good fit for, and the ways to express those problems, 
are substantially different from the kinds of problems and expressions used in classical computing. 

Quantum annealers, in particular, are an interesting kind of quantum computers to considering how they are promising in solving specific types of problems 
efficiently in the near term. However, they are also the most foreign compared to classical programs, as they require a different kind of computational thinking.

In my work, I have created a novel formulation of the well known software engineering problem of code clone detection by expressing it as an 
optimization problem in the framework of quantum annealing, a type of quantum computing. It also serves as an example of how software engineering problems 
can be formulated to be solved using quantum annealing. This work elaborates on how I rendered the code clone detection problem as a subgraph isomorphism 
problem and formulated it as a quadratic optimization. The formulation compares the Abstract Syntax Tree (AST) representations of two given code fragments and 
reports an energy value indicative of their similarity. It is then implemented on an actual quantum annealer (DWave Advantage System).

The motivation behind this research goes well beyond code duplicate detection: this novel approach to thinking about software engineering problems as optimization problems paves the way into expressing them as problems that an be solved using optimization architectures not only like quantum annealing, but also other classical devices such as Support Vector Machines, Digital Annealers (Fujitsu), and GPUs simulating quantum computers.

You can find the final programs used to generate the results in the paper in the folder 'Experiment Code'.
You will have to install the DWave Ocean SDK to be able to run these programs. It would be beneficial to do so in a virtual environment. 
See the 'instructions' file for more information on ow to run the programs in the 'Experiment Code' folder

**Link to Paper:** https://dl.acm.org/doi/10.1145/3622758.3622889
We are in the process of updating the structure of this repository to make it easier to navigate and access the programs. In the meantime, feel free to reach out to this email ID for any questions: samyaknj@uci.edu.

**Citation**

The programs in this repository have been developed as part of the following paper. We appreciate it if you would please cite the following paper if you found the repository useful for your work:

```
@inproceedings{jhaveri2023cloning,
  title={Cloning and Beyond: A Quantum Solution to Duplicate Code},
  author={Jhaveri, Samyak and Krone-Martins, Alberto and Lopes, Cristina V},
  booktitle={Proceedings of the 2023 ACM SIGPLAN International Symposium on New Ideas, New Paradigms, and Reflections on Programming and Software},
  pages={32--49},
  year={2023}
}
