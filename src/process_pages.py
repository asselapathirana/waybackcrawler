import os
import re
import trafilatura

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

for date in ulist:
    print("DATE: {}".format(date))
    alltext=""
    pattern = re.compile("^{}[0-9]+.snapshot$".format(date))
    with open("../output/processed/{}.processed.txt".format(date),"w", errors="ignore") as outf:
        for root, dirs, files in os.walk("../output/pages"):
            for file in files:
                if pattern.search(file):
                    print("doing: {}".format(file))
                    with open(os.path.join(root, file),"r", errors="ignore") as inf:
                        html=inf.read()
                        text = trafilatura.extract(html)
                        if text:
                            text_clean = text.replace("\n", " ").replace("\'", "")                        
                            alltext+=" "+text_clean
            outf.write(alltext)
        
    
