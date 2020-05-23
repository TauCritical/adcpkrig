# adcpkrig

This repository contains a python package adcpkrig and associated helper scripts/functions/environments to analyze a sample dataset with multiple hyperparameters.

The package 'adcpkrig' is meant to be reproducible code that can be applied to a variety of datasets. The code requires input csv files created by another codebase (USGS geomorph toolbox, currently unpublished), with examples shown as 'bin_sample.csv' and 'vpts_sample.csv'.

Files in this upper level directory are part of a semester project for Georgia Tech's ISYE 6748, in which I conducted a variety of analyses using adcpkrig for the sample dataset provided. For the final report on this project, please see 'GT_ISYE_final_report.pdf'. Files containing the name 'prototype' or 'sample' contain code specific to this analysis and may be used as templates for reproducing this work or applying adcpkrig to other datasets. Currently, the analysis workflow is as follows:

## Build and run docker image
docker build -t <containername> .
docker run -P -d -v /home/ec2-user/adcpkrig:/app <containername>

Replace /home/ec2-user/adcpkrig with wherever the github repository has been cloned.

The docker image as currently written uses a reproducible Python environment specified in 'requirements.txt' and calls the script 'batch_sample_train.sh'. All analyses specified in the shell script will then be run in the background.

In turn, the called shell script calls the Python code 'sample_train.py'. This code takes as command line input chunk dimensionality and vector component to interpolate to allow for batch testing of different chunk shapes for the same dataset.

In sample_train.py, various adcpkrig functions are called to read in the data, partition an interpolation grid into appropriate chunks, and calculate interpolated velocities within the grid, lastly saving the interpolated data as .pickle files.

Of note, the code to merge individual chunks into a final grid is currently housed in 'prototype_utils.py' and should be moved to the adcpkrig package.

## Transfer .pickle files

Outputs from the sample_train.py interpolation process are saved as .pickle objects. If running analysis on a VM (e.g. EC2 instance) they should be transferred to the same directory as 'Prototype.ipynb'.

## View output

Once .pickle files have been generated for a given interpolation, outputs can be viewed without rerunning the interpolation. For samples, see 'Prototype.ipynb'. This notebook relies on numerous helper objects/functions contained in 'prototype_utils.py'.

# Files
Individual files in this repository are listed and explained below.

## adcpkrig

Directory containing python package adcpkrig. Contains functions for creating and interpolating grids.

## .dockerignore

Docker ignore file.

## .gitignore

Untracked files in git repository.

## Dockerfile

Docker file to reproduce analysis.

## Prototype.ipynb

Notebook file containing figures used to make final report and some other sample analyses presented to project supervisor. Useful for looking at examples of how to implement code.

## README.md

This file

## batch_sample_train.sh

Bash shell script to run multiple versions of sample_train.py

## batch_sample_transfer.sh

Bash shell script to transfer files from ec2 to s3

## bin_sample.csv

Bin csv file output from geomorph tools

## krig3d.yml

Conda yml file containing specifications for local environment to run prototype notebook

## prototype_utils.py

Python module containing helper functions to analyze data for notebook

## requirements.txt

PIP requirements file to install python modules in docker container

## sample_train.py

Python code to interpolate a grid based on sample csv files provided in this repository

## setup.py

Python package setup file (currently empty)

## vpts_sample.csv

Vpts csv file output from geomorph tools


