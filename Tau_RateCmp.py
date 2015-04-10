'''
Makes optionally EG efficiency, rate and resolution plots
Authors: T.M.Perry, E.K.Friis, M.Cepeda, A.G.Levine, N.Woods UW Madison
'''
from sys import argv, stdout, stderr
import ROOT

ratePlots = True
# which curves to draw on rate and efficiency plots
drawUCTIso = False
drawUCTRlx_4x4 = False
drawUCTRlx_4x8 = True
drawUCTIso_byhand_4x4 = False
drawUCTIso_byhand_4x8 = True
drawL1Iso = False
drawL1Rlx = False

##################
# Set Parameters #
##################
LIso=3
LSB=50
l1ptVal=40
recoPtVal=0
ISOTHRESHOLD_4x4=0.4
ISOTHRESHOLD_4x8 =0.1
turnOffIso=63
turnOffTauVeto=90
L1_CALIB_FACTOR = 1.0
L1G_CALIB_FACTOR = 1.0
#ZEROBIAS_RATE=15000000.00
ZEROBIAS_RATE = 11246.0*2590.0 #frequency X bunches
saveWhere='plots/SignalBackground'


###################
# Input Arguments #
###################
savedir = argv[1]
doVeto = argv[2]
doEdge = argv[3]
doNeighbors = argv[4]
print doEdge
print doNeighbors
if doEdge == "True" and doNeighbors == "True":
	print "can't do edges and neighbors"
	exit()
saveWhere = savedir
if "ECAL1" in savedir:
	legendStr = " ECAL 1 "
	EThresh = "1"
	fname = "tau_eff_4x8_E1"
        rname = "tau_rate_4x8_E1"
elif "ECAL2" in savedir:
	legendStr = " ECAL 2 "
        EThresh = "2"
        fname = "tau_eff_4x8_E2"
        rname = "tau_rate_4x8_E2"
elif "ECAL3" in savedir:
	legendStr = " ECAL 3 "
        EThresh = "3"
        fname = "tau_eff_4x8_E3"
        rname = "tau_rate_4x8_E3"
elif "ECAL4" in savedir:
	legendStr = " ECAL 4 "
        EThresh = "4"
        fname = "tau_eff_4x8_E4"
        rname = "tau_rate_4x8_E4"
elif "ECAL5" in savedir:
	legendStr = " ECAL 5 "
        EThresh = "5"
        fname = "tau_eff_4x8_E5"
        rname = "tau_rate_4x8_E5"

#rate plot
rateLine = True # line at recoPtVal
binIso = [50,0,1]
#binTauVeto = [36,10,80]
binTauVeto = [46,10,100]

########
# File #
########
#Rate
#rate_ntuple = 'uct_rate_tree.root'
#rate_ntuple_4x4= 'tau_rate_4x4point4iso.root'
#rate_ntuple_4x4 = 'tau_rate_4x4_1point0iso.root'
rate_ntuple_4x4 = 'tau_rate_4x4_Neutrino.root'
#rate_ntuple_4x8 = 'tau_rate_4x8point4iso.root'
#rate_ntuple_4x8 = 'tau_rate_4x8_Neutrino.root'
#rate_ntuple_4x8 = 'tau_rate_4x8_NoExtraTauSeedNeutrinoGun.root'
#rate_ntuple_4x8 = 'tau_rate_4x8_NoExtraTauSeedNeutrinoGun_TauSeed10.root'
#eff_ntuple_4x8 = 'tau_eff_4x8_NoExtraTauSeed.root'
#rate_ntuple_4x8 = 'tau_rate_4x8_Ecal2.root'
#eff_ntuple_4x8 = 'tau_eff_4x8_Ecal2.root'
eff_ntuple_4x8 = 'tau_eff_4x8_Ecal2.root'
rate_ntuple_4x8 = 'tau_rate_4x8_Ecal2.root'
eff_ntuple_4x8_hcal1 = savedir+fname+'H1_NoNeighborSeed.root'
rate_ntuple_4x8_hcal1 = savedir+rname+'H1_NoNeighborSeed.root'
eff_ntuple_4x8_hcal2 = savedir+fname+'H2_NoNeighborSeed.root'
rate_ntuple_4x8_hcal2 = savedir+rname+'H2_NoNeighborSeed.root'
eff_ntuple_4x8_hcal3 = savedir+fname+'H3_NoNeighborSeed.root'
rate_ntuple_4x8_hcal3 = savedir+rname+'H3_NoNeighborSeed.root'
eff_ntuple_4x8_hcal4 = savedir+fname+'H4_NoNeighborSeed.root'
rate_ntuple_4x8_hcal4 = savedir+rname+'H4_NoNeighborSeed.root'
eff_ntuple_4x8_hcal5 = savedir+fname+'H5_NoNeighborSeed.root'
rate_ntuple_4x8_hcal5 = savedir+rname+'H5_NoNeighborSeed.root'
print rate_ntuple_4x8_hcal5
#rate_ntuple_4x8 = 'tau_rate_nodiag.root'
#rate_ntuple_4x8 = 'tau_rate_4x8iso4x4.root'
#rate_ntuple = 'uct_rate_4by8veto.root'
#rate_ntuple = 'uct_rate_4x8iso.root'
rate_ntuple_file_4x4 = ROOT.TFile(rate_ntuple_4x4)
rate_ntuple_file_4x8 = ROOT.TFile(rate_ntuple_4x8)
eff_ntuple_file_4x8 = ROOT.TFile(eff_ntuple_4x8)
rate_ntuple_file_4x8_hcal1 = ROOT.TFile(rate_ntuple_4x8_hcal1)
eff_ntuple_file_4x8_hcal1 = ROOT.TFile(eff_ntuple_4x8_hcal1)
rate_ntuple_file_4x8_hcal2 = ROOT.TFile(rate_ntuple_4x8_hcal2)
eff_ntuple_file_4x8_hcal2 = ROOT.TFile(eff_ntuple_4x8_hcal2)
rate_ntuple_file_4x8_hcal3 = ROOT.TFile(rate_ntuple_4x8_hcal3)
eff_ntuple_file_4x8_hcal3 = ROOT.TFile(eff_ntuple_4x8_hcal3)
rate_ntuple_file_4x8_hcal4 = ROOT.TFile(rate_ntuple_4x8_hcal4)
eff_ntuple_file_4x8_hcal4 = ROOT.TFile(eff_ntuple_4x8_hcal4)
rate_ntuple_file_4x8_hcal5 = ROOT.TFile(rate_ntuple_4x8_hcal5)
eff_ntuple_file_4x8_hcal5 = ROOT.TFile(eff_ntuple_4x8_hcal5)

# UCT
rate_rlx_UCT_spot = 'rlxTauUCTRate/Ntuple'
rate_iso_UCT_spot = 'isoTauUCTRate/Ntuple'
eff_rlx_UCT_spot = 'rlxTauEfficiency/Ntuple'
rate_rlx_UCT_ntuple_4x4 = rate_ntuple_file_4x4.Get(rate_rlx_UCT_spot)
rate_iso_UCT_ntuple_4x4 = rate_ntuple_file_4x4.Get(rate_iso_UCT_spot)
rate_rlx_UCT_ntuple_4x8 = rate_ntuple_file_4x8.Get(rate_rlx_UCT_spot)
rate_iso_UCT_ntuple_4x8 = rate_ntuple_file_4x8.Get(rate_iso_UCT_spot)
eff_rlx_UCT_ntuple_4x8 = eff_ntuple_file_4x8.Get(eff_rlx_UCT_spot)
rate_rlx_hcal1 = rate_ntuple_file_4x8_hcal1.Get(rate_rlx_UCT_spot)
rate_iso_hcal1 = rate_ntuple_file_4x8_hcal1.Get(rate_iso_UCT_spot)
eff_rlx_hcal1 = eff_ntuple_file_4x8_hcal1.Get(eff_rlx_UCT_spot)
rate_rlx_hcal2 = rate_ntuple_file_4x8_hcal1.Get(rate_rlx_UCT_spot)
rate_iso_hcal2 = rate_ntuple_file_4x8_hcal2.Get(rate_iso_UCT_spot)
eff_rlx_hcal2 = eff_ntuple_file_4x8_hcal2.Get(eff_rlx_UCT_spot)
rate_rlx_hcal3 = rate_ntuple_file_4x8_hcal3.Get(rate_rlx_UCT_spot)
rate_iso_hcal3 = rate_ntuple_file_4x8_hcal3.Get(rate_iso_UCT_spot)
eff_rlx_hcal3 = eff_ntuple_file_4x8_hcal3.Get(eff_rlx_UCT_spot)
rate_rlx_hcal4 = rate_ntuple_file_4x8_hcal4.Get(rate_rlx_UCT_spot)
rate_iso_hcal4 = rate_ntuple_file_4x8_hcal4.Get(rate_iso_UCT_spot)
eff_rlx_hcal4 = eff_ntuple_file_4x8_hcal4.Get(eff_rlx_UCT_spot)
rate_rlx_hcal5 = rate_ntuple_file_4x8_hcal5.Get(rate_rlx_UCT_spot)
rate_iso_hcal5 = rate_ntuple_file_4x8_hcal5.Get(rate_iso_UCT_spot)
print "Ntuple Entries: " + str(rate_iso_hcal5.GetEntries())
eff_rlx_hcal5 = eff_ntuple_file_4x8_hcal5.Get(eff_rlx_UCT_spot)
# Current
rate_rlx_L1_spot = 'tauL1Rate/Ntuple'
rate_iso_L1_spot = 'tauL1Rate/Ntuple'
rate_rlx_L1_ntuple = rate_ntuple_file_4x8.Get(rate_rlx_L1_spot)
rate_iso_L1_ntuple = rate_ntuple_file_4x8.Get(rate_iso_L1_spot)

#To Be Made
store = ROOT.TFile(saveWhere+'.root','RECREATE')

name=''
if drawUCTIso or drawUCTRlx_4x4 or drawUCTRlx_4x8 or drawUCTIso_byhand_4x4 or drawUCTIso_byhand_4x8: name+='_UCT_'
if drawUCTRlx_4x4: name+='R4'
if drawUCTRlx_4x8: name+='R8'
if drawUCTIso: name+='I'
if drawUCTIso_byhand_4x4: name+='Ibh4'+str(int(ISOTHRESHOLD_4x4 * 10))
if drawUCTIso_byhand_4x8: name+='Ibh8'+str(int(ISOTHRESHOLD_4x8 * 10))
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
log.write('ISOTHRESHOLD_4x4 = '+str(ISOTHRESHOLD_4x4)+'\n')
log.write('ISOTHRESHOLD_4x8 = '+str(ISOTHRESHOLD_4x8)+'\n')
log.write('L1_CALIB_FACTOR = '+str(L1_CALIB_FACTOR)+'\n')
log.write('L1G_CALIB_FACTOR = '+str(L1G_CALIB_FACTOR)+'\n')
log.write('ZEROBIAS_RATE = '+str(ZEROBIAS_RATE)+'\n\n')

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
colorUI=ROOT.EColor.kBlue
markerUI=21
#colorUIbh=ROOT.EColor.kGreen+3
#colorUIbh=ROOT.EColor.kBlue
colorUIbh=ROOT.EColor.kRed
#colorUIbh=ROOT.EColor.kViolet-7
#colorUIbh=ROOT.EColor.kBlack
markerUIbh=21
colorCI=ROOT.EColor.kRed
markerCI=24
colorCR=ROOT.EColor.kViolet-7
markerCR=20

canvas = ROOT.TCanvas("asdf", "adsf", 800, 800)

def make_plot(tree, variable, selection, binning, xaxis='', title='',calFactor=1):
 ''' Plot a variable using draw and return the histogram '''
 draw_string = "%s * %0.2f>>htemp(%s)" % (variable,calFactor, ", ".join(str(x) for x in binning))
 print draw_string
 print selection
 tree.Draw(draw_string, selection, "goff")
 print tree.GetEntries()
 output_histo = ROOT.gDirectory.Get("htemp").Clone()
 output_histo.GetXaxis().SetTitle(xaxis)
 output_histo.SetTitle(title)
 print output_histo.GetEntries()
 print output_histo.Integral()
 return output_histo


#####################################################################
#####TAUVETO#########################################################
#####################################################################

def make_tauVeto(ntuple_rate1_rlx_4x8,ntuple_eff1_rlx_4x8,ntuple_rate2_rlx_4x8,ntuple_eff2_rlx_4x8,ntuple_rate3_rlx_4x8,ntuple_eff3_rlx_4x8,ntuple_rate4_rlx_4x8,ntuple_eff4_rlx_4x8,ntuple_rate5_rlx_4x8,ntuple_eff5_rlx_4x8,reco,l1,l1g,binning,cutPtVarg='l1gPt',cutPtVar='l1Pt',cutPtQCD = 'pt[0]',cutPt=l1ptVal,filename='',extraCut='',extraCutb='',setLOG=False):
 canvas.SetLogy(setLOG)
 if doEdge == "True":
 	info = 'EdgeVetoIso'+str(reco)+'_'+cutPtVar+''
	#extraCut = extraCut +'&&l1gTauVetoNeighbor==0&&(l1gTauVeto==0||l1gPt > 90)'
	extraCut = extraCut +'&&l1gTauVetoNeighbor==0&&(l1gTauVeto==0)'
	extraCutRate = '&&l1gTauVetoNeighbor[0]==0&&(l1gTauVeto[0]==0)'
	title_str = 'Fraction of Events With TauVeto=0 in Central and Neighbor' + legendStr
 elif doNeighbors == "True":
	info = 'NeighborVetoIso'+str(reco)+'_'+cutPtVar+''
	extraCut = extraCut + '&&l1gTauVetoNeighbor==0'
	extraCutRate = '&&l1gTauVetoNeighbor[0]==0'
	title_str = 'Tau ID efficiency In Highest Neighbor 4x4' + legendStr
 else:
	info = 'TauVetoIso'+str(reco)+'_'+cutPtVar+''
	#extraCut = extraCut+ '&&(l1gTauVeto==0||l1gPt>90)'
	extraCut = extraCut+ '&&(l1gTauVeto==0)'
	extraCutRate = '&&(l1gTauVeto[0]==0)'
	title_str = 'Tau ID efficiency In Central 4x4' + legendStr

 l1gplot_rate1_rlx_4x8 = make_plot(
  ntuple_rate1_rlx_4x8,'pt[0]' ,
  ''+cutPtQCD+'>'+str(cutPt)+extraCutRate+'&&eta[0] > -2.5 && eta[0] < 2.5'+'&&(( pt[0]>=63 && (jetPt[0]-pt[0])/pt[0]<100)||(pt[0]<63&&(jetPt[0]-pt[0])/pt[0]<'+str(ISOTHRESHOLD_4x8)+'))',binning
 )
 l1gplot_eff1_rlx_4x8 = make_plot(
  ntuple_eff1_rlx_4x8, '('+str(L1G_CALIB_FACTOR)+' * '+str(l1g)+')',
  ''+cutPtVarg+'>'+str(cutPt)+extraCut+'&&(l1gPt>=60||(l1gJetPt-l1gPt)/l1gPt<'+str(ISOTHRESHOLD_4x8)+')',binning
 )
 l1gplot_rate1_tauVetodenom_rlx_4x8 = make_plot(
  ntuple_rate1_rlx_4x8,'pt[0]' ,
  ''+cutPtQCD+'>'+str(cutPt)+'&&eta[0] > -2.5 && eta[0] < 2.5',binning
 )
 l1gplot_eff1_tauVetodenom_rlx_4x8 = make_plot(
  ntuple_eff1_rlx_4x8, '('+str(L1G_CALIB_FACTOR)+' * '+str(l1g)+')',
  ''+cutPtVarg+'>'+str(cutPt)+'',binning
 )
 l1gplot_rate2_rlx_4x8 = make_plot(
  ntuple_rate2_rlx_4x8,'pt[0]' ,
  ''+cutPtQCD+'>'+str(cutPt)+extraCutRate+'&&eta[0] > -2.5 && eta[0] < 2.5'+'&&(( pt[0]>=63 && (jetPt[0]-pt[0])/pt[0]<100)||(pt[0]<63&&(jetPt[0]-pt[0])/pt[0]<'+str(ISOTHRESHOLD_4x8)+'))',binning
 )
 l1gplot_eff2_rlx_4x8 = make_plot(
  ntuple_eff2_rlx_4x8, '('+str(L1G_CALIB_FACTOR)+' * '+str(l1g)+')',
  ''+cutPtVarg+'>'+str(cutPt)+extraCut+'&&(l1gPt>=60||(l1gJetPt-l1gPt)/l1gPt<'+str(ISOTHRESHOLD_4x8)+')',binning
 )
 l1gplot_rate2_tauVetodenom_rlx_4x8 = make_plot(
  ntuple_rate2_rlx_4x8,'pt[0]' ,
  ''+cutPtQCD+'>'+str(cutPt)+'&&eta[0] > -2.5 && eta[0] < 2.5',binning
 )
 l1gplot_eff2_tauVetodenom_rlx_4x8 = make_plot(
  ntuple_eff2_rlx_4x8, '('+str(L1G_CALIB_FACTOR)+' * '+str(l1g)+')',
  ''+cutPtVarg+'>'+str(cutPt)+'',binning
 )
 l1gplot_rate3_rlx_4x8 = make_plot(
  ntuple_rate3_rlx_4x8,'pt[0]' ,
  ''+cutPtQCD+'>'+str(cutPt)+extraCutRate+'&&eta[0] > -2.5 && eta[0] < 2.5'+'&&(( pt[0]>=63 && (jetPt[0]-pt[0])/pt[0]<100)||(pt[0]<63&&(jetPt[0]-pt[0])/pt[0]<'+str(ISOTHRESHOLD_4x8)+'))',binning
 )
 l1gplot_eff3_rlx_4x8 = make_plot(
  ntuple_eff3_rlx_4x8, '('+str(L1G_CALIB_FACTOR)+' * '+str(l1g)+')',
  ''+cutPtVarg+'>'+str(cutPt)+extraCut+'&&(l1gPt>=60||(l1gJetPt-l1gPt)/l1gPt<'+str(ISOTHRESHOLD_4x8)+')',binning
 )
 l1gplot_rate3_tauVetodenom_rlx_4x8 = make_plot(
  ntuple_rate3_rlx_4x8,'pt[0]' ,
  ''+cutPtQCD+'>'+str(cutPt)+'&&eta[0] > -2.5 && eta[0] < 2.5',binning
 )

 l1gplot_eff3_tauVetodenom_rlx_4x8 = make_plot(
  ntuple_eff3_rlx_4x8, '('+str(L1G_CALIB_FACTOR)+' * '+str(l1g)+')',
  ''+cutPtVarg+'>'+str(cutPt)+'',binning
 )
 l1gplot_rate4_rlx_4x8 = make_plot(
  ntuple_rate4_rlx_4x8,'pt[0]' ,
  ''+cutPtQCD+'>'+str(cutPt)+extraCutRate+'&&eta[0] > -2.5 && eta[0] < 2.5'+'&&(( pt[0]>=63 && (jetPt[0]-pt[0])/pt[0]<100)||(pt[0]<63&&(jetPt[0]-pt[0])/pt[0]<'+str(ISOTHRESHOLD_4x8)+'))',binning
 )
 l1gplot_eff4_rlx_4x8 = make_plot(
  ntuple_eff4_rlx_4x8, '('+str(L1G_CALIB_FACTOR)+' * '+str(l1g)+')',
  ''+cutPtVarg+'>'+str(cutPt)+extraCut+'&&(l1gPt>=60||(l1gJetPt-l1gPt)/l1gPt<'+str(ISOTHRESHOLD_4x8)+')',binning
 )
 l1gplot_rate4_tauVetodenom_rlx_4x8 = make_plot(
  ntuple_rate4_rlx_4x8,'pt[0]' ,
  ''+cutPtQCD+'>'+str(cutPt)+'&&eta[0] > -2.5 && eta[0] < 2.5',binning
 )
 l1gplot_eff4_tauVetodenom_rlx_4x8 = make_plot(
  ntuple_eff4_rlx_4x8, '('+str(L1G_CALIB_FACTOR)+' * '+str(l1g)+')',
  ''+cutPtVarg+'>'+str(cutPt)+'',binning
 )
 l1gplot_rate5_rlx_4x8 = make_plot(
  ntuple_rate5_rlx_4x8,'pt[0]' ,
  ''+cutPtQCD+'>'+str(cutPt)+extraCutRate+'&&eta[0] > -2.5 && eta[0] < 2.5'+'&&(( pt[0]>=63 && (jetPt[0]-pt[0])/pt[0]<100)||(pt[0]<63&&(jetPt[0]-pt[0])/pt[0]<'+str(ISOTHRESHOLD_4x8)+'))',binning
 )
 l1gplot_eff5_rlx_4x8 = make_plot(
  ntuple_eff5_rlx_4x8, '('+str(L1G_CALIB_FACTOR)+' * '+str(l1g)+')',
  ''+cutPtVarg+'>'+str(cutPt)+extraCut+'&&(l1gPt>=60||(l1gJetPt-l1gPt)/l1gPt<'+str(ISOTHRESHOLD_4x8)+')',binning
 )
 l1gplot_rate5_tauVetodenom_rlx_4x8 = make_plot(
  ntuple_rate5_rlx_4x8,'pt[0]' ,
  ''+cutPtQCD+'>'+str(cutPt)+'&&eta[0] > -2.5 && eta[0] < 2.5',binning
 )
 l1gplot_eff5_tauVetodenom_rlx_4x8 = make_plot(
  ntuple_eff5_rlx_4x8, '('+str(L1G_CALIB_FACTOR)+' * '+str(l1g)+')',
  ''+cutPtVarg+'>'+str(cutPt)+'',binning
 )

 print "HCAL 3 num integral: " + str(l1gplot_rate3_rlx_4x8.Integral())
 print "HCAL 3 denom integral: " + str(l1gplot_rate3_tauVetodenom_rlx_4x8.Integral())
 l1gplot_rate1_rlx_4x8.Divide(l1gplot_rate1_tauVetodenom_rlx_4x8)
 l1gplot_eff1_rlx_4x8.Divide(l1gplot_eff1_tauVetodenom_rlx_4x8)
 l1gplot_rate2_rlx_4x8.Divide(l1gplot_rate2_tauVetodenom_rlx_4x8)
 l1gplot_eff2_rlx_4x8.Divide(l1gplot_eff2_tauVetodenom_rlx_4x8)
 l1gplot_rate3_rlx_4x8.Divide(l1gplot_rate3_tauVetodenom_rlx_4x8)
 l1gplot_eff3_rlx_4x8.Divide(l1gplot_eff3_tauVetodenom_rlx_4x8)
 l1gplot_rate4_rlx_4x8.Divide(l1gplot_rate4_tauVetodenom_rlx_4x8)
 l1gplot_eff4_rlx_4x8.Divide(l1gplot_eff4_tauVetodenom_rlx_4x8)
 l1gplot_rate5_rlx_4x8.Divide(l1gplot_rate5_tauVetodenom_rlx_4x8)
 l1gplot_eff5_rlx_4x8.Divide(l1gplot_eff5_tauVetodenom_rlx_4x8)

 #l1gplot_iso_4x4 = make_plot(
 # ntuple_iso_4x4, '('+str(L1G_CALIB_FACTOR)+'*l1gJetPt - ('+str(L1G_CALIB_FACTOR)+' * '+str(l1g)+'))/('+str(L1G_CALIB_FACTOR)+' * '+str(l1g)+')',
 # ''+cutPtVarg+'>'+str(cutPt)+extraCut,binning
 #)
 #l1gplot_iso_4x8 = make_plot(
 # ntuple_iso_4x8, '('+str(L1G_CALIB_FACTOR)+'*l1gJetPt - ('+str(L1G_CALIB_FACTOR)+' * '+str(l1g)+'))/('+str(L1G_CALIB_FACTOR)+' * '+str(l1g)+')',
 # ''+cutPtVarg+'>'+str(cutPt)+extraCut,binning
 #)

 #l1gplot_rate_rlx_4x8.SetTitle('Fraction of Events Passing TauVeto')
 #l1gplot_rate_rlx_4x8.GetXaxis().SetTitle('Region Et')
 
 l1gplot_eff1_rlx_4x8.SetTitle(title_str)
 l1gplot_eff1_rlx_4x8.GetXaxis().SetTitle('4x8 Et')
  
 l1gplot_rate1_rlx_4x8.SetLineColor(ROOT.EColor.kBlue+3)
 l1gplot_rate1_rlx_4x8.SetLineWidth(3)
 l1gplot_rate1_rlx_4x8.SetLineStyle(ROOT.kDashed)
 l1gplot_rate2_rlx_4x8.SetLineColor(ROOT.EColor.kMagenta+3)
 l1gplot_rate2_rlx_4x8.SetLineWidth(3)
 l1gplot_rate2_rlx_4x8.SetLineStyle(ROOT.kDashed)
 l1gplot_rate3_rlx_4x8.SetLineColor(ROOT.EColor.kGreen+3)
 l1gplot_rate3_rlx_4x8.SetLineWidth(3)
 l1gplot_rate3_rlx_4x8.SetLineStyle(ROOT.kDashed)
 l1gplot_rate4_rlx_4x8.SetLineColor(ROOT.EColor.kRed+3)
 l1gplot_rate4_rlx_4x8.SetLineWidth(3)
 l1gplot_rate4_rlx_4x8.SetLineStyle(ROOT.kDashed)
 l1gplot_rate5_rlx_4x8.SetLineColor(ROOT.EColor.kOrange+3)
 l1gplot_rate5_rlx_4x8.SetLineWidth(3)
 l1gplot_rate5_rlx_4x8.SetLineStyle(ROOT.kDashed)
 l1gplot_eff1_rlx_4x8.SetLineColor(ROOT.EColor.kBlue-3)
 l1gplot_eff1_rlx_4x8.SetLineWidth(3)
 l1gplot_eff2_rlx_4x8.SetLineColor(ROOT.EColor.kMagenta-3)
 l1gplot_eff2_rlx_4x8.SetLineWidth(3)
 l1gplot_eff3_rlx_4x8.SetLineColor(ROOT.EColor.kGreen-3)
 l1gplot_eff3_rlx_4x8.SetLineWidth(3)
 l1gplot_eff4_rlx_4x8.SetLineColor(ROOT.EColor.kRed-3)
 l1gplot_eff4_rlx_4x8.SetLineWidth(3)
 l1gplot_eff5_rlx_4x8.SetLineColor(ROOT.EColor.kOrange-3)
 l1gplot_eff5_rlx_4x8.SetLineWidth(3)

 legend = ROOT.TLegend(0.15,0.25,0.35,0.85,'','brNDC')
 legend.SetFillColor(ROOT.EColor.kWhite)
 legend.SetBorderSize(0)
 legend.SetTextSize(0.025)
 legend.AddEntry(l1gplot_rate1_rlx_4x8,'QCD HCAL 1')
 legend.AddEntry(l1gplot_eff1_rlx_4x8,'Signal HCAL 1')
 legend.AddEntry(l1gplot_rate2_rlx_4x8,'QCD HCAL 2')
 legend.AddEntry(l1gplot_eff2_rlx_4x8,'Signal HCAL 2')
 legend.AddEntry(l1gplot_rate3_rlx_4x8,'QCD HCAL 3')
 legend.AddEntry(l1gplot_eff3_rlx_4x8,'Signal HCAL 3')
 legend.AddEntry(l1gplot_rate4_rlx_4x8,'QCD HCAL 4')
 legend.AddEntry(l1gplot_eff4_rlx_4x8,'Signal HCAL 4')
 legend.AddEntry(l1gplot_rate5_rlx_4x8,'QCD HCAL 5')
 legend.AddEntry(l1gplot_eff5_rlx_4x8,'Signal HCAL 5')
 #legend.AddEntry(l1gplot_iso_4x4,'4x4 UCT: Iso <%0.1f'%(ISOTHRESHOLD_4x4))
 #legend.AddEntry(l1gplot_iso_4x8,'4x8 UCT: Iso <%0.1f'%(ISOTHRESHOLD_4x8))
  
 #legend.AddEntry(l1bplot,'Stage 1B upgrade')
 #l1gplot_rate_rlx_4x8.Scale(1/l1gplot_rate_rlx_4x8.Integral())
 #l1gplot_eff_rlx_4x8.Scale(1/l1gplot_eff_rlx_4x8.Integral())
 #l1gplot_iso_4x4.Scale(1/l1gplot_iso_4x4.Integral())
 #l1gplot_iso_4x8.Scale(1/l1gplot_iso_4x8.Integral())
 l1gplot_eff1_rlx_4x8.SetMaximum(1.0)
 l1gplot_eff1_rlx_4x8.Draw()
 l1gplot_rate1_rlx_4x8.Draw("sames")
 l1gplot_eff2_rlx_4x8.Draw("sames")
 l1gplot_rate2_rlx_4x8.Draw("sames")
 l1gplot_eff3_rlx_4x8.Draw("sames")
 l1gplot_rate3_rlx_4x8.Draw("sames")
 l1gplot_eff4_rlx_4x8.Draw("sames")
 l1gplot_rate4_rlx_4x8.Draw("sames")
 l1gplot_eff5_rlx_4x8.Draw("sames")
 l1gplot_rate5_rlx_4x8.Draw("sames")
 legend.Draw("sames")
 canvas.SaveAs(saveWhere+info+filename+'.png')


#####################################################################
#####ISOLATION#######################################################
#####################################################################

def make_iso_nrml(ntuple_rlx_4x4,ntuple_rlx_4x8,reco,l1,l1g,binning,cutPtVarg='l1gPt',cutPtVar='l1Pt',cutPt=l1ptVal,filename='',extraCut='',extraCutb='',setLOG=False):
 canvas.SetLogy(setLOG)
 info = 'ISO_SignalvBackground'+str(reco)+'_'+cutPtVar+'Cut'

 #l1gplot_rlx_4x4 = make_plot(
 # ntuple_rlx_4x4, '((jetPt[0] - regionPt[0])/regionPt[0])','regionPt[0]>'+str(cutPt)+extraCut,binning
 #)
 l1gplot_rlx_4x4 = make_plot(
  ntuple_rlx_4x4, '((jetPt[0] - pt[0])/pt[0])','pt[0]>'+str(cutPt)+extraCut,binning
 )


 l1gplot_rlx_4x8 = make_plot(
  ntuple_rlx_4x8, '('+str(L1G_CALIB_FACTOR)+'*l1gJetPt - ('+str(L1G_CALIB_FACTOR)+' * '+str(l1g)+'))/('+str(L1G_CALIB_FACTOR)+' * '+str(l1g)+')',
  ''+cutPtVarg+'>'+str(cutPt)+extraCut,binning
 )

 #l1gplot_iso_4x4 = make_plot(
 # ntuple_iso_4x4, '('+str(L1G_CALIB_FACTOR)+'*l1gJetPt - ('+str(L1G_CALIB_FACTOR)+' * '+str(l1g)+'))/('+str(L1G_CALIB_FACTOR)+' * '+str(l1g)+')',
 # ''+cutPtVarg+'>'+str(cutPt)+extraCut,binning
 #)
 #l1gplot_iso_4x8 = make_plot(
 # ntuple_iso_4x8, '('+str(L1G_CALIB_FACTOR)+'*l1gJetPt - ('+str(L1G_CALIB_FACTOR)+' * '+str(l1g)+'))/('+str(L1G_CALIB_FACTOR)+' * '+str(l1g)+')',
 # ''+cutPtVarg+'>'+str(cutPt)+extraCut,binning
 #)

 l1gplot_rlx_4x4.SetTitle('Isolation')
 l1gplot_rlx_4x4.GetXaxis().SetTitle('Isolation')
 l1gplot_rlx_4x4.SetLineColor(ROOT.EColor.kBlue)

 legend = ROOT.TLegend(0.4,0.4,0.89,0.89,'','brNDC')
 legend.SetFillColor(ROOT.EColor.kWhite)
 legend.SetBorderSize(0)
 legend.AddEntry(l1gplot_rlx_4x4,'4x8 UCT: QCD Rlx')
 #legend.AddEntry(l1gplot_rlx_4x4,'4x8 UCT: TTbar Rlx') #changed to do a quick comparison between relaxed signal and background
 legend.AddEntry(l1gplot_rlx_4x8,'4x8 UCT: Signal Rlx')
 #legend.AddEntry(l1gplot_iso_4x4,'4x4 UCT: Iso <%0.1f'%(ISOTHRESHOLD_4x4))
 #legend.AddEntry(l1gplot_iso_4x8,'4x8 UCT: Iso <%0.1f'%(ISOTHRESHOLD_4x8))
  
 #legend.AddEntry(l1bplot,'Stage 1B upgrade')
 l1gplot_rlx_4x4.SetLineColor(ROOT.EColor.kGreen+3)
 l1gplot_rlx_4x4.SetLineWidth(3)
 l1gplot_rlx_4x8.SetLineColor(ROOT.EColor.kMagenta+2)
 l1gplot_rlx_4x8.SetLineWidth(3)
 l1gplot_rlx_4x8.SetLineWidth(3)
 l1gplot_rlx_4x4.Scale(1/l1gplot_rlx_4x4.Integral())
 l1gplot_rlx_4x8.Scale(1/l1gplot_rlx_4x8.Integral())
 #l1gplot_iso_4x4.Scale(1/l1gplot_iso_4x4.Integral())
 #l1gplot_iso_4x8.Scale(1/l1gplot_iso_4x8.Integral())
 l1gplot_rlx_4x4.SetMaximum(0.5)
 l1gplot_rlx_4x4.Draw()
 l1gplot_rlx_4x8.Draw("sames")
 legend.Draw("sames")
 canvas.SaveAs(saveWhere+info+filename+'.png')

######################################################################
##### RATES ##########################################################
######################################################################
def make_l1_rate(pt, color=ROOT.EColor.kBlack, marker=20):
 ''' Make a rate plot out of L1Extra Pts '''
 numBins = pt.GetXaxis().GetNbins()
 rate = pt.Clone()
 print "entries: " + str(pt.GetEntries())
 for i in range(1,numBins):
  print pt.Integral(i,numBins)
  rate.SetBinContent(i,pt.Integral(i,numBins))
 rate.SetLineColor(color)
 rate.SetMarkerStyle(marker)
 rate.SetMarkerColor(color)
 return rate

def rate_histo(ntuple,cut,binning,calibfactor,scale,color,marker,leg,title,logg,line,ptLine,w,s):
 print "rate_histo info"
 print ntuple.GetEntries()
 print cut
 print binning
 print calibfactor
 #pt = make_plot(ntuple,'regionPt[0]',cut,binning,'','',calibfactor)
 pt = make_plot(ntuple,'pt[0]',cut,binning,'','',calibfactor)
 print "ptEntries: " + str(pt.GetEntries())
 rate = make_l1_rate(pt,color,marker)
 rate.Scale(scale)
 rate.Draw('phsame')
 print rate.Integral()
 leg.AddEntry(rate,title,'pe')
 maxx = rate.GetMaximum()
 print maxx
 print leg
 binn = rate.GetXaxis().FindBin(ptLine)
 rateVal = rate.GetBinContent(binn)
 vert=None
 hor=None
 if line==True:
  vert=ROOT.TLine(ptLine,0,ptLine,rateVal)
  vert.SetLineWidth(w)
  vert.SetLineStyle(s)
  hor=ROOT.TLine(binning[1],rateVal,ptLine,rateVal)
  hor.SetLineWidth(w)
  hor.SetLineStyle(s)
  vert.Draw()
  hor.Draw()
 logg.write('---------------------------------\n')
 logg.write(title+'\n\n')
 logg.write('Tree: '+ntuple.GetDirectory().GetName()+'\n\n')
 logg.write('Cut: '+cut+'\n\n')
 logg.write('At pT = '+str(ptLine)+', Rate = '+str(rateVal)+'\n\n')
 return rate,maxx,vert,hor,rateVal

def make_rate_plot(
 binning,
 ntuple_UCT_rlx_4x4=None,
 ntuple_UCT_iso_4x4=None,
 ntuple_UCT_rlx_4x8=None,
 ntuple_UCT_iso_4x8=None,
 ntuple_L1_rlx =None,
 ntuple_L1_iso =None,
 filename='',
 setLOG=False,
 isoCut_4x4='(2>1)',isoCut_4x8='(2>1)',extraCut='(2>1)',
 drawUCTIso_=False,
 drawUCTRlx_4x4=False,
 drawUCTIso_byhand_4x4=False,
 drawUCTRlx_4x8=False,
 drawUCTIso_byhand_4x8=False,
 drawL1Iso_=False,
 drawL1Rlx_=False,
 line=False,
 ptLine=20,
 HThresh = '',
 ):

 info = 'Rate_ECAL'+str(EThresh)+'_HCAL'+str(HThresh)+'_TauVetoOffAbove'+str(turnOffTauVeto)+'_OffIso'+str(turnOffIso)+'_'
 #scale_4x4 = ZEROBIAS_RATE/ntuple_UCT_rlx_4x4.GetEntries()
 scale_4x8 = ZEROBIAS_RATE/ntuple_UCT_rlx_4x8.GetEntries()
 print "scale" + str(scale_4x8)
 print(ntuple_UCT_rlx_4x8.GetEntries())
 print(ntuple_UCT_iso_4x8.GetEntries())
 #print(ntuple_L1_rlx.GetEntries())
 #print(ntuple_L1_iso.GetEntries())
 
 canvas.SetLogy(setLOG)
 frame = ROOT.TH1F('frame','frame',*binning)
 frame.Draw()
 frame.SetTitle('')
 frame.GetYaxis().SetTitle('Hz (13TeV,1.4E34)')
 frame.GetXaxis().SetTitle('p_{T}')
 tex.DrawLatex(0.1,0.91,'Tau Rate')
 tex.SetTextSize(0.03)
 tex.SetTextAlign(31)
 tex.DrawLatex(0.9,0.91,'CMS Preliminary')
 tex.DrawLatex(0.5,0.87,'ECAL: '+EThresh+' HCAL: '+str(HThresh))
 tex.SetTextSize(0.07)
 tex.SetTextAlign(11)
 legend = ROOT.TLegend(0.53,0.7,0.89,0.89,'','brNDC')
 legend.SetTextSize(0.03)
 legend.SetFillColor(0)
 legend.SetBorderSize(0)
 #legend.SetHeader("Tau Rate")

 # line (a=width b=style)
 aUR=3
 bUR=3
 aUI=3
 bUI=3
 aUIbh=3
 bUIbh=3
 aCR=3
 bCR=3
 aCI=3
 bCI=3

 log.write('________________\n')
 log.write('----- Rate -----\n\n')
 log.write('File : '+rate_ntuple_4x8+'\n')

 max_UCT_rlx=1
 max_UCT_iso=1
 max_UCT_isoByHand=1
 max_L1_rlx=1
 max_L1_iso=1
# Current Relaxed
 if drawL1Rlx_:
  cut_L1_rlx=extraCut
  h_L1_rlx,max_L1_rlx,vert_L1_rlx,hor_L1_rlx = rate_histo(
   ntuple_L1_rlx,cut_L1_rlx,binning,L1G_CALIB_FACTOR,
   scale_4x4,colorCR,markerCR,legend,
   'L1: Rlx',
   log,line,ptLine,aCR,bCR)
# Current Isolated
 if drawL1Iso_:
  cut_L1_iso=extraCut
  h_L1_iso,max_L1_iso,vert_L1_iso,hor_L1_iso = rate_histo(
   ntuple_L1_iso,cut_L1_iso,binning,L1G_CALIB_FACTOR,
   scale_4x4,colorCI,markerCI,legend,
   'L1: Iso',
   log,line,ptLine,aCI,bCI)
# UCT Relaxed
 if drawUCTRlx_4x4:
  cut_UCT_rlx=extraCut
  h_UCT_rlx_4x4,max_UCT_rlx_4x4,vert_UCT_rlx_4x4,hor_UCT_rlx_4x4 = rate_histo(
   ntuple_UCT_rlx_4x4,cut_UCT_rlx,binning,L1G_CALIB_FACTOR,
   scale_4x4,colorUR,markerUR,legend,
   '4x4 UCT: Rlx',
   log,line,ptLine,aUR,bUR)
 if drawUCTRlx_4x8:
  cut_UCT_rlx=extraCut
  h_UCT_rlx,max_UCT_rlx,vert_UCT_rlx,hor_UCT_rlx,uctrlxRateVal = rate_histo(
   ntuple_UCT_rlx_4x8,cut_UCT_rlx,binning,L1G_CALIB_FACTOR,
   scale_4x8,(ROOT.EColor.kMagenta+2),markerUR,legend,
   '4x8 UCT: Rlx',
   log,line,ptLine,aUR,bUR)
# UCT Rlx + Isolation by hand
 if drawUCTIso_byhand_4x4:
  cut_UCT_isoByHand=isoCut_4x4+'&&'+extraCut
  print(cut_UCT_isoByHand)
  h_UCT_isoByHand_4x4,max_UCT_isoByHand_4x4,vert_UCT_isoByHand_4x4,hor_UCT_isoByHand_4x4 = rate_histo(
   ntuple_UCT_iso_4x4,cut_UCT_isoByHand,binning,L1G_CALIB_FACTOR,
   scale_4x4,colorUIbh,markerUIbh,legend,
   '4x4 UCT: Iso < %0.1f'%(ISOTHRESHOLD_4x4),
   #'UCT: Rlx + IsoByHand<%0.1f'%(ISOTHRESHOLD),
   log,line,ptLine,aUIbh,bUIbh)
 if drawUCTIso_byhand_4x8:
  cut_UCT_isoByHand=isoCut_4x8+'&&'+extraCut
  print(cut_UCT_isoByHand)
  h_UCT_isoByHand,max_UCT_isoByHand,vert_UCT_isoByHand,hor_UCT_isoByHand,uctibhRateVal = rate_histo(
   ntuple_UCT_rlx_4x8,cut_UCT_isoByHand,binning,L1G_CALIB_FACTOR,
   scale_4x8,(ROOT.EColor.kOrange+2),markerUIbh,legend,
   '4x8 UCT: Iso < %0.1f '%(ISOTHRESHOLD_4x8),
   log,line,ptLine,aUIbh,bUIbh)
# UCT Isolated
 if drawUCTIso_:
  cut_UCT_iso=extraCut
  h_UCT_iso,max_UCT_iso,vert_UCT_iso,hor_UCT_iso = rate_histo(
   ntuple_UCT_iso,cut_UCT_iso,binning,L1G_CALIB_FACTOR,
   scale_4x4,colorUI,markerUI,legend,
   'UCT: Iso',
   log,line,ptLine,aUI,bUI)
 frame.SetMaximum(3E7)
 #frame.SetMaximum(5*max(max_UCT_rlx,max_UCT_iso,max_UCT_isoByHand,max_L1_rlx,max_L1_iso))
 frame.SetMinimum(1E3)
 legend.Draw()
 latex = ROOT.TLatex()
 latex.SetNDC()
 latex.SetTextSize(0.03)
 latex.SetTextAlign(31)
 latexStrRlx = "Rlx Rate:  %.2f kHz "%(uctrlxRateVal/1000)
 latexStrIso = "Iso Rate:  %.2f kHz "%(uctibhRateVal/1000)
 latex.DrawLatex(0.75,0.65,latexStrRlx)
 latex.DrawLatex(0.75,0.6, latexStrIso)
 #save=raw_input("Type save to save as "+saveWhere+name+info+'.png (enter to continue)\n')
 print "segfault?"
 #if save=="save": 
 canvas.SaveAs(saveWhere+name+info+'.png')
 print "segfault?"
 #canvas.SaveAs(saveWhere+name+info+'.png')
######################################################################
##### RATES ##########################################################
######################################################################

######################################################################
###### DRAW PLOTS ####################################################
######################################################################
##############
# Rate Plots #
##############
if ratePlots == True:
 binRate = [36,0,80]

# binning,
# ntuple_UCT_rlx=None,
# ntuple_UCT_iso=None,
# ntuple_L1_rlx =None,
# ntuple_L1_iso =None,
# filename='',
# setLOG=True,
# isoCut='(2>1)',extraCut='(2>1)',
# drawUCTIso_=False,
# drawUCTRlx_=False,
# drawUCTIso_byhand_=False,
# drawL1Iso_=False,
# drawL1Rlx_=False,
# line=False
# ptLine=20,
 #make_iso_nrml(rate_rlx_UCT_ntuple_4x8,eff_rlx_UCT_ntuple_4x8,'recoPt', 'l1Pt', 'l1gPt', binIso, cutPtVarg='l1gPt',cutPtVar='l1Pt',cutPt=l1ptVal,filename='')
 if doNeighbors == "True" or doVeto == "True" or doEdge == "True":
   make_tauVeto(rate_rlx_hcal1,eff_rlx_hcal1,rate_rlx_hcal2,eff_rlx_hcal2,rate_rlx_hcal3,eff_rlx_hcal3,rate_rlx_hcal4,eff_rlx_hcal4,rate_rlx_hcal5,eff_rlx_hcal5,'recoPt', 'l1Pt', 'l1gPt', binTauVeto, cutPtVarg='l1gPt',cutPtVar='l1Pt',cutPtQCD = 'pt[0]',cutPt=l1ptVal,filename='')
 else: 
   make_rate_plot(
   binRate,
   ntuple_UCT_rlx_4x4=rate_rlx_UCT_ntuple_4x4,
   ntuple_UCT_iso_4x4=rate_iso_UCT_ntuple_4x4,
   ntuple_UCT_rlx_4x8=rate_rlx_hcal1,
   ntuple_UCT_iso_4x8=rate_iso_hcal1,
   ntuple_L1_rlx =rate_rlx_L1_ntuple,
   ntuple_L1_iso =rate_iso_L1_ntuple,
   filename='',
   setLOG=True,
   # 12x12 - 4x4 (I think)
   isoCut_4x4='(( pt[0]>=63 && (jetPt[0]-regionPt[0])/regionPt[0]<100)||(pt[0]<63&&(jetPt[0]-regionPt[0])/regionPt[0]<'+str(ISOTHRESHOLD_4x4)+'))',
   #isoCut_4x8='(( pt[0]>=63 && (jetPt[0]-regionPt[0])/regionPt[0]<100)||(pt[0]<63&&(jetPt[0]-regionPt[0])/regionPt[0]<'+str(ISOTHRESHOLD_4x8)+'))',
   isoCut_4x8='(( pt[0]>=90 && (jetPt[0]-pt[0])/pt[0]<100)||(pt[0]<90&&(jetPt[0]-pt[0])/pt[0]<'+str(ISOTHRESHOLD_4x8)+'))',
   # old thing 12x12 - 2x1 before 63
   #isoCut='(( pt[0]>=63 && (jetPt[0]-regionPt[0])/regionPt[0]<100)||(pt[0]<63&&(jetPt[0]-pt[0])/pt[0]<'+str(ISOTHRESHOLD)+'))',
   extraCut='(eta[0] > -2.5 && eta[0] < 2.5 && l1gTauVeto[0] == 0)',
   drawUCTIso_=drawUCTIso,
   drawUCTRlx_4x4=False,
   drawUCTIso_byhand_4x4=False,
   drawUCTRlx_4x8=True,
   drawUCTIso_byhand_4x8=True,
   drawL1Iso_=drawL1Iso,
   drawL1Rlx_=drawL1Rlx,
   line=rateLine,
   ptLine=l1ptVal,
   HThresh = 1
   )
   make_rate_plot(
   binRate,
   ntuple_UCT_rlx_4x4=rate_rlx_UCT_ntuple_4x4,
   ntuple_UCT_iso_4x4=rate_iso_UCT_ntuple_4x4,
   ntuple_UCT_rlx_4x8=rate_rlx_hcal2,
   ntuple_UCT_iso_4x8=rate_iso_hcal2,
   ntuple_L1_rlx =rate_rlx_L1_ntuple,
   ntuple_L1_iso =rate_iso_L1_ntuple,
   filename='',
   setLOG=True,
   # 12x12 - 4x4 (I think)
   isoCut_4x4='(( pt[0]>=63 && (jetPt[0]-regionPt[0])/regionPt[0]<100)||(pt[0]<63&&(jetPt[0]-regionPt[0])/regionPt[0]<'+str(ISOTHRESHOLD_4x4)+'))',
   #isoCut_4x8='(( pt[0]>=90 && (jetPt[0]-regionPt[0])/regionPt[0]<100)||(pt[0]<63&&(jetPt[0]-regionPt[0])/regionPt[0]<'+str(ISOTHRESHOLD_4x8)+'))',
   isoCut_4x8='(( pt[0]>=90 && (jetPt[0]-pt[0])/pt[0]<100)||(pt[0]<90&&(jetPt[0]-pt[0])/pt[0]<'+str(ISOTHRESHOLD_4x8)+'))',
   # old thing 12x12 - 2x1 before 63
   #isoCut='(( pt[0]>=63 && (jetPt[0]-regionPt[0])/regionPt[0]<100)||(pt[0]<63&&(jetPt[0]-pt[0])/pt[0]<'+str(ISOTHRESHOLD)+'))',
   extraCut='(eta[0] > -2.5 && eta[0] < 2.5 && l1gTauVeto[0] == 0)',
   drawUCTIso_=drawUCTIso,
   drawUCTRlx_4x4=False,
   drawUCTIso_byhand_4x4=False,
   drawUCTRlx_4x8=True,
   drawUCTIso_byhand_4x8=True,
   drawL1Iso_=drawL1Iso,
   drawL1Rlx_=drawL1Rlx,
   line=rateLine,
   ptLine=l1ptVal,
   HThresh = 2
   )
   make_rate_plot(
   binRate,
   ntuple_UCT_rlx_4x4=rate_rlx_UCT_ntuple_4x4,
   ntuple_UCT_iso_4x4=rate_iso_UCT_ntuple_4x4,
   ntuple_UCT_rlx_4x8=rate_rlx_hcal3,
   ntuple_UCT_iso_4x8=rate_iso_hcal3,
   ntuple_L1_rlx =rate_rlx_L1_ntuple,
   ntuple_L1_iso =rate_iso_L1_ntuple,
   filename='',
   setLOG=True,
   # 12x12 - 4x4 (I think)
   isoCut_4x4='(( pt[0]>=63 && (jetPt[0]-regionPt[0])/regionPt[0]<100)||(pt[0]<63&&(jetPt[0]-regionPt[0])/regionPt[0]<'+str(ISOTHRESHOLD_4x4)+'))',
   #isoCut_4x8='(( pt[0]>=63 && (jetPt[0]-regionPt[0])/regionPt[0]<100)||(pt[0]<63&&(jetPt[0]-regionPt[0])/regionPt[0]<'+str(ISOTHRESHOLD_4x8)+'))',
   isoCut_4x8='(( pt[0]>=90 && (jetPt[0]-pt[0])/pt[0]<100)||(pt[0]<90&&(jetPt[0]-pt[0])/pt[0]<'+str(ISOTHRESHOLD_4x8)+'))',
   # old thing 12x12 - 2x1 before 63
   #isoCut='(( pt[0]>=63 && (jetPt[0]-regionPt[0])/regionPt[0]<100)||(pt[0]<63&&(jetPt[0]-pt[0])/pt[0]<'+str(ISOTHRESHOLD)+'))',
   extraCut='(eta[0] > -2.5 && eta[0] < 2.5 && l1gTauVeto[0] == 0)',
   drawUCTIso_=drawUCTIso,
   drawUCTRlx_4x4=False,
   drawUCTIso_byhand_4x4=False,
   drawUCTRlx_4x8=True,
   drawUCTIso_byhand_4x8=True,
   drawL1Iso_=drawL1Iso,
   drawL1Rlx_=drawL1Rlx,
   line=rateLine,
   ptLine=l1ptVal,
   HThresh = 3
   )
   make_rate_plot(
   binRate,
   ntuple_UCT_rlx_4x4=rate_rlx_UCT_ntuple_4x4,
   ntuple_UCT_iso_4x4=rate_iso_UCT_ntuple_4x4,
   ntuple_UCT_rlx_4x8=rate_rlx_hcal4,
   ntuple_UCT_iso_4x8=rate_iso_hcal4,
   ntuple_L1_rlx =rate_rlx_L1_ntuple,
   ntuple_L1_iso =rate_iso_L1_ntuple,
   filename='',
   setLOG=True,
   # 12x12 - 4x4 (I think)
   isoCut_4x4='(( pt[0]>=63 && (jetPt[0]-regionPt[0])/regionPt[0]<100)||(pt[0]<63&&(jetPt[0]-regionPt[0])/regionPt[0]<'+str(ISOTHRESHOLD_4x4)+'))',
   #isoCut_4x8='(( pt[0]>=63 && (jetPt[0]-regionPt[0])/regionPt[0]<100)||(pt[0]<63&&(jetPt[0]-regionPt[0])/regionPt[0]<'+str(ISOTHRESHOLD_4x8)+'))',
   isoCut_4x8='(( pt[0]>=90 && (jetPt[0]-pt[0])/pt[0]<100)||(pt[0]<90&&(jetPt[0]-pt[0])/pt[0]<'+str(ISOTHRESHOLD_4x8)+'))',
   # old thing 12x12 - 2x1 before 63
   #isoCut='(( pt[0]>=63 && (jetPt[0]-regionPt[0])/regionPt[0]<100)||(pt[0]<63&&(jetPt[0]-pt[0])/pt[0]<'+str(ISOTHRESHOLD)+'))',
   extraCut='(eta[0] > -2.5 && eta[0] < 2.5 && l1gTauVeto[0] == 0)',
   drawUCTIso_=drawUCTIso,
   drawUCTRlx_4x4=False,
   drawUCTIso_byhand_4x4=False,
   drawUCTRlx_4x8=True,
   drawUCTIso_byhand_4x8=True,
   drawL1Iso_=drawL1Iso,
   drawL1Rlx_=drawL1Rlx,
   line=rateLine,
   ptLine=l1ptVal,
   HThresh = 4
   )
   make_rate_plot(
   binRate,
   ntuple_UCT_rlx_4x4=rate_rlx_UCT_ntuple_4x4,
   ntuple_UCT_iso_4x4=rate_iso_UCT_ntuple_4x4,
   ntuple_UCT_rlx_4x8=rate_rlx_hcal5,
   ntuple_UCT_iso_4x8=rate_iso_hcal5,
   ntuple_L1_rlx =rate_rlx_L1_ntuple,
   ntuple_L1_iso =rate_iso_L1_ntuple,
   filename='',
   setLOG=True,
   # 12x12 - 4x4 (I think)
   isoCut_4x4='(( pt[0]>=63 && (jetPt[0]-regionPt[0])/regionPt[0]<100)||(pt[0]<63&&(jetPt[0]-regionPt[0])/regionPt[0]<'+str(ISOTHRESHOLD_4x4)+'))',
   #isoCut_4x8='(( pt[0]>=63 && (jetPt[0]-regionPt[0])/regionPt[0]<100)||(pt[0]<63&&(jetPt[0]-regionPt[0])/regionPt[0]<'+str(ISOTHRESHOLD_4x8)+'))',
   isoCut_4x8='(( pt[0]>=90 && (jetPt[0]-pt[0])/pt[0]<100)||(pt[0]<90&&(jetPt[0]-pt[0])/pt[0]<'+str(ISOTHRESHOLD_4x8)+'))',
   # old thing 12x12 - 2x1 before 63
   #isoCut='(( pt[0]>=63 && (jetPt[0]-regionPt[0])/regionPt[0]<100)||(pt[0]<63&&(jetPt[0]-pt[0])/pt[0]<'+str(ISOTHRESHOLD)+'))',
   extraCut='(eta[0] > -2.5 && eta[0] < 2.5 && l1gTauVeto[0] == 0)',
   drawUCTIso_=drawUCTIso,
   drawUCTRlx_4x4=False,
   drawUCTIso_byhand_4x4=False,
   drawUCTRlx_4x8=True,
   drawUCTIso_byhand_4x8=True,
   drawL1Iso_=drawL1Iso,
   drawL1Rlx_=drawL1Rlx,
   line=rateLine,
   ptLine=l1ptVal,
   HThresh = 5
   )
 

