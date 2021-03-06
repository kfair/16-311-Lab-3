#pragma config(Sensor, S1,     lightSensor,    sensorLightActive)
#pragma config(Sensor, S2,     ultrasonic,     sensorSONAR)
#pragma config(Motor,  motorA,          leftMotor,     tmotorNXT, PIDControl, encoder)
#pragma config(Motor,  motorB,          rightMotor,    tmotorNXT, PIDControl, encoder)
//*!!Code automatically generated by 'ROBOTC' configuration wizard               !!*//

// Line following values
int black = 35;
int white = 55;
int waitTime = 1;
int speed = 35;
float curve = 6.5;

// Dead recknoning values
float tickAngle = 360 / 16.0;

// Sonar values
int distance = 30;
int sonar = SensorValue(ultrasonic);
int prevSonar[5];
int prevAvg = SensorValue(ultrasonic);

// Localization values
int map[16];
float whereWeAre[16];
float probsCopy[16];

// Line following functions
task straight()
{
		motor[leftMotor] = speed + curve;
		motor[rightMotor] = speed - curve;
}
task left()
{
		motor[leftMotor] = speed - curve;
		motor[rightMotor] = speed + curve;
}
task right()
{
		motor[leftMotor] = speed + 2*curve;
		motor[rightMotor] = speed - 2*curve;
}

//Dead Reckoning
float position2(int rightDegrees) {
	return rightDegrees / 800.0 * 90.0;
}

void updateProbabilities() {
	for (int i = 0; i < 16; i++) {
		whereWeAre[i] = whereWeAre[i] * (map[i] + .5);
		if(map[i] == 1){
			if(i == 0){
				whereWeAre[15] = whereWeAre[15] * 1.25;
			}
			else {
				whereWeAre[i-1] = whereWeAre[i-1]*1.25;
	  	}
	  	if(i == 15){
	  		whereWeAre[0] = whereWeAre[0] *1.25;
	  	}
	  	else{
	  		whereWeAre[i+1] = whereWeAre[i+1] * 1.25;
	  	}
	  }

		writeDebugStream("%f ", map[i] + .5);
	}
	writeDebugStreamLine("");
}

void blurProbabilities() {
	float filter[3];
	//Convolution filter for blurring the probabilities.
	filter[0] = 0.1;
	filter[1] = 0.8;
	filter[2] = 0.1;
	for (int i = 0; i < 16; i++) {
		probsCopy[i] = whereWeAre[i];
	}
	for (int i = 0; i < 16; i++) {
		whereWeAre[i] = 0;
		for (int j = 0; j < 3; j++) {
			int pIndex = i + j - 1;
			if (pIndex < 0) {
				pIndex += 16;
			}
			if(pIndex > 15){
				pIndex -= 16;
			}
			whereWeAre[i] += filter[j] * probsCopy[pIndex];
		}
	}
}

bool seenLastOne(int ticks, int wallsSeen){
	int sum = 0;
	for (int i = 0; i < 16; i++){
		sum += map[i];
	}
	return(sum <= wallsSeen);
}

bool determineLocation(){
	float maxProb = 0;
	for(int i = 0; i<16; i++){
		if(whereWeAre[i] > maxProb){
			maxProb = whereWeAre[i];
		}
	}
	int count = 0;
	for(int i = 0; i <16; i++){
		if(abs(whereWeAre[i] - maxProb) < .01){
			count++;
		}
	}
	return (count == 1 && maxProb >= 1)
}

task main()
{
	int goal = 11;
	map[0] = 1; map[1] = 0; map[2] = 0; map[3] = 0;
	map[4] = 0; map[5] = 0; map[6] = 0; map[7] = 1;
	map[8] = 0; map[9] = 0; map[10] = 0; map[11] = 0;
	map[12] = 0; map[13] = 0; map[14] = 0; map[15] = 0;

	float angle = 0;
	float ticks = 0;
	bool foundFirstWall = false;

	int wallsSeen = 0;

	nMotorEncoder[leftMotor] = 0;
	nMotorEncoder[rightMotor] = 0;

	int valTime1 = time1[T1];

	while (time1[T1] < valTime1 + 3000){
		//Line following
		int light = SensorValue(lightSensor);
		if (light < black)
		{
			motor[leftMotor] = 10 - 2*curve;
			motor[rightMotor] = 10 + 2* curve;
		}
		else if (light > white)
		{
			startTask(right);
		}
		else
		{
			startTask(straight);
		}
	}

	while ((!seenLastOne(ticks, wallsSeen)||!determineLocation()) && valTime1 + 60000 > time1[T1])
	{
		//Line following
		int light = SensorValue(lightSensor);
		if (light < black)
		{
			startTask(left);
		}
		else if (light > white)
		{
			startTask(right);
		}
		else
		{
			startTask(straight);
		}

		sonar = SensorValue(ultrasonic);

		angle = position2(nMotorEncoder[rightMotor]);

		int prevTicks = ceil(ticks);
		ticks = ((angle / tickAngle));

		if ((sonar < distance) && (prevAvg >= distance)) {

			writeDebugStreamLine("PrevSonar: %f, %f, %f, %f, %f", prevSonar[0], prevSonar[1], prevSonar[2], prevSonar[3], prevSonar[4]);
			writeDebugStreamLine("CurrentSonar: %f", sonar);

		  prevSonar[0] = sonar;
			prevSonar[1] = sonar;
			prevSonar[2] = sonar;
			prevSonar[3] = sonar;
			prevSonar[4] = sonar
			wallsSeen += 1;
			writeDebugStreamLine("Ticks %f", ticks);
			writeDebugStreamLine("Walls Seen %f", wallsSeen);
			playTone(500, 25); while(bSoundActive);
			if (!foundFirstWall) {
				//Only start counting ticks from our first wall.
				nMotorEncoder[leftMotor] = 0;
				nMotorEncoder[rightMotor] = 0;
				for(int i = 0; i <16; i++){
					whereWeAre[i] = map[i];
				}
				ticks = 0;
				prevTicks = 0;
			}
			else{
				writeDebugStreamLine("%f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f", whereWeAre[0], whereWeAre[1], whereWeAre[2], whereWeAre[3], whereWeAre[4], whereWeAre[5], whereWeAre[6], whereWeAre[7], whereWeAre[8], whereWeAre[9], whereWeAre[10], whereWeAre[11], whereWeAre[12], whereWeAre[13], whereWeAre[14], whereWeAre[15]);
				updateProbabilities();
				writeDebugStreamLine("%f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f", whereWeAre[0], whereWeAre[1], whereWeAre[2], whereWeAre[3], whereWeAre[4], whereWeAre[5], whereWeAre[6], whereWeAre[7], whereWeAre[8], whereWeAre[9], whereWeAre[10], whereWeAre[11], whereWeAre[12], whereWeAre[13], whereWeAre[14], whereWeAre[15]);
			}
			foundFirstWall = true;

			}
		prevSonar = sonar;
		if (foundFirstWall && prevTicks != ceil(ticks) && prevTicks != 0) {
			float save = whereWeAre[15];
			for(int i = 15; i >= 1; i--){
				whereWeAre[i] = whereWeAre[i-1];
			}
			whereWeAre[0] = save;

			writeDebugStreamLine("Shifting!!!");
			writeDebugStreamLine("Ticks: %d", ceil(ticks));
			writeDebugStreamLine("%f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f", whereWeAre[0], whereWeAre[1], whereWeAre[2], whereWeAre[3], whereWeAre[4], whereWeAre[5], whereWeAre[6], whereWeAre[7], whereWeAre[8], whereWeAre[9], whereWeAre[10], whereWeAre[11], whereWeAre[12], whereWeAre[13], whereWeAre[14], whereWeAre[15]);
		}

		int sum = 0;
		//update previous sonar values
		for (int i = 0; i < 4; i++){
			prevSonar[i] = prevSonar[i+1];
			sum = sum + prevSonar[i];
		}
		sum = sum + sonar;
		sum = sum - prevSonar[0];
		prevSonar[4] = sonar;

		prevAvg = sum/4;

		wait1Msec(waitTime);
	}
	int whereWeThinkWeAre = 0;
	float maxProb = 0;
	for (int i = 0; i < 16; i++) {
		if(whereWeAre[i] > maxProb) {
			maxProb = whereWeAre[i];
			whereWeThinkWeAre = i;
		}
	}
	ticks = 0;
	float distance = (goal - whereWeThinkWeAre) % 16 + 0.3;
	if (distance < 0) {
		distance += 16;
	}
	writeDebugStreamLine("Goal: %d Where we think we are: %d Distance: %f", goal, whereWeThinkWeAre, distance);
	nMotorEncoder[rightMotor] = 0;
	while(ticks < distance) {

		//Line following
		int light = SensorValue(lightSensor);
		if (light < black)
		{
			startTask(left);
		}
		else if (light > white)
		{
			startTask(right);
		}
		else
		{
			startTask(straight);
		}
		angle = position2(nMotorEncoder[rightMotor]);
		ticks = ((angle / tickAngle));
	}
}
