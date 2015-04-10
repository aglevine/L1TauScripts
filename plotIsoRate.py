from sys import argv, stdout, stderr
import math
import array
import numpy
import ROOT

ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetOptStat(0)
iso = array.array('f',[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
rate4x4=array.array('f',[4.8647435,6.1626895,6.7503425,7.0671640,7.2409050,7.3533255,7.4401960,7.4708560, 7.5015160,7.5321760])
rate4x8 = array.array('f',[5.7436675,6.9700735,7.3431055,7.3993155,7.4044255,7.4197555,7.4197555,7.4197555,7.4197555,7.4197555])
#rlx4x8 = array.array('f',[7.4197555,7.4197555,7.4197555,7.4197555,7.4197555,7.4197555,7.4197555,7.4197555,7.4197555,7.4197555])
#rlx4x4 = array.array('f',[7.5730565,7.5730565,7.5730565,7.5730565,7.5730565,7.5730565,7.5730565,7.5730565,7.5730565,7.5730565])


isovec = ROOT.TVectorF(len(iso),iso)
rate4x4vec = ROOT.TVectorF(len(rate4x4),rate4x4)
rate4x8vec = ROOT.TVectorF(len(rate4x8),rate4x8)
#rlx4x8vec = ROOT.TVectorF(len(rlx4x8),rlx4x8)
#rlx4x4vec = ROOT.TVectorF(len(rlx4x4),rlx4x4)


canvas = ROOT.TCanvas("asdf","asdf",800,800)

isoPlat4x4 = ROOT.TGraph(isovec,rate4x4vec)
isoPlat4x8 = ROOT.TGraph(isovec,rate4x8vec)
#rlxPlat4x4 = ROOT.TGraph(isovec,rlx4x4vec)
#rlxPlat4x8 = ROOT.TGraph(isovec,rlx4x8vec)

#rlxPlat4x4.SetLineColor(ROOT.EColor.kGreen+3)
#rlxPlat4x8.SetLineColor(ROOT.EColor.kMagenta+2)
isoPlat4x4.SetLineColor(ROOT.EColor.kRed)
isoPlat4x4.SetLineWidth(3)
isoPlat4x8.SetLineWidth(3)
#rlxPlat4x4.SetLineWidth(3)
#rlxPlat4x8.SetLineWidth(3)
isoPlat4x8.SetLineColor(ROOT.EColor.kBlue)

isoPlat4x8.Draw("AL*")
isoPlat4x4.Draw("L*,sames")
#rlxPlat4x8.Draw("L,sames")
#rlxPlat4x4.Draw("L,sames")

isoPlat4x8.GetYaxis().SetTitle("Rate (1E6 Hz)")
isoPlat4x8.GetXaxis().SetTitle("Isolation Threshold")
isoPlat4x8.GetYaxis().SetRangeUser(4.0,10.0)
isoPlat4x8.GetYaxis().SetTitleOffset(1.15)

legend = ROOT.TLegend(0.4,0.6,0.7,0.89,'','brNDC')
legend.SetFillColor(ROOT.EColor.kWhite)
legend.SetFillStyle(0)
legend.SetBorderSize(0)
legend.AddEntry(isoPlat4x4,'4x4 Taus','lp')
legend.AddEntry(isoPlat4x8,'4x8 Taus','lp')
#legend.AddEntry(rlxPlat4x4,'4x4 Relaxed','l')
#legend.AddEntry(rlxPlat4x8,'4x8 Relaxed','l')
legend.Draw("sames")

isoPlat4x8.SetTitle("")
canvas.SaveAs("plots/IsoRate.png")
