[![Paper](https://img.shields.io/badge/paper-arXiv%3A1912.12002-B31B1B.svg)](https://arxiv.org/abs/2306.17122)

# Partial Syndrome Measurement for Hypergraph Product Codes

[Noah F. Berthusen](https://noahberthusen.github.io), Daniel Gottesman

### Abstract
Hypergraph product codes are a promising avenue to achieving fault-tolerant quantum computation with constant overhead. When embedding these and other constant-rate qLDPC codes into 2D, a significant number of nonlocal connections are required, posing difficulties for some quantum computing architectures. In this work, we introduce a fault-tolerance scheme that aims to alleviate the effects of implementing this nonlocality by measuring generators acting on spatially distant qubits less frequently than those which do not. We investigate the performance of a simplified version of this scheme, where the measured generators are randomly selected. When applied to hypergraph product codes and a modified small-set-flip decoding algorithm, we prove that for a sufficiently high percentage of generators being measured, a threshold still exists. We also find numerical evidence that the logical error rate is exponentially suppressed even when a large constant fraction of generators are not measured.

### Description
This repository includes information, code, and data to generate the figures in the paper. Most of the code was sourced from Antoine Grospellier and Anirudh Krishna and their paper [Numerical study of hypergraph product codes](https://arxiv.org/abs/1810.03681) and then edited for the purposes of this work.

### Figures
All the codes used to create the figures in the paper are found in the **figure_scripts** folder. They are all written in Python, and use the matplotlib library.

### Data Generation
The main files to perform simulations as described in the paper are described below. Both Python and C++ code is available.
* ```src/src_cpp/decoder.cpp``` Implementation of the SSF decoder which has been edited to allow for incomplete syndromes.
* ```src/src_cpp/read_result.cpp``` Specification of the simulation results.
* ```src/src_cpp/main.cpp``` Main file to run to execute simulations of a multi-round decoding protocol.