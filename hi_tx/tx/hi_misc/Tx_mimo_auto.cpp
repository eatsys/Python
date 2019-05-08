// IQAPIDemo.cpp : Defines the entry point for the console application.
//


#include "stdafx.h"
#include "IQmeasure.h"
#include "iqapiDefines.h"
#include <math.h>
#include <stdio.h>
#include <conio.h>			// For _kbhit
#include <Windows.h>
#include <direct.h>
#ifndef __IQ_MODE__
#define __IQ_MODE__
#include <fstream>
#include <iostream>
using namespace std;
typedef enum{
	IQ_MODE_11B = 0, 
	IQ_MODE_11G, 
	IQ_MODE_11A, 
	IQ_MODE_11N_20, 
	IQ_MODE_11N_40, 
	IQ_MODE_MAX
} IQ_MODE;
#endif

#define MAX_BUFFER_SIZE   4096;
static char sEchoBuf[1024];
static int g_debug_printf;

enum VSA_ENUM;

void help()
{
	cout<< "******* PARAM COMMAND ****************\n"
		<< "EXAMPLE:\n "
		<<"	MIMO_TX_Auto.exe -m 11n -f 2412\n"
		<< "\t	-m --> specify FR mode as 11g, 11a, 11n, 11ac;\n"
		<< "\t	-f --> specify the recieve freqenecy of Radio as 2412, 5800 ...\n"
		//<<"\t	-b --> specify the bandwith;\n"
		//<< "\t	-i --> specify the IQxel's interface as 1 or 2;\n"
		//<< "\t	-c --> specify the AP's chain as 1 or 2;\n"
		//<<"\t	-p --> specify the correction power of FR;\n"
		<< "\t	-h|help --> help;\n"
		<< "********************************\n"<<endl;
	
}
int wifiTest(char *mode, double freq, float power1,float power2)
{
	int hr = ERR_OK;
	double maxsiglevel = 0;
	double tFreq = freq*1000000;
	float correctPwr1=power1;
	float correctPwr2=power2;
	

	char buf[256];
	char *ip;
	ifstream infile;//定义，以输入方式打开文件，文件名infile
	infile.open("IQAdress.txt");//只有一个文件名参数，普通方式打开
	//以上两句等同于 ifstream infile("CorrectPwrTable.txt")
	
	if(infile.is_open())          //文件打开成功.  file.open打开文件，file.is_open打开文件成功返回true
	{
		//cout<<"打开"<<endl;
		while(infile.good() && !infile.eof())//while(infile.good() && !infile.eof())//eof状态标识符，bool型返回值；eof-文件到达末尾时返回true;good-其它任一状态标识符返回true,次函数返回false
		{
			memset (buf,0,256);
			infile.getline(buf,1024);//
			ip = buf;
			cout<<"Setting IP:"<<ip<<endl;
		}
	}

	if (ERR_OK == hr)  hr = LP_Init(IQTYPE_XEL,0);		// 
	//printf("\n\nERROR1: %s\n", LP_GetErrorString(hr));
	//if (ERR_OK == hr)  hr = LP_Term();
	

	//if (ERR_OK == hr)  hr = LP_IQXEL160_DualHead_ConOpen(3,0,ip); 

	if (ERR_OK == hr)  hr = LP_InitTester2(ip,ip,1);   //	if (ERR_OK == hr)  hr = LP_InitTester2("192.168.100.254", "192.168.100.253");			// 连接仪器
	
	if(hr)
		printf("Disconnected to IQXel! \n");
	else
		printf("Connected to IQXel! \n");
	//VSA--------------------------------------------------------------------------------------------------------------------------------------------
	/*
	
	char vbuffer[65535];
	LP_GetVersion(vbuffer,65535);
	cout<<vbuffer<<endl;

	if (ERR_OK == hr)
	{
		double re_level_dbm[4]={10,10,10,10};
		int vsa_Ports[4]={2,3,0,0};  // 设置仪器VSA的参数

		if (ERR_OK == hr) hr = LP_SetVsaNxN(tFreq,re_level_dbm,vsa_Ports);	
		// 设置仪器VSA的参数
		printf("\n\nERROR2: %s\n", LP_GetErrorString(hr));
		if (ERR_OK == hr) hr = LP_EnableVsgRFNxN(0,0,0,0);
		printf("\n\nERROR3: %s\n", LP_GetErrorString(hr));

		char *buff[100];
		memset(buff,0,100);
		_getcwd(*buff,100);
	}
	//VSA--------------------------------------------------------------------------------------------------------------------------------------------
*/

	if (ERR_OK == hr)
	{
		if (ERR_OK == hr) hr = LP_SetVsa(tFreq,0,0);		
		char *m1,*m2,*m3,*m4,*m5,*m6,*m7,*m8,*m9;
		m1 = "SYS;MVSA:DEL";
		m2 = "SYS;MROUT:DEL";
		m3 = "MVSA:DEF:ADD VSA11";
		m4 = "MVSA:DEF:ADD VSA12";
		m5 = "MROUT:DEF:ADD ROUT11";
		m6 = "MROUT:DEF:ADD ROUT12";
		m7 = "MROUT1;PORT:RES RF1A,VSA11";
		m8 = "MROUT2;PORT:RES RF2A,VSA12";
		m9 = "MVSAALL;FREQ 2412000000";

		if (ERR_OK == hr) hr = 	LP_ScpiCommandSet (m1);
		if (ERR_OK == hr) hr = 	LP_ScpiCommandSet (m2);
		if (ERR_OK == hr) hr = 	LP_ScpiCommandSet (m3);
		//printf("\n\nERROR2: %s\n", LP_GetErrorString(hr));
		if (ERR_OK == hr) hr = 	LP_ScpiCommandSet (m4);
		if (ERR_OK == hr) hr = 	LP_ScpiCommandSet (m5);
		if (ERR_OK == hr) hr = 	LP_ScpiCommandSet (m6);
		if (ERR_OK == hr) hr = 	LP_ScpiCommandSet (m7);
		if (ERR_OK == hr) hr = 	LP_ScpiCommandSet (m8);
		//if (ERR_OK == hr) hr =  LP_ScpiCommandSet (m9);
		//printf("\n\nERROR3: %s\n", LP_GetErrorString(hr));
	}
	//VSA--------------------------------------------------------------------------------------------------------------------------------------------

	
	Sleep(100);

	//Analyze--------------------------------------------------------------------------------------------------------------------------------------------
	
	if (ERR_OK == hr)  
	{
			hr = ERR_OK;

			if (ERR_OK == hr)  hr = LP_Agc(&maxsiglevel);						// AGC
			// Analysis Signal ...............

			Sleep(100);
			cout << "WiFi's mode is : "<< mode<< "\n";
			if (strcmp(mode,"n") == 0) //
			{

				if (ERR_OK == hr)  hr = LP_VsaDataCapture(5000e-6);
				cout << "Setting analyze for 11n ...\n";
				//printf("\n\nERROR4: %s\n", LP_GetErrorString(hr));


				if (ERR_OK == hr)  hr = LP_Analyze80211n("EWC","nxn",1,1,0,1,1);
				//printf("\n\nERROR5: %s\n", LP_GetErrorString(hr));
			}
			
			if (strcmp(mode,"ac") == 0) //
			{

				if (ERR_OK == hr)  hr = LP_VsaDataCapture(5000e-6,1,160e6);
				cout << "Setting analyze for 11ac ...\n";

				if (ERR_OK == hr)  hr = LP_Analyze80211ac("nxn", 1, 1, 0, 0, 1, 2, 0, NULL, 0);
			}

			if (ERR_OK == hr) 
			{
				
				
				if (strcmp(mode,"n") == 0 )
				{
					printf("\n\n--------11n results ---------\n");
					printf("Rate: %.2fMbps\n",LP_GetScalarMeasurement("rateInfo_dataRateMbps"));
					printf("Power_A: %.2fdBm\n",LP_GetScalarMeasurement("powerPreambleDbm",0)+correctPwr1);
					printf("Power_B: %.2fdBm\n",LP_GetScalarMeasurement("powerPreambleDbm",1)+correctPwr2);
					printf("EVM_A: %.2fdB\n", LP_GetScalarMeasurement("evmAvgAll",0));
					printf("EVM_B: %.2fdB\n", LP_GetScalarMeasurement("evmAvgAll",1));
					printf("Freq Error_A: %.2fppm\n",LP_GetScalarMeasurement("symClockErrorPpm",0));
					printf("Freq Error_B: %.2fppm\n",LP_GetScalarMeasurement("symClockErrorPpm",1));
					printf("LO_Leakage_A: %.2fdB\n",LP_GetScalarMeasurement("dcLeakageDbc",0));
					printf("LO_Leakage_B: %.2fdB\n",LP_GetScalarMeasurement("dcLeakageDbc",1));	
					cout<<"----------------------------\r\n";
				}
					
				
				if (strcmp(mode,"ac") ==  0 )
				{
					printf("\n\n--------11ac results ---------\n");
					printf("Rate: %.2fMbps\n",LP_GetScalarMeasurement("rateInfo_dataRateMbps"));
					printf("Power_A: %.2fdBm\n",LP_GetScalarMeasurement("powerPreambleDbm",0)+correctPwr1);
					printf("Power_B: %.2fdBm\n",LP_GetScalarMeasurement("powerPreambleDbm",1)+correctPwr2);
					printf("EVM_A: %.2fdB\n", LP_GetScalarMeasurement("evmAvgAll",0));
					printf("EVM_B: %.2fdB\n", LP_GetScalarMeasurement("evmAvgAll",1));
					printf("Freq Error_A: %.2fppm\n",LP_GetScalarMeasurement("symClockErrorPpm",0));
					printf("Freq Error_B: %.2fppm\n",LP_GetScalarMeasurement("symClockErrorPpm",1));
					printf("LO_Leakage_A: %.2fdB\n",LP_GetScalarMeasurement("dcLeakageDbc",0));
					printf("LO_Leakage_B: %.2fdB\n",LP_GetScalarMeasurement("dcLeakageDbc",1));
					cout<<"----------------------------\r\n";
				}
					
				getchar();

			}
			else
			{
				printf("\n\nERROR6: %s\n", LP_GetErrorString(hr));
			}
		//}
	}

	// ---------------------------------------------------------------------------------------
	if (ERR_OK != hr)
	{
		printf("\n\nERROR7: %s\n", LP_GetErrorString(hr));
	}

	hr = LP_Term();
	

	return 0;

}
int _tmain(int argc, _TCHAR* argv[])
{

	char *wMode;
	double wFreq;
	int wBW, i;



	if(argc < 2) 
	{
		help();
		return 0;
	}

    for (i=0; i < argc; i++)
    {
		if (*(argv[i]) == '-')
		{
			switch (tolower (*(argv[i]+1)))
			{
				case 'h':
					help();
					return 0;
				case 'm':			
					wMode = argv[++i];
					cout << "Mode is :" << wMode <<"\n";
					break;
				case 'f':
					wFreq = atoi(argv[++i]);
					cout << "Freq is :" << wFreq <<"\n";
					break;
				case 'b':
					wBW = atoi(argv[++i]);
					cout << "BW is :" << wBW <<"\n";
					break;

				default:
					break;
            }
			//return 0;
        }
	}
	
	const char *d = ",";
	char *p;
	char *ptr=NULL;

	struct freq_param {
	int		freq;
	float	power[5];
};
	
	struct freq_param	freqs[100];
	int					freq_count = 0;


	char buf[1024];                //临时保存读取出来的文件内容
	memset(buf,0,1024);//清零存储空间
	ifstream infile;			  //定义，以输入方式打开文件，文件名infile
	infile.open("CorrectPwrTable.txt");//只有一个文件名参数，普通方式打开
	//以上两句等同于 ifstream infile("CorrectPwrTable.txt")
	if(infile.is_open())          //文件打开成功.  file.open打开文件，file.is_open打开文件成功返回true
	{
		while(infile.good() && !infile.eof())//eof状态标识符，bool型返回值；eof-文件到达末尾时返回true;good-其它任一状态标识符返回true,次函数返回false
		{
			
			infile.getline(buf,1024);
			//cout<<buf<<endl;
			p=strtok_s(buf,d,&ptr);
			//cout<<"判断文件"<<p<<endl;
			if (p) {
				
				//cout	<< "freq is : " << atoi(p) << endl;
				if (atoi(p) == 0) {
					
					continue;
				}
				//cout	<< "freq: " << p << endl;
				freqs[freq_count].freq = atoi(p);
				//cout<<"如果是频率则赋值频率"<<freqs[freq_count].freq<<endl;  
				int	pn = 0;
				while(p!=NULL && pn < 2)
				{
					p=strtok_s(NULL,d,&ptr);
					freqs[freq_count].power[pn++] = atof(p);
					//cout<<"从当前频率下赋值功率"<<p<<endl;   
				}
				freq_count++;
				//cout<<"频率计数"<<freq_count<<endl;   
			}
			
		}
		infile.close();
	}

	for (i = 0; i < freq_count; i++) {
		if (freqs[i].freq == wFreq) 
		{
			//cout << wMode << "\t" << wFreq <<"\t" <<iPort<< "\t" << freqs[i].power[wChain] << endl;
			cout<<"Channel:"<<freqs[i].freq<<"\nChainA.Att:"<<freqs[i].power[0]<<"\nChainB.Att:"<<freqs[i].power[1]<<endl;
			wifiTest(wMode,wFreq,freqs[i].power[0],freqs[i].power[1]);	
		}
	}


	
	_getch();
	return 0; 
}


