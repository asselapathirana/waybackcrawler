import os
import re
import trafilatura
import gzip
import charset_normalizer as chardet

print ("ha")
print(os.getcwd())
ulist=set()
for root, dirs, files in os.walk("../output/pages"):
    for file in files:
        if file.endswith(".snapshot"):
            #print(os.path.join(root, file))
            ulist.add(file[:4])
# 
ulist=list(ulist)
ulist.sort()
print(ulist)
print(len(ulist))


LIMIT=9999999999999999999999 
# change for debug and change back.
ulist=ulist #[2020] # ulist=ulist
# LIMIT=25
# ^^^^^ 
ct=0
for date in ulist:
    print("DATE: {}".format(date))
    with gzip.open("../output/processed/{}.gz".format(date),"wt", encoding='utf-8') as outf:
        alltext=""
        pattern = re.compile("^{}[0-9]+.snapshot$".format(date))        
        for root, dirs, files in os.walk("../output/pages"):
            for file in files:
                if pattern.search(file):
                    if ct > LIMIT:
                         break
                    ct += 1
                    file_=os.path.join(root, file)
                    rawdata = open(file_, 'rb').read()
                    result = chardet.detect(rawdata)
                    charenc = result['encoding']                    
                    print("doing: {} with codec {}".format(file, charenc))
                    with open(file_,"rt", encoding=charenc, errors = 'ignore') as inf:
                        html=inf.read()
                        text = trafilatura.extract(html)
                        if text:
                            text_clean = text.replace("\n", " ").replace("\'", "").replace("_", " ")                      
                            alltext+=" "+text_clean
        outf.write(" " + alltext + " ")
        
    
