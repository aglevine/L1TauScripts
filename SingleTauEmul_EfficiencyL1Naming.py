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
drawLine=True
L1Denom=False
doRlxVeto=False
l1PtVal=float(argv[1])
l1PtValLow = float(argv[2])
l1PtValHigh = float(argv[3])
etaLow = float(argv[4])
etaHigh = float(argv[5])
l1ptResLow = float(argv[6])
l1ptResHigh = float(argv[7])
etaResLow = float(argv[8])
etaResHigh = float(argv[9])
#ISOTHRESHOLD=0.15a
ISOTHRESHOLD = 0.1
ISOTHRESHOLD4x4=0.25
turnOffIso = 192
L1CalibFactor = float(argv[10])
ZEROBIAS_RATE=5623.0*2590.0 #frequency X bunches
#saveWhere = 'EmulatorTestingNov/BinnedTausEOBIB/ThirdPassSingleTauEffMatchFixThreshFixJan280Point1Iso'
#saveWhere = 'EmulatorTestingNov/BinnedTausEOBIB/ResL1OnBottom'
saveWhere = 'March25LutTests/Plots/SingleTauEffNewCalibNewLUT'
name = 'recoPt_'+str(l1PtValLow)+'l1PtLow_'+str(l1PtValLow)+'l1PtHigh_'+str(l1PtValHigh)+'etaLow_'+str(etaLow)+'etaHigh_'+str(etaHigh)
var2D = 'dREgTau'
do2DRes = False


########
# File #
########
#Efficiency
#eff_ntuple_str = "EmulatorTestingNov/tau_emul_effDoublingNoFixRlxDec6.root"
#eff_iso_ntuple_str = "EmulatorTestingNov/tau_emul_effDoublingNoFixIsoDec6.root"
#eff_ntuple_str = "tau_emul_effTauEGCmpJan5.root"
#eff_iso_ntuple_str = "tau_emul_effTauEGCmpJan5Iso.root"
#eff_rlx_veto_ntuple_str = "tau_emul_effTauNoIsoWithTauVeto.root"
#eff_ntuple_str = "tau_emul_effJan14RlxNoTauVetoEGdR.root"
#eff_ntuple_str = "tau_rlxNoVeto8GeVTauThreshold8GeVNeighborThresholdSmallStatsJan22.root"
#eff_rlx_veto_ntuple_str = "tau_emul_effJan14RlxTauVetoEGdR.root"
#eff_iso_ntuple_str = "tau_emul_effJan14IsoTauVetoEGdR.root"
#eff_ntuple_str = "tau_emul_effJan27RlxNoTauVetoMatchFix.root"
#eff_rlx_veto_ntuple_str = "tau_emul_effJan27RlxTauVetoMatchFix.root"
#eff_iso_ntuple_str = "tau_emul_effJan27IsoTauVetoMatchFix.root"
#eff_ntuple_str = "tau_emul_effJan28RlxNoTauVetoThreshFix.root"
eff_ntuple_str = "March25LutTests/tau_emul_effMarch27NewCalibNewLUTIsoPoint1.root"
eff_rlx_veto_ntuple_str = "tau_emul_effJan28RlxTauVetoThreshFix.root"
#eff_iso_ntuple_str = "tau_emul_effJan28IsoTauVetoThreshFix.root"
eff_iso_ntuple_str="tau_emul_effJan28IsoTauVetoThreshFix0Point1Iso.root"
eff_ntuple_NoDoubling_str = "EmulatorTestingNov/tau_emul_effDoublingFixRecoSlightFixRlxDec6.root"
eff_iso_ntuple_NoDoubling_str = "EmulatorTestingNov/tau_emul_effDoublingFixRecoSlightFixIsoDec6.root"

eff_ntuple_file = ROOT.TFile(eff_ntuple_str)
eff_iso_ntuple_file = ROOT.TFile(eff_iso_ntuple_str)
eff_rlx_veto_ntuple_file = ROOT.TFile(eff_rlx_veto_ntuple_str)
eff_ntuple_NoDoubling_file = ROOT.TFile(eff_ntuple_NoDoubling_str)
eff_iso_ntuple_NoDoubling_file = ROOT.TFile(eff_iso_ntuple_NoDoubling_str)
#
eff_spot = 'TauEmulEffi/Ntuple'
eff_iso_spot = 'TauEmulEffiIso/Ntuple'
eff_ntuple = eff_ntuple_file.Get(eff_spot)
print eff_ntuple.GetEntries()
#eff_iso_ntuple = eff_iso_ntuple_file.Get(eff_spot) 72X
eff_iso_ntuple = eff_ntuple_file.Get(eff_iso_spot)
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

canvas = ROOT.TCanvas("asdf", "adsf", 800, 800)

def make_resolution(ntuple,ntuple_iso,binning,recoPtCut,l1PtCutLow,l1PtCutHigh,extraCut):
 info = 'EmulResPlot_reco'+str(recoPtCut)+'_l1Low'+str(l1ptResLow)+'_l1High'+str(l1ptResHigh)+'_etaLow'+str(etaResLow)+'_etaHigh'+str(etaResHigh)+'L1CalibFactor_'+str(L1CalibFactor)
 if (do2DRes):
 	info = 'EmulResPlot2DPU_'+var2D+'_reco'+str(recoPtCut)+'_l1Low'+str(l1PtCutLow)+'_l1High'+str(l1PtCutHigh)+'_etaLow'+str(etaLow)+'_etaHigh'+str(etaHigh) 	
 if (do2DRes):
 	varString = '(pt[0]-L1Matchedpt[0])/pt[0]:'+var2D+'[0]'
 else:
	if (L1Denom):
		varString = '(pt[0]-'+str(L1CalibFactor)+'*L1Matchedpt[0])/('+str(L1CalibFactor)+'*L1Matchedpt[0])'
	else:
		varString = '(pt[0]-'+str(L1CalibFactor)+'*L1Matchedpt[0])/(pt[0])'
 rlxRes = make_plot(ntuple,varString,'pt[0]>=4&&L1Matchedpt[0]>='+str(l1PtCutLow)+'&&L1Matchedpt[0]<'+str(l1PtCutHigh)+'&&L1matches[0]>=0'+extraCut,binning)
 isoRes = make_plot(ntuple_iso,varString,'pt[0]>=4&&L1Matchedpt[0]>='+str(l1PtCutLow)+'&&L1Matchedpt[0]<'+str(l1PtCutHigh)+'&&L1matches[0]>=0'+extraCut,binning)

 rlxRes.SetTitle('Resolution')
 if (do2DRes):
 	rlxRes.GetXaxis().SetTitle(var2D)
	rlxRes.GetYaxis().SetTitle('(RecoPt-L1Pt)/RecoPt')
 else:
	if (L1Denom):
		rlxRes.GetXaxis().SetTitle('(RecoPt-L1Pt)/L1Pt')
	else:
		rlxRes.GetXaxis().SetTitle('(RecoPt-L1Pt)/RecoPt')

 rlxRes.GetXaxis().SetRangeUser(-1,1)

 legend = ROOT.TLegend(0.65,0.55,0.85,0.79,'','brNDC')
 legend.SetBorderSize(0)
 legend.SetTextSize(0.023)
 legend.SetFillColor(0)
 print "???" + str(rlxRes.Integral())
 rlxResGauss = rlxRes.Clone()
 isoResGauss = isoRes.Clone()
 
 if (not do2DRes):
 	rlxResGauss.Scale(1/rlxResGauss.Integral())
 	isoResGauss.Scale(1/isoResGauss.Integral())

 rlxResFit = ROOT.TF1("asdf","gaus",-0.4,0.4)
 isoResFit = ROOT.TF1("asdf","gaus",-0.4,0.4)

 rlxResGauss.Fit(rlxResFit,"R")
 isoResGauss.Fit(isoResFit,"R")

 rlxResFit.SetLineColor(ROOT.EColor.kGreen+3)
 isoResFit.SetLineColor(ROOT.EColor.kYellow+3)
 
 legend.AddEntry(rlxRes,"Relaxed Taus")
 legend.AddEntry(rlxResFit,"Rlx Gaussian Fit")
 legend.AddEntry(isoRes,"Isolated Taus")
 legend.AddEntry(isoResFit,"Iso Gaussian Fit")

 rlxRes.SetLineColor(ROOT.EColor.kGreen+3)
 rlxRes.SetMarkerColor(ROOT.EColor.kGreen+3)
 rlxRes.SetMarkerSize(1.5)
 rlxRes.SetMarkerStyle(22)
 rlxRes.SetLineWidth(3)

 isoRes.SetLineColor(ROOT.EColor.kYellow+3)
 isoRes.SetMarkerColor(ROOT.EColor.kYellow+3)
 isoRes.SetMarkerSize(1.5)
 isoRes.SetMarkerStyle(22)
 isoRes.SetLineWidth(3)
 
 rlxRes.Sumw2()
 rlxRes.Scale(1/rlxRes.Integral())
 isoRes.Sumw2()
 isoRes.Scale(1/isoRes.Integral())

 if(not do2DRes):
 	rlxRes.Draw("ep")
 	rlxResFit.Draw("lsames")
 	isoRes.Draw("epsames")
 	isoResFit.Draw("lsames")
 else:
	rlxRes.Draw("col")
 if(not do2DRes):
 	rlxResTailIntegral = rlxRes.Integral(1,9)
 	isoResTailIntegral = isoRes.Integral(1,9)
 	print "rlxRes tail Integral: " + str(rlxResTailIntegral)
 	print "isoRes tail Integral: " + str(isoResTailIntegral)
 	legend.Draw()

 latex = ROOT.TLatex()
 latex.SetNDC()
 latex.SetTextSize(0.04)
 latex.SetTextAlign(31)
 strRlxMean = "Rlx Fit Mean: %.2f"%(rlxResFit.GetParameter(1))
 strRlxSigma = "Rlx Fit #sigma: %.2f"%(rlxResFit.GetParameter(2))
 strIsoMean = "Iso Fit Mean: %.2f"%(isoResFit.GetParameter(1))
 strIsoSigma = "Iso Fit #sigma: %.2f"%(isoResFit.GetParameter(2))
 strL1 = str(l1PtCutLow)+' < L1 pT < '+str(l1PtCutHigh)
 strEta = str(etaResLow)+' < |Eta| < '+str(etaResHigh)
 
 if(not do2DRes):
 	latex.DrawLatex(0.4,0.8,strRlxMean)
 	latex.DrawLatex(0.4,0.77,strRlxSigma)
 	latex.DrawLatex(0.4,0.74,strIsoMean)
 	latex.DrawLatex(0.4,0.71,strIsoSigma)
 	latex.DrawLatex(0.4,0.67,strL1)
	latex.DrawLatex(0.4,0.63,strEta)
	
 rlxRes.GetYaxis().SetRangeUser(0,0.3)
 canvas.SaveAs(saveWhere+info+'.png')

def make_plot(tree, variable, selection, binning, xaxis='', title='',calFactor=1):
 ''' Plot a variable using draw and return the histogram '''
 #draw_string = "%s * %0.2f>>htemp(%s)" % (variable,calFactor, ", ".join(str(x) for x in binning))
 draw_string = variable+" * %0.2f>>htemp(%s)" % (calFactor, ", ".join(str(x) for x in binning))
 print "draw_string "+ draw_string
 print selection
 #selectionMin0 = selection+"&&pt[1]>pt[0]"
 #tree.Draw(draw_string, selectionMin0, "goff")
 print tree.GetEntries() 
 tree.Draw(draw_string, selection, "goff")
 #output_histoMin0 = ROOT.gDirectory.Get("htemp").Clone()
 output_histo = ROOT.gDirectory.Get("htemp").Clone()
 print "output_histo entries" + str(output_histo.Integral())
 #draw_string = "pt[1] * %0.2f>>htemp2(%s)" % (calFactor, ", ".join(str(x) for x in binning))
 #selectionMin1 = selection+"&&pt[0]>pt[1]"
 #tree.Draw(draw_string, selectionMin1, "goff")
 #output_histoMin1 = ROOT.gDirectory.Get("htemp2").Clone()
 #output_histo = output_histoMin0.Clone()
 #output_histo.Add(output_histoMin1)
 output_histo.GetXaxis().SetTitle("Reco P_{T} [GeV]")
 ROOT.gDirectory.Clear()
 #output_histo.Rebin(16,"output_histoRebinned",xBins)
 #output_histoRebinned = ROOT.gDirectory.Get("output_histoRebinned").Clone()

 #output_histoRebinned.SetTitle(title)
 #for i in range(1,13):
 	#print "printing" + str(i)
 	#print output_histoRebinned.GetBinContent(i)
 #return output_histoRebinned
 return output_histo


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
 print "making num plot"
 num = make_plot(ntuple,variable,cut,binning)
 print "num entries" + str(num.GetEntries())
 print "denom entries" + str(denom.GetEntries())
 for i in range (1,num.GetNbinsX()):
   print num.GetBinContent(i)
 for i in range (1,denom.GetNbinsX()):
   print denom.GetBinContent(i)


 efiHist = num.Clone()
 efiHist.Divide(denom)
 efi = make_l1_efficiency(denom,num,color,marker)
 #efi = make_2D_l1_efficiency(denom,num)
 leg.AddEntry(efi,title,'pe')
 #efi.Draw('colz')
 efi.Draw('pe')
 efi.GetXaxis().SetTitle("Reco P_{T} [GeV]")
 #efi.GetXaxis().SetRangeUser(-3,3)
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
 

 #denom_NoDoubling_rlx = make_plot(ntuple_NoDoubling, variable, cutD_rlx, binning)
 if "pt" in variable:
 	frame = ROOT.TH1F('frame','frame',20,0,100)
 if "eta" in variable:
 	frame = ROOT.TH1F('frame','frame',12,-3,3)
 canvas.SetLogy(setLOG)
 frame.Draw("")
 frame.SetTitle('')
 frame.GetYaxis().SetTitle('Efficiency')
 frame.SetMaximum(1.1)
 frame.GetYaxis().SetTitle("Efficiency")
 tex.DrawLatex(0.1,0.91,'Single Tau Efficiency')
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
 if "eta" in variable:
 	frame.GetYaxis().SetRangeUser(0,1.0)
 	frame.GetXaxis().SetRangeUser(-3.0,3.0)
 if "pt" in variable:
	frame.GetXaxis().SetRangeUser(0,100)
 #tex.DrawLatex(0.1,0.91,'Tau '+variable+' Efficiency')
 #tex.SetTextSize(0.03)
 #tex.DrawLatex(0.1,0.87,'CMS Preliminary')
 #tex.SetTextSize(0.07)
 if "eta" in variable:
	legend=ROOT.TLegend(0.63,0.65,0.95,0.9)
	if (l1PtValLow > 35):
		legend=ROOT.TLegend(0.63,0.15,0.95,0.4)
 else:
 	legend = ROOT.TLegend(0.63,0.15,0.95,0.45,'','brNDC')
 legend.SetTextSize(0.023)
 legend.SetFillColor(0)
 legend.SetBorderSize(0)
 
 info ='_'+variable
 if variable=='nPVs': info+=str(recoPtVal)
 
# Current Relaxed
 cut_L1_rlx=cutD_rlx+'&&'+l1PtCut+'&& L1matches[0]>-1'
 _L1_rlx=effi_histo(ntuple,variable,cut_L1_rlx,binning,denom_rlx,
 'L1: Rlx',legend, ROOT.EColor.kGreen+3,20)
 if doRlxVeto:
 	_L1_rlx_veto=effi_histo(ntuple_rlx_veto,variable,cut_L1_rlx,binning,denom_rlx,
 	'L1: Rlx (Tau Veto)',legend, ROOT.EColor.kRed,20)
 	print "l1 rlx done"
 _L1_iso=effi_histo(ntuple_iso,variable,cut_L1_rlx,binning,denom_rlx,
 'L1: Iso',legend, ROOT.EColor.kBlue,20)
# _L1_rlx_NoDoubling=effi_histo(ntuple_NoDoubling,variable,cut_L1_rlx,binning,denom_NoDoubling_rlx,
 #'L1: Rlx No Doubling',legend, ROOT.EColor.kMagenta+3,25)
 #print "l1 iso nodoubling done"
# _L1_iso_NoDoubling=effi_histo(ntuple_NoDoublingIso,variable,cut_L1_rlx,binning,denom_NoDoubling_rlx,
 #'L1: Iso No Doubling',legend, ROOT.EColor.kBlue-1,25)
 #print "l1 rlx nodoubling done"
 
 latex = ROOT.TLatex()
 latex.SetNDC()
 latex.SetTextSize(0.03)
 latex.SetTextAlign(31)
 recoStr = "reco pT > " + str(l1PtValLow)
 L1Str = str(l1PtValLow) +" < L1 pT < "+str(l1PtValHigh)
 etaStr = str(etaLow) +" < |Eta| < "+str(etaHigh)

 if drawLine == True:
   vert = ROOT.TLine(l1PtVal,0,l1PtVal,1.1)
   vert.SetLineWidth(3)
   vert.SetLineStyle(3)
   vert.Draw()

# if "pt" in variable:
#	latex.DrawLatex(0.8,0.53,L1Str)
#	latex.DrawLatex(0.8,0.48,etaStr)
# elif "eta" in variable:
#	latex.DrawLatex(0.8,0.53,L1Str)
#	latex.DrawLatex(0.8,0.48,recoStr)
 
 legend.Draw()

 
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
xBins = array.array('d',[20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100])
#binRes = [25,-1,1]
if (do2DRes):
	#binRes = [25, 0,75,25,-1,1]
        #binRes = [25,-2.5,2.5,25,-1,1]
	binRes = [10,0,5,25,-1,1]
 	#binRes = [20,0,100,25,-1,1]
else:
	binRes = [25,-1,1]
binPt = [20,0,100]
binVert=[10,0,35]
binJetPt=[40,0,70]
binEta = [12,-3,3]
binEtaGen = [12,-3,3,20,0,100]
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
'''
compare_efficiencies(
 #'pt[0]:pt[1]',
 "L1Matchedeta[0]",
 binEta,
 eff_ntuple,
 eff_iso_ntuple,
 eff_rlx_veto_ntuple,
 eff_ntuple_NoDoubling,
 eff_iso_ntuple_NoDoubling,
 recoPtCut = '(pt[0] >= '+str(l1PtValLow)+')',
#+'&&pt[0] <'+str(recoPtHigh)+')',
 #recoPtCut='1',
 l1PtCut='(L1Matchedpt[0] >= '+str(l1PtValLow)+'&&L1Matchedpt[0]<'+str(l1PtValHigh)+')',
 extraCut='&&eta[0]>-2.5&&eta[0]<2.5&&L1Matchedeta[0]>-2.5&&L1Matchedeta[0]<2.5',
)
compare_efficiencies(
 #'pt[0]:pt[1]',
 "pt[0]",
 binPt,
 eff_ntuple,
 eff_iso_ntuple,
 eff_rlx_veto_ntuple,
 eff_ntuple_NoDoubling,
 eff_iso_ntuple_NoDoubling,
 recoPtCut = '(pt[0] >= '+str(recoPtVal)+')',
 #recoPtCut='1',
 l1PtCut='(L1Matchedpt[0] >='+ str(l1PtVal)+')',
 extraCut='&&eta[0]>-2.5&&eta[0]<2.5&&L1Matchedeta[0]>'+str(etaLow)+'&&L1Matchedeta[0]<'+str(etaHigh),
)
'''
compare_efficiencies(
 #'pt[0]:pt[1]',
 "pt[0]",
 binPt,
 eff_ntuple,
 eff_iso_ntuple,
 eff_rlx_veto_ntuple,
 eff_ntuple_NoDoubling,
 eff_iso_ntuple_NoDoubling,
 recoPtCut = '(pt[0] >= '+str(20)+'&&eta[0]>='+str(etaLow)+'&&eta[0]<'+str(etaHigh)+')',
 #recoPtCut='1',
 #l1PtCut='((L1Matchedpt[0] >='+ str(36/1.255)+'&&abs(L1Matchedeta[0])<0.9)||(L1Matchedpt[0] >='+ str(36/1.208)+'&&abs(L1Matchedeta[0])<1.4&&abs(L1Matchedeta[0])>=0.9)||(L1Matchedpt[0] >='+ str(36/1.185)+'&&abs(L1Matchedeta[0])<2.5&&abs(L1Matchedeta[0])>=1.4))',
 #l1PtCut='((L1Matchedpt[0] >='+ str(44/1.163)+'&&abs(L1Matchedeta[0])<0.9)||(L1Matchedpt[0] >='+ str(44/1.122)+'&&abs(L1Matchedeta[0])<1.4&&abs(L1Matchedeta[0])>=0.9)||(L1Matchedpt[0] >='+ str(44/1.070)+'&&abs(L1Matchedeta[0])<2.5&&abs(L1Matchedeta[0])>=1.4))',
 
 #l1PtCut = '(L1Matchedpt[0]>='+str(36/1.255)+')',
 #l1PtCut = '(L1Matchedpt[0]>='+str(36)+')',
 l1PtCut = '(L1Matchedpt[0] >= '+str(l1PtVal) +')',
 extraCut='&&eta[0]>-2.5&&eta[0]<2.5&&L1Matchedeta[0]>-2.5&&L1Matchedeta[0]<2.5',
)

make_resolution(eff_ntuple,
                eff_iso_ntuple,
                binRes,
                recoPtCut = 4,
                l1PtCutLow= l1ptResLow,
                l1PtCutHigh = l1ptResHigh,
                #extraCut = '&&eta[0]>-2.5&&eta[0]<2.5&&L1Matchedeta[0]>'+str(etaResLow)+'&&L1Matchedeta[0]<' + str(etaResHigh)
                extraCut = '&&abs(eta[0])<=2.5&&abs(L1Matchedeta[0])<=2.5&&abs(L1Matchedeta[0])>='+str(etaResLow)+'&&abs(L1Matchedeta[0])<'+str(etaResHigh)
)
 
