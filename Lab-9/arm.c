
void move(int angle1, int angle2){
	float scaleFactor = 5;
	if(angle1 > 80) {
		scaleFactor = 5.2;
	}
	int speed = 20;
	angle1 = -1*angle1;
	while(abs(nMotorEncoder[motorA] - angle1*scaleFactor) > 2){
		writeDebugStreamLine("motor A %d", nMotorEncoder[motorA]);
		if(angle1*scaleFactor < nMotorEncoder[motorA]){
			motor[motorA] = -speed;
		}
		else
			motor[motorA] = speed;
	}
	motor[motorA] = 0;

	while(abs(nMotorEncoder[motorB] - angle2 * scaleFactor) > 2){
		writeDebugStreamLine("motor B %d", nMotorEncoder[motorB]);
		if(angle2*scaleFactor < nMotorEncoder[motorB]){
			motor[motorB] = -speed;
		}
		else
			motor[motorB] = speed;
	}
	motor[motorB] = 0;
}

task main()
{
	nMotorEncoder[motorA] = 0;
	nMotorEncoder[motorB] = 0;


	//Add generated code here:
move(0, 0);
move(16, 0);
move(16, 65);

wait1Msec(3000);
// At point A
move(15.963441595611839, 64.95478563822485);
move(16, 65);
move(44, 65);
move(44, 78);
move(84, 68);
wait1Msec(3000);
// At point B
move(84, 68);
move(16, 78);
move(16, 65);
move(15.963441595611839, 64.95478563822485);
wait1Msec(3000);
// At point A
move(15.963441595611839, 64.95478563822485);
move(16, 65);
move(0, 65);
move(0, 0);
	//move(-170, 0);
}
