import ROOT
from sys import argv, stdout, stderr


ROOT.gROOT.SetStyle("Plain")
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

canvas = ROOT.TCanvas("canvas","canvas",800,800)

Signal12x12 = ROOT.TH2F("Signal12x12","Signa12x12",3,-1,1,3,-1,1)
#Signal12x12.SetBinContent(1,1,0.42357)
#Signal12x12.SetBinContent(1,2,0.5658)
#Signal12x12.SetBinContent(1,3,0.4480)
#Signal12x12.SetBinContent(2,1,1.186619)
#Signal12x12.SetBinContent(2,2,9.88235)
#Signal12x12.SetBinContent(2,3,1.8910522)
#Signal12x12.SetBinContent(3,1,0.43454)
#Signal12x12.SetBinContent(3,2,0.59299)
#Signal12x12.SetBinContent(3,3,0.43164)


Signal12x12.SetBinContent(1,1,0.63423309)
Signal12x12.SetBinContent(1,2,0.8700857)
Signal12x12.SetBinContent(1,3,0.5941886)
Signal12x12.SetBinContent(2,1,1.186619)
Signal12x12.SetBinContent(2,2,21.31597332)
Signal12x12.SetBinContent(2,3,1.7238488)
Signal12x12.SetBinContent(3,1,0.55287393)
Signal12x12.SetBinContent(3,2,0.8804064)
Signal12x12.SetBinContent(3,3,0.6298825)

Signal12x12.GetXaxis().SetTitle("#eta")
Signal12x12.GetYaxis().SetTitle("#phi")
Signal12x12.GetXaxis().SetLabelSize(0)
Signal12x12.GetXaxis().SetNdivisions(0)
Signal12x12.GetYaxis().SetLabelSize(0)
Signal12x12.GetYaxis().SetNdivisions(0)
Signal12x12.Draw("LEGO")
Signal12x12.GetZaxis().SetLabelSize(0.02)
#Vert1 = ROOT.TLine(-0.333333,-1.0,-0.333333,1.0)
#Vert1.Draw("sames")
#Vert2 = ROOT.TLine(0.333333,-1.0,0.333333,1.0)
#Vert2.Draw("sames")
#Horz1 = ROOT.TLine(1.0,-0.333333,-1.0,-0.333333)
#Horz1.Draw("sames")
#Horz2 = ROOT.TLine(1.0,0.333333,-1.0,0.333333)
#Horz2.Draw("sames")
canvas.SaveAs("plots/12x12EtSignal.png")

