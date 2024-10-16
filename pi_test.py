#burgular detection in pi
#burgular detection in pi
import RPi.GPIO as GPIO
import time

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# PIR Sensor
PIR_PIN = 5
GPIO.setup(PIR_PIN, GPIO.IN)

# Ultrasonic Sensor
TRIG = 2
ECHO = 3
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Buzzer and LED
BUZZER_PIN = 1
LED_PIN = 4
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(LED_PIN, GPIO.OUT)

def get_distance():
    # Send a 10us pulse to TRIG
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    
    # Measure the ECHO response pulse
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        
    pulse_duration = pulse_end - pulse_start
    # Calculate distance (34300 cm/s is the speed of sound)
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    
    return distance

try:
    print("Burglar detection system activated...")
    
    while True:
        # Check motion detection from PIR sensor
        if GPIO.input(PIR_PIN):
            print("Motion detected!")
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            GPIO.output(LED_PIN, GPIO.HIGH)
            
            # Check distance from the ultrasonic sensor
            distance = get_distance()
            print(f"Distance to object: {distance} cm")
            
            if distance < 40:  # Trigger based on distance
                print("Object is too close!")
                
            time.sleep(2)  # Alert for 2 seconds
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            GPIO.output(LED_PIN, GPIO.LOW)
        
        time.sleep(1)

except KeyboardInterrupt:
    print("System deactivated")
    
finally:
    GPIO.cleanup()
