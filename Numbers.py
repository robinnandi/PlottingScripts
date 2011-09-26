import ROOT as r

r.gStyle.SetOptStat(0)
#r.gStyle.SetOptStat(11111)
dir = "data/"
#dir = "../../results/"

def make_list(hist):
    nums = [ hist.GetBinContent(1,1), hist.GetBinContent(1,2), hist.GetBinContent(1,3), hist.GetBinContent(1,4),
             hist.GetBinContent(2,1), hist.GetBinContent(2,2), hist.GetBinContent(2,3), hist.GetBinContent(2,4),
             hist.GetBinContent(3,1), hist.GetBinContent(3,2), hist.GetBinContent(3,3), hist.GetBinContent(3,4),
             hist.GetBinContent(4,1), hist.GetBinContent(4,2), hist.GetBinContent(4,3), hist.GetBinContent(4,4) ]
    str = "["
    for i in range(len(nums)):
        str = str + "%.6f" % nums[i]
        if i != len(nums) - 1:
            str = str + ", "
    str = str + "]"
    return str

def make_pset(obs_and_bkd_text, susy, susy_jes, intlumi, intlumierror, xsec, xsecerror, mSquark, mGluino):
    text = "inputData_"+str(mSquark)+"_"+str(mGluino)+" = PSet(\n"
    text = text + "    nBins = 16,\n"
    #text = text + "    Observation = "+make_list(data)+",\n"
    #text = text + "    Background = "+make_list(bkgd)+",\n"
    #text = text + "    BackgroundError = "+make_list(bkgderror)+",\n"
    # Generate 3 commented out lines above using a separate function since they need only be calculated once not for every parameter point
    text = text + obs_and_bkd_text
    text = text + "    SignalEfficiency = "+make_list(susy)+",\n"
    text = text + "    SignalEfficiency_JES = "+make_list(susy_jes)+",\n"
#    text = text + "    SignalEfficiency_JERes = "+make_list(susy_jeres)+",\n"
#    text = text + "    SignalEfficiency_PU = "+make_list(susy_pu)+",\n"
    text = text + "    Lumi = "+str(intlumi)+",\n"
    text = text + "    LumiError = "+str(intlumierror)+",\n"
    text = text + "    CrossSection = "+str(xsec)+",\n"
    text = text + "    CrossSectionError = "+str(xsecerror)+"\n"
    text = text + ")\n"
    return text

def draw_hist_with_overflow(hist, name):
    c = r.TCanvas("c", "c", 1000, 1000)
    big_hist = r.TH2F("n", "Number of Events;HT;pfMET", 4, 400., 800., 4, 50., 250.)
    for xbin in range(1,hist.GetNbinsX()+2):
        for ybin in range(1,hist.GetNbinsY()+2):
            big_hist.Fill(hist.GetXaxis().GetBinCenter(xbin), hist.GetYaxis().GetBinCenter(ybin), hist.GetBinContent(hist.GetBin(xbin, ybin)))
    big_hist.Draw("TEXT")
    c.SaveAs(name+".png")

def renormalise(hist, hist_norm):
    for xbin in range(1,hist.GetNbinsX()+2):
        for ybin in range(1,hist.GetNbinsY()+2):
            hist.SetBinContent(xbin, ybin, hist.GetBinContent(xbin,ybin)*hist_norm.GetBinContent(xbin,0)/hist.GetBinContent(xbin,0))
    return hist

def get_file_number(mSquark, mGluino):
    return 21*( int((mSquark - 400)/80) ) + int((mGluino - 400)/80) + 1

def draw_xsec(mChi0):
    file = r.TFile(dir+"CrossSection_SUSYScan_"+str(mChi0)+".root")
    hist = file.Get("CrossSection/CrossSections")
    c = r.TCanvas("c", "c", 1000, 1000)
    hist.Draw("TEXT")
    c.SaveAs("plots/Numbers/CrossSection_"+str(mChi0)+".png")

def get_xsec(mChi0, mSquark, mGluino):
    file = r.TFile(dir+"CrossSection_SUSYScan_"+str(mChi0)+".root")
    hist = file.Get("CrossSection/CrossSections")
    return hist.GetBinContent(int((mSquark - 400)/80) + 1, int((mGluino - 400)/80) + 1)

def get_background():
    f_data = r.TFile.Open(dir+"PF_ra3tight_PhotonHad_Run2011A_uptoRun171106_1.root")
    cont = f_data.Get("StandardPlots_HT_cont/nEvents")
    data = f_data.Get("StandardPlots_HT_sele/nEvents")
    draw_hist_with_overflow(data, "Data")
    bkgd = renormalise(cont, data)
    draw_hist_with_overflow(bkgd, "plots/Numbers/QCD")
    sb_cont = f_data.Get("StandardPlots_HT_sb_cont/nEvents")
    sb_data = f_data.Get("StandardPlots_HT_sb_sele/nEvents")
    draw_hist_with_overflow(sb_data, "plots/Numbers/sb_Data")
    sb_bkgd = renormalise(sb_cont, sb_data)
    draw_hist_with_overflow(sb_bkgd, "plots/Numbers/sb_QCD")
    f_mc = r.TFile.Open(dir+"PF_ra3tight_TuneZ2_pythia6.root")
    mc_cont = f_mc.Get("StandardPlots_HT_cont/nEvents")
    mc_data = f_mc.Get("StandardPlots_HT_sele/nEvents")
    draw_hist_with_overflow(mc_data, "plots/Numbers/mc_Data")
    mc_bkgd = renormalise(mc_cont, mc_data)
    bkgderror = mc_data - mc_bkgd
    bkgderror.Divide(mc_data)
    bkgderror.Scale(0.5)
    bkgderror.Multiply(bkgd)
    draw_hist_with_overflow(bkgderror, "plots/Numbers/Bkgd_error")
    text = "    Observation = "+make_list(data)+",\n"
    text = text + "    Background = "+make_list(bkgd)+",\n"
    text = text + "    BackgroundError = "+make_list(bkgderror)+",\n"
    return text

def extract_numbers(f, mChi0, mSquark, mGluino, intlumi, intlumierror, obs_and_bkd_text):
    n = get_file_number(mSquark, mGluino)
    print n
    f_susy = r.TFile.Open(dir+"PF_ra3tight_SUSYScan_"+str(mChi0)+"_"+str(n)+".root")
    susy = f_susy.Get("StandardPlots_HT_sele/nEvents")
    draw_hist_with_overflow(susy, "plots/Numbers/SUSY_"+str(mChi0)+"_"+str(mSquark)+"_"+str(mGluino))
    f_susy_jesplus = r.TFile.Open(dir+"PF_ra3tight_JESplus_SUSYScan_"+str(mChi0)+"_"+str(n)+".root")
    susy_jesplus = f_susy_jesplus.Get("StandardPlots_HT_sele/nEvents")
    draw_hist_with_overflow(susy_jesplus, "plots/Numbers/SUSY_"+str(mChi0)+"_"+str(mSquark)+"_"+str(mGluino)+"_JESplus")
    f_susy_jesminus = r.TFile.Open(dir+"PF_ra3tight_JESminus_SUSYScan_"+str(mChi0)+"_"+str(n)+".root")
    susy_jesminus = f_susy_jesminus.Get("StandardPlots_HT_sele/nEvents")
    susy_jes = susy_jesplus - susy_jesminus
    susy_jes.Scale(0.5)
    draw_hist_with_overflow(susy_jesminus, "plots/Numbers/SUSY_"+str(mChi0)+"_"+str(mSquark)+"_"+str(mGluino)+"_JESminus")
    xsec = get_xsec(mChi0, mSquark, mGluino)
    xsecerror = 0.1*xsec
    f.write(make_pset(obs_and_bkd_text, susy, susy_jes, intlumi, intlumierror, xsec, xsecerror, mSquark, mGluino))

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
for mSquark in [400, 480, 560, 640, 720, 800, 880, 960, 1040, 1120, 1200, 1280, 1360, 1440, 1520, 1600, 1680, 1760, 1840, 1920, 2000]:
    for mGluino in [400, 480, 560, 640, 720, 800, 880, 960, 1040, 1120, 1200, 1280, 1360, 1440, 1520, 1600, 1680, 1760, 1840, 1920, 2000]:
        print "Extracting numbers for mSquark = "+str(mSquark)+"; mGluino = "+str(mGluino)+"."
        extract_numbers(f, mChi0, mSquark, mGluino, intlumi, intlumierror, obs_and_bkd_text)
        input_data_list.append("inputData_"+str(mChi0)+"_"+str(mSquark)+"_"+str(mGluino))
f.write("inputData = ["+", ".join(id for id in input_data_list)+"]")
