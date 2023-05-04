# Python program to generate WordCloud
 
# importing all necessary modules
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import numpy as np

# Reads 'top_words' file
words = pd.read_csv(r"C:/Users/battl/Documents/Dash Final Project/Combined CSVs/top_words.csv")
comment_words = ''
stopwords = set(STOPWORDS)
 
# iterate through the csv file
for val in words.word:
     
    # typecaste each val to string
    val = str(val)
 
    # split the value
    tokens = val.split()
     
    # Converts each token into lowercase
    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower()
     
    comment_words += " ".join(tokens)+" "
 
mask = Image.open("C:/Users/battl/Documents/Dash Final Project/Combined CSVs/PythonSymbol.png")
mask = mask.resize((800, 800), resample=Image.BILINEAR)
mask = np.array(mask)
wordcloud = WordCloud(width=mask.shape[1], height=mask.shape[0],
                background_color ='white',
                stopwords = stopwords,
                min_font_size = 10,
                mask = mask,
                contour_width=3,
                contour_color='#000033').generate(comment_words)

# plot the WordCloud image                      
plt.figure(figsize = (4, 4), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
 
plt.show()