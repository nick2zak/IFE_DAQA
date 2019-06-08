import serial
import time 
from datetime import datetime
import threading
from serial.tools import list_ports
#from queue import Queue
import csv
import ntplib
import pynmea2
import random

filestamp = datetime.now().strftime("%Y:%m:%d-%H:%M:%S")
filename = open("CAN_log_%s.txt"%filestamp,'a+')
filename.close()
port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=3.0)

#with open("CAN_log.txt") as log:
 
while 1: 
        time =  datetime.now().strftime("%H:%M:%S")
        port.reset_input_buffer()
        receive = port.read(26)
        print(receive)
        split_msg = receive.split(',')
        #print(split_msg[0])
        print(split_msg)
        if(len(split_msg)==9):
            if(split_msg[8].endswith('\x00') and len(split_msg)==9):
                split_msg[8] = split_msg[8][:-4] 
			
        if (split_msg[0] == "A7") or (split_msg[0] == "a7" or (split_msg[0] == "167")) :
            log = open('CAN_log_%s.txt'%filestamp,'a')
            voltage_list_baby = []
            voltage_list_baby.append(time)
            voltage_list_baby.append(int(split_msg[1]+split_msg[2], 16)/10)
            voltage_list_baby.append(int(split_msg[3]+split_msg[4], 16)/10)
            voltage_list_baby.append(int(split_msg[5]+split_msg[6], 16)/10)
            voltage_list_baby.append(int(split_msg[7]+split_msg[8], 16)/10)
            # voltage_list.append(voltage_list_baby)
            voltage_print = "Time: " + str(voltage_list_baby[0]) + ", Voltage_Data -  DC Bus Voltage: " + str(voltage_list_baby[1]) + "V, Output Voltage: " + str(voltage_list_baby[2]) + "V, VAB_Vd_Voltage: " + str(voltage_list_baby[3]) + "V, VBC_Vq_Voltage: " + str(voltage_list_baby[4]) + "V\n" 
            print(voltage_print)
            log.write(voltage_print)
            log.close()
   

        elif (split_msg[0] == "A6") or (split_msg[0] == "a6") or (split_msg[0] == "166"):
            log = open('CAN_log_%s.txt'%filestamp,'a')
            current_list_baby = []
            current_list_baby.append(time)
            current_list_baby.append(int(split_msg[1]+split_msg[2], 16)/10)
            current_list_baby.append(int(split_msg[3]+split_msg[4], 16)/10)
            current_list_baby.append(int(split_msg[5]+split_msg[6], 16)/10)
            current_list_baby.append(int(split_msg[7]+split_msg[8], 16)/10)
            #current_list.append(current_list_baby)
            current_print = "Time: " + str(current_list_baby[0]) + ", Current_Data - Phase A: " + str(current_list_baby[1]) + "A, Phase B: " + str(current_list_baby[2]) + "A, Phase C: " + str(current_list_baby[3]) + "A, DC Bus: " + str(current_list_baby[4]) + "A\n" 
            print(current_print)
            log.write(current_print)
            log.close()           

        elif (split_msg[0] == "AC") or (split_msg[0] == "ac") or (split_msg[0] == "172"):
            log = open('CAN_log_%s.txt'%filestamp,'a')
            torque_list_baby = []
            torque_list_baby.append(time)
            torque_list_baby.append(int(split_msg[1]+split_msg[2], 16)/10)
            torque_list_baby.append(int(split_msg[3]+split_msg[4], 16)/10)
            torque_list_baby.append((int(split_msg[5],16) * 2^23 + int(split_msg[6],16) * 2^15 + int(split_msg[7], 16) * 2^7 + int(split_msg[8],16))/10)
            #torque_list.append(torque_list_baby)
            torque_print = "Time: " + str(torque_list_baby[0]) + ", Torque_Data - Command Torque: " + str(torque_list_baby[1]) + "Nm, Torque Feedback: " + str(torque_list_baby[2]) + ", Power on Timer: "  + str(torque_list_baby[3]) + "sec\n" 
            print(torque_print)
            log.write(torque_print)
            log.close()

        elif (split_msg[0] == "A8") or (split_msg[0] == "a8") or (split_msg[0] == "168"):
            log = open('CAN_log_%s.txt'%filestamp,'a')
            flux_list_baby = []
            flux_list_baby.append(time)
            flux_list_baby.append(int(split_msg[1]+split_msg[2], 16)/1000)
            flux_list_baby.append(int(split_msg[3]+split_msg[4], 16)/1000)
            flux_list_baby.append(int(split_msg[5]+split_msg[6], 16)/1000)
            flux_list_baby.append(int(split_msg[7]+split_msg[8], 16)/1000)
            #flux_list.append(flux_list_baby)
            flux_print = "Time: " + str(flux_list_baby[0]) + ", Flux_Data - Flux Command: " + str(flux_list_baby[1]) + ", Flux Feedback:" + str(flux_list_baby[2]) + ", Id Feedback:" + str(flux_list_baby[3]) + "A, Iq Feedback:" + str(flux_list_baby[4]) + "A\n"
            print(flux_print)
            log.write(flux_print)
            log.close()

        elif (split_msg[0] == "A0") or (split_msg[0] == "a0") or (split_msg[0] == "160"):
            log = open('CAN_log_%s.txt'%filestamp,'a')
            temperature1_list_baby = []
            temperature1_list_baby.append(time)
            temperature1_list_baby.append(int(split_msg[1]+split_msg[2], 16)/10)
            temperature1_list_baby.append(int(split_msg[3]+split_msg[4], 16)/10)
            temperature1_list_baby.append(int(split_msg[5]+split_msg[6], 16)/10)
            temperature1_list_baby.append(int(split_msg[7]+split_msg[8], 16)/10)
            #temperature1_list.append(temperature1_list_baby)
            temp1_print = "Time: "  + str(temperature1_list_baby[0]) + ", Temperature1_data - Module A Temperature: " + str(temperature1_list_baby[1]) + "C, Module B Temperature: " + str(temperature1_list_baby[2]) + "C, Module C Temperature: " + str(temperature1_list_baby[3]) + "C, Gate Driver Board Temperature: " + str(temperature1_list_baby[4]) + "C\n"
            print(temp1_print)
            log.write(temp1_print)
            log.close()

        elif (split_msg[0] == "A1") or (split_msg[0] == "a1") or (split_msg[0] == "161"):
            log = open('CAN_log_%s.txt'%filestamp,'a')
            temperature2_list_baby = []
            temperature2_list_baby.append(time)
            temperature2_list_baby.append(int(split_msg[1]+split_msg[2], 16)/10)
            temperature2_list_baby.append(int(split_msg[3]+split_msg[4], 16)/10)
            temperature2_list_baby.append(int(split_msg[5]+split_msg[6], 16)/10)
            temperature2_list_baby.append(int(split_msg[7]+split_msg[8], 16)/10)
            #temperature2_list.append(temperature2_list_baby)
            temp2_print = "Time: " + str(temperature2_list_baby[0]) + ", Temperature2_data - Central Board Temperature: " + str(temperature2_list_baby[1]) + "C, RTD_1 Temperature: " + str(temperature2_list_baby[2]) + "V, RTD_2 Temperature: " + str(temperature2_list_baby[3]) + "C, RTD_3 Temperature: " + str(temperature2_list_baby[4]) + "C\n"
            print(temp2_print)
            log.write(temp2_print)
            log.close() 

        elif (split_msg[0] == "A2") or (split_msg[0] == "a2") or (split_msg[0] == "162"):
            log = open('CAN_log_%s.txt'%filestamp, 'a')
            temperature3_list_baby = []
            temperature3_list_baby.append(time)
            temperature3_list_baby.append(int(split_msg[1]+split_msg[2], 16)/10)
            temperature3_list_baby.append(int(split_msg[3]+split_msg[4], 16)/10)
            temperature3_list_baby.append(int(split_msg[5]+split_msg[6], 16)/10)
            temperature3_list_baby.append(int(split_msg[7]+split_msg[8], 16)/10)
            #temperature3_list.append(temperature3_list_baby)
            temp3_print = "Time: " + str(temperature3_list_baby[0]) + ", Temperature_Data - RTD_4 Temperature: " + str(temperature3_list_baby[1]) + "C, RTD_5 Temperature: " + str(temperature3_list_baby[2]) + "C, Motor Temperature: " + str(temperature3_list_baby[3]) + "C, Torque Shudder: " + str(temperature3_list_baby[4]) + "Nm\n"
            print(temp3_print)
            log.write(temp3_print)
            log.close()

        elif (split_msg[0] == "A9") or split_msg[0] == 'a9':
            log = open('CAN_log_%s.txt'%filestamp, 'a')
            internal_voltage_list_baby = []
            internal_voltage_list_baby.append(time)
            internal_voltage_list_baby.append(int(split_msg[1]+split_msg[2], 16)/10)
            internal_voltage_list_baby.append(int(split_msg[3]+split_msg[4], 16)/10)
            internal_voltage_list_baby.append(int(split_msg[5]+split_msg[6], 16)/10)
            internal_voltage_list_baby.append(int(split_msg[7]+split_msg[8], 16)/10)
            #internal_voltage_list.append(internal_voltage_list_baby)
            internal_voltage_print = "Time: " + str(internal_voltage_list_baby[0]) + ", Internal_Voltage_data - 1.5V Reference Voltage: " + str(internal_voltage_list_baby[1]) + "V, 2.5V Reference Voltage: " + str(internal_voltage_list_baby[2]) + "V, 5.0V Reference Voltage:: " + str(internal_voltage_list_baby[3]) + "V, 12V Reference Voltage: " + str(internal_voltage_list_baby[4]) + "V\n" 
            print(internal_voltage_print)
            log.write(internal_voltage_print)
            log.close()

        #NEEDS WORK
        elif (split_msg[0] == "AAAAAAAAAA") or (split_msg[0] == "aaaaaa") or (split_msg[0] == "170,170,170"):
            internal_state_list_baby = []
            internal_state_list_output = []
            internal_state_list_baby.append(time)
            internal_state_list_baby.append(int((split_msg[1]) + (split_msg[2]),16))
            internal_state_list_baby.append(int(split_msg[3], 16))
            internal_state_list_baby.append(split_msg[4])
            internal_state_list_baby.append(int(split_msg[5] , 16)& 1)  #internal_state_list_baby[4]
            internal_state_list_baby.append((int(split_msg[5] , 16)& 224)/32)  #internal_state_list_baby[5]
            internal_state_list_baby.append(int(split_msg[6], 16))  #internal_state_list_baby[6]
            internal_state_list_baby.append(int(split_msg[7] , 16)& 1)  #internal_state_list_baby[7]
            internal_state_list_baby.append((int(split_msg[7] , 16)& 224)/32)  #internal_state_list_baby[8]
            internal_state_list_baby.append(int(split_msg[8] , 16)& 1)  #internal_state_list_baby[9]
            internal_state_list_baby.append(int(split_msg[8] , 16)& 2)  #internal_state_list_baby[10]
            internal_state_list_baby.append(int(split_msg[8] , 16)& 4)  #internal_state_list_baby[11]
            #internal_state_list.append(internal_state_list_baby)

            if internal_state_list_baby[1] == 0:
                internal_state_list_output.append('VSM Start State')
            elif internal_state_list_baby[1] == 1:
                internal_state_list_output.append('Pre-charge Init State')
            elif internal_state_list_baby[1] == 2:
                internal_state_list_output.append('Pre-charge Active State')
            elif internal_state_list_baby[1] == 3:
                internal_state_list_output.append('Pre-charge Complete State') 
            elif internal_state_list_baby[1] == 4:
                internal_state_list_output.append('VSM Wait State')
            elif internal_state_list_baby[1] == 5:
                internal_state_list_output.append('VSM Ready State')
            elif internal_state_list_baby[1] == 6:
                internal_state_list_output.append('Motor Running State')
            elif internal_state_list_baby[1] == 7:
                internal_state_list_output.append('Blink Fault Code State')
            elif internal_state_list_baby[1] == 14:
                internal_state_list_output.append('Shutdown in Process')
            elif internal_state_list_baby[1] == 15:
                internal_state_list_output.append('Recycle Power State')
            else:
                internal_state_list_output.append('Error Unknown Value')
            
            if internal_state_list_baby[2] == 0:
                internal_state_list_output.append('Power on State')
            elif internal_state_list_baby[2] == 1:
                internal_state_list_output.append('Stop State')
            elif internal_state_list_baby[2] == 2:
                internal_state_list_output.append('Open Loop State')
            elif internal_state_list_baby[2] == 3:
                internal_state_list_output.append('Closed Loop State')
            elif internal_state_list_baby[2] == 4:
                internal_state_list_output.append('Wait State')
            elif internal_state_list_baby[2] == 5 or internal_state_list_baby[2] == 6 or internal_state_list_baby[2] == 7:
                internal_state_list_output.append('Internal States')
            elif internal_state_list_baby[2] == 8:
                internal_state_list_output.append('Idle Run State')
            elif internal_state_list_baby[2] == 9:
                internal_state_list_output.append('Idle Stop State')
            elif internal_state_list_baby[2] == 10 or internal_state_list_baby[2] == 11 or internal_state_list_baby[2] == 12: 
                internal_state_list_output.append('Internal States')
            
            if (int(internal_state_list_baby[3],16) & 1) == 0:
                internal_state_list_output.append('Relay 1 Off')
            else:
                internal_state_list_output.append('Relay 1 On')
            
            if (int(internal_state_list_baby[3],16) & 2) == 0:
                internal_state_list_output.append('Relay 2 Off')
            else:
                internal_state_list_output.append('Relay 2 On')
            
            if (int(internal_state_list_baby[3],16) & 4) == 0:
                internal_state_list_output.append('Relay 3 Off')
            else:
                internal_state_list_output.append('Relay 3 On')
            
            if (int(internal_state_list_baby[3],16) & 8) == 0:
                internal_state_list_output.append('Relay 4 Off')
            else:
                internal_state_list_output.append('Relay 4 On')
            
            if (int(internal_state_list_baby[3],16) & 16) == 0:
                internal_state_list_output.append('Relay 5 Off')
            else:
                internal_state_list_output.append('Relay 5 On')
            
            if (int(internal_state_list_baby[3],16) & 32) == 0:
                internal_state_list_output.append('Relay 6 Off')
            else:
                internal_state_list_output.append('Relay 6 On')

            if internal_state_list_baby[4] == 0:
                internal_state_list_output.append('Torque Mode')
            elif internal_state_list_baby[4] == 1:
                internal_state_list_output.append('Speed Mode')
            
            if internal_state_list_baby[5] == 0:
                internal_state_list_output.append('Current Inverter Active Discharge State: Discharge Disabled')
            elif internal_state_list_baby[5] == 1:
                internal_state_list_output.append('Current Inverter Active Discharge State: Discharge Enabled, Waiting')
            elif internal_state_list_baby[5] == 2:
                internal_state_list_output.append('Current Inverter Active Discharge State: Performing Speed Check')
            elif internal_state_list_baby[5] == 3:
                internal_state_list_output.append('Current Inverter Active Discharge State: Discharge Actively Occurring')
            elif internal_state_list_baby[5] == 4:
                internal_state_list_output.append('Current Inverter Active Discharge State: Discharge Completed')

            if internal_state_list_baby[6] == 0:
                internal_state_list_output.append('CAN Mode')
            elif internal_state_list_baby[6] == 1:
                internal_state_list_output.append('VSM Mode')

            if internal_state_list_baby[7] == 0:
                internal_state_list_output.append('Inverter is Disabled')
            elif internal_state_list_baby[7] == 1:
                internal_state_list_output.append('Inverter is Enabled')

            if internal_state_list_baby[8] == 0:
                internal_state_list_output.append('Inverter can be Enabled')
            else :
                internal_state_list_output.append('Inverter canot be Enabled')

            if internal_state_list_baby[9] == 0:
                internal_state_list_output.append('Reverse, if inverter is enabled - Stopped, if inverter is disabled')
            elif internal_state_list_baby[9] == 1:
                internal_state_list_output.append('Forward')

            if internal_state_list_baby[10] == 0:
                internal_state_list_output.append('BMS Message is NOT being Received')
            else:
                internal_state_list_output.append('BMS Message is being Received')

            if internal_state_list_baby[11] == 0:
                internal_state_list_output.append('Torque is NOT being limited by the BMS')
            else:
                internal_state_list_output.append('Torque is being limited by the BMS')

            print(internal_state_list_output)
            
            
            #print("Internal_State_data - Time: " internal_state_list_baby[0] ", VSM State: " internal_state_list_baby[1] ", Inverter State: " internal_state_list_baby[2] ", Relay State: " internal_state_list_baby[3])
            #print(", Inverter Run Mode: " internal_state_list_baby[4] ", Inverter Active Discharge State: " internal_state_list_baby[5] "Inverter Command Mode: " internal_state_list_baby[6])
            #print(", Inverter Enable State: " internal_state_list_baby[7])
            
        #INCLUDE Analog Singals NEEDS WORK
        elif (split_msg[0] == "A3") or (split_msg[0] == "a3") or (split_msg[0] == "163"):
            log = open('CAN_log_%s.txt'%filestamp,'a')
            analog_input_voltages_list_baby = []
            analog_input_voltages_list_baby.append(time)
            analog_input_voltages_list_baby.append((int(split_msg[1] + split_msg[2] , 16)&int('1111111111000000',2))/64/10.)
            analog_input_voltages_list_baby.append((int(split_msg[2] + split_msg[3] , 16)&int('0011111111110000',2))/16/10.)
            analog_input_voltages_list_baby.append((int(split_msg[3] + split_msg[4] , 16)&int('0000111111111100',2))/4/10.)
            analog_input_voltages_list_baby.append((int(split_msg[4] + split_msg[5] , 16)&int('0000001111111111',2))/10.)
            analog_input_voltages_list_baby.append((int(split_msg[6] + split_msg[7] , 16)&int('1111111111000000',2))/64/10.)
            analog_input_voltages_list_baby.append((int(split_msg[7] + split_msg[8] , 16)&int('0011111111110000',2))/16/10.)
            #analog_input_voltages_list.append(analog_input_voltages_list_baby)
            analog_input_volt_print = "Time: " + str(analog_input_voltages_list_baby[0]) + ", Analog_Input_Voltages -  Analog Input 1: " + str(analog_input_voltages_list_baby[1]) + "V, Analog Input 2: " + str(analog_input_voltages_list_baby[2]) + "V, Analog Input 3: " + str(analog_input_voltages_list_baby[3]) + "V, Analog Input 4: " + str(analog_input_voltages_list_baby[4]) + "V, Analog Input 5: " + str(analog_input_voltages_list_baby[5]) + "V, Analog Input 6: " + str(analog_input_voltages_list_baby[6]) + '\n'
            print(analog_input_volt_print)
            log.write(analog_input_volt_print)
            log.close()

        elif (split_msg[0] == "AB") or (split_msg[0] == "ab") or (split_msg[0] == "171"):
            log = open('CAN_log_%s.txt'%filestamp,'a')
            fault_codes_list_baby = []
            fault_codes_list_baby.append(time)
            fault_codes_list_baby.append(int(split_msg[1]+split_msg[2], 16)/10)
            fault_codes_list_baby.append(int(split_msg[3]+split_msg[4], 16)/10)
            fault_codes_list_baby.append(int(split_msg[5]+split_msg[6], 16)/10)
            fault_codes_list_baby.append(int(split_msg[7]+split_msg[8], 16)/10)
            #fault_codes_list.append(fault_codes_list_baby)
            fault_codes_print = "Time: " + str(fault_codes_list_baby[0]) + ", Fault_Codes_Data - POST Fault Lo: " + str(fault_codes_list_baby[1]) + " POST Fault HI: " + str(fault_codes_list_baby[2]) + " Run Fault Lo: " + str(fault_codes_list_baby[3]) + " Run Fault Hi: " + str(fault_codes_list_baby[4]) + '\n'
            print(fault_codes_print)
            log.write(fault_codes_print)
            log.close()


        elif (split_msg[0] == "007") or (split_msg[0] == "7"):
            log = open('CAN_log_%s.txt'%filestamp,'a')
            cell_data_list_baby = []
            cell_data_output = []
            cell_data_list_baby.append(time)
            cell_data_list_baby.append(int(split_msg[1], 16))
            cell_data_list_baby.append(int(split_msg[2], 16))
            cell_data_list_baby.append(int(split_msg[3], 16)/1000.)
            cell_data_list_baby.append(int(split_msg[4], 16)/1000.)
            cell_data_list_baby.append(int(split_msg[5], 16)/500.-20)
            cell_data_list_baby.append(int(split_msg[6], 16)/500.-20)
            #cell_data_list.append(cell_data_list_baby)
            status_byte = cell_data_list_baby[2]

            if(status_byte & 1 ==0):
                cell_data_output.append(", Cell is NOT CONNECTED")
            else:
                cell_data_output.append(", Cell is CONNECTED")

            if(status_byte & 2 ==0):
                cell_data_output.append(", Data is INVALID")
            else:
                cell_data_output.append(", Cell is VALID")

            if(status_byte & 4 ==0):
                cell_data_output.append(", Cell is NOT BEING BALANCED")
            else:
                cell_data_output.append(", Cell is BEING BALACNED")
            if(status_byte & 1 ==0):
                cell_data_output.append(", temp sensor is CONNECTED")
            else:
                cell_data_output.append(", temp sensor is DISCONNECTED")

            cell_data_print = ("Time: " + str(fault_codes_list_baby[0]) + ", Cell_data - Cell Number:" + str(fault_codes_list_baby[1])+ "Cell Status: " + str(status_byte) + ", Voltage H: "+str(fault_codes_list_baby[3]) + ", Voltage L: "+str(fault_codes_list_baby[4]) + ", Temp H: "+str(fault_codes_list_baby[5]) + ", Temp L: "+str(fault_codes_list_baby[6]))
            print(cell_data_print)
            log.write(cell_data_print)
            log.close()

        elif (split_msg[0] == "008") or (split_msg[0] == "8"):
            log = open('CAN_log_%s.txt'%filestamp,'a')
            bms_data_list_baby = []
            bms_data_output = []
            bms_data_list_baby.append(time)
            bms_data_list_baby.append(int(split_msg[1], 16))
            bms_data_list_baby.append(int(split_msg[2], 16))
            bms_data_list_baby.append(int(split_msg[3], 16))
            bms_data_list_baby.append(int(split_msg[4], 16))
            bms_data_list_baby.append(int(split_msg[5], 16))
            bms_data_list_baby.append(int(split_msg[6], 16))
            #bms_data_list.append(bms_data_list_baby)

            status_byte = bms_data_list_baby[2]

            if(status_byte & 1 ==0):
                bms_data_output.append(", There is no OV fault")
            else:
                bms_data_output.append(", OV FAULT")

            if(status_byte & 2 ==0):
                bms_data_output.append(", There is no UV fault")
            else:
                bms_data_output.append(", UV FAULT")

            if(status_byte & 4 ==0):
                bms_data_output.append(", There is no OT fault")
            else:
                bms_data_output.append(", OT FAULT")
            if(status_byte & 8 ==0):
                bms_data_output.append(", There is no disconnected cell fault")
            else:
                bms_data_output.append(", DISCONNECTED CELL FAULT")
            if(status_byte & 16 ==0):
                bms_data_output.append(", There is no disconnected temp sensor fault")
            else:
                bms_data_output.append(", DISCONNECTED TEMP SENSOR FAULT")
            

            bms_data_print = ("Time: " + str(bms_data_list_baby[0]) + ", bms_data - Status: " + bms_data_output + ",  OV Cell Num: "+str(bms_data_list_baby[2]) + ", UV Cell Num: "+str(bms_data_list_baby[3]) + ", OT Cell Num: "+str(bms_data_list_baby[4]) + ", Disconnected Voltage Cell Num: " +str(bms_data_list_baby[5])+ ", Disconnected Temp Cell Num: " +str(bms_data_list_baby[6]))
            print(bms_data_print)
            log.write(bms_data_print)
            log.close()

        elif (split_msg[0] == "009") or (split_msg[0] == "9"):
            log = open('CAN_log_%s.txt'%filestamp,'a')
            bms_Vin_list_baby = []
            bms_Vin_list_baby.append(time)
            bms_Vin_list_baby.append(int(split_msg[1], 16)/1000.)
            bms_Vin_list_baby.append(int(split_msg[2], 16)/1000.)
            bms_Vin_list_baby.append(int(split_msg[3], 16)/1000.)
            bms_Vin_list_baby.append(int(split_msg[4], 16)/1000.)
            bms_Vin_list_baby.append(int(split_msg[5], 16)/1000.)
            bms_Vin_list_baby.append(int(split_msg[6], 16)/1000.)
            bms_Vin_list_baby.append(int(split_msg[7], 16)/1000.)
            bms_Vin_list_baby.append(int(split_msg[8], 16)/1000.)
            #bms_Vin_list.append(bms_Vin_list_baby)
            bms_Vin_print = ("Time: " + str(bms_Vin_list_baby[0]) + ", bms_Vin_data - Voltage Max H: " + str(bms_Vin_list_baby[1]) + ", Voltage Max L: " + str(bms_Vin_list_baby[2]) + ", Cell Max Num: " + str(bms_Vin_list_baby[3]) + ", Voltage Min H: " + str(bms_Vin_list_baby[4]) + ", Voltage Min L: " + str(bms_Vin_list_baby[5]) + ", Cell Min Num " + str(bms_Vin_list_baby[6]) + ", Voltage Avg H: " + str(bms_Vin_list_baby[7]) + ", Voltage Avg L: " + str(bms_Vin_list_baby[8]))
            print(bms_Vin_print)
            log.write(bms_Vin_print)
            log.close()

        elif (split_msg[0] == "0A") or (split_msg[0] == "10"):
            log = open('CAN_log_%s.txt'%filestamp,'a')
            bms_Tin_list_baby = []
            bms_Tin_list_baby.append(time)
            bms_Tin_list_baby.append(int(split_msg[1], 16)/500.-20)
            bms_Tin_list_baby.append(int(split_msg[2], 16)/500.-20)
            bms_Tin_list_baby.append(int(split_msg[3], 16)/500.-20)
            bms_Tin_list_baby.append(int(split_msg[4], 16)/500.-20)
            bms_Tin_list_baby.append(int(split_msg[5], 16)/500.-20)
            bms_Tin_list_baby.append(int(split_msg[6], 16)/500.-20)
            bms_Tin_list_baby.append(int(split_msg[7], 16)/500.-20)
            bms_Tin_list_baby.append(int(split_msg[8], 16)/500.-20)
            #bms_Tin_list.append(bms_Tin_list_baby)
            bms_Tin_print = print("Time: " + str(bms_Tin_list_baby[0]) + ", bms_Tin_Data - Temp Max H: " + str(bms_Tin_list_baby[1]) + ", Temp Max L: " + str(bms_Tin_list_baby[2]) + ", Cell Max Num: " + str(bms_Tin_list_baby[3]) + ", Temp Min H: " + str(bms_Tin_list_baby[4]) + ", Temp Min L: " + str(bms_Tin_list_baby[5]) + ", Cell Min Num " + str(bms_Tin_list_baby[6]) + ", Temp Avg H: " + str(bms_Tin_list_baby[7]) + ", Temp Avg L: " + str(bms_Tin_list_baby[8]))
            #bms_Tin_print = "what the fuck"
            print(bms_Tin_print)
            log.write(bms_Tin_print)
            log.close()

        elif (split_msg[0] == "0B") or (split_msg[0] == "11"):
            log = open('CAN_log_%s.txt'%filestamp,'a')
            bms_packstat_baby = []
            bms_packstat_baby.append(time)
            bms_packstat_baby.append(int(split_msg[1], 16))
            bms_packstat_baby.append(int(split_msg[2], 16))
            bms_packstat_baby.append(int(split_msg[3], 16))
            bms_packstat_baby.append(int(split_msg[4], 16))
            #bms_packstatTin_list.append(bms_packstat_baby)
            bms_packstat_print = print("Time: " + str(bms_packstat_baby[0]) + ", Packstat - Pack Voltage H: " + str(bms_packstat_list_baby[1]) + ", Pack Voltage L: " + str(bms_packstat_baby[2]) + ", Pack Current H: " + str(bms_packstat_baby[3]) + ", Pack Current L: " + str(bms_packstat_baby[4]))
            #bms_packstat_print = "Even more what the fuck"
            print(bms_packstat_print)
            log.write(bms_packstat_print)
            log.close()


        elif split_msg[0] == bin(int("0D0",16))[2:]:
            log = open('CAN_log_%s.txt'%filestamp,'a')
            saftey_faults_list_baby = []
            saftey_faults_list_baby.append(time)
            saftey_faults_list_baby.append(int(split_msg[1],16))
            saftey_faults_list_baby.append(int(split_msg[2],16))
            saftey_faults_list_baby.append(int(split_msg[3],16))
            saftey_faults_list_baby.append(int(split_msg[4],16))
            #saftey_faults_list.append(saftey_faults_list_baby)
            output = []
            if(saftey_faults_list_baby[1] !=0):
                output.append("BMS: Fault Present ")
            else:
                output.append("BMS: no fault ")
            if(saftey_faults_list_baby[2] !=0):
                output.append("IMD: Fault Present ")
            else:
                output.append("IMD: no fault")
            if(saftey_faults_list_baby[3] !=0):
                output.append("BSPD: Fault Present ")
            else:
                output.append("BSPD: no fault")
            if(saftey_faults_list_baby[4] !=0):
                output.append("APPS: Fault Present ")
            else:
                output.append("APPS: no fault ")
            safety_faults_print = ("Time: "+str(saftey_faults_list_baby[0])+", Safety Faults - "+output)
            print(safety_faults_print)
            log.write(safety_faults_print)
            log.close()

        elif (split_msg[0] == "0D1") or (split_msg[0] == "209"):
            log = open('CAN_log_%s.txt'%filestamp,'a')
            saftey_precharge_list_baby = []
            saftey_precharge_list_baby.append(time)
            saftey_precharge_list_baby.append(int(split_msg[1],16))
            #saftey_precharge_list.append(saftey_precharge_list_baby)
            output = []
            if(saftey_precharge_list_baby[1] !=0):
                output.append("not charged")
            else:
                output.append("Charged")
            safety_precharge_print=("Time: "+str(saftey_precharge_list_baby[0])+", Precharge - " +output)
            print(safety_precharge_print)
            log.write(safety_precharge_print)
            log.close()

        elif (split_msg[0] == "0D2") or (split_msg[0] == "210"):
            log = open('CAN_log_%s.txt'%filestamp,'a')
            saftey_enable_list_baby = []
            saftey_enable_list_baby.append(time)
            saftey_enable_list_baby.append(int(split_msg[1],16))
            #saftey_enable_list.append(saftey_enable_list_baby)
            output = []
            if(saftey_enable_list_baby[1] !=0):
                output.append("not enabled")
            else:
                output.append("Enabled")
            safety_enable_print = ("Time: "+str(saftey_enable_list_baby[0])+", Enable - " +output)
            print(safety_enable_print)
            log.write(safety_enable_print)
            log.close()
