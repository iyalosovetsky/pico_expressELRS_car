from robot_car import RobotCar
import utime
from machine import UART, Pin
uart = UART(1, baudrate=420000, bits=8, parity=None, stop=1, tx=Pin(8), rx=Pin(9))

CRSF_SYNC = 0xC8
CHANNELS=[0 for jj in range(16)]
LEFT_VERTICAL=2
LEFT_HORIZONTAL=3

RIGHT_VERTICAL=1
RIGHT_HORIZONTAL=0
E_SWITCH=4
B_SWITCH=5

F_SWITCH=7
C_SWITCH=6
A_SWITCH=8



# Pico W GPIO Pin
'''LEFT_MOTOR1_PIN_1 = 16
LEFT_MOTOR1_PIN_2 = 17
RIGHT_MOTOR1_PIN_1 = 18
RIGHT_MOTOR1_PIN_2 = 19
MOTOR1_STBY = 20

LEFT_MOTOR2_PIN_1 = 15
LEFT_MOTOR2_PIN_2 = 14
RIGHT_MOTOR2_PIN_1 = 13
RIGHT_MOTOR2_PIN_2 = 12
MOTOR2_STBY = 11
'''

''' 16 17 gnd 18 19 20
 forward nc  AIN2 AIN1 STBY BIN1 BIN2 NC GND
         -    17   16   20   18   19  -  GND
         -    blue mag  red  yel  ora -  green  
 16 17 -> 0A 0B -> AIN1 AIN2 ->magenta blue
 18 19 -> 1A 1B -> BIN1 BIN2 ->yellow orange
 20 stand by
 #0A
#define LEFT_MOTOR_FORWARD_PIN_1 18
 #0B
#define LEFT_MOTOR_FORWARD_PIN_2 19
 #1A
#define RIGHT_MOTOR_FORWARD_PIN_1 16
 #1B
#define RIGHT_MOTOR_FORWARD_PIN_2 17
#define MOTOR_FORWARD_STBY 20

/* MOTOR_BACKWARD*/
// 15 14 gnd  13 12 11
// bacward nc  AIN2 AIN1 STBY BIN1 BIN2 NC GND
//         -    15   14   11    12   13  -  GND
//         -    mage blue red oran yell  -  green  
// 14 15 -> 7A 7B -> AIN1 AIN2 -> blue magenta
// 12 13 -> 6A 6B -> BIN1 BIN2 -> orange yellow
// 11 stand by red
// #7A
#define LEFT_MOTOR_BACKWARD_PIN_1 14
// #7B
#define LEFT_MOTOR_BACKWARD_PIN_2 15
// #6A
#define RIGHT_MOTOR_BACKWARD_PIN_1 12
// #6B
#define RIGHT_MOTOR_BACKWARD_PIN_2 13
#define MOTOR_BACKWARD_STBY 11

'''
LEFT_MOTOR1_PIN_1 = 18 
LEFT_MOTOR1_PIN_2 = 19 
RIGHT_MOTOR1_PIN_1 = 16
RIGHT_MOTOR1_PIN_2 = 17
MOTOR1_STBY = 20


LEFT_MOTOR2_PIN_1 = 14
LEFT_MOTOR2_PIN_2 = 15
RIGHT_MOTOR2_PIN_1 = 12
RIGHT_MOTOR2_PIN_2 = 13
MOTOR2_STBY = 11


motor_forw_pins = [LEFT_MOTOR1_PIN_1, LEFT_MOTOR1_PIN_2, RIGHT_MOTOR1_PIN_1, RIGHT_MOTOR1_PIN_2,MOTOR1_STBY]
motor_back_pins = [LEFT_MOTOR2_PIN_1, LEFT_MOTOR2_PIN_2, RIGHT_MOTOR2_PIN_1, RIGHT_MOTOR2_PIN_2,MOTOR2_STBY]

# Create an instance of our robot car
robot_car_forw = RobotCar(motor_forw_pins, 20000)
robot_car_back = RobotCar(motor_back_pins, 20000)



#https://github.com/crsf-wg/crsf/wiki/Packet-Types
class PacketsTypes():
    # https://github.com/crsf-wg/crsf/wiki/CRSF_FRAMETYPE_GPS
    '''Telemetry Item

int32_t latitude in degrees * 1e7, big-endian
e.g. 28.0805804N sent as 0x10BCC1AC / 280805804
int32_t longitude
int16_t ground speed in km/h * 10, big-endian
e.g. 88 km/h sent as 0x0370 / 880
e.g. 15m/s sent as 0x021C / 540
int16_t ground course / GPS heading in degrees * 100, big-endian
e.g. 90 degrees sent as 0x2328 / 9000
uint16_t GPS altitude in meters + 1000m, big-endian
e.g. 0m sent as 0x03E8 / 1000
e.g. 10m sent as 0x03F2 / 1010
e.g. -10m sent as 0x03DE / 990
uint8_t satellite count'''
    GPS = 0x02
    
    #https://github.com/crsf-wg/crsf/wiki/Packet-Types
    VARIO = 0x07
    #https://github.com/crsf-wg/crsf/wiki/CRSF_FRAMETYPE_BATTERY_SENSOR
    BATTERY_SENSOR = 0x08
    #https://github.com/crsf-wg/crsf/wiki/CRSF_FRAMETYPE_BARO_ALTITUDE
    BARO_ALT = 0x09
    #https://github.com/crsf-wg/crsf/wiki/CRSF_FRAMETYPE_HEARTBEAT
    HEARTBEAT = 0x0B
    #
    VIDEO_TRANSMITTER = 0x0F
    #https://github.com/crsf-wg/crsf/wiki/CRSF_FRAMETYPE_LINK_STATISTICS
    LINK_STATISTICS = 0x14
    #https://github.com/crsf-wg/crsf/wiki/CRSF_FRAMETYPE_RC_CHANNELS_PACKED
    RC_CHANNELS_PACKED = 0x16
    ATTITUDE = 0x1E
    FLIGHT_MODE = 0x21
    DEVICE_INFO = 0x29
    CONFIG_READ = 0x2C
    CONFIG_WRITE = 0x2D
    RADIO_ID = 0x3A

def crc8_dvb_s2(crc, a) -> int:
    crc = crc ^ a
    for ii in range(8):
        if crc & 0x80:
            crc = (crc << 1) ^ 0xD5
        else:
            crc = crc << 1
    return crc & 0xFF

def crc8_data(data) -> int:
    crc = 0
    for a in data:
        crc = crc8_dvb_s2(crc, a)
    return crc

def crsf_validate_frame(frame) -> bool:
    return crc8_data(frame[2:-1]) == frame[-1]

def signed_byte(b):
    return b - 256 if b >= 128 else b


def zfl(s):
  # Pads the provided string with leading 0's to suit the specified 'chrs' length
  # Force # characters, fill with leading 0's
  return '{:0>{w}}'.format(bin(s)[2:], w=8)


rc=''

def handleCrsfPacket(ptype, data):
    global rc, CHANNELS
    if ptype == PacketsTypes.GPS:
        lat = int.from_bytes(data[3:7], byteorder='big', signed=True) / 1e7
        lon = int.from_bytes(data[7:11], byteorder='big', signed=True) / 1e7
        gspd = int.from_bytes(data[11:13], byteorder='big', signed=True) / 36.0
        hdg = int.from_bytes(data[13:15], byteorder='big', signed=True) / 100.0
        alt = int.from_bytes(data[15:17], byteorder='big', signed=True) - 1000
        sats = data[17]
        print(f"GPS: Pos={lat} {lon} GSpd={gspd:0.1f}m/s Hdg={hdg:0.1f} Alt={alt}m Sats={sats}")
    elif ptype == PacketsTypes.VARIO:
        vspd = int.from_bytes(data[3:5], byteorder='big', signed=True) / 10.0
        print(f"VSpd: {vspd:0.1f}m/s")
    elif ptype == PacketsTypes.ATTITUDE:
        pitch = int.from_bytes(data[3:5], byteorder='big', signed=True) / 10000.0
        roll = int.from_bytes(data[5:7], byteorder='big', signed=True) / 10000.0
        yaw = int.from_bytes(data[7:9], byteorder='big', signed=True) / 10000.0
        print(f"Attitude: Pitch={pitch:0.2f} Roll={roll:0.2f} Yaw={yaw:0.2f} (rad)")
    elif ptype == PacketsTypes.BARO_ALT:
        alt = int.from_bytes(data[3:7], byteorder='big', signed=True) / 100.0
        print(f"Baro Altitude: {alt}m")
    elif ptype == PacketsTypes.LINK_STATISTICS:
        rssi1 = signed_byte(data[3])
        rssi2 = signed_byte(data[4])
        lq = data[5]
        snr = signed_byte(data[6])
        print(f"RSSI={rssi1}/{rssi2}dBm LQ={lq:03}")
    elif ptype == PacketsTypes.BATTERY_SENSOR:
        vbat = int.from_bytes(data[3:5], byteorder='big', signed=True) / 10.0
        curr = int.from_bytes(data[5:7], byteorder='big', signed=True) / 10.0
        mah = data[7] << 16 | data[8] << 7 | data[9]
        pct = data[10]
        print(f"Battery: {vbat:0.2f}V {curr:0.1f}A {mah}mAh {pct}%")
    elif ptype == PacketsTypes.RC_CHANNELS_PACKED:
        zz=''
        kk=data[3:25]  
        for ii in kk:
            zz='{:0>{w}}'.format(bin(ii)[2:], w=8)+zz #+
        if zz!=rc and len(zz)==176:
            CHANNELS=[sum([(1<<(10-ii) if (zz[(15-jj)*11:(16-jj)*11])[ii]=='1' else 0) for ii in range(11)]) for jj in range(16) ]
            #print('->',CHANNELS[E_SWITCH],CHANNELS[LEFT_VERTICAL],CHANNELS[LEFT_HORIZONTAL],CHANNELS[RIGHT_VERTICAL],CHANNELS[RIGHT_HORIZONTAL])
            #print('22->',CHANNELS)
            rc=zz
            return 1
        else:
            return 0
        
            
        
    else :
        print("unknown ptype",ptype)
        return 0
    
        
 


'''input_buffer = bytearray()
while True:
     if uart.any() :
        #input_buffer.extend(uart.read())
         input_buffer=uart.read()
     else:
        time.sleep(0.010)
     if len(input_buffer) > 2:
        if input_buffer[0]!=CRSF_SYNC:
            input_buffer = []
     if len(input_buffer) > 2:       
            expected_len = input_buffer[1] + 2
            
            if expected_len > 64 or expected_len < 4:
                input_buffer = []
            elif len(input_buffer) >= expected_len:
                single_packet = input_buffer[:expected_len]
                input_buffer = input_buffer[expected_len:]
                #print(single_packet)
                if not crsf_validate_frame(single_packet):
                    packet = ' '.join(map(hex, single_packet))
                    print(f"CRC error: {packet}")
                else:
                  if single_packet[2]  == PacketsTypes.RC_CHANNELS_PACKED:
                    handleCrsfPacket(single_packet[2], single_packet)

'''

input_buffer=[]
maxLeftVertical=1700
minLeftVertical=180

maxLeftHorizontal=1700
minLeftHorizontal=180


MIN=180
MAX=1750
CENTER=992
TH=40





old_speed=0
old_arrow=0
old_turn=0
old_turn_val=0
if __name__ == '__main__':
    
    try:
        # Test forward, reverse, stop, turn left and turn right
        print("*********Testing forward, reverse and loop*********")
        '''for i in range(200):
            print("Moving forward")
            robot_car_forw.move_forward()
            robot_car_back.move_forward()
            utime.sleep(2)
            print("Moving backward")
            robot_car_forw.move_backward()
            robot_car_back.move_backward()
            utime.sleep(2)
            print("stop")
            robot_car_forw.stop()
            robot_car_back.stop()
            utime.sleep(2)
            print("turn left")
            robot_car_forw.turn_left()
            robot_car_back.turn_left()
            utime.sleep(2)
            print("turn right")
            robot_car_forw.turn_right()
            robot_car_back.turn_right()
            utime.sleep(2)

            robot_car_forw.stop()
            robot_car_back.stop()
        for i in range(2):
            print("Moving at 100% speed")
            robot_car_forw.change_speed(100);
            robot_car_back.change_speed(100);
            robot_car_forw.move_forward()
            robot_car_back.move_forward()
            utime.sleep(2)
            
            print("Moving at 50% speed")
            robot_car_forw.change_speed(50);
            robot_car_back.change_speed(50);
            robot_car_forw.move_forward()
            robot_car_back.move_forward()
            utime.sleep(2)
            
            print("Moving at 20% of speed")
            robot_car_forw.change_speed(20);
            robot_car_back.change_speed(20);
            robot_car_forw.move_forward()
            robot_car_back.move_forward()
            utime.sleep(2)
            
            print("Moving at 0% of speed or the slowest")
            robot_car_forw.change_speed(0);
            robot_car_back.change_speed(0);
            robot_car_forw.move_forward()
            robot_car_back.move_forward()
            utime.sleep(2)            '''
        while True:
          if uart.any() :
            input_buffer=uart.read()
          else:
            utime.sleep_ms(10)
          if len(input_buffer) < 3:
              input_buffer = []
              continue
          
          if input_buffer[0]!=CRSF_SYNC:
            input_buffer = []
            continue
          expected_len = input_buffer[1] + 2
          if expected_len > 64 or expected_len < 4:
             input_buffer = []
             continue
          if len(input_buffer) >= expected_len:
                single_packet = input_buffer[:expected_len]
                input_buffer = input_buffer[expected_len:]
                #print(single_packet)
                if not crsf_validate_frame(single_packet):
                    packet = ' '.join(map(hex, single_packet))
                    print(f"CRC error: {packet}")
                else:
                  if single_packet[2]  == PacketsTypes.RC_CHANNELS_PACKED:
                    if handleCrsfPacket(single_packet[2], single_packet)>0:
                      #print('->',CHANNELS[E_SWITCH],CHANNELS[LEFT_VERTICAL],CHANNELS[LEFT_HORIZONTAL],CHANNELS[RIGHT_VERTICAL],CHANNELS[RIGHT_HORIZONTAL])
                      arrow=0
                      speed=0
                      turn=0
                      turn_val=0
                      if abs(CHANNELS[LEFT_VERTICAL]-CENTER)>TH:
                        arrow=0
                        speed=abs(CHANNELS[LEFT_VERTICAL]-CENTER)/CENTER
                        if CHANNELS[LEFT_VERTICAL]-CENTER>0:
                            arrow=1
                        else:
                            arrow=-1
                        #print('dir',arrow,speed)

                      if abs(CHANNELS[RIGHT_HORIZONTAL]-CENTER)>TH:
                        turn=0
                        turn_val=abs(CHANNELS[RIGHT_HORIZONTAL]-CENTER)/CENTER
                        if CHANNELS[RIGHT_HORIZONTAL]-CENTER>0:
                            turn=1
                        else:
                            turn=-1
                        #print('turn',turn,turn_val)


                      if CHANNELS[E_SWITCH]>CENTER and  (old_arrow!=arrow or old_speed!=speed or old_turn!=old_turn or old_turn_val!=turn_val):
                          old_arrow=arrow 
                          old_speed=speed
                          old_turn=turn
                          old_turn_val=turn_val
                          if (arrow==0 or speed<0.12) and turn!=0 and turn_val>0.2 and (CHANNELS[LEFT_VERTICAL]-CENTER>TH//2 or CENTER-CHANNELS[LEFT_VERTICAL]>TH//2):
                              robot_car_forw.change_speed(0.19,0.);
                              robot_car_back.change_speed(0.19,0.);
                              robot_car_forw.move_reverse(turn)
                              robot_car_back.move_reverse(turn)
                                  
                          elif speed==0 or arrow==0:
                            robot_car_forw.stop()
                            robot_car_back.stop()
                          elif arrow>0:
                              robot_car_forw.change_speed(speed,turn*turn_val);
                              robot_car_back.change_speed(speed,turn*turn_val);
                              robot_car_forw.move_forward()
                              robot_car_back.move_forward()
                          elif arrow<0:
                              robot_car_forw.change_speed(speed,turn*turn_val);
                              robot_car_back.change_speed(speed,turn*turn_val);
                              robot_car_forw.move_backward()
                              robot_car_back.move_backward()
                             
                      elif CHANNELS[E_SWITCH]<=CENTER :
                            robot_car_forw.stop()
                            robot_car_back.stop()

                            



        robot_car_forw.deinit()
        robot_car_back.deinit()

    except KeyboardInterrupt:
        robot_car_forw.deinit()
        robot_car_back.deinit()