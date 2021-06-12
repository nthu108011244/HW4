#include <iostream>
#include "mbed.h"
#include "bbcar.h"
#include "bbcar_rpc.h"
using namespace std;

/* BBcar */
Ticker servo_ticker;
PwmOut pin5(D5); // left wheel (yellow)
PwmOut pin6(D6); // right wheel (orange)
BBCar car(pin5, pin6, servo_ticker);

/* Xbee */
BufferedSerial xbee(D1, D0); //tx,rx

/* Uart */
BufferedSerial pc(USBTX,USBRX); //tx,rx
BufferedSerial uart(D10,D9); //tx,rx

/* DigitalOut */
DigitalOut led1(LED1); // for aptag
DigitalOut led2(LED2); // for line 
DigitalOut led3(LED3); // for ping
DigitalOut d4(D4);
DigitalInOut d11(D11);
RpcDigitalOut RPCled1(LED1,"LED1"); 
RpcDigitalOut RPCled2(LED2,"LED2");

/* Ping */


////////////////////////////////////////////////////

/* Thread */
Thread rpc_thread;
Thread park_thread;
Thread line_thread;
Thread aptag_thread;
Thread ping_thread;

/* EventQueue */
EventQueue rpc_event;
EventQueue park_event;
EventQueue line_event;
EventQueue aptag_event;
EventQueue ping_event;

/* Function */
void readRPC();   // read RPC command
void park() {};
void line();
void aptag();
void dectPing();

////////////////////////////////////////////////////

int main() 
{
   /* set up three mode */
   rpc_event.call(&readRPC);
   park_event.call(&park);
   line_event.call(&line);
   aptag_event.call(&aptag);
   //ping_event.call(&dectPing);
   rpc_thread.start(callback(&rpc_event, &EventQueue::dispatch_forever));
   park_thread.start(callback(&park_event, &EventQueue::dispatch_forever));
   line_thread.start(callback(&line_event, &EventQueue::dispatch_forever));
   aptag_thread.start(callback(&aptag_event, &EventQueue::dispatch_forever));
   //ping_thread.start(callback(&ping_event, &EventQueue::dispatch_forever));

   //readRPC();
   dectPing();
}
////////////////////////////////////////////////////

void readRPC()
{
   char buf[256], outbuf[256];
   FILE *devin = fdopen(&xbee, "r");
   FILE *devout = fdopen(&xbee, "w");
   while (1) {
      memset(buf, 0, 256);
      for( int i = 0; ; i++ ) {
         char recv = fgetc(devin);
         if(recv == '\n') {
            printf("\r\n");
            break;
         }
         buf[i] = fputc(recv, devout);
      }
   RPC::call(buf, outbuf);
   }
}

void line()
{
   uart.set_baud(9600);
   while (1) {
      if (uart.readable() && led2) {
         char recv[1];
         uart.read(recv, sizeof(recv));

         if (recv[0] == 'y') car.goStraight(200);
         else if (recv[0] == 'n') car.stop();

         if (!led2) car.stop();
      }
   }
}

void dectPing()
{
   parallax_ping ping(d11);

   while (1) {
      if(float(ping) < 20 & !led1) {
         led3 = 1;
         d4 = 1;
         car.stop();

         if(!led1) {
            car.goStraight(-200);
            ThisThread::sleep_for(100ms);
            car.stop();
         }
      }
      else {
         led3 = 0;
         d4 = 0;
      }

      char buffer[20];
      sprintf(buffer, "ping: %.2f\r\n", float(ping));
      pc.write(buffer, sizeof(buffer));
      ThisThread::sleep_for(100ms);
   }
}

void aptag()
{
   uart.set_baud(9600);
    while (1) {
      if (uart.readable()) {
         char recv[1];
         uart.read(recv, sizeof(recv));
         //pc.write(recv, sizeof(recv));
         if (led1) {
            if (recv[0] == 'w') {
               car.goStraight(200);
               ThisThread::sleep_for(100ms);
            }
            else if (recv[0] == 'd') {
               car.turn(200, 1);
               ThisThread::sleep_for(100ms);
            }
            else if (recv[0] == 'a') {
               car.turn(200, -1);
               ThisThread::sleep_for(100ms);
            }
            car.stop();
            ThisThread::sleep_for(100ms);
         }
      }  
   }
}