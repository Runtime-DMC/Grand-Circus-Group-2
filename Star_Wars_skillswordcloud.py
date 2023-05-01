# -*- coding: utf-8 -*-

# Python program to generate WordCloud
 
# importing all necessary modules
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import numpy as np
import math

# Reads 'sorted_skills' file
skills = pd.read_csv(r'/content/sorted_skills.csv')
comment_words = ''
stopwords = set(STOPWORDS)
 
# iterate through the csv file
for val in skills.skill:
    
    # typecaste each val to string
    val = str(val)
 
    # split the value
    tokens = val.split()
     
    # Converts each token into lowercase
    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower()

    comment_words += " ".join(tokens)+" "
 
mask = Image.open("spiky.png")
mask = mask.resize((800, 800), resample=Image.BILINEAR)
mask = np.array(mask)
wordcloud = WordCloud(width = 500, height = 500,
                background_color ='white',
                stopwords = stopwords,
                min_font_size = 15,
                mask = mask,
                contour_width=3,
                contour_color='#330066').generate(comment_words)
 
# plot the WordCloud image                      
plt.figure(figsize = (6, 6), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
 
plt.show()