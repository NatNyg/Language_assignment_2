"""
First I'll import the libraries I will be using for the script - make sure that the packages in the requirements.txt has been installed first. 
"""
import argparse

import os
import spacy
from tqdm import tqdm

#creating a nlp pipeline 
nlp = spacy.load("en_core_web_sm")

import pandas as pd

# sentiment analysis VADER
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
# sentiment with spacyTextBlob
from spacytextblob.spacytextblob import SpacyTextBlob
nlp.add_pipe('spacytextblob')

def load_data(data_set):
    """
This function reads the user-defined dataset as a pandas dataframe and deletes unwanted columns, and adds a column containing an ID for each text. It then splits the data into two new dataframes; one for the fake and one for the real news. For this project I'm using the fake_or_real_news.csv dataset - if this is changed, be aware that the output file-names might not make syntactic sense. 
    """
    
    filepath = os.path.join("in",data_set)
    data = pd.read_csv(filepath) 
    del data["Unnamed: 0"]
    data["Text_ID"] = data.index+1
    
    fake_news_df = data[data["label"]=="FAKE"]
    
    real_news_df = data[data["label"]=="REAL"]
    return fake_news_df, real_news_df 
    
def sentiment_analysis(real_news_df,fake_news_df):
    """
This function performs sentiment analysis on the two new dataframes, creating lists for the sentiment of respectively the fake and real news headlines. I then loop over the headlines using the Vader analyzer to get the polarity scores of each headline in the dataframes and appends the sentiment to the lists. 
    """
    rn_sentiment = []
    fn_sentiment = []
    
    for headline in real_news_df["title"]:
        rn_sentiment.append(analyzer.polarity_scores(headline))
        
    for headline in fake_news_df["title"]:
        fn_sentiment.append(analyzer.polarity_scores(headline))
    return rn_sentiment, fn_sentiment

def geo_mentions(real_news_df, fake_news_df):
    """
This function finds geopolitical entities (if any) for each headline and saves them in a list (one for the fake news data and one for the real news). 
I first find the batchsize for the dataframes so I can use a nlp pipe when running over the dataframes and look for entities with the label "GPE" (geopolitical entities) and append these entities, first to a temporary list and then to the predefined list - this way I get a list that contains a list of GPE's for each headline. 
The tqdm is used for tracking the process, as for the user to keep track on how far along in the process the function is when looping over the headlines. 
    """
    rn_batch = real_news_df["label"].value_counts()
    rn_batch_size = int(rn_batch[0])
    rn_gpe_ents = [] 

    for headline in tqdm(nlp.pipe(real_news_df["title"], batch_size=rn_batch_size)):
        temp_list = []
        for entity in headline.ents:
            if entity.label_ == "GPE":
                temp_list.append(entity.text)
            else:
                pass
        rn_gpe_ents.append(temp_list)
        
    fn_batch = fake_news_df["label"].value_counts()
    fn_batch_size = int(fn_batch[0])
    fn_gpe_ents = [] 
    
    for headline in tqdm(nlp.pipe(fake_news_df["title"], batch_size=fn_batch_size)):
        temp_list = []
        for entity in headline.ents:
            if entity.label_ == "GPE":
                temp_list.append(entity.text)
            else:
                pass
        fn_gpe_ents.append(temp_list)
    return fn_gpe_ents, rn_gpe_ents, rn_batch_size, fn_batch_size

def save_results(fn_sentiment,fn_gpe_ents, rn_sentiment, rn_gpe_ents, fake_news_df, real_news_df):
    """
This function saves the results I have achieved so far - that is for each datasets (fake and real news): the ID for each headline, the sentiment analysis of the headlines and the gpe's identified in each headlines. This is all saved to two seperate pandas dataframes (one for fake, and one for real news) with the appropriate columnnames and then saved as .csv files for the "out" folder. 
    """
    fake_news_ID = fake_news_df.iloc[:,3]
    real_news_ID = real_news_df.iloc[:,3]
   
    fn_list_content = list(zip(fake_news_ID, fn_sentiment, fn_gpe_ents))

    fn_df = pd.DataFrame(fn_list_content,columns=['Text_ID','Headlines_Sentiment','GPE_entities'])
    
    path = "out"
    collocate_file = "fn.csv"
    fn_df.to_csv(os.path.join(path, collocate_file),index=False)
    
    rn_list_content = list(zip(real_news_ID, rn_sentiment, rn_gpe_ents))
    
    rn_df = pd.DataFrame(rn_list_content,columns=['Text_ID','Headlines_Sentiment','GPE_entities'])
    path = "out"
    collocate_file = "rn.csv"
    rn_df.to_csv(os.path.join(path, collocate_file),index=False)
    return fn_df, rn_df
    
    
def common_geo(fake_news_df, real_news_df, rn_batch_size, fn_batch_size):
    """
This function finds the top 20 most common geopoliticial entities in each of the datasets (fake and real news)
I do this by once again looping over the headlines in each dataframe using the nlp pipeline, but instead of appending to a temporary list in order to get the entities for each individual headline, I append the GPE's onto a final list straight away - in this way I get all of the GPE's for each dataset in one list for each dataset. 
The tqdm is used for tracking the process, as for the user to keep track on how far along in the process the function is when looping over the headlines. 
I then use the value counts and nlargest functions to find the 20 most used GPE's, create a dataframe for each dataset containing these and finally creating a barplot for each dataset, visualizing the top 20 enitities. The figures are then saved as images to the "out" folder. 
    """
    rn_only_ents=[]
    fn_only_ents =[]
    for headline in tqdm(nlp.pipe(real_news_df["title"], batch_size=rn_batch_size)):
        for entity in headline.ents:
            if entity.label_ == "GPE":
                rn_only_ents.append(entity.text)
                
    for headline in tqdm(nlp.pipe(fake_news_df["title"], batch_size=fn_batch_size)):
        for entity in headline.ents:
            if entity.label_ == "GPE":
                fn_only_ents.append(entity.text)
    
    fn_only_ents_df = pd.DataFrame(fn_only_ents, columns = ["GPE"])


    rn_only_ents_df = pd.DataFrame(rn_only_ents, columns = ["GPE"])
    
    top20_fn = fn_only_ents_df["GPE"].value_counts().nlargest(20)
    top20_rn=rn_only_ents_df["GPE"].value_counts().nlargest(20)
    
    
    fig_f = (top20_fn.plot.bar(x=None, y=None).set_title("20 most common geopolitical entities in fake news")).get_figure()
    fig_f.tight_layout()
    fig_f.savefig(os.path.join("out","fn_top_20_gpe.png"))
    
    
    fig_r = (top20_rn.plot.bar(x=None, y=None).set_title("20 most common geopolitical entities in real news")).get_figure()
    fig_r.tight_layout()
    fig_r.savefig(os.path.join("out","rn_top_20_gpe.png"))
    return top20_fn
                        
                                                                                                               
    
def parse_args():
    """
This function initialises the argument parser and defines the command line parameters 
    """
    ap = argparse.ArgumentParser()
    ap.add_argument("-ds","--data_set",required=True, help = "The dataset for sentiment analysis and geopolitical entity search")
    args = vars(ap.parse_args())
    return args 
    
def main():
    """
This function defines the functions to be executed when the script is run from the terminal, and which arguments that has to be passed from the user, using the args. 
    """
    args = parse_args()
    fake_news_df, real_news_df = load_data(args["data_set"])
    rn_sentiment, fn_sentiment = sentiment_analysis(real_news_df,fake_news_df)
    fn_gpe_ents, rn_gpe_ents, rn_batch_size, fn_batch_size = geo_mentions(real_news_df, fake_news_df)
    fn_df, rn_df = save_results(fn_sentiment,fn_gpe_ents, rn_sentiment, rn_gpe_ents, fake_news_df, real_news_df)
    top20_fn = common_geo(fake_news_df, real_news_df, rn_batch_size, fn_batch_size)
    
    
if __name__== "__main__":
    main()

    
   

