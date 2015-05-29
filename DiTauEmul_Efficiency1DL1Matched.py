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
doOldCmp=False
l1PtVal=float(argv[1])
eff_ntuple_str=argv[2]
saveStr=argv[3]
do2BiniEtaCut=False
Longxaxis=False
if (do2BiniEtaCut):
        saveStr = saveStr+'_tightEtaCut'
if (Longxaxis):
	saveStr = saveStr+'_400GeV'
drawLine=True
#ISOTHRESHOLD=0.15a
ISOTHRESHOLD = 0.1
ISOTHRESHOLD4x4=0.25
turnOffIso = 192
L1_CALIB_FACTOR = 1.0
L1G_CALIB_FACTOR = 1.0
ZEROBIAS_RATE=11246.0*2590.0 #frequency X bunches
#saveWhere = 'EmulatorTestingNov/DiTau1DEffiLauraNewCalibThreshPoint15Iso'
#saveWhere = 'March25LutTests/Plots/OldCalibOldLutPoint1Iso_'
#saveDir = 'March25LutTests/Plots/'
saveDir = 'RCTV2CalibNtuples_FullStatsApril28/Plots/'
#saveDir = 'RCTV2CalibNtuples_LUTFileTest/Plots/'
saveWhere = saveDir+saveStr

name = 'l1Pt'+str(l1PtVal)

########
# File #
########
#Efficiency
#eff_ntuple = 'EactHactTaus_June13/ECAL3/tau_eff_4x8_E3H3_NoNeighborSeed.root'
#eff_ntuple = 'uct_efficiency_tree_numEvent5000.root'
#eff_ntuple_str = "EmulatorTestingNov/emulatorEffNtupleDRFixNov22.root"
#eff_iso_ntuple_str = "EmulatorTestingNov/emulatorEffisIso.root"
#eff_ntuple_str = "EmulatorTestingNov/tau_emul_effDoublingNoFixRlxDec6.root"
#eff_iso_ntuple_str = "EmulatorTestingNov/tau_emul_effDoublingNoFixIsoDec6.root"
#eff_ntuple_str = "tau_emul_effFeb17RlxNoTauVetoNewCalib.root"
#effOld_ntuple_str ="March25LutTests/tau_emul_effMarch27OldCalibOldLUTIsoPoint1.root"
#effOld_ntuple_str ="March25LutTests/tau_emul_effMarch30NewCalibNewLUTIsoPoint15.root"
effOld_ntuple_str = "RCTV2CalibNtuples_LUTFileTest/tau_emul_effRCTV2CalibDefaultIso15LUTFileTest.root"
eff_rlx_veto_ntuple_str = "tau_emul_effFeb17RlxTauVetoNewCalib.root"
#eff_iso_ntuple_str = "tau_emul_effFeb17IsoTauVetoNewCalib.root"
eff_iso_ntuple_str = "tau_emul_effMarch10IsoTauVetoNewCalibPoint15.root"
#eff_ntuple_str = "tau_emul_effJan28RlxNoTauVetoThreshFix.root"
#eff_rlx_veto_ntuple_str = "tau_emul_effJan28RlxTauVetoThreshFix.root"
#eff_iso_ntuple_str="tau_emul_effJan28IsoTauVetoThreshFix0Point1Iso.root"
eff_ntuple_NoDoubling_str = "EmulatorTestingNov/tau_emul_effDoublingFixRecoSlightFixRlxDec6.root"
eff_iso_ntuple_NoDoubling_str = "EmulatorTestingNov/tau_emul_effDoublingFixRecoSlightFixIsoDec6.root"

eff_ntuple_file = ROOT.TFile(eff_ntuple_str)
effOld_ntuple_file = ROOT.TFile(effOld_ntuple_str)
eff_iso_ntuple_file = ROOT.TFile(eff_iso_ntuple_str)
eff_rlx_veto_ntuple_file = ROOT.TFile(eff_rlx_veto_ntuple_str)
eff_ntuple_NoDoubling_file = ROOT.TFile(eff_ntuple_NoDoubling_str)
eff_iso_ntuple_NoDoubling_file = ROOT.TFile(eff_iso_ntuple_NoDoubling_str)
#
eff_spot = 'TauEmulEffi/Ntuple'
eff_iso_spot = 'TauEmulEffiIso/Ntuple'
eff_ntuple = eff_ntuple_file.Get(eff_spot)
effOld_ntuple = effOld_ntuple_file.Get(eff_spot)
effOld_iso_ntuple =effOld_ntuple_file.Get(eff_iso_spot)
#eff_iso_ntuple = eff_iso_ntuple_file.Get(eff_spot)
eff_iso_ntuple = eff_ntuple_file.Get(eff_iso_spot)
eff_rlx_veto_ntuple = eff_rlx_veto_ntuple_file.Get(eff_spot)
eff_ntuple_NoDoubling = eff_ntuple_NoDoubling_file.Get(eff_spot)
eff_iso_ntuple_NoDoubling = eff_iso_ntuple_NoDoubling_file.Get(eff_spot)
store = ROOT.TFile(saveWhere+'.root','RECREATE')


#########
# STYLE #
#########

ROOT.gROOT.LoadMacro("tdrstyle.C")
ROOT.setTDRStyle()
ROOT.gROOT.SetStyle("Plain")
#ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

tex = ROOT.TLatex()
tex.SetTextSize(0.07)
tex.SetTextAlign(11)
tex.SetNDC(True)

colorUR=ROOT.EColor.kGreen+3
markerUR=21
#markerUR=21
colorUI=ROOT.EColor.kBlue
markerUI=20
colorUIbh=ROOT.EColor.kBlack
#colorUIbh=ROOT.EColor.kGreen+3
#colorUIbh=ROOT.EColor.kBlue
colorUIbh=ROOT.EColor.kRed
#colorUIbh=ROOT.EColor.kViolet-7
markerUIbh=25
#markerUIbh=22
colorCR=ROOT.EColor.kViolet-7
markerCR=20
colorCI=ROOT.EColor.kRed
markerCI=24
variable = "pt[1]"
canvas = ROOT.TCanvas("asdf", "adsf", 800, 800)
canvas.SetGrid()

def make_plot(tree, variable, selection, binning, xaxis='', title='',calFactor=1):
 ''' Plot a variable using draw and return the histogram '''
 #draw_string = "%s * %0.2f>>htemp(%s)" % (variable,calFactor, ", ".join(str(x) for x in binning))
 draw_string = variable +" * %0.2f>>htemp(%s)" % (calFactor, ", ".join(str(x) for x in binning))
 print "draw_string "+ draw_string
 print selection
 #selectionMin0 = selection+"&&pt[1]>pt[0]"
 #tree.Draw(draw_string, selectionMin0, "goff")
 tree.Draw(draw_string, selection, "goff")
 #output_histoMin0 = ROOT.gDirectory.Get("htemp").Clone()
 output_histo = ROOT.gDirectory.Get("htemp").Clone()
 #draw_string = "pt[1] * %0.2f>>htemp2(%s)" % (calFactor, ", ".join(str(x) for x in binning))
 print "draw_string "+ draw_string
 print selection
 #selectionMin1 = selection+"&&pt[0]>pt[1]"
 #tree.Draw(draw_string, selectionMin1, "goff")
 #output_histoMin1 = ROOT.gDirectory.Get("htemp2").Clone()
 #output_histo = output_histoMin0.Clone()
 #output_histo.Add(output_histoMin1)
 if (variable == "pt[1]"):
 	output_histo.GetXaxis().SetTitle("Min(P_{T}1, P_{T}2)")
 ROOT.gDirectory.Clear()
 output_histo.Rebin(10,"output_histoRebinned",xBins)
 output_histoRebinned = ROOT.gDirectory.Get("output_histoRebinned").Clone()

 output_histoRebinned.SetTitle(title)
 print output_histo.GetBinContent(8)
 for i in range(1,13):
 	print "printing" + str(i)
 	print output_histoRebinned.GetBinContent(i)
 return output_histoRebinned


######################################################################
##### EFFICIENCY #####################################################
######################################################################
def make_l1_efficiency(denom, num,color=ROOT.EColor.kBlue,marker=20):
 ''' Make an efficiency graph '''
 num.Sumw2()
 denom.Sumw2()
 eff = ROOT.TGraphAsymmErrors(num, denom)
 eff.SetMarkerStyle(marker)
 eff.SetMarkerColor(color)
 eff.SetMarkerSize(1.5)
 eff.SetLineColor(color)
 return eff

def make_2D_l1_efficiency(denom,num):
 eff = num.Clone()
 eff.Divide(denom)
 return eff

def effi_histo(ntuple,variable,cut,binning,denom,title,leg,color,marker):
 num = make_plot(ntuple,variable,cut,binning)
 print "num entries" + str(num.GetEntries())
 print "denom entries" + str(denom.GetEntries())
 efiHist = num.Clone()
 efiHist.Divide(denom)
 efi = make_l1_efficiency(denom,num,color,marker)
 #efi = make_2D_l1_efficiency(denom,num)
 leg.AddEntry(efi,title,'pe')
 #efi.Draw('colz')
 efi.Draw('pe')
 efi.GetXaxis().SetTitle("Min(reco pT Tau1, reco pT Tau2)")
 #efi.GetYaxis().SetTitle("Leading Tau")

 tex = ROOT.TLatex()
 tex.SetNDC(True)
 tex.SetTextSize(0.04)
 tex.SetTextAlign(31)
 for i in range (1,efiHist.GetNbinsX()):
	print efiHist.GetBinContent(i)
 return efi

def compare_efficiencies(
 variable,
 binning,
 ntuple=None,
 ntuple_iso=None,
 ntupleOld=None,
 ntupleOld_iso=None,
 ntuple_rlx_veto=None,
 ntuple_NoDoubling=None,
 ntuple_NoDoublingIso=None,
 recoPtCut='(1)',l1PtCut='(1)',l1PtCutOld='(1)',
 extraCut = '&&(1)',
 setLOG=False
):
 '''
Returns a (L1, L1G) tuple of TGraphAsymmErrors
'''
 print ntuple.GetEntries()
 cutD_rlx = recoPtCut+extraCut
 print "cutD_rlx"+cutD_rlx
 denom_rlx = make_plot(
  ntuple,variable,
  cutD_rlx,
  binning
 )
 
 denomOld_rlx = make_plot(
  ntupleOld,variable,
  cutD_rlx,
  binning
 )

 #denom_NoDoubling_rlx = make_plot(ntuple_NoDoubling, variable, cutD_rlx, binning)
 if (Longxaxis):
 	frame = ROOT.TH1F('frame','frame',10,0,400)
 else:
 	frame = ROOT.TH1F('frame','frame',10,0,100)
 canvas.SetLogy(setLOG)
 frame.Draw("")
 frame.SetTitle('')
 frame.GetYaxis().SetTitle('Efficiency')
 frame.SetMaximum(1.1)
 frame.GetYaxis().SetTitle("Efficiency")
 tex.DrawLatex(0.1,0.91,'DiTau Efficiency')
 tex.SetTextSize(0.03)
 tex.SetTextAlign(31)
 tex.DrawLatex(0.9,0.91,'CMS Preliminary')
 tex.SetTextSize(0.07)
 tex.SetTextAlign(11)

 if variable is 'nPVs': frame.GetXaxis().SetTitle('Nr. Primary Vertices')
 elif variable is 'pt[0]:pt[1]':
	frame.GetXaxis().SetTitle('pt[1]')
	frame.GetYaxis().SetTitle('pt[0]')
 elif variable is 'Min(pt[1],pt[0])': frame.GetXaxis().SetTitle("Min(P_{T}1, P_{T}2)")
 else: frame.GetXaxis().SetTitle(variable)
 if Longxaxis==True:
 	frame.GetXaxis().SetRangeUser(0,400)
 else:
	frame.GetXaxis().SetRangeUser(0,100)
 #tex.DrawLatex(0.1,0.91,'Tau '+variable+' Efficiency')
 #tex.SetTextSize(0.03)
 #tex.DrawLatex(0.1,0.87,'CMS Preliminary')
 #tex.SetTextSize(0.07)
 legend = ROOT.TLegend(0.63,0.15,0.95,0.45,'','brNDC')
 legend.SetTextSize(0.033)
 legend.SetFillColor(0)
 legend.SetBorderSize(0)
 
 info ='_'+variable
 if variable=='nPVs': info+=str(recoPtVal)
 
# Current Relaxed
 cut_L1_rlx=cutD_rlx+'&&'+l1PtCut+'&& L1matches[0]>-1&&L1matches[1]>-1'
 cut_L1_rlxOld=cutD_rlx+'&&'+l1PtCutOld+'&& L1matches[0]>-1&&L1matches[1]>-1'
 _L1_rlx=effi_histo(ntuple,variable,cut_L1_rlx,binning,denom_rlx,
 'L1: Rlx',legend, ROOT.EColor.kGreen+3,20)
 print "l1 rlx done"
 #_L1_rlx_veto=effi_histo(ntuple_rlx_veto,variable,cut_L1_rlx,binning,denom_rlx,
 #'L1: Rlx (Tau Veto)',legend, ROOT.EColor.kRed,20)
 _L1_iso=effi_histo(ntuple_iso,variable,cut_L1_rlx,binning,denom_rlx,
 'L1: Iso',legend, ROOT.EColor.kBlue,20)
 if doOldCmp:
 	_L1_rlx_Old=effi_histo(ntupleOld,variable,cut_L1_rlxOld,binning,denomOld_rlx,
 '	L1: Rlx, 7 GeV Seed',legend, ROOT.EColor.kGreen+3,25)
 	_L1_iso_Old=effi_histo(ntupleOld_iso,variable,cut_L1_rlxOld,binning,denomOld_rlx,
 	'L1: Rlx, 7 GeV Seed',legend, ROOT.EColor.kBlue+2,25)
 L1RlxCurve=_L1_rlx.Clone()
 L1IsoCurve=_L1_iso.Clone()
 
 formula = '[0]+[1]*x'
 Poly1=ROOT.TFormula("adf",formula)
 
 L1RlxFit = ROOT.TF1("adsf","tanh([0]*x+[1])+[2]",20,100)
 L1IsoFit = ROOT.TF1("asdf","tanh([0]*x+[1])+[2]",20,100)

 L1RlxCurve.Fit(L1RlxFit,"R")
 L1IsoCurve.Fit(L1IsoFit,"R")

 L1RlxFit.SetLineColor(ROOT.EColor.kGreen+3)
 L1IsoFit.SetLineColor(ROOT.EColor.kBlue)
 
 L1RlxFit.Draw("lsames")
 L1IsoFit.Draw("lsames")
 
 print "l1 iso done"
 #_L1_rlx_NoDoubling=effi_histo(ntuple_NoDoubling,variable,cut_L1_rlx,binning,denom_NoDoubling_rlx,
 #'L1: Rlx No Doubling',legend, ROOT.EColor.kMagenta+3,25)
 #print "l1 iso nodoubling done"
 #_L1_iso_NoDoubling=effi_histo(ntuple_NoDoublingIso,variable,cut_L1_rlx,binning,denom_NoDoubling_rlx,
 #'L1: Iso No Doubling',legend, ROOT.EColor.kBlue-1,25)
 #print "l1 rlx nodoubling done"

 legend.Draw()

 if drawLine == True:
   vert = ROOT.TLine(l1PtVal,0,l1PtVal,1.1)
   vert.SetLineWidth(3)
   vert.SetLineStyle(3)
   vert.Draw()
 
 #save=raw_input("Type save to save as "+saveWhere+name+info+".png (enter to continue):\n")
 #if save=="save": 
 canvas.SaveAs(saveWhere+name+info+'.png')
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
#xBins = array.array('d',[20,25,30,35,40,45,50,55,60,80,100,130,200])
if Longxaxis:
	xBins = array.array('d',[20,25,30,35,40,45,50,55,60,80,120,200,300,400])
else:
	xBins = array.array('d',[20,25,30,35,40,45,50,55,60,80,100])
binPt = [20,0,100]
binVert=[10,0,35]
binJetPt=[40,0,70]
binEta = [40,-3,3]
bin2DPt = [10,0,100,10,0,100]

# variable,
# binning,
# ntuple_rlx=None,
# ntuple_iso=None,
# recoPtCut='(1)',l1PtCut='(1)',l1gPtCut='(1)',
# isoCut='(1)',extraCut='(1)',
# drawUCTIso_=False,
# drawUCTRlx_=False,
# drawUCTIso_byhand_=False,
# drawL1Iso_=False,
# drawL1Rlx_=False
# legExtra='',
# setLOG=False
if (do2BiniEtaCut):
	extraCutStr='&&eta[0]>-1.9&&eta[0]<1.9&&eta[1]>-1.9&&eta[1]<1.9&&L1Matchedeta[1]<1.9 &&L1Matchedeta[0]>-1.9&&L1Matchedeta[0]<1.9&&L1Matchedeta[1]>-1.9&&L1Matchedeta[1]<1.9'
else:
	extraCutStr='&&eta[0]>-2.5&&eta[0]<2.5&&eta[1]>-2.5&&eta[1]<2.5&&L1Matchedeta[1]<2.5 &&L1Matchedeta[0]>-2.5&&L1Matchedeta[0]<2.5&&L1Matchedeta[1]>-2.5&&L1Matchedeta[1]<2.5'

compare_efficiencies(
 "pt[1]",
 binPt,
 eff_ntuple,
 eff_iso_ntuple,
 effOld_ntuple,
 effOld_iso_ntuple,
 eff_rlx_veto_ntuple,
 eff_ntuple_NoDoubling,
 eff_iso_ntuple_NoDoubling,
 recoPtCut = '(pt[0] >= '+str(recoPtVal)+')&&(pt[1] >= '+str(recoPtVal)+')',
 #recoPtCut='1',
 l1PtCut='(L1Matchedpt[0] >= '+str(l1PtVal)+')&&(L1Matchedpt[1]>= '+str(l1PtVal)+')',
 l1PtCutOld='(L1Matchedpt[0] >= 40)&&(L1Matchedpt[1]>= 40)',
 #l1PtCut='((L1Matchedpt[0] >='+ str(32/1.185)+'&&abs(L1Matchedeta[0])<0.9)||(L1Matchedpt[0] >='+ str(32/1.153)+'&&abs(L1Matchedeta[0])<1.4&&abs(L1Matchedeta[0])>=0.9)||(L1Matchedpt[0] >='+ str(32/1.081)+'&&abs(L1Matchedeta[0])<2.5&&abs(L1Matchedeta[0])>=1.4))&&((L1Matchedpt[1] >='+ str(32/1.185)+'&&abs(L1Matchedeta[1])<0.9)||(L1Matchedpt[1] >='+ str(36/1.153)+'&&abs(L1Matchedeta[1])<1.4&&abs(L1Matchedeta[1])>=0.9)||(L1Matchedpt[1] >='+ str(32/1.081)+'&&abs(L1Matchedeta[1])<2.5&&abs(L1Matchedeta[1])>=1.4))',
 #l1PtCut='((L1Matchedpt[0] >='+ str(36/1.131)+'&&abs(L1Matchedeta[0])<0.9)||(L1Matchedpt[0] >='+ str(36/1.061)+'&&abs(L1Matchedeta[0])<1.4&&abs(L1Matchedeta[0])>=0.9)||(L1Matchedpt[0] >='+ str(36/1.050)+'&&abs(L1Matchedeta[0])<2.5&&abs(L1Matchedeta[0])>=1.4))&&((L1Matchedpt[1] >='+ str(36/1.131)+'&&abs(L1Matchedeta[1])<0.9)||(L1Matchedpt[1] >='+ str(36/1.061)+'&&abs(L1Matchedeta[1])<1.4&&abs(L1Matchedeta[1])>=0.9)||(L1Matchedpt[1] >='+ str(36/1.050)+'&&abs(L1Matchedeta[1])<2.5&&abs(L1Matchedeta[1])>=1.4))',
 extraCut=extraCutStr,
 #extraCut='&&eta[0]>-2.5&&eta[0]<2.5&&eta[1]>-2.5&&eta[1]<2.5&&L1eta[1]<2.5 &&L1eta[0]>-2.5&&L1eta[0]<2.5&&L1eta[1]>-2.5&&L1eta[1]<2.5',
)

