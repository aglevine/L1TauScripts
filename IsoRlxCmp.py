from sys import argv, stdout, stderr
import ROOT


#eff_ntuple = 'uct_efficiency_tree_denomfix.root'
#eff_ntuple = 'uct_efficiency_tree_tightiso.root'
#eff_ntuple = 'uct_tau4by8_efficiency_tree.root'
eff_ntuple = 'uct_efficiency_tree4x8veto.root'
#eff_ntuple = '/afs/hep.wisc.edu/cms/aglevine/L1Taus/src/L1Trigger/UWTriggerTools/test/uct_tau_highSeed.root'
eff_ntuple_file = ROOT.TFile(eff_ntuple)
#
#eff_rlx_spot = 'rlxTauEcalSeedEfficiency/Ntuple'
eff_rlx_spot = 'rlxTauEfficiency/Ntuple'
#eff_iso_spot = 'isoTauEcalSeedEfficiency/Ntuple'
eff_iso_spot = 'isoTauEfficiency/Ntuple'
eff_rlx_eg_ntuple = eff_ntuple_file.Get(eff_rlx_spot)
eff_iso_eg_ntuple = eff_ntuple_file.Get(eff_iso_spot)

eff_rlx_eg_ntuple.AddFriend(eff_iso_eg_ntuple,"iso")
eff_rlx_eg_ntuple.Scan("l1gPt:iso.l1gPt:l1gDR:iso.l1gDR:((l1gPt-l1gJetPt)/l1gPt):((iso.l1gPt-iso.l1gJetPt)/iso.l1gPt)","l1gPt!=iso.l1gPt && iso.l1gPt>0")


