# AAWZ Technical Challenge

This guide describes the steps necessary to install and run the Flask application from the [desafio-tecnico-aawz](https://github.com/BrunaRochaL/desafio-tecnico-aawz) repository on your local machine.

# Documentation
The documentation of the requests can be found in: https://documenter.getpostman.com/view/30268092/2sA3e1A9t2

# Extra
- sellers.csv - CSV to load sellers
- sale_sellers.csv - CSV to load sales from sellers
- sellers.db - SQLite that contains seller and sales information (can be deleted)

## Prerequisites

- A Linux-based system (can be adapted for other OSes).
- Git installed on your system.
- Python 3 installed on your system.

## Setup Steps

### 1. Install Python

1. Update system packages: sudo apt update

2. Install Python 3 and the python3-venv package: sudo apt install python3 python3-venv python3-pip

### 2. Clone the Repository

1. Clone the repository:

   git clone https://github.com/BrunaRochaL/desafio-tecnico-aawz
   cd desafio-tecnico-aawz

### 3. Set Up the Virtual Environment

1. Create and activate the virtual environment:

   python3 -m venv venv
   source venv/bin/activate

2. Install the Python dependencies:
   pip install -r requirements.txt

### 4. Run the Flask Application

1. Initialize the database and run the application:
   python3 app.py

### 5. Run Tests with Pytest

1. Make sure the virtual environment is activated:
   source venv/bin/activate

2. Run the tests using pytest:
   pytest
