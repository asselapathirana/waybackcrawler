import multidict as multidict

import numpy as np

import os
import re
from PIL import Image
from os import path
from wordcloud import WordCloud
import matplotlib.pyplot as plt



import pandas as pd
import setup_dir

TOPN=100

removes=[
"^keywords\s+keywords",
"^fulltext\s+keywords"]

def clean(series):
    for regex in removes:
        idx=[itm[0] for itm in series.index.str.findall(regex) if len(itm)>0]
        series=series.drop(index=idx)
    return series

def makeImage(text_, filename):
    mask = np.array(Image.open(setup_dir.MASKFILE))
    text=clean(text_)
    wc = WordCloud(background_color="white", max_words=1000, mask=mask, width=100, height=200)
    # generate word cloud
    wc.generate_from_frequencies(text)

    # show
    plt.figure(figsize=(5,8))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.text(.5, .05, filename, fontsize=24)
    plt.savefig(setup_dir.DIR_GR+filename+".png", format='png', dpi=200 )

if __name__=='__main__':

    df = pd.read_csv("../output/keywords/results.csv", sep='\t')
    df.loc[ (df['METHOD'] == "Yake"), 'WEIGHT']=1/df['METRIC']
    df.loc[ (df['METHOD'] == "Bert"), 'WEIGHT']=df['METRIC']
    print (df)
    dfs={}
    freqs={}
    for item in ["Yake", "Bert"]:
        #dfs[item]=df[df.METHOD==item]
        dfs[item]=df[(df.METHOD==item) & (df.RANK<TOPN)]
        freqs[item]=dfs[item].groupby('KEYWORD')['WEIGHT'].sum().sort_values(ascending=False).apply(np.log10)
        print(freqs[item])
    print("ha")    
    makeImage(freqs['Yake'], "2002-2021")    
    print("all.png done")
    for year in range(2002,2021+1):
        dfs["Yake"]=df[(df.METHOD=="Yake") & (df.RANK<TOPN) & (df.YEAR==year)]
        freqs["Yake"]=dfs["Yake"].groupby('KEYWORD')['WEIGHT'].sum().sort_values(ascending=False).apply(np.log10)
        makeImage(freqs['Yake'], "{}".format(year))