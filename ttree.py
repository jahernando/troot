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

#DUMMY = TFile('dummy.root','RECREATE')
DEBUG = False

#------------ ntuples and histograms

def treel_labels(tree):
    """ return the list of tree labels """
    a = tree.GetListOfLeaves()
    vars = map(lambda ai: ai.GetName(),a)
    return vars

def treevar(tree,varname,n=-1):
    """ return a list with the value of a varible (name) in all the entries of the tree
    """
    vals = map(lambda i: getattr(tree,varname),tree)
    return vals
    #vals = []
    #for e in tree:
    #    val = tree_value(tree,name)
    #    vals.append(val)
    #    if (n>0 and len(vals)>=n): return vals
    #return vals    

def treevar_entry(tree,varname):
    """ return the value of the tree variable in the current entry """
    return getattr(tree,varname)

def treevar_histo(tree,var,n=100,x0=None,xf=None):
    """ create and fill a TH1F histogram with the variable of the tree
    if uflow is set to True the under/overflow are set in the first/last bin
    """
    xs = treevar(tree,var)
    th = thisto(xs,n,x0,xf)
    return th

def treevar_histo2(tree,var1,var2,nx,x0,xf,ny,y0,yf):
    """ create and fill a TH1D histogram with the variable of the tree
    """
    #xs = treevar(tree,var1)
    #ys = treevar(tree,var2)
    h = TH2F(va1+'vs '+va2,va1+' + '+va2,nx,x0,xf,ny,y0,yf)
    for e in tree: 
        x = getattr(tree,va1)
        y = getattr(tree,va2)
        h.Fill(x,y)
    return h

#------------ operation with trees

def tree_reduce(t1,vars,tname='tree',fname='tree_reduce.root'):
    """ create a new tree with a reduced number of variables
    """
    nvars = len(vars)
    leafs = map(lambda var: var+"/F",vars)
    leafsvalue = map(lambda i: array.array('f',[0.0]),range(nvars))
    print ' creating file ',fname
    nfile = TFile(fname,'RECREATE')
    ntree = TTree(tname,tname)
    print ' creating tree ',tname,' labels ',vars
    map(lambda var,leafvalue,leaf: ntree.Branch(var,leafvalue,leaf),
        vars,leafsvalue,leafs)
    for i in range(t1.GetEntries()):
        t1.GetEntry(i)
        vals = map(lambda var: tree_varentry(t1,var),vars)
        for j in range(nvars):
            var = vars[j]
            leafsvalue[j][0]=float(vals[j])
        ntree.Fill()
        if (i%100 == 0): print " reducing tree, event ",i,vals
    ntree.Write()
    nfile.Close()
    print ' created reduced tree'
    return nfile,ntree

def tree_to_dictionary(tt,vars):
    """ returns a python dictionary with the labels of the ntuple and value content is the list of the values of the variable in the ntuple
    """
    tdic = {}
    if (not vars): vars = tree_labels()
    for var in vars: tdic[var] = treevar(tt,var)
    return tdic

def dictionary_to_tree(tdic,tname="Tree",fname="dtree.root"):
    """ convert a dictionary into a ntuple (floats)
    """
    vars = tdic.keys()
    nvars = len(vars)
    nsize = len(tdic[vars[0]])
    leafs = map(lambda var: var+"/F",vars)
    leafsvalue = map(lambda i: array.array('f',[0.0]),range(nvars))
    print ' creating file ',fname
    nfile = TFile(fname,'RECREATE')
    ntree = TTree(tname,tname)
    print ' creating tree ',tname,' labels ',vars
    map(lambda var,leafvalue,leaf: ntree.Branch(var,leafvalue,leaf),
        vars,leafsvalue,leafs)
    for i in range(nsize):
        vals = map(lambda var: tdic[var][i],vars)
        for j in range(nvars):
            var = vars[j]
            leafsvalue[j][0]=float(vals[j])
        ntree.Fill()
        if (i%100 == 0): print " creating tree, event ",i,vals
    ntree.Write()
    nfile.Close()
    print ' created tree ',tname,' in ',tname
    return ntree

