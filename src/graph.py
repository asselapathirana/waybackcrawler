import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import setup_dir

MAXY=14
YCUTOFF=250

def set_labels(cols, ax, locdict):
    """loclist is a list of lists like
    [
    """
    # Add the text--for each line, find the end, annotate it with a label, and
    # adjust the chart axes so that everything fits on.
    for line, name in zip(ax.lines, cols):
        try:
            idx=locdict[name]
            if len(idx)==1:
                y = line.get_ydata()[idx[0]]
                x = line.get_xdata()[idx[0]] 
            else:
                x=idx[0]
                y=idx[1]
        except:      
            idx=-1
            y = line.get_ydata()[idx]
            x = line.get_xdata()[idx]            
        print('name:{}, idx:{}, x:{:.1f} y:{:.1f}'.format(name, idx, x, y))
        if not np.isfinite(y):
            y=next(reversed(line.get_ydata()[~line.get_ydata().mask]),float("nan"))
        if not np.isfinite(y) or not np.isfinite(x):
            continue     
        text = ax.annotate(name,
                            xy=(x, y),
                           xytext=(0, 0),
                           color=line.get_color(),
                           xycoords=(ax.get_xaxis_transform(),
                                     ax.get_yaxis_transform()),
                           textcoords="offset points")
        #text_width = (text.get_window_extent(
                #fig.canvas.get_renderer()).transformed(ax.transData.inverted()).width)
        #print ("text width", text_width)
        #if np.isfinite(text_width):
            #ax.set_xlim(ax.get_xlim()[0], text.xy[0] + text_width * 1.05)

if __name__=='__main__':
    
    df_ = pd.read_csv(setup_dir.DIR_KW+"results.csv", sep='\t')
    df_.loc[ (df_['METHOD'] == "Yake"), 'WEIGHT']=1/df_['METRIC']
    df_.loc[ (df_['METHOD'] == "Bert"), 'WEIGHT']=df_['METRIC']
    
    df = df_[df_['METHOD']== "Yake"]
    kw_=list(set(df[df['RANK']<5]['KEYWORD']))
    year=list(set(df['YEAR']))
    kw_.sort()
    year.sort()
    remove=['keywords keywords']
    kw = [x for x in kw_ if x not in remove]
    cols={}
    for kk in kw:
        fil=df[df['KEYWORD']==kk] # only occurances of kk
        kwrl=[]
        for yy in year:
            ll=fil[fil['YEAR']==yy]
            val=ll.iloc[0]['RANK'] if len(ll) else 999
            val=None if val > YCUTOFF else val
            kwrl.append(val)
        cols[kk]=kwrl
    cols['YEAR']=year
    grdf=pd.DataFrame(data=cols)
    
    gg=sns.lmplot(x='YEAR', y='Rank', hue='Keyword', 
                  scatter_kws = {'facecolors':'none'},
                  lowess=True,
                  ci=None,
                 legend=None,
                 data=pd.melt(grdf,['YEAR'],
                 value_name='Rank',
                 var_name='Keyword',
                              ))
    ax=gg.axes[0][0]
    #ax.invert_yaxis()
    ax.set(ylim=(MAXY, -.5))
    ax.set(xlim=(2002,2025))
    cols=kw
    
    loclist=['water policy', 'water data', 'irrigation water', 'irrigation', 'international']
    locdict={}
    for li in loclist:
        locdict[li]=[grdf[li].idxmin()]
        print("line:{}, min:{}, data:{}".format(li,locdict[li], list(grdf[li])))
    # locdict['water data']=[2014,12.]
    set_labels(cols, ax, locdict)
   
    plt.show()
    print (df)
    # get all keywords
    