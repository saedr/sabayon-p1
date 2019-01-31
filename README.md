# sabayon-p1

## Table of contents

1. [Purpose](#purpose)
2. [Requirements](#requirements)
3. [Dataset](#dataset)
4. [Usage](#usage)
5. [License](#license)
6. [Contact info](#contact-info)

## Purpose

sabayon-p1 creates a classifier to classfiy malware for project 1, course CSCI8360 of UGA. 

The project addresses the malware detection problem in the context of text classification.

## Requiremnets

This project requires Python 3.x with `pyspark` library installed.

## Dataset

The dataset consists of a set of documents belong to 9 different malware families. The content of the documents is in hexadecimal.

Since the size of the dataset is large, the data is not included in the repository, however a script to download a sample of the data is provided in the repository. To download the data navigate to `scripts/` directory and run on of the follwoings in command line (note that [`google-cloud-sdk`](https://cloud.google.com/sdk/) is required for the script): 

`$./get_files.sh`

`$python3 get_files.py`

## Usage

TBA

## License
The code in this repository is free software: you can redistribute it and/or modify it under the terms of the MIT lisense. 

## Contact info

For questions please email one of the authors: 

**saedr@uga.edu**

**marcdh@uga.edu**

**Jayant.Parashar@uga.edu**
