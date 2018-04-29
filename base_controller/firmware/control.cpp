#include <ros.h>
#include <std_msgs/String.h>

#include <Arduino.h>

#include "Encoder.h"
Encoder left(3, 2);       //motor place number = 3
Encoder right(18, 19);      //motor place number = 4

char odom_str[50];

int left_motor_a = 5;
int left_motor_b = 6;
int left_motor_en = 4;

int right_motor_a = 7;
int right_motor_b = 8;
int right_motor_en = 9;

ros::NodeHandle nh;

std_msgs::String odom_msg;
ros::Publisher odom_pub("odom_pub", &odom_msg);

void stop_bot();
void move_front(int spd);
void move_back(int spd);
void move_left(int spd);
void move_right(int spd);
void move_bot(char dir, int spd);


void base_cmdCallback(const std_msgs::String& in_cmd){
  String ss = ((const char * ) in_cmd.data);
  char s[ss.length() + 1];
  ss.toCharArray(s, ss.length() + 1);

  char *p = s;
  char dir_ = String(strtok_r(p, ",", &p))[0];
  int mag_ = String(strtok_r(p, ",", &p)).toInt();
  move_bot(dir_, mag_);
}

ros::Subscriber<std_msgs::String> sub("base_cmd", &base_cmdCallback);

void setup(){
  nh.initNode();
  nh.advertise(odom_pub);
  nh.subscribe(sub);

  pinMode(right_motor_a, OUTPUT);
  pinMode(right_motor_b, OUTPUT);
  pinMode(left_motor_a, OUTPUT);
  pinMode(left_motor_b, OUTPUT);

  analogWrite(right_motor_en, 0);
  analogWrite(left_motor_en, 0);
}

void loop(){
  // ###################### Better use this ##############################
  long leftEn = left.read();
  long rightEn = right.read();
  leftEn = round(2 *(leftEn)/17.067);
  rightEn = round(2 *(rightEn)/17.067);
  // ######################################################################

  char l[10];
  dtostrf(leftEn, 6, 2, l);

  char r[10];
  dtostrf(rightEn, 6, 2, r);

  String s = String(l) + "," + String(r);
  s.toCharArray(odom_str, 50);

  odom_msg.data = odom_str;
  odom_pub.publish(&odom_msg);

  nh.spinOnce();

  // while(Serial.available()){
  //   char c = Serial.readStringUntil('\n')[0];
  //   move_bot(c, 100);
  // }
}

void stop_bot(){
  digitalWrite(right_motor_a, HIGH);
  digitalWrite(right_motor_b, HIGH);
  analogWrite(right_motor_en, 0);
  digitalWrite(left_motor_a, HIGH);
  digitalWrite(left_motor_b, HIGH);
  analogWrite(left_motor_en, 0);

}
void move_front(int spd){
  digitalWrite(right_motor_a, HIGH);
  digitalWrite(right_motor_b, LOW);
  analogWrite(right_motor_en, spd);
  digitalWrite(left_motor_a, HIGH);
  digitalWrite(left_motor_b, LOW);
  analogWrite(left_motor_en, spd);

}

void move_back(int spd){
  digitalWrite(right_motor_a, LOW);
  digitalWrite(right_motor_b, HIGH);
  analogWrite(right_motor_en, spd);
  digitalWrite(left_motor_a, LOW);
  digitalWrite(left_motor_b, HIGH);
  analogWrite(left_motor_en, spd);

}

void move_left(int spd){
  digitalWrite(right_motor_a, HIGH);
  digitalWrite(right_motor_b, LOW);
  analogWrite(right_motor_en, spd);
  digitalWrite(left_motor_a, LOW);
  digitalWrite(left_motor_b, HIGH);
  analogWrite(left_motor_en, spd);

}
void move_right(int spd){
  digitalWrite(right_motor_a, LOW);
  digitalWrite(right_motor_b, HIGH);
  analogWrite(right_motor_en, spd);
  digitalWrite(left_motor_a, HIGH);
  digitalWrite(left_motor_b, LOW);
  analogWrite(left_motor_en, spd);

}
void move_bot(char dir, int spd){
  switch(dir){
  case 'a':
    move_left(spd);
    break;
  case 'w':
    move_front(spd);
    break;
  case 'd':
    move_right(spd);
    break;
  case 's':
    move_back(spd);
    break;
  default:
    stop_bot();
  }
}
