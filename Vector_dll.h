#ifndef _FID_CPMG_DLL___INCLUDE_H____
#define _FID_CPMG_DLL___INCLUDE_H____
#endif

#ifdef __cplusplus
extern "C" {
#endif

//functions in DLL

int __stdcall SetComPortn(int port_number);    	
//port_number=1:com1; 
//port_number=2:com2;


int __stdcall CloseCommPort(int port_number);
//port_number=1:com1;
//port_number=2:com2;


void __stdcall SetSpeed(int Channel,int Speed);
//Channel = 0,1,2,3 = X,Y,Z,L chaneel
//Speed =-4096~4095
	

void __stdcall SetDistance(int Channel,int Distance);
//Channel = 0,1,2,3 = X,Y,Z,L channel
//Distance = -2^30~2^30-1


void __stdcall SetMaxSpeed(int channel,int MaxSpeed);
//Channel = 0,1,2,3,4 = X,Y,Z,L,joint channel
//MaxSpeed =-4096~4095

int __stdcall GetDisplay(int Channel);
//Channel = 0,1,2,3 = X,Y,Z,L chaneel

int __stdcall GetStatus(int Content);
//Content = 0/1/2 = stage/joint status/home


void __stdcall SetJointData(int Joint[4],int Total_Seg,double Modulus[400],double Component[400][4]);
//Joint[0,1,2,3] = 0/1 = [X,Y,Z,L] not/in joint action;
//Total_Seg: Total number of line segment(0~400)
//Compnent[400][0,1,2,3] = [X,Y,Z,L] component;


void __stdcall TrigJointAction(int Repeat);
//Repeat: joint action repeat times


void __stdcall Stop(void);
//Stop all motors immediately



#ifdef __cplusplus
}
#endif


