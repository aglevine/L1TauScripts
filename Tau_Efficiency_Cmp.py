'''
Makes Tau efficiency plots
Authors: T.M.Perry, E.K.Friis, M.Cepeda, A.G.Levine, N.Woods UW Madison
'''
from sys import argv, stdout, stderr
import ROOT

efficiencyPlots=True
# which curves to draw on rate and efficiency plots
drawUCTIso_4x4 = False
drawUCTIso_4x8 = False
drawUCTRlx_4x4 = False
drawUCTRlx_4x8 = True
drawUCTIso_byhand = True
drawL1Iso = False
drawL1Rlx = False

##################
# Set Parameters #
##################
LIso=3
LSB=50
l1ptVal=40
recoPtVal=30
ISOTHRESHOLD_4x4=0.4
ISOTHRESHOLD_4x8=0.10
turnOffIso=63
turnOffTauVeto=90
L1_CALIB_FACTOR = 1.0
L1G_CALIB_FACTOR = 1.0
ZEROBIAS_RATE=15000000.00
savedir = argv[1]
doTauVeto = argv[2]
neighborEff = argv[3]
#saveWhere='../plots/Tau_Efficiency_ECALseed'
#saveWhere='plots/Tau_Efficiency_highSeed'
#saveWhere = 'plots/Tau_Efficiency_halfIso'
#saveWhere = 'plots/Tau_EfficiencyTightIso'
#saveWhere = 'plots/TauEff4x4cmp4x8NoDiag0point2IsoPlot'
#saveWhere = 'plots/TauEff4x4cmp4x8NoExtraTauSeed'
saveWhere = savedir
if "ECAL1" in savedir:
        legendStr = " ECAL 1 "
        EThresh = "1"
        fname = "tau_eff_4x8_E1"
elif "ECAL2" in savedir:
        legendStr = " ECAL 2 "
        EThresh = "2"
        fname = "tau_eff_4x8_E2"
elif "ECAL3" in savedir:
        legendStr = " ECAL 3 "
        EThresh = "3"
        fname = "tau_eff_4x8_E3"
elif "ECAL4" in savedir:
        legendStr = " ECAL 4 "
        EThresh = "4"
        fname = "tau_eff_4x8_E4"
elif "ECAL5" in savedir:
        legendStr = " ECAL 5 "
        EThresh = "5"
        fname = "tau_eff_4x8_E5"

########
# File #
########
#Efficiency
#eff_ntuple = '../data/h2tau.root'
#eff_ntuple = 'uct_tau_efficiency_tree.root'
#eff_ntuple = 'uct_tau_highSeed.root'
#eff_ntuple = 'uct_efficiency_tau_5iso.root'
#eff_ntuple = 'uct_efficiency_tree_halfIsoredo.root'
#eff_ntuple = 'uct_efficiency_tree_oneandahalfIso.root'
#eff_ntuple = 'uct_efficiency_tree_threshold80.root'
#eff_ntuple = 'uct_efficiency_tree_denomfix.root'
#eff_ntuple = 'uct_efficiency_tree_tightiso.root'
#aeff_ntuple = 'uct_efficiency_tree4x8veto.root'
#aeff_ntuple = 'uct_efficiency_tree_4x8iso.root'
#eff_ntuple_4x4= 'tau_eff_4x4point4iso.root'
eff_ntuple_4x4 ='tau_eff_4x4_1point0iso.root'
#eff_ntuple_4x4 = 'tau_eff_4x8_TTbar.root' #actually ttbar 4x8 background, not 4x4 ntuples
#eff_ntuple_4x8 = 'tau_eff_4x8point4iso.root'
#eff_ntuple_4x8 = 'tau_eff_4x8point2iso.root'
#eff_ntuple_4x8 = 'tau_eff_nodiag.root'
eff_ntuple_4x8_hcal1 = savedir +fname+'H1_NoNeighborSeed.root'
eff_ntuple_4x8_hcal2 = savedir +fname+'H2_NoNeighborSeed.root'
eff_ntuple_4x8_hcal3 = savedir +fname+'H3_NoNeighborSeed.root'
eff_ntuple_4x8_hcal4 = savedir +fname+'H4_NoNeighborSeed.root'
eff_ntuple_4x8_hcal5 = savedir +fname+'H5_NoNeighborSeed.root'
#eff_ntuple_4x8 = 'tau_eff_4x8_TTbar.root'
#aeff_ntuple_4x8 = 'tau_eff_4x8iso4x4.root'
#eff_ntuple = '/afs/hep.wisc.edu/cms/aglevine/L1Taus/src/L1Trigger/UWTriggerTools/test/uct_tau_highSeed.root'
eff_ntuple_file_4x4 = ROOT.TFile(eff_ntuple_4x4)
eff_ntuple_file_4x8_hcal1 = ROOT.TFile(eff_ntuple_4x8_hcal1)
eff_ntuple_file_4x8_hcal2 = ROOT.TFile(eff_ntuple_4x8_hcal2)
eff_ntuple_file_4x8_hcal3 = ROOT.TFile(eff_ntuple_4x8_hcal3)
eff_ntuple_file_4x8_hcal4 = ROOT.TFile(eff_ntuple_4x8_hcal4)
eff_ntuple_file_4x8_hcal5 = ROOT.TFile(eff_ntuple_4x8_hcal5)
#
#eff_rlx_spot = 'rlxTauEcalSeedEfficiency/Ntuple'
eff_rlx_spot = 'rlxTauEfficiency/Ntuple'
#eff_iso_spot = 'isoTauEcalSeedEfficiency/Ntuple'
eff_iso_spot = 'isoTauEfficiency/Ntuple'
eff_rlx_eg_ntuple_4x4 = eff_ntuple_file_4x4.Get(eff_rlx_spot)
eff_iso_eg_ntuple_4x4 = eff_ntuple_file_4x4.Get(eff_iso_spot)
eff_rlx_eg_ntuple_4x8_hcal1 = eff_ntuple_file_4x8_hcal1.Get(eff_rlx_spot)
eff_iso_eg_ntuple_4x8_hcal1 = eff_ntuple_file_4x8_hcal1.Get(eff_iso_spot)
eff_rlx_eg_ntuple_4x8_hcal2 = eff_ntuple_file_4x8_hcal2.Get(eff_rlx_spot)
eff_iso_eg_ntuple_4x8_hcal2 = eff_ntuple_file_4x8_hcal2.Get(eff_iso_spot)
eff_rlx_eg_ntuple_4x8_hcal3 = eff_ntuple_file_4x8_hcal3.Get(eff_rlx_spot)
eff_iso_eg_ntuple_4x8_hcal3 = eff_ntuple_file_4x8_hcal3.Get(eff_iso_spot)
eff_rlx_eg_ntuple_4x8_hcal4 = eff_ntuple_file_4x8_hcal4.Get(eff_rlx_spot)
eff_iso_eg_ntuple_4x8_hcal4 = eff_ntuple_file_4x8_hcal4.Get(eff_iso_spot)
eff_rlx_eg_ntuple_4x8_hcal5 = eff_ntuple_file_4x8_hcal5.Get(eff_rlx_spot)
eff_iso_eg_ntuple_4x8_hcal5 = eff_ntuple_file_4x8_hcal5.Get(eff_iso_spot)

#To Be Made
store = ROOT.TFile(saveWhere+'.root','RECREATE')

name=''
if drawUCTIso_4x4 or drawUCTRlx_4x4 or drawUCTIso_4x8 or drawUCTRlx_4x8 or drawUCTIso_byhand: name+='_UCT_'
if drawUCTRlx_4x4: name+='R4'
if drawUCTIso_4x4: name+='I4'
if drawUCTRlx_4x8: name+='R8'
if drawUCTIso_4x8: name+='I8'
if drawUCTIso_byhand: name+='Ibh'+str(int(ISOTHRESHOLD_4x8 * 10))
name+='_'

if drawL1Iso or drawL1Rlx: name+= 'L1_'
if drawL1Rlx: name+='R'
if drawL1Iso: name+='I'

extraName=''
name+=extraName
name = name+str(ISOTHRESHOLD_4x8)
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
 draw_string = "%s * %0.2f>>htemp(%s)" % (variable,calFactor, ", ".join(str(x) for x in binning))
 print "draw_string "+ draw_string
 print selection
 tree.Draw(draw_string, selection, "goff")
 output_histo = ROOT.gDirectory.Get("htemp").Clone()
 output_histo.GetXaxis().SetTitle(xaxis)
 output_histo.SetTitle(title)
 return output_histo

################RESOLUTION##############################################
def make_res_nrml(ntuple_rlx_4x4,ntuple_iso_4x4,ntuple_rlx_4x8,ntuple_iso_4x8,reco,l1,l1g,binning,cutPtVarg='l1gPt',cutPtVar='l1Pt',cutPt=l1ptVal,filename='',extraCut='',extraCutb='',setLOG=False):
 canvas.SetLogy(setLOG)
 info = 'RES_'+str(reco)+'_'+cutPtVar+'Cut'

 l1gplot_rlx_4x4 = make_plot(
  ntuple_rlx_4x4, '('+str(reco)+' - ('+str(L1G_CALIB_FACTOR)+' * '+str(l1g)+'))/'+str(reco),
  'l1gMatch&&'+cutPtVarg+'>'+str(cutPt)+extraCut,binning
 )
 l1gplot_rlx_4x8 = make_plot(
  ntuple_rlx_4x8, '('+str(reco)+' - ('+str(L1G_CALIB_FACTOR)+' * '+str(l1g)+'))/'+str(reco),
  'l1gMatch&&'+cutPtVarg+'>'+str(cutPt)+extraCut,binning
 )
 l1gplot_iso_4x4 = make_plot(
  ntuple_iso_4x4, '('+str(reco)+' - ('+str(L1G_CALIB_FACTOR)+' * '+str(l1g)+'))/'+str(reco),
  'l1gMatch&&'+cutPtVarg+'>'+str(cutPt)+extraCut,binning
 )
 l1gplot_iso_4x8 = make_plot(
  ntuple_iso_4x8, '('+str(reco)+' - ('+str(L1G_CALIB_FACTOR)+' * '+str(l1g)+'))/'+str(reco),
  'l1gMatch&&'+cutPtVarg+'>'+str(cutPt)+extraCut,binning
 )

 l1gplot_rlx_4x4.SetTitle('Resolution')
 l1gplot_rlx_4x4.GetXaxis().SetTitle('(recoPt- l1gPt)/recoPt')
 l1gplot_rlx_4x4.SetLineColor(ROOT.EColor.kBlue)

 legend = ROOT.TLegend(0.6,0.7,0.89,0.89,'','brNDC')
 legend.SetFillColor(ROOT.EColor.kWhite)
 legend.SetBorderSize(0)
 legend.AddEntry(l1gplot_rlx_4x4,'4x4 UCT: Rlx')
 legend.AddEntry(l1gplot_rlx_4x8,'4x8 UCT: Rlx')
 legend.AddEntry(l1gplot_iso_4x4,'4x4 UCT: Iso <%0.2f'%(ISOTHRESHOLD_4x4))
 legend.AddEntry(l1gplot_iso_4x8,'4x8 UCT: Iso <%0.2f'%(ISOTHRESHOLD_4x8))
  
 #legend.AddEntry(l1bplot,'Stage 1B upgrade')
 
 l1gplot_rlx_4x4.SetLineColor(ROOT.EColor.kGreen+3)
 l1gplot_rlx_4x4.SetLineWidth(3)
 l1gplot_rlx_4x8.SetLineColor(ROOT.EColor.kMagenta+2)
 l1gplot_rlx_4x8.SetLineWidth(3)
 l1gplot_iso_4x4.SetLineColor(ROOT.EColor.kRed)
 l1gplot_rlx_4x8.SetLineWidth(3)
 l1gplot_iso_4x8.SetLineColor(ROOT.EColor.kOrange+2)
 l1gplot_iso_4x8.SetLineWidth(3)
 l1gplot_rlx_4x4.Scale(1/l1gplot_rlx_4x4.Integral())
 l1gplot_rlx_4x8.Scale(1/l1gplot_rlx_4x8.Integral())
 l1gplot_iso_4x4.Scale(1/l1gplot_iso_4x4.Integral())
 l1gplot_iso_4x8.Scale(1/l1gplot_iso_4x8.Integral())
 l1gplot_rlx_4x4.Draw()
 l1gplot_rlx_4x8.Draw("sames")
 l1gplot_iso_4x4.Draw("sames")
 l1gplot_iso_4x8.Draw("sames")
 #l1bplot.Draw('sames')
 #l1gplot.SetMaximum(1.1*max(l1gplot.GetMaximum(),l1bplot.GetMaximum()))
 l1gplot_rlx_4x4.SetMaximum(0.15)
 legend.Draw()

 canvas.SaveAs(saveWhere+info+filename+'.png')

def make_iso_nrml(ntuple_rlx_4x4,ntuple_iso_4x4,ntuple_rlx_4x8,ntuple_iso_4x8,reco,l1,l1g,binning,cutPtVarg='l1gPt',cutPtVar='l1Pt',cutPt=l1ptVal,filename='',extraCut='',extraCutb='',setLOG=False):
 canvas.SetLogy(setLOG)
 info = 'ISO_NoMatch'+str(reco)+'_'+cutPtVar+'Cut'

 l1gplot_rlx_4x4 = make_plot(
  ntuple_rlx_4x4, '('+str(L1G_CALIB_FACTOR)+'*l1gJetPt - ('+str(L1G_CALIB_FACTOR)+' * '+str(l1g)+'))/('+str(L1G_CALIB_FACTOR)+' * '+str(l1g)+')',
  ''+cutPtVarg+'>'+str(cutPt)+extraCut,binning
 )
 l1gplot_rlx_4x8 = make_plot(
  ntuple_rlx_4x8, '('+str(L1G_CALIB_FACTOR)+'*l1gJetPt - ('+str(L1G_CALIB_FACTOR)+' * '+str(l1g)+'))/('+str(L1G_CALIB_FACTOR)+' * '+str(l1g)+')',
  ''+cutPtVarg+'>'+str(cutPt)+extraCut,binning
 )
 l1gplot_iso_4x4 = make_plot(
  ntuple_iso_4x4, '('+str(L1G_CALIB_FACTOR)+'*l1gJetPt - ('+str(L1G_CALIB_FACTOR)+' * '+str(l1g)+'))/('+str(L1G_CALIB_FACTOR)+' * '+str(l1g)+')',
  ''+cutPtVarg+'>'+str(cutPt)+extraCut,binning
 )
 l1gplot_iso_4x8 = make_plot(
  ntuple_iso_4x8, '('+str(L1G_CALIB_FACTOR)+'*l1gJetPt - ('+str(L1G_CALIB_FACTOR)+' * '+str(l1g)+'))/('+str(L1G_CALIB_FACTOR)+' * '+str(l1g)+')',
  ''+cutPtVarg+'>'+str(cutPt)+extraCut,binning
 )

 l1gplot_rlx_4x4.SetTitle('Isolation')
 l1gplot_rlx_4x4.GetXaxis().SetTitle('(l1gJetPt- l1gPt)/l1gPt')
 l1gplot_rlx_4x4.SetLineColor(ROOT.EColor.kBlue)

 legend = ROOT.TLegend(0.4,0.4,0.89,0.89,'','brNDC')
 legend.SetFillColor(ROOT.EColor.kWhite)
 legend.SetBorderSize(0)
 legend.AddEntry(l1gplot_rlx_4x4,'4x4 UCT: Rlx')
 #legend.AddEntry(l1gplot_rlx_4x4,'4x8 UCT: TTbar Rlx') #changed to do a quick comparison between relaxed signal and background
 legend.AddEntry(l1gplot_rlx_4x8,'4x8 UCT: Rlx')
 #legend.AddEntry(l1gplot_iso_4x4,'4x4 UCT: Iso <%0.1f'%(ISOTHRESHOLD_4x4))
 #legend.AddEntry(l1gplot_iso_4x8,'4x8 UCT: Iso <%0.1f'%(ISOTHRESHOLD_4x8))
  
 #legend.AddEntry(l1bplot,'Stage 1B upgrade')
 
 l1gplot_rlx_4x4.SetLineColor(ROOT.EColor.kGreen+3)
 l1gplot_rlx_4x4.SetLineWidth(3)
 l1gplot_rlx_4x8.SetLineColor(ROOT.EColor.kMagenta+2)
 l1gplot_rlx_4x8.SetLineWidth(3)
 l1gplot_iso_4x4.SetLineColor(ROOT.EColor.kRed)
 l1gplot_rlx_4x8.SetLineWidth(3)
 l1gplot_iso_4x8.SetLineColor(ROOT.EColor.kOrange+2)
 l1gplot_iso_4x8.SetLineWidth(3)
 l1gplot_rlx_4x4.Scale(1/l1gplot_rlx_4x4.Integral())
 l1gplot_rlx_4x8.Scale(1/l1gplot_rlx_4x8.Integral())
 #l1gplot_iso_4x4.Scale(1/l1gplot_iso_4x4.Integral())
 #l1gplot_iso_4x8.Scale(1/l1gplot_iso_4x8.Integral())
 l1gplot_rlx_4x4.SetMaximum(0.5)
 l1gplot_rlx_4x4.Draw()
 l1gplot_rlx_4x8.Draw("sames")
 #l1gplot_iso_4x4.Draw("sames")
 #l1gplot_iso_4x8.Draw("sames")
 print "scanning 4x4 bins"
 
 for i in range(1,l1gplot_iso_4x4.GetNbinsX()):
 	print l1gplot_rlx_4x4.GetBinContent(i)
 print "scanning 4x8 bins"

 for i in range(1,l1gplot_iso_4x8.GetNbinsX()):
        print l1gplot_rlx_4x8.GetBinContent(i)
 #l1bplot.Draw('sames')
 #l1gplot_rlx_4x4.SetMaximum(1.1*max(l1gplot_iso_4x4.GetMaximum(),l1gplot_iso_4x8.GetMaximum(),l1gplot_rlx_4x4.GetMaximum(),l1gplot_rlx_4x8.GetMaximum()))
 #l1gplot_rlx_4x4.SetMaximum(0.35)
 legend.Draw()

 canvas.SaveAs(saveWhere+info+filename+'.png')


################RESOLUTION####################################################

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

def effi_histo(ntuple,variable,cut,binning,denom,title,leg,color,marker,logg):
 num = make_plot(ntuple,variable,cut,binning)
 efiHist = num.Clone()
 efiHist.Divide(denom)
 efi = make_l1_efficiency(denom,num,color,marker)
 leg.AddEntry(efi,title,'pe')
 efi.Draw('pe')
 logg.write('---------------------------------\n')
 logg.write(title+'\n\n')
 logg.write('Tree: '+ntuple.GetDirectory().GetName()+'\n\n')
 logg.write('Cut: '+cut+'\n\n')
 print "looping through: " + title
 for i in range(1,efiHist.GetNbinsX()):
        print efiHist.GetBinContent(i)
 return efi

def compare_efficiencies(
 variable,
 binning,
 ntuple_rlx_4x4=None,
 ntuple_iso_4x4=None,
 ntuple_rlx_4x8=None,
 ntuple_iso_4x8=None,
 recoPtCut='(2>1)',l1PtCut='(2>1)',l1gPtCut='(2>1)',
 isoCut_4x4='(2>1)',isoCut_4x8 = '(2>1)',extraCut='&&(2>1)',
 drawUCTIso_4x4=False,
 drawUCTRlx_4x4=False,
 drawUCTIso_4x8=False,
 drawUCTRlx_4x8=False,
 drawUCTIso_byhand_=False,
 drawL1Iso_=False,
 drawL1Rlx_=False,
 legExtra='',
 setLOG=False,
 HThresh = ''
):
 '''
Returns a (L1, L1G) tuple of TGraphAsymmErrors
'''

 cutD_rlx = recoPtCut+extraCut
 #denom_rlx_4x4 = make_plot(
 # ntuple_rlx_4x4,variable,
 # cutD_rlx,
 # binning
 #)
 denom_rlx_4x8 = make_plot(
  ntuple_rlx_4x8,variable,
  cutD_rlx,
  binning
 )
 cutD_iso = cutD_rlx #+ '&& (dr03CombinedEt/recoPt)<0.2'
 #denom_iso_4x4 = make_plot(
 # ntuple_iso_4x4,variable,
 # cutD_iso,
 # binning
 #)
 denom_iso_4x8 = make_plot(
  ntuple_iso_4x8,variable,
  cutD_iso,
  binning
 )
 
 log.write('_____________________________\n')
 log.write('-------- Efficiency ---------\n\n')
 log.write('Variable: '+variable+'\n\n')
 log.write('Denominator Tree: '+ntuple_rlx_4x8.GetDirectory().GetName()+'\n')
 #log.write('Denominator Cut: '+cutD+'\n\n')
 
 frame = ROOT.TH1F('frame','frame',*binning)
 canvas.SetLogy(setLOG)
 frame.Draw()
 frame.SetTitle('')
 if doTauVeto:
 	if neighborEff == "False":
 		frame.GetYaxis().SetTitle('Efficiency, TauVeto = 0')
 	else:
		frame.GetYaxis().SetTitle('Efficiency, TauVetoNeighbor = 0')
 else:
	frame.GetYaxis().SetTitle('Efficiency, No Tau Veto Cut')
 frame.SetMaximum(1.1)
 if variable is 'nPVs': frame.GetXaxis().SetTitle('Nr. Primary Vertices')
 else: frame.GetXaxis().SetTitle(variable)
 frame.GetXaxis().SetRangeUser(0,100)
 tex.DrawLatex(0.1,0.91,'Tau '+variable+' Efficiency')
 tex.SetTextSize(0.03)
 tex.DrawLatex(0.1,0.87,'CMS Preliminary')
 tex.DrawLatex(0.5,0.87,'ECAL: '+EThresh+' HCAL: '+HThresh)
 tex.SetTextSize(0.07)
 #legend = ROOT.TLegend(0.15,0.35,0.69,0.55,'','brNDC')
 legend = ROOT.TLegend(0.15,0.65,0.35,0.85,'','brNDC')
 legend.SetTextSize(0.03)
 legend.SetFillColor(0)
 legend.SetBorderSize(0)
 legend.SetHeader(legExtra)
 
 info ='Eff_ECAL'+EThresh+'_HCAL'+HThresh+'_'+variable+'_TauVetoOffAbove'+str(turnOffTauVeto)+'_OffIso'+str(turnOffIso)+'_'
 if neighborEff == "True":
	info = info + "_neighborEff"
 if doTauVeto == "False":
	info = info+"_NoTauVeto"
 else:
	info = info+"TauVeto"
 if variable=='nPVs': info+=str(recoPtVal)
 vetoCut =extraCut
 if doTauVeto == "True":
 	if neighborEff == "True":
       	  vetoCut = vetoCut+"&& (l1gTauVetoNeighbor ==0)"
       	  print neighborEff + "True"
 	if neighborEff == "False":
       	  vetoCut = vetoCut +"&& (l1gTauVeto == 0 || l1gPt >" + str(turnOffTauVeto)+")"
       	  print neighborEff +"False"
 print neighborEff
# Current Relaxed
 if drawL1Rlx_:
  cut_L1_rlx=recoPtCut+'&&'+l1PtCut+'&& l1Match'
  h_L1_rlx=effi_histo(ntuple_rlx,variable,cut_L1_rlx,binning,denom_rlx,
  'L1: Rlx',legend,
  colorCR,markerCR,log)
  h_L1_rlx.SetName('h_L1_rlx')
  h_L1_rlx.Write()
# Current With Isolation
 if drawL1Iso_:
  cut_L1_iso=recoPtCut+'&&'+l1PtCut+'&& l1Match'# && (dr03CombinedEt/recoPt)<0.2'
  h_L1_iso=effi_histo(ntuple_iso,variable,cut_L1_iso,binning,denom_iso,
  'L1: Iso',legend,
  colorCI,markerCI,log)
  h_L1_iso.SetName('h_L1_iso')
  h_L1_iso.Write()
# UCT Relaxed
 if drawUCTRlx_4x4:
  cut_uctR=recoPtCut+'&&'+l1gPtCut+'&&l1gMatch'# &&l1gTauVeto == 1'
  h_UCT_rlx_4x4=effi_histo(ntuple_rlx_4x4,variable,cut_uctR,binning,denom_rlx_4x4,
  '4x4 UCT: Rlx',legend,
   colorUR,markerUR,log)
  h_UCT_rlx_4x4.SetName('h_UCT_rlx')
  h_UCT_rlx_4x4.Write()
 if drawUCTRlx_4x8:
  cut_uctR=recoPtCut+'&&'+l1gPtCut+'&&l1gMatch'+vetoCut
  h_UCT_rlx_4x8=effi_histo(ntuple_rlx_4x8,variable,cut_uctR,binning,denom_rlx_4x8,
  '4x8 UCT: Rlx',legend,
   (ROOT.EColor.kMagenta+2),markerUR,log)
  h_UCT_rlx_4x8.SetName('h_UCT_rlx')
  h_UCT_rlx_4x8.Write()
# UCT Rlx + Isolation by hand
 if drawUCTIso_byhand_:
  cut_UCT_isoByHand=recoPtCut+'&&'+l1gPtCut+'&&'+isoCut_4x8+'&& l1gMatch'+vetoCut # && (dr03CombinedEt/recoPt)<0.2'
  h_UCT_isoByHand=effi_histo(ntuple_rlx_4x8,variable,cut_UCT_isoByHand,binning,denom_iso_4x8,
  'UCT: Iso < %0.2f'%(ISOTHRESHOLD_4x8),legend,
  #'UCT: Rlx + IsoByHand<%0.1f'%(ISOTHRESHOLD),legend,
  colorUIbh,markerUIbh,log)
  h_UCT_isoByHand.SetName('h_UCT_isoByHand')
  h_UCT_isoByHand.Write()
# UCT Isolated
 if drawUCTIso_4x4:
  cut_uctI=recoPtCut+'&&'+l1gPtCut+'&&'+isoCut_4x4+'&&l1gMatch'# &&l1gTauVeto == 1'#&& (dr03CombinedEt/recoPt)<0.2'
  h_UCT_iso_4x4=effi_histo(ntuple_iso_4x4,variable,cut_uctI,binning,denom_iso_4x4,
  '4x4 UCT: Iso<%0.1f'%(ISOTHRESHOLD_4x4),legend,
   colorUI,markerUI,log)
  h_UCT_iso_4x4.SetName('h_UCT_iso_4x4')
  h_UCT_iso_4x4.Write()

 if drawUCTIso_4x8:
  cut_uctI=recoPtCut+'&&'+l1gPtCut+'&&'+isoCut_4x8+'&&l1gMatch' #&&l1gTauVeto == 1'#&& (dr03CombinedEt/recoPt)<0.2'
  h_UCT_iso_4x8=effi_histo(ntuple_iso_4x8,variable,cut_uctI,binning,denom_iso_4x8,
  '4x8 UCT: Iso<%0.1f'%(ISOTHRESHOLD_4x8),legend,
   (ROOT.EColor.kOrange+2),markerUI,log)
  h_UCT_iso_4x8.SetName('h_UCT_iso_4x8')
  h_UCT_iso_4x8.Write()

 legend.Draw()
 #save=raw_input("Type save to save as "+saveWhere+name+info+".png (enter to continue):\n")
 #if save=="save": 
 canvas.SaveAs(saveWhere+name+info+'.png')
 #canvas.SaveAs(saveWhere+name+info+'.png')
######################################################################
##### EFFICIENCY #####################################################
######################################################################


######################################################################
###### DRAW PLOTS ####################################################
######################################################################

####################
# Efficiency Plots #
####################
if efficiencyPlots == True:
 #binPt = [10,40,80] #l120
 binPt = [40,0,200]
 binVert=[10,0,35]
 binJetPt=[40,0,70]
 binRes = [100,-2,2]
 binIso = [50,0,1]

# variable,
# binning,
# ntuple_rlx=None,
# ntuple_iso=None,
# recoPtCut='(2>1)',l1PtCut='(2>1)',l1gPtCut='(2>1)',
# isoCut='(2>1)',extraCut='(2>1)',
# drawUCTIso_=False,
# drawUCTRlx_=False,
# drawUCTIso_byhand_=False,
# drawL1Iso_=False,
# drawL1Rlx_=False
# legExtra='',
# setLOG=False


 compare_efficiencies(
  'recoPt',
  binPt,
  eff_rlx_eg_ntuple_4x4, eff_iso_eg_ntuple_4x4,eff_rlx_eg_ntuple_4x8_hcal1, eff_iso_eg_ntuple_4x8_hcal1,
  recoPtCut = '(recoPt >= '+str(recoPtVal)+')',
  l1PtCut = '(l1Pt >= '+str(l1ptVal)+')',
  #l1gPtCut = '(l1gRegionEt >= '+str(l1ptVal)+')',
  l1gPtCut = '(l1gPt >= '+str(l1ptVal)+')',
  # 12x12-4x4
  isoCut_4x4='(l1gPt>='+str(turnOffIso)+'||(l1gJetPt-l1gRegionEt)/l1gRegionEt<'+str(ISOTHRESHOLD_4x4)+')',
  #isoCut_4x8='(l1gPt>=60||(l1gJetPt-l1gRegionEt)/l1gRegionEt<'+str(ISOTHRESHOLD_4x8)+')',
  isoCut_4x8='(l1gPt>='+str(turnOffIso)+'||(l1gJetPt-l1gPt)/l1gPt<'+str(ISOTHRESHOLD_4x8)+')',
  #extraCut ='&&(decayMode == 10)',
  # 12x12 - 2x1
  #isoCut='(l1gPt[0]>=60||(l1gJetPt[0]-l1gPt[0])/l1gPt[0]<'+str(ISOTHRESHOLD)+')',
  drawUCTIso_4x4 = False,
  drawUCTRlx_4x4 = False,
  drawUCTIso_4x8 = False,
  drawUCTRlx_4x8 = True,
  drawUCTIso_byhand_=drawUCTIso_byhand,
  drawL1Iso_=drawL1Iso,
  drawL1Rlx_=drawL1Rlx,
  HThresh = '1'
  #legExtra = 'Tau 4x4'
 )

 compare_efficiencies(
  'recoPt',
  binPt,
  eff_rlx_eg_ntuple_4x4, eff_iso_eg_ntuple_4x4,eff_rlx_eg_ntuple_4x8_hcal2, eff_iso_eg_ntuple_4x8_hcal2,
  recoPtCut = '(recoPt >= '+str(recoPtVal)+')',
  l1PtCut = '(l1Pt >= '+str(l1ptVal)+')',
  #l1gPtCut = '(l1gRegionEt >= '+str(l1ptVal)+')',
  l1gPtCut = '(l1gPt >= '+str(l1ptVal)+')',
  # 12x12-4x4
  isoCut_4x4='(l1gPt>='+str(turnOffIso)+'||(l1gJetPt-l1gRegionEt)/l1gRegionEt<'+str(ISOTHRESHOLD_4x4)+')',
  #isoCut_4x8='(l1gPt>=60||(l1gJetPt-l1gRegionEt)/l1gRegionEt<'+str(ISOTHRESHOLD_4x8)+')',
  isoCut_4x8='(l1gPt>='+str(turnOffIso)+'||(l1gJetPt-l1gPt)/l1gPt<'+str(ISOTHRESHOLD_4x8)+')',
  #extraCut ='&&(decayMode == 10)',
  # 12x12 - 2x1
  #isoCut='(l1gPt[0]>=60||(l1gJetPt[0]-l1gPt[0])/l1gPt[0]<'+str(ISOTHRESHOLD)+')',
  drawUCTIso_4x4 = False,
  drawUCTRlx_4x4 = False,
  drawUCTIso_4x8 = False,
  drawUCTRlx_4x8 = True,
  drawUCTIso_byhand_=drawUCTIso_byhand,
  drawL1Iso_=drawL1Iso,
  drawL1Rlx_=drawL1Rlx,
  HThresh = '2'
  #legExtra = 'Tau 4x4'
 )

 compare_efficiencies(
  'recoPt',
  binPt,
  eff_rlx_eg_ntuple_4x4, eff_iso_eg_ntuple_4x4,eff_rlx_eg_ntuple_4x8_hcal3, eff_iso_eg_ntuple_4x8_hcal3,
  recoPtCut = '(recoPt >= '+str(recoPtVal)+')',
  l1PtCut = '(l1Pt >= '+str(l1ptVal)+')',
  #l1gPtCut = '(l1gRegionEt >= '+str(l1ptVal)+')',
  l1gPtCut = '(l1gPt >= '+str(l1ptVal)+')',
  # 12x12-4x4
  isoCut_4x4='(l1gPt>='+str(turnOffIso)+'||(l1gJetPt-l1gRegionEt)/l1gRegionEt<'+str(ISOTHRESHOLD_4x4)+')',
  #isoCut_4x8='(l1gPt>=60||(l1gJetPt-l1gRegionEt)/l1gRegionEt<'+str(ISOTHRESHOLD_4x8)+')',
  isoCut_4x8='(l1gPt>='+str(turnOffIso)+'||(l1gJetPt-l1gPt)/l1gPt<'+str(ISOTHRESHOLD_4x8)+')',
  #extraCut ='&&(decayMode == 10)',
  # 12x12 - 2x1
  #isoCut='(l1gPt[0]>=60||(l1gJetPt[0]-l1gPt[0])/l1gPt[0]<'+str(ISOTHRESHOLD)+')',
  drawUCTIso_4x4 = False,
  drawUCTRlx_4x4 = False,
  drawUCTIso_4x8 = False,
  drawUCTRlx_4x8 = True,
  drawUCTIso_byhand_=drawUCTIso_byhand,
  drawL1Iso_=drawL1Iso,
  drawL1Rlx_=drawL1Rlx,
  HThresh = '3'
  #legExtra = 'Tau 4x4'
 )

 compare_efficiencies(
  'recoPt',
  binPt,
  eff_rlx_eg_ntuple_4x4, eff_iso_eg_ntuple_4x4,eff_rlx_eg_ntuple_4x8_hcal4, eff_iso_eg_ntuple_4x8_hcal4,
  recoPtCut = '(recoPt >= '+str(recoPtVal)+')',
  l1PtCut = '(l1Pt >= '+str(l1ptVal)+')',
  #l1gPtCut = '(l1gRegionEt >= '+str(l1ptVal)+')',
  l1gPtCut = '(l1gPt >= '+str(l1ptVal)+')',
  # 12x12-4x4
  isoCut_4x4='(l1gPt>='+str(turnOffIso)+'||(l1gJetPt-l1gRegionEt)/l1gRegionEt<'+str(ISOTHRESHOLD_4x4)+')',
  #isoCut_4x8='(l1gPt>=60||(l1gJetPt-l1gRegionEt)/l1gRegionEt<'+str(ISOTHRESHOLD_4x8)+')',
  isoCut_4x8='(l1gPt>='+str(turnOffIso)+'||(l1gJetPt-l1gPt)/l1gPt<'+str(ISOTHRESHOLD_4x8)+')',
  #extraCut ='&&(decayMode == 10)',
  # 12x12 - 2x1
  #isoCut='(l1gPt[0]>=60||(l1gJetPt[0]-l1gPt[0])/l1gPt[0]<'+str(ISOTHRESHOLD)+')',
  drawUCTIso_4x4 = False,
  drawUCTRlx_4x4 = False,
  drawUCTIso_4x8 = False,
  drawUCTRlx_4x8 = True,
  drawUCTIso_byhand_=drawUCTIso_byhand,
  drawL1Iso_=drawL1Iso,
  drawL1Rlx_=drawL1Rlx,
  HThresh = '4'
  #legExtra = 'Tau 4x4'
 )

 compare_efficiencies(
  'recoPt',
  binPt,
  eff_rlx_eg_ntuple_4x4, eff_iso_eg_ntuple_4x4,eff_rlx_eg_ntuple_4x8_hcal5, eff_iso_eg_ntuple_4x8_hcal5,
  recoPtCut = '(recoPt >= '+str(recoPtVal)+')',
  l1PtCut = '(l1Pt >= '+str(l1ptVal)+')',
  #l1gPtCut = '(l1gRegionEt >= '+str(l1ptVal)+')',
  l1gPtCut = '(l1gPt >= '+str(l1ptVal)+')',
  # 12x12-4x4
  isoCut_4x4='(l1gPt>='+str(turnOffIso)+'||(l1gJetPt-l1gRegionEt)/l1gRegionEt<'+str(ISOTHRESHOLD_4x4)+')',
  #isoCut_4x8='(l1gPt>=60||(l1gJetPt-l1gRegionEt)/l1gRegionEt<'+str(ISOTHRESHOLD_4x8)+')',
  isoCut_4x8='(l1gPt>='+str(turnOffIso)+'||(l1gJetPt-l1gPt)/l1gPt<'+str(ISOTHRESHOLD_4x8)+')',
  #extraCut ='&&(decayMode == 10)',
  # 12x12 - 2x1
  #isoCut='(l1gPt[0]>=60||(l1gJetPt[0]-l1gPt[0])/l1gPt[0]<'+str(ISOTHRESHOLD)+')',
  drawUCTIso_4x4 = False,
  drawUCTRlx_4x4 = False,
  drawUCTIso_4x8 = False,
  drawUCTRlx_4x8 = True,
  drawUCTIso_byhand_=drawUCTIso_byhand,
  drawL1Iso_=drawL1Iso,
  drawL1Rlx_=drawL1Rlx,
  HThresh = '5'
  #legExtra = 'Tau 4x4'
 )

 compare_efficiencies(
  'nPVs',
  binPt,
  eff_rlx_eg_ntuple_4x4, eff_iso_eg_ntuple_4x4,eff_rlx_eg_ntuple_4x8_hcal1, eff_iso_eg_ntuple_4x8_hcal1,
  recoPtCut = '(recoPt >= '+str(recoPtVal)+')',
  l1PtCut = '(l1Pt >= '+str(l1ptVal)+')',
  #l1gPtCut = '(l1gRegionEt >= '+str(l1ptVal)+')',
  l1gPtCut = '(l1gPt >= '+str(l1ptVal)+')',
  # 12x12-4x4
  isoCut_4x4='(l1gPt>='+str(turnOffIso)+'||(l1gJetPt-l1gRegionEt)/l1gRegionEt<'+str(ISOTHRESHOLD_4x4)+')',
  #isoCut_4x8='(l1gPt>=60||(l1gJetPt-l1gRegionEt)/l1gRegionEt<'+str(ISOTHRESHOLD_4x8)+')',
  isoCut_4x8='(l1gPt>='+str(turnOffIso)+'||(l1gJetPt-l1gPt)/l1gPt<'+str(ISOTHRESHOLD_4x8)+')',
  #extraCut ='&&(decayMode == 10)',
  # 12x12 - 2x1
  #isoCut='(l1gPt[0]>=60||(l1gJetPt[0]-l1gPt[0])/l1gPt[0]<'+str(ISOTHRESHOLD)+')',
  drawUCTIso_4x4 = False,
  drawUCTRlx_4x4 = False,
  drawUCTIso_4x8 = False,
  drawUCTRlx_4x8 = True,
  drawUCTIso_byhand_=drawUCTIso_byhand,
  drawL1Iso_=drawL1Iso,
  drawL1Rlx_=drawL1Rlx,
  HThresh = '1'
  #legExtra = 'Tau 4x4'
 )

 compare_efficiencies(
  'nPVs',
  binPt,
  eff_rlx_eg_ntuple_4x4, eff_iso_eg_ntuple_4x4,eff_rlx_eg_ntuple_4x8_hcal2, eff_iso_eg_ntuple_4x8_hcal2,
  recoPtCut = '(recoPt >= '+str(recoPtVal)+')',
  l1PtCut = '(l1Pt >= '+str(l1ptVal)+')',
  #l1gPtCut = '(l1gRegionEt >= '+str(l1ptVal)+')',
  l1gPtCut = '(l1gPt >= '+str(l1ptVal)+')',
  # 12x12-4x4
  isoCut_4x4='(l1gPt>='+str(turnOffIso)+'||(l1gJetPt-l1gRegionEt)/l1gRegionEt<'+str(ISOTHRESHOLD_4x4)+')',
  #isoCut_4x8='(l1gPt>=60||(l1gJetPt-l1gRegionEt)/l1gRegionEt<'+str(ISOTHRESHOLD_4x8)+')',
  isoCut_4x8='(l1gPt>='+str(turnOffIso)+'||(l1gJetPt-l1gPt)/l1gPt<'+str(ISOTHRESHOLD_4x8)+')',
  #extraCut ='&&(decayMode == 10)',
  # 12x12 - 2x1
  #isoCut='(l1gPt[0]>=60||(l1gJetPt[0]-l1gPt[0])/l1gPt[0]<'+str(ISOTHRESHOLD)+')',
  drawUCTIso_4x4 = False,
  drawUCTRlx_4x4 = False,
  drawUCTIso_4x8 = False,
  drawUCTRlx_4x8 = True,
  drawUCTIso_byhand_=drawUCTIso_byhand,
  drawL1Iso_=drawL1Iso,
  drawL1Rlx_=drawL1Rlx,
  HThresh = '2'
  #legExtra = 'Tau 4x4'
 )
 compare_efficiencies(
  'nPVs',
  binPt,
  eff_rlx_eg_ntuple_4x4, eff_iso_eg_ntuple_4x4,eff_rlx_eg_ntuple_4x8_hcal3, eff_iso_eg_ntuple_4x8_hcal3,
  recoPtCut = '(recoPt >= '+str(recoPtVal)+')',
  l1PtCut = '(l1Pt >= '+str(l1ptVal)+')',
  #l1gPtCut = '(l1gRegionEt >= '+str(l1ptVal)+')',
  l1gPtCut = '(l1gPt >= '+str(l1ptVal)+')',
  # 12x12-4x4
  isoCut_4x4='(l1gPt>='+str(turnOffIso)+'||(l1gJetPt-l1gRegionEt)/l1gRegionEt<'+str(ISOTHRESHOLD_4x4)+')',
  #isoCut_4x8='(l1gPt>=60||(l1gJetPt-l1gRegionEt)/l1gRegionEt<'+str(ISOTHRESHOLD_4x8)+')',
  isoCut_4x8='(l1gPt>='+str(turnOffIso)+'||(l1gJetPt-l1gPt)/l1gPt<'+str(ISOTHRESHOLD_4x8)+')',
  #extraCut ='&&(decayMode == 10)',
  # 12x12 - 2x1
  #isoCut='(l1gPt[0]>=60||(l1gJetPt[0]-l1gPt[0])/l1gPt[0]<'+str(ISOTHRESHOLD)+')',
  drawUCTIso_4x4 = False,
  drawUCTRlx_4x4 = False,
  drawUCTIso_4x8 = False,
  drawUCTRlx_4x8 = True,
  drawUCTIso_byhand_=drawUCTIso_byhand,
  drawL1Iso_=drawL1Iso,
  drawL1Rlx_=drawL1Rlx,
  HThresh = '3'
  #legExtra = 'Tau 4x4'
 )
 compare_efficiencies(
  'nPVs',
  binPt,
  eff_rlx_eg_ntuple_4x4, eff_iso_eg_ntuple_4x4,eff_rlx_eg_ntuple_4x8_hcal4, eff_iso_eg_ntuple_4x8_hcal4,
  recoPtCut = '(recoPt >= '+str(recoPtVal)+')',
  l1PtCut = '(l1Pt >= '+str(l1ptVal)+')',
  #l1gPtCut = '(l1gRegionEt >= '+str(l1ptVal)+')',
  l1gPtCut = '(l1gPt >= '+str(l1ptVal)+')',
  # 12x12-4x4
  isoCut_4x4='(l1gPt>='+str(turnOffIso)+'||(l1gJetPt-l1gRegionEt)/l1gRegionEt<'+str(ISOTHRESHOLD_4x4)+')',
  #isoCut_4x8='(l1gPt>=60||(l1gJetPt-l1gRegionEt)/l1gRegionEt<'+str(ISOTHRESHOLD_4x8)+')',
  isoCut_4x8='(l1gPt>='+str(turnOffIso)+'||(l1gJetPt-l1gPt)/l1gPt<'+str(ISOTHRESHOLD_4x8)+')',
  #extraCut ='&&(decayMode == 10)',
  # 12x12 - 2x1
  #isoCut='(l1gPt[0]>=60||(l1gJetPt[0]-l1gPt[0])/l1gPt[0]<'+str(ISOTHRESHOLD)+')',
  drawUCTIso_4x4 = False,
  drawUCTRlx_4x4 = False,
  drawUCTIso_4x8 = False,
  drawUCTRlx_4x8 = True,
  drawUCTIso_byhand_=drawUCTIso_byhand,
  drawL1Iso_=drawL1Iso,
  drawL1Rlx_=drawL1Rlx,
  HThresh = '4'
  #legExtra = 'Tau 4x4'
 )
 compare_efficiencies(
  'nPVs',
  binPt,
  eff_rlx_eg_ntuple_4x4, eff_iso_eg_ntuple_4x4,eff_rlx_eg_ntuple_4x8_hcal5, eff_iso_eg_ntuple_4x8_hcal5,
  recoPtCut = '(recoPt >= '+str(recoPtVal)+')',
  l1PtCut = '(l1Pt >= '+str(l1ptVal)+')',
  #l1gPtCut = '(l1gRegionEt >= '+str(l1ptVal)+')',
  l1gPtCut = '(l1gPt >= '+str(l1ptVal)+')',
  # 12x12-4x4
  isoCut_4x4='(l1gPt>='+str(turnOffIso)+'||(l1gJetPt-l1gRegionEt)/l1gRegionEt<'+str(ISOTHRESHOLD_4x4)+')',
  #isoCut_4x8='(l1gPt>=60||(l1gJetPt-l1gRegionEt)/l1gRegionEt<'+str(ISOTHRESHOLD_4x8)+')',
  isoCut_4x8='(l1gPt>='+str(turnOffIso)+'||(l1gJetPt-l1gPt)/l1gPt<'+str(ISOTHRESHOLD_4x8)+')',
  #extraCut ='&&(decayMode == 10)',
  # 12x12 - 2x1
  #isoCut='(l1gPt[0]>=60||(l1gJetPt[0]-l1gPt[0])/l1gPt[0]<'+str(ISOTHRESHOLD)+')',
  drawUCTIso_4x4 = False,
  drawUCTRlx_4x4 = False,
  drawUCTIso_4x8 = False,
  drawUCTRlx_4x8 = True,
  drawUCTIso_byhand_=drawUCTIso_byhand,
  drawL1Iso_=drawL1Iso,
  drawL1Rlx_=drawL1Rlx,
  HThresh = '5'
  #legExtra = 'Tau 4x4'
 )

#make_res_nrml(eff_rlx_eg_ntuple_4x4, eff_iso_eg_ntuple_4x4,eff_rlx_eg_ntuple_4x8,eff_iso_eg_ntuple_4x8,'recoPt', 'l1Pt', 'l1gPt', binRes, cutPtVarg='l1gPt',cutPtVar='l1Pt',cutPt=l1ptVal,filename='')

#make_iso_nrml(eff_rlx_eg_ntuple_4x4, eff_iso_eg_ntuple_4x4,eff_rlx_eg_ntuple_4x8,eff_iso_eg_ntuple_4x8,'recoPt', 'l1Pt', 'l1gPt', binIso, cutPtVarg='l1gPt',cutPtVar='l1Pt',cutPt=l1ptVal,filename='')
 
 #compare_efficiencies(
 #'nPVs',
 #binVert,
 #eff_rlx_eg_ntuple, eff_iso_eg_ntuple,
 #recoPtCut = '(recoPt >= '+str(recoPtVal)+')',
 #l1PtCut = '(l1Pt >= '+str(l1ptVal)+')',
 #l1gPtCut = '(l1gPt >= '+str(l1ptVal)+')',
 #isoCut='(l1gPt>=60||(l1gJetPt-l1gPt)/l1gPt<'+str(ISOTHRESHOLD)+')',
 #drawUCTIso_=drawUCTIso,
 #drawUCTRlx_=drawUCTRlx,
 #drawUCTIso_byhand_=drawUCTIso_byhand,
 #drawL1Iso_=drawL1Iso,
 #drawL1Rlx_=drawL1Rlx,
 #legExtra='Reco Pt > '+str(recoPtVal)
#)
