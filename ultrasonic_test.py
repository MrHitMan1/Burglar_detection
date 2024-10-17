import RPi.GPIO as GPIO
import time

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for Trigger and Echo
TRIG_PIN = 23  # Replace with your actual GPIO pin for TRIG
ECHO_PIN = 24  # Replace with your actual GPIO pin for ECHO

# Set up the GPIO pins
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

def measure_distance():
    # Ensure trigger is low
    GPIO.output(TRIG_PIN, False)
    time.sleep(2)  # Allow the sensor to settle

    # Send a 10 microsecond pulse to trigger the sensor
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)  # 10 microseconds
    GPIO.output(TRIG_PIN, False)

    # Wait for the Echo pin to go HIGH (start the pulse) with a timeout
    timeout_start = time.time()
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()
        if time.time() - timeout_start > 1:  # Timeout after 1 second
            print("Timeout waiting for Echo to go HIGH")
            return None

    # Wait for the Echo pin to go LOW (end the pulse) with a timeout
    timeout_start = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()
        if time.time() - timeout_start > 1:  # Timeout after 1 second
            print("Timeout waiting for Echo to go LOW")
            return None

    # Calculate the time difference between start and end
    pulse_duration = pulse_end - pulse_start

    # Calculate the distance (speed of sound is 34300 cm/s)
    distance = pulse_duration * 17150  # Distance in centimeters
    distance = round(distance, 2)  # Round to two decimal places

    return distance

try:
    while True:
        distance = measure_distance()
        if distance is not None:
            print(f"Distance: {distance} cm")
        else:
            print("Failed to measure distance")
        time.sleep(1)

except KeyboardInterrupt:
    print("Measurement stopped by user")
    GPIO.cleanup()  # Reset GPIO settings
