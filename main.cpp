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
DigitalOut led2(LED2);
RpcDigitalOut RPCled2(LED2,"LED2");

////////////////////////////////////////////////////

/* Thread */
Thread park_thread;
Thread line_thread;
Thread aptag_thread;

/* EventQueue */
EventQueue park_event;
EventQueue line_event;
EventQueue aptag_event;

/* Function */
void park() {};
void line();
void aptag() {};
void RPC();   // read RPC command

////////////////////////////////////////////////////

int main() 
{
   /* set up three mode */ 
   park_event.call(&park);
   line_event.call(&line);
   aptag_event.call(&aptag);
   park_thread.start(callback(&park_event, &EventQueue::dispatch_forever));
   line_thread.start(callback(&line_event, &EventQueue::dispatch_forever));
   aptag_thread.start(callback(&aptag_event, &EventQueue::dispatch_forever));

   char buf[256], outbuf[256];
   FILE *devin = fdopen(&xbee, "r");
   FILE *devout = fdopen(&xbee, "w");
   while (1) {
      memset(buf, 0, 256);
      for( int i = 0; ; i++ ) {
         char recv = fgetc(devin);
         cout << recv; // 
         if(recv == '\n') {
            printf("\r\n");
            break;
         }
         buf[i] = fputc(recv, devout);
      }
   RPC::call(buf, outbuf);
   }
}
////////////////////////////////////////////////////

void RPC()
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