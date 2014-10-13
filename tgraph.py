# /usr/bin/python

#
# methods to operate with ROOT
# @author Jose A. Hernando
# @date 120810
#

from ROOT import *
from math import *
import array
import os

def tgraph(vals,title='tgraph'):
    """ makes a graph from a list of values, 
    the 1st list is the x axis, the 2nd list is y axis.
    (optional): the 3rd list are the x-errors; 4th list are y-errors. 
    """
    nx = len(vals)
    nn = len(vals[0])
    x = array.array('f',vals[0])
    y = array.array('f',vals[1])
    if (nx==2):
        t = TGraph(nn,x,y)
    elif (nx==4):
        ex = array.array('f',vals[2])
        ey = array.array('f',vals[3])
        t = TGraphErrors(nn,x,y,ex,ey)
    else:
        raise TypeError('Not valid number of values!')
    t.SetTitle(title)
    return t  


def tasymgraph(vals,title='tasymgraph'):
    """ takes a list of list of values and makes an asymmetric graph.
    the first list is the x axis, the second the y
    3rd the lower errors on y and the 4th the upper ones
    (optional): 5th they lowers x-errors, 6th the upper x-errros
    """
    x = array.array('f',map(lambda x: x[0],vals))
    y = array.array('f',map(lambda x: x[1],vals))
    ey0 = array.array('f',vals[2])
    ey1 = array.array('f',vals[3])
    ex0 = array.array('f',[0.]*len(x))
    ex1 = array.array('f',[0.]*len(x))
    nx = len(vals)
    if (nx == 6):
        ex0 = array.array('f',vals[4])
        ex1 = array.array('f',vals[5])        
    t = TGraphAsymmErrors(n,x,y,ex0,ex1,ey0,ey1)
    t.SetTitle(title)
    return t  

def tmultigraph(tgs):
    """ returns a multigraph from a list of graph
    """
    mg = TMultiGraph()
    for tg in tgs: mg.Add(tg)
    return mg

def tgraph_from_histo(h1):
    """ makes a graph from a histogram
    """
    nps=range(h1.GetXaxis().GetNbins())
    xs=[]
    ys=[]
    exs=[]
    eys=[]
    for po in nps:
        x = (h1.GetBinLowEdge(po+1)+h1.GetBinLowEdge(po))/2.
        y = h1.GetBinContent(po)
        if (y==0): continue
        xs.append(x)
        exs.append((h1.GetBinLowEdge(po+1)-h1.GetBinLowEdge(po))/sqrt(12))
        ys.append(h1.GetBinContent(po))
        eys.append(h1.GetBinError(po))
    myg=tgraph([xs,ys,exs,eys])
    return myg
