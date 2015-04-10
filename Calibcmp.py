from sys import argv
import ROOT

var =argv[1]

ROOT.gROOT.LoadMacro("tdrstyle.C")
ROOT.setTDRStyle()

ROOT.gROOT.SetStyle("Plain")
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)


canvas = ROOT.TCanvas("canvas","canvas",800,800)
canvas.SetLogy(True)

NewCalib_file_str = "March25LutTests/tau_emul_rateMarch25NewCalibNewLUTIsoPoint1.root"
#NewCalib_file_str = "March25LutTests/tau_emul_rate_April1_72X_NewCalibPoint1Iso.root"
#OldCalib_file_str = "March25LutTests/tau_emul_rate_April1_72X_OldCalibPoint1Iso.root"
OldCalib_file_str = "March25LutTests/tau_emul_rateMarch25OldCalibNewLUTIsoPoint1.root"

NewCalibFile = ROOT.TFile(NewCalib_file_str) 
OldCalibFile = ROOT.TFile(OldCalib_file_str)

histSpot = "TauEmul/Ntuple"

OldCalib = OldCalibFile.Get(histSpot)
NewCalib = NewCalibFile.Get(histSpot)

binPt = [25,0,100]
draw_string = var + " >> htemp(%s)" % (", ".join(str(x) for x in binPt))
eta0CutStr = "eta[0]>-2.5&&eta[0]<2.5"
eta1CutStr = eta0CutStr + "&&eta[1]>-2.5&&eta[1]<2.5"
NewCalib.Draw(draw_string,eta1CutStr,"goff")
histoNew = ROOT.gDirectory.Get("htemp").Clone()
OldCalib.Draw(draw_string,eta1CutStr,"goff")
histoOld = ROOT.gDirectory.Get("htemp").Clone()

histoOld.SetLineWidth(3)
histoOld.SetLineColor(ROOT.EColor.kRed)
histoNew.SetLineWidth(3)
histoNew.SetLineColor(ROOT.EColor.kBlue)

histoOld.Draw("hist")
histoNew.Draw("sameshist")

histoOldMax = histoOld.GetMaximum()
histoNewMax = histoNew.GetMaximum()

maxHist = max(histoOldMax,histoNewMax)
maxHist = 1.5*maxHist

histoOld.GetYaxis().SetRangeUser(100,maxHist)

histoOld.GetXaxis().SetTitle(var)

legend = ROOT.TLegend(0.43,0.60,0.93,0.97,' ','brNDC')

legend.AddEntry(histoOld,"Old Calib")
legend.AddEntry(histoNew,"New Calib")

legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.SetFillStyle(0)
legend.SetTextSize(0.03)
legend.Draw("sames")

canvas.SaveAs("March25LutTests/Plots/CalibPtEta1CutCmp_"+var+".png")
for i in range (1, histoNew.GetNbinsX()+1):
	diff = histoNew.GetBinContent(i) - histoOld.GetBinContent(i)
	binName = str((i-1)*4)
	print "new-old at " + binName + " GeV = " + str(diff)
