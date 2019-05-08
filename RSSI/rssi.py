#!/user/bin/env python
# encoding: utf-8
#@time      : 2019/4/28 14:10


import time
from ctypes import *
from ctypes.wintypes import *
from sys import exit
import re


def customresize(array, new_size):
    return (array._type_ * new_size).from_address(addressof(array))


wlanapi = windll.LoadLibrary('wlanapi.dll')

ERROR_SUCCESS = 0


class GUID(Structure):
    _fields_ = [
        ('Data1', c_ulong),
        ('Data2', c_ushort),
        ('Data3', c_ushort),
        ('Data4', c_ubyte * 8),
    ]


WLAN_INTERFACE_STATE = c_uint
(wlan_interface_state_not_ready,
 wlan_interface_state_connected,
 wlan_interface_state_ad_hoc_network_formed,
 wlan_interface_state_disconnecting,
 wlan_interface_state_disconnected,
 wlan_interface_state_associating,
 wlan_interface_state_discovering,
 wlan_interface_state_authenticating) = map(WLAN_INTERFACE_STATE, range(0, 8))


class WLAN_INTERFACE_INFO(Structure):
    _fields_ = [
        ("InterfaceGuid", GUID),
        ("strInterfaceDescription", c_wchar * 256),
        ("isState", WLAN_INTERFACE_STATE)
    ]


class WLAN_INTERFACE_INFO_LIST(Structure):
    _fields_ = [
        ("NumberOfItems", DWORD),
        ("Index", DWORD),
        ("InterfaceInfo", WLAN_INTERFACE_INFO * 1)
    ]


WLAN_MAX_PHY_TYPE_NUMBER = 0x8
DOT11_SSID_MAX_LENGTH = 32
WLAN_REASON_CODE = DWORD

DOT11_BSS_TYPE = c_uint
(dot11_BSS_type_infrastructure,
 dot11_BSS_type_independent,
 dot11_BSS_type_any) = map(DOT11_BSS_TYPE, range(1, 4))

DOT11_PHY_TYPE = c_uint
dot11_phy_type_unknown = 0
dot11_phy_type_any = 0
dot11_phy_type_fhss = 1
dot11_phy_type_dsss = 2
dot11_phy_type_irbaseband = 3
dot11_phy_type_ofdm = 4
dot11_phy_type_hrdsss = 5
dot11_phy_type_erp = 6
dot11_phy_type_ht = 7
dot11_phy_type_IHV_start = 0x80000000
dot11_phy_type_IHV_end = 0xffffffff

DOT11_AUTH_ALGORITHM = c_uint
DOT11_AUTH_ALGO_80211_OPEN = 1
DOT11_AUTH_ALGO_80211_SHARED_KEY = 2
DOT11_AUTH_ALGO_WPA = 3
DOT11_AUTH_ALGO_WPA_PSK = 4
DOT11_AUTH_ALGO_WPA_NONE = 5
DOT11_AUTH_ALGO_RSNA = 6
DOT11_AUTH_ALGO_RSNA_PSK = 7
DOT11_AUTH_ALGO_IHV_START = 0x80000000
DOT11_AUTH_ALGO_IHV_END = 0xffffffff

DOT11_CIPHER_ALGORITHM = c_uint
DOT11_CIPHER_ALGO_NONE = 0x00
DOT11_CIPHER_ALGO_WEP40 = 0x01
DOT11_CIPHER_ALGO_TKIP = 0x02
DOT11_CIPHER_ALGO_CCMP = 0x04
DOT11_CIPHER_ALGO_WEP104 = 0x05
DOT11_CIPHER_ALGO_WPA_USE_GROUP = 0x100
DOT11_CIPHER_ALGO_RSN_USE_GROUP = 0x100
DOT11_CIPHER_ALGO_WEP = 0x101
DOT11_CIPHER_ALGO_IHV_START = 0x80000000
DOT11_CIPHER_ALGO_IHV_END = 0xffffffff

WLAN_AVAILABLE_NETWORK_CONNECTED = 1
WLAN_AVAILABLE_NETWORK_HAS_PROFILE = 2

WLAN_AVAILABLE_NETWORK_INCLUDE_ALL_ADHOC_PROFILES = 0x00000001
WLAN_AVAILABLE_NETWORK_INCLUDE_ALL_MANUAL_HIDDEN_PROFILES = 0x00000002


class DOT11_SSID(Structure):
    _fields_ = [
        ("SSIDLength", c_ulong),
        ("SSID", c_char * DOT11_SSID_MAX_LENGTH)
    ]


class WLAN_AVAILABLE_NETWORK(Structure):
    _fields_ = [
        ("ProfileName", c_wchar * 256),
        ("dot11Ssid", DOT11_SSID),
        ("dot11BssType", DOT11_BSS_TYPE),
        ("NumberOfBssids", c_ulong),
        ("NetworkConnectable", c_bool),
        ("wlanNotConnectableReason", WLAN_REASON_CODE),
        ("NumberOfPhyTypes", c_ulong),
        ("dot11PhyTypes", DOT11_PHY_TYPE * WLAN_MAX_PHY_TYPE_NUMBER),
        ("MorePhyTypes", c_bool),
        ("wlanSignalQuality", c_ulong),
        ("SecurityEnabled", c_bool),
        ("dot11DefaultAuthAlgorithm", DOT11_AUTH_ALGORITHM),
        ("dot11DefaultCipherAlgorithm", DOT11_CIPHER_ALGORITHM),
        ("Flags", DWORD),
        ("Reserved", DWORD)
    ]


class WLAN_AVAILABLE_NETWORK_LIST(Structure):
    _fields_ = [
        ("NumberOfItems", DWORD),
        ("Index", DWORD),
        ("Network", WLAN_AVAILABLE_NETWORK * 1)
    ]


DOT11_MAC_ADDRESS = c_ubyte * 6

DOT11_CIPHER_ALGORITHM = c_uint
DOT11_CIPHER_ALGO_NONE = 0x00
DOT11_CIPHER_ALGO_WEP40 = 0x01
DOT11_CIPHER_ALGO_TKIP = 0x02

DOT11_PHY_TYPE = c_uint
DOT11_PHY_TYPE_UNKNOWN = 0
DOT11_PHY_TYPE_ANY = 0
DOT11_PHY_TYPE_FHSS = 1
DOT11_PHY_TYPE_DSSS = 2
DOT11_PHY_TYPE_IRBASEBAND = 3
DOT11_PHY_TYPE_OFDM = 4
DOT11_PHY_TYPE_HRDSSS = 5
DOT11_PHY_TYPE_ERP = 6
DOT11_PHY_TYPE_HT = 7
DOT11_PHY_TYPE_IHV_START = 0X80000000
DOT11_PHY_TYPE_IHV_END = 0XFFFFFFFF


class WLAN_RATE_SET(Structure):
    _fields_ = [
        ("uRateSetLength", c_ulong),
        ("usRateSet", c_ushort * 126)
    ]


class WLAN_BSS_ENTRY(Structure):
    _fields_ = [
        ("dot11Ssid", DOT11_SSID),
        ("uPhyId", c_ulong),
        ("dot11Bssid", DOT11_MAC_ADDRESS),
        ("dot11BssType", DOT11_BSS_TYPE),
        ("dot11BssPhyType", DOT11_PHY_TYPE),
        ("lRssi", c_long),
        ("uLinkQuality", c_ulong),
        ("bInRegDomain", c_bool),
        ("usBeaconPeriod", c_ushort),
        ("ullTimestamp", c_ulonglong),
        ("ullHostTimestamp", c_ulonglong),
        ("usCapabilityInformation", c_ushort),
        ("ulChCenterFrequency", c_ulong),
        ("wlanRateSet", WLAN_RATE_SET),
        ("ulIeOffset", c_ulong),
        ("ulIeSize", c_ulong)]


class WLAN_BSS_LIST(Structure):
    _fields_ = [
        ("TotalSize", DWORD),
        ("NumberOfItems", DWORD),
        ("NetworkBSS", WLAN_BSS_ENTRY * 1)
    ]


class WLAN_AVAILABLE_NETWORK_LIST_BSS(Structure):
    _fields_ = [
        ("TotalSize", DWORD),
        ("NumberOfItems", DWORD),
        ("Network", WLAN_BSS_ENTRY * 1)
    ]


WlanOpenHandle = wlanapi.WlanOpenHandle
WlanOpenHandle.argtypes = (DWORD, c_void_p, POINTER(DWORD), POINTER(HANDLE))
WlanOpenHandle.restype = DWORD

WlanCloseHandle = wlanapi.WlanCloseHandle
WlanCloseHandle.argtypes = (HANDLE, c_void_p)
WlanCloseHandle.restype = DWORD

WlanEnumInterfaces = wlanapi.WlanEnumInterfaces
WlanEnumInterfaces.argtypes = (HANDLE, c_void_p,
                               POINTER(POINTER(WLAN_INTERFACE_INFO_LIST)))
WlanEnumInterfaces.restype = DWORD

WlanGetAvailableNetworkList = wlanapi.WlanGetAvailableNetworkList
WlanGetAvailableNetworkList.argtypes = (HANDLE, POINTER(GUID), DWORD, c_void_p,
                                        POINTER(POINTER(WLAN_AVAILABLE_NETWORK_LIST)))
WlanGetAvailableNetworkList.restype = DWORD

WlanGetNetworkBssList = wlanapi.WlanGetNetworkBssList
WlanGetNetworkBssList.argtypes = (HANDLE, POINTER(GUID), POINTER(GUID), POINTER(GUID), c_bool, c_void_p,
                                  POINTER(POINTER(WLAN_BSS_LIST)))
WlanGetNetworkBssList.restype = DWORD

WlanFreeMemory = wlanapi.WlanFreeMemory
WlanFreeMemory.argtypes = [c_void_p]

WlanScan = wlanapi.WlanScan
WlanScan.argtypes = (HANDLE, POINTER(GUID), c_void_p, c_void_p, c_void_p)
WlanScan.restype = DWORD


def get_interface():
    NegotiatedVersion = DWORD()
    ClientHandle = HANDLE()
    ret = WlanOpenHandle(1, None, byref(NegotiatedVersion), byref(ClientHandle))
    if ret != ERROR_SUCCESS:
        exit(FormatError(ret))
        # find all wireless network interfaces
    pInterfaceList = pointer(WLAN_INTERFACE_INFO_LIST())
    ret = WlanEnumInterfaces(ClientHandle, None, byref(pInterfaceList))
    if ret != ERROR_SUCCESS:
        exit(FormatError(ret))
    try:
        ifaces = customresize(pInterfaceList.contents.InterfaceInfo,
                              pInterfaceList.contents.NumberOfItems)
        # find each available network for each interface
        for iface in ifaces:
            #print("Interface: %s" % (iface.strInterfaceDescription))
            interface = iface.strInterfaceDescription

    finally:
        WlanFreeMemory(pInterfaceList)
    print(interface)
    return interface


class MAC_BSSID_POWER:
    """Classe para os valores retirados"""

    def __init__(self, mac, bssid):
        self.mac = str(mac)
        self.bssid = str(bssid)
        self.valores = []

    def addPower(self, power):
        self.valores.append(int(power))

    def getBssid(self):
        return self.bssid

    def getPowers(self):
        return self.valores

    def getMac(self):
        return self.mac


def get_BSSI():
    BSSI_Values = {}
    RATE_Values = {}

    NegotiatedVersion = DWORD()
    ClientHandle = HANDLE()
    ret = WlanOpenHandle(1, None, byref(NegotiatedVersion), byref(ClientHandle))
    if ret != ERROR_SUCCESS:
        exit(FormatError(ret))
        # find all wireless network interfaces
    pInterfaceList = pointer(WLAN_INTERFACE_INFO_LIST())
    ret = WlanEnumInterfaces(ClientHandle, None, byref(pInterfaceList))
    if ret != ERROR_SUCCESS:
        exit(FormatError(ret))
    try:
        ifaces = customresize(pInterfaceList.contents.InterfaceInfo,
                              pInterfaceList.contents.NumberOfItems)
        # find each available network for each interface
        for iface in ifaces:
            print("Interface: %s" % (iface.strInterfaceDescription))

            pAvailableNetworkList2 = pointer(WLAN_BSS_LIST())

            ret2 = WlanGetNetworkBssList(ClientHandle,
                                         byref(iface.InterfaceGuid),
                                         None,
                                         None, True, None,
                                         byref(pAvailableNetworkList2))
        if ret2 != ERROR_SUCCESS:
            exit(FormatError(ret2))
        try:
            retScan = WlanScan(ClientHandle, byref(iface.InterfaceGuid), None, None, None)
            if retScan != ERROR_SUCCESS:
                exit(FormatError(retScan))
            avail_net_list2 = pAvailableNetworkList2.contents
            networks2 = customresize(avail_net_list2.NetworkBSS,
                                     avail_net_list2.NumberOfItems)

            for network in networks2:
                SSID = str(network.dot11Ssid.SSID[:network.dot11Ssid.SSIDLength])
                BSSID = ':'.join('%02x' % b for b in network.dot11Bssid).upper()
                signal_strength = str(network.lRssi)
                link_rate = str(network.ulIeSize)
                #print(xxx)
                #print("SSID: " + SSID + " BSSID: " + BSSID + " RSSI: "+signal_strength + ' LINK_RATE:' + link_rate)

                BSSI_Values[BSSID] = [SSID, signal_strength, link_rate]

                # print "Total "+str(len(networks2))
                # print BSSI_Values

        finally:
            WlanFreeMemory(pAvailableNetworkList2)
            WlanCloseHandle(ClientHandle, None)
    finally:
        WlanFreeMemory(pInterfaceList)
    #print('XXX', BSSI_Values)
    return BSSI_Values


def get_BSSI_times_and_total_seconds(times, seconds):
    BSSI_to_return = {}

    for i in range(0, seconds * times):
        time_to_sleep = float(1.0 / times)
        time.sleep(time_to_sleep)
        got_bssi_temp = get_BSSI()

        for bssi in got_bssi_temp:
            if not BSSI_to_return.get(bssi):
                BSSI_to_return[bssi] = MAC_BSSID_POWER(bssi, got_bssi_temp[bssi][0])
                BSSI_to_return[bssi].addPower(got_bssi_temp[bssi][1])

                # BSSI_to_return[bssi] = [got_bssi_temp[bssi][1]]

            else:
                BSSI_to_return[bssi].addPower(got_bssi_temp[bssi][1])
                # BSSI_to_return[bssi].append(got_bssi_temp[bssi][1])
        print("Medicao " + str(i) + " de " + str(seconds * times))
    print(BSSI_to_return)
    return BSSI_to_return


def get_RSSI(ssid_require):
    rssi_value = None
    test = get_BSSI()
    for i in range(1, 2):
        time.sleep(0.5)
        oldTest = test
        test = get_BSSI()
        print("GET TIMES: " + str(i))
        if oldTest == test:
            print("SAME")
        else:
            print("DIFFERENT")
        for item in test.items():
            # print(item)
            # print(item[1])
            ssids = re.sub('b\'', '', item[1][0])
            ssids = re.sub('\'', '', ssids)
            # print(ssids)
            ssid_get = ssid_require
            if ssids == ssid_get:
                print('SSID', ssids, 'RSSI', item[1][1])
                rssi_value = item[1][1]
                link_rate_value = item[1][2]
            #print('xxx', rssi_value, link_rate_value)
    return rssi_value, link_rate_value

if __name__ == '__main__':
    ssid_file = 'ssid.txt'
    with open(ssid_file, 'r') as f:
        ssid_require = f.readline().strip()
        print(ssid_require)
    # print get_interface()
    #test = get_BSSI()
    rssi_value_list = []
    link_rate_value_list = []
    for i in range(0, 10):
        time.sleep(0.5)
        #oldTest = test
        test = get_BSSI()
        print("Test: " + str(i))
        #if oldTest == test:
        #    print("IGUAL")
        #else:
        #    print("DIFERENTE")
        for item in test.items():
            #print('111', item)
            #print('222', item[1])
            ssids = re.sub('b\'', '', item[1][0])
            ssids = re.sub('\'', '', ssids)
            #print('333', ssids)
            ssid_get = ssid_require
            if ssids == ssid_get:
                rssi_value = item[1][1]
                link_rate_value = item[1][2]
                print('SSID', ssids, 'RSSI', rssi_value, 'RATE', link_rate_value)
                rssi_value_list.append(rssi_value)
                link_rate_value_list.append(link_rate_value)
    print(rssi_value_list)
    print(link_rate_value_list)
    #RSSI_sum = 0
    #RSSI_length = len(rssi_value_list)
    #RATE_sum = 0
    #RATE_length = len(link_rate_value_list)
    #for i in rssi_value_list:
    #    RSSI_sum = RSSI_sum + int(i)
    #RSSI_AVG = RSSI_sum/RATE_length
    #for x in link_rate_value_list:
    #    RATE_sum = RATE_sum + int(x)
    #RATE_AVG = RATE_sum/RATE_length
    RSSI_AVG = max(set(rssi_value_list), key=rssi_value_list.count)
    RATE_AVG = max(set(link_rate_value_list), key=link_rate_value_list.count)
    print('SSID', ssid_get, 'RSSI', RSSI_AVG, 'RATE', RATE_AVG)
    file = 'result.txt'
    result = open(file, 'w')
    result.write(str(RSSI_AVG)+'\r\n')
    result.write(str(RATE_AVG))
    result.close()
