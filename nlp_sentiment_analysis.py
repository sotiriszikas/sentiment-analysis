####################################################################################################################################################

import requests
from bs4 import BeautifulSoup
import nltk
import re
import unicodedata
from nltk.corpus import stopwords

nltk.download('stopwords')

# Defining Greek stopwords
greek_stopwords = set(stopwords.words('greek'))

# Defining positive and negative word lists in Greek (the lists are a work in process)
positive_words = ["καλος", "ευτυχια", "αγαπη", "θετικος", "επιτυχια", "θαυμασιος","υπεροχος"]
negative_words = ["κακος", "θλιψη", "μισος", "αρνητικος", "αποτυχια", "κραζω", "οχι", "βιαστης", "λουκετο", "αναποφευκτη", "προβλημα"]

# Removing and normalize text
def remove_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text)
                   if unicodedata.category(c) != 'Mn')

# Tokenization function for Greek text using regex
def custom_tokenize(text):
    return re.findall(r'\b\w+\b', text)

# Preprocessing Greek text
def preprocess_text(text):
    
    # Step 1: Removing special characters and numbers
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    
    # Step 2: Converting to lowercase
    text = text.lower()
    
    # Step 3: Removing accents
    text = remove_accents(text)
    
    # Step 4: Tokenization 
    tokens = custom_tokenize(text)
    
    # Step 5: Removing stopwords
    processed_tokens = [token for token in tokens if token not in greek_stopwords]
    
    return processed_tokens

# Determining sentiment based on word counts and display relevant words
def classify_sentiment(tokens):
    
    # Finding positive and negative words in the text
    positive_matches = [token for token in tokens if token in positive_words]
    negative_matches = [token for token in tokens if token in negative_words]
    
    # Counting the positive and negative words
    positive_count = len(positive_matches)
    negative_count = len(negative_matches)
    
    # Displaying the counts and matched words
    print(f"Positive words count: {positive_count} | Words: {', '.join(positive_matches)}")
    print(f"Negative words count: {negative_count} | Words: {', '.join(negative_matches)}")
    
    # Classifying sentiment and provide an explanation
    if positive_count > negative_count:
        print("Final Sentiment: POSITIVE")
        print("Explanation: The text contains more positive words than negative ones.")
    elif negative_count > positive_count:
        print("Final Sentiment: NEGATIVE")
        print("Explanation: The text contains more negative words than positive ones.")
    else:
        print("Final Sentiment: NEUTRAL")
        print("Explanation: The number of positive and negative words is equal, or no significant sentiment words were found.")

# Fetching and extracing the text from an online article
def fetch_article_text(url):
    try:
        
        # Custom headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Sending a request to the article URL with custom headers
        response = requests.get(url, headers=headers)
        
        # Checking if the request was successful
        if response.status_code == 200:
            
            # Parsing the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extracting the main content of the article (e.g., within <p> tags)
            paragraphs = soup.find_all('p')
            
            # Combining all paragraphs into a single string
            article_text = " ".join([p.get_text() for p in paragraphs])
            
            return article_text
        else:
            print(f"Failed to fetch the article. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

url = input("Article URL: ")

# Fetching the article text
article_text = fetch_article_text(url)

if article_text:
    
    # Preprocessing the fetched article text
    processed_tokens = preprocess_text(article_text)
    
    # Printing the processed text (tokens joined back into a string)
    processed_text = " ".join(processed_tokens)
    print("Processed Text:", processed_text)
    
    # Classifying the sentiment based on the processed tokens and provide explanation
    classify_sentiment(processed_tokens)

####################################################################################################################################################
