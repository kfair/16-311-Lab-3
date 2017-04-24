
void move(int angle1, int angle2){
	int scaleFactor = 5.1;
	angle1 = -1*angle1;
	while(abs(nMotorEncoder[motorA] - angle1*scaleFactor) > 2){
		writeDebugStreamLine("motor A %d", nMotorEncoder[motorA]);
		if(angle1*scaleFactor < nMotorEncoder[motorA]){
			motor[motorA] = -40;
		}
		else
			motor[motorA] = 40;
	}
	motor[motorA] = 0;

	while(abs(nMotorEncoder[motorB] - angle2 * scaleFactor) > 2){
		writeDebugStreamLine("motor B %d", nMotorEncoder[motorB]);
		if(angle2*scaleFactor < nMotorEncoder[motorB]){
			motor[motorB] = -40;
		}
		else
			motor[motorB] = 40;
	}
	motor[motorB] = 0;
}

task main()
{
	nMotorEncoder[motorA] = 0;
	nMotorEncoder[motorB] = 0;

move(0, 0);
move(0, 90);
move(0, 90.0);
wait1Msec(3000);
// At point A
move(0, 90.0);
move(0, 90);
move(113, 90);
move(112.61986494804043, 90.0);
wait1Msec(3000);
// At point B
move(112.61986494804043, 90.0);
move(113, 90);
move(0, 90);
move(0, 90.0);
wait1Msec(3000);
// At point A
move(0,0);
}
