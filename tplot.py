#------------------------------------------
# Interface module for graph and histos
# Implementation with ROOT
#------------------------------------------

from ROOT import *
from math import *
from thisto import thisto
from tgraph import tgraph
import array 
import random

# default style
#-----------------------

gStyle.SetFillColor(0)
gStyle.SetLineWidth(2)

#-----------------------------------------
#  Histograms, Graphs
#-----------------------------------------

class TDeco():
    """ Virtual class to decorate objects with a menu
    """

    def __init__(self,menu):
        """ constructor with a dictonary with the menu (options listed by key)
        """
        self._menu = dict(menu)
        self._configs = {}

    def menu(self):
        """ returns the keys of the menu """
        return self._menu.keys()

    def options(self,name):
        """ returns the option of a given name (key) of the menu """
        if (not self._menu.has_key(name)):
            raise TypeError(' not name in menu!')
        return self._menu[name]
    
    def configurations(self):
        """ return the list of pre-defined configurations """
        return self._configs.keys()
    
    def defconfiguration(self,name,conf):
        """ define a configuration with a given name. 
        conf is a list os pair (key,option) """
        self._configs[name] = list(conf)
        return

    def configuration(self,name):
        """ return the list of (key,option) list of the configuration """
        if (not self._configs.has_key(name)):
            raise TypeError(' No configuration with that name!')
        return self._configs[name]
    
    def hasdeco(self,h):
        """ returns true if the h-object has a decorator as attribute """
        return hasattr(h,'deco')

    def setconfiguration(self,h,name):
        """ sets a given configuration inside an object h """
        if (not self._configs.has_key(name)):
            raise TypeError(' No configuration with that name!')
        conf = self._configs[name]
        for iconf in conf:
            cc,val = iconf
            self.setoption(h,cc,val)
        return
    
    def setoption(self,h,name,val):
        """ set an option of a name (key) of the menu on an object """
        if (not self.hasdeco(h)): h.deco = {}
        h.deco[name] = val
        
    def getoption(self,h,name):
        """ get the option of name (key) of the menu of an object """
        if (not self.hasdeco(h)): return None
        if (not h.deco.has_key(name)): return None
        return h.deco[name]
    
#-----------------------------------------
#     Menu to decorate histograms
#-----------------------------------------

TMenu = {'color':['black','red','blue','violet','orange'],
         'marker':['circle','square','triangle','star','cross'],
         'line':['full','dashed','dotted','dash-dot','dashed-short']}

#------------------------------------------
#     TDeco implementation for histograms
#------------------------------------------

class RootTDeco(TDeco):
    """ class to decorate ROOT histograms objects with a menu
    """

    dcolors = {'black':kBlack,'red':kRed,'blue':kBlue,
               'violet':kViolet,'orange':kOrange}
    dmarkers = {'circle':kFullCircle,'square':kFullSquare,
                'triange':kFullTriangleUp,'star':kFullStar,'cross':34}
    dlines = {'full':1,'dashed':9,'dotted':3,'dash-dot':10,'dashed-short':5}

    def __init__(self):
        """ create the RootTDeco class and set defaults configurations
        """
        TDeco.__init__(self,TMenu)
        i = 0
        for marker in TMenu['marker']:
            for line in TMenu['line']:
                for color in TMenu['color']:
                    conf=zip(('color','maker','line','width'),
                             (color,marker,line,2))
                    self.defconfiguration(i,conf)
                    i+=1
        return
        
    def setoption(self,h,name,val):
        """ set option (keys: color, marker, line, width, xtitle, ytitle)
        """
        TDeco.setoption(self,h,name,val)
        if (name == 'color'):
            h.SetLineColor(RootTDeco.dcolors[val])
            h.SetMarkerColor(RootTDeco.dcolors[val])
        elif (name == 'marker'):
            h.SetMarkerStyle(RootTDeco.dmarkers[val])
        elif (name == 'line'):
            h.SetLineStyle(RootTDeco.dlines[val])
        elif (name=='width'):
            h.SetLineWidth(val)
            #h.SetMarkerSize(val)
        elif (name=='xtitle'): 
            obj.GetXaxis().SetTitle(val)
        elif (name=='ytitle'):
            obj.GetYaxis().SetTitle(val)
        return

#-----------------------------------------------------
#  functions to create histograms, graphs and draw 
#  ROOT implementation
#-----------------------------------------------------

# shortcut for RootTDeco class
RTDeco = RootTDeco()

def tsetoption(h,opt,val):
    """ set an option into a object
    """
    RTDeco.setoption(h,opt,val)
    return 

def tconfigure(hs,confs=None):
    """ use a predefined configuration to set options in object
    """
    if (not isinstance(hs,list)): hs = [hs]
    if (not confs): confs = RTDeco.configurations()
    if (len(confs)<len(hs)):
        raise TypeError('Not enough different configurations!')
    else: confs = confs[:len(hs)]
    map(lambda hi,conf: RTDeco.setconfiguration(hi,conf),hs,confs)
    return

def tdraw(h,opt=''):
    """ draw a ROOT object, default opt 'E' for TH1F, and 'AL' for TGraph.
    If h is a list, 'same' opt in applied
    """
    if (isinstance(h,list)):
        tdraw(h[0],opt)
        map(lambda hi: tdraw(hi,'same'+opt),h[1:])
        return
    if (isinstance(h,TH1F)): opt = ''+opt #opt='E'+opt
    elif (isinstance(h,TGraph)): 
        if (opt.find('same')): opt='L'+opt
        else: opt = 'AL'+opt
    elif (isinstance(h,TLegend)): opt+='same'
    elif (isinstance(h,TPaveText)): opt+='same'
    h.Draw(opt)
    return 

def tcanvas(hs,nx=1,name=None,opts=None):
    """ makes a canvas a plot the objects in hs in a nx,xy grid """
    c = TCanvas()
    if (not isinstance(hs,list)): hs=[hs]
    ny = len(hs)/nx+len(hs)%nx
    c.Divide(nx,ny)
    for i in range(len(hs)):
        c.cd(i+1)
        opt = ''
        if (opts): opt = opts[i]
        tdraw(hs[i],opt)
    if (name): c.SaveAs(name+'.pdf')
    return c

def tlegend(objs,names,opt='PL'):
    """ creates a legend for a list of object
    """
    t = TLegend(0.6,0.6,0.8,0.8)
    t.SetBorderSize(1)
    t.SetTextSize(0.04)
    map(lambda o,n: t.AddEntry(o,str(n),opt),objs,names)
    return t

def tpave(lines,ene=7,x0=0.6,y0=0.8,x1=0.9,y1=0.9):
    t = TPaveText(x0,y0,x1,y1,'BRNDC')
    t.SetBorderSize(1)
    t.SetTextSize(0.04)
    for line in lines: t.AddText(line)
    return t

#----------------------------------------
# check
#----------------------------------------

def check():
    """ check of some configurations
    """ 
    import random
    n = 1000
    hs = []
    for i in range(4):
        xs = map(lambda k: random.gauss(1.*i,1.),range(n))
        hi = thisto(xs,'h'+str(i),100,-10.,10.)
        hs.append(hi)
    tconfigure(hs)
    c1 = tcanvas([hs])
    legend = tlegend(hs,[0,1,2,3])
    tdraw(legend)
    c2 = tcanvas(hs,nx=2)
    return c1,c2,hs,legend # returns all the object otherwise ROOT delete them!
