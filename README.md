# HW4

# mbed (mian.cpp)
Each part has its own thread and eventQueue, moreover, ping use the main thread.

## BBCar
Control the BBCar.
``` bash
''' global variable '''
Ticker servo_ticker;
PwmOut pin5(D5); # left wheel 
PwmOut pin6(D6); # right wheel (orange)
BBCar car(pin5, pin6, servo_ticker);
```

## openMV
Receive signal from openMV.
``` bash
''' global variable '''
BufferedSerial uart(D10,D9); # tx,rx
```

## Ping
If the distance is smaller than 20 (cm), then red LED and LED3 wiil turn on, what's more, BBCar wiil go back.
``` bash
''' global variable '''
DigitalOut led3(LED3);
DigitalOut d4(D4);      # for red LED
DigitalInOut d11(D11);  # for ping

''' function '''
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
```

## RPC
Always read RPC command from PC (python).
``` bash
''' global variable '''
BufferedSerial xbee(D1, D0); #  tx, rx
RpcDigitalOut RPCled1(LED1,"LED1"); 
RpcDigitalOut RPCled2(LED2,"LED2");

Thread rpc_thread;
EventQueue rpc_event;

''' function '''
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
```

## Parking mode
Here, mbed does nothing in parking mode.

## Line-following mode
Read the signal from openMV, and do the corresponding action.\
y -> go.\
n -> stop.
``` bash
''' global variable '''
DigitalOut led2(LED2); # for line 

Thread line_thread;
EventQueue line_event;

''' function '''
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
``` 

## AprilTag-following mode
Read the signal from openMV, and do the corresponding action.\
w -> go.\
d -> spin clockwise.\
a -> soin counterclockwise.
``` bash
''' global variable '''
DigitalOut led1(LED1); # for aptag

Thread aptag_thread;
EventQueue aptag_event;

''' function '''
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
``` 