<!--# xDD collaboration docker recipe
## Objective
Provide a base image and define a process for collaborators to use in building a Docker image to be deployed against subsets of the xDD corpus.

## Needs
- Application overview
- Input definition (what documents and product are expected?)
- Input expectations (e.g. read from /input?)
- Output definition (what does the app spit out?)
- Output expectations (e.g write to /output?)
- Permissions 
- Userid - test run
- Resource estimates?
- Terms of use document?



## Previous attempts
We tried to use a generic application template for similar purposes in the past:

https://github.com/UW-Deepdive-Infrastructure/app-template

A few people used it, but it didn't generate as many users as initially hoped. Additionally, for the few users who did use it, success often depended on my giving a lot of time and attention to help troubleshoot and debug things. Part of this is because I wanted to help and wanted to have people use xDD for science.

Flaws:
  - Too much complexity up-front. Needed to clone repo in git, potentially understand postgres, define thigs in config files, etc.
  - From Czaplewski: "i think it didn't work because the goal of it was so poorly defined. "run apps" and "use our infrastructure" are not actionable"-->




# Objective
This document describes a recipe to create a docker image, containing all required software, in order for a text-datamining application to be deployed against the xDD corpus.

# Background
xDD is among the largest collections of text-and-datamining-ready scientific literature in the world. Through unique partnerships with publishers and access to high-throughput computing resources, the system enables researchers to develop science-driven applications using any of a number of available data products, including:

- Stanford CoreNLP [todo link]
- ScienceParse [todo link]
- Extracted raw text [todo link]
- OCRed representations
- COSMOS-derived tables, figures, and captions

Users are empowered to utilize these products to mine and survey the literature, developing applications to extract entities, relationships, figures, tables, equations, models, trends, and predictions from relevant published works.

Due to contractual obligations, these applications may only be deployed across wide subsets of the corpus within UW-Madison resources. The portability of docker containers [todo link] make them an ideal candidate for this deployment model -- a docker container developed by a scientist locally on their machine will be easily deployable within the computing resources available to xDD in UW-Madison's Center for High Throughput Computing (CHTC). 

# Examples
These are examples of applications deployed against the xDD infrastructure. 

https://github.com/jonhusson/gdd_demo - Finds and extracts relationships between two sets of targets
https://github.com/mclapham/app-template - Mines the literature for ichnofossil occurences 
https://github.com/ItoErika/Reservoir_app - Extracts geologic units acting as aquifers
https://github.com/bserna-usgs/app-template - Recognizes sentences related to the impact of dam removal
https://github.com/aazaff/usgs_geochron - Mines for geochronology measurements
https://github.com/adamancer/speciminer - Finds occurrences of USNM speciments mentioned in the literature

# Communicating application behavior
The first step in the process is to communicate the application behavior to the xDD team.

- What does the application do?
- What data product(s) are needed for an input?
- How is the target corpus defined? (keyword, set of keywords, defined list of DOIs, specific journal, etc.)
- Is each document processed independently, or does the result depend on _all_ documents in a set?
- What software does the application use?
- What external dependencies, if any, exist (e.g. connection to an outside database)
- What are the approximate resources required for the application? 

[TODO: what is this communication channel? Email?]

## Defining an input 
In order to deploy an application against the xDD, the _type_ and _set definition_ of input data must be defined. Fundamental questions of each are:

- _Type_ : Which of the data products that xDD can provide does the application need?
- _Set definition_ : What documents need to be processed? 

Applications can utilize any or all of the above data products. For example, an application may utilize natural language output from Stanford's CoreNLP to extract entity relationships, then read data from COSMOS-derived tables mentioning those entities.

Because xDD's corpus is large and multi-disciplinary, it is often important to restrict the set of documents used as input. This can be accomplished in several ways:

1. Specifying a list of article DOIs.
2. Supplying a list of journals to target.
3. Filtering the corpus by keyword, phrases, publication date ranges, etc.

Filtering is done within the processing framework -- only a defined target is needed from the user.

## Defining an output
Output must be well-defined and discussed with the xDD team prior to application deployment. Contractual obligations may limit allowed returns (for example, returning image representations of full pages or large sections of text may not be allowed). Output should be _machine-readable_ instead of designed for human consumption.

# Creating an image
(link to dockerfile documentation)
http://chtc.cs.wisc.edu/docker-build.shtml

## xDD-specific requirements
- Input and output paths must be defineable when instantiating the script (or default to a `/input` and `/output`)
- Images should contain all necessary components, modules, and data. They should ideally be self-contained processing units, without requiring any additional downloads or module installations at runtime.
- Images will _not_ be run as root. For security reasons, images are run as unprivelged `nobody` user within the infrastructure. Be sure that the software in the container does not expect root-level priveleges (see "Testing the Image" below)

## Testing the image
See http://chtc.cs.wisc.edu/docker-test.shtml for information about testing the image locally. Especially important is:

- Running as a non-root user.
- Ensuring that no extra files are being downloaded or installed.
- Think about resource usage as your app is running -- how many CPUs is it using? Memory? Disk? These are important to know, even approximately, before deploying at scale within xDD

# xDD promises
- Data files will be prefixed with the documents' unique internal xDD id.
- CoreNLP will be provided as .tsv files (see the readme for more information), with a column structure of:
  -  docid (text) -- document's unique ID within our internal database
  -  sentid (integer) -- sentence's index within the document
  -  wordidx (integer[]) -- Word's index within the sentences
  -  word (text[]) -- Word
  -  poses (text[]) -- Parts of speech
  -  ners (text[]) -- Named entity recognizer
  -  lemmas (text[]) -- base or dictionary form of word
  -  dep_paths (text[]) -- Dependency type
  -  dep_parents (integer[]) -- Word index of the dependency parent

- Text contents will be provided in a .txt file.
- Scienceparse will be provided as a .json file.


# Example
A simple sample application is provided in `example` directory. It's a simple example: use [spaCy](https://spacy.io) to extract all known geopolitical entities (country, states, cites) from text. It uses as its input the text extracted from PDF documents.

  - The `Dockerfile` is the recipe for creating the docker image. It is commented to provide explanation and guidance as you build your own. 
  - The application logic itself is contained in `extract_gpe.py`. It reads from `/input` and writes to `/output` within the running container
  - requirements.txt defines the python modules to install
  - `input/` provides an example text input file.

To build and test the image, run:

```
docker build . -t my_first_xdd_app
docker run -it -u $(id -u) -v $(pwd)/input/:/input/ -v $(pwd)/output:/output/ my_first_xdd_app bash
```
The `-u` command specifies which user to be within the container -- in this case, it uses your current user id on the host machine within the container. Your user likely won't exist there, but that's ok, since that will be the same behavior as within xDD.

Then, within the container run:
```
python extract_gpe.py
```

If all goes well, the extracted geopolitical entities will be written to /output/, now visible outside of the container as well.

This application is almost ready for deployment within xDD -- you just need to upload the image to https://hub.docker.com or, if it can't be made publically available, supploy the xDD team with the source code and Dockerfile.


