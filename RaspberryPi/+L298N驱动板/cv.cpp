#include<opencv2/opencv.hpp>
#include<cv.h>
#include<iostream>
#include"cxcore.h"

#include <stdio.h>//控制部分头文件
#include <stdlib.h>
#include <softPwm.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <netdb.h>
#include <sys/types.h>
#include <time.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <wiringPi.h>

using namespace cv;
using namespace std;
/*
#define MOTOR_GO_FORWARD   softPwmWrite(1,300);softPwmWrite(4,0);softPwmWrite(5,300);softPwmWrite(6,0)//M1、M2正转
#define MOTOR_GO_BACK      softPwmWrite(4,300);softPwmWrite(1,0);softPwmWrite(6,300);softPwmWrite(5,0)
#define MOTOR_GO_RIGHT     softPwmWrite(1,300);softPwmWrite(4,0);softPwmWrite(6,300);softPwmWrite(5,0)//M1正转，M2反
#define MOTOR_GO_LEFT      softPwmWrite(4,300);softPwmWrite(1,0);softPwmWrite(5,300);softPwmWrite(6,0)
#define MOTOR_GO_STOP      softPwmWrite(1, 0);softPwmWrite(4,0);softPwmWrite(5, 0);softPwmWrite(6,0)
*/
/*
#define MOTOR_GO_FORWARD   softPwmWrite(1,400);softPwmWrite(4,0);softPwmWrite(5,400);softPwmWrite(6,0)//M1、M2正转
#define MOTOR_GO_BACK      softPwmWrite(4,400);softPwmWrite(1,0);softPwmWrite(6,400);softPwmWrite(5,0)
#define MOTOR_GO_RIGHT     softPwmWrite(1,400);softPwmWrite(4,0);softPwmWrite(6,400);softPwmWrite(5,0)//M1正转，M2反
#define MOTOR_GO_LEFT      softPwmWrite(4,400);softPwmWrite(1,0);softPwmWrite(5,400);softPwmWrite(6,0)
#define MOTOR_GO_STOP      softPwmWrite(1, 0);softPwmWrite(4,0);softPwmWrite(5, 0);softPwmWrite(6,0)
*/

#define MOTOR_GO_FORWARD   softPwmWrite(1,250);softPwmWrite(4,0);softPwmWrite(5,250);softPwmWrite(6,0)//M1、M2正转
#define MOTOR_GO_BACK      softPwmWrite(4,250);softPwmWrite(1,0);softPwmWrite(6,250);softPwmWrite(5,0)
#define MOTOR_GO_RIGHT     softPwmWrite(1,300);softPwmWrite(4,0);softPwmWrite(6,0);softPwmWrite(5,50)//M1正转，M2反
#define MOTOR_GO_LEFT      softPwmWrite(4,0);softPwmWrite(1,50);softPwmWrite(5,300);softPwmWrite(6,0)
#define MOTOR_GO_STOP      softPwmWrite(1,0);softPwmWrite(4,0);softPwmWrite(5,0);softPwmWrite(6,0)

int main()
{
    VideoCapture capture(0);//打开摄像头

    int delaytime = 1;
    int whitethres = 120;
	wiringPiSetup();//电平的初始化
    /*WiringPi GPIO*/
    pinMode (1, OUTPUT);    //IN1
    pinMode (4, OUTPUT);    //IN2
    pinMode (5, OUTPUT);    //IN3
    pinMode (6, OUTPUT);    //IN4

    //pinMode (3, OUTPUT);    //beed
    
    //设置一个最初的电平
    /*Init output*/
    //digitalWrite(1,HIGH);
    //digitalWrite(4,HIGH);
    //digitalWrite(5,HIGH);
    //digitalWrite(6,HIGH);

    //create PWM 
    softPwmCreate(1,1,500);   
    softPwmCreate(4,1,500);
    softPwmCreate(5,1,500);
    softPwmCreate(6,1,500);


	Mat var;//存储图像的mat变量
	int white_num_l, white_num_r;//定义左右两端的计数变量
	int r;//定义记录差值的变量
    delay(3000);
    cout<<"init done"<<endl;
	while (1)
	{
		Mat frame;//存储信息流的mat矩阵
		capture >> frame;
		if (frame.empty())//如果无法得到图像输出语句
		{
			cout<<"--(!) No captured frame -- Break!"<<endl;
		         	break;
		}
		else//成功得到图像
		{
			Mat gray;
			cvtColor(frame, gray, CV_RGB2GRAY);//图像转化为灰度图并存入gray
			threshold(gray, var, whitethres, 255, CV_THRESH_BINARY);//将图像二值化
			//imshow("二值化图像", var);//显示图像小车运行的过程中可以忽略
			white_num_l = 0;//初始化计数变量
			white_num_r = 0;
            //Mat c = Mat::zeros(480, 6, CV_8U);
            //c.copyTo(var.colRange(0, 6));
            imshow("二值化图像", var);
            if(waitKey(delaytime)>=0){break;}
            
			for (int i = 0; i<(var.cols)/2; i++)//计数左端的白点
			{
				//for (int j = var.rows-10; j<var.rows; j++)
                for (int j = 440; j<441; j++)
				{
					int k = int(var.at<uchar>(j, i));
					if (k >= 125)
					{
						white_num_l++;
					}
				}
			}

			for (int i = (var.cols)/2; i<=(var.cols); i++)//计数右端白点
			{
				//for (int j = var.rows-10; j<var.rows; j++)
                for (int j = 440; j<441; j++)
				{
					int k = int(var.at<uchar>(j, i));

					if (k >= 125)
					{
						white_num_r++;
					}
				}
			}
            

			int t=white_num_r-white_num_l;
            cout<<"right: "<<white_num_r<<"  left: "<<white_num_l<<endl;
			r=abs(t);
            
			//if (r>300)//大于30则左右转
            if (r>40)
			{
				if(white_num_r>white_num_l)
                {
					MOTOR_GO_RIGHT;
                    delay(delaytime);
                    cout<<"turn right"<<endl;
                }
				else{
					MOTOR_GO_LEFT;
                    delay(delaytime);
                    cout<<"turn left"<<endl;
                }
			}
			else//否则直行
			{
				MOTOR_GO_FORWARD;
                delay(delaytime);
                cout<<"go forward"<<endl;
			}
			
		}
	}
    MOTOR_GO_STOP;
	return 0;
}