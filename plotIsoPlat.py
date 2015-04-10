from sys import argv, stdout, stderr
import math
import array
import numpy
import ROOT

ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetOptStat(0)
iso = array.array('f',[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
eff4x4=array.array('f',[0.83700352907,0.86852690577,0.88134741783,0.89346075058,0.91343222061,0.9265127182,0.93824980656,0.94502037763,0.95128937562,0.95128937562])
eff4x8 = array.array('f',[0.9666582942, 0.97529274225,0.9781165719,0.98564606905,0.99715099732, 0.99715099732,0.99715099732,0.99715099732,0.99715099732,0.9971509973])

isovec = ROOT.TVectorF(len(iso),iso)
eff4x4vec = ROOT.TVectorF(len(eff4x4),eff4x4)
eff4x8vec = ROOT.TVectorF(len(eff4x8),eff4x8)

canvas = ROOT.TCanvas("asdf","asdf",800,800)

isoPlat4x4 = ROOT.TGraph(isovec,eff4x4vec)
isoPlat4x8 = ROOT.TGraph(isovec,eff4x8vec)

isoPlat4x4.SetLineColor(ROOT.EColor.kRed)
isoPlat4x4.SetLineWidth(3)
isoPlat4x8.SetLineWidth(3)
isoPlat4x8.SetLineColor(ROOT.EColor.kBlue)

isoPlat4x8.Draw("AL*")
isoPlat4x4.Draw("L*,sames")

isoPlat4x8.GetYaxis().SetTitle("Efficiency Plateau")
isoPlat4x8.GetXaxis().SetTitle("Isolation Threshold")
isoPlat4x8.GetYaxis().SetRangeUser(0.7,1.0)
isoPlat4x8.GetYaxis().SetTitleOffset(1.15)

legend = ROOT.TLegend(0.6,0.3,0.89,0.6,'','brNDC')
legend.SetFillColor(ROOT.EColor.kWhite)
legend.SetFillStyle(0)
legend.SetBorderSize(0)
legend.AddEntry(isoPlat4x4,'4x4 Taus','lp')
legend.AddEntry(isoPlat4x8,'4x8 Taus','lp')
legend.Draw("sames")

isoPlat4x8.SetTitle("")
canvas.SaveAs("plots/IsoPlat.png")
