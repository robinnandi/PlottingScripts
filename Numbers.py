import ROOT as r

r.gStyle.SetOptStat(0)

def make_list(hist):
    return [hist.GetBinContent(1,1), hist.GetBinContent(1,2), hist.GetBinContent(1,3), hist.GetBinContent(1,4),
            hist.GetBinContent(2,1), hist.GetBinContent(2,2), hist.GetBinContent(2,3), hist.GetBinContent(2,4),
            hist.GetBinContent(3,1), hist.GetBinContent(3,2), hist.GetBinContent(3,3), hist.GetBinContent(3,4),
            hist.GetBinContent(4,1), hist.GetBinContent(4,2), hist.GetBinContent(4,3), hist.GetBinContent(4,4)]

def make_pset(data, bkgd, bkgderror, susy, susy_jesplus, susy_jesminus, intlumi, intlumierror, xsec, xsecerror):
    text = "from utils import PSet\n\n"
    text = text + "inputData = PSet(\n"
    text = text + "    nBins = 16,\n"
    text = text + "    Observation = "+str(make_list(data))+",\n"
    text = text + "    Background = "+str(make_list(bkgd))+",\n"
    text = text + "    BackgroundError = "+str(make_list(bkgderror))+",\n"
    text = text + "    SignalEfficiency = "+str(make_list(susy))+",\n"
    text = text + "    SignalEfficiency_JESplus = "+str(make_list(susy_jesplus))+",\n"
    text = text + "    SignalEfficiency_JESminus = "+str(make_list(susy_jesminus))+",\n"
#    text = text + "    SignalEfficiency_JERes = "+str(make_list(susy_jeres))+",\n"
#    text = text + "    SignalEfficiency_PESplus = "+str(make_list(susy_pesplus))+",\n"
#    text = text + "    SignalEfficiency_PESminus = "+str(make_list(susy_pesminus))+",\n"
#    text = text + "    SignalEfficiency_PERes = "+str(make_list(susy_peres))+",\n"
#    text = text + "    SignalEfficiency_PUplus = "+str(make_list(susy_puplus))+",\n"
#    text = text + "    SignalEfficiency_PUminus = "+str(make_list(susy_puminus))+",\n"
    text = text + "    Lumi = "+str(intlumi)+",\n"
    text = text + "    LumiError = "+str(intlumierror)+",\n"
    text = text + "    CrossSection = "+str(xsec)+",\n"
    text = text + "    CrossSectionError = "+str(xsecerror)+"\n"
    text = text + ")"
    return text

def draw_hist_with_overflow(hist, name):
    c = r.TCanvas("c", "c", 1000, 1000)
    big_hist = r.TH2F("n", "Number of Events;HT;pfMET", 4, 400., 800., 4, 50., 250.)
    for xbin in range(1,hist.GetNbinsX()+2):
        for ybin in range(1,hist.GetNbinsY()+2):
            big_hist.Fill(hist.GetXaxis().GetBinCenter(xbin), hist.GetYaxis().GetBinCenter(ybin), hist.GetBinContent(xbin, ybin))
    big_hist.Draw("TEXT")
    c.SaveAs(name+".png")

def renormalise(hist, hist_norm):
    for xbin in range(1,hist.GetNbinsX()+2):
        for ybin in range(1,hist.GetNbinsY()+2):
            hist.SetBinContent(xbin, ybin, hist.GetBinContent(xbin,ybin)*hist_norm.GetBinContent(xbin,0)/hist.GetBinContent(xbin,0))
    return hist

intlumi = 1100.
intlumierror = 44.
#file = r.TFile.Open("../../results/Calo_ra3tight_Skim_WJetsToLNu_TuneZ2_7TeV_madgraph_tauola_Summer11_PU_S4_START42_V11_v1_1.root")
#hist = file.Get("StandardPlots_HT_sele/nEvents")
#hist.Scale(intlumi/100)
#draw_hist_with_overflow(hist, "EWK")
#file = r.TFile.Open("../../results/Calo_ra3tight_Skim_TTJets_TuneZ2_7TeV_madgraph_tauola_Summer11_PU_S4_START42_V11_v1_1.root")
#hist = file.Get("StandardPlots_HT_sele/nEvents")
#hist.Scale(intlumi/100)
#draw_hist_with_overflow(hist, "ttbar")
file = r.TFile.Open("../../results/Calo_ra3tight_JESplus_GGMSignalScan_94.root")
susy = file.Get("StandardPlots_HT_sele/nEvents")
susy.Scale(intlumi/100)
draw_hist_with_overflow(susy, "SUSY")
file = r.TFile.Open("../../results/Calo_ra3tight_JESplus_GGMSignalScan_94.root")
susy_jesplus = file.Get("StandardPlots_HT_sele/nEvents")
susy_jesplus.Scale(intlumi/100)
draw_hist_with_overflow(susy_jesplus, "SUSY_JESplus")
file = r.TFile.Open("../../results/Calo_ra3tight_JESminus_GGMSignalScan_94.root")
susy_jesminus = file.Get("StandardPlots_HT_sele/nEvents")
susy_jesminus.Scale(intlumi/100)
draw_hist_with_overflow(susy_jesminus, "SUSY_JESminus")
file = r.TFile.Open("../../results/Calo_ra3tight_PhotonHad_Run2011A_uptoRun171106_1.root")
cont = file.Get("StandardPlots_HT_cont/nEvents")
data = file.Get("StandardPlots_HT_sele/nEvents")
draw_hist_with_overflow(data, "Data")
bkgd = renormalise(cont, data)
draw_hist_with_overflow(bkgd, "QCD")
sb_cont = file.Get("StandardPlots_HT_sb_cont/nEvents")
sb_data = file.Get("StandardPlots_HT_sb_sele/nEvents")
draw_hist_with_overflow(sb_data, "sb_Data")
sb_bkgd = renormalise(sb_cont, sb_data)
draw_hist_with_overflow(sb_bkgd, "sb_QCD")
#file = r.TFile.Open("../../results/Calo_ra3tight_TuneZ2_pythia6.root")
#mc_cont = file.Get("StandardPlots_HT_cont/nEvents")
#mc_data = file.Get("StandardPlots_HT_sele/nEvents")
#draw_hist_with_overflow(mc_data, "mc_Data")
#mc_bkgd = renormalise(mc_cont, mc_data)
f = open("inputData.py", "w")
f.write(make_pset(data, bkgd, bkgderror, susy, susy_jesplus, susy_jesminus, intlumi, intlumierror, xsec, xsecerror))
