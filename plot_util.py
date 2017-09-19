# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import time, os
import matplotlib.pylab as plt
import matplotlib

LINEWIDTH=0.5

c1 = plt.rcParams['axes.color_cycle'][0]
c2 = plt.rcParams['axes.color_cycle'][1]


matplotlib.rcParams.update({
    'font.family'    :'Myriad Pro',
    'font.size'      :7,
    'axes.labelsize' :'large',
    'axes.titlesize' :'large',
    'xtick.labelsize':'medium',
    'ytick.labelsize':'medium',
    'legend.fontsize':'medium',
    'axes.linewidth' :LINEWIDTH,
    'axes.grid'      :False,
    'xtick.major.size':2,
    'xtick.minor.size':0,
    'ytick.major.size':0,
    'ytick.minor.size':0,
    'legend.numpoints':1,
    'legend.frameon':False,
    'patch.facecolor':.4*np.ones(3),
    'patch.edgecolor':'None',
    })

import analysis_util

metadata_names = {'origin1':'Region', 'origin2':'Country', 'genre1':'Genre Class', 'genre2': 'Genre', 'era1': 'Era', 'chordRoot':'Chord Root'}
        
def plot_metadata_valence(metadata_df, lyric_info_df, plot_col, connectline=False, rotate=False):
    #most_popular = global_popular_vals[plot_col] # 
    most_popular = analysis_util.get_most_popular(metadata_df, plot_col)
    
    overall_happiness, oh_SE = analysis_util.get_sentiment_values(c_lyrics_all, plot_col)
    print ('Valence values (sorted)')
    print (overall_happiness.sort_values())
    print ()
    print ()
    if plot_col not in ['year','decade', 'era1']:
        pdf = overall_happiness.sort_values()
    else:
        pdf = overall_happiness # .iloc[::-1]
        
    analysis_util.bar_plot(pdf, 1.96*oh_SE, False, connectline, rotate=rotate)
    #plt.grid(False)
    xlabel, ylabel = 'Valence', metadata_names[plot_col]
    if not rotate:
        plt.xlabel(xlabel)
        plt.ylabel('')
        plt.title('')
    else:
        plt.xlabel(ylabel)
        plt.ylabel(xlabel)
        plt.title('')


def titlecase(s):
    return s[0].upper() + s[1:]


def do_wordshift(catdf, allwords_df, numtop=10, grpby='word'):
    mean_happiness = allwords_df.happiness.mean()
    avgprevalence = allwords_df.word.value_counts() / len(allwords_df)
    word_happiness = pd.DataFrame.from_records(list(analysis_util.happiness_dict.items()), columns=['word','happiness']).set_index('word').happiness

    catprevalence = catdf.word.value_counts() / len(catdf)
    cat_mean_happiness = catdf.happiness.mean()

    #catprevalence - avgprevalence
    wordshift = (100.0/np.abs(cat_mean_happiness - mean_happiness)) * (word_happiness - mean_happiness) * (catprevalence - avgprevalence)

    wordshift_df = pd.DataFrame({'ws':wordshift, 'wsabs':np.abs(wordshift)})
    #print (' sum:', wordshift_df.ws.sum())
    #print ('cat meanhappiness vs meanhappiness: %0.4f vs %.4f' % ( cat_mean_happiness , mean_happiness ))


    topvals = wordshift_df.sort_values(by='wsabs', ascending=False).iloc[numtop:0:-1]
    c1 = 'orange'
    c2 = 'blue'
    lbls = {}
    colors = {}
    for cword in topvals.index.values:
        # up_or_down = '\\uparrow' if catprevalence.loc[cword]>avgprevalence.loc[cword] else '\\downarrow'
        # plus_or_minus = '+' if word_happiness.loc[cword]>mean_happiness else '-'
        # spacer = '\\!\\!\\!\\!\\!'
        # if topvals.loc[cword].ws > 0:
        #     lbltext = cword + '$' + up_or_down + spacer + plus_or_minus + '$'
        # else:
        #     lbltext = '$' + up_or_down + spacer + plus_or_minus + '$' + cword
        up_or_down = '$\\!\\!\\%s\\!\\!$' % ('uparrow' if catprevalence.loc[cword]>avgprevalence.loc[cword] else 'downarrow')
        plus_or_minus = '+' if word_happiness.loc[cword]>mean_happiness else '-'
        if topvals.loc[cword].ws > 0:
            lbltext = cword + up_or_down + plus_or_minus
        else:
            lbltext = up_or_down + plus_or_minus + ' ' + cword
        lbls[cword] = lbltext
        colors[cword] = c1 if word_happiness.loc[cword]>mean_happiness else c2
    topvals['lbl'] = pd.Series(lbls)
    topvals['cols'] = pd.Series(colors)
    topvals = topvals.set_index('lbl')
        
    wordshift_plot(topvals, xpadding=0, textopts={'weight':'600','stretch':'condensed'})#,'fontsize':9})
    #plt.ylabel('Words in decreasing order of contribution percentage')
    plt.ylabel('')
    plt.xlabel('Contribution %')

def wordshift_plot(topvals, xpadding=0.0, textopts={}):
    c1 = plt.rcParams['axes.color_cycle'][0]
    c2 = plt.rcParams['axes.color_cycle'][1]

    all_ixs = np.arange(len(topvals))

    scolor = 0

    is_pos = np.array((topvals.ws >= 0).tolist())

    kw = {'color': topvals.cols} if 'cols' in topvals.columns else {}
    topvals.ws.plot(kind='barh', ax=plt.gca(), edgecolor='None',  width=.4, grid=False, **kw)

    plt.vlines(0, -20, 20, color='k', lw=LINEWIDTH)
    xmin, xmax = None, None
    invTrans = plt.gca().transData.inverted()
    for y, x in enumerate(topvals.ws):
        cword = topvals.index.values[y]
        ckw = textopts.copy()
        if 'cols' in topvals.columns:
            ckw['color'] = topvals.iloc[y].cols

        textobj = plt.text(x, y-0.1, ' ' + cword+ ' ', 
                           ha='left' if x>0 else 'right', 
                           va='center', **ckw)
        plt.draw()
        we = textobj.get_window_extent()
        cxmax, _ = invTrans.transform((we.xmax, we.ymax))
        if xmax is None or xmax < cxmax: 
            xmax = cxmax
        cxmin, _ = invTrans.transform((we.xmin, we.ymin))
        if xmin is None or xmin > cxmin: 
            xmin = cxmin
    plt.xlim([xmin-xpadding, xmax+xpadding])
    #plt.xlim([xmin*1.1-xpadding, xmax*1.1+xpadding])
    plt.ylim([-0.5, len(topvals)])
    plt.yticks([])
    #plt.gca().spines['top'].setp('color', 'k')
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.locator_params(axis='x',nbins=5)

def despine():
    ax=plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

def labelsubplots(axs, xoffset=None, yoffset=None):
    subplotlabels = 'abcdefghijklmnopqrst'.upper()
    for ndx, ax in enumerate(axs):
        cxoffset = xoffset[ndx] if type(xoffset)==list  else xoffset
        cyoffset = yoffset[ndx] if type(yoffset)==list  else yoffset
        if cxoffset is None:
            cxoffset = -15
        if cyoffset is None:
            cyoffset = 15
        plt.sca(ax)
        ncoords = ax.transAxes.transform([0,1])+np.array([cxoffset,cyoffset])
        ncoords = ax.transAxes.inverted().transform(ncoords)
        plt.text(ncoords[0], ncoords[1], subplotlabels[ndx], fontweight=550, fontsize='xx-large', va='top', transform=ax.transAxes)


def bar_plot(pdf, err=None, plot0=False, connectline=False, rotate=False, facecolor='None', edgecolor='k', plotargs={}, yoffset=0.0, xoffset=0.0, ax=None):
    df = pdf if not rotate else pdf.T
    if not rotate:
        df = pdf
    else:
        df = pdf.T[pdf.index.values]

    linewidth = LINEWIDTH
    df2 = pd.DataFrame({'val':df,'lbl':df.index.values,'linenum':range(len(df))})

    xcol = 'val' if not rotate else 'linenum'
    ycol = 'linenum' if not rotate else 'val'

    pfx = 'x' if not rotate else 'y'
    otherpfx = 'y' if not rotate else 'x'
    zeroline = 'vlines' if not rotate else 'hlines'

    df2[ycol] += yoffset
    df2[xcol] += xoffset

    ax = ax if ax is not None else plt.gca()
    h = df2.plot(kind='scatter', x=xcol, y=ycol, marker='o', s=25, zorder=10,
             c=[facecolor,]*len(df2), edgecolors=[edgecolor,]*len(df2), linewidth=linewidth, 
             sharex=False, sharey=False, ax=ax, grid=plt.rcParams['axes.grid']
             )
    handles = [h,]
    if err is not None:
        plt.errorbar(df2[xcol], df2[ycol], fmt='None', capthick=linewidth, capsize=3,
            linewidth=linewidth, ecolor=edgecolor, 
            #ax=ax, 
            grid=plt.rcParams['axes.grid'], **{pfx+'err':err.loc[df2.index.values]})

    limfunc = getattr(plt, pfx+'lim')
    lims = limfunc()
    if connectline:
        h = df2.plot(kind='line', x=xcol,y=ycol, ax=plt.gca(), linewidth=linewidth, color=edgecolor,
            sharex=False, sharey=False, legend=False, grid=plt.rcParams['axes.grid'])
        handles.append(h)
    limfunc(lims)

    getattr(plt, otherpfx+'ticks')(range(len(df)), df2.lbl.tolist())

    otherlims = [-0.5,len(df2)-0.5]
    getattr(plt,otherpfx+'lim')(otherlims)
    if plot0:
        getattr(plt, zeroline)(0, otherlims[0], otherlims[1], linestyles='--', colors='grey', linewidth=linewidth)

    plt.xlabel('')
    plt.ylabel('')

    despine()
    #plt.grid(False)
    if rotate:
        ax.tick_params('y', length=2, width=LINEWIDTH, which='major')

    return handles

def wordshift_legend(ax, xoffset, yoffset, bwidth=1.05):
    lineheight = 0.09
    import matplotlib.transforms as transforms

    trans = transforms.blended_transform_factory(
        ax.transAxes, ax.transAxes)

    ax2 = plt.gcf().add_axes([0,0,1,1])
    ax2.axis('off')
    ax2.xaxis.set_visible(False)
    ax2.yaxis.set_visible(False)
    ax2.set_zorder(1000)

    patch = plt.Rectangle((xoffset-0.025, yoffset-4*lineheight), bwidth, 4.5*lineheight , facecolor=[0.9,0.9,0.9], edgecolor='k',
                          linewidth=LINEWIDTH, transform=trans)
    ax2.add_patch(patch)

    txtprops = {'va':'top','transform':trans, 'fontsize':'small'}

    plt.text(xoffset, yoffset               , u'+  High valence', color='orange', **txtprops)
    plt.text(xoffset, yoffset - 1*lineheight, u' -  Low valence' , color='blue', **txtprops)
    plt.text(xoffset, yoffset - 2*lineheight, u'$↑$ Overexpressed', **txtprops)
    plt.text(xoffset, yoffset - 3*lineheight, u'$↓$ Underexpressed' , **txtprops)


def sharexlims(axs):
    xmin=min([0,]+[cax.get_xlim()[0] for cax in axs])
    xmax=max([0,]+[cax.get_xlim()[1] for cax in axs])

    for cax in axs:
        cax.set_xlim(xmin, xmax)

def mysavefig(fname):
    from config import PLOTOUTPUTDIR
    bname = PLOTOUTPUTDIR + fname + '.pdf'
    print("Saving to %s" % bname)
    plt.savefig(bname, dpi=300, bbox_inches='tight')


