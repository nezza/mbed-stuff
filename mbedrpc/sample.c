/* Based on the code from the mbed cookbook. */
#include "mbed.h"
#include "rpc.h"

/* Configure the serial port (the USB port): */
Serial communication(USBTX, USBRX);

int main() {
	/* Add the class DigitalOut to the classes we want *
         * to use via rpc.                                 */
	Base::add_rpc_class<DigitalOut>();

	/* Other choices would be:
	     Base::add_rpc_class<AnalogIn>();
	     Base::add_rpc_class<AnalogOut>();
	     Base::add_rpc_class<DigitalIn>();
	     Base::add_rpc_class<DigitalInOut>();
	     Base::add_rpc_class<PwmOut>();
	     Base::add_rpc_class<Timer>();
	     Base::add_rpc_class<SPI>();
	     Base::add_rpc_class<BusOut>();
	     Base::add_rpc_class<BusIn>();
	     Base::add_rpc_class<BusInOut>();
	     Base::add_rpc_class<Serial>();
	*/

	/* The buffers for receiving and transmitting data.*/
	char receive_buffer[256];
	char transmit_buffer[256];

	while(1) {
		/* Receive data from host */
		communication.gets(receive_buffer, 256);
		/* Parse the data using the rpc library */
		rpc(receive_buffer, transmit_buffer);
		/* Transmit result back to host. */
		communication.printf("%s\n", transmit_buffer);
	}
}
