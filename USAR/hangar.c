#pragma config(Sensor, S1,     leftSensor,     sensorTouch)
#pragma config(Sensor, S2,     rightSensor,    sensorTouch)
#pragma config(Motor,  motorA,          rightMotor,    tmotorNXT, PIDControl, reversed, encoder)
#pragma config(Motor,  motorB,          leftMotor,     tmotorNXT, PIDControl, reversed, encoder)
//*!!Code automatically generated by 'ROBOTC' configuration wizard               !!*//

int rightTurns = 0;
task main()
{
	clearTimer(T1);
	// Motors are reversed to drive backwards.
	while(true) {
		if (time1[T1] > 15000) {
			motor[leftMotor] = -25;
			motor[rightMotor] = -60; //50
			wait1Msec(2000);
			clearTimer(T1);
		}
		else if (SensorValue[leftSensor] || SensorValue[rightSensor]) {
			clearTimer(T1);
			rightTurns += 1;
			motor[leftMotor] = -20;
			motor[rightMotor] = -20;
			wait1Msec(900);
			motor[leftMotor] = 0;
			motor[rightMotor] = 0;
			wait1Msec(200);
			if (rightTurns < 15) {
				motor[leftMotor] = 30;
				motor[rightMotor] = -30;
			}
			else {
				motor[leftMotor] = -30;
				motor[rightMotor] = 30;
			}
			wait1Msec(1050);
		}
		else {
			motor[leftMotor] = 20;
			motor[rightMotor] = 20;
		}
	}

}
