# Krig3dADCP

This repository contains a python package adcpkrig and associated helper scripts/functions/environments to analyze a sample dataset with multiple hyperparameters.

# Files

## adcpkrig

Directory containing python module adcpkrig. Contains functions for creating and interpolating grids.

## .dockerignore

Docker ignore file.

## .gitignore

Untracked files in git repository.

## Dockerfile

Docker file to reproduce analysis.

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


