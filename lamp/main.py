import RPi.GPIO as GPIO
import time as unix_time_

from datetime import datetime, time


PIR_PIN = 17
RELAY_PIN = 25

BLOCK_MODE_START = time(hour=6)
BLOCK_MODE_END = time(hour=19)
DEFAULT_STATE = {'state': False, 'time': None}

DELAY_EVENT = 5 * 60

def is_in_block_mode(now):
    time_part = now.time()
    return time_part >= BLOCK_MODE_START and time_part < BLOCK_MODE_END

def main():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(PIR_PIN, GPIO.IN)
    GPIO.setup(RELAY_PIN, GPIO.OUT)

    first_state = False

    previous_event = {'state': first_state, 'time': None}

    while True:
        now = datetime.now()

        if not is_in_block_mode(now):
            pir_input = GPIO.input(PIR_PIN)
            delta = None
            new_state = None

            if pir_input:
                previous_time = previous_event['time']
                if previous_time is None:
                    delta = DELAY_EVENT
                else:
                    delta = (now - previous_time).total_seconds()

                if delta >= DELAY_EVENT:
                    previous_state = previous_event['state']
                    new_state = previous_state

                    if not previous_state:
                        GPIO.output(RELAY_PIN, GPIO.HIGH)
                        new_state = True
                    else:
                        GPIO.output(RELAY_PIN, GPIO.LOW)
                        new_state = False

                    previous_event = {'state': new_state, 'time': now}
            print(now, ' pir ', pir_input, ' delta ', delta, ' new state ', new_state)
        else:
            print(now, ' in blocking time')
        unix_time_.sleep(1)


if __name__ == '__main__':
    main()
