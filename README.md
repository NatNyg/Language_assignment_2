# Language_assignment_2 - sentiment and NER

## This is the repository for assignment 2 in Language Analytics.

### Project Description
This projects provides for a tool that can get every sentiment score in headlines in a dataset, find all geopolitical mentions in each headline and lastly find the 20 most common geopoliticial mentioned across each dataset. For this project I have used a "fake-or-real-news dataset". 


### Method

### Repository Structure

The repository includes three folders:

    in: this folder should contain the data that the code is run on
    out: this folder will contain the results after the code has been run
    src: this folder contains the script of code that has to be run to achieve the results

### Usage

In order to reproduce the results I have gotten (and which can be found in the "out" folder), a few steps has to be followed:

1) Install the relevant packages - relevant packages for both scripts can be found in the "requirements.txt" file.
2) Make sure to place the script in the "src" folder and the data in the "in" folder. The data used for this project can is placed in the in folder.
3) Run the script from the terminal and remember to pass the required argument (-fn (filename)
-> Make sure to navigate to the main folder before executing the script - then you just have to type the following in the terminal: 
"python src/Sentiment_and_NER.py -fn {name of the desired filename}"

This should give you the same results as I have gotten in the "out" folder.
 
### Results
