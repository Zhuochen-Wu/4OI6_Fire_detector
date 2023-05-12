
#include <wiringPi.h>
#include <softPwm.h>
#include <sys/time.h>
#include <stdio.h>
#include <stdlib.h>

#define ON  1       
#define OFF 0       

int Left_motor_go = 28;   
int Left_motor_back = 29; 

int Right_motor_go = 24;  
int Right_motor_back = 25;

int Left_motor_pwm = 27;  
int Right_motor_pwm = 23; 

int key = 10;             

int EchoPin = 30;         
int TrigPin = 31;         

int ServoPin = 4;

int ServoPos = 90;

const int AvoidSensorLeft =  26; 
const int AvoidSensorRight = 0;  

int LeftSensorValue ;           
int RightSensorValue ;

void brake();
void spin_left(int);
void spin_right(int);
void back(int);
float Distance_test();
void bubble(unsigned long *, int);


void servo_pulse(int ServoPin, int myangle)
{
  int PulseWidth;                    
  PulseWidth = (myangle * 11) + 500; 
  digitalWrite(ServoPin, HIGH);      
  delayMicroseconds(PulseWidth);     
  digitalWrite(ServoPin, LOW);      
  delay(20 - PulseWidth / 1000);     
  return;
}


void servo_appointed_detection(int pos)
{
  int i = 0;
  for (i = 0; i <= 15; i++)    
  {
    servo_pulse(ServoPin, pos);
  }
}


void servo_color_carstate()
{
  float distance;
  int iServoPos = 0;
  int LeftDistance = 0;    
  int RightDistance = 0;   
  int FrontDistance = 0;  
  back(80);               
  brake();

  
  servo_appointed_detection(0);
  delay(500);
  distance = Distance_test();  
  RightDistance = distance;    
  
  servo_appointed_detection(165);
  delay(500);
  distance = Distance_test();  
  LeftDistance = distance;
  // printf("leftdistance :%d\n",LeftDistance);

  servo_appointed_detection(75);
  delay(500);
  distance = Distance_test();
  FrontDistance = distance;
  //printf("FrontDistance:%d\n",FrontDistance);
 
  if (LeftDistance < 30 && RightDistance < 30 && FrontDistance < 30  )
  {
    spin_right(700);
  }
  else if ( LeftDistance >= RightDistance) 
  {
    
    spin_left(350);
  }
  else if (LeftDistance < RightDistance ) 
  {
    
    spin_right(350);
  }
}

void run(int LeftSpeed, int RightSpeed)
{
  digitalWrite(Left_motor_go, HIGH);   
  digitalWrite(Left_motor_back, LOW);  
  softPwmWrite(Left_motor_pwm, LeftSpeed);

  digitalWrite(Right_motor_go, HIGH);  
  digitalWrite(Right_motor_back, LOW); 
  softPwmWrite(Right_motor_pwm, RightSpeed);
}

void brake()
{
  digitalWrite(Left_motor_go, LOW);
  digitalWrite(Left_motor_back, LOW);
  digitalWrite(Right_motor_go, LOW);
  digitalWrite(Right_motor_back, LOW);
}

void left()
{
  digitalWrite(Left_motor_go, LOW);    
  digitalWrite(Left_motor_back, LOW);  
  softPwmWrite(Left_motor_pwm, 0);


  digitalWrite(Right_motor_go, HIGH);  
  digitalWrite(Right_motor_back, LOW); 
  softPwmWrite(Right_motor_pwm, 80);
}

void right()
{
 
  digitalWrite(Left_motor_go, HIGH);   
  digitalWrite(Left_motor_back, LOW);  
  softPwmWrite(Left_motor_pwm, 80);

  digitalWrite(Right_motor_go, LOW);   
  digitalWrite(Right_motor_back, LOW); 
  softPwmWrite(Right_motor_pwm, 0);
}

void spin_left(int time)
{
  digitalWrite(Left_motor_go, LOW);     
  digitalWrite(Left_motor_back, HIGH);  
  softPwmWrite(Left_motor_pwm, 100);

  digitalWrite(Right_motor_go, HIGH);  
  digitalWrite(Right_motor_back, LOW); 
  softPwmWrite(Right_motor_pwm, 70);

  delay(time);
}

void spin_right(int time)
{
  digitalWrite(Left_motor_go, HIGH);   
  digitalWrite(Left_motor_back, LOW);  
  softPwmWrite(Left_motor_pwm, 70);

  digitalWrite(Right_motor_go, LOW);    
  digitalWrite(Right_motor_back, HIGH);
  softPwmWrite(Right_motor_pwm, 100);

  delay(time);
}


void back(int time)
{
  
  digitalWrite(Left_motor_go, LOW);     
  digitalWrite(Left_motor_back, HIGH);  
  softPwmWrite(Left_motor_pwm, 80);

  digitalWrite(Right_motor_go, LOW);    
  digitalWrite(Right_motor_back, HIGH); 
  softPwmWrite(Right_motor_pwm, 80);

  delay(time);
}


float Distance()
{
	float distance;
	struct timeval tv1;
	struct timeval tv2;
	struct timeval tv3;
	struct timeval tv4;
	long start, stop;
	
	digitalWrite(TrigPin, LOW);
	delayMicroseconds(2);
	digitalWrite(TrigPin, HIGH);      
	delayMicroseconds(15);
	digitalWrite(TrigPin, LOW);
    
	
    gettimeofday(&tv3, NULL);        
	start = tv3.tv_sec * 1000000 + tv3.tv_usec;
	while(!digitalRead(EchoPin) == 1)
	{
		gettimeofday(&tv4, NULL);    
		stop = tv4.tv_sec * 1000000 + tv4.tv_usec;
		
		if ((stop - start) > 30000)  
		{
			return -1;               
		}
	} 
	
	
	gettimeofday(&tv1, NULL);      
    start = tv1.tv_sec*1000000+tv1.tv_usec;
	while(!digitalRead(EchoPin) == 0)
	{
		gettimeofday(&tv3,NULL);   
		stop = tv3.tv_sec*1000000+tv3.tv_usec;
		if ((stop - start) > 30000)
		{
			return -1;
		}
	}                              
	gettimeofday(&tv2, NULL);      

	start = tv1.tv_sec * 1000000 + tv1.tv_usec;
	stop = tv2.tv_sec * 1000000 + tv2.tv_usec;

	distance = (float)(stop - start)/1000000 * 34000 / 2;
	return distance;
}

float Distance_test()
{
  float distance;
  unsigned long ultrasonic[5] = {0};
  int num = 0;
  while (num < 5)
  {
     distance = Distance();
	 while((int)distance == -1)
	 {
		 distance = Distance();
	 }
    while ( distance >= 500 || (int)distance == 0)
    {
         distance = Distance();
    }
    ultrasonic[num] = distance;
    num++;
	delay(10);
  }
  num = 0;
  bubble(ultrasonic, 5);
  distance = (ultrasonic[1] + ultrasonic[2] + ultrasonic[3]) / 3;
  
  printf("distance:%f\n",distance);    
  return distance;
}

void bubble(unsigned long *a, int n)

{
  int i, j, temp;
  for (i = 0; i < n - 1; i++)
  {
    for (j = i + 1; j < n; j++)
    {
      if (a[i] > a[j])
      {
        temp = a[i];
        a[i] = a[j];
        a[j] = temp;
      }
    }
  }
}

void key_scan()
{
  while (digitalRead(key));       
  while (!digitalRead(key))       
  {
    delay(10);	                  
    if (digitalRead(key)  ==  LOW)
    {
      delay(100);
      while (!digitalRead(key));  
    }
  }
  return;
}

void main()
{
  float distance;
  wiringPiSetup();	
  pinMode(Left_motor_go, OUTPUT);
  pinMode(Left_motor_back, OUTPUT);
  pinMode(Right_motor_go, OUTPUT);
  pinMode(Right_motor_back, OUTPUT);
  softPwmCreate(Left_motor_pwm,0,255); 
  softPwmCreate(Right_motor_pwm,0,255);
  pinMode(key, INPUT);
  pinMode(EchoPin, INPUT);    
  pinMode(TrigPin, OUTPUT);  
  servo_appointed_detection(ServoPos);
  pinMode(ServoPin, OUTPUT);
  pinMode(AvoidSensorLeft, INPUT);
  pinMode(AvoidSensorRight, INPUT);
  key_scan();
  
  while(1)
  {
   distance = Distance_test();        
   if (distance > 50  )   
   {
    LeftSensorValue = digitalRead(AvoidSensorLeft);
    RightSensorValue = digitalRead(AvoidSensorRight);
    if (LeftSensorValue == HIGH && RightSensorValue == LOW)
    {
      spin_left(200); 
    }
    else if (RightSensorValue == HIGH && LeftSensorValue == LOW)
    {
      spin_right(200);
    }
    else if (RightSensorValue == LOW && LeftSensorValue == LOW)
    {
      spin_left(200);
    }
    run(80, 80);
  }
  else if ((distance >= 30 && distance <= 50))
  {
    LeftSensorValue = digitalRead(AvoidSensorLeft);
    RightSensorValue = digitalRead(AvoidSensorRight);

    if (LeftSensorValue == HIGH && RightSensorValue == LOW)
    {
      spin_left(200); 
    }
    else if (RightSensorValue == HIGH && LeftSensorValue == LOW)
    {
      spin_right(200);
    }
    else if (RightSensorValue == LOW && LeftSensorValue == LOW)
    {
      spin_left(200);
    }
    run(60, 60);
  }
  else if (  distance < 30  )
  {
    servo_color_carstate();
  }
 }
	return;
}



