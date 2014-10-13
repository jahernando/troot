# /usr/bin/python

#
# methods to operate with ROOT
# @author Jose A. Hernando
# @date 120810
#

from ROOT import *
from math import *
import array
import random
import os

DEBUG = False

#--------- histograms 

def thisto(xs,title='thisto',nbins=100,x0=None,xf=None):
    """ fill a histogram from a list """
    if (not x0): x0 = min(xs)
    if (not xf): xf = 1.01*max(xs)
    h = TH1F(title,title,nbins,x0,xf)
    for x in xs: h.Fill(x)
    return h

def thisto_scale(h,size=1.):
    """ Scale the histogram to a given size, the current histogram is modified
    """ 
    n = h.GetEntries()
    h.Scale(size/float(n))
    return 

def thistos_scale(href,his):
    """ takes a reference histogram and a list of histograms
    scale the histograms in the list to the entries in the reference histograms
    histograms are modified, nothing is returned
    """
    n1 = float(href.GetEntries())
    map(lambda h : h.Scale(n1/float(h.GetEntries())), his)
    return
