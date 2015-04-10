'''
Makes Tau efficiency plots
Authors: T.M.Perry, E.K.Friis, M.Cepeda, A.G.Levine, N.Woods UW Madison
'''
from sys import argv, stdout, stderr
import ROOT
import sys


##################
# Set Parameters #
##################
eff_ntuple = ' '
LIso=3
LSB=50
recoPtVal=20
L1_CALIB_FACTOR = 1.0
L1G_CALIB_FACTOR = 1.0
ZEROBIAS_RATE=11246.0*2590.0 #frequency X bunches
saveWhere = 'EmulatorTestingNov/EffiTest'


########
# File #
########
#Efficiency
#eff_ntuple = 'EactHactTaus_June13/ECAL3/tau_eff_4x8_E3H3_NoNeighborSeed.root'
#eff_ntuple = 'uct_efficiency_tree_numEvent5000.root'
eff_ntuple_file = ROOT.TFile(eff_ntuple)
#
eff_spot = 'DiTauEfficiency/Ntuple'
eff_ntuple = eff_ntuple_file.Get(eff_spot)
store = ROOT.TFile(saveWhere+'.root','RECREATE')

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
 efi = make_2D_l1_efficiency(denom,num)
 leg.AddEntry(efi,title,'pe')
 efi.Draw('colz')
 efi.GetXaxis().SetTitle("Tau 2")
 efi.GetYaxis().SetTitle("Tau 1")
 efi.GetYaxis().SetTitleOffset(1.3)

 tex = ROOT.TLatex()
 tex.SetNDC(True)
 tex.SetTextSize(0.04)
 isoStr = "No ISO"
 pTStr = "L1 PT > %0.0f"%(float(l1ptVal))
 cutStr = isoStr +", "+pTStr+", "+ selectionStr

 tex.DrawLatex(0.1,0.91,cutStr)
 tex.SetTextAlign(31)
 for i in range (1,efiHist.GetNbinsX()):
	print efiHist.GetBinContent(i)
 return efi

def compare_efficiencies(
 variable,
 binning,
 ntuple,
 recoPtCut='(1)',l1PtCut='(1)',l1gPtCut='(1)',
 isoCut='(1)', isoCut4x4 = '(1)',extraCut = '&&(1)',
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
 
 frame = ROOT.TH1F('frame','frame',20,0,100)
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
 else: frame.GetXaxis().SetTitle(variable)
 frame.GetXaxis().SetRangeUser(0,100)
 #tex.DrawLatex(0.1,0.91,'Tau '+variable+' Efficiency')
 #tex.SetTextSize(0.03)
 #tex.DrawLatex(0.1,0.87,'CMS Preliminary')
 #tex.SetTextSize(0.07)
 legend = ROOT.TLegend(0.13,0.65,0.45,0.85,'','brNDC')
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
  'pt[0]:pt[1]',
  bin2DPt,
  eff_rlx_eg_ntuple, eff_iso_eg_ntuple,
  eff_rlx_eg_ntuple4x4, eff_iso_eg_ntuple4x4,
  recoPtCut = '(pt[0] >= '+str(recoPtVal)+')&&(pt[1] >= '+str(recoPtVal)+')',
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
