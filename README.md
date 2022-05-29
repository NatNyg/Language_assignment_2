# Language_assignment_2 - sentiment and NER

## This is the repository for assignment 2 in Language Analytics.

### Project Description
This project provides for a tool that can get every sentiment score in headlines in a dataset, find all geopolitical mentions in each headline and lastly find the 20 most common geopoliticial entities across each dataset. For this project I have used a "fake-or-real-news dataset". 


### Method
For this project I have used the small English spacy model as my nlp pipeline, which I define after importing the packages needed for the script. 
I have further used the SentimentAnalyzer from Vader and SpacyTextBlob. 
The script first loads the user-defined dataset as a pandas dataframe and adds a column containing the ID for each of the texts. I then split my dataset into two dataframes; one that contains the fake news and one that contains the real news. 
After this the script has a sentiment_analysis function that performs sentiment analysis on each headline in the dataframes, using the Vader SentimentAnalyzer and appends the calculated sentiments into a list for each category (fake and real news). 
My function geo_mentions then finds the geopolitical mentions across each of the dataframes, using again the nlp-pipeline and the tqdm that allows us to follow how far along we are in the process of looping through the headlines, finding all the geopolitical named entities and appending these entities into a list for each headline. This temporary list is lastly appended into another list that ends up containing geo entities for all of the headlines in each dataframe. 
My function save_results then saves the ID, sentiment and geopolitical enities for each headline in two new dataframes (one for fake and one for real news), both of which is lastly saved as .csv files to the "out" folder. 
Lastly my function common_geo loops over each of the dataframes, finds the geopolitical entities, creates a new dataframe consisting of only these entities, finding the top 20 entities and saves one barplot of the entities for each dataframe (one for fake and one for real news) to the "out" folder. 

### Repository Structure

The repository includes three folders:

    in: this folder should contain the data that the code is run on
    out: this folder will contain the results after the code has been run
    src: this folder contains the script of code that must be run to achieve the results

### Usage

In order to reproduce the results I have gotten (and which can be found in the "out" folder), a few steps has to be followed:

1) Install the relevant packages - relevant packages for both scripts can be found in the "requirements.txt" file.
2) Make sure to place the script in the "src" folder and the data in the "in" folder. Ross has the data used for this project.  
3) Run the script from the terminal and remember to pass the required argument (-ds (dataset)
-> Make sure to navigate to the main folder before executing the script - then you just have to type the following in the terminal: 
"python src/Sentiment_and_NER.py -ds {name of the desired dataset}"

This should give you the same results as I have gotten in the "out" folder.
 
### Results
The results are interesting to look at, as it gives us a quick and easy overview about what geopolitical entities is being spoken about in a text, and how the sentiment is about the content. It becomes even more interesting when comparing these informations across datasets, as we have done here. This could also be done across different news media to see if there is a difference in the way the sentiment is, compared to different named entities. The barplots provides a quick overview which is interesting to look at for potential further analysis. 
