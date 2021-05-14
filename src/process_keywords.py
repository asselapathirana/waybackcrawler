import gzip
from keybert import KeyBERT
from yake import KeywordExtractor
yake_kw_extractor = KeywordExtractor(lan="en", n=2, top=25)

kw_extractor = KeyBERT('distilbert-base-nli-mean-tokens')
for year in [2002, 2003, 2004]: #range(2002,2021+1):
    with gzip.open("../output/processed/{}.gz".format(year), "rt", encoding='utf-8') as inf:
        txt=inf.read() 
        #txt="Research Reports Working Papers SWIM Papers Other Research Pubs. Newsletters Pb. Catalogue (pdf) Library Services Resource Pages Research Archive |Whats new ___________________| |Recent research ______________| SIMA Global Dialogue Comprehensive Assessment A basin persective on water savings How do we ensure enough water for the future? Many believe that the worlds increased water demands can be met by reducing the amount of water wasted in agriculture. But when looked at from a basin perspective,"
        keywords = keywords = yake_kw_extractor.extract_keywords(text=txt)
        #kw_extractor.extract_keywords(txt,  stop_words='english', top_n=25)
        print("Year {}: {}".format(year, keywords))
