

## About
This repo contains the unformatted tex document for the publication "Detection of Markers for Discrete Phenotypes".
The paper was published and is available at

 * https://dl.acm.org/doi/10.1145/3486713.3486729

A video of the presentation at CSBio21 is available here

 * https://www.youtube.com/watch?v=47JGU5p9m2c

If you have questions, want to discuss ideas or report errors and typos in the manuscript please open an [issue](http://github.com/hklarner/detection_of_markers_for_discrete_phenotypes/issues) or contact

 * hannes.klarner@fu-berlin.de (developer)
 * heike.siebert@fu-berlin.de

The repo also contains a Python CLI tool, called `biomarkers`, that can be used to compute the markers for a given Boolean network and phenotype components.


## Installation
To install the master branch use:

``` 
pip3 install pip --upgrade
pip3 install --force-reinstall git+https://github.com/hklarner/detection_of_markers_for_discrete_phenotypes
```

To install a tagged version use the `@`: 

``` 
pip3 install pip --upgrade
pip3 install git+https://github.com/hklarner/detection_of_markers_for_discrete_phenotypes@1.0.0
```


## The biomarkers tool
If the installation was successful you should be able to see the help menu for the biomarkers tool:
```
$ biomarkers -h
Usage: biomarkers [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

Options:
  -v, --version  Display version.
  -h, --help     Show this message and exit.

Commands:
  control-create             Create a control file.
  control-export             Export a control file.
  json-info                  Reads json file and prints summary.
  markers-export             Exports markers as CSV.
  markers-factorize          Factorizes a marker set.
  markers-graph              Creates a marker graph.
  markers-info               Prints info about a markers file.
  markers-validate           Validates a marker set.
  problem-create             Creates a marker detection problem.
  problem-info               Displays info about a problem file.
  problem-solve              Solves a marker detection problem.
  repo                       Access to the pyboolnet repository.
  steady-states-correlation  Creates the steady state correlation graph.
  steady-states-matrix       Prints the steady state matrix.
```
To see the help text and available options of a command call the command with the option `-h`.
E.g., to see the help text for the command `markers-create` call `biomarks markers-create -h`.


## Computation of markers
The computation of the markers is a two-step process.
First, define a problem file by specifying a Boolean network and the phenotype subspace using the command `problem-create`:.
```
biomarkers problem-create --problem emt_problem.json --bnet selvaggio_emt --phenotype AJ_b1=0,AJ_b2=0
```
Instead of specifying a phenotype subspace you may specify the phenotype components:
```
biomarkers problem-create --problem emt_problem.json --bnet selvaggio_emt --phenotype AJ_b1,AJ_b2
```
The command creates a problem file in `json` format.

To compute the markers for a problem file use the command `problem-solve`:
```
biomarkers problem-solve --problem emt_problem.json --forbidden AJ_b1,AJ_b2 --marker-size-max 5 --markers emt_markers.json
```
The command creates a markers file in `json` format.
To export a marker set in `csv` format use the command `biomarkers markers-export`:
```
biomarkers markers-export --markers emt_markers.json --csv emt_markers.csv
```

To factorize a marker set use the command `biomarkers markers-factorize` and specify the markers file:
```
biomarkers markers-factorize --markers emt_markers.json
```



## repo
biomarkers repo --list
## Developers
- [clingo documentation](https://potassco.org/clingo/python-api/5.4/)
- [clingo tutorial](https://potassco.org/clingo/python-api/current/clingo/)
