import ROOT as r
import math

r.gStyle.SetOptStat(0)
r.gStyle.SetOptTitle(0)
r.gStyle.SetTitleOffset(1.4,"y")
r.gStyle.SetPadLeftMargin(0.12)
r.gStyle.SetNdivisions(4,"xy")
#r.gStyle.SetPaintTextFormat(".3f")

dir = "data2/"

def make_list(hist):
    #nums = [ hist.GetBinContent(1,1), hist.GetBinContent(1,2), hist.GetBinContent(1,3), hist.GetBinContent(1,4),
    #         hist.GetBinContent(2,1), hist.GetBinContent(2,2), hist.GetBinContent(2,3), hist.GetBinContent(2,4),
    #         hist.GetBinContent(3,1), hist.GetBinContent(3,2), hist.GetBinContent(3,3), hist.GetBinContent(3,4),
    #         hist.GetBinContent(4,1), hist.GetBinContent(4,2), hist.GetBinContent(4,3), hist.GetBinContent(4,4) ]
    nums = [ hist.GetBinContent(4,4) ]
    str = "["
    for i in range(len(nums)):
        str = str + "%.6f" % nums[i]
        if i != len(nums) - 1:
            str = str + ", "
    str = str + "]"
    return str

def make_pset(obs_and_bkd_text, eff, efferror, intlumi, intlumierror, xsec, xsecerror, mSquark, mGluino):
    text = "inputData_"+str(mSquark)+"_"+str(mGluino)+" = PSet(\n"
    text = text + "    nBins = 1,\n"
    text = text + obs_and_bkd_text
    text = text + "    SignalEfficiency = "+make_list(eff)+",\n"
    text = text + "    SignalEfficiencyError = "+make_list(efferror)+",\n"
    text = text + "    Lumi = "+str(intlumi)+",\n"
    text = text + "    LumiError = "+str(intlumierror)+",\n"
    text = text + "    CrossSection = "+str(xsec)+",\n"
    text = text + "    CrossSectionError = "+str(xsecerror)+"\n"
    text = text + ")\n"
    return text

def draw_hist_with_overflow(hist, name):
    c = r.TCanvas("c", "c", 1000, 1000)
    big_hist = r.TH2F("n", "Number of Events;H_{T} / GeV;ME_{T} / GeV", 4, 400., 800., 4, 50., 250.)
    #big_hist.GetXaxis().SetBinLabel(4, "inf")
    big_hist.Draw("TEXT")
    boxes = []
    for xbin in range(1,hist.GetNbinsX()+2):
        for ybin in range(1,hist.GetNbinsY()+2):
            big_hist.Fill(hist.GetXaxis().GetBinCenter(xbin), hist.GetYaxis().GetBinCenter(ybin), hist.GetBinContent(hist.GetBin(xbin, ybin)))
            #text = "%.1f" % hist.GetBinContent(hist.GetBin(xbin, ybin))
            #boxes.append(r.TLatex(hist.GetXaxis().GetBinLowEdge(xbin)+30, hist.GetYaxis().GetBinCenter(ybin), text))
    #for box in boxes:
    #    box.Draw("SAME")
    #c.SaveAs(name+".png")
    c.SaveAs(name+".eps")
    c.SaveAs(name+".pdf")

def draw_syst_hist(hist, hist_plus, hist_minus, name):
    c = r.TCanvas("c", "c", 1000, 1000)
    big_hist = r.TH2F("n", "Signal Efficiency;H_{T} / GeV;ME_{T} / GeV", 4, 400., 800., 4, 50., 250.)
    #big_hist.GetXaxis().SetBinLabel(4, "inf")
    big_hist.Draw("TEXT")
    boxes = []
    for xbin in range(1,hist.GetNbinsX()+2):
        for ybin in range(1,hist.GetNbinsY()+2):
            n = hist.GetBinContent(hist.GetBin(xbin, ybin))
            if (n > 0):
                n_plus = 100 * ( hist_plus.GetBinContent(hist.GetBin(xbin, ybin)) - n ) / n
                n_minus = 100 * ( hist_minus.GetBinContent(hist.GetBin(xbin, ybin)) - n ) / n
                text = "%.3f" %n + "^{" + "%.1f" %n_plus + "%}_{" + "%.1f" %n_minus + "%}"
            else:
                text = "%.3f" %n
            boxes.append(r.TLatex(hist.GetXaxis().GetBinLowEdge(xbin), hist.GetYaxis().GetBinCenter(ybin), text))
    for box in boxes:
        box.Draw("SAME")
    #c.SaveAs(name+".png")
    c.SaveAs(name+".eps")
    c.SaveAs(name+".pdf")

def renormalise(hist, hist_norm):
    for xbin in range(1,hist.GetNbinsX()+2):
        for ybin in range(1,hist.GetNbinsY()+2):
            hist.SetBinContent(xbin, ybin, hist.GetBinContent(xbin,ybin)*hist_norm.GetBinContent(xbin,0)/hist.GetBinContent(xbin,0))
    return hist

def correct_sb_obs(hist):
    hist.SetBinContent(1,2,2)
    hist.SetBinContent(3,2,1)
    hist.SetBinContent(4,2,1)
    hist.SetBinContent(2,3,1)
    hist.SetBinContent(4,3,0)
    hist.SetBinContent(1,4,1)
    hist.SetBinContent(4,4,1)
    
def correct_mc_obs(hist, hist_pred):
    rand = r.TRandom3()
    for xbin in range(1,hist.GetNbinsX()+2):
        for ybin in range(1,hist.GetNbinsY()+2):
            hist.SetBinContent(xbin, ybin, hist_pred.GetBinContent(xbin,ybin)*(1 + rand.Gaus(0,0.2)))
    return hist

def get_file_number(mSquark, mGluino):
    return 21*( int((mSquark - 400)/80) ) + int((mGluino - 400)/80) + 1

def draw_xsec(mChi0):
    file = r.TFile(dir+"CrossSection_SUSYScan_"+str(mChi0)+".root")
    hist = file.Get("CrossSection/CrossSections")
    c = r.TCanvas("c", "c", 1000, 1000)
    hist.Draw("TEXT")
    #c.SaveAs("plots/new/CrossSection_"+str(mChi0)+".png")
    c.SaveAs("plots/new/CrossSection_"+str(mChi0)+".eps")
    c.SaveAs("plots/new/CrossSection_"+str(mChi0)+".pdf")

def get_xsec(mChi0, mSquark, mGluino):
    file = r.TFile(dir+"CrossSection_SUSYScan_"+str(mChi0)+".root")
    hist = file.Get("CrossSection/CrossSections")
    return hist.GetBinContent(int((mSquark - 400)/80) + 1, int((mGluino - 400)/80) + 1)

def modulus(hist):
    for xbin in range(1,hist.GetNbinsX()+2):
        for ybin in range(1,hist.GetNbinsY()+2):
            hist.SetBinContent(xbin, ybin, math.fabs(hist.GetBinContent(xbin, ybin)))

def quadrature(hist_list):
    hist = r.TH2F("n", "Number of Events;H_{T} / GeV;ME_{T} / GeV", 4, 400., 800., 4, 50., 250.)
    #hist = hist_list[0].Clone()
    for xbin in range(1,hist.GetNbinsX()+2):
        for ybin in range(1,hist.GetNbinsY()+2):
            sum2 = 0.
            for hist in hist_list:
                sum2 = sum2 + hist.GetBinContent(xbin, ybin)**2
            hist.SetBinContent(xbin, ybin, math.sqrt(sum2))
    return hist

def get_background():
    f_ttbar = r.TFile.Open(dir+"PF_ra3tight_Skim_TTJets_TuneZ2_7TeV_madgraph_tauola_Summer11_PU_S4_START42_V11_v1_1.root")
    ttbar = f_ttbar.Get("StandardPlots_HT_sele/nEvents")
    draw_hist_with_overflow(ttbar, "plots/new/ttbar")
    f_data = r.TFile.Open(dir+"PF_ra3tight_PhotonHad_Run2011A_uptoRun171106_1.root")
    cont = f_data.Get("StandardPlots_HT_cont/nEvents")
    data = f_data.Get("StandardPlots_HT_sele/nEvents")
    draw_hist_with_overflow(data, "plots/new/Data_obs")
    bkgd = renormalise(cont, data)
    draw_hist_with_overflow(bkgd, "plots/new/Data_pred")
    sb_cont = f_data.Get("StandardPlots_HT_sb_cont/nEvents")
    sb_data = f_data.Get("StandardPlots_HT_sb_sele/nEvents")
    correct_sb_obs(sb_data)
    draw_hist_with_overflow(sb_data, "plots/new/sb_obs")
    sb_bkgd = renormalise(sb_cont, sb_data)
    draw_hist_with_overflow(sb_bkgd, "plots/new/sb_pred")
    f_mc = r.TFile.Open(dir+"PF_ra3tight_TuneZ2_pythia6.root")
    mc_cont = f_mc.Get("StandardPlots_HT_cont/nEvents")
    mc_data = f_mc.Get("StandardPlots_HT_sele/nEvents")
    mc_data.Scale(28.)
    mc_bkgd = renormalise(mc_cont, mc_data)
    draw_hist_with_overflow(mc_cont, "plots/new/mc_pred")
    correct_mc_obs(mc_data, mc_cont)
    draw_hist_with_overflow(mc_data, "plots/new/mc_obs")
    bkgderror = mc_data - mc_bkgd
    bkgderror.Divide(mc_data)
    bkgderror.Scale(0.5)
    bkgderror.Multiply(bkgd)
    modulus(bkgderror)
    draw_hist_with_overflow(bkgderror, "plots/new/Bkgd_error")
    text = "    Observation = "+make_list(data)+",\n"
    text = text + "    Background = "+make_list(bkgd)+",\n"
    text = text + "    BackgroundError = "+make_list(bkgderror)+",\n"
    return text

def extract_numbers(f, mChi0, mSquark, mGluino, intlumi, intlumierror, obs_and_bkd_text):
    n = get_file_number(mSquark, mGluino)
    print n
    f_susy = r.TFile.Open(dir+"PF_ra3tight_SUSYScan_"+str(mChi0)+"_"+str(n)+".root")
    eff = f_susy.Get("StandardPlots_HT_sele/nEvents")
    #draw_hist_with_overflow(eff, "plots/new/SUSY_"+str(mChi0)+"_"+str(mSquark)+"_"+str(mGluino))
    # Jet Enegry Scale
    f_susy_jesplus = r.TFile.Open(dir+"PF_ra3tight_JESplus_SUSYScan_"+str(mChi0)+"_"+str(n)+".root")
    susy_jesplus = f_susy_jesplus.Get("StandardPlots_HT_sele/nEvents")
    f_susy_jesminus = r.TFile.Open(dir+"PF_ra3tight_JESminus_SUSYScan_"+str(mChi0)+"_"+str(n)+".root")
    susy_jesminus = f_susy_jesminus.Get("StandardPlots_HT_sele/nEvents")
    draw_syst_hist(eff, susy_jesplus, susy_jesminus, "plots/new/SUSY_"+str(mChi0)+"_"+str(mSquark)+"_"+str(mGluino)+"_JES")
    susy_jes = susy_jesplus - susy_jesminus
    susy_jes.Scale(0.5)
    modulus(susy_jes)
    print "JES: %.1f" % (100*susy_jes.GetBinContent(4,4)/eff.GetBinContent(4,4))
    # Jet Enegry Resolution
    f_susy_jerplus = r.TFile.Open(dir+"PF_ra3tight_JERPlus_SUSYScan_"+str(mChi0)+"_"+str(n)+".root")
    susy_jerplus = f_susy_jerplus.Get("StandardPlots_HT_sele/nEvents")
    f_susy_jerminus = r.TFile.Open(dir+"PF_ra3tight_JERMinus_SUSYScan_"+str(mChi0)+"_"+str(n)+".root")
    susy_jerminus = f_susy_jerminus.Get("StandardPlots_HT_sele/nEvents")
    draw_syst_hist(eff, susy_jerplus, susy_jerminus, "plots/new/SUSY_"+str(mChi0)+"_"+str(mSquark)+"_"+str(mGluino)+"_JER")
    susy_jer = susy_jerplus - susy_jerminus
    susy_jer.Scale(0.5)
    modulus(susy_jer)
    print "JER: %.1f" % (100*susy_jer.GetBinContent(4,4)/eff.GetBinContent(4,4))
    # PU HT shift
    f_susy_htpuplus = r.TFile.Open(dir+"PF_ra3tight_htPUplus_SUSYScan_"+str(mChi0)+"_"+str(n)+".root")
    susy_htpuplus = f_susy_htpuplus.Get("StandardPlots_HT_sele/nEvents")
    f_susy_htpuminus = r.TFile.Open(dir+"PF_ra3tight_htPUminus_SUSYScan_"+str(mChi0)+"_"+str(n)+".root")
    susy_htpuminus = f_susy_htpuminus.Get("StandardPlots_HT_sele/nEvents")
    draw_syst_hist(eff, susy_htpuplus, susy_htpuminus, "plots/new/SUSY_"+str(mChi0)+"_"+str(mSquark)+"_"+str(mGluino)+"_htPU")
    susy_htpu = susy_htpuplus - susy_htpuminus
    susy_htpu.Scale(0.5)
    modulus(susy_htpu)
    print "PU HT: %.1f" % (100*susy_htpu.GetBinContent(4,4)/eff.GetBinContent(4,4))
    # PU MET smearing
    f_susy_metpuplus = r.TFile.Open(dir+"PF_ra3tight_metPUplus_SUSYScan_"+str(mChi0)+"_"+str(n)+".root")
    susy_metpuplus = f_susy_metpuplus.Get("StandardPlots_HT_sele/nEvents")
    f_susy_metpuminus = r.TFile.Open(dir+"PF_ra3tight_metPUminus_SUSYScan_"+str(mChi0)+"_"+str(n)+".root")
    susy_metpuminus = f_susy_metpuminus.Get("StandardPlots_HT_sele/nEvents")
    draw_syst_hist(eff, susy_metpuplus, susy_metpuminus, "plots/new/SUSY_"+str(mChi0)+"_"+str(mSquark)+"_"+str(mGluino)+"_metPU")
    susy_metpu = susy_metpuplus - susy_metpuminus
    susy_metpu.Scale(0.5)
    modulus(susy_metpu)
    print "PU MET: %.1f" % (100*susy_metpu.GetBinContent(4,4)/eff.GetBinContent(4,4))
    # PU photon efficiency
    f_susy_phoeffplus = r.TFile.Open(dir+"PF_ra3tight_phoeffplus_SUSYScan_"+str(mChi0)+"_"+str(n)+".root")
    susy_phoeffplus = f_susy_phoeffplus.Get("StandardPlots_HT_sele/nEvents")
    f_susy_phoeffminus = r.TFile.Open(dir+"PF_ra3tight_phoeffminus_SUSYScan_"+str(mChi0)+"_"+str(n)+".root")
    susy_phoeffminus = f_susy_phoeffminus.Get("StandardPlots_HT_sele/nEvents")
    draw_syst_hist(eff, susy_phoeffplus, susy_phoeffminus, "plots/new/SUSY_"+str(mChi0)+"_"+str(mSquark)+"_"+str(mGluino)+"_phoeff")
    susy_phoeff = susy_phoeffplus - susy_phoeffminus
    susy_phoeff.Scale(0.5)
    modulus(susy_phoeff)
    print "PU phoeff: %.1f" % (100*susy_phoeff.GetBinContent(4,4)/eff.GetBinContent(4,4))
    efferror = quadrature([susy_jes, susy_jer, susy_htpu, susy_metpu, susy_phoeff])
    print "Total Error: %.1f" % (100*efferror.GetBinContent(4,4)/eff.GetBinContent(4,4))
    xsec = get_xsec(mChi0, mSquark, mGluino)
    xsecerror = 0.2*xsec
    f.write(make_pset(obs_and_bkd_text, eff, efferror, intlumi, intlumierror, xsec, xsecerror, mSquark, mGluino))

intlumi = 1100.
intlumierror = 44.
mChi0 = 150
draw_xsec(mChi0)
obs_and_bkd_text = get_background()
f = open("inputData_"+str(mChi0)+".py", "w")
f.write("from utils import PSet\n\n")
f.close()
f = open("inputData_"+str(mChi0)+".py", "a")
input_data_list = []
for mSquark in [1040]:#[400, 480, 560, 640, 720, 800, 880, 960, 1040, 1120, 1200, 1280, 1360, 1440, 1520, 1600, 1680, 1760, 1840, 1920, 2000]:
    for mGluino in [1200]:#[400, 480, 560, 640, 720, 800, 880, 960, 1040, 1120, 1200, 1280, 1360, 1440, 1520, 1600, 1680, 1760, 1840, 1920, 2000]:
        print "Extracting numbers for mSquark = "+str(mSquark)+"; mGluino = "+str(mGluino)+"."
        extract_numbers(f, mChi0, mSquark, mGluino, intlumi, intlumierror, obs_and_bkd_text)
        input_data_list.append("inputData_"+str(mSquark)+"_"+str(mGluino))
f.write("inputData = ["+", ".join(id for id in input_data_list)+"]")
