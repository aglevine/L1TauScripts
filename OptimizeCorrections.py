import ROOT
import sys


eff_ntuple = 'tau_eff_DY_E3H3_Sept23_tpgCalib24.root'
eff_ntuple_file = ROOT.TFile(eff_ntuple)
#eff_rlx_spot = 'rlxTauEcalSeedEfficiency/Ntuple'
eff_rlx_spot = 'rlxTauEfficiency/Ntuple'
#eff_iso_spot = 'isoTauEcalSeedEfficiency/Ntuple'
eff_iso_spot = 'isoTauEfficiency/Ntuple'
eff_rlx_eg_ntuple = eff_ntuple_file.Get(eff_rlx_spot)
eff_iso_eg_ntuple = eff_ntuple_file.Get(eff_iso_spot)

binRes = [18,-1.0,1.0]



def optimize (tree, binning):
 negFactor = 1.0
 negFactorOld = 10.0
 posFactor = 1.0
 posFactorOld = 10.0
 i =0
 while (abs(negFactor-negFactorOld) > 0.1 or abs(posFactor - posFactorOld) > 0.1):
  if (i % 2 == 1):
    negFactorOld = negFactor
    lowBound,highBound = getInterval(eff_rlx_eg_ntuple,binRes, False, posFactor)
    negFactor = (lowBound+highBound)/2
  elif (i % 2 == 0):
    posFactorOld = posFactor
    lowBound,highBound = getInterval(eff_rlx_eg_ntuple,binRes, True, negFactor)
    posFactor = (lowBound+highBound)/2
  i = i+1
  print "negFactor: " + str(negFactor)
  print "posFactor: " + str(posFactor)
  
  
def getInterval (tree, binning):
 lowFactor = 0.0
 highFactor = 1.0
 width = 1.0
 lowMean = 1000
 highMean = 100
 draw_stringNoScale = "((recoPt-l1gPt)/recoPt) >>htempNoScale(%s)" % (", ".join(str(x) for x in binning))
 selectionInitial = "l1gPt > 70 && l1gPt < 90 && l1gMatch&&l1gTauVeto==0"
 tree.Draw(draw_stringNoScale,selectionInitial,"")
 output_histoInitial = ROOT.gDirectory.Get("htempNoScale").Clone()
 maxBin = output_histoInitial.GetMaximumBin()
 print "maxBin" + str(maxBin)
 maxBinx = output_histoInitial.GetBinContent(maxBin)
 print "maxBinx" + str(maxBinx)
 binwidth = output_histoInitial.GetBinWidth(maxBin)
 print "binwidth" + str(binwidth)
 print str(binning[1])
 maxBinStart = binning[1]+(maxBin-1)*binwidth
 maxAverage = maxBinStart+binwidth/2
 print "max bin start" + str(maxBinStart)
 print "mean" + str(maxAverage)
 raw_input() 
 selectionNoScale = "l1gPt > 70 && l1gPt < 90 && l1gMatch&&l1gTauVeto==0&&(recoPt-l1gPt)/recoPt>"+str(maxBinStart)
 tree.Draw(draw_stringNoScale, selectionNoScale)
 #raw_input()
 output_histoNoScale = ROOT.gDirectory.Get("htempNoScale").Clone()
 while(abs(lowMean-highMean) > 0.00001):
 	draw_stringLow = "((recoPt-(" + str(lowFactor) +"*l1gPt))/recoPt) >>htempLow(%s)" % (", ".join(str(x) for x in binning))
 	draw_stringHigh = "((recoPt-(" + str(highFactor)+"*l1gPt))/recoPt) >>htempHigh(%s)" % (", ".join(str(x) for x in binning))
        print draw_stringLow
        print draw_stringHigh
 
 	selectionLow = "l1gPt > 70 && l1gPt < 90 && l1gMatch&&l1gTauVeto==0&&(recoPt-l1gPt)/recoPt<"+str(maxBinStart)
 	selectionHigh = "l1gPt > 70 && l1gPt < 90 && l1gMatch&&l1gTauVeto==0&&(recoPt-l1gPt)/recoPt<"+str(maxBinStart)
 	tree.Draw(draw_stringLow, selectionLow)
        #raw_input()
 	tree.Draw(draw_stringHigh, selectionLow)
        #raw_input()
 	output_histoLow = ROOT.gDirectory.Get("htempLow").Clone()
 	output_histoHigh = ROOT.gDirectory.Get("htempHigh").Clone()
 	output_histoLow.Add(output_histoNoScale)
	output_histoHigh.Add(output_histoNoScale)
 	lowFit = ROOT.TF1("asdf","gaus")
 	highFit = ROOT.TF1("asdf","gaus")
 	#output_histoLow.Fit(lowFit)
 	#lowMean = lowFit.GetParameter(1)
 	lowMean = output_histoLow.GetMean()
	#output_histoHigh.Fit(highFit)
 	#highMean = highFit.GetParameter(1)
	highMean = output_histoHigh.GetMean()
        output_histoLow.Delete()
        lowFit.Delete()
	highFit.Delete()
	output_histoHigh.Delete()
	print "lowMean" + str(lowMean)
	print "highMean" + str(highMean)
	print highFactor
	print lowFactor
        lowMean = lowMean-maxAverage
 	highMean = highMean - maxAverage
 	if (lowMean * highMean) < 0:
		width = width/2
		highFactor = lowFactor+width
		
	elif (lowMean * highMean >= 0):
		lowFactor = highFactor
		highFactor = highFactor+width
 
 return lowFactor,highFactor

getInterval(eff_rlx_eg_ntuple,binRes)
#optFactor = findFactor(eff_rlx_eg_ntuple,binRes,-2.4,-1.8,lowBound)
#print optFactor

