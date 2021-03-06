#!/user/bin/env python
# encoding: utf-8
# @time      : 2019/5/6 13:38
"""get RSSI through product
2019.8.8 拆分各个查询，便于并行设计"""
__author__ = 'Ethan'

from time import sleep
import telnetlib
import paramiko
import serial
import re
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # logger的总开关，只有大于Debug的日志才能被logger对象处理

# 第二步，创建一个handler，用于写入日志文件
file_handler = logging.FileHandler('./log/log.txt', mode='w')
file_handler.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
# 创建该handler的formatter
file_handler.setFormatter(
    logging.Formatter(
        fmt='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
)
# 添加handler到logger中
logger.addHandler(file_handler)

# 第三步，创建一个handler，用于输出到控制台
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # 输出到控制台的log等级的开关
# 创建该handler的formatter
console_handler.setFormatter(
    logging.Formatter(
        fmt='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
)
logger.addHandler(console_handler)


class product_RSSI_telnet:
    def __init__(self, ip, username, password, radio, ap_type):
        self.tn = telnetlib.Telnet(ip, port=23, timeout=5)
        self.tn.set_debuglevel(1)
        self.username = username
        self.password = password
        self.radio = radio
        self.ap_type = ap_type
        self.tn.timeout = 0.5

    def login(self, username, password):
        if username:
            self.tn.read_until(b'Login:')
            self.tn.write(username.encode('ascii') + b'\r\n')
            if password:
                self.tn.read_until(b'Password:')
                self.tn.write(password.encode('ascii') + b'\r\n')
            else:
                logger.info('No password')
            self.tn.read_until(b'>')
            self.tn.write(b'su\r\n')
            self.tn.write(b'shell\r\n')
        else:
            logger.info('No user')

    def qca_reset(self):
        self.tn.write(b'wifistats wifi0 wifiX 9\r\n')
        self.tn.write(b'wifistats wifi0 wifiX 10\r\n')
        self.tn.write(b'wifistats wifi1 wifiX 9\r\n')
        self.tn.write(b'wifistats wifi1 wifiX 10\r\n')
        self.tn.write(b'iwpriv ath0 txrx_fw_stats 0xff\r\n')
        self.tn.write(b'iwpriv ath1 txrx_fw_stats 0xff\r\n')
        sleep(2)

    def get_testradio_qca(self):
        test_radio = 'ath0'
        self.tn.write(b'\r\n')
        self.tn.read_until(b'root@OpenWrt:/# ')
        self.tn.write(b'iwconfig ath0\r\n')
        command_result = self.tn.read_until(b'root@OpenWrt:/#  ', timeout=2)
        logger.debug(command_result)
        ath_result = re.findall(b'ath0\r\nath0(.+)', command_result)
        logger.debug(ath_result[0].split())
        ath_result = ath_result[0].split()[0]
        if ath_result.decode('utf-8') == 'No':
            self.tn.write(b'iwconfig ath1\r\n')
            command_result = self.tn.read_until(b'No', timeout=2)
            logger.debug(command_result)
            ath_result = re.findall(b'ath1(.+)', command_result)[1].split()[0]
            logger.debug(ath_result)
            if ath_result.decode('utf-8') == 'No':
                logger.error('No such device')
                test_radio = None
            else:
                frequency = re.findall(b'Frequency:(\d+\.\d+) GHz', command_result)[0].decode('utf-8')
                logger.debug(frequency)
                power = re.findall(b'(Tx-Power:\d+ dBm)', command_result)[0].decode('utf-8')
                logger.debug(power)
                if float(frequency) < 5.0:
                    radio_2g = '1'
                    radio_5g = '0'
                else:
                    radio_2g = '0'
                    radio_5g = '1'
        else:
            frequency = re.findall(b'Frequency:(\d+\.\d+) GHz', command_result)[0].decode('utf-8')
            logger.debug(frequency)
            power = re.findall(b'(Tx-Power:\d+ dBm)', command_result)[0].decode('utf-8')
            logger.debug(power)
            if float(frequency) < 5.0:
                radio_2g = '0'
                radio_5g = '1'
            else:
                radio_2g = '1'
                radio_5g = '0'
        logger.info(power)
        logger.info(radio_2g)
        logger.info(radio_5g)
        return power, radio_2g, radio_5g

    def get_APRSSI_qca(self, radio, radio_2g, radio_5g):
        get_txrate_list = []
        get_rxrate_list = []
        get_aprssi_list = []
        get_bw_list = []
        get_nsstx_list = []
        get_nssrx_list = []
        get_channel = TXRATE_AVG = RXRATE_AVG = APRSSI_AVG = TXNSS_AVG = RXNSS_AVG = None
        if radio == '2.4g':
            radio_value = radio_2g
        elif radio == '5g':
            radio_value = radio_5g
        else:
            logger.error('Radio type is wrong')
            radio_value = None
        for i in range(10):
            self.tn.write(b'\r\n')
            logger.info('Test Radio is ' + radio + ' ath' + radio_value)
            self.tn.write(b'wlanconfig ath%s list\r\n' % radio_value.encode('ascii'))
            command_result = self.tn.read_until(b'root@OpenWrt:/#  ', timeout=2)
            logger.debug(command_result)
            type_result = re.findall(b'list\r\n(.+)', command_result)[0].split()
            logger.debug(type_result)
            client_type = type_result[0].decode('utf-8')
            logger.debug(client_type)
            if client_type == 'Error':
                logger.info('Raido is not opened')
            else:
                basic_info = re.findall(b'PSMODE\r\n(.+)', command_result)[0].split()
                logger.debug(basic_info)
                self.tn.write(b'\r\n')
                if basic_info[0].decode('utf-8') == 'root@OpenWrt:/#':
                    logger.info('No client')
                    break
                else:
                    get_channel = basic_info[2].decode('utf-8')
                    get_txrate = re.sub('M', '', basic_info[3].decode('utf-8'))
                    get_txrate_list.append(get_txrate)
                    get_rxrate = re.sub('M', '', basic_info[4].decode('utf-8'))
                    get_rxrate_list.append(get_rxrate)
                    get_aprssi = basic_info[5].decode('utf-8')
                    get_aprssi_list.append(get_aprssi)
                    # get_bw = basic_info[20].decode('utf-8')
                    # get_bw_list.append(get_bw)
                    get_nsstx = basic_info[-2].decode('utf-8')
                    get_nsstx_list.append(get_nsstx)
                    get_nssrx = basic_info[-3].decode('utf-8')
                    get_nssrx_list.append(get_nssrx)

                logger.debug(get_channel)
                logger.debug(get_txrate_list)
                logger.debug(get_rxrate_list)
                logger.debug(get_aprssi_list)
                logger.debug(get_nsstx_list)
                logger.debug(get_nssrx_list)
                TXRATE_AVG = max(set(get_txrate_list), key=get_txrate_list.count)
                RXRATE_AVG = max(set(get_rxrate_list), key=get_rxrate_list.count)
                APRSSI_AVG = max(set(get_aprssi_list), key=get_aprssi_list.count)
                # RXBW_AVG = max(set(get_bw_list), key=get_bw_list.count)
                TXNSS_AVG = max(set(get_nsstx_list), key=get_nsstx_list.count)
                RXNSS_AVG = max(set(get_nssrx_list), key=get_nssrx_list.count)
        logger.info('AP:')
        logger.info('Channel:')
        logger.info(get_channel)
        logger.info('TXRATE:')
        logger.info(TXRATE_AVG)
        logger.info('RXRATE:')
        logger.info(RXRATE_AVG)
        logger.info('APRSSI:')
        logger.info(APRSSI_AVG)
        # logger.info('RXBW:')
        # logger.info(RXBW_AVG)
        logger.info('TXNSS:')
        logger.info(TXNSS_AVG)
        logger.info('RXNSS:')
        logger.info(RXNSS_AVG)
        # return get_channel, TXRATE_AVG, RXRATE_AVG, APRSSI_AVG, RXBW_AVG, TXNSS_AVG, RXNSS_AVG
        return get_channel, TXRATE_AVG, RXRATE_AVG, APRSSI_AVG, TXNSS_AVG, RXNSS_AVG

    def get_txcounts_qca(self, radio, radio_2g, radio_5g):
        if radio == '2.4g':
            radio_value = radio_2g
        elif radio == '5g':
            radio_value = radio_5g
        else:
            logger.error('Radio type is wrong')
            radio_value = None

        # # tx info 9
        self.tn.write(b'wifistats wifi%s 9\r\n' % radio_value.encode('ascii'))
        tx_result = self.tn.read_until(b'11ax_trigger_type', timeout=2)
        # legacy_cck_rates = re.findall(b'(Legacy CCK Rates:.+)', tx_result)[0].decode('utf-8')
        # logger.debug(legacy_cck_rates)
        # legacy_ofdm_rates = re.findall(b'(Legacy OFDM Rates:.+)', tx_result)[0].decode('utf-8')
        # logger.debug(legacy_ofdm_rates)
        tx_mcs = re.findall(b'(tx_mcs =.+)', tx_result)[0].decode('utf-8')
        logger.debug(tx_mcs)
        # acmumimo_tx_mcs = re.findall(b'(ac_mu_mimo_tx_mcs =.+)', tx_result)[0].decode('utf-8')
        # logger.debug(acmumimo_tx_mcs)
        # axmumimo_tx_mcs = re.findall(b'(ax_mu_mimo_tx_mcs =.+)', tx_result)[0].decode('utf-8')
        # logger.debug(axmumimo_tx_mcs)
        # ofdma_tx_mcs = re.findall(b'(ofdma_tx_mcs =.+)', tx_result)[0].decode('utf-8')
        # logger.debug(ofdma_tx_mcs)
        tx_nss = re.findall(b'(tx_nss =.+)', tx_result)[0].decode('utf-8')
        logger.debug(tx_nss)
        # acmumimo_tx_nss = re.findall(b'(ac_mu_mimo_tx_nss =.+)', tx_result)[0].decode('utf-8')
        # logger.debug(acmumimo_tx_nss)
        # axmumimo_tx_nss = re.findall(b'(ax_mu_mimo_tx_nss =.+)', tx_result)[0].decode('utf-8')
        # logger.debug(axmumimo_tx_nss)
        # ofdma_tx_nss = re.findall(b'(ofdma_tx_nss =.+)', tx_result)[0].decode('utf-8')
        # logger.debug(ofdma_tx_nss)
        tx_bw = re.findall(b'(tx_bw =.+)', tx_result)[0].decode('utf-8')
        logger.debug(tx_bw)
        # acmumimo_tx_bw = re.findall(b'(ac_mu_mimo_tx_bw =.+)', tx_result)[0].decode('utf-8')
        # logger.debug(acmumimo_tx_bw)
        # axmumimo_tx_bw = re.findall(b'(ax_mu_mimo_tx_bw =.+)', tx_result)[0].decode('utf-8')
        # logger.debug(axmumimo_tx_bw)
        # ofdma_tx_bw = re.findall(b'(ofdma_tx_bw =.+)', tx_result)[0].decode('utf-8')
        # logger.debug(ofdma_tx_bw)
        # tx_stbc = re.findall(b'(tx_stbc =.+)', tx_result)[0].decode('utf-8')
        # logger.debug(tx_stbc)
        # tx_pream = re.findall(b'(tx_pream =.+)', tx_result)[0].decode('utf-8')
        # logger.debug(tx_pream)
        return tx_mcs, tx_nss, tx_bw

    def get_rxcounts_qca(self, radio, radio_2g, radio_5g):
        if radio == '2.4g':
            radio_value = radio_2g
        elif radio == '5g':
            radio_value = radio_5g
        else:
            logger.error('Radio type is wrong')
            radio_value = None
        get_rssi_list = []
        get_rssi0_list = []
        get_rssi1_list = []
        get_rssi2_list = []
        get_rssi3_list = []
        get_rssi4_list = []
        get_rssi5_list = []
        get_rssi6_list = []
        get_rssi7_list = []
        # # rx info 10
        for i in range(10):
            self.tn.write(b'wifistats wifi%s 10\r\n' % radio_value.encode('ascii'))
            rx_result = self.tn.read_until(b'per_chain_rssi_pkt_type', timeout=2)
            logger.debug(rx_result)
            get_rssi = re.findall(b'rssi_in_dbm =(.+)', rx_result)[0].decode('utf-8')
            logger.debug(get_rssi)
            get_rssi_list.append(get_rssi)
            rx_mcs = re.findall(b'rx_mcs =(.+)', rx_result)[0].decode('utf-8')
            logger.debug(rx_mcs)
            rx_nss = re.findall(b'rx_nss =(.+)', rx_result)[0].decode('utf-8')
            logger.debug(rx_nss)
            # rx_dcm = re.findall(b'rx_dcm =(.+)', rx_result)[0].decode('utf-8')
            # logger.debug(rx_dcm)
            # rx_stbc = re.findall(b'rx_stbc =(.+)', rx_result)[0].decode('utf-8')
            # logger.debug(rx_stbc)
            rx_bw = re.findall(b'rx_bw =(.+)', rx_result)[0].decode('utf-8')
            logger.debug(rx_bw)
            rssi_chain0 = re.findall(b'rssi_chain\[0] =  0:(\d+)', rx_result)[0].decode('utf-8')
            logger.debug(rssi_chain0)
            get_rssi0_list.append(rssi_chain0)
            rssi_chain1 = re.findall(b'rssi_chain\[1] =  0:(\d+)', rx_result)[0].decode('utf-8')
            logger.debug(rssi_chain1)
            get_rssi1_list.append(rssi_chain1)
            rssi_chain2 = re.findall(b'rssi_chain\[2] =  0:(\d+)', rx_result)[0].decode('utf-8')
            logger.debug(rssi_chain2)
            get_rssi2_list.append(rssi_chain2)
            rssi_chain3 = re.findall(b'rssi_chain\[3] =  0:(\d+)', rx_result)[0].decode('utf-8')
            logger.debug(rssi_chain3)
            get_rssi3_list.append(rssi_chain3)
            rssi_chain4 = re.findall(b'rssi_chain\[4] =  0:(\d+)', rx_result)[0].decode('utf-8')
            logger.debug(rssi_chain4)
            get_rssi4_list.append(rssi_chain4)
            rssi_chain5 = re.findall(b'rssi_chain\[5] =  0:(\d+)', rx_result)[0].decode('utf-8')
            logger.debug(rssi_chain5)
            get_rssi5_list.append(rssi_chain5)
            rssi_chain6 = re.findall(b'rssi_chain\[6] =  0:(\d+)', rx_result)[0].decode('utf-8')
            logger.debug(rssi_chain6)
            get_rssi6_list.append(rssi_chain6)
            rssi_chain7 = re.findall(b'rssi_chain\[7] =  0:(\d+)', rx_result)[0].decode('utf-8')
            logger.debug(rssi_chain7)
            get_rssi7_list.append(rssi_chain7)
            # rx_pream = re.findall(b'rx_(pream =.+)', rx_result)[0].decode('utf-8')
            # logger.debug(rx_pream)
            # rx_legacycck_rate = re.findall(b'rx_(legacy_cck_rate =.+)', rx_result)[0].decode('utf-8')
            # logger.debug(rx_legacycck_rate)
            # rx_legacyofdm_rate = re.findall(b'rx_(legacy_ofdm_rate =.+)', rx_result)[0].decode('utf-8')
            # logger.debug(rx_legacyofdm_rate)
            # ulofdma_rx_mcs = re.findall(b'(ul_ofdma_rx_mcs =.+)', rx_result)[0].decode('utf-8')
            # logger.debug(ulofdma_rx_mcs)
            # ulofdma_rx_nss = re.findall(b'(ul_ofdma_rx_nss =.+)', rx_result)[0].decode('utf-8')
            # logger.debug(ulofdma_rx_nss)
            # ulofdma_rx_bw = re.findall(b'(ul_ofdma_rx_bw =.+)', rx_result)[0].decode('utf-8')
            # logger.debug(ulofdma_rx_bw)
            logger.debug(get_rssi_list)
            logger.debug(get_rssi0_list)
            logger.debug(get_rssi1_list)
            logger.debug(get_rssi2_list)
            logger.debug(get_rssi3_list)
            logger.debug(get_rssi4_list)
            logger.debug(get_rssi5_list)
            logger.debug(get_rssi6_list)
            logger.debug(get_rssi7_list)
        RSSI_AVG = max(set(get_rssi_list), key=get_rssi_list.count)
        RSSI0_AVG = max(set(get_rssi0_list), key=get_rssi0_list.count)
        RSSI1_AVG = max(set(get_rssi1_list), key=get_rssi1_list.count)
        RSSI2_AVG = max(set(get_rssi2_list), key=get_rssi2_list.count)
        RSSI3_AVG = max(set(get_rssi3_list), key=get_rssi3_list.count)
        RSSI4_AVG = max(set(get_rssi4_list), key=get_rssi4_list.count)
        RSSI5_AVG = max(set(get_rssi5_list), key=get_rssi5_list.count)
        RSSI6_AVG = max(set(get_rssi6_list), key=get_rssi6_list.count)
        RSSI7_AVG = max(set(get_rssi7_list), key=get_rssi7_list.count)
        logger.info('RSSI:')
        logger.info(RSSI_AVG)
        logger.info(RSSI0_AVG+','+RSSI1_AVG+','+RSSI2_AVG+','+RSSI3_AVG+','+RSSI4_AVG+','+RSSI5_AVG+','+RSSI6_AVG+','
                    +RSSI7_AVG)
        return RSSI_AVG, rx_mcs, rx_nss, rx_bw, RSSI0_AVG, RSSI1_AVG, RSSI2_AVG, RSSI3_AVG, RSSI4_AVG, RSSI5_AVG,\
               RSSI6_AVG, RSSI7_AVG

    def get_RSSI_bcm(self, radio):
        if radio == '2.4g':
            test_radio = 'wl0'
        elif radio == '5g_H':
            test_radio = 'wl2'
        else:
            test_radio = 'wl1'
        get_rssi_list = []
        get_ant0rssi_list = []
        get_ant1rssi_list = []
        get_ant2rssi_list = []
        get_ant3rssi_list = []
        RSSI_AVG = RSSI_ANT0_AVG = RSSI_ANT1_AVG = RSSI_ANT2_AVG = RSSI_ANT3_AVG = None
        for i in range(10):
            self.tn.write(b'sh\r\n')
            self.tn.write(b'\r\n')
            self.tn.read_until(b'# ')
            self.tn.write(b'wl -i %s dump rssi\r\n' % test_radio.encode('ascii'))
            rssi_result = self.tn.read_until(b'#  ', timeout=2)
            logger.debug(rssi_result)
            rssi_result_len = len(rssi_result)
            logger.debug(rssi_result_len)
            if rssi_result_len < 150:
                get_rssi = get_ant0_rssi = get_ant1_rssi = get_ant2_rssi = get_ant3_rssi = None
            else:
                get_rssi = re.findall(b'RSSI(.+)', rssi_result)[0].split()[-1].decode('utf-8')
                get_rssi_list.append(get_rssi)
                logger.debug(get_rssi)
                logger.debug(get_rssi_list)
                get_ant0_rssi = re.findall(b'ANT0(.+)', rssi_result)[1].split()[-1].decode('utf-8')
                get_ant0rssi_list.append(get_ant0_rssi)
                logger.debug(get_ant0_rssi)
                logger.debug(get_ant0rssi_list)
                get_ant1_rssi = re.findall(b'ANT1(.+)', rssi_result)[1].split()[-1].decode('utf-8')
                get_ant1rssi_list.append(get_ant1_rssi)
                logger.debug(get_ant1_rssi)
                logger.debug(get_ant1rssi_list)
                get_ant2_rssi = re.findall(b'ANT2(.+)', rssi_result)[1].split()[-1].decode('utf-8')
                get_ant2rssi_list.append(get_ant2_rssi)
                logger.debug(get_ant2_rssi)
                logger.debug(get_ant2rssi_list)
                get_ant3_rssi = re.findall(b'ANT3(.+)', rssi_result)[1].split()[-1].decode('utf-8')
                get_ant3rssi_list.append(get_ant3_rssi)
                logger.debug(get_ant3_rssi)
                logger.debug(get_ant3rssi_list)
                sleep(1)

        RSSI_AVG = max(set(get_rssi_list), key=get_rssi_list.count)
        RSSI_ANT0_AVG = max(set(get_ant0rssi_list), key=get_ant0rssi_list.count)
        RSSI_ANT1_AVG = max(set(get_ant1rssi_list), key=get_ant1rssi_list.count)
        RSSI_ANT2_AVG = max(set(get_ant2rssi_list), key=get_ant2rssi_list.count)
        RSSI_ANT3_AVG = max(set(get_ant3rssi_list), key=get_ant3rssi_list.count)
        logger.info('RSSI:')
        logger.info(RSSI_AVG)
        logger.info('RSSI_ANT0:')
        logger.info(RSSI_ANT0_AVG)
        logger.info('RSSI_ANT1:')
        logger.info(RSSI_ANT1_AVG)
        logger.info('RSSI_ANT2:')
        logger.info(RSSI_ANT2_AVG)
        logger.info('RSSI_ANT3:')
        logger.info(RSSI_ANT3_AVG)
        logger.info('POWER_ANT0:')
        return RSSI_AVG, RSSI_ANT0_AVG, RSSI_ANT1_AVG, RSSI_ANT2_AVG, RSSI_ANT3_AVG

    def get_counts_bcm(self, radio):
        if radio == '2.4g':
            test_radio = 'wl0'
        elif radio == '5g_H':
            test_radio = 'wl2'
        else:
            test_radio = 'wl1'
        get_rate_list = []
        get_rssi_list = []
        get_mcs_list = []
        get_nss_list = []
        get_bw_list = []
        get_ant0rssi_list = []
        get_ant1rssi_list = []
        get_ant2rssi_list = []
        get_ant3rssi_list = []
        power_chain0_list = []
        power_chain1_list = []
        power_chain2_list = []
        power_chain3_list = []
        get_channel = get_mode = RATE_AVG = MCS_AVG = NSS_AVG = BW_AVG = POWER_ANT0_AVG = POWER_ANT1_AVG = \
            POWER_ANT2_AVG = POWER_ANT3_AVG = None
        i = 1
        for i in range(10):
            self.tn.write(b'sh\r\n')
            self.tn.write(b'\r\n')
            self.tn.read_until(b'# ')
            self.tn.write(b'wl -i %s status\r\n' % test_radio.encode('ascii'))
            command_result = self.tn.read_until(b'HT Capabilities:', timeout=2)
            logger.debug(command_result)
            channel_result = re.findall(b'Chanspec:(.+)', command_result)[0].split()
            logger.debug(channel_result)
            get_channel = channel_result[2].decode('utf-8')

            self.tn.write(b'\r\n')
            self.tn.read_until(b'# ')
            self.tn.write(b'wl -i %s rate\r\n' % test_radio.encode('ascii'))
            rate_result = self.tn.read_until(b' Mbps', timeout=5)
            logger.debug(rate_result)
            rate_result = re.findall(b'(.+) Mbps', rate_result)[0].split()
            logger.debug(rate_result)
            get_rate = rate_result[0].decode('utf-8')
            get_rate_list.append(get_rate)

            self.tn.write(b'\r\n')
            self.tn.read_until(b'# ')
            self.tn.write(b'wl -i %s nrate\r\n' % test_radio.encode('ascii'))
            nrate_result = self.tn.read_until(b'auto', timeout=2)
            logger.debug(nrate_result)
            nrate_result = re.findall(b'(.+)auto', nrate_result)[0].split()
            logger.debug(nrate_result)
            get_mode = nrate_result[0].decode('utf-8')
            get_mcs = nrate_result[2].decode('utf-8')
            get_mcs_list.append(get_mcs)
            get_nss = nrate_result[4].decode('utf-8')
            get_nss_list.append(get_nss)
            get_bw = nrate_result[8].decode('utf-8')
            get_bw_list.append(get_bw)

            self.tn.write(b'\r\n')
            self.tn.read_until(b'# ')
            self.tn.write(b'wl -i %s curpower | grep ower\r\n' % test_radio.encode('ascii'))
            power_result = self.tn.read_until(b'Last adjusted est. power', timeout=2)
            logger.debug(power_result)
            power_result_a = re.findall(b'PHY Maximum Power Target among all rates(.+)', power_result)[0]
            logger.debug('PHY Maximum Power Target among all rates' + str(power_result_a.decode('utf-8')))
            power_result_b = re.findall(b'PHY Power Target for the current rate(.+)', power_result)[0]
            logger.debug('PHY Power Target for the current rate' + str(power_result_b.decode('utf-8')))
            power_result_c = re.findall(b'Last est. power(.+)', power_result)[0]
            logger.debug('Last est. power' + str(power_result_c.decode('utf-8')))
            # power_result_d = re.findall(b'Last adjusted est. power(.+)', power_result)[0]
            # logger.info('Last adjusted est. power' + str(power_result_d.decode('utf-8')))
            # logger.info(power_result_d.split())
            power_chain0 = power_result_c.split()[1].decode('utf-8')
            power_chain0_list.append(power_chain0)
            power_chain1 = power_result_c.split()[2].decode('utf-8')
            power_chain1_list.append(power_chain1)
            power_chain2 = power_result_c.split()[3].decode('utf-8')
            power_chain2_list.append(power_chain2)
            power_chain3 = power_result_c.split()[4].decode('utf-8')
            power_chain3_list.append(power_chain3)
            sleep(1)

        RATE_AVG = max(set(get_rate_list), key=get_rate_list.count)
        MCS_AVG = max(set(get_mcs_list), key=get_mcs_list.count)
        MCS_AVG = str(get_mode) + MCS_AVG
        NSS_AVG = max(set(get_nss_list), key=get_nss_list.count)
        BW_AVG = max(set(get_bw_list), key=get_bw_list.count)
        POWER_ANT0_AVG = max(set(power_chain0_list), key=power_chain0_list.count)
        POWER_ANT1_AVG = max(set(power_chain1_list), key=power_chain1_list.count)
        POWER_ANT2_AVG = max(set(power_chain2_list), key=power_chain2_list.count)
        POWER_ANT3_AVG = max(set(power_chain3_list), key=power_chain3_list.count)
        logger.info('Info from AP:Channel:')
        logger.info(get_channel)
        logger.info('RATE:')
        logger.info(RATE_AVG)
        logger.info('MCS:')
        logger.info(MCS_AVG)
        logger.info('NSS:')
        logger.info(NSS_AVG)
        logger.info('BW:')
        logger.info(BW_AVG)
        logger.info('POWER_ANT0:')
        logger.info(POWER_ANT0_AVG)
        logger.info('POWER_ANT1:')
        logger.info(POWER_ANT1_AVG)
        logger.info('POWER_ANT2:')
        logger.info(POWER_ANT2_AVG)
        logger.info('POWER_ANT3:')
        logger.info(POWER_ANT3_AVG)
        # print(RXRSSI_AVG)
        return get_channel, RATE_AVG, MCS_AVG, NSS_AVG, BW_AVG, POWER_ANT0_AVG, POWER_ANT1_AVG, POWER_ANT2_AVG, \
               POWER_ANT3_AVG

    def get_testradio_mtk(self):
        test_radio = 'ra0'
        self.tn.write(b'\r\n')
        self.tn.read_until(b':/#', timeout=2)
        self.tn.write(b'iwconfig ra0\r\n')
        sleep(0.2)
        command_result = self.tn.read_very_eager()
        logger.debug(command_result)
        ath_result = re.findall(b'ra0\r\nra0(.+)', command_result)
        logger.debug(ath_result[0].split())
        ath_result = ath_result[0].split()[0]
        if ath_result.decode('utf-8') == 'No':
            self.tn.write(b'iwconfig rai0\r\n')
            command_result = self.tn.read_until(b'No', timeout=2)
            logger.debug(command_result)
            ath_result = re.findall(b'rai0(.+)', command_result)[1].split()[0]
            logger.debug(ath_result)
            if ath_result.decode('utf-8') == 'No':
                logger.error('No such device')
                test_radio = None
            else:
                frequency = re.findall(b'Channel=(\d+)', command_result)[0].decode('utf-8')
                logger.debug(frequency)
                if int(frequency) < 36:
                    radio_2g = '1'
                    radio_5g = '0'
                else:
                    radio_2g = '0'
                    radio_5g = '1'
        else:
            frequency = re.findall(b'Channel=(\d+)', command_result)[0].decode('utf-8')
            logger.debug(frequency)
            if int(frequency) < 36:
                radio_2g = '0'
                radio_5g = 'i0'
            else:
                radio_2g = 'i0'
                radio_5g = '0'
        logger.info('2g:ra'+radio_2g)
        logger.info('5g:ra'+radio_5g)
        return radio_2g, radio_5g

    def get_RSSI_mtk(self, radio, radio_2g, radio_5g):
        get_txrate_list = []
        get_rxrate_list = []
        get_aprssi_list = []
        get_ant0rssi_list = []
        get_ant1rssi_list = []
        get_ant2rssi_list = []
        get_ant3rssi_list = []
        get_bw_list = []
        get_nsstx_list = []
        get_nssrx_list = []
        get_mcstx_list = []
        get_mcsrx_list = []
        TXRATE_AVG = RXRATE_AVG = APRSSI_AVG = RXBW_AVG = TXNSS_AVG = RXNSS_AVG = TXMCS_AVG = RXMCS_AVG = \
            APRSSI0_AVG = APRSSI1_AVG = APRSSI2_AVG = APRSSI3_AVG = None
        if radio == '2.4g':
            radio_value = radio_2g
        elif radio == '5g':
            radio_value = radio_5g
        else:
            logger.error('Radio type is wrong')
            radio_value = None
        for i in range(10):
            self.tn.write(b'\r\n')
            logger.info('Test Radio is ' + radio + ' ra' + radio_value)
            self.tn.write(b'iwpriv ra%s show stainfo;dmesg -c\r\n' % radio_value.encode('ascii'))
            sleep(0.5)
            command_result = self.tn.read_very_eager()
            logger.debug(command_result)
            result_list = []
            for result in command_result.split():
                logger.debug(result.decode('utf-8'))
                result_list.append(result.decode('utf-8'))
            logger.debug(result_list)
            if 'HTMIX' in result_list:
                regex = re.compile(r'-\d+')
                rssi_list = []
                for i in result_list:
                    logger.debug(regex.findall(i))
                    rssi_list.append(regex.findall(i))
                while [] in rssi_list:
                    rssi_list.remove([])
                logger.info(rssi_list)
                res = result_list.index('HTMIX')
                logger.debug(res)
                get_txrate = result_list[res+5]
                get_txrate_list.append(get_txrate)
                get_rxrate = result_list[res+6]
                get_rxrate_list.append(get_rxrate)
                get_aprssi = max(rssi_list[0][0], rssi_list[0][1])
                get_ant0rssi = rssi_list[0][0]
                get_ant0rssi_list.append(get_ant0rssi)
                get_ant1rssi = rssi_list[0][1]
                get_ant1rssi_list.append(get_ant1rssi)
                if len(rssi_list[0]) > 2:
                    get_ant2rssi = rssi_list[0][2]
                    get_ant2rssi_list.append(get_ant2rssi)
                elif len(rssi_list[0]) > 3:
                    get_ant3rssi = rssi_list[0][3]
                    get_ant3rssi_list.append(get_ant3rssi)
                get_aprssi_list.append(get_aprssi)
                get_bw = result_list[res+1]
                get_bw_list.append(get_bw)
                get_nsstx = len(rssi_list[0])
                get_nsstx_list.append(get_nsstx)
                get_nssrx = len(rssi_list[0])
                get_nssrx_list.append(get_nssrx)
                get_mcstx = result_list[res+2]
                get_mcstx_list.append(get_mcstx)
                get_mcsrx = result_list[res + 2]
                get_mcsrx_list.append(get_mcsrx)

                logger.debug(get_txrate_list)
                logger.debug(get_rxrate_list)
                logger.debug(get_aprssi_list)
                logger.debug(get_bw_list)
                logger.debug(get_nsstx_list)
                logger.debug(get_nssrx_list)
                logger.debug(get_mcstx_list)
                logger.debug(get_mcsrx_list)
                TXRATE_AVG = max(set(get_txrate_list), key=get_txrate_list.count)
                RXRATE_AVG = max(set(get_rxrate_list), key=get_rxrate_list.count)
                APRSSI_AVG = max(set(get_aprssi_list), key=get_aprssi_list.count)
                APRSSI0_AVG = max(set(get_ant0rssi_list), key=get_ant0rssi_list.count)
                APRSSI1_AVG = max(set(get_ant1rssi_list), key=get_ant1rssi_list.count)
                if len(rssi_list[0]) > 2:
                    APRSSI2_AVG = max(set(get_ant2rssi_list), key=get_ant2rssi_list.count)
                elif len(rssi_list[0]) > 3:
                    APRSSI3_AVG = max(set(get_ant3rssi_list), key=get_ant3rssi_list.count)
                RXBW_AVG = max(set(get_bw_list), key=get_bw_list.count)
                TXNSS_AVG = max(set(get_nsstx_list), key=get_nsstx_list.count)
                RXNSS_AVG = max(set(get_nssrx_list), key=get_nssrx_list.count)
                TXMCS_AVG = max(set(get_mcstx_list), key=get_mcstx_list.count)
                RXMCS_AVG = max(set(get_mcsrx_list), key=get_mcsrx_list.count)
            else:
                logger.info('Raido is not opened')
        logger.info('AP:')
        logger.info('TXRATE:')
        logger.info(TXRATE_AVG)
        logger.info('RXRATE:')
        logger.info(RXRATE_AVG)
        logger.info('APRSSI:')
        logger.info(APRSSI_AVG)
        logger.info('APRSSI0:')
        logger.info(APRSSI0_AVG)
        logger.info('APRSSI1:')
        logger.info(APRSSI1_AVG)
        logger.info('APRSSI2:')
        logger.info(APRSSI2_AVG)
        logger.info('APRSSI3:')
        logger.info(APRSSI3_AVG)
        logger.info('RXBW:')
        logger.info(RXBW_AVG)
        logger.info('TXNSS:')
        logger.info(TXNSS_AVG)
        logger.info('RXNSS:')
        logger.info(RXNSS_AVG)
        logger.info('TXMCS:')
        logger.info(TXMCS_AVG)
        logger.info('RXMCS:')
        logger.info(RXMCS_AVG)
        # return get_channel, TXRATE_AVG, RXRATE_AVG, APRSSI_AVG, RXBW_AVG, TXNSS_AVG, RXNSS_AVG
        # return TXRATE_AVG, RXRATE_AVG, APRSSI_AVG, RXBW_AVG, TXNSS_AVG, RXNSS_AVG, TXMCS_AVG, RXMCS_AVG
        return RXRATE_AVG, APRSSI_AVG, RXBW_AVG, RXNSS_AVG, RXMCS_AVG

    def get_testradio_celeno(self):
        test_radio = 'wlan0_0'
        self.tn.write(b'\r\n')
        self.tn.read_until(b':/#', timeout=2)
        self.tn.write(b'iw wlan0_0 info\r\n')
        sleep(0.2)
        command_result = self.tn.read_very_eager()
        logger.debug(command_result)
        try:
            channel = re.findall(b'channel (.\d+)', command_result)
            logger.debug(channel)
            logger.debug(channel[0].decode('utf-8'))
            channel = channel[0].decode('utf-8')
            if int(channel) < 36:
                radio_2g = '0'
                radio_5g = '1'
            else:
                radio_2g = '1'
                radio_5g = '0'
        except:
            logger.error('No such device')
            self.tn.write(b'iw wlan1_0 info\r\n')
            sleep(0.2)
            command_result = self.tn.read_very_eager()
            logger.debug(command_result)
            try:
                channel = re.findall(b'channel (.\d+)', command_result)
                logger.debug(channel)
                logger.debug(channel[0].decode('utf-8'))
                channel = channel[0].decode('utf-8')
                if int(channel) < 36:
                    radio_2g = '1'
                    radio_5g = '0'
                else:
                    radio_2g = '0'
                    radio_5g = '1'
            except:
                logger.error('No such device')
        logger.info('2g:wlan'+radio_2g+'_0')
        logger.info('5g:wlan'+radio_5g+'_0')
        return radio_2g, radio_5g

    def get_RSSI_celeno(self, radio, radio_2g, radio_5g):
        get_ant0rssi_list = []
        get_ant1rssi_list = []
        get_ant2rssi_list = []
        get_ant3rssi_list = []
        if radio == '2.4g':
            radio_value = radio_2g
        elif radio == '5g':
            radio_value = radio_5g
        else:
            logger.error('Radio type is wrong')
            radio_value = None
        for i in range(10):
            self.tn.write(b'\r\n')
            self.tn.write(b'iw wlan%s_0 ATE stat' % radio_value.encode('ascii') + b'\n')
            sleep(0.5)
            command_result = self.tn.read_very_eager()
            logger.debug(command_result)
            get_ant0rssi = re.findall(b'RSSI_0= (-\d+)', command_result)[0].decode('ascii')
            get_ant0rssi_list.append(get_ant0rssi)
            get_ant1rssi = re.findall(b'RSSI_1= (-\d+)', command_result)[0].decode('ascii')
            get_ant1rssi_list.append(get_ant1rssi)
            get_ant2rssi = re.findall(b'RSSI_2= (-\d+)', command_result)[0].decode('ascii')
            get_ant2rssi_list.append(get_ant2rssi)
            get_ant3rssi = re.findall(b'RSSI_3= (-\d+)', command_result)[0].decode('ascii')
            get_ant3rssi_list.append(get_ant3rssi)
            logger.debug(get_ant0rssi_list)
            logger.debug(get_ant1rssi_list)
            logger.debug(get_ant2rssi_list)
            logger.debug(get_ant3rssi_list)
        APRSSI0_AVG = max(set(get_ant0rssi_list), key=get_ant0rssi_list.count)
        APRSSI1_AVG = max(set(get_ant1rssi_list), key=get_ant1rssi_list.count)
        APRSSI2_AVG = max(set(get_ant2rssi_list), key=get_ant2rssi_list.count)
        APRSSI3_AVG = max(set(get_ant3rssi_list), key=get_ant3rssi_list.count)
        logger.info('APRSSI0:')
        logger.info(APRSSI0_AVG)
        logger.info('APRSSI1:')
        logger.info(APRSSI1_AVG)
        logger.info('APRSSI2:')
        logger.info(APRSSI2_AVG)
        logger.info('APRSSI3:')
        logger.info(APRSSI3_AVG)
        return APRSSI0_AVG, APRSSI1_AVG, APRSSI2_AVG, APRSSI3_AVG

    # def get_RSSI(self, radio):
    #     if self.ap_type == 'WF-194':
    #         test_radio = 'ath0'
    #         self.tn.read_until(b'root@OpenWrt:/# ')
    #         self.tn.write(b'iwconfig ath0\r\n')
    #         command_result = self.tn.read_until(b'No', timeout=2)
    #         logger.debug(command_result.split())
    #         ath_result = re.findall(b'ath0(.+)', command_result)[1].split()[0]
    #         logger.debug(ath_result)
    #         if ath_result.decode('utf-8') == 'No':
    #             self.tn.write(b'iwconfig ath1\r\n')
    #             command_result = self.tn.read_until(b'No', timeout=2)
    #             logger.debug(command_result)
    #             ath_result = re.findall(b'ath1(.+)', command_result)[1].split()[0]
    #             logger.debug(ath_result)
    #             if ath_result.decode('utf-8') == 'No':
    #                 logger.error('No such device')
    #                 test_radio = None
    #             else:
    #                 frequency = re.findall(b'Frequency:(\d+\.\d+) GHz', command_result)[0].decode('utf-8')
    #                 logger.debug(frequency)
    #                 power = re.findall(b'(Tx-Power:\d+ dBm)', command_result)[0].decode('utf-8')
    #                 logger.debug(power)
    #                 if float(frequency) < 5.0:
    #                     radio_2g = '1'
    #                     radio_5g = '0'
    #                 else:
    #                     radio_2g = '0'
    #                     radio_5g = '1'
    #         else:
    #             frequency = re.findall(b'Frequency:(\d+\.\d+) GHz', command_result)[0].decode('utf-8')
    #             logger.debug(frequency)
    #             power = re.findall(b'(Tx-Power:\d+ dBm)', command_result)[0].decode('utf-8')
    #             logger.debug(power)
    #             if float(frequency) < 5.0:
    #                 radio_2g = '0'
    #                 radio_5g = '1'
    #             else:
    #                 radio_2g = '1'
    #                 radio_5g = '0'
    #         get_txrate_list = []
    #         get_rxrate_list = []
    #         get_rxrssi_list = []
    #         get_nsstx_list = []
    #         get_nssrx_list = []
    #         get_channel = TXRATE_AVG = RXRATE_AVG = RXRSSI_AVG = TXNSS_AVG = RXNSS_AVG = None
    #         i = 1
    #         for i in range(10):
    #             # self.tn.write(b'\r\n')
    #             self.tn.read_until(b'root@OpenWrt:/# ')
    #             if radio == '2.4g':
    #                 logger.info('Test Radio is ' + radio + ' ath' + radio_2g)
    #                 self.tn.write(b'wlanconfig ath%s list\r\n' % radio_2g.encode('ascii'))
    #                 # self.tn.write(b'wifistats wifi%s 9\r\n' % radio_2g.encode('ascii'))
    #                 # self.tn.write(b'wifistats wifi%s 10\r\n' % radio_2g.encode('ascii'))
    #             elif radio == '5g':
    #                 logger.info('Test Radio is ' + radio + ' ath' + radio_5g)
    #                 self.tn.write(b'wlanconfig ath%s list\r\n' % radio_5g.encode('ascii'))
    #                 # self.tn.write(b'wifistats wifi%s 9\r\n' % radio_5g.encode('ascii'))
    #                 # self.tn.write(b'wifistats wifi%s 10\r\n' % radio_5g.encode('ascii'))
    #             else:
    #                 logger.error('Radio type is wrong')
    #                 break
    #             command_result = self.tn.read_until(b'root@OpenWrt:/# ', timeout=2)
    #             logger.debug(command_result.split())
    #             client_type = command_result.split()[3].decode('utf-8')
    #             logger.debug(client_type)
    #             if client_type == 'Error':
    #                 logger.info('Client')
    #                 self.tn.write(b'\r\n')
    #             else:
    #                 basic_info = re.findall(b'PSMODE\r\n(.+)', command_result)[0].split()
    #                 logger.debug(basic_info)
    #                 self.tn.write(b'\r\n')
    #                 if basic_info[0].decode('utf-8') == 'root@OpenWrt:/#':
    #                     logger.info('No client')
    #                     break
    #                 else:
    #                     get_channel = basic_info[2].decode('utf-8')
    #                     get_txrate = re.sub('M', '', basic_info[3].decode('utf-8'))
    #                     get_txrate_list.append(get_txrate)
    #                     get_rxrate = re.sub('M', '', basic_info[4].decode('utf-8'))
    #                     get_rxrate_list.append(get_rxrate)
    #                     get_rxrssi = basic_info[5].decode('utf-8')
    #                     get_rxrssi_list.append(get_rxrssi)
    #                     get_nsstx = basic_info[22].decode('utf-8')
    #                     get_nsstx_list.append(get_nsstx)
    #                     get_nssrx = basic_info[21].decode('utf-8')
    #                     get_nssrx_list.append(get_nssrx)
    #
    #                 logger.debug(get_channel)
    #                 logger.debug(get_txrate_list)
    #                 logger.debug(get_rxrate_list)
    #                 logger.debug(get_rxrssi_list)
    #                 logger.debug(get_nsstx_list)
    #                 logger.debug(get_nssrx_list)
    #                 TXRATE_AVG = max(set(get_txrate_list), key=get_txrate_list.count)
    #                 RXRATE_AVG = max(set(get_rxrate_list), key=get_rxrate_list.count)
    #                 RXRSSI_AVG = int(max(set(get_rxrssi_list), key=get_rxrssi_list.count)) - 96
    #                 TXNSS_AVG = max(set(get_nsstx_list), key=get_nsstx_list.count)
    #                 RXNSS_AVG = max(set(get_nssrx_list), key=get_nssrx_list.count)
    #         logger.info('AP:')
    #         logger.info(power)
    #         logger.info('Channel:')
    #         logger.info(get_channel)
    #         logger.info('TXRATE:')
    #         logger.info(TXRATE_AVG)
    #         logger.info('RXRATE:')
    #         logger.info(RXRATE_AVG)
    #         logger.info('RXRSSI:')
    #         logger.info(RXRSSI_AVG)
    #         logger.info('TXNSS:')
    #         logger.info(TXNSS_AVG)
    #         logger.info('RXNSS:')
    #         logger.info(RXNSS_AVG)
    #         if radio == '2.4g':
    #             # self.tn.write(b'wifistats wifi%s 9\r\n' % radio_2g.encode('ascii'))
    #             self.tn.write(b'wifistats wifi%s 10\r\n' % radio_2g.encode('ascii'))
    #         elif radio == '5g':
    #             # self.tn.write(b'wifistats wifi%s 9\r\n' % radio_5g.encode('ascii'))
    #             self.tn.write(b'wifistats wifi%s 10\r\n' % radio_5g.encode('ascii'))
    #         else:
    #             logger.error('Radio type is wrong')
    #         command_result = self.tn.read_until(b'per_chain_rssi_pkt_type', timeout=2)
    #         logger.debug(command_result.split())
    #         # # tx info 9
    #         # legacy_cck_rates = re.findall(b'(Legacy CCK Rates:.+)', command_result)[0].decode('utf-8')
    #         # logger.debug(legacy_cck_rates)
    #         # legacy_ofdm_rates = re.findall(b'(Legacy OFDM Rates:.+)', command_result)[0].decode('utf-8')
    #         # logger.debug(legacy_ofdm_rates)
    #         # tx_mcs = re.findall(b'(tx_mcs =.+)', command_result)[0].decode('utf-8')
    #         # logger.debug(tx_mcs)
    #         # acmumimo_tx_mcs = re.findall(b'(ac_mu_mimo_tx_mcs =.+)', command_result)[0].decode('utf-8')
    #         # logger.debug(acmumimo_tx_mcs)
    #         # axmumimo_tx_mcs = re.findall(b'(ax_mu_mimo_tx_mcs =.+)', command_result)[0].decode('utf-8')
    #         # logger.debug(axmumimo_tx_mcs)
    #         # ofdma_tx_mcs = re.findall(b'(ofdma_tx_mcs =.+)', command_result)[0].decode('utf-8')
    #         # logger.debug(ofdma_tx_mcs)
    #         # tx_nss = re.findall(b'(tx_nss =.+)', command_result)[0].decode('utf-8')
    #         # logger.debug(tx_nss)
    #         # acmumimo_tx_nss = re.findall(b'(ac_mu_mimo_tx_nss =.+)', command_result)[0].decode('utf-8')
    #         # logger.debug(acmumimo_tx_nss)
    #         # axmumimo_tx_nss = re.findall(b'(ax_mu_mimo_tx_nss =.+)', command_result)[0].decode('utf-8')
    #         # logger.debug(axmumimo_tx_nss)
    #         # ofdma_tx_nss = re.findall(b'(ofdma_tx_nss =.+)', command_result)[0].decode('utf-8')
    #         # logger.debug(ofdma_tx_nss)
    #         # tx_bw = re.findall(b'(tx_bw =.+)', command_result)[0].decode('utf-8')
    #         # logger.debug(tx_bw)
    #         # acmumimo_tx_bw = re.findall(b'(ac_mu_mimo_tx_bw =.+)', command_result)[0].decode('utf-8')
    #         # logger.debug(acmumimo_tx_bw)
    #         # axmumimo_tx_bw = re.findall(b'(ax_mu_mimo_tx_bw =.+)', command_result)[0].decode('utf-8')
    #         # logger.debug(axmumimo_tx_bw)
    #         # ofdma_tx_bw = re.findall(b'(ofdma_tx_bw =.+)', command_result)[0].decode('utf-8')
    #         # logger.debug(ofdma_tx_bw)
    #         # tx_stbc = re.findall(b'(tx_stbc =.+)', command_result)[0].decode('utf-8')
    #         # logger.debug(tx_stbc)
    #         # tx_pream = re.findall(b'(tx_pream =.+)', command_result)[0].decode('utf-8')
    #         # logger.debug(tx_pream)
    #         # rx info 10
    #         rssi_in_dbm = re.findall(b'rssi_in_dbm =(.+)', command_result)[0].decode('utf-8')
    #         logger.debug(rssi_in_dbm)
    #         rx_mcs = re.findall(b'rx_mcs =(.+)', command_result)[0].decode('utf-8')
    #         logger.debug(rx_mcs)
    #         rx_nss = re.findall(b'rx_nss =(.+)', command_result)[0].decode('utf-8')
    #         logger.debug(rx_nss)
    #         rx_dcm = re.findall(b'rx_dcm =(.+)', command_result)[0].decode('utf-8')
    #         logger.debug(rx_dcm)
    #         rx_stbc = re.findall(b'rx_stbc =(.+)', command_result)[0].decode('utf-8')
    #         logger.debug(rx_stbc)
    #         rx_bw = re.findall(b'rx_bw =(.+)', command_result)[0].decode('utf-8')
    #         logger.debug(rx_bw)
    #         rssi_chain0 = re.findall(b'(rssi_chain\[0] =.+)', command_result)[0].decode('utf-8')
    #         logger.debug(rssi_chain0)
    #         rssi_chain1 = re.findall(b'(rssi_chain\[1] =.+)', command_result)[0].decode('utf-8')
    #         logger.debug(rssi_chain1)
    #         rssi_chain2 = re.findall(b'(rssi_chain\[2] =.+)', command_result)[0].decode('utf-8')
    #         logger.debug(rssi_chain2)
    #         rssi_chain3 = re.findall(b'(rssi_chain\[3] =.+)', command_result)[0].decode('utf-8')
    #         logger.debug(rssi_chain3)
    #         rssi_chain4 = re.findall(b'(rssi_chain\[4] =.+)', command_result)[0].decode('utf-8')
    #         logger.debug(rssi_chain4)
    #         rssi_chain5 = re.findall(b'(rssi_chain\[5] =.+)', command_result)[0].decode('utf-8')
    #         logger.debug(rssi_chain5)
    #         rssi_chain6 = re.findall(b'(rssi_chain\[6] =.+)', command_result)[0].decode('utf-8')
    #         logger.debug(rssi_chain6)
    #         rssi_chain7 = re.findall(b'(rssi_chain\[7] =.+)', command_result)[0].decode('utf-8')
    #         logger.debug(rssi_chain7)
    #         rx_pream = re.findall(b'rx_(pream =.+)', command_result)[0].decode('utf-8')
    #         logger.debug(rx_pream)
    #         rx_legacycck_rate = re.findall(b'rx_(legacy_cck_rate =.+)', command_result)[0].decode('utf-8')
    #         logger.debug(rx_legacycck_rate)
    #         rx_legacyofdm_rate = re.findall(b'rx_(legacy_ofdm_rate =.+)', command_result)[0].decode('utf-8')
    #         logger.debug(rx_legacyofdm_rate)
    #         ulofdma_rx_mcs = re.findall(b'(ul_ofdma_rx_mcs =.+)', command_result)[0].decode('utf-8')
    #         logger.debug(ulofdma_rx_mcs)
    #         ulofdma_rx_nss = re.findall(b'(ul_ofdma_rx_nss =.+)', command_result)[0].decode('utf-8')
    #         logger.debug(ulofdma_rx_nss)
    #         ulofdma_rx_bw = re.findall(b'(ul_ofdma_rx_bw =.+)', command_result)[0].decode('utf-8')
    #         logger.debug(ulofdma_rx_bw)
    #         # return power, get_channel, TXRATE_AVG, RXRATE_AVG, RXRSSI_AVG, TXNSS_AVG, RXNSS_AVG, legacy_cck_rates, \
    #         #        legacy_ofdm_rates, tx_mcs, acmumimo_tx_mcs, axmumimo_tx_mcs, ofdma_tx_mcs, tx_nss, acmumimo_tx_nss, \
    #         #        axmumimo_tx_nss, ofdma_tx_nss, tx_bw, ofdma_tx_bw, rx_legacycck_rate, rx_legacyofdm_rate, rx_mcs, \
    #         #        ulofdma_rx_mcs, rx_nss, ulofdma_rx_nss, rx_bw, ulofdma_rx_bw, rssi_chain0, rssi_chain1, rssi_chain2, \
    #         #        rssi_chain3
    #         return power, get_channel, TXRATE_AVG, RXRATE_AVG, RXRSSI_AVG, TXNSS_AVG, RXNSS_AVG, rssi_in_dbm, rx_mcs, \
    #                rx_nss, rx_bw, rssi_chain0, rssi_chain1, rssi_chain2, rssi_chain3, rx_legacycck_rate, \
    #                rx_legacyofdm_rate, ulofdma_rx_mcs, ulofdma_rx_nss, ulofdma_rx_bw
    #     elif self.ap_type == 'WF-8186':
    #         if radio == '2.4g':
    #             test_radio = 'wl0'
    #         elif radio == '5g_H':
    #             test_radio = 'wl2'
    #         else:
    #             test_radio = 'wl1'
    #         get_rate_list = []
    #         get_rssi_list = []
    #         get_mcs_list = []
    #         get_nss_list = []
    #         get_bw_list = []
    #         get_ant0_list = []
    #         get_ant1_list = []
    #         get_ant2_list = []
    #         get_ant3_list = []
    #         power_chain0_list = []
    #         power_chain1_list = []
    #         power_chain2_list = []
    #         power_chain3_list = []
    #         get_channel = get_mode = TXRATE_AVG = RXRATE_AVG = RXRSSI_AVG = MCS_AVG = NSS_AVG = BW_AVG = \
    #             RSSI_ANT0_AVG = RSSI_ANT1_AVG = RSSI_ANT2_AVG = RSSI_ANT3_AVG = POWER_ANT0_AVG = POWER_ANT1_AVG = \
    #             POWER_ANT2_AVG = POWER_ANT3_AVG = RSSI_ANT_AVG = None
    #         i = 1
    #         for i in range(1):
    #             self.tn.write(b'sh')
    #             self.tn.write(b'\r\n')
    #             self.tn.read_until(b'# ')
    #             self.tn.write(b'wl -i %s status\r\n' % test_radio.encode('ascii'))
    #             command_result = self.tn.read_until(b'HT Capabilities:', timeout=2)
    #             logger.info(command_result)
    #             channel_result = re.findall(b'Chanspec:(.+)', command_result)[0].split()
    #             logger.info(channel_result)
    #             get_channel = channel_result[2].decode('utf-8')
    #             # rssi_result = re.findall(b'Mode:(.+)', command_result)[0].split()
    #             # get_rssi = rssi_result[2].decode('utf-8')
    #             # get_rssi_list.append(get_rssi)
    #             self.tn.write(b'\r\n')
    #             self.tn.read_until(b'# ')
    #             self.tn.write(b'wl -i %s rate\r\n' % test_radio.encode('ascii'))
    #             rate_result = self.tn.read_until(b' Mbps', timeout=5)
    #             logger.info(rate_result)
    #             rate_result = re.findall(b'(.+) Mbps', rate_result)[0].split()
    #             logger.info(rate_result)
    #             get_rate = rate_result[0].decode('utf-8')
    #             get_rate_list.append(get_rate)
    #             self.tn.write(b'\r\n')
    #             self.tn.read_until(b'# ')
    #             self.tn.write(b'wl -i %s nrate\r\n' % test_radio.encode('ascii'))
    #             nrate_result = self.tn.read_until(b'auto', timeout=2)
    #             logger.info(nrate_result)
    #             nrate_result = re.findall(b'(.+)auto', nrate_result)[0].split()
    #             logger.info(nrate_result)
    #             get_mode = nrate_result[0].decode('utf-8')
    #             get_mcs = nrate_result[2].decode('utf-8')
    #             get_mcs_list.append(get_mcs)
    #             get_nss = nrate_result[4].decode('utf-8')
    #             get_nss_list.append(get_nss)
    #             get_bw = nrate_result[8].decode('utf-8')
    #             get_bw_list.append(get_bw)
    #             self.tn.write(b'\r\n')
    #             self.tn.read_until(b'# ')
    #             self.tn.write(b'wl -i %s curpower | grep ower\r\n' % test_radio.encode('ascii'))
    #             power_result = self.tn.read_until(b'Last adjusted est. power', timeout=2)
    #             logger.info(power_result)
    #             power_result_a = re.findall(b'PHY Maximum Power Target among all rates(.+)', power_result)[0]
    #             logger.info('PHY Maximum Power Target among all rates' + str(power_result_a.decode('utf-8')))
    #             power_result_b = re.findall(b'PHY Power Target for the current rate(.+)', power_result)[0]
    #             logger.info('PHY Power Target for the current rate' + str(power_result_b.decode('utf-8')))
    #             power_result_c = re.findall(b'Last est. power(.+)', power_result)[0]
    #             logger.info('Last est. power' + str(power_result_c.decode('utf-8')))
    #             # power_result_d = re.findall(b'Last adjusted est. power(.+)', power_result)[0]
    #             # logger.info('Last adjusted est. power' + str(power_result_d.decode('utf-8')))
    #             # logger.info(power_result_d.split())
    #             power_chain0 = power_result_c.split()[1].decode('utf-8')
    #             power_chain0_list.append(power_chain0)
    #             power_chain1 = power_result_c.split()[2].decode('utf-8')
    #             power_chain1_list.append(power_chain1)
    #             power_chain2 = power_result_c.split()[3].decode('utf-8')
    #             power_chain2_list.append(power_chain2)
    #             power_chain3 = power_result_c.split()[4].decode('utf-8')
    #             power_chain3_list.append(power_chain3)
    #         self.tn.write(b'\r\n')
    #         self.tn.read_until(b'# ')
    #         self.tn.write(b'wl -i %s dump rssi\r\n' % test_radio.encode('ascii'))
    #         rssi_result = self.tn.read_until(b'#  ', timeout=2)
    #         logger.info(rssi_result)
    #         rssi_result_len = len(rssi_result)
    #         logger.info(rssi_result_len)
    #         if rssi_result_len < 150:
    #             get_ant_0 = get_ant_1 = get_ant_2 = get_ant_3 = None
    #         else:
    #             RSSI_ANT_AVG = re.findall(b'RSSI(.+)', rssi_result)[0].split()[-1].decode('utf-8')
    #             logger.info(RSSI_ANT_AVG)
    #             RSSI_ANT0_AVG = re.findall(b'ANT0(.+)', rssi_result)[1].split()[-1].decode('utf-8')
    #             logger.info(RSSI_ANT0_AVG)
    #             RSSI_ANT1_AVG = re.findall(b'ANT1(.+)', rssi_result)[1].split()[-1].decode('utf-8')
    #             logger.info(RSSI_ANT1_AVG)
    #             RSSI_ANT2_AVG = re.findall(b'ANT2(.+)', rssi_result)[1].split()[-1].decode('utf-8')
    #             logger.info(RSSI_ANT2_AVG)
    #             RSSI_ANT3_AVG = re.findall(b'ANT3(.+)', rssi_result)[1].split()[-1].decode('utf-8')
    #             logger.info(RSSI_ANT3_AVG)
    #         RATE_AVG = max(set(get_rate_list), key=get_rate_list.count)
    #         # RSSI_AVG = int(max(set(get_rssi_list), key=get_rssi_list.count))
    #         MCS_AVG = max(set(get_mcs_list), key=get_mcs_list.count)
    #         MCS_AVG = str(get_mode) + MCS_AVG
    #         NSS_AVG = max(set(get_nss_list), key=get_nss_list.count)
    #         BW_AVG = max(set(get_bw_list), key=get_bw_list.count)
    #         # RSSI_ANT0_AVG = max(set(get_ant0_list), key=get_ant0_list.count)
    #         # RSSI_ANT1_AVG = max(set(get_ant1_list), key=get_ant1_list.count)
    #         # RSSI_ANT2_AVG = max(set(get_ant2_list), key=get_ant2_list.count)
    #         # RSSI_ANT3_AVG = max(set(get_ant3_list), key=get_ant3_list.count)
    #         POWER_ANT0_AVG = max(set(power_chain0_list), key=power_chain0_list.count)
    #         POWER_ANT1_AVG = max(set(power_chain1_list), key=power_chain1_list.count)
    #         POWER_ANT2_AVG = max(set(power_chain2_list), key=power_chain2_list.count)
    #         POWER_ANT3_AVG = max(set(power_chain3_list), key=power_chain3_list.count)
    #         logger.info('Info from AP:Channel:')
    #         logger.info(get_channel)
    #         logger.info('RATE:')
    #         logger.info(RATE_AVG)
    #         logger.info('RSSI:')
    #         logger.info(RSSI_ANT_AVG)
    #         logger.info('MCS:')
    #         logger.info(MCS_AVG)
    #         logger.info('NSS:')
    #         logger.info(NSS_AVG)
    #         logger.info('BW:')
    #         logger.info(BW_AVG)
    #         logger.info('RSSI_ANT0:')
    #         logger.info(RSSI_ANT0_AVG)
    #         logger.info('RSSI_ANT1:')
    #         logger.info(RSSI_ANT1_AVG)
    #         logger.info('RSSI_ANT2:')
    #         logger.info(RSSI_ANT2_AVG)
    #         logger.info('RSSI_ANT3:')
    #         logger.info(RSSI_ANT3_AVG)
    #         logger.info('POWER_ANT0:')
    #         logger.info(POWER_ANT0_AVG)
    #         logger.info('POWER_ANT1:')
    #         logger.info(POWER_ANT1_AVG)
    #         logger.info('POWER_ANT2:')
    #         logger.info(POWER_ANT2_AVG)
    #         logger.info('POWER_ANT3:')
    #         logger.info(POWER_ANT3_AVG)
    #         # print(RXRSSI_AVG)
    #         return get_channel, RATE_AVG, RSSI_ANT_AVG, MCS_AVG, NSS_AVG, BW_AVG, RSSI_ANT0_AVG, RSSI_ANT1_AVG, \
    #                RSSI_ANT2_AVG, RSSI_ANT3_AVG, POWER_ANT0_AVG, POWER_ANT1_AVG, POWER_ANT2_AVG, POWER_ANT3_AVG
    #     elif self.ap_type == 'WF-6601':
    #         test_radio = 'ath0'
    #         self.tn.read_until(b'root@OpenWrt:/# ')
    #         self.tn.write(b'clear\r\n')
    #         self.tn.write(b'iwconfig ath0\r\n')
    #         command_result = self.tn.read_until(b'No', timeout=2)
    #         logger.debug(command_result)
    #         logger.debug(command_result.split())
    #
    #         ath_result = re.findall(b'iwconfig ath0\r\nath0(.+)', command_result)[0].split()[0]
    #         logger.debug(ath_result)
    #         if ath_result.decode('utf-8') == 'No':
    #             self.tn.write(b'iwconfig ath1\r\n')
    #             command_result = self.tn.read_until(b'No', timeout=2)
    #             logger.debug(command_result)
    #             ath_result = re.findall(b'ath1(.+)', command_result)[1].split()[0]
    #             logger.debug(ath_result)
    #             if ath_result.decode('utf-8') == 'No':
    #                 logger.error('No such device')
    #                 test_radio = None
    #             else:
    #                 frequency = re.findall(b'Frequency:(\d+\.\d+) GHz', command_result)[0].decode('utf-8')
    #                 logger.debug(frequency)
    #                 power = re.findall(b'(Tx-Power=\d+ dBm)', command_result)[0].decode('utf-8')
    #                 logger.debug(power)
    #                 if float(frequency) < 5.0:
    #                     radio_2g = '1'
    #                     radio_5g = '0'
    #                 else:
    #                     radio_2g = '0'
    #                     radio_5g = '1'
    #         else:
    #             frequency = re.findall(b'Frequency:(\d+\.\d+) GHz', command_result)[0].decode('utf-8')
    #             logger.debug(frequency)
    #             power = re.findall(b'(Tx-Power=\d+ dBm)', command_result)[0].decode('utf-8')
    #             logger.debug(power)
    #             if float(frequency) < 5.0:
    #                 radio_2g = '0'
    #                 radio_5g = '1'
    #             else:
    #                 radio_2g = '1'
    #                 radio_5g = '0'
    #         get_txrate_list = []
    #         get_rxrate_list = []
    #         get_txrssi_list = []
    #         get_rxrssi_list = []
    #         get_nsstx_list = []
    #         get_nssrx_list = []
    #         get_channel = TXRATE_AVG = RXRATE_AVG = TXRSSI_AVG = RXRSSI_AVG = TXNSS_AVG = RXNSS_AVG = None
    #         i = 1
    #         for i in range(10):
    #             # self.tn.write(b'\r\n')
    #             self.tn.read_until(b'root@OpenWrt:/# ')
    #             if radio == '2.4g':
    #                 logger.info('Test Radio is ' + radio + ' ath' + radio_2g)
    #                 self.tn.write(b'wlanconfig ath%s list\r\n' % radio_2g.encode('ascii'))
    #                 # self.tn.write(b'wifistats wifi%s 9\r\n' % radio_2g.encode('ascii'))
    #                 # self.tn.write(b'wifistats wifi%s 10\r\n' % radio_2g.encode('ascii'))
    #             elif radio == '5g':
    #                 logger.info('Test Radio is ' + radio + ' ath' + radio_5g)
    #                 self.tn.write(b'wlanconfig ath%s list\r\n' % radio_5g.encode('ascii'))
    #                 # self.tn.write(b'wifistats wifi%s 9\r\n' % radio_5g.encode('ascii'))
    #                 # self.tn.write(b'wifistats wifi%s 10\r\n' % radio_5g.encode('ascii'))
    #             else:
    #                 logger.error('Radio type is wrong')
    #                 break
    #             command_result = self.tn.read_until(b'root@OpenWrt:/# ', timeout=2)
    #             logger.debug(command_result.split())
    #             client_type = command_result.split()[4].decode('utf-8')
    #             logger.debug(client_type)
    #             if client_type == 'unable':
    #                 logger.info('Client')
    #                 self.tn.write(b'\r\n')
    #                 if radio == '2.4g':
    #                     # self.tn.write(b'wifistats wifi%s 9\r\n' % radio_2g.encode('ascii'))
    #                     self.tn.write(b'iwpriv ath%s txrx_fw_stats 3\r\n' % radio_2g.encode('ascii'))
    #                     self.tn.write(b'iwpriv ath%s txrx_fw_stats 6\r\n' % radio_2g.encode('ascii'))
    #                     self.tn.write(b'dmesg -c\r\n')
    #                 elif radio == '5g':
    #                     # self.tn.write(b'wifistats wifi%s 9\r\n' % radio_5g.encode('ascii'))
    #                     self.tn.write(b'iwpriv ath%s txrx_fw_stats 3\r\n' % radio_5g.encode('ascii'))
    #                     self.tn.write(b'iwpriv ath%s txrx_fw_stats 6\r\n' % radio_5g.encode('ascii'))
    #                     self.tn.write(b'dmesg -c\r\n')
    #                 else:
    #                     logger.error('Radio type is wrong')
    #                 command_result = self.tn.read_until(b'Ack RSSI:', timeout=2)
    #                 logger.debug(command_result.split())
    #                 rssi_in_dbm = re.findall(b'RSSI \(comb_ht\):(.+)', command_result)[0].decode('utf-8')
    #                 logger.debug(rssi_in_dbm)
    #                 get_txrssi_list.append(rssi_in_dbm)
    #                 logger.debug(get_txrssi_list)
    #                 TXRSSI_AVG = int(max(set(get_txrssi_list), key=get_txrssi_list.count)) - 95
    #             else:
    #                 basic_info = re.findall(b'PSMODE\r\n(.+)', command_result)[0].split()
    #                 logger.debug(basic_info)
    #                 self.tn.write(b'\r\n')
    #                 if basic_info[0].decode('utf-8') == 'root@OpenWrt:/#':
    #                     logger.info('No client')
    #                     break
    #                 else:
    #                     get_channel = basic_info[2].decode('utf-8')
    #                     get_txrate = re.sub('M', '', basic_info[3].decode('utf-8'))
    #                     get_txrate_list.append(get_txrate)
    #                     get_rxrate = re.sub('M', '', basic_info[4].decode('utf-8'))
    #                     get_rxrate_list.append(get_rxrate)
    #                     get_rxrssi = basic_info[5].decode('utf-8')
    #                     get_rxrssi_list.append(get_rxrssi)
    #                     # get_nsstx = basic_info[22].decode('utf-8')
    #                     # get_nsstx_list.append(get_nsstx)
    #                     # get_nssrx = basic_info[21].decode('utf-8')
    #                     # get_nssrx_list.append(get_nssrx)
    #                 logger.debug(get_channel)
    #                 logger.debug(get_txrate_list)
    #                 logger.debug(get_rxrate_list)
    #                 logger.debug(get_rxrssi_list)
    #                 logger.debug(get_nsstx_list)
    #                 logger.debug(get_nssrx_list)
    #                 TXRATE_AVG = max(set(get_txrate_list), key=get_txrate_list.count)
    #                 RXRATE_AVG = max(set(get_rxrate_list), key=get_rxrate_list.count)
    #                 RXRSSI_AVG = int(max(set(get_rxrssi_list), key=get_rxrssi_list.count)) - 95
    #                 # TXNSS_AVG = max(set(get_nsstx_list), key=get_nsstx_list.count)
    #                 # RXNSS_AVG = max(set(get_nssrx_list), key=get_nssrx_list.count)
    #         logger.info('AP:')
    #         logger.info(power)
    #         logger.info('Channel:')
    #         logger.info(get_channel)
    #         logger.info('TXRATE:')
    #         logger.info(TXRATE_AVG)
    #         logger.info('RXRATE:')
    #         logger.info(RXRATE_AVG)
    #         logger.info('TXRSSI:')
    #         logger.info(TXRSSI_AVG)
    #         logger.info('RXRSSI:')
    #         logger.info(RXRSSI_AVG)
    #         # logger.info('TXNSS:')
    #         # logger.info(TXNSS_AVG)
    #         # logger.info('RXNSS:')
    #         # logger.info(RXNSS_AVG)
    #         return power, get_channel, TXRATE_AVG, RXRATE_AVG, TXRSSI_AVG, RXRSSI_AVG

    def close(self):
        self.tn.close()


class product_RSSI_ssh:
    def __init__(self, ip, username, password, radio, ap_type):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=ip, port=22, username=username, password=password)
        self.username = username
        self.password = password
        self.radio = radio
        self.ap_type = ap_type

    def counts_reset(self):
        stdin, stdout, stderr = self.ssh.exec_command('df')
        result, err = stdout.read(), stderr.read()
        logger.debug(result.decode())
        logger.debug(err.decode())
        stdin, stdout, stderr = self.ssh.exec_command(b'dmesg -c')
        result, err = stdout.read(), stderr.read()
        logger.debug(result.decode())
        logger.debug(err.decode())
        stdin, stdout, stderr = self.ssh.exec_command(b'iwpriv wdev0ap0 setcmd "qstats reset"')
        result, err = stdout.read(), stderr.read()
        logger.debug(result.decode())
        logger.debug(err.decode())
        stdin, stdout, stderr = self.ssh.exec_command(b'iwpriv wdev0sta0 setcmd "qstats reset"')
        result, err = stdout.read(), stderr.read()
        logger.debug(result.decode())
        logger.debug(err.decode())
        stdin, stdout, stderr = self.ssh.exec_command(b'iwpriv wdev1ap0 setcmd "qstats reset"')
        result, err = stdout.read(), stderr.read()
        logger.debug(result.decode())
        logger.debug(err.decode())
        stdin, stdout, stderr = self.ssh.exec_command(b'iwpriv wdev1sta0 setcmd "qstats reset"')
        result, err = stdout.read(), stderr.read()
        logger.debug(result.decode())
        logger.debug(err.decode())
        sleep(1)

    def get_RSSI_marvellap(self, radio):
        if radio == '2.4g':
            test_radio = '1'
        else:
            test_radio = '0'
        get_linkrate_list = []
        get_rssi_list = []
        get_ant0rssi_list = []
        get_ant1rssi_list = []
        get_ant2rssi_list = []
        get_ant3rssi_list = []
        LINK_RATE_AVG = RSSI_ANT0_AVG = RSSI_ANT1_AVG = RSSI_ANT2_AVG = RSSI_ANT3_AVG = None
        i = 1
        for i in range(10):
            stdin, stdout, stderr = self.ssh.exec_command(b'iwpriv wdev%sap0 getstalistext;dmesg -c' % test_radio.encode('ascii'))
            result, err = stdout.read(), stderr.read()
            logger.debug(result.decode())
            logger.debug(err.decode())

            rssi_result = result
            logger.debug(rssi_result)
            link_result = re.findall(b'Total(.+)', rssi_result)[0].split()[0].decode('utf-8')
            logger.debug(link_result)
            if link_result != '1':
                get_rssi = get_ant0_rssi = get_ant1_rssi = get_ant2_rssi = get_ant3_rssi = None
            else:
                get_link_rate = re.findall(b'Rate(.+)', rssi_result)[0].split()[0].decode('utf-8')
                get_linkrate_list.append(get_link_rate)
                logger.debug(get_link_rate)
                logger.debug(get_linkrate_list)
                get_ant0_rssi = re.findall(b'RSSI:(.+)', rssi_result)[0].split()[1].decode('utf-8')
                get_ant0rssi_list.append(get_ant0_rssi)
                logger.debug(get_ant0_rssi)
                logger.debug(get_ant0rssi_list)
                get_ant1_rssi = re.findall(b'RSSI:(.+)', rssi_result)[0].split()[3].decode('utf-8')
                get_ant1rssi_list.append(get_ant1_rssi)
                logger.debug(get_ant1_rssi)
                logger.debug(get_ant1rssi_list)
                get_ant2_rssi = re.findall(b'RSSI:(.+)', rssi_result)[0].split()[5].decode('utf-8')
                get_ant2rssi_list.append(get_ant2_rssi)
                logger.debug(get_ant2_rssi)
                logger.debug(get_ant2rssi_list)
                get_ant3_rssi = re.findall(b'RSSI:(.+)', rssi_result)[0].split()[7].decode('utf-8')
                get_ant3rssi_list.append(get_ant3_rssi)
                logger.debug(get_ant3_rssi)
                logger.debug(get_ant3rssi_list)
                sleep(1)
        LINK_RATE_AVG = max(set(get_linkrate_list), key=get_linkrate_list.count)
        RSSI_ANT0_AVG = max(set(get_ant0rssi_list), key=get_ant0rssi_list.count)
        get_rssi_list.append(RSSI_ANT0_AVG)
        RSSI_ANT1_AVG = max(set(get_ant1rssi_list), key=get_ant1rssi_list.count)
        get_rssi_list.append(RSSI_ANT1_AVG)
        RSSI_ANT2_AVG = max(set(get_ant2rssi_list), key=get_ant2rssi_list.count)
        get_rssi_list.append(RSSI_ANT2_AVG)
        RSSI_ANT3_AVG = max(set(get_ant3rssi_list), key=get_ant3rssi_list.count)
        get_rssi_list.append(RSSI_ANT3_AVG)
        RSSI_AVG = max(set(get_rssi_list), key=get_rssi_list.count)
        logger.info('LINK_RATE:')
        logger.info(LINK_RATE_AVG)
        logger.info('RSSI_ANT0:')
        logger.info(RSSI_ANT0_AVG)
        logger.info('RSSI_ANT1:')
        logger.info(RSSI_ANT1_AVG)
        logger.info('RSSI_ANT2:')
        logger.info(RSSI_ANT2_AVG)
        logger.info('RSSI_ANT3:')
        logger.info(RSSI_ANT3_AVG)
        return LINK_RATE_AVG, RSSI_AVG, RSSI_ANT0_AVG, RSSI_ANT1_AVG, RSSI_ANT2_AVG, RSSI_ANT3_AVG

    def get_txcounts_marvellap(self, radio):
        if radio == '2.4g':
            test_radio = '1'
        else:
            test_radio = '0'
        self.ssh.exec_command(b'iwpriv wdev%sap0 setcmd "qstats txrate_histogram";dmesg -c > /tmp/txrssi' % test_radio.encode('ascii'))
        stdin, stdout, stderr = self.ssh.exec_command(b'cat /tmp/txrssi')
        result, err = stdout.read(), stderr.read()
        logger.debug(result.decode())
        logger.debug(err.decode())
        txcounts_result = result
        logger.debug(txcounts_result)
        return txcounts_result

    def get_rxcounts_marvellap(self, radio):
        if radio == '2.4g':
            test_radio = '1'
        else:
            test_radio = '0'
        self.ssh.exec_command(b'iwpriv wdev%sap0 setcmd "qstats rxrate_histogram";dmesg -c > /tmp/rxrssi' % test_radio.encode('ascii'))
        stdin, stdout, stderr = self.ssh.exec_command(b'cat /tmp/rxrssi')
        result, err = stdout.read(), stderr.read()
        logger.debug(result.decode())
        logger.debug(err.decode())
        rxcounts_result = result
        logger.debug(rxcounts_result)
        return rxcounts_result

    def get_noise_marvellap(self, radio):
        if radio == '2.4g':
            test_radio = '1'
        else:
            test_radio = '0'
        get_ant0noise_list = []
        get_ant1noise_list = []
        get_ant2noise_list = []
        get_ant3noise_list = []
        NOISE_ANT0_AVG = NOISE_ANT1_AVG = NOISE_ANT2_AVG = NOISE_ANT3_AVG = None
        self.ssh.exec_command(b'iwpriv wdev%s setcmd "getnf";dmesg -c' % test_radio.encode('ascii'))
        stdin, stdout, stderr = self.ssh.exec_command(
            b'iwpriv wdev%s setcmd "getnf";dmesg -c' % test_radio.encode('ascii'))
        result, err = stdout.read(), stderr.read()
        logger.debug(result.decode())
        logger.debug(err.decode())

        noise_result = result
        logger.debug(noise_result)
        get_ant0_noise = re.findall(b'noise:(.+)', noise_result)[0].split()[1].decode('utf-8')
        get_ant0noise_list.append(get_ant0_noise)
        logger.debug(get_ant0_noise)
        logger.debug(get_ant0noise_list)
        get_ant1_noise = re.findall(b'noise:(.+)', noise_result)[0].split()[3].decode('utf-8')
        get_ant1noise_list.append(get_ant1_noise)
        logger.debug(get_ant1_noise)
        logger.debug(get_ant1noise_list)
        get_ant2_noise = re.findall(b'noise:(.+)', noise_result)[0].split()[5].decode('utf-8')
        get_ant2noise_list.append(get_ant2_noise)
        logger.debug(get_ant2_noise)
        logger.debug(get_ant2noise_list)
        get_ant3_noise = re.findall(b'noise:(.+)', noise_result)[0].split()[7].decode('utf-8')
        get_ant3noise_list.append(get_ant3_noise)
        logger.debug(get_ant3_noise)
        logger.debug(get_ant3noise_list)
        sleep(1)
        NOISE_ANT0_AVG = max(set(get_ant0noise_list), key=get_ant0noise_list.count)
        NOISE_ANT1_AVG = max(set(get_ant1noise_list), key=get_ant1noise_list.count)
        NOISE_ANT2_AVG = max(set(get_ant2noise_list), key=get_ant2noise_list.count)
        NOISE_ANT3_AVG = max(set(get_ant3noise_list), key=get_ant3noise_list.count)
        logger.info('NOISE_ANT0:')
        logger.info(NOISE_ANT0_AVG)
        logger.info('NOISE_ANT1:')
        logger.info(NOISE_ANT1_AVG)
        logger.info('NOISE_ANT2:')
        logger.info(NOISE_ANT2_AVG)
        logger.info('NOISE_ANT3:')
        logger.info(NOISE_ANT3_AVG)
        return NOISE_ANT0_AVG, NOISE_ANT1_AVG, NOISE_ANT2_AVG, NOISE_ANT3_AVG

    def close(self):
        if self.ssh is not None:
            self.ssh.close()
            self.ssh = None


class product_RSSI_com:
    """
        for serial connect
        """

    def __init__(self, com, baudrate):
        """
        param, timeout must set if use readline() or readlines()
        :param com:
        :param baudrate:
        """
        self.com = com
        self.baudrate = baudrate
        self.sn = serial.Serial(self.com, self.baudrate)
        self.sn.timeout = 0.5

    def close(self):
        if self.sn is not None:
            self.sn.close()
            self.sn = None

    def login(self, username, password):
        """

        :param username:
        :param password:
        :return:
        """
        if username is not None:
            self.sn.read_until(b'Login: ')
            self.sn.write(username.encode('ascii') + b'\n')
        if password is not None:
            self.sn.read_until(b'Password:')
            self.sn.write(password.encode('ascii') + b'\n')

        command_result = self.sn.readlines()
        for result in command_result:
            logger.debug(result.strip().decode('utf-8'))
        if 'wrong' not in command_result:
            logging.info('%s Sign up' % username)
            return True
        else:
            logging.warning('%s Login Fail' % username)
            return False

    def init(self, str1, str2, str3, str4):
        """
        additional command if you need to excite
        :param str1:
        :param str2:
        :param str3:
        :return:
        """
        self.sn.write(b'\r\n')
        self.sn.write(str1.encode('ascii') + b'\r\n')
        self.sn.write(str2.encode('ascii') + b'\r\n')
        self.sn.write(str3.encode('ascii') + b'\r\n')
        self.sn.write(str4.encode('ascii') + b'\r\n')
        command_result = self.sn.readlines()
        for result in command_result:
            logger.debug(result.strip().decode('utf-8'))

    def get_testradio_hi(self):
        get_band_list = []
        band_list = []
        self.sn.write(b'ifconfig\r\n')
        command_result = self.sn.readlines()
        for result in command_result:
            logger.debug(result)
            get_band = str(re.findall(b'vap(\d+)', result))
            logger.debug(get_band)
            get_band_list.append(get_band)
            logger.debug(get_band_list)
        for bd in get_band_list:
            logger.debug(bd)
            for band in bd:
                if band[0].isdigit() is True:
                    band_list.append(band[0])
        logger.debug(band_list)
        self.sn.write(b'./iwpriv vap%s get_channel\r\n' % band_list[0].encode('ascii'))
        command_result = self.sn.readlines()
        logger.debug(command_result)
        for result in command_result:
            logger.debug(result)
        channel = command_result[1]
        logger.debug(channel)
        channel = re.findall(b'get_channel:(\d+)', channel)[0].decode('utf-8')
        logger.debug(channel)
        if int(channel) < 30:
            radio_2g = band_list[0]
            radio_5g = band_list[1]
        else:
            radio_2g = band_list[1]
            radio_5g = band_list[0]
        return channel, radio_2g, radio_5g

    def get_sta_mac(self, radio, radio_2g, radio_5g):
        if radio == '2.4g':
            radio_value = radio_2g
        elif radio == '5g':
            radio_value = radio_5g
        else:
            logger.error('Radio type is wrong')
            radio_value = None
        self.sn.write(b'./iwpriv vap%s get_sta_info\r\n' % radio_value.encode('ascii'))
        command_result = self.sn.readlines()
        for result in command_result:
            logger.debug(result)
        sta_mac = command_result[5]
        logger.debug(sta_mac)
        sta_mac = re.findall(b'MAC ADDR: (.+)', sta_mac)[0].decode('utf-8')
        logger.debug(sta_mac)
        return sta_mac

    def get_txlinkrate(self, radio, radio_2g, radio_5g):
        if radio == '2.4g':
            radio_value = radio_2g
        elif radio == '5g':
            radio_value = radio_5g
        else:
            logger.error('Radio type is wrong')
            radio_value = None
        TXRATE_AVG = None
        get_txrate_list = []
        for i in range(10):
            self.sn.write(b'./iwpriv vap%s get_sta_info\r\n' % radio_value.encode('ascii'))
            command_result = self.sn.readlines()
            for result in command_result:
                logger.debug(result)
            tx_linkrate = command_result[6]
            logger.debug(tx_linkrate)
            tx_linkrate = re.findall(b'TX rate: (\d+)kbps', tx_linkrate)[0].decode('utf-8')
            logger.debug(tx_linkrate)
            get_txrate_list.append(tx_linkrate)
        TXRATE_AVG = max(set(get_txrate_list), key=get_txrate_list.count)
        TXRATE_AVG = int(TXRATE_AVG)/1000
        logger.debug(TXRATE_AVG)
        return TXRATE_AVG

    def get_rxlinkrate(self, radio, radio_2g, radio_5g):
        if radio == '2.4g':
            radio_value = radio_2g
        elif radio == '5g':
            radio_value = radio_5g
        else:
            logger.error('Radio type is wrong')
            radio_value = None
        RXRATE_AVG = None
        get_rxrate_list = []
        for i in range(10):
            self.sn.write(b'./iwpriv vap%s get_sta_info\r\n' % radio_value.encode('ascii'))
            command_result = self.sn.readlines()
            for result in command_result:
                logger.debug(result)
            rx_linkrate = command_result[7]
            logger.debug(rx_linkrate)
            rx_linkrate = re.findall(b'RX rate: (\d+)kbps', rx_linkrate)[0].decode('utf-8')
            logger.debug(rx_linkrate)
            get_rxrate_list.append(rx_linkrate)
        RXRATE_AVG = max(set(get_rxrate_list), key=get_rxrate_list.count)
        RXRATE_AVG = int(RXRATE_AVG) / 1000
        logger.debug(RXRATE_AVG)
        return RXRATE_AVG

    def get_aprssi(self, radio, radio_2g, radio_5g):
        if radio == '2.4g':
            radio_value = radio_2g
        elif radio == '5g':
            radio_value = radio_5g
        else:
            logger.error('Radio type is wrong')
            radio_value = None
        AP_RSSI_AVG = None
        get_aprssi_list = []
        get_ant0rssi_list = []
        get_ant1rssi_list = []
        for i in range(10):
            self.sn.write(b'./iwpriv vap%s get_ant_rssi\r\n' % radio_value.encode('ascii'))
            command_result = self.sn.readlines()
            for result in command_result:
                logger.debug(result)
            ap_rssi = command_result[1]
            logger.debug(ap_rssi)
            ap_rssi_ant0 = re.findall(b'ant1 RSSI: (-\d+)', ap_rssi)[0].decode('utf-8')
            ap_rssi_ant1 = re.findall(b'ant2 RSSI: (-\d+)', ap_rssi)[0].decode('utf-8')
            logger.debug(ap_rssi_ant0)
            logger.debug(ap_rssi_ant1)
            ap_rssi_avg = (int(ap_rssi_ant0) + int(ap_rssi_ant1))/2
            get_aprssi_list.append(ap_rssi_avg)
            get_ant0rssi_list.append(ap_rssi_ant0)
            get_ant1rssi_list.append(ap_rssi_ant1)
        AP_RSSI_AVG = max(set(get_aprssi_list), key=get_aprssi_list.count)
        AP_RSSI0_AVG = max(set(get_ant0rssi_list), key=get_ant0rssi_list.count)
        AP_RSSI1_AVG = max(set(get_ant1rssi_list), key=get_ant1rssi_list.count)
        logger.debug(AP_RSSI_AVG)
        return AP_RSSI_AVG, AP_RSSI0_AVG, AP_RSSI1_AVG

    def get_starssi(self, radio, radio_2g, radio_5g, mac):
        if radio == '2.4g':
            radio_value = radio_2g
        elif radio == '5g':
            radio_value = radio_5g
        else:
            logger.error('Radio type is wrong')
            radio_value = None
        STA_RSSI_AVG = None
        get_starssi_list = []
        for i in range(10):
            self.sn.write(b'./iwpriv vap%s get_sta_rssi %s\r\n' % (radio_value.encode('ascii'), mac.encode('ascii')))
            command_result = self.sn.readlines()
            for result in command_result:
                logger.debug(result)
            sta_rssi = command_result[1]
            logger.debug(sta_rssi)
            sta_rssi = re.findall(b'vap0      get_sta_rssi:(\d+)', sta_rssi)[0].decode('utf-8')
            logger.debug(sta_rssi)
            get_starssi_list.append(sta_rssi)
        STA_RSSI_AVG = int(max(set(get_starssi_list), key=get_starssi_list.count)) - 96
        logger.debug(STA_RSSI_AVG)
        return STA_RSSI_AVG


if __name__ == '__main__':
    ### telnet
    ## bcm
    ap = product_RSSI_telnet('192.168.100.1', 'root', 'admin', '2.4g', '8245')
    ap.login('root', 'admin')
    radio_2g, radio_5g = ap.get_testradio_celeno()
    ap.get_RSSI_celeno('2.4g', radio_2g, radio_5g)
    #ap.close()
    ###serial
    # ap = product_RSSI_com('COM6', 9600)
    # ap.login('admin', 'Admin@huawei')
    # radio_2g, radio_5g = ap.get_testradio_hi()
    # # sta_mac = ap.get_sta_mac('0')
    # ap.get_txlinkrate('2.4g', radio_2g, radio_5g)
    # # ap.get_aprssi('0')
    # # ap.get_rxlinkrate('0')
    # # ap.get_starssi('0', sta_mac)
