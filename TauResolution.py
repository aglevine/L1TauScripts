'''
Makes Tau efficiency plots
Authors: T.M.Perry, E.K.Friis, M.Cepeda, A.G.Levine, N.Woods UW Madison
'''
from sys import argv, stdout, stderr
import ROOT
import sys
import array

##################
# Set Parameters #
##################
LIso=3
LSB=50
recoPtVal=20
saveDir=argv[1]
res_ntuple_str=argv[2]
saveStr=argv[3]
etaLow=argv[4]
etaHigh=argv[5]
l1PtLow=argv[6]
l1PtHigh=argv[7]
L1_CALIB_FACTOR = 1.0
L1G_CALIB_FACTOR = 1.0
saveWhere = saveDir+'Plots/Res_'+saveStr+'eta_'+etaLow+'_'+etaHigh+'_l1pt_'+l1PtLow+'_'+l1PtHigh

########
# File #
########
#Efficiency
res_ntuple_str=saveDir+res_ntuple_str
print res_ntuple_str
res_ntuple_file = ROOT.TFile(res_ntuple_str)
#res_mc_ntuple_file = ROOT.TFile("RCTV2CalibNtuples_FullStatsApril28/tau_emul_effRCTV2CalibDefaultActs3TauVetoThresh60Iso12.root")
res_mc_ntuple_file = ROOT.TFile("StartupMC2015/tau_emul_eff_DYStartupActs3TauVetoThresh60Iso12.root")
print res_ntuple_file
#
res_spot = 'TauEmulEffi/Ntuple'
res_iso_spot = 'TauEmulEffiIso/Ntuple'
res_ntuple = res_ntuple_file.Get(res_spot)
print res_ntuple
res_iso_ntuple = res_ntuple_file.Get(res_iso_spot)
res_mc_ntuple = res_mc_ntuple_file.Get(res_spot)
res_mc_iso_ntuple = res_mc_ntuple_file.Get(res_iso_spot)
store = ROOT.TFile(saveWhere+'.root','RECREATE')

#########
# STYLE #
#########

ROOT.gROOT.LoadMacro("tdrstyle.C")
ROOT.setTDRStyle()
ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetOptStat(0)

tex = ROOT.TLatex()
tex.SetTextSize(0.07)
tex.SetTextAlign(11)
tex.SetNDC(True)

variable = "pt[1]"
canvas = ROOT.TCanvas("asdf", "adsf", 800, 800)
canvas.SetGrid()

def make_plot(tree, variable, selection, binning, title,leg,color,marker,calFactor=1):
  ''' Plot a variable using draw and return the histogram '''
  draw_string = variable +" * %0.2f>>htemp(%s)" % (calFactor, ", ".join(str(x) for x in binning))
  print "draw_string "+ draw_string
  print selection
  tree.Draw(draw_string, selection, "goff")
  print tree
  resHisto = ROOT.gDirectory.Get("htemp").Clone()
  print "draw_string "+ draw_string
  print selection
  #ROOT.gDirectory.Clear()
  #output_histo.Rebin(10,"output_histoRebinned",xBins)
  #output_histoRebinned=ROOT.gDirectory.Get("output_histo").Clone()
  #ROOT.gDirectory.Clear()
  #output_histoRebinned = ROOT.gDirectory.Get("output_histoRebinned").Clone()
 
  resHisto.SetTitle(title)
  resHisto.SetMarkerStyle(marker)
  resHisto.SetMarkerColor(color)
  resHisto.SetMarkerSize(1.5)
  resHisto.SetLineColor(color)
  leg.AddEntry(resHisto,title,'pe')
  
  resHisto.Sumw2()
  resHisto.Scale(1/resHisto.Integral())
  resHisto.Draw("ep")

  
  resGauss = resHisto.Clone()
  resFit = ROOT.TF1("asdf","gaus",-0.4,0.4)
  resGauss.Fit(resFit,"R")
  resGauss.SetLineColor(color)

  #resFit.Draw("lsames")
  resFitMean = resFit.GetParameter(1)
  return resHisto,resFit,resFitMean



def compare_resolution(
  variable,
  binning,
  ntuple=None,
  ntuple_iso=None,
  ntuple_mc=None,
  ntuple_mc_iso=None,
  recoPtCut='(1)',l1PtCut='(1)',l1PtCutOld='(1)',
  extraCut = '&&(1)',
):
  '''
  Returns a (L1, L1G) tuple of TGraphAsymmErrors
  '''
  print ntuple.GetEntries()
  cutD_rlx = recoPtCut+extraCut
  cut_L1=cutD_rlx+'&&'+l1PtCut+'&& L1matches[0]>-1'
  print "cut_L1" 
  print ntuple
  
  frame.SetTitle('Resolution')
  frame.SetMaximum(0.3)

  frame.GetXaxis().SetTitle("(recoPt-L1Pt)/recoPt")

  legend = ROOT.TLegend(0.63,0.55,0.95,0.95,'','brNDC')
  legend.SetTextSize(0.033)
  legend.SetFillColor(0)
  legend.SetBorderSize(0)

  res,resFit,resMean= make_plot(
   ntuple,variable,
   cut_L1,
   binning,'Data: Rlx',legend,ROOT.EColor.kGreen+3,20
  )
  res_iso,res_isoFit,res_isoMean= make_plot(
   ntuple_iso,variable,
   cut_L1,
   binning,'Data: Iso',legend,ROOT.EColor.kBlue,20
  )
  res_mc,res_mcFit,res_mcMean= make_plot(
   ntuple_mc,variable,
   cut_L1,
   binning,'MC: Rlx',legend,ROOT.EColor.kGreen+3,24
  )
  res_mc_iso,res_mc_isoFit,res_mc_isoMean= make_plot(
   ntuple_mc_iso,variable,
   cut_L1,
   binning,'MC: Iso',legend,ROOT.EColor.kBlue,24
  )

  frame = ROOT.TH1F('frame','frame',25,-1,1)
  frame.Draw("")
  frame.SetTitle('Resolution')
  frame.SetMaximum(0.3)

  frame.GetXaxis().SetTitle("(recoPt-L1Pt)/recoPt")
  
  
  res.Draw("ep")
  res_iso.Draw("epsames")
  res_mc.Draw("epsames")
  res_mc_iso.Draw("epsames")
  res.GetYaxis().SetRangeUser(0,0.3)
  res.SetTitle("L1 Tau Resolution")
  print ntuple

  latex = ROOT.TLatex()
  latex.SetNDC()
  latex.SetTextSize(0.035)
  latex.SetTextAlign(31)
  strRlxMean = "Rlx Data Fit Mean: %.2f"%(resMean)
  strIsoMean = "Iso Data Fit Mean: %.2f"%(res_isoMean)
  strRlxMCMean = "Rlx MC Fit Mean: %.2f"%(res_mcMean)
  strIsoMCMean = "Iso MC Fit Mean: %.2f"%(res_mc_isoMean)
  strL1PtRange = str(l1PtLow)+" L1Pt < "+str(l1PtHigh)
  strEtaRange = "       |#eta|<2.5"
  latex.DrawLatex(0.4,0.8,strRlxMean)
  latex.DrawLatex(0.4,0.77,strIsoMean)
  latex.DrawLatex(0.4,0.74,strRlxMCMean)
  latex.DrawLatex(0.4,0.71,strIsoMCMean)
  latex.DrawLatex(0.4,0.68,strL1PtRange)
  latex.DrawLatex(0.4,0.65,strEtaRange)
  
  
 
  legend.Draw("sames")
 
  canvas.SaveAs(saveWhere+saveStr+'.png')
######################################################################
##### EFFICIENCY #####################################################
######################################################################


######################################################################
###### DRAW PLOTS ####################################################
######################################################################
####################
# Efficiency Plots #
####################
#binPt = [10,40,80] #l120
xBins = array.array('d',[20,25,30,35,40,45,50,55,60,80,100,130,200])
binPt = [20,0,100]
binVert=[10,0,35]
binJetPt=[40,0,70]
binEta = [10,-2.5,2.5]
bin2DPt = [10,0,100,10,0,100]
binRes = [25,-1,1]

resVar = '(pt[0]-L1Matchedpt[0])/pt[0]'
resRecoPtCut = '(pt[0] >= '+str(recoPtVal)+')'
resL1PtCut = '(L1Matchedpt[0] >= '+str(l1PtLow)+'&&L1Matchedpt[0]< '+str(l1PtHigh)+')'
extraCutStr = '&&eta[0]>'+str(-2.5)+'&&eta[0]<'+str(2.5)+'&&L1Matchedeta[0]>'+str(etaLow)+'&&L1Matchedeta[0]<'+str(etaHigh)
compare_resolution(
  resVar,
  binRes,
  res_ntuple,
  res_iso_ntuple,
  res_mc_ntuple,
  res_mc_iso_ntuple,
  resRecoPtCut,
  resL1PtCut,
  l1PtCutOld='(L1Matchedpt[0] >= 40)&&(L1Matchedpt[1]>= 40)',
  extraCut=extraCutStr,
)
