# COMP0034 Coursework 1 - A Flask REST API

## Introduction

This document outlines the specifications for a Flask-based REST API designed to manage and disseminate data derived from the Metropolitan Police Freedom of Information (FOI) Requests. The system aims to provide a robust and scalable platform that allows users to interact with and extract insights from the data, enhancing transparency and accessibility.

### Background

Freedom of Information requests are a fundamental component of modern governance, providing the public with the right to access information held by public authorities. The Metropolitan Police receives a significant volume of these requests annually, encompassing a wide range of topics pertinent to their operations and public interactions.

### Project Objective

The primary objective of this project is to develop a Flask REST API that efficiently handles, stores, and retrieves data related to FOI requests made to the Metropolitan Police. This API will serve as a backbone for potential front-end applications that aim to visualize, analyze, and report on the data, thus facilitating better public understanding and research capabilities.

### Requirements

To run this project, you will need Python installed on your machine. Additionally, you will need to install the project dependencies which are listed in the `requirements.txt` file.

### Installation

Any of the commands used will have to be ran from the top-most directory in the project.

1. Clone the repository:

    git clone https://github.com/bianchibruno/comp0034-fyp/

2. Navigate to the project directory:

    cd comp0034-fyp

3. Create a virtual environment for the project (suggested):

    (venv)
    python -m venv comp0034cw1env
    source comp0034cw1env/bin/activate

    OR

    (conda)
    conda create -n comp0034cw1
    conda activate comp0034cw1

4. Install the required dependencies:

    pip install -r requirements.txt

5. Install the app code:

    pip install -e .

### Running and testing the app 

Any of the commands used will have to be ran from the top-most directory in the project.

1. Run the app:

    flask --app app run --debug 

    http://127.0.0.1:5000/requests should display a JSON view of the Request data.

2. Stop the app:

    Ctrl + C

3. To run tests:

    pytest



