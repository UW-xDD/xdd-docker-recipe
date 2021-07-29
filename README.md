# Objective
This document outlines the steps necessary to constract a machine-learning application for bulk data-analysis of scientific texts located within the [xDD corpus](https://xdd.wisc.edu).

## Table of Contents
1. [Prepatory Steps](#prepatory-steps)
    1. [Determining if xDD is right for your project](#determining-if-xdd-is-right-for-your-project)
    2. [Finding relevant data within the xDD corpus](#finding-relevant-data-within-the-xdd-corpus)
2. [Building your application](#building-your-application)
    1. [Obtaining Sample Data for development purposes](#obtaining-sample-data-for-development-purposes)
    2. [Defining inputs and outputs within your application](#defining-inputs-and-outputs-within-your-application)
    3. [Creating and testing your docker image](#creating-a-docker-image)
    4. [Examples](#examples)
3. [Running your application](#running-your-application)
    1. [Requesting application review by xDD team](#requesting-application-review-by-xDD-team)
    2. [Application Run Request and Obtaining Results](#application-run-request-and-obtaining-results)

# Prepatory Steps
## Determining if xDD is right for your project
xDD is among the largest collections of text-and-datamining-ready scientific literature in the world. Users can construct applications to extract entities, relationships, figures, tables, equations, models, trends, and predictions from relevant published works.

Due to contractual obligations with the various publishing entities that make up the xDD library, applications may only be deployed within UW-Madison computing resources. The portability of [docker](https://www.docker.com/) containers make them an ideal candidate for this deployment model -- a docker container developed by a scientist locally on their machine will be easily deployable within xDD [high-throughput computing framework](https://chtc.cs.wisc.edu/). 

More details about these contractual obligations and other considerations when using the xDD system can be found in the [Terms of Service](https://github.com/ngds/ADEPT_frontend/blob/main/TOS.md#terms-of-service). Two good rules of thumb for determining if your application is permissable under xDD terms are: 1) output is *machine-readable* and not designed for human consumption and 2) output cannot be used to reconstruct large-sections of indivdual articles. We strongly encourage users with any doubts about the vaiability of a potential project to reach out directly to the xDD team (contact@geodeepdive.org) for consultation. 

## Finding relevant data within the xDD corpus
The first step in the process of building an xDD application is to identify which (if any) documents within the xDD corpus are of interest to your project. There are two principal mechanisms available to find data-mining targets in xDD available, though users should not hesitate to reach out directly to xDD staff if these methods are insufficient to see if other possibilities are available.

1. **TEXT BASED SEARCHES** The xDD development team has created the **A**utomated **D**ata **E**xtraction **P**la**T**form ([ADEPT](https://xdd.wisc.edu/adept)) to facilitate this process. The ADEPT front-end allows users to browse available documents in the xDD library using full-text search terms (powered by [ElasticSearch](elastic.co)) and other common serach parameters (e.g., publication date, journal name). Alternativey, users may intract with the xDD API (https://xdd.wisc.edu/api/v1) directly to search for relevant texts.

2. **IMAGE BASED SEARCHES** Users can also search for the presence of specific types of *tables*, *figures*, *equations*, and *captions* within xDD articles using the [COSMOS system](https://github.com/UW-COSMOS/cosmos). It is also possible to combine text-based and image-based search methods when defining a target data set.

# Building your application

## Obtaining Sample Data for development purposes
Once a user has identified a set of target publications for potential analysis, using either the [ADEPT browser](https://xdd.wisc.edu/adept#loginPanel), [xDD REST API](https://xdd.wisc.edu/api/v1), the [COSMOS system](https://github.com/UW-COSMOS/cosmos), or some combination thereof, users can request a subset of these publications for local development purposes. 

Requests for development datasets can be made through the [ADEPT browser](https://xdd.wisc.edu/adept) or by contacting the xDD administrative team directly by email (https://contact@geodeepdive.org). Users will then be provided a project and user-specific URL to 200 documents randomly sampled from the identified pool of documents. This link will be provided either by email or through the ADEPT browser depending on how the sample data was requested.

## Defining inputs and outputs within your application
An xDD application should have a defined `/input/` and `/output/` directory. The application should be designed such that the expected format of the `/input/` folder is identical to the [sample data](#obtaining-sample-data-for-development-purposes) provided at the beginning of the development process. 

Output must be well-defined and meet [Terms of Service](#determining-if-xdd-is-right-for-your-project). We strongly recommend that users with any doubts about the permissability of output format reach out to the xDD team directly (contact@geodeepdive.org). *Only* items found within the `/output/` directory upon application completion will be returned to users.

## Creating and testing your docker image
UW-Madison's Center for High Throughput Compouting provides a guide for creating a docker image [here](http://chtc.cs.wisc.edu/docker-build.shtml). Full documentation for the Dockerfile specification can be found [here](https://docs.docker.com/engine/reference/builder/). CHTC also provides a guide for testing a docker image locally [here](http://chtc.cs.wisc.edu/docker-test.shtml). 

#### Important tips and considerations:
- Make sure the application is running as a non-root user.
- Ensure that no extra files are being downloaded or installed at runtime.
- Think about resource usage as your app is running -- how many CPUs is it using? Memory? Disk? These are important to know, even approximately, before deploying at scale within xDD
- Input and output paths must be defineable when instantiating the script (or default to a `/input` and `/output`)
- Images should contain all necessary components, modules, and data. They should ideally be self-contained processing units, without requiring any additional downloads or module installations at runtime.
- Images will _not_ be run as root. For security reasons, images are run as unprivelged `nobody` user within the infrastructure. Be sure that the software in the container does not expect root-level priveleges (see "Testing the Image" below)

## Examples
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

If all goes well, the extracted geopolitical entities will be written to /output/, now visible outside of the container as well. A more comprehensive example application from one of our flagship partners can also be viewed [here](https://github.com/throughput-ec/UnacquiredSites/tree/master).

# Running your application

## Requesting application review by xDD team
xDD administrators need to monitor whether a submitted application is 1) respectful of the [Terms of Service](#determining-if-xdd-is-right-for-your-project) and will work properly on the [high-throughput computing infrastructure](https://chtc.cs.wisc.edu/). Users can use the [ADEPT platform](https://xdd.wisc.edu/adept) to request that an xDD administrator review and approve an application by 1) logging in to https://xdd.wisc.edu/adept, 2) going to the `My Data` pane, 3) navigating to the `Applications` tab, and 4) then clicking on the `New` button and filling out the application submission form. Users can expect approval or rejection of their submission within 7 business days and can check on the status of the approval request from the applications tab.

If users do not wish to use the ADEPT platform they can reach out to xDD staff by email (contact@geodeepdive.org). This method is most suitable when users do not wish to publish their application on DockerHub, as is encouraged by the ADEPT platform. If reaching out by email, users should ensure that the following information is included.

1. What does the application do?
2. What data product(s) are needed for an input?
3. How is the target corpus defined? (keyword, set of keywords, defined list of DOIs, specific journal, etc.)
4. What are the approximate resources required for the application?
5. Does the application require access to all desired data at once, or can it be split into smaller datasets?

## Application Run Request and Obtaining Results
Once an application has been approved by xDD administrators, a user can request that it be deployed at scale on the actual xDD corpus by going through the ADEPT platform and clicking on the *application name* in the Applications tab and filling out the generated form. Results will be returned to users in the form of a unique project and user-specific URL to a zipfile of the `/output/` folder contents by email.
