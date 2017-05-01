task main()
{

	motor[motorB] = 50;
	motor[motorC] = -30;
	wait1Msec(2000);
	for(int i = 0; i < 4; i++) {
		motor[motorC] = 0;
		motor[motorA] = -20;
		wait1Msec(300);
		motor[motorA] = 0;
		wait1Msec(50);
		motor[motorA] = 20;
		wait1Msec(300);
		motor[motorA] = 0;
		motor[motorC] = -30;
		wait1Msec(800);

	}
}
