# Psychomotor Vigilance Test - Brief (PVT-B) Statistics
## About
Calculates descriptive statistics for PVT-B data. PVT-B is ran via PsyToolkit[^1,2].

The range of a valid RT is 100 <= x >= 500.

The PVT-B script has been modified to count RTs < 100ms as commissions.

## Input
The program takes a command line argument: the path to a directory. The directory should contain .txt files that have the data for each trial of a given condition.

The program assumes data files have the following columns: Trial, Error, RT, Average RT, Commissions, and Lapses. The program assumes data files use whitespace as a delimiter.

## Credits
[1] G. Stoet, “PsyToolkit: A Novel Web-Based Method for Running Online Questionnaires and Reaction-Time Experiments,” Teaching of Psychology, vol. 44, no. 1, pp. 24–31, Jan. 2017, doi: 10.1177/0098628316677643.
[2] G. Stoet, “PsyToolkit: A software package for programming psychological experiments using Linux,” Behavior Research Methods, vol. 42, no. 4, pp. 1096–1104, Nov. 2010, doi: 10.3758/BRM.42.4.1096.
