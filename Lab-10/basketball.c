task main()
{

	motor[motorB] = 50;
<<<<<<< HEAD
	motor[motorC] = -30;
	wait1Msec(2000);
	for(int i = 0; i < 4; i++) {
=======
	wait1Msec(1000);
	motor[motorC] = -30;
	wait1Msec(200);
	for(int i = 0; i < 6; i++) {
		if (i == 1) {
			motor[motorB] = 60;
		}
		if (i == 2) {
			motor[motorB] = 70;
		}
		if (i == 3) {
			motor[motorB] = 80;
		}
		if (i == 4) {
			motor[motorB] = 95;
		}
		if (i == 5) {
			motor[motorB] = 110;
		}
		motor[motorC] = -30;
		wait1Msec(1250);
>>>>>>> origin/master
		motor[motorC] = 0;
		motor[motorA] = -20;
		wait1Msec(320 + i * 7);
		motor[motorA] = 0;
		wait1Msec(50);
		if (i != 5) {
			motor[motorA] = 20;
			wait1Msec(320 + i * 7);
		}
		motor[motorA] = 0;
		motor[motorC] = -30;
		wait1Msec(800);

	}
}
