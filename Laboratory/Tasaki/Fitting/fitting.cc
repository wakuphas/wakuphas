#include <iostream>  // for cout
#include <math.h>    // for sqrt
#include <stdio.h>   // for printf()
#include <fstream>   // for wrinting

using namespace std;


//static const Int_t N=19; //3.0cm 
//static const Int_t N=17; //0.0cm 
//static const Int_t N=14; //0.1cm
static const Int_t N=12; //observed
//static const Int_t N=11; //r=1m, 10m, bigreal2pi, bigreallimited
//static const Int_t N=18; //2pi, 1cm
//static const Int_t N=20; //2pi, 1cm
//static const Int_t N=19; //2pi, 0.0cm



void fitting(){




  double lag[N];
  double dcf[N];
  double counts[N];
  double n[N];



  //ifstream ifs("662cts_soil=0cm_2pi_r=10m.dat"); // 0.0cm
  //ifstream ifs("662cts_soil=0cm_2pi_r=1m.dat"); // 0.0cm
  //ifstream ifs("662cts_hosei_soildepth0_bigRealCsI_2pi.dat"); //bigReal2pi
  //ifstream ifs("662cts_hosei_soildepth0_bigRealCsI_limitedAngle.dat"); //bigRealLimited
  //ifstream ifs("662cts_hosei_soildepth0.dat"); // 0.0cm
  //ifstream ifs("662cts_hosei_soildepth0.1cm.dat"); // 0.1cm
  //ifstream ifs("662cts_hosei.dat"); // 3.0cm
  ifstream ifs("observed662_hpk.dat"); // Observed hpk
  //ifstream ifs("ALL_alt_662cts.dat"); // 
  //ifstream ifs("all.dat"); //2pi 0.0cm


  string dummy;

  for(int i=0; i<N; i++)
    {
      //ifs >> lag[i] >> counts[i] >> dcf[i];
      ifs >> lag[i] >> dcf[i];
    }


  printf("\n***************************\n");


  Double_t gaussian (Double_t *a, Double_t *par){
    Double_t Gauss,x;
    x = a[0];
    //Gauss = 2.5e-4 * log(pow(sqrt(par[1]*par[1]-x*x)/x, 2)+1) * par[0];
    Gauss = 2.5e-4 * log(pow(par[1]/x, 2)+1) * par[0];

    return Gauss;
  }


  
  TGraphAsymmErrors *graph1;
  
  graph1 = new TGraphAsymmErrors(N, lag, dcf, 0,0, 0,0);
  TCanvas *c = new TCanvas("c", "DCF", 600, 600);
  graph1->SetTitle("662keV vs. Height");
  graph1->SetMarkerStyle(21);
  graph1->Draw("ap");
  

  TF1 *f1 = new TF1("f1",gaussian, 0, 160, 2);
  f1->SetParameter(0,1.4); //第１引数が変数の番号、第２引数がその値
  f1->SetParameter(1,200);  
  //f1->SetParameter(1,69);
  f1->SetParLimits(1,60,500);

  f1->Draw("same");
  graph1->Fit("f1","","",3,160);

  printf("***************************\n");


}
