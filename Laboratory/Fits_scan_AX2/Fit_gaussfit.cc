#include <iostream>  // for cout
#include <math.h>    // for sqrt
#include <stdio.h>   // for printf()
#include <fstream>   // for wrinting
using namespace std;


static const Int_t N=5000;



void Fit_gaussfit(){
    //int binx=208; //width
    //int biny=134; //height
    int binx;
    int biny;
    int binx_min;
    int binx_max;
    int biny_min;
    int biny_max;
    
    ifstream ifs2("width_height_for_root.txt");
    ifs2 >> binx >> biny >> binx_min >> binx_max >> biny_min >> biny_max;
    printf("%d, %d, %d, %d, %d, %d\n", binx, biny, binx_min, binx_max, biny_min, biny_max);
    printf("x_min = %f, y_min = %f\n", binx_min +0.5, biny_min +0.5);

    
    //TH2F *h = new TH2F("name","title; X; Y", binx, binx_min+0.5, binx_max+0.5, biny, biny_min+0.5, biny_max+0.5);
    TH2F *h = new TH2F("name","title; X; Y", binx, 0+0.5, binx+0.5, biny, 0+0.5, biny+0.5);


    double data[binx][biny];


    
    ifstream ifs("test.txt");
    
    
    string dummy;
    
    int count =0;
    int x=0;
    int y=0;
    int x2;
    int y2;
    for(y=0; y<biny; y++){
        for(x=0; x<binx; x++){
            x2 = 0;
            y2 = 0;
            x2 = binx_min + x;
            y2 = biny_min + y;
            data[x][y]=0;
            ifs >> data[x][y];
            int bin = h->GetBin(x,y);
            h -> SetBinContent(bin,data[x][y]);
            
            //cout<<x<<","<<y<<","<<bin << ","<<data[x][y]<<endl;
        }
    }
    
    



    //void SetBinContent(Int_t x, Int_t y, Double_t content);
    h->Fill(x,y);
    h->Draw("colz");


    
    printf("Complete!!!\n***************************\n");
    
    
 
}
