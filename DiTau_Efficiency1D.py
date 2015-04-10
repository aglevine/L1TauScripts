'''
Makes Tau efficiency plots
Authors: T.M.Perry, E.K.Friis, M.Cepeda, A.G.Levine, N.Woods UW Madison
'''
from sys import argv, stdout, stderr
import ROOT
import sys
import array

efficiencyPlots=True
# which curves to draw on rate and efficiency plots
# most recent tau veto settings are only used for uct rlx and uct iso by hand
drawUCTIso = False #draw curves with isolation specified by inputs in makeRates or makeEfficiencies (should be set to false by default)
drawUCTRlx = True #draw relaxed curves
drawUCTRlxVeto = False
drawUCTIso_byhand = True #draw curves with isolation specified by user
Cmp4x4 = False #compare 4x4 and 4x8 taus
TauVetoRlx = False #apply tau veto to relaxed taus (should be set to false by default)
Veto4x4 = False #apply tau veto to 4x4 taus (should be set to false by default)
IsoRes = False #isolated resolution plot
drawPtCmp = False
drawPtCmpRlx = False
#Legacy taus
drawL1Iso = False
drawL1Rlx = False

##################
# Set Parameters #
##################
eff_ntuple = argv[1]
if "E2" in eff_ntuple:
	Ethresh = 2
elif "E3" in eff_ntuple:
	Ethresh = 3
elif "E4" in eff_ntuple:
	Ethresh = 4
else:
	"missing Ethresh"
	sys.exit()
if "H2" in eff_ntuple:
        Hthresh = 2
elif "H3" in eff_ntuple:
        Hthresh = 3
elif "H4" in eff_ntuple:
        Hthresh = 4
else:
        "missing Hthresh"
        sys.exit()
selection = argv[2]
turnOffTauVeto = argv[3]
LIso=3
LSB=50
l1ptVal=argv[4]
recoPtVal=20
#ISOTHRESHOLD=0.15a
ISOTHRESHOLD = 0.1
ISOTHRESHOLD4x4=0.25
turnOffIso = 192
L1_CALIB_FACTOR = 1.0
L1G_CALIB_FACTOR = 1.0
ZEROBIAS_RATE=11246.0*2590.0 #frequency X bunches
saveWhere = 'DiTauplots/July26Taus/EffTau4x8vs4x4E'+str(Ethresh)+'H'+str(Hthresh)+selection+'RlxVeto'+str(TauVetoRlx)+'Apply4x4TauVeto'+str(Veto4x4)+'OffIso'+str(turnOffIso)+'OffVeto'+str(turnOffTauVeto)+'Iso'+str(ISOTHRESHOLD)+'L1pTVal'+str(l1ptVal)
if Cmp4x4 == False:
        saveWhere = 'DiTauplots/PtOrdering/1DDiTauEffNoMinAdding'+str(Ethresh)+'H'+str(Hthresh)+selection+'RlxVeto'+str(TauVetoRlx)+'OffIso'+str(turnOffIso)+'OffVeto'+str(turnOffTauVeto)+'Iso'+str(ISOTHRESHOLD)+'L1pTThresh'+str(l1ptVal)
if drawL1Rlx == True:
	saveWhere = saveWhere+'L1Rlx'
if drawPtCmp == True:
	saveWhere = saveWhere+'PtCmp'
if drawPtCmpRlx == True:
	saveWhere = saveWhere+'PtCmpRlx'
#saveWhere = 'plots/4x4Taus/EffTau4x4'+selection+'OffIso'+str(turnOffIso)+'OffVeto'+str(turnOffTauVeto)+'Iso'+str(ISOTHRESHOLD)
#saveWhere = 'plots/test4x8Efficiency'

########
# File #
########
#Efficiency
#eff_ntuple = 'EactHactTaus_June13/ECAL3/tau_eff_4x8_E3H3_NoNeighborSeed.root'
#eff_ntuple = 'uct_efficiency_tree_numEvent5000.root'
eff_ntuple_file = ROOT.TFile(eff_ntuple)
#
eff_rlx_spot = 'DiTauEfficiency/Ntuple'
#eff_iso_spot = 'isoTauEfficiency/Ntuple'
eff_iso_spot = 'DiTauEfficiency/Ntuple'
eff_rlx_eg_ntuple = eff_ntuple_file.Get(eff_rlx_spot)
eff_iso_eg_ntuple = eff_ntuple_file.Get(eff_iso_spot)
if Cmp4x4 == True:
	#eff_ntuple4x4 = '4x4Taus/tau_eff_4x4_E3H3.root'
	eff_ntuple4x4 = 'tau_eff_4x4_E3H3_fixdo4x4Flag_July17.root'
	eff_ntuple_file4x4 = ROOT.TFile(eff_ntuple4x4)
	eff_rlx_eg_ntuple4x4 = eff_ntuple_file4x4.Get(eff_rlx_spot)
	eff_iso_eg_ntuple4x4 = eff_ntuple_file4x4.Get(eff_iso_spot)
else:
        eff_rlx_eg_ntuple4x4 = None
        eff_iso_eg_ntuple4x4 = None
#To Be Made
store = ROOT.TFile(saveWhere+'.root','RECREATE')

name=''
if drawUCTIso or drawUCTRlx or drawUCTIso_byhand: name+='_UCT_'
if drawUCTRlx: name+='R'
if drawUCTIso: name+='I'
if drawUCTIso_byhand: name+='Ibh'+str(int(ISOTHRESHOLD * 10))
if Cmp4x4: name+='4x4'
name+='_'

if drawL1Iso or drawL1Rlx: name+= 'L1_'
if drawL1Rlx: name+='R'
if drawL1Iso: name+='I'

extraName=''
name+=extraName

log = open(saveWhere+name+extraName+'.log','w')
log.write('LIso = '+str(LIso)+'\n')
log.write('LSB = '+str(LSB)+'\n')
log.write('l1ptVal = '+str(l1ptVal)+'\n')
log.write('recoPtVal = '+str(recoPtVal)+'\n')
log.write('ISOTHRESHOLD = '+str(ISOTHRESHOLD)+'\n')
log.write('L1_CALIB_FACTOR = '+str(L1_CALIB_FACTOR)+'\n')
log.write('L1G_CALIB_FACTOR = '+str(L1G_CALIB_FACTOR)+'\n')
log.write('ZEROBIAS_RATE = '+str(ZEROBIAS_RATE)+'\n\n')
#########
# STYLE #
#########
ROOT.gROOT.SetStyle("Plain")
#ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

#tex = ROOT.TLatex()
#tex.SetTextSize(0.07)
#tex.SetTextAlign(11)
#tex.SetNDC(True)

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

def make_plot(tree, variable, selection, binning, xaxis='', title='',calFactor=1):
 ''' Plot a variable using draw and return the histogram '''
 #draw_string = "%s * %0.2f>>htemp(%s)" % (variable,calFactor, ", ".join(str(x) for x in binning))
 draw_string = "pt[1] * %0.2f>>htemp(%s)" % (calFactor, ", ".join(str(x) for x in binning))
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
 output_histo.GetXaxis().SetTitle("Min(P_{T}1, P_{T}2)")
 ROOT.gDirectory.Clear()
 output_histo.Rebin(12,"output_histoRebinned",xBins)
 output_histoRebinned = ROOT.gDirectory.Get("output_histoRebinned").Clone()

 output_histoRebinned.SetTitle(title)
 print output_histo.GetBinContent(8)
 for i in range(1,13):
 	print "printing" + str(i)
 	print output_histoRebinned.GetBinContent(i)
 return output_histoRebinned


######################################################################
##### RESOLUTION #####################################################
######################################################################


def make_res_nrml(ntuple_rlx_4x8,ntuple_iso_4x8,ntuple_rlx_4x4,ntuple_iso_4x4,reco,l1,l1g,binning,cutPtVarg='l1gPt',cutPtVar='l1Pt',cutPt=l1ptVal,isoCut='',isoCut4x4='',filename='',extraCut='',extraCutb='',setLOG=False):
 canvas.SetLogy(setLOG)
 info = 'RES_'+str(reco)+'_'+cutPtVar+'Cut'
 eff_jet_spot = 'jetEfficiency/Ntuple'
 jet_ntuple = eff_ntuple_file.Get(eff_jet_spot)
 eff_eg_spot = 'rlxEGEfficiency/Ntuple'
 eg_ntuple = eff_ntuple_file.Get(eff_eg_spot)
 #ntuple_rlx_4x8 = eg_ntuple
 vetoCut = extraCut
 if selection == "NoVeto":
        #frame.GetYaxis().SetTitle("Efficiency")
        vetoCut4x4 = vetoCut
 elif selection == "NeighborVeto":
        #frame.GetYaxis().SetTitle("Efficiency, TauVetoNeighbor = 0")
        vetoCut4x4 = vetoCut
        vetoCut = vetoCut + "&&l1gTauVetoNeighbor[0] == 0 &&l1gTauVetoNeighbor[1]==0"
 elif selection == "TauVeto":
        #frame.GetYaxis().SetTitle("Efficiency, TauVeto=0")
        vetoCut = vetoCut + "&&((l1gTauVeto[0] == 0  || l1gPt[0] > " +str(turnOffTauVeto) + ")&&(l1gTauVeto[1] == 0  || l1gPt[1] > " +str(turnOffTauVeto) + "))"
        vetoCut4x4 = vetoCut
 elif selection == "TauVetoAndNeighbor":
        vetoCut4x4 = vetoCut + "&&((l1gTauVeto[0] == 0  || l1gPt[0] > " +str(turnOffTauVeto) + ")&&(l1gTauVeto[1] == 0  || l1gPt[1] > " +str(turnOffTauVeto) + "))"
        vetoCut = vetoCut + "&&(l1gTauVetoNeighbor[0] == 0 || l1gPt[0] > "+str(turnOffTauVeto)+")&&(l1gTauVetoNeighbor[1]==0 || l1gPt[1] > "+str(turnOffTauVeto)+")&&((l1gTauVeto[0] == 0  || l1gPt[0] > " +str(turnOffTauVeto) + ")&&(l1gTauVeto[1] == 0  || l1gPt[1] > " +str(turnOffTauVeto) + "))"
        #frame.GetYaxis().SetTitle("Efficiency, TauVeto=0,TauVetoNeighbor=0")
 elif selection == "AllTauVeto":
	vetoCut4x4 = vetoCut + "&&(l1gTauVeto == 0 || l1gPt > " +str(turnOffTauVeto) + ")"
	vetoCut = vetoCut + "&&l1gTauVetoNeighborE == 0&&l1gTauVetoNeighborSE == 0&&l1gTauVetoNeighborS == 0&&l1gTauVetoNeighborSW == 0&&l1gTauVetoNeighborW == 0&&l1gTauVetoNeighborNW == 0&&l1gTauVetoNeighborN == 0&&l1gTauVetoNeighborNE == 0&&(l1gTauVeto == 0 || l1gPt > " +str(turnOffTauVeto) + ")"
 else:
        print "Invalid selection"
        sys.exit()
 if Veto4x4 == False:
        vetoCut4x4 = extraCut
        #frame.GetYaxis().SetTitle("Efficiency")

 l1gplot_rlx_4x8 = make_plot(
  ntuple_rlx_4x8, '('+str(reco)+' - ('+str(L1G_CALIB_FACTOR)+' * '+str(l1g)+'))/'+str(reco),
  str(reco)+'>'+str(cutPt)+'&&l1gPt>='+str(lowbound)+"&&l1gPt < "+str(highbound)+'&&l1gMatch==1'+extraCut,binning
 )

 l1gplot_iso_4x8 = make_plot(
  ntuple_rlx_4x8, '('+str(reco)+' - ('+str(L1G_CALIB_FACTOR)+' * '+str(l1g)+'))/'+str(reco),
  str(reco)+'>'+str(cutPt)+'&&l1gPt>='+str(lowbound)+"&&l1gPt < "+str(highbound)+'&&l1gMatch==1'+extraCut+isoCut+vetoCut,binning
 )

 if Cmp4x4:
   l1gplot_rlx_4x4 = make_plot(
     ntuple_rlx_4x4, '('+str(reco)+' - ('+str(L1G_CALIB_FACTOR)+' * '+str(l1g)+'))/'+str(reco),
    str(reco)+'>'+str(cutPt)+extraCut,binning
   )

   l1gplot_iso_4x4 = make_plot(
     ntuple_rlx_4x4, '('+str(reco)+' - ('+str(L1G_CALIB_FACTOR)+' * '+str(l1g)+'))/'+str(reco),
    str(reco)+'>'+str(cutPt)+extraCut+isoCut4x4+vetoCut4x4,binning
   )

 l1gplot_rlx_4x8.SetTitle('Resolution')
 l1gplot_rlx_4x8.GetXaxis().SetTitle('(RecoPt- L1Pt)/RecoPt')
 l1gplot_iso_4x8.SetTitle('Resolution')
 l1gplot_iso_4x8.GetXaxis().SetTitle('(RecoPt- L1Pt)/RecoPt')

 legend = ROOT.TLegend(0.65,0.55,0.95,0.89,'','brNDC')
 legend.SetFillColor(ROOT.EColor.kWhite)
 legend.SetBorderSize(0)
 legend.SetTextSize(0.023)
  
 #l1gplot_rlx_4x4.Scale(1/l1gplot_rlx_4x4.Integral())
 l1gplot_rlx_4x8.Scale(1/l1gplot_rlx_4x8.Integral())
 #l1gplot_iso_4x4.Scale(1/l1gplot_iso_4x4.Integral())
 l1gplot_iso_4x8.Scale(1/l1gplot_iso_4x8.Integral())

 Rlx4x8Gauss = l1gplot_rlx_4x8.Clone()
 #Rlx4x4Gauss = l1gplot_rlx_4x4.Clone()
 Iso4x8Gauss = l1gplot_iso_4x8.Clone()
 #Iso4x4Gauss = l1gplot_iso_4x4.Clone()
 rlx4x8Fit = ROOT.TF1("asdf","gaus",-1,1)
 #rlx4x4Fit = ROOT.TF1("asdf","gaus",-1,1)
 iso4x8Fit = ROOT.TF1("asdf","gaus",-1,1)
 #iso4x4Fit = ROOT.TF1("asdf","gaus",-1,1)
 Iso4x8Gauss.Fit(iso4x8Fit)
 #Iso4x4Gauss.Fit(iso4x4Fit)
 Rlx4x8Gauss.Fit(rlx4x8Fit)
 #Rlx4x4Gauss.Fit(rlx4x4Fit)
 rlx4x8Fit.SetLineColor(ROOT.EColor.kGreen+3)
 #rlx4x4Fit.SetLineColor(ROOT.EColor.kMagenta)
 iso4x8Fit.SetLineColor(ROOT.EColor.kYellow+3)
 #iso4x4Fit.SetLineColor(ROOT.EColor.kRed)
 if IsoRes:
 	legend.AddEntry(iso4x8Fit,"4x8 Iso Gaussian Fit")
 #	legend.AddEntry(iso4x4Fit,"4x4 Iso Gaussian Fit")
        legend.AddEntry(l1gplot_iso_4x8,'UCT (4x8): Iso (No Tau Veto)')
  #      legend.AddEntry(l1gplot_iso_4x4,'UCT (4x4): Iso')
 else:
 	legend.AddEntry(rlx4x8Fit,"4x8 Rlx Gaussian Fit")
 #	legend.AddEntry(rlx4x4Fit,"4x4 Rlx Gaussian Fit")
 	legend.AddEntry(l1gplot_rlx_4x8,'UCT (4x8): Rlx (No Tau Veto)')
 #	legend.AddEntry(l1gplot_rlx_4x4,'UCT (4x4): Rlx')


 #l1gplot_rlx_4x4.SetLineColor(ROOT.EColor.kMagenta)
 #l1gplot_rlx_4x4.SetMarkerColor(ROOT.EColor.kMagenta)
 #l1gplot_rlx_4x4.SetMarkerSize(1.5)
 #l1gplot_rlx_4x4.SetMarkerStyle(22) 
 #l1gplot_rlx_4x4.SetLineWidth(3)
 l1gplot_rlx_4x8.SetLineColor(ROOT.EColor.kGreen+3)
 l1gplot_rlx_4x8.SetMarkerColor(ROOT.EColor.kGreen+3)
 l1gplot_rlx_4x8.SetMarkerSize(1.5)
 l1gplot_rlx_4x8.SetMarkerStyle(22)
 #l1gplot_rlx_4x8.SetLineWidth(3)
 #l1gplot_iso_4x4.SetLineColor(ROOT.EColor.kRed)
 #l1gplot_iso_4x4.SetMarkerColor(ROOT.EColor.kRed)
 #l1gplot_iso_4x4.SetMarkerSize(1.5)
 #l1gplot_iso_4x4.SetMarkerStyle(25)

 #l1gplot_rlx_4x8.SetLineWidth(3)
 l1gplot_iso_4x8.SetLineColor(ROOT.EColor.kYellow+3)
 l1gplot_iso_4x8.SetMarkerColor(ROOT.EColor.kYellow+3)
 l1gplot_iso_4x8.SetMarkerSize(1.5)
 l1gplot_iso_4x8.SetMarkerStyle(25)

 #l1gplot_iso_4x8.SetLineWidth(3)
 #l1gplot_rlx_4x4.Scale(1/l1gplot_rlx_4x4.Integral())
 l1gplot_rlx_4x8.Scale(1/l1gplot_rlx_4x8.Integral())
 #l1gplot_iso_4x4.Scale(1/l1gplot_iso_4x4.Integral())
 l1gplot_iso_4x8.Scale(1/l1gplot_iso_4x8.Integral())
 if IsoRes:
	l1gplot_iso_4x8.Draw("p")
 	iso4x8Fit.Draw("lsames")
 #	iso4x4Fit.Draw("lsames")
# 	l1gplot_iso_4x4.Draw("psames")
 else:
	l1gplot_rlx_4x8.Draw("p")
 	rlx4x8Fit.Draw("lsames")
 #	rlx4x4Fit.Draw("lsames")
 #	l1gplot_rlx_4x4.Draw("psames")
 print "Mean 4x8:" + str(iso4x8Fit.GetParameter(1))
 print "Sigma 4x8:" + str(iso4x8Fit.GetParameter(2))
 #print "Mean 4x4:" + str(iso4x4Fit.GetParameter(1))
 #print "Sigma 4x4:" + str(iso4x4Fit.GetParameter(2))
 #l1gplot_iso_4x4.Draw("psames")
 #l1gplot_iso_4x8.Draw("psames")
 #l1bplot.Draw('sames')
 #l1gplot.SetMaximum(1.1*max(l1gplot.GetMaximum(),l1bplot.GetMaximum()))
 #l1gplot_rlx_4x4.SetMaximum(0.15)
 #legend.Draw()
 
 latex = ROOT.TLatex()
 latex.SetNDC()
 latex.SetTextSize(0.03)
 latex.SetTextAlign(31)
 if IsoRes == False:
 	str4x8Mean = "4x8 Fit Mean: %.2f"%(rlx4x8Fit.GetParameter(1))
	str4x8Sigma = "4x8 Fit #sigma: %.2f"%(rlx4x8Fit.GetParameter(2))
 #	str4x4Mean = "4x4 Fit Mean: %.2f"%(rlx4x4Fit.GetParameter(1))
 #	str4x4Sigma = "4x4 Fit #sigma: %.2f"%(rlx4x4Fit.GetParameter(2)) 
 else:
	str4x8Mean = "4x8 Fit Mean: %.2f"%(iso4x8Fit.GetParameter(1))
        str4x8Sigma = "4x8 Fit #sigma: %.2f"%(iso4x8Fit.GetParameter(2))
  #      str4x4Mean = "4x4 Fit Mean: %.2f"%(iso4x4Fit.GetParameter(1))
   #     str4x4Sigma = "4x4 Fit #sigma: %.2f"%(iso4x4Fit.GetParameter(2))
 latex.DrawLatex(0.4,0.8,str4x8Mean)
 latex.DrawLatex(0.4,0.77,str4x8Sigma)
 #latex.DrawLatex(0.4,0.74,str4x4Mean)
 #latex.DrawLatex(0.4,0.71,str4x4Sigma)
 canvas.SaveAs(saveWhere+info+filename+str(lowbound)+str(highbound)+str(IsoRes)+'.png')


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

def effi_histo(ntuple,variable,cut,binning,denom,title,leg,color,marker,logg):
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
 if ISOTHRESHOLD < 1000:
 	cutStr = "L1 PT > %0.0f"%(float(l1ptVal))
 else:
        cutStr = "No ISO, L1 PT > %0.0f, Tau Veto Selection"%(float(l1ptVal))

 if drawPtCmp == True or drawPtCmpRlx == True:
	cutStr = ""
 tex.DrawLatex(0.1,0.91,cutStr)
 tex.SetTextAlign(31)
 logg.write('---------------------------------\n')
 logg.write(title+'\n\n')
 logg.write('Tree: '+ntuple.GetDirectory().GetName()+'\n\n')
 logg.write('Cut: '+cut+'\n\n')
 for i in range (1,efiHist.GetNbinsX()):
	print efiHist.GetBinContent(i)
 return efi

def compare_efficiencies(
 variable,
 binning,
 ntuple_rlx=None,
 ntuple_iso=None,
 ntuple_rlx4x4=None,
 ntuple_iso4x4=None,
 recoPtCut='(1)',l1PtCut='(1)',l1gPtCut='(1)',
 isoCut='(1)', isoCut4x4 = '(1)',extraCut = '&&(1)',
 drawUCTIso_=False,
 drawUCTRlx_=False,
 drawUCTIso_byhand_=False,
 drawL1Iso_=False,
 drawL1Rlx_=False,
 legExtra='',
 setLOG=False
):
 '''
Returns a (L1, L1G) tuple of TGraphAsymmErrors
'''

 cutD_rlx = recoPtCut+extraCut
 print "cutD_rlx"+cutD_rlx
 denom_rlx = make_plot(
  ntuple_rlx,variable,
  cutD_rlx,
  binning
 )
 print denom_rlx.GetEntries()
 cutD_iso = cutD_rlx #+ '&& (dr03CombinedEt/recoPt)<0.2'
 denom_iso = make_plot(
  ntuple_iso,variable,
  cutD_iso,
  binning
 )
 
 if Cmp4x4:
 	denom_rlx4x4 = make_plot(
  	  ntuple_rlx4x4,variable,
  	  cutD_rlx,
  	  binning
 	)

 	denom_iso4x4 = make_plot(
  	  ntuple_iso4x4,variable,
  	  cutD_iso,
  	  binning
 	)
 log.write('_____________________________\n')
 log.write('-------- Efficiency ---------\n\n')
 log.write('Variable: '+variable+'\n\n')
 log.write('Denominator Tree: '+ntuple_rlx.GetDirectory().GetName()+'\n')
 #log.write('Denominator Cut: '+cutD+'\n\n')
 
 frame = ROOT.TH1F('frame','frame',20,0,200)
 canvas.SetLogy(setLOG)
 frame.Draw("")
 frame.SetTitle('')
 frame.GetYaxis().SetTitle('Efficiency')
 frame.SetMaximum(1.1)
 vetoCut = extraCut
 if selection == "NoVeto":
	frame.GetYaxis().SetTitle("Efficiency")
	vetoCut4x4 = vetoCut
 elif selection == "NeighborVeto":
	frame.GetYaxis().SetTitle("Efficiency, TauVetoNeighbor = 0")
	vetoCut4x4 = vetoCut
	vetoCut = vetoCut + "&&l1gTauVetoNeighbor[0] == 0&&l1gTauVetoNeighbor[1]==0"
 elif selection == "TauVeto":
        frame.GetYaxis().SetTitle("Efficiency, TauVeto=0")
	vetoCut = vetoCut + "&&((l1gTauVeto[0] == 0  || l1gPt[0] > " +str(turnOffTauVeto) + ")&&(l1gTauVeto[1] == 0  || l1gPt[1] > " +str(turnOffTauVeto) + "))"
	vetoCut4x4 = vetoCut
 elif selection == "TauVetoAndNeighbor":
	vetoCut4x4 = vetoCut + "&&((l1gTauVeto[0] == 0  || l1gPt[0] > " +str(turnOffTauVeto) + ")&&(l1gTauVeto[1] == 0  || l1gPt[1] > " +str(turnOffTauVeto) + "))"
        vetoCut = vetoCut + "&&(l1gTauVetoNeighbor[0] == 0 || l1gPt[0] > "+str(turnOffTauVeto)+")&&(l1gTauVetoNeighbor[1]==0 || l1gPt[1] > "+str(turnOffTauVeto)+")&&((l1gTauVeto[0] == 0  || l1gPt[0] > " +str(turnOffTauVeto) + ")&&(l1gTauVeto[1] == 0  || l1gPt[1] > " +str(turnOffTauVeto) + "))"
	frame.GetYaxis().SetTitle("Efficiency, TauVeto=0,TauVetoNeighbor=0")
 elif selection == "AllTauVeto":
        vetoCut4x4 = vetoCut + "&&(l1gTauVeto == 0 || l1gPt > " +str(turnOffTauVeto) + ")"
        vetoCut = vetoCut + "&&l1gTauVetoNeighborE == 0&&l1gTauVetoNeighborSE == 0&&l1gTauVetoNeighborS == 0&&l1gTauVetoNeighborSW == 0&&l1gTauVetoNeighborW == 0&&l1gTauVetoNeighborNW == 0&&l1gTauVetoNeighborN == 0&&l1gTauVetoNeighborNE == 0&&(l1gTauVeto == 0 || l1gPt > " +str(turnOffTauVeto) + ")"
 else:
	print "Invalid selection"
	sys.exit()
 if Veto4x4 == False:
	vetoCut4x4 = extraCut
	frame.GetYaxis().SetTitle("Efficiency")
 if variable is 'nPVs': frame.GetXaxis().SetTitle('Nr. Primary Vertices')
 elif variable is 'pt[0]:pt[1]':
	frame.GetXaxis().SetTitle('pt[1]')
	frame.GetYaxis().SetTitle('pt[0]')
 elif variable is 'Min(pt[1],pt[0])': frame.GetXaxis().SetTitle("Min(P_{T}1, P_{T}2)")
 else: frame.GetXaxis().SetTitle(variable)
 frame.GetXaxis().SetRangeUser(0,200)
 #tex.DrawLatex(0.1,0.91,'Tau '+variable+' Efficiency')
 #tex.SetTextSize(0.03)
 #tex.DrawLatex(0.1,0.87,'CMS Preliminary')
 #tex.SetTextSize(0.07)
 legend = ROOT.TLegend(0.63,0.15,0.95,0.45,'','brNDC')
 legend.SetTextSize(0.023)
 legend.SetFillColor(0)
 legend.SetBorderSize(0)
 legend.SetHeader(legExtra)
 
 info ='_'+variable
 if variable=='nPVs': info+=str(recoPtVal)
 
# Current Relaxed
 if drawL1Rlx_:
  cut_L1_rlx=recoPtCut+'&&'+l1PtCut+'&& l1Match[0]&&l1Match[1]'
  h_L1_rlx=effi_histo(ntuple_rlx,variable,cut_L1_rlx,binning,denom_rlx,
  'L1: Rlx',legend,
  colorCR,markerCR,log)
  h_L1_rlx.SetName('h_L1_rlx')
  h_L1_rlx.Write()
# Current With Isolation
 if drawL1Iso_:
  cut_L1_iso=recoPtCut+'&&'+l1PtCut+'&& l1Match[0]&&l1Match[1]'# && (dr03CombinedEt/recoPt)<0.2'
  h_L1_iso=effi_histo(ntuple_iso,variable,cut_L1_iso,binning,denom_iso,
  'L1: Iso',legend,
  colorCI,markerCI,log)
  h_L1_iso.SetName('h_L1_iso')
  h_L1_iso.Write()
# UCT Relaxed
 if drawUCTRlx_:
  if TauVetoRlx == False:
  	cut_uctR=cutD_rlx+'&&'+l1gPtCut
	rlxLegendStr = 'UCT (4x8): Rlx (No Tau Veto)'
  else:
	cut_uctR=cutD_rlx+'&&'+l1gPtCut+vetoCut
 	rlxLegendStr = 'UCT (4x8): Rlx'
  h_UCT_rlx=effi_histo(ntuple_rlx,variable,cut_uctR,binning,denom_rlx,
  rlxLegendStr,legend,
   colorUR,22,log)
  h_UCT_rlx.SetName('h_UCT_rlx')
  h_UCT_rlx.Write()
 if drawUCTRlxVeto:
  cut_uctRVeto=recoPtCut+'&&'+l1gPtCut+vetoCut
  rlxVetoLegendStr = 'UCT (4x8, Tau Veto): Rlx'
  h_UCT_rlxVeto=effi_histo(ntuple_rlx,variable,cut_uctRVeto,binning,denom_rlx,
   rlxVetoLegendStr,legend,
   ROOT.EColor.kGreen+4,22,log)
  h_UCT_rlxVeto.SetName('h_UCT_rlxVeto')
  h_UCT_rlxVeto.Write()

# UCT Rlx + Isolation by hand
 if drawUCTIso_byhand_:
  cut_UCT_isoByHand=cutD_rlx+'&&'+l1gPtCut+'&&'+isoCut+vetoCut # && (dr03CombinedEt/recoPt)<0.2'
  h_UCT_isoByHand=effi_histo(ntuple_rlx,variable,cut_UCT_isoByHand,binning,denom_rlx,
  'UCT (4x8): Iso < %0.2f'%(ISOTHRESHOLD),legend,
  #'UCT: Rlx + IsoByHand<%0.1f'%(ISOTHRESHOLD),legend,
  ROOT.EColor.kYellow+3,markerUIbh,log)
  h_UCT_isoByHand.SetName('h_UCT_isoByHand')
  h_UCT_isoByHand.Write()
 if drawPtCmp:
  cut_UCT_Pt30=cutD_rlx+'&&l1gPt[0]>30&&l1gPt[1]>30&&'+isoCut+vetoCut # && (dr03CombinedEt/recoPt)<0.2'
  h_UCT_Pt30=effi_histo(ntuple_rlx,variable,cut_UCT_Pt30,binning,denom_rlx,
  'L1 Pt > 30',legend,
  #'UCT: Rlx + IsoByHand<%0.1f'%(ISOTHRESHOLD),legend,
  ROOT.EColor.kYellow+3,markerUIbh,log)
  h_UCT_Pt30.SetName('h_UCT_Pt30')
  h_UCT_Pt30.Write()
  cut_UCT_Pt40=cutD_rlx+'&&l1gPt[0]>40&&l1gPt[1]>40&&'+isoCut+vetoCut # && (dr03CombinedEt/recoPt)<0.2'
  h_UCT_Pt40=effi_histo(ntuple_rlx,variable,cut_UCT_Pt40,binning,denom_rlx,
  'L1 Pt > 40',legend,
  #'UCT: Rlx + IsoByHand<%0.1f'%(ISOTHRESHOLD),legend,
  ROOT.EColor.kMagenta+3,22,log)
  h_UCT_Pt40.SetName('h_UCT_Pt40')
  h_UCT_Pt40.Write()
  cut_UCT_Pt50=cutD_rlx+'&&l1gPt[0]>50&&l1gPt[1]>50&&'+isoCut+vetoCut # && (dr03CombinedEt/recoPt)<0.2'
  h_UCT_Pt50=effi_histo(ntuple_rlx,variable,cut_UCT_Pt50,binning,denom_rlx,
  'L1 Pt > 50',legend,
  #'UCT: Rlx + IsoByHand<%0.1f'%(ISOTHRESHOLD),legend,
  ROOT.EColor.kBlue+3,24,log)
  h_UCT_Pt50.SetName('h_UCT_Pt50')
  h_UCT_Pt50.Write()


 if drawPtCmpRlx:
  cut_UCT_Pt30=cutD_rlx+'&&l1gPt[0]>30&&l1gPt[1]>30' # && (dr03CombinedEt/recoPt)<0.2'
  h_UCT_Pt30=effi_histo(ntuple_rlx,variable,cut_UCT_Pt30,binning,denom_rlx,
  'L1 Pt (Rlx) > 30',legend,
  #'UCT: Rlx + IsoByHand<%0.1f'%(ISOTHRESHOLD),legend,
  ROOT.EColor.kYellow+3,markerUIbh,log)
  h_UCT_Pt30.SetName('h_UCT_Pt30')
  h_UCT_Pt30.Write()
  cut_UCT_Pt40=cutD_rlx+'&&l1gPt[0]>40&&l1gPt[1]>40'# && (dr03CombinedEt/recoPt)<0.2'
  h_UCT_Pt40=effi_histo(ntuple_rlx,variable,cut_UCT_Pt40,binning,denom_rlx,
  'L1 Pt (Rlx) > 40',legend,
  #'UCT: Rlx + IsoByHand<%0.1f'%(ISOTHRESHOLD),legend,
  ROOT.EColor.kMagenta+3,22,log)
  h_UCT_Pt40.SetName('h_UCT_Pt40')
  h_UCT_Pt40.Write()
  cut_UCT_Pt50=cutD_rlx+'&&l1gPt[0]>50&&l1gPt[1]>50'# && (dr03CombinedEt/recoPt)<0.2'
  h_UCT_Pt50=effi_histo(ntuple_rlx,variable,cut_UCT_Pt50,binning,denom_rlx,
  'L1 Pt (Rlx) > 50',legend,
  #'UCT: Rlx + IsoByHand<%0.1f'%(ISOTHRESHOLD),legend,
  ROOT.EColor.kBlue+3,24,log)
  h_UCT_Pt50.SetName('h_UCT_Pt50')
  h_UCT_Pt50.Write()


# UCT Isolated
 if drawUCTIso_:
  cut_uctI=recoPtCut+'&&'+l1gPtCut+'&&l1gMatch[0]&&l1gMatch[1] '#&& (dr03CombinedEt/recoPt)<0.2'
  h_UCT_iso=effi_histo(ntuple_iso,variable,cut_uctI,binning,denom_iso,
  'UCT (4x8): Iso',legend,
   colorUI,markerUI,log)
  h_UCT_iso.SetName('h_UCT_iso')
  h_UCT_iso.Write()
 if Cmp4x4:
   if TauVetoRlx == False:
        cut_uctR4x4=recoPtCut+'&&'+l1gPtCut+'&&l1gMatch[0]&&l1gMatch[1]'
        rlxLegendStr4x4 = 'UCT (4x4): Rlx (No Tau Veto)'
	print cut_uctR4x4
   else:
        cut_uctR4x4=recoPtCut+'&&'+l1gPtCut+'&&l1gMatch[0]&&l1gMatch[1]'+vetoCut4x4
        rlxLegendStr4x4 = 'UCT (4x4): Rlx'
   if Veto4x4 == False:
        rlxLegendStr4x4 = 'UCT (4x4): Rlx' #don't need to say that we aren't using a tau veto for the 4x4s when it usually is not used

	print cut_uctR4x4
   h_UCT_rlx4x4=effi_histo(ntuple_rlx4x4,variable,cut_uctR4x4,binning,denom_rlx4x4,
    rlxLegendStr4x4,legend,
    ROOT.EColor.kMagenta,22,log)
   h_UCT_rlx4x4.SetName('h_UCT_rlx4x4')
   h_UCT_rlx4x4.Write()

   cut_UCT_isoByHand4x4=recoPtCut+'&&'+l1gPtCut+'&&'+isoCut4x4+'&& l1gMatch[0]&&l1gMatch[1]'+vetoCut4x4 # && (dr03CombinedEt/recoPt)<0.2'
   h_UCT_isoByHand4x4=effi_histo(ntuple_rlx4x4,variable,cut_UCT_isoByHand4x4,binning,denom_rlx4x4,
   'UCT (4x4): Iso < %0.2f'%(ISOTHRESHOLD4x4),legend,
   #'UCT: Rlx + IsoByHand<%0.1f'%(ISOTHRESHOLD),legend,
   ROOT.EColor.kRed,markerUIbh,log)
   h_UCT_isoByHand4x4.SetName('h_UCT_isoByHand4x4')
   h_UCT_isoByHand4x4.Write()

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
'''
binRes=[50,-1,1]
make_res_nrml(
 eff_rlx_eg_ntuple,
 eff_iso_eg_ntuple,
 eff_rlx_eg_ntuple4x4,
 eff_iso_eg_ntuple4x4,
 'recoPt',
 'l1Pt',
 'l1gPt',
 binRes,
 cutPtVarg='l1gPt',
 cutPtVar='l1Pt',
 cutPt=30,
 isoCut='&&((l1gPt>='+str(turnOffIso)+'&& (l1gJetPt-l1gPt)/l1gPt < 100)||(l1gPt < '+str(turnOffIso)+'&&(l1gJetPt-l1gPt)/l1gPt<'+str(ISOTHRESHOLD)+'))',
 isoCut4x4 = '&&((l1gPt>='+str(turnOffIso)+'&& (l1gJetPt-l1gPt)/l1gPt < 100)||(l1gPt < '+str(turnOffIso)+'&&(l1gJetPt-l1gPt)/l1gPt<'+str(ISOTHRESHOLD4x4)+'))',
 filename='')
'''
####################
# Efficiency Plots #
####################
if efficiencyPlots == True:
 #binPt = [10,40,80] #l120
 xBins = array.array('d',[20,25,30,35,40,45,50,55,60,80,100,130,200])
 binPt = [40,0,200]
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
  #'pt[0]:pt[1]',
  "Min(P_{T}1, P_{T}2)",
  binPt,
  eff_rlx_eg_ntuple, eff_iso_eg_ntuple,
  eff_rlx_eg_ntuple4x4, eff_iso_eg_ntuple4x4,
  recoPtCut = '(pt[0] >= '+str(recoPtVal)+')&&(pt[1] >= '+str(recoPtVal)+'&&l1gPt[0] > 0 && l1gPt[1] >= 0)',
  l1PtCut = '(l1Pt[0] >= '+str(l1ptVal)+')&&(l1Pt[1]>= '+str(l1ptVal)+')',
  #l1gPtCut = '(l1gRegionEt >= '+str(l1ptVal)+')',
  l1gPtCut = '(l1gPt[0] >= '+str(l1ptVal)+'&&l1gPt[1] >= '+str(l1ptVal)+')',
  # 12x12-4x4
  #isoCut='(l1gPt>=60||(l1gJetPt-l1gRegionEt)/l1gRegionEt<'+str(ISOTHRESHOLD)+')',
  isoCut = '((l1gPt[0]>='+str(turnOffIso)+'&& (l1gJetPt[0]-l1gPt[0])/l1gPt[0] < 100)||(l1gPt[0] < '+str(turnOffIso)+'&&(l1gJetPt[0]-l1gPt[0])/l1gPt[0]<'+str(ISOTHRESHOLD)+'))&&((l1gPt[1]>='+str(turnOffIso)+'&& (l1gJetPt[1]-l1gPt[1])/l1gPt[1] < 100)||(l1gPt[1] < '+str(turnOffIso)+'&&(l1gJetPt[1]-l1gPt[1])/l1gPt[1]<'+str(ISOTHRESHOLD)+'))',
  isoCut4x4 = '((l1gPt[0]>='+str(turnOffIso)+'&& (l1gJetPt[0]-l1gPt[0])/l1gPt[0] < 100)||(l1gPt[0] < '+str(turnOffIso)+'&&(l1gJetPt[0]-l1gPt[0])/l1gPt[0]<'+str(ISOTHRESHOLD4x4)+'))&&((l1gPt[1]>='+str(turnOffIso)+'&& (l1gJetPt[1]-l1gPt[1])/l1gPt[1] < 100)||(l1gPt[1] < '+str(turnOffIso)+'&&(l1gJetPt[1]-l1gPt[1])/l1gPt[1]<'+str(ISOTHRESHOLD4x4)+'))',
  #extraCut='&&eta[0]>-1.9&&eta[0]<1.9&&eta[1]>-1.9&&eta[1]<1.9',
  extraCut ='',
  # 12x12 - 2x1
  #isoCut='(l1gPt[0]>=60||(l1gJetPt[0]-l1gPt[0])/l1gPt[0]<'+str(ISOTHRESHOLD)+')',
  drawUCTIso_=drawUCTIso,
  drawUCTRlx_=drawUCTRlx,
  drawUCTIso_byhand_=drawUCTIso_byhand,
  drawL1Iso_=drawL1Iso,
  drawL1Rlx_=drawL1Rlx,
  #legExtra = 'Tau 4x4'
 )
 
# compare_efficiencies(
# 'nPVs',
# binVert,
# eff_rlx_eg_ntuple, eff_iso_eg_ntuple,
# recoPtCut = '(recoPt >= '+str(recoPtVal)+')',
# l1PtCut = '(l1Pt >= '+str(l1ptVal)+')',
# l1gPtCut = '(l1gPt >= '+str(l1ptVal)+')',
# isoCut='(l1gPt>=60||(l1gJetPt-l1gPt)/l1gPt<'+str(ISOTHRESHOLD)+')',
# drawUCTIso_=drawUCTIso,
# drawUCTRlx_=drawUCTRlx,
# drawUCTIso_byhand_=drawUCTIso_byhand,
# drawL1Iso_=drawL1Iso,
# drawL1Rlx_=drawL1Rlx,
# legExtra='Reco Pt > '+str(recoPtVal)
#)
