'''
Makes optionally EG efficiency, rate and resolution plots
Authors: T.M.Perry, E.K.Friis, M.Cepeda, A.G.Levine, N.Woods UW Madison
'''
from sys import argv, stdout, stderr
import ROOT


##################
# Set Parameters #
##################
LIso=3
LSB=50
l1ptVal=argv[1]
rate_ntuple_str=argv[2]
name=argv[3]
#name = "72XIsoTestNewCalibPoint15Iso_"
recoPtVal=0
L1_CALIB_FACTOR = 1.0
L1G_CALIB_FACTOR = 1.0
#ZEROBIAS_RATE=15000000.00
ZEROBIAS_RATE = 5623.0*2590.0 #frequency X bunches
#saveWhere = 'March25LutTests/Plots/'+str(name)+str(l1ptVal)
saveWhere = 'RCTV2CalibNtuples_FullStatsApril28/Plots/'+str(name)+str(l1ptVal)

#rate plot
rateLine = True # line at recoPtVal
#######
# File #
########
#Rate
#rate_ntuple = 'EactHactTaus_June13/ECAL3/tau_rate_4x8_E3H3_NoNeighborSeed.root'
#rate_ntuple = 'uct_rate_tree_numEvent5000.root'
#rate_ntuple_str = 'EmulatorTestingNov/tau_emul_rateDoublingNoFixRlxDec4.root'
#rate_iso_ntuple_str = 'EmulatorTestingNov/tau_emul_rateDoublingNoFixIsoDec4.root'
#rate_ntuple_str = "tau_emul_rateJan10RlxNoTauVeto.root"
#rate_rlx_veto_ntuple_str = "tau_emul_rateJan10RlxWithTauVeto.root"
#rate_iso_ntuple_str = "tau_emul_rateJan10IsoWithTauVeto.root"
#rate_ntuple_str = "tau_emul_rateFeb17RlxNoTauVetoNewCalib.root"
rate_rlx_veto_ntuple_str = "tau_emul_rateFeb17RlxTauVetoNewCalib.root"
#rate_iso_ntuple_str = "tau_emul_rateFeb17IsoTauVetoNewCalib.root"
#rate_iso_ntuple_str = "tau_emul_rateMarch10IsoTauVetoNewCalibPoint2EventCapTest.root"
rate_iso_ntuple_str = "March25LutTests/tau_emul_rate_April1_72X_NewCalibPoint15Iso.root"
#rate_ntuple_str = "tau_emul_rateFeb4RlxNoTauVetoCheck.root"
#rate_rlx_veto_ntuple_str = "tau_emul_rateFeb4RlxTauVetoCheck.root"
#rate_iso_ntuple_str = "tau_emul_rateFeb4IsoTauVetoCheck.root"
#rate_ntuple_str = "March25LutTests/tau_emul_rateMarch25IsoPoint1.root"
#rate_ntuple_str = "March25LutTests/tau_emul_rateMarch25NewCalibIsoPoint1.root"
#rate_ntuple_str = "March25LutTests/tau_emul_rateMarch25NewCalibNewLUTIsoPoint2.root"


rate_ntuple_NoDoubling_str = 'EmulatorTestingNov/tau_emul_rateDoublingFixRlxDec4.root'
rate_iso_ntuple_NoDoubling_str = 'EmulatorTestingNov/tau_emul_rateDoublingFixIsoDec4.root'
rate_ntuple_file = ROOT.TFile(rate_ntuple_str)
rate_iso_ntuple_file = ROOT.TFile(rate_iso_ntuple_str)
rate_rlx_veto_ntuple_file = ROOT.TFile(rate_rlx_veto_ntuple_str)
rate_ntuple_NoDoubling_file = ROOT.TFile(rate_ntuple_NoDoubling_str)
rate_iso_ntuple_NoDoubling_file = ROOT.TFile(rate_iso_ntuple_NoDoubling_str)


# UCT
rate_spot = 'TauEmul/Ntuple'
rate_iso_spot = 'TauEmulIso/Ntuple'
#rate_ntuple = rate_ntuple_file.Get(rate_spot)
#rate_iso_ntuple = rate_iso_ntuple_file.Get(rate_spot)
rate_rlx_veto_ntuple = rate_rlx_veto_ntuple_file.Get(rate_spot)
rate_ntuple = rate_ntuple_file.Get(rate_spot)
rate_iso_ntuple = rate_ntuple_file.Get(rate_iso_spot)
rate_ntuple_NoDoubling = rate_ntuple_NoDoubling_file.Get(rate_spot)
rate_iso_ntuple_NoDoubling = rate_iso_ntuple_NoDoubling_file.Get(rate_spot)
rateEntries = rate_ntuple.GetEntries()
store = ROOT.TFile(saveWhere+'.root','RECREATE')

#rate_ntuple.AddFriend(rate_ntuple_NoDoubling,"rlxNoDoub")
#print "????" + str(rate_ntuple.GetFriendAlias(rate_ntuple_NoDoubling))
#rate_ntuple.Scan("pt[0]:pt[1]:rlxNoDoub.pt[0]:rlxNoDoub.pt[1]",'(eta[0] > -2.5 && eta[0] < 2.5&&eta[1] > -2.5 && eta[1] < 2.5&&pt[0]>0&&pt[1]>0)&&(pt[0]!=rlxNoDoub.pt[0]||pt[1]!=rlxNoDoub.pt[1])')

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


canvas = ROOT.TCanvas("asdf", "adsf", 800, 800)

def make_plot(tree, variable, selection, binning, xaxis='', title='',calFactor=1):
 ''' Plot a variable using draw and return the histogram '''
 draw_string = "%s * %0.2f>>htemp(%s)" % (variable,calFactor, ", ".join(str(x) for x in binning))
 print draw_string
 tree.Draw(draw_string, selection, "goff")
 print tree.GetEntries()
 output_histo = ROOT.gDirectory.Get("htemp").Clone()
 output_histo.GetXaxis().SetTitle(xaxis)
 output_histo.SetTitle(title)
 print output_histo.GetEntries()
 print output_histo.Integral()
 return output_histo

######################################################################
##### RATES ##########################################################
######################################################################
def make_l1_rate(pt, color=ROOT.EColor.kBlack, marker=20):
 ''' Make a rate plot out of L1Extra Pts '''
 numBins = pt.GetXaxis().GetNbins()
 rate = pt.Clone()
 print "Entries" + str(pt.GetEntries())
 for i in range(1,numBins):
  print pt.Integral(i,numBins)
  rate.SetBinContent(i,pt.Integral(i,numBins))
 rate.SetLineColor(color)
 rate.SetMarkerStyle(marker)
 rate.SetMarkerColor(color)
 return rate

def rate_histo(ntuple,cut,binning,calibfactor,scale,color,marker,leg,title,line,ptLine,w,s):
 print "rate_histo info"
 print ntuple.GetEntries()
 print cut
 print binning
 print calibfactor
 #pt = make_plot(ntuple,'regionPt[0]',cut,binning,'','',calibfactor)
 #let's do this in a really inefficient way
 '''
 cut0 = cut + '&&pt[1] < 20'
 cut20IB = cut + '&&pt[1] >= 20 &&pt[1] < 24 && abs(eta[1]) <0.9'
 cut20OB = cut + '&&pt[1] >= 20 &&pt[1] < 24 && abs(eta[1]) <1.4 && abs(eta[1])>=0.9'
 cut20E = cut + '&&pt[1] >= 20  &&pt[1] < 24  && abs(eta[1]) <2.5 && abs(eta[1])>=1.4'
 cut24IB = cut + '&&pt[1] >= 24 &&pt[1] < 28 && abs(eta[1]) <0.9'
 cut24OB = cut + '&&pt[1] >= 24 &&pt[1] < 28 && abs(eta[1]) <1.4 && abs(eta[1])>=0.9'
 cut24E = cut + '&&pt[1] >= 24  &&pt[1] < 28  && abs(eta[1]) <2.5 && abs(eta[1])>=1.4'
 cut28IB = cut + '&&pt[1] >= 28 &&pt[1] < 32 && abs(eta[1]) <0.9'
 cut28OB = cut + '&&pt[1] >= 28 &&pt[1] < 32 && abs(eta[1]) <1.4 && abs(eta[1])>=0.9'
 cut28E = cut + '&&pt[1] >= 28  &&pt[1] < 32  && abs(eta[1]) <2.5 && abs(eta[1])>=1.4'
 cut32IB = cut + '&&pt[1] >= 32 &&pt[1] < 36 && abs(eta[1]) <0.9'
 cut32OB = cut + '&&pt[1] >= 32 &&pt[1] < 36 && abs(eta[1]) <1.4 && abs(eta[1])>=0.9'
 cut32E = cut + '&&pt[1] >= 32  &&pt[1] < 36  && abs(eta[1]) <2.5 && abs(eta[1])>=1.4'
 cut36IB = cut + '&&pt[1] >= 36 &&pt[1] < 40 && abs(eta[1]) <0.9'
 cut36OB = cut + '&&pt[1] >= 36 &&pt[1] < 40 && abs(eta[1]) <1.4 && abs(eta[1])>=0.9'
 cut36E = cut + '&&pt[1] >= 36  &&pt[1] < 40  && abs(eta[1]) <2.5 && abs(eta[1])>=1.4'
 cut40IB = cut + '&&pt[1] >= 40 &&pt[1] < 44 && abs(eta[1]) <0.9'
 cut40OB = cut + '&&pt[1] >= 40 &&pt[1] < 44 && abs(eta[1]) <1.4 && abs(eta[1])>=0.9'
 cut40E = cut + '&&pt[1] >= 40  &&pt[1] < 44  && abs(eta[1]) <2.5 && abs(eta[1])>=1.4'
 cut44IB = cut + '&&pt[1] >= 44 &&pt[1] < 48 && abs(eta[1]) <0.9'
 cut44OB = cut + '&&pt[1] >= 44 &&pt[1] < 48 && abs(eta[1]) <1.4 && abs(eta[1])>=0.9'
 cut44E = cut + '&&pt[1] >= 44  &&pt[1] < 48  && abs(eta[1]) <2.5 && abs(eta[1])>=1.4'
 cut48IB = cut + '&&pt[1] >= 48 &&pt[1] < 52 && abs(eta[1]) <0.9'
 cut48OB = cut + '&&pt[1] >= 48 &&pt[1] < 52 && abs(eta[1]) <1.4 && abs(eta[1])>=0.9'
 cut48E = cut + '&&pt[1] >= 48  &&pt[1] < 52  && abs(eta[1]) <2.5 && abs(eta[1])>=1.4'
 cut52IB = cut + '&&pt[1] >= 52 &&pt[1] < 56 && abs(eta[1]) <0.9'
 cut52OB = cut + '&&pt[1] >= 52 &&pt[1] < 56 && abs(eta[1]) <1.4 && abs(eta[1])>=0.9'
 cut52E = cut + '&&pt[1] >= 52  &&pt[1] < 56  && abs(eta[1]) <2.5 && abs(eta[1])>=1.4'
 cutInf = cut + '&& pt[1] >= 56'
 
 pt_0 = make_plot(ntuple, 'pt[1]', cut0,binning,'','',calibfactor)
 pt_20IB = make_plot(ntuple,'pt[1]',cut20IB,binning,'','',1.404)
 pt_20OB = make_plot(ntuple,'pt[1]',cut20OB,binning,'','',1.361)
 pt_20E = make_plot(ntuple,'pt[1]',cut20E,binning,'','',1.304)
 pt_24IB = make_plot(ntuple,'pt[1]',cut24IB,binning,'','',1.314)
 pt_24OB = make_plot(ntuple,'pt[1]',cut24OB,binning,'','',1.267)
 pt_24E = make_plot(ntuple,'pt[1]',cut24E,binning,'','',1.231)
 pt_28IB = make_plot(ntuple,'pt[1]',cut28IB,binning,'','',1.255)
 pt_28OB = make_plot(ntuple,'pt[1]',cut28OB,binning,'','',1.208)
 pt_28E = make_plot(ntuple,'pt[1]',cut28E,binning,'','',1.185)
 pt_32IB = make_plot(ntuple,'pt[1]',cut32IB,binning,'','',1.204)
 pt_32OB = make_plot(ntuple,'pt[1]',cut32OB,binning,'','',1.153)
 pt_32E = make_plot(ntuple,'pt[1]',cut32E,binning,'','',1.131)
 pt_36IB = make_plot(ntuple,'pt[1]',cut36IB,binning,'','',1.163)
 pt_36OB = make_plot(ntuple,'pt[1]',cut36OB,binning,'','',1.122)
 pt_36E = make_plot(ntuple,'pt[1]',cut36E,binning,'','',1.090)
 pt_40IB = make_plot(ntuple,'pt[1]',cut40IB,binning,'','',1.132)
 pt_40OB = make_plot(ntuple,'pt[1]',cut40OB,binning,'','',1.091)
 pt_40E = make_plot(ntuple,'pt[1]',cut40E,binning,'','',1.070)
 pt_44IB = make_plot(ntuple,'pt[1]',cut44IB,binning,'','',1.101)
 pt_44OB = make_plot(ntuple,'pt[1]',cut44OB,binning,'','',1.050)
 pt_44E = make_plot(ntuple,'pt[1]',cut44E,binning,'','',1.040)
 pt_48IB = make_plot(ntuple,'pt[1]',cut48IB,binning,'','',1.081)
 pt_48OB = make_plot(ntuple,'pt[1]',cut48OB,binning,'','',1.020)
 pt_48E = make_plot(ntuple,'pt[1]',cut48E,binning,'','',1.020)
 pt_52IB = make_plot(ntuple,'pt[1]',cut52IB,binning,'','',1.050)
 pt_52OB = make_plot(ntuple,'pt[1]',cut52OB,binning,'','',1.000)
 pt_52E = make_plot(ntuple,'pt[1]',cut52E,binning,'','',1.010)
 pt_Inf = make_plot(ntuple,'pt[1]',cutInf,binning,'','',calibfactor)
 
 pt_0 = make_plot(ntuple, 'pt[1]', cut0,binning,'','',calibfactor)
 pt_20IB = make_plot(ntuple,'pt[1]',cut20IB,binning,'','',1.253)
 pt_20OB = make_plot(ntuple,'pt[1]',cut20OB,binning,'','',1.205)
 pt_20E = make_plot(ntuple,'pt[1]',cut20E,binning,'','',1.185)
 pt_24IB = make_plot(ntuple,'pt[1]',cut24IB,binning,'','',1.185)
 pt_24OB = make_plot(ntuple,'pt[1]',cut24OB,binning,'','',1.153)
 pt_24E = make_plot(ntuple,'pt[1]',cut24E,binning,'','',1.132)
 pt_28IB = make_plot(ntuple,'pt[1]',cut28IB,binning,'','',1.131)
 pt_28OB = make_plot(ntuple,'pt[1]',cut28OB,binning,'','',1.070)
 pt_28E = make_plot(ntuple,'pt[1]',cut28E,binning,'','',1.081)
 pt_32IB = make_plot(ntuple,'pt[1]',cut32IB,binning,'','',1.090)
 pt_32OB = make_plot(ntuple,'pt[1]',cut32OB,binning,'','',1.061)
 pt_32E = make_plot(ntuple,'pt[1]',cut32E,binning,'','',1.050)
 pt_36IB = make_plot(ntuple,'pt[1]',cut36IB,binning,'','',1.060)
 pt_36OB = make_plot(ntuple,'pt[1]',cut36OB,binning,'','',1.030)
 pt_36E = make_plot(ntuple,'pt[1]',cut36E,binning,'','',1.030)
 pt_40IB = make_plot(ntuple,'pt[1]',cut40IB,binning,'','',1.040)
 pt_40OB = make_plot(ntuple,'pt[1]',cut40OB,binning,'','',1.010)
 pt_40E = make_plot(ntuple,'pt[1]',cut40E,binning,'','',1.020)
 pt_44IB = make_plot(ntuple,'pt[1]',cut44IB,binning,'','',1.010)
 pt_44OB = make_plot(ntuple,'pt[1]',cut44OB,binning,'','',0.990)
 pt_44E = make_plot(ntuple,'pt[1]',cut44E,binning,'','',1.000)
 pt_48IB = make_plot(ntuple,'pt[1]',cut48IB,binning,'','',0.990)
 pt_48OB = make_plot(ntuple,'pt[1]',cut48OB,binning,'','',0.967)
 pt_48E = make_plot(ntuple,'pt[1]',cut48E,binning,'','',0.970)
 pt_52IB = make_plot(ntuple,'pt[1]',cut52IB,binning,'','',0.970)
 pt_52OB = make_plot(ntuple,'pt[1]',cut52OB,binning,'','',0.950)
 pt_52E = make_plot(ntuple,'pt[1]',cut52E,binning,'','',0.980)
 pt_Inf = make_plot(ntuple,'pt[1]',cutInf,binning,'','',calibfactor)

 
 pt_0 = make_plot(ntuple, 'pt[1]', cut0,binning,'','',1.0)
 pt_20IB = make_plot(ntuple,'pt[1]',cut20IB,binning,'','',1.0)
 pt_20OB = make_plot(ntuple,'pt[1]',cut20OB,binning,'','',1.0)
 pt_20E = make_plot(ntuple,'pt[1]',cut20E,binning,'','',1.0)
 pt_24IB = make_plot(ntuple,'pt[1]',cut24IB,binning,'','',1.0)
 pt_24OB = make_plot(ntuple,'pt[1]',cut24OB,binning,'','',1.0)
 pt_24E = make_plot(ntuple,'pt[1]',cut24E,binning,'','',1.0)
 pt_28IB = make_plot(ntuple,'pt[1]',cut28IB,binning,'','',1.0)
 pt_28OB = make_plot(ntuple,'pt[1]',cut28OB,binning,'','',1.0)
 pt_28E = make_plot(ntuple,'pt[1]',cut28E,binning,'','',1.0)
 pt_32IB = make_plot(ntuple,'pt[1]',cut32IB,binning,'','',1.0)
 pt_32OB = make_plot(ntuple,'pt[1]',cut32OB,binning,'','',1.0)
 pt_32E = make_plot(ntuple,'pt[1]',cut32E,binning,'','',1.0)
 pt_36IB = make_plot(ntuple,'pt[1]',cut36IB,binning,'','',1.0)
 pt_36OB = make_plot(ntuple,'pt[1]',cut36OB,binning,'','',1.0)
 pt_36E = make_plot(ntuple,'pt[1]',cut36E,binning,'','',1.0)
 pt_40IB = make_plot(ntuple,'pt[1]',cut40IB,binning,'','',1.0)
 pt_40OB = make_plot(ntuple,'pt[1]',cut40OB,binning,'','',1.0)
 pt_40E = make_plot(ntuple,'pt[1]',cut40E,binning,'','',1.0)
 pt_44IB = make_plot(ntuple,'pt[1]',cut44IB,binning,'','',1.0)
 pt_44OB = make_plot(ntuple,'pt[1]',cut44OB,binning,'','',1.0)
 pt_44E = make_plot(ntuple,'pt[1]',cut44E,binning,'','',1.0)
 pt_48IB = make_plot(ntuple,'pt[1]',cut48IB,binning,'','',1.0)
 pt_48OB = make_plot(ntuple,'pt[1]',cut48OB,binning,'','',1.0)
 pt_48E = make_plot(ntuple,'pt[1]',cut48E,binning,'','',1.0)
 pt_52IB = make_plot(ntuple,'pt[1]',cut52IB,binning,'','',1.0)
 pt_52OB = make_plot(ntuple,'pt[1]',cut52OB,binning,'','',1.0)
 pt_52E = make_plot(ntuple,'pt[1]',cut52E,binning,'','',1.0)
 pt_Inf = make_plot(ntuple,'pt[1]',cutInf,binning,'','',1.0)
 
 pt = pt_0.Clone()
 pt.Add(pt_20IB,1)
 pt.Add(pt_20OB,1)
 pt.Add(pt_20E,1)
 pt.Add(pt_24IB,1)
 pt.Add(pt_24OB,1)
 pt.Add(pt_24E,1)
 pt.Add(pt_28IB,1)
 pt.Add(pt_28OB,1)
 pt.Add(pt_28E,1)
 pt.Add(pt_32IB,1)
 pt.Add(pt_32OB,1)
 pt.Add(pt_32E,1)
 pt.Add(pt_36IB,1)
 pt.Add(pt_36OB,1)
 pt.Add(pt_36E,1)
 pt.Add(pt_40IB,1)
 pt.Add(pt_40OB,1)
 pt.Add(pt_40E,1)
 pt.Add(pt_44IB,1)
 pt.Add(pt_44OB,1)
 pt.Add(pt_44E,1)
 pt.Add(pt_48IB,1)
 pt.Add(pt_48OB,1)
 pt.Add(pt_48E,1)
 pt.Add(pt_52IB,1)
 pt.Add(pt_52OB,1)
 pt.Add(pt_52E,1)
 pt.Add(pt_Inf,1)
 '''
 pt = make_plot(ntuple,'pt[1]',cut,binning,'','',calibfactor)
 print "ptEntries: " + str(pt.GetEntries())
 rate = make_l1_rate(pt,color,marker)
 rate.Scale(scale)
 rate.Draw('phsame')
 leg.AddEntry(rate,title,'pe')
 maxx = rate.GetMaximum()
 binn = rate.GetXaxis().FindBin(ptLine)
 rateVal = rate.GetBinContent(binn)
 print "rateVal : " + str(rateVal)
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
 print cut
 return rate,maxx,vert,hor,rateVal

def make_rate_plot(
 binning,
 ntuple=None,
 ntuple_iso=None,
 ntuple_rlx_veto=None,
 ntuple_NoDoubling=None,
 ntuple_NoDoublingIso=None,
 filename='',
 setLOG=True,
 line=True,
 ptLine=20
 ):

 info = ''
 #scale = ZEROBIAS_RATE/ntuple.GetEntries()
 scale = ZEROBIAS_RATE/rateEntries
 print "scale" + str(scale)
 print(ntuple.GetEntries())
 
 canvas.SetLogy(setLOG)
 frame = ROOT.TH1F('frame','frame',*binning)
 frame.Draw()
 frame.SetTitle('')
 frame.GetYaxis().SetTitle('Hz (13TeV,7E33)')
 frame.GetXaxis().SetTitle('p_{T}')
 tex.DrawLatex(0.1,0.91,'DiTau Rate')
 tex.SetTextSize(0.03)
 tex.SetTextAlign(31)
 tex.DrawLatex(0.9,0.91,'CMS Preliminary')
 tex.SetTextSize(0.07)
 tex.SetTextAlign(11)
 legend = ROOT.TLegend(0.4,0.6,0.89,0.89,'','brNDC')
 legend.SetFillColor(0)
 legend.SetBorderSize(0)
 #legend.SetHeader("DiTau Rate")


 max_ntuple=1
 cut='(eta[0] > -2.5 && eta[0] < 2.5&&eta[1] > -2.5 && eta[1] < 2.5&&pt[0]>0&&pt[1]>0)'
 h_L1_rlx,max_L1_rlx,vert_L1_rlx,hor_L1_rlx,rateValRlx = rate_histo(
   ntuple,cut,binning,L1G_CALIB_FACTOR,
   scale,ROOT.EColor.kGreen+3,20,legend,
   'Tau Rate Rlx', line,ptLine,3,3)
 print "done with rlx"
 #h_L1_rlx_veto,max_L1_rlx_veto,vert_L1_rlx_veto,hor_L1_rlx_veto,rateValRlxVeto= rate_histo(
 #  ntuple_rlx_veto,cut,binning,L1G_CALIB_FACTOR,
 #  scale,ROOT.EColor.kRed,20,legend,
 #  'Tau Rate Rlx (With Tau Veto)', line,ptLine,3,3)
 #print "done with rlx veto"
 h_L1_iso,max_L1_iso,vert_L1_iso,hor_L1_iso,rateValIso = rate_histo(
   ntuple_iso,cut,binning,L1G_CALIB_FACTOR,
   scale,ROOT.EColor.kBlue,20,legend,
   'Tau Rate Iso', line,ptLine,3,3)
 print "done with iso"
 #h_L1_rlx_NoDouble,max_L1_rlx_NoDouble,vert_L1_rlx_NoDouble,hor_L1_rlx_NoDouble,rateValRlxFix = rate_histo(
 #  ntuple_NoDoubling,cut,binning,L1G_CALIB_FACTOR,
 #  scale,ROOT.EColor.kMagenta+3,25,legend,
 #  'Tau Rate Double Counting Fix Rlx', line,ptLine,3,3)
 #h_L1_iso_NoDouble,max_L1_iso_NoDouble,vert_L1_iso_NoDouble,hor_L1_iso_NoDouble,rateValIsoFix = rate_histo(
 #  ntuple_NoDoublingIso,cut,binning,L1G_CALIB_FACTOR,
 #  scale,ROOT.EColor.kBlue-1,25,legend,
 #  'Tau Rate Double Counting Fix Iso', line,ptLine,3,3)

 frame.SetMaximum(3E7)
 #frame.SetMaximum(5*max(max_UCT_rlx,max_UCT_iso,max_UCT_isoByHand,max_L1_rlx,max_L1_iso))
 frame.SetMinimum(1E3)
 legend.Draw()
 latex = ROOT.TLatex()
 latex.SetNDC()
 latex.SetTextSize(0.03)
 latex.SetTextAlign(31)
 latexStrRlx= "Rlx Rate :  %.2f kHz "%(rateValRlx/1000)
 #latexStrRlxVeto = "Rlx Rate (With Veto) :  %.2f kHz "%(rateValRlxVeto/1000)
 latexStrIso = "Iso Rate :  %.2f kHz "%(rateValIso/1000)
 #latexStrRlxFix = "Rlx Rate (New) : %.2f kHz"%(rateValRlxFix/1000)
 #latexStrIsoFix = "Iso Rate (New) : %.2f kHz"%(rateValIsoFix/1000) 
 
 latex.SetTextAlign(11)
 latex.DrawLatex(0.55,0.55,latexStrRlx)
 #latex.DrawLatex(0.55,0.5,latexStrRlxVeto)
 latex.DrawLatex(0.55,0.45,latexStrIso)
 #latex.DrawLatex(0.55,0.4,latexStrIsoFix)
 canvas.SaveAs(saveWhere+info+'.png')
######################################################################
##### RATES ##########################################################
######################################################################

######################################################################
###### DRAW PLOTS ####################################################
######################################################################
##############
# Rate Plots #
##############
binRate = [25,0,100]


make_rate_plot(
binRate,
ntuple=rate_ntuple,
ntuple_iso=rate_iso_ntuple,
ntuple_rlx_veto=rate_rlx_veto_ntuple,
ntuple_NoDoubling=rate_ntuple_NoDoubling,
ntuple_NoDoublingIso=rate_iso_ntuple_NoDoubling,
filename='',
setLOG=True,
line=rateLine,
ptLine= float(l1ptVal)
)
