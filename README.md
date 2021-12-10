
## About
This repo contains the unformatted tex document for the publication "Detection of Markers for Discrete Phenotypes".
The paper was published and is available at

 * https://dl.acm.org/doi/10.1145/3486713.3486729

A video of the presentation at CSBio21 is available here

 * https://www.youtube.com/watch?v=47JGU5p9m2c

If you have questions, want to discuss ideas or report errors and typos in the manuscript please open an [issue](http://github.com/hklarner/detection_of_markers_for_discrete_phenotypes/issues) or contact

 * hannes.klarner@fu-berlin.de (developer)
 * heike.siebert@fu-berlin.de


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

## Command line interface
For help on the available commands call `biomarkers -h`.

### problem-create
To create a marker detection problem use the command `problem-create`:
```
biomarkers problem-create --forbidden AJ_b1,AJ_b2,FA_b1,FA_b2,FA_b3 --bnet selvaggio_emt --phenotype AJ_b1=0,AJ_b2=0,FA_b1=1,FA_b2=0,FA_b3=0 marker-size-max 3
```

### problem-solve
To compute the markers for a problem file use the command `problem-solve`:
```
biomarkers problem-solve
```


## repo
biomarkers repo --list
## Developers
- [clingo documentation](https://potassco.org/clingo/python-api/5.4/)
- [clingo tutorial](https://potassco.org/clingo/python-api/current/clingo/)
