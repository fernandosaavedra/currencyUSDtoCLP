# USD to CLP Calculator in Django + DRF

## Introduction

This REST service shows the value of the dollar (USD) in Chilean Pesos (CLP) at a given historical date.

The service must extract the historical information of the value of the Dollar to pesos from the SII website (sii.cl) and store it in your own database.

Then the service must respond to the consultation of the value in pesos of a dollar amount for a certain date, and vice versa.

## Code Samples

To display the value in pesos [clp] of the amount in dollars [usd], on the date [date], we will execute the following request.

`[ GET: /clp?usd=XXXX&date=yyyymmdd ] `

** If date field is empty, it takes the last record saved in database.*
To display the value in USD of an amount of CLP on a certain date, we must execute the following request.

`[ GET: /usd?clp=XXXX&date=yyyymmdd ] `

** If date field is empty, it takes the last record saved in database.*

__*To use this application, we reccomend download some tool for REST API testing like Postman<br/>__

## Installation

For install this application, follow the next steps that are detailed below:

#### 1. Creating the Virtual Environment

It is suggested to create the virtual environment with Anaconda3. We must write the following commands:

~~~
# Create empty Conda Environment using Python 3.6
conda create -n <venv-name> python=3.6

# Activate Virtual Environment
activate <venv-name>
~~~
#### 2. Clonning the Repo
~~~
# Clone the Repository
git clone https://github.com/fernandosaavedra/gitfernando.git

# Enter to Folder
cd valorDolar
~~~
#### 3. Installing the Dependencies
~~~
# Install Django, DRF and the other libraries
pip install -r requirements.txt
~~~
#### 4. Enjoy it!
Your app is ready to use!
