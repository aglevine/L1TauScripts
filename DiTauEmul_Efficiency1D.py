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
l1PtVal=float(argv[1])
drawLine=True
#ISOTHRESHOLD=0.15a
ISOTHRESHOLD = 0.1
ISOTHRESHOLD4x4=0.25
turnOffIso = 192
L1_CALIB_FACTOR = 1.0
L1G_CALIB_FACTOR = 1.0
ZEROBIAS_RATE=11246.0*2590.0 #frequency X bunches
saveWhere = 'EmulatorTestingNov/DiTau1DEffiLauraThresh'
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
eff_ntuple_str = "tau_emul_rateFeb17RlxNoTauVetoNewCalib.root"
eff_rlx_veto_ntuple_str = "tau_emul_rateFeb17RlxTauVetoNewCalib.root"
eff_iso_ntuple_str = "tau_emul_rateFeb17IsoTauVetoNewCalib.root"
#eff_ntuple_str = "tau_emul_effJan28RlxNoTauVetoThreshFix.root"
#eff_rlx_veto_ntuple_str = "tau_emul_effJan28RlxTauVetoThreshFix.root"
#eff_iso_ntuple_str="tau_emul_effJan28IsoTauVetoThreshFix0Point1Iso.root"
eff_ntuple_NoDoubling_str = "EmulatorTestingNov/tau_emul_effDoublingFixRecoSlightFixRlxDec6.root"
eff_iso_ntuple_NoDoubling_str = "EmulatorTestingNov/tau_emul_effDoublingFixRecoSlightFixIsoDec6.root"

eff_ntuple_file = ROOT.TFile(eff_ntuple_str)
eff_iso_ntuple_file = ROOT.TFile(eff_iso_ntuple_str)
eff_rlx_veto_ntuple_file = ROOT.TFile(eff_rlx_veto_ntuple_str)
eff_ntuple_NoDoubling_file = ROOT.TFile(eff_ntuple_NoDoubling_str)
eff_iso_ntuple_NoDoubling_file = ROOT.TFile(eff_iso_ntuple_NoDoubling_str)
#
eff_spot = 'TauEmulEffi/Ntuple'
eff_ntuple = eff_ntuple_file.Get(eff_spot)
eff_iso_ntuple = eff_iso_ntuple_file.Get(eff_spot)
eff_rlx_veto_ntuple = eff_rlx_veto_ntuple_file.Get(eff_spot)
eff_ntuple_NoDoubling = eff_ntuple_NoDoubling_file.Get(eff_spot)
eff_iso_ntuple_NoDoubling = eff_iso_ntuple_NoDoubling_file.Get(eff_spot)
store = ROOT.TFile(saveWhere+'.root','RECREATE')


#########
# STYLE #
#########
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
 ntuple_rlx_veto=None,
 ntuple_NoDoubling=None,
 ntuple_NoDoublingIso=None,
 recoPtCut='(1)',l1PtCut='(1)',
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

 denom_NoDoubling_rlx = make_plot(ntuple_NoDoubling, variable, cutD_rlx, binning)
 
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
 frame.GetXaxis().SetRangeUser(0,100)
 #tex.DrawLatex(0.1,0.91,'Tau '+variable+' Efficiency')
 #tex.SetTextSize(0.03)
 #tex.DrawLatex(0.1,0.87,'CMS Preliminary')
 #tex.SetTextSize(0.07)
 legend = ROOT.TLegend(0.63,0.15,0.95,0.45,'','brNDC')
 legend.SetTextSize(0.023)
 legend.SetFillColor(0)
 legend.SetBorderSize(0)
 
 info ='_'+variable
 if variable=='nPVs': info+=str(recoPtVal)
 
# Current Relaxed
 cut_L1_rlx=cutD_rlx+'&&'+l1PtCut+'&& genmatches[0]>-1&&genmatches[1]>-1'
 _L1_rlx=effi_histo(ntuple,variable,cut_L1_rlx,binning,denom_rlx,
 'L1: Rlx',legend, ROOT.EColor.kGreen+3,20)
 print "l1 rlx done"
 _L1_rlx_veto=effi_histo(ntuple_rlx_veto,variable,cut_L1_rlx,binning,denom_rlx,
 'L1: Rlx (Tau Veto)',legend, ROOT.EColor.kRed,20)
 _L1_iso=effi_histo(ntuple_iso,variable,cut_L1_rlx,binning,denom_rlx,
 'L1: Iso',legend, ROOT.EColor.kBlue,20)
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


compare_efficiencies(
 "pt[1]",
 binPt,
 eff_ntuple,
 eff_iso_ntuple,
 eff_rlx_veto_ntuple,
 eff_ntuple_NoDoubling,
 eff_iso_ntuple_NoDoubling,
 recoPtCut = '(pt[0] >= '+str(recoPtVal)+')&&(pt[1] >= '+str(recoPtVal)+')',
 #recoPtCut='1',
 l1PtCut='(genpt[0] >= '+str(l1PtVal)+')&&(genpt[1]>= '+str(l1PtVal)+')',
 #l1PtCut='((genpt[0] >='+ str(36/1.314)+'&&abs(geneta[0])<0.9)||(genpt[0] >='+ str(36/1.208)+'&&abs(geneta[0])<1.4&&abs(geneta[0])>=0.9)||(genpt[0] >='+ str(36/1.185)+'&&abs(geneta[0])<2.5&&abs(geneta[0])>=1.4))&&((genpt[1] >='+ str(36/1.314)+'&&abs(geneta[1])<0.9)||(genpt[1] >='+ str(36/1.208)+'&&abs(geneta[1])<1.4&&abs(geneta[1])>=0.9)||(genpt[1] >='+ str(36/1.185)+'&&abs(geneta[1])<2.5&&abs(geneta[1])>=1.4))',
 extraCut='&&eta[0]>-2.5&&eta[0]<2.5&&eta[1]>-2.5&&eta[1]<2.5&&geneta[1]<2.5 &&geneta[0]>-2.5&&geneta[0]<2.5&&geneta[1]>-2.5&&geneta[1]<2.5',
)

