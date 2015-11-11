'''
Makes Tau efficiency plots
Authors: T.M.Perry, E.K.Friis, M.Cepeda, A.G.Levine, N.Woods UW Madison
'''
from sys import argv, stdout, stderr
import ROOT
import sys
import array
import math
import random

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
L1_CALIB_FACTOR = float(argv[8])
doProngs=False
doActs=False
doTauVetos=False
doIsos=False
doTauCalib=False
doPreLauraRCTCalib=False
saveWhere = saveDir+'Plots_Res/Res_'+saveStr+'eta_'+etaLow+'_'+etaHigh+'_l1pt_'+l1PtLow+'_'+l1PtHigh+'_CalibFactor_'+str(L1_CALIB_FACTOR)
if (doActs):
        saveWhere = saveWhere+'ActsCmp'
if(doTauVetos):
        saveWhere = saveWhere+'TauVetosCmp'
if(doIsos):
        saveWhere = saveWhere+'IsosCmp'
if(doProngs):
	saveWhere = saveWhere+'Prongs'
if(doPreLauraRCTCalib):
	saveWhere = saveWhere+'PreRCTCalibTauLUT'

########
# File #
########
#Efficiency
res_ntuple_str=saveDir+res_ntuple_str
print res_ntuple_str
res_ntuple_file = ROOT.TFile(res_ntuple_str)
#res_mc_ntuple_file = ROOT.TFile("RCTV2CalibNtuples_FullStatsApril28/tau_emul_effRCTV2CalibDefaultActs3TauVetoThresh60Iso12.root")
#res_mc_ntuple_file = ROOT.TFile("EffiData2015C/tau_emul_eff_DYStartup25ns_Acts4TauVetoThresh64Iso1_CalibFrom4.root")
res_mc_ntuple_file = ROOT.TFile("EffiData2015D/tau_emul_eff_DYStartup25ns_Acts4TauVetoThresh64Iso1_V1Calib.root")
print res_ntuple_file
#
res_spot = 'TauEmulEffi/Ntuple'
res_iso_spot = 'TauEmulEffiIso/Ntuple'
res_ntuple = res_ntuple_file.Get(res_spot)
print res_ntuple
res_iso_ntuple = res_ntuple_file.Get(res_iso_spot)
res_mc_ntuple = res_mc_ntuple_file.Get(res_spot)
res_mc_iso_ntuple = res_mc_ntuple_file.Get(res_iso_spot)

resA2_ntuple=None
resA3_ntuple=None
resA4_ntuple=None
resA5_ntuple=None
resTV52_ntuple=None
resTV56_ntuple=None
resTV60_ntuple=None
resTV64_ntuple=None
resTV68_ntuple=None
resIso1_ntuple=None
resIso12_ntuple=None
resIso13_ntuple=None
resIso15_ntuple=None
resIso2_ntuple=None
if (doActs):
        resA2_ntuple_file = ROOT.TFile("EffiData/tau_emul_eff_SingleMuon2015B_Acts2TauVetoThresh60Iso12_LaserCalib_DecayMode_RecoForIsobel.root")
        resA3_ntuple_file = ROOT.TFile("EffiData/tau_emul_eff_SingleMuon2015B_Acts3TauVetoThresh60Iso12_LaserCalib_DecayMode_RecoForIsobel.root")
        resA4_ntuple_file = ROOT.TFile("EffiData/tau_emul_eff_SingleMuon2015B_Acts4TauVetoThresh60Iso12_LaserCalib_DecayMode_RecoForIsobel.root")
        resA5_ntuple_file = ROOT.TFile("EffiData/tau_emul_eff_SingleMuon2015B_Acts5TauVetoThresh60Iso12_LaserCalib_DecayMode_RecoForIsobel.root")

        resA2_ntuple = resA2_ntuple_file.Get(eff_spot)

        resA3_ntuple = resA3_ntuple_file.Get(eff_spot)

        resA4_ntuple = resA4_ntuple_file.Get(eff_spot)

        resA5_ntuple = resA5_ntuple_file.Get(eff_spot)

if (doTauVetos):
        resTV52_ntuple_file = ROOT.TFile("EffiData/tau_emul_eff_SingleMuon2015B_Acts3TauVetoThresh52Iso12_LaserCalib_DecayMode_RecoForIsobel.root")
        resTV56_ntuple_file = ROOT.TFile("EffiData/tau_emul_eff_SingleMuon2015B_Acts3TauVetoThresh56Iso12_LaserCalib_DecayMode_RecoForIsobel.root")
        resTV60_ntuple_file = ROOT.TFile("EffiData/tau_emul_eff_SingleMuon2015B_Acts3TauVetoThresh60Iso12_LaserCalib_DecayMode_RecoForIsobel.root")
        resTV64_ntuple_file = ROOT.TFile("EffiData/tau_emul_eff_SingleMuon2015B_Acts3TauVetoThresh64Iso12_LaserCalib_DecayMode_RecoForIsobel.root")
        resTV68_ntuple_file = ROOT.TFile("EffiData/tau_emul_eff_SingleMuon2015B_Acts3TauVetoThresh68Iso12_LaserCalib_DecayMode_RecoForIsobel.root")

        resTV52_ntuple = resTV52_ntuple_file.Get(eff_spot)

        resTV56_ntuple = resTV56_ntuple_file.Get(eff_spot)

        resTV60_ntuple = resTV60_ntuple_file.Get(eff_spot)

        resTV64_ntuple = resTV64_ntuple_file.Get(eff_spot)

        resTV68_ntuple = resTV68_ntuple_file.Get(eff_spot)

if (doIsos):
        resIso1_ntuple_file = ROOT.TFile("EffiData/tau_emul_eff_SingleMuon2015B_Acts3TauVetoThresh60Iso1_LaserCalib_DecayMode_RecoForIsobel.root")
        resIso12_ntuple_file = ROOT.TFile("EffiData/tau_emul_eff_SingleMuon2015B_Acts3TauVetoThresh60Iso12_LaserCalib_DecayMode_RecoForIsobel.root")
        resIso13_ntuple_file = ROOT.TFile("EffiData/tau_emul_eff_SingleMuon2015B_Acts3TauVetoThresh60Iso13_LaserCalib_DecayMode_RecoForIsobel.root")
        resIso15_ntuple_file = ROOT.TFile("EffiData/tau_emul_eff_SingleMuon2015B_Acts3TauVetoThresh60Iso15_LaserCalib_DecayMode_RecoForIsobel.root")
        resIso2_ntuple_file = ROOT.TFile("EffiData/tau_emul_eff_SingleMuon2015B_Acts3TauVetoThresh60Iso2_LaserCalib_DecayMode_RecoForIsobel.root")

        resIso1_ntuple = resIso1_ntuple_file.Get(eff_spot)

        resIso12_ntuple = resIso12_ntuple_file.Get(eff_spot)

        resIso13_ntuple = resIso13_ntuple_file.Get(eff_spot)

        resIso15_ntuple = resIso15_ntuple_file.Get(eff_spot)

        resIso2_ntuple = resIso2_ntuple_file.Get(eff_spot)

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
  variableNoCalib,
  binning,
  ntuple=None,
  ntuple_iso=None,
  ntuple_mc=None,
  ntuple_mc_iso=None,
  ntupleA2=None,
  ntupleA3=None,
  ntupleA4=None,
  ntupleA5=None,
  ntupleTV52=None,
  ntupleTV56=None,
  ntupleTV60=None,
  ntupleTV64=None,
  ntupleTV68=None,
  ntupleIso1=None,
  ntupleIso12=None,
  ntupleIso13=None,
  ntupleIso15=None,
  ntupleIso2=None,
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
   
  frame = ROOT.TH1F('frame','frame',*binning)
  frame.Draw("")
  frame.SetTitle('Resolution')
  frame.SetMaximum(0.3)

  frame.GetXaxis().SetTitle("(recoPt-L1Pt)/recoPt")

  legend = ROOT.TLegend(0.63,0.55,0.95,0.95,'','brNDC')
  legend.SetTextSize(0.033)
  legend.SetFillColor(0)
  legend.SetBorderSize(0)
  '''
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
   ntuple_mc,variableNoCalib,
   cut_L1,
   binning,'MC: Rlx',legend,ROOT.EColor.kGreen+3,24
  )
  res_mc_iso,res_mc_isoFit,res_mc_isoMean= make_plot(
   ntuple_mc_iso,variableNoCalib,
   cut_L1,
   binning,'MC: Iso',legend,ROOT.EColor.kBlue,24
  )
  print "resMean: " + str(resMean)
  #frame.SetMaximum(0.3)

  #frame.GetXaxis().SetTitle("(recoPt-L1Pt)/recoPt")
  
  
  res.Draw("ep")
  res.GetXaxis().SetTitle("(recoPt-L1Pt)/recoPt")
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
  strL1PtRange = str(l1PtLow)+" < L1Pt < "+str(l1PtHigh)
  strEtaRange = str(etaLow)+" < |#eta| < "+str(etaHigh)
  strCalib = "L1 Calib Factor: " + str(L1_CALIB_FACTOR)
  latex.DrawLatex(0.4,0.8,strRlxMean)
  latex.DrawLatex(0.4,0.77,strIsoMean)
  latex.DrawLatex(0.4,0.74,strRlxMCMean)
  latex.DrawLatex(0.4,0.71,strIsoMCMean)
  latex.DrawLatex(0.4,0.68,strL1PtRange)
  latex.DrawLatex(0.4,0.65,strEtaRange)
  '''
  resMean=0 
  res_isoMean=0
  if (doProngs):
    cut_L13prong = cut_L1+"&&decayMode[0]==10"
    cut_L11prong = cut_L1+"&&decayMode[0]==1"
    cut_L10prong = cut_L1+"&&decayMode[0]==0"
    res3prong,resFit3prong,resMean3prong= make_plot(
     ntuple,variable,
     cut_L13prong,
     binning,'Data: Rlx 3 prong',legend,ROOT.EColor.kGreen+3,20
    )
    res1prong,resFit1prong,resMean1prong= make_plot(
     ntuple,variable,
     cut_L11prong,
     binning,'Data: Rlx 1 prong 1 pi0',legend,ROOT.EColor.kRed,20
    )
    res0prong,resFit0prong,resMean0prong= make_plot(
     ntuple,variable,
     cut_L10prong,
     binning,'Data: Rlx 1 prong 0 pi0',legend,ROOT.EColor.kBlue,20
    )	

    res3prong.Draw("ep")
    res3prong.GetXaxis().SetTitle("(recoPt-L1Pt)/recoPt")
    res1prong.Draw("epsames")
    res0prong.Draw("epsames")
    res3prong.GetYaxis().SetRangeUser(0,0.3)
    res3prong.SetTitle("L1 Tau Resolution")
    print ntuple
 
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.035)
    latex.SetTextAlign(31)
    str3prongMean = "3 Prong Fit Mean: %.2f"%(resMean3prong)
    str1prongMean = "1 Prong Fit Mean: %.2f"%(resMean1prong)
    str0prongMean = "0 Prong Fit Mean: %.2f"%(resMean0prong)
    strL1PtRange = str(l1PtLow)+" < L1Pt < "+str(l1PtHigh)
    strEtaRange = str(etaLow)+" < |#eta| < "+str(etaHigh)
    strCalib = "L1 Calib Factor: " + str(L1_CALIB_FACTOR)
    latex.DrawLatex(0.45,0.8,str3prongMean)
    latex.DrawLatex(0.45,0.77,str1prongMean)
    latex.DrawLatex(0.45,0.74,str0prongMean)
    legend.Draw("sames")
  elif (doActs):
    resA2,resFitA2,resMeanA2= make_plot(
     ntupleA2,variable,
     cut_L1,
     binning,'L1: A2 Rlx',legend,ROOT.EColor.kGreen+3,20
    )
    resA3,resFitA3,resMeanA3= make_plot(
     ntupleA3,variable,
     cut_L1,
     binning,'L1: A3 Rlx',legend,ROOT.EColor.kGreen+3,20
    )
    resA4,resFitA4,resMeanA4= make_plot(
     ntupleA4,variable,
     cut_L1,
     binning,'L1: A4 Rlx',legend,ROOT.EColor.kGreen+3,20
    )
    resA5,resFitA5,resMeanA5= make_plot(
     ntupleA5,variable,
     cut_L1,
     binning,'L1: A5 Rlx',legend,ROOT.EColor.kGreen+3,20
    )
    resA2.Draw("ep")
    resA2.GetXaxis().SetTitle("(recoPt-L1Pt)/recoPt")
    resA3.Draw("epsames")
    resA4.Draw("epsames")
    resA5.Draw("epsames")
    resA2.GetYaxis().SetRangeUser(0,0.3)
    resA2.SetTitle("L1 Tau Resolution")
 
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.035)
    latex.SetTextAlign(31)
    strRlxMeanA2 = "Rlx L1 A2 Fit Mean: %.2f"%(resMeanA2)
    strRlxMeanA3 = "Rlx L1 A3 Fit Mean: %.2f"%(resMeanA3)
    strRlxMeanA4 = "Rlx L1 A4 Fit Mean: %.2f"%(resMeanA4)
    strRlxMeanA5 = "Rlx L1 A5 Fit Mean: %.2f"%(resMeanA5)
    strL1PtRange = str(l1PtLow)+" < L1Pt < "+str(l1PtHigh)
    strEtaRange = str(etaLow)+" < |#eta| < "+str(etaHigh)
    strCalib = "L1 Calib Factor: " + str(L1_CALIB_FACTOR)
    latex.DrawLatex(0.4,0.8,strRlxMeanA2)
    latex.DrawLatex(0.4,0.77,strRlxMeanA3)
    latex.DrawLatex(0.4,0.74,strRlxMeanA4)
    latex.DrawLatex(0.4,0.71,strRlxMeanA5)

  elif (doTauVetos):

    resTV52,resFitTV52,resMeanTV52= make_plot(
     ntupleTV52,variable,
     cut_L1,
     binning,'L1: TV52 Rlx',legend,ROOT.EColor.kGreen+3,20
    )
    resTV56,resFitTV56,resMeanTV56= make_plot(
     ntupleTV56,variable,
     cut_L1,
     binning,'L1: TV56 Rlx',legend,ROOT.EColor.kGreen+3,20
    )
    resTV60,resFitTV60,resMeanTV60= make_plot(
     ntupleTV60,variable,
     cut_L1,
     binning,'L1: TV60 Rlx',legend,ROOT.EColor.kGreen+3,20
    )
    resTV64,resFitTV64,resMeanTV64= make_plot(
     ntupleTV64,variable,
     cut_L1,
     binning,'L1: TV64 Rlx',legend,ROOT.EColor.kGreen+3,20
    )
    resTV68,resFitTV68,resMeanTV68= make_plot(
     ntupleTV68,variable,
     cut_L1,
     binning,'L1: TV68 Rlx',legend,ROOT.EColor.kGreen+3,20
    )
    resTV52.Draw("ep")
    resTV52.GetXaxis().SetTitle("(recoPt-L1Pt)/recoPt")
    resTV56.Draw("epsames")
    resTV60.Draw("epsames")
    resTV64.Draw("epsames")
    resTV68.Draw("epsames")
    resTV52.GetYaxis().SetRangeUser(0,0.3)
    resTV52.SetTitle("L1 Tau Resolution")
 
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.035)
    latex.SetTextAlign(31)
    strRlxMeanTV52 = "Rlx L1 TV52 Fit Mean: %.2f"%(resMeanTV52)
    strRlxMeanTV56 = "Rlx L1 TV56 Fit Mean: %.2f"%(resMeanTV56)
    strRlxMeanTV60 = "Rlx L1 TV60 Fit Mean: %.2f"%(resMeanTV60)
    strRlxMeanTV64 = "Rlx L1 TV64 Fit Mean: %.2f"%(resMeanTV64)
    strRlxMeanTV68 = "Rlx L1 TV68 Fit Mean: %.2f"%(resMeanTV68)
    strL1PtRange = str(l1PtLow)+" < L1Pt < "+str(l1PtHigh)
    strEtaRange = str(etaLow)+" < |#eta| < "+str(etaHigh)
    strCalib = "L1 Calib Factor: " + str(L1_CALIB_FACTOR)
    latex.DrawLatex(0.4,0.8,strRlxMeanTV52)
    latex.DrawLatex(0.4,0.77,strRlxMeanTV56)
    latex.DrawLatex(0.4,0.74,strRlxMeanTV60)
    latex.DrawLatex(0.4,0.71,strRlxMeanTV64)
    latex.DrawLatex(0.4,0.68,strRlxMeanTV68)
  elif (doIsos):
    resIso1,resFitIso1,resMeanIso1= make_plot(
     ntupleIso1,variable,
     cut_L1,
     binning,'L1: Iso1 Rlx',legend,ROOT.EColor.kGreen+3,20
    )
    resIso15,resFitIso15,resMeanIso15= make_plot(
     ntupleIso15,variable,
     cut_L1,
     binning,'L1: Iso15 Rlx',legend,ROOT.EColor.kGreen+3,20
    )
    resIso2,resFitIso2,resMeanIso2= make_plot(
     ntupleIso2,variable,
     cut_L1,
     binning,'L1: Iso2 Rlx',legend,ROOT.EColor.kGreen+3,20
    )
    resIso3,resFitIso3,resMeanIso3= make_plot(
     ntupleIso3,variable,
     cut_L1,
     binning,'L1: Iso3 Rlx',legend,ROOT.EColor.kGreen+3,20
    )
    resIso1.Draw("ep")
    resIso1.GetXaxis().SetTitle("(recoPt-L1Pt)/recoPt")
    resIso15.Draw("epsames")
    resIso2.Draw("epsames")
    resIso3.Draw("epsames")
    resIso1.GetYaxis().SetRangeUser(0,0.3)
    resIso1.SetTitle("L1 Tau Resolution")
 
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.035)
    latex.SetTextAlign(31)
    strRlxMeanIso1 = "Rlx L1 Iso1 Fit Mean: %.2f"%(resMeanIso1)
    strRlxMeanIso15 = "Rlx L1 Iso15 Fit Mean: %.2f"%(resMeanIso15)
    strRlxMeanIso2 = "Rlx L1 Iso2 Fit Mean: %.2f"%(resMeanIso2)
    strRlxMeanIso3 = "Rlx L1 Iso3 Fit Mean: %.2f"%(resMeanIso3)
    strL1PtRange = str(l1PtLow)+" < L1Pt < "+str(l1PtHigh)
    strEtaRange = str(etaLow)+" < |#eta| < "+str(etaHigh)
    strCalib = "L1 Calib Factor: " + str(L1_CALIB_FACTOR)
    latex.DrawLatex(0.4,0.8,strRlxMeanIso1)
    latex.DrawLatex(0.4,0.77,strRlxMeanIso15)
    latex.DrawLatex(0.4,0.74,strRlxMeanIso2)
    latex.DrawLatex(0.4,0.71,strRlxMeanIso3)
  #latex.DrawLatex(0.4,0.63,strCalib)
  if (doPreLauraRCTCalib):
    cut20IB = cut_L1 + '&&pt[0] >= 20 &&pt[0] < 24 && abs(eta[0]) <0.9'
    cut20OB = cut_L1 + '&&pt[0] >= 20 &&pt[0] < 24 && abs(eta[0]) <1.4 && abs(eta[0])>=0.9'
    cut20E = cut_L1 + '&&pt[0] >= 20  &&pt[0] < 24  && abs(eta[0]) <2.5 && abs(eta[0])>=1.4'
    cut24IB = cut_L1 + '&&pt[0] >= 24 &&pt[0] < 28 && abs(eta[0]) <0.9'
    cut24OB = cut_L1 + '&&pt[0] >= 24 &&pt[0] < 28 && abs(eta[0]) <1.4 && abs(eta[0])>=0.9'
    cut24E = cut_L1 + '&&pt[0] >= 24  &&pt[0] < 28  && abs(eta[0]) <2.5 && abs(eta[0])>=1.4'
    cut28IB = cut_L1 + '&&pt[0] >= 28 &&pt[0] < 32 && abs(eta[0]) <0.9'
    cut28OB = cut_L1 + '&&pt[0] >= 28 &&pt[0] < 32 && abs(eta[0]) <1.4 && abs(eta[0])>=0.9'
    cut28E = cut_L1 + '&&pt[0] >= 28  &&pt[0] < 32  && abs(eta[0]) <2.5 && abs(eta[0])>=1.4'
    cut32IB = cut_L1 + '&&pt[0] >= 32 &&pt[0] < 36 && abs(eta[0]) <0.9'
    cut32OB = cut_L1 + '&&pt[0] >= 32 &&pt[0] < 36 && abs(eta[0]) <1.4 && abs(eta[0])>=0.9'
    cut32E = cut_L1 + '&&pt[0] >= 32  &&pt[0] < 36  && abs(eta[0]) <2.5 && abs(eta[0])>=1.4'
    cut36IB = cut_L1 + '&&pt[0] >= 36 &&pt[0] < 40 && abs(eta[0]) <0.9'
    cut36OB = cut_L1 + '&&pt[0] >= 36 &&pt[0] < 40 && abs(eta[0]) <1.4 && abs(eta[0])>=0.9'
    cut36E = cut_L1 + '&&pt[0] >= 36  &&pt[0] < 40  && abs(eta[0]) <2.5 && abs(eta[0])>=1.4'
    cut40IB = cut_L1 + '&&pt[0] >= 40 &&pt[0] < 44 && abs(eta[0]) <0.9'
    cut40OB = cut_L1 + '&&pt[0] >= 40 &&pt[0] < 44 && abs(eta[0]) <1.4 && abs(eta[0])>=0.9'
    cut40E = cut_L1 + '&&pt[0] >= 40  &&pt[0] < 44  && abs(eta[0]) <2.5 && abs(eta[0])>=1.4'
    cut44IB = cut_L1 + '&&pt[0] >= 44 &&pt[0] < 48 && abs(eta[0]) <0.9'
    cut44OB = cut_L1 + '&&pt[0] >= 44 &&pt[0] < 48 && abs(eta[0]) <1.4 && abs(eta[0])>=0.9'
    cut44E = cut_L1 + '&&pt[0] >= 44  &&pt[0] < 48  && abs(eta[0]) <2.5 && abs(eta[0])>=1.4'
    cut48IB = cut_L1 + '&&pt[0] >= 48 &&pt[0] < 52 && abs(eta[0]) <0.9'
    cut48OB = cut_L1 + '&&pt[0] >= 48 &&pt[0] < 52 && abs(eta[0]) <1.4 && abs(eta[0])>=0.9'
    cut48E = cut_L1 + '&&pt[0] >= 48  &&pt[0] < 52  && abs(eta[0]) <2.5 && abs(eta[0])>=1.4'
    cut52IB = cut_L1 + '&&pt[0] >= 52 &&pt[0] < 56 && abs(eta[0]) <0.9'
    cut52OB = cut_L1 + '&&pt[0] >= 52 &&pt[0] < 56 && abs(eta[0]) <1.4 && abs(eta[0])>=0.9'
    cut52E = cut_L1 + '&&pt[0] >= 52  &&pt[0] < 56  && abs(eta[0]) <2.5 && abs(eta[0])>=1.4'
    res_20IB,resFit,resMean = make_plot(ntuple,variable,cut20IB,binning,'Rlx',legend,ROOT.EColor.kGreen+3,20,1.404)
    res_20OB,resFit,resMean = make_plot(ntuple,variable,cut20OB,binning,'Rlx',legend,ROOT.EColor.kGreen+3,20,1.361)
    res_20E,resFit,resMean = make_plot(ntuple,variable,cut20E,binning,'Rlx',legend,ROOT.EColor.kGreen+3,20,1.304)
    res_24IB,resFit,resMean = make_plot(ntuple,variable,cut24IB,binning,'Rlx',legend,ROOT.EColor.kGreen+3,20,1.314)
    res_24OB,resFit,resMean = make_plot(ntuple,variable,cut24OB,binning,'Rlx',legend,ROOT.EColor.kGreen+3,20,1.267)
    res_24E,resFit,resMean = make_plot(ntuple,variable,cut24E,binning,'Rlx',legend,ROOT.EColor.kGreen+3,20,1.231)
    res_28IB,resFit,resMean = make_plot(ntuple,variable,cut28IB,binning,'Rlx',legend,ROOT.EColor.kGreen+3,20,1.255)
    res_28OB,resFit,resMean = make_plot(ntuple,variable,cut28OB,binning,'Rlx',legend,ROOT.EColor.kGreen+3,20,1.208)
    res_28E,resFit,resMean = make_plot(ntuple,variable,cut28E,binning,'Rlx',legend,ROOT.EColor.kGreen+3,20,1.185)
    res_32IB,resFit,resMean = make_plot(ntuple,variable,cut32IB,binning,'Rlx',legend,ROOT.EColor.kGreen+3,20,1.204)
    res_32OB,resFit,resMean = make_plot(ntuple,variable,cut32OB,binning,'Rlx',legend,ROOT.EColor.kGreen+3,20,1.153)
    res_32E,resFit,resMean = make_plot(ntuple,variable,cut32E,binning,'Rlx',legend,ROOT.EColor.kGreen+3,20,1.131)
    res_36IB,resFit,resMean = make_plot(ntuple,variable,cut36IB,binning,'Rlx',legend,ROOT.EColor.kGreen+3,20,1.163)
    res_36OB,resFit,resMean = make_plot(ntuple,variable,cut36OB,binning,'Rlx',legend,ROOT.EColor.kGreen+3,20,1.122)
    res_36E,resFit,resMean = make_plot(ntuple,variable,cut36E,binning,'Rlx',legend,ROOT.EColor.kGreen+3,20,1.090)
    res_40IB,resFit,resMean = make_plot(ntuple,variable,cut40IB,binning,'Rlx',legend,ROOT.EColor.kGreen+3,20,1.132)
    res_40OB,resFit,resMean = make_plot(ntuple,variable,cut40OB,binning,'Rlx',legend,ROOT.EColor.kGreen+3,20,1.091)
    res_40E,resFit,resMean = make_plot(ntuple,variable,cut40E,binning,'Rlx',legend,ROOT.EColor.kGreen+3,20,1.070)
    res_44IB,resFit,resMean = make_plot(ntuple,variable,cut44IB,binning,'Rlx',legend,ROOT.EColor.kGreen+3,20,1.101)
    res_44OB,resFit,resMean = make_plot(ntuple,variable,cut44OB,binning,'Rlx',legend,ROOT.EColor.kGreen+3,20,1.050)
    res_44E,resFit,resMean = make_plot(ntuple,variable,cut44E,binning,'Rlx',legend,ROOT.EColor.kGreen+3,20,1.040)
    res_48IB,resFit,resMean = make_plot(ntuple,variable,cut48IB,binning,'Rlx',legend,ROOT.EColor.kGreen+3,20,1.081)
    res_48OB,resFit,resMean = make_plot(ntuple,variable,cut48OB,binning,'Rlx',legend,ROOT.EColor.kGreen+3,20,1.020)
    res_48E,resFit,resMean = make_plot(ntuple,variable,cut48E,binning,'Rlx',legend,ROOT.EColor.kGreen+3,20,1.020)
    res_52IB,resFit,resMean = make_plot(ntuple,variable,cut52IB,binning,'Rlx',legend,ROOT.EColor.kGreen+3,20,1.050)
    res_52OB,resFit,resMean = make_plot(ntuple,variable,cut52OB,binning,'Rlx',legend,ROOT.EColor.kGreen+3,20,1.000)
    res_52E,resFit,resMean = make_plot(ntuple,variable,cut52E,binning,'Rlx',legend,ROOT.EColor.kGreen+3,20,1.010)
    res = res_20IB.Clone()
    #res.Add(res_20OB,1)
    #res.Add(res_20E,1)
    #res.Add(res_24IB,1)
    #res.Add(res_24OB,1)
    #res.Add(res_24E,1)
    #res.Add(res_28IB,1)
    #res.Add(res_28OB,1)
    #res.Add(res_28E,1)
    #res.Add(res_32IB,1)
    #res.Add(res_32OB,1)
    #res.Add(res_32E,1)
    #res.Add(res_36IB,1)
    #res.Add(res_36OB,1)
    #res.Add(res_36E,1)
    #res.Add(res_40IB,1)
    #res.Add(res_40OB,1)
    #res.Add(res_40E,1)
    #res.Add(res_44IB,1)
    #res.Add(res_44OB,1)
    #res.Add(res_44E,1)
    #res.Add(res_48IB,1)
    #res.Add(res_48OB,1)
    #res.Add(res_48E,1)
    #res.Add(res_52IB,1)
    #res.Add(res_52OB,1)
    #res.Add(res_52E,1)
    #res.Draw("ep")
    res.GetXaxis().SetTitle("(recoPt-L1Pt)/recoPt")
    #res_iso.Draw("epsames")
    #res_mc.Draw("epsames")
    #res_mc_iso.Draw("epsames")
    res.GetYaxis().SetRangeUser(0,0.3)
    res.SetTitle("L1 Tau Resolution (Pre RCT Calib)")
    res.Sumw2()
    res.Scale(1/res.Integral())
    res.Draw("ep")
 
 
    resGauss = res.Clone()
    resFit = ROOT.TF1("asdf","gaus",-0.4,0.4)
    resGauss.Fit(resFit,"R")
    resGauss.SetLineColor(ROOT.EColor.kGreen+3)

    #resFit.Draw("lsames")
    resFitMean = resFit.GetParameter(1)
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.035)
    latex.SetTextAlign(31)
    strRlxMean = "Rlx Fit Mean: %.2f"%(resFitMean)
    #strIsoMCMean = "Iso MC Fit Mean: %.2f"%(res_mc_isoMean)
    strL1PtRange = str(l1PtLow)+" < L1Pt < "+str(l1PtHigh)
    strEtaRange = str(etaLow)+" < |#eta| < "+str(etaHigh)
    strCalib = "L1 Calib Factor: " + str(L1_CALIB_FACTOR)
    latex.DrawLatex(0.45,0.8,strRlxMean)
    #latex.DrawLatex(0.45,0.77,strIsoMean)
    #latex.DrawLatex(0.45,0.74,strRlxMCMean)
    #latex.DrawLatex(0.45,0.71,strIsoMCMean)
    #legend.Draw("sames")


  else: 
    res,resFit,resMean= make_plot(
     ntuple,variable,
     cut_L1,
     binning,'Rlx',legend,ROOT.EColor.kGreen+3,20
    )
    res_iso,res_isoFit,res_isoMean= make_plot(
     ntuple_iso,variable,
     cut_L1,
     binning,'Iso',legend,ROOT.EColor.kBlue,20
    )
    #res_mc,res_mcFit,res_mcMean= make_plot(
    # ntuple_mc,variableNoCalib,
    # cut_L1,
    # binning,'MC: Rlx',legend,ROOT.EColor.kGreen+3,24
    #)
    #res_mc_iso,res_mc_isoFit,res_mc_isoMean= make_plot(
    # ntuple_mc_iso,variableNoCalib,
    # cut_L1,
    # binning,'MC: Iso',legend,ROOT.EColor.kBlue,24
    #)
    print "resMean: " + str(resMean)
    #frame.SetMaximum(0.3)
 
    #frame.GetXaxis().SetTitle("(recoPt-L1Pt)/recoPt")
    

    res.Draw("ep")
    res.GetXaxis().SetTitle("(recoPt-L1Pt)/recoPt")
    res_iso.Draw("epsames")
    #res_mc.Draw("epsames")
    #res_mc_iso.Draw("epsames")
    res.GetYaxis().SetRangeUser(0,0.3)
    res.SetTitle("L1 Tau Resolution")
    print ntuple
 
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.035)
    latex.SetTextAlign(31)
    strRlxMean = "Rlx Fit Mean: %.2f"%(resMean)
    strIsoMean = "Iso Fit Mean: %.2f"%(res_isoMean)
    #strRlxMCMean = "Rlx MC Fit Mean: %.2f"%(res_mcMean)
    #strIsoMCMean = "Iso MC Fit Mean: %.2f"%(res_mc_isoMean)
    strL1PtRange = str(l1PtLow)+" < L1Pt < "+str(l1PtHigh)
    strEtaRange = str(etaLow)+" < |#eta| < "+str(etaHigh)
    strCalib = "L1 Calib Factor: " + str(L1_CALIB_FACTOR)
    latex.DrawLatex(0.45,0.8,strRlxMean)
    latex.DrawLatex(0.45,0.77,strIsoMean)
    #latex.DrawLatex(0.45,0.74,strRlxMCMean)
    #latex.DrawLatex(0.45,0.71,strIsoMCMean)
    legend.Draw("sames")
  
  latex.DrawLatex(0.45,0.68,strL1PtRange)
  latex.DrawLatex(0.45,0.65,strEtaRange)
  
  print saveWhere+saveStr
  canvas.SaveAs(saveWhere+saveStr+'.png')
  return resMean, res_isoMean
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
binRes = [25,-1,1]

resVarCalib = '(pt[0]-' + str(L1_CALIB_FACTOR)+'*L1Matchedpt[0])/pt[0]'
resVarNoCalib = '(pt[0]-L1Matchedpt[0])/pt[0]'
resRecoPtCut = '(pt[0] >= '+str(recoPtVal)+')'
resL1PtCut = '(L1Matchedpt[0] >= '+str(l1PtLow)+'&&L1Matchedpt[0]< '+str(l1PtHigh)+')'
extraCutStr = '&&eta[0]>'+str(-2.5)+'&&eta[0]<'+str(2.5)+'&&abs(L1Matchedeta[0])>='+str(etaLow)+'&&abs(L1Matchedeta[0])<'+str(etaHigh)
#extraCutStr = '&&eta[0]>'+str(-2.5)+'&&eta[0]<'+str(2.5)+'&&L1Matchedeta[0]>'+str(etaLow)+'&&L1Matchedeta[0]<'+str(etaHigh)
res_Mean=2.0
res_MeanIso=2.0
#print str(abs(res_Mean-1.0))
if (not doTauCalib):
  res_Mean=compare_resolution(
    resVarCalib,
    resVarNoCalib,
    binRes,
    res_ntuple,
    res_iso_ntuple,
    res_mc_ntuple,
    res_mc_iso_ntuple,
    resA2_ntuple,
    resA3_ntuple,
    resA4_ntuple,
    resA5_ntuple,
    resTV52_ntuple,
    resTV56_ntuple,
    resTV60_ntuple,
    resTV64_ntuple,
    resTV68_ntuple,
    resIso1_ntuple,
    resIso12_ntuple,
    resIso13_ntuple,
    resIso15_ntuple,
    resIso2_ntuple,
    resRecoPtCut,
    resL1PtCut,
    l1PtCutOld='(L1Matchedpt[0] >= 40)&&(L1Matchedpt[1]>= 40)',
    extraCut=extraCutStr,
  )
else:
  f = open('TauLutNoRCTCalib.txt','a')
  while (abs(res_Mean)>0.015):
    print "making plot"
    res_Mean,res_MeanIso=compare_resolution(
      resVarCalib,
      resVarNoCalib,
      binRes,
      res_ntuple,
      res_iso_ntuple,
      res_mc_ntuple,
      res_mc_iso_ntuple,
      resA2_ntuple,
      resA3_ntuple,
      resA4_ntuple,
      resA5_ntuple,
      resTV52_ntuple,
      resTV56_ntuple,
      resTV60_ntuple,
      resTV64_ntuple,
      resTV68_ntuple,
      resIso1_ntuple,
      resIso12_ntuple,
      resIso13_ntuple,
      resIso15_ntuple,
      resIso2_ntuple,
      resRecoPtCut,
      resL1PtCut,
      l1PtCutOld='(L1Matchedpt[0] >= 40)&&(L1Matchedpt[1]>= 40)',
      extraCut=extraCutStr,
    )
    L1_CALIB_FACTOR = L1_CALIB_FACTOR*(1+res_Mean)*(1+(0.02*(random.random()-0.5)))
    print "resMean: " + str(res_Mean)
    print "new calib factor: " + str(L1_CALIB_FACTOR)
    resVarCalib = '(pt[0]-' + str(L1_CALIB_FACTOR)+'*L1Matchedpt[0])/pt[0]'
    saveWhere = saveDir+'Plots_Res/Res_'+saveStr+'eta_'+etaLow+'_'+etaHigh+'_l1pt_'+l1PtLow+'_'+l1PtHigh+'_CalibFactor_'+str(L1_CALIB_FACTOR)
    ScaleStr = str(L1_CALIB_FACTOR)+","
  f.write(ScaleStr)
  f.close()

