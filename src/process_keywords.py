import gzip
from keybert import KeyBERT
from yake import KeywordExtractor
import re

import setup_dir

NWORDS=100
FMT="{}\t{}\t{}\t{}\t{}\n"
cleans={
"international\s+water\s+management\s+institute": "IWMI",
"sunil\s+mawatha": "",
"the\s+consultative\s+group\s+on\s+international\s+agricultural\s+research": "CGIAR",
"fulltext\s+keywords": "",
"keywords\s+keywords": "",
}

yake_kw_extractor = KeywordExtractor(lan="en", n=2, top=NWORDS)

kw_extractor = KeyBERT('distilbert-base-nli-mean-tokens')
with open(setup_dir.DIR_KW+"results.csv", "wt", encoding='utf-8') as kwf:
    
    kwf.write(FMT.format("YEAR", "METHOD", "RANK", "KEYWORD",  "METRIC"))
    for year in range(2002,2021+1):
        with gzip.open(setup_dir.DIR_PROC+"{}.gz".format(year), "rt", encoding='utf-8') as inf:
            txt=inf.read() 
            for item in cleans.items():
                txt=txt.replace(*item)
            txt=txt.lower()
            #txt="Research Reports Working Papers SWIM Papers Other Research Pubs. Newsletters Pb. Catalogue (pdf) Library Services Resource Pages Research Archive |Whats new ___________________| |Recent research ______________| SIMA Global Dialogue Comprehensive Assessment A basin persective on water savings How do we ensure enough water for the future? Many believe that the worlds increased water demands can be met by reducing the amount of water wasted in agriculture. But when looked at from a basin perspective,"
            keywords_yake = yake_kw_extractor.extract_keywords(text=txt)
            for ii,kw in enumerate(keywords_yake):
                kwf.write(FMT.format(year, "Yake", ii, *kw))
            print("Yake: Year {}: {}".format(year, keywords_yake))
            keywords_bert = kw_extractor.extract_keywords(txt,  stop_words='english', top_n=NWORDS)
            for ii,kw in enumerate(keywords_bert):
                kwf.write(FMT.format(year, "Bert", ii, *kw))            
            print("Bert: Year {}: {}".format(year, keywords_bert))

