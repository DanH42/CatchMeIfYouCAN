import sys, socket
from pykeyboard import PyKeyboard
import time

BRAKING = "30"
ACCEL = "00"
LIGHTS = "00"
WIPERS = "00"
STEERING = 0
STEERING_RELEASE = time.time()
NEED_DELAY = 0
MAX_LOCK = 0.1
k = PyKeyboard()

" CTRL " 
def process_braking_change():
	if BRAKING == "30":
		k.release_key(k.control_key)
		print("We are no longer braking.")
	else:
		k.press_key(k.control_key)
		print("We are braking.")
" SHIFT "
def process_accel_change():
	if ACCEL == "00":
		k.release_key(k.shift_key)
		print("We are no longer accel.")
	else:
		k.press_key(k.shift_key)
		print("We are accel.")

" C " 
def process_lights_change():
	if LIGHTS == "00":
		k.release_key("c")
		print("We are no longer lights.")
	else:
		k.press_key("c")
		print("We are lights.")

" Z " 
def process_wipers_change():
	if WIPERS == "00":
		k.release_key("z")
		print("We are no longer wipers.")
	else:
		k.press_key("z")
		print("We are wipers.")

" Direction Keys " 
def process_steering_change():
	if STEERING == 0:
		k.release_key(k.left_key)
		k.release_key(k.right_key)
		print("We are driving straight.")
	elif STEERING < 0:
		k.release_key(k.right_key)
		k.press_key(k.left_key)
		print("We are turning left.")
	elif STEERING > 0:
		k.release_key(k.left_key)
		k.press_key(k.right_key)
		print("We are turning right.")


def process_packet(line):
	global BRAKING, ACCEL, LIGHTS, WIPERS, STEERING, STEERING_RELEASE, NEED_DELAY, MAX_LOCK

	processed = line.split(" ")
	if len(processed) < 4 or not len(processed[3]):
		return

	if processed[0] == "17C" and len(processed) > 7 and processed[7] in ["30", "31"] and processed[7] != BRAKING:
		BRAKING = processed[7]
		process_braking_change()

	current_accel = "00" if processed[3] == "00" else "FF"
	if processed[0] == "17C" and current_accel != ACCEL:
		ACCEL = current_accel
		process_accel_change()

	current_lights = "FF" if processed[3] == "07"  else "00"
	if processed[0] == "1A6" and current_lights != LIGHTS:
		LIGHTS = current_lights
		process_lights_change()

	current_wipers = "00" if processed[3] == "04" else "FF"
	if processed[0] == "294" and current_wipers != WIPERS:
		WIPERS = current_wipers
		process_wipers_change()

	if processed[0] == "156":
		cur_time = time.time()
		if STEERING_RELEASE < cur_time:
			current_steering = 0
			if NEED_DELAY == 1:
				# add delay and start again
				STEERING_RELEASE = cur_time + 0.01
				NEED_DELAY = 0
 			else:
				steering_num = int(processed[3] + processed[4], 16)

				STEERING_THRESHOLD = 128
				if 65535 - STEERING_THRESHOLD > steering_num > 32767:
					current_steering = -1
					diff = 65535 - steering_num
				elif STEERING_THRESHOLD < steering_num < 32767:
					current_steering = 1
					diff = steering_num
				else:
					diff = 0

				if diff > 818:
					STEERING_RELEASE = cur_time + MAX_LOCK
				else:
					STEERING_RELEASE = cur_time + (MAX_LOCK * (float(diff) / 818))
				NEED_DELAY = 1

			if current_steering != STEERING:
				STEERING = current_steering
				process_steering_change()

UDP_IP = "10.0.0.20"
UDP_PORT = 1738

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
	data, addr = sock.recvfrom(512)
	lines = data.split("\n")
	for line in lines:
		if line.startswith("  can0"):
			process_packet(line[8:])
