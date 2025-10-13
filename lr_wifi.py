
class LrWifi:
    def __init__(self):
        self.foo = 'bar'

    def ResponseWifiGetNbResults(self):
        return 'wifi NBresults:' + str(self.ba_miso[1])

    def WifiGetNbResults(self):
        self.next_transfer_response = 1
        return 'WifiGetNbResults'

    def ResponseWifiReadResults(self):
        result_format = getattr(self, 'wifi_result_format', None)
        result_count = getattr(self, 'wifi_result_count', 0)

        if result_format is None:
            return 'WifiReadResults response ' + str(len(self.ba_miso) - 1) + ' bytes'

        data_len = len(self.ba_miso) - 1  # Exclude stat1 byte
        offset = 1  # Start after stat1

        if result_format == 1:  # BASIC_COMPLETE
            result_size = 22
            _str = f'WifiReadResults {result_count} results (basic): '
            for i in range(result_count):
                if offset + result_size > len(self.ba_miso):
                    break
                rssi = self.ba_miso[offset + 2]
                mac = ':'.join(f'{self.ba_miso[offset + 4 + j]:02x}' for j in range(6))
                _str += f'[RSSI=-{rssi/2:.0f}dBm MAC={mac}] '
                offset += result_size
            return _str.rstrip()

        elif result_format == 4:  # BASIC_MAC_TYPE_CHANNEL
            result_size = 9
            _str = f'WifiReadResults {result_count} results (mac/type/ch): '
            for i in range(result_count):
                if offset + result_size > len(self.ba_miso):
                    break
                channel = self.ba_miso[offset + 1] & 0x0F
                rssi = self.ba_miso[offset + 2]
                mac = ':'.join(f'{self.ba_miso[offset + 3 + j]:02x}' for j in range(6))
                _str += f'[CH={channel} RSSI=-{rssi/2:.0f}dBm MAC={mac}] '
                offset += result_size
            return _str.rstrip()

        else:
            return f'WifiReadResults response format={result_format}, {data_len} bytes'

    def WifiReadResults(self):
        _str = "index:" + str(self.ba_mosi[2])
        _str = _str +  " NbResults:" + str(self.ba_mosi[3])
        _format = self.ba_mosi[4]
        self.wifi_result_format = _format
        self.wifi_result_count = self.ba_mosi[3]
        _str = _str + ' format:'
        if _format == 1:
            _str = _str + "basic"
        elif _format == 4:
            _str = _str + "mac/type/ch"
        else:
            _str = _str + hex(_format)
        self.next_transfer_response = 1
        return 'WifiReadResults ' + _str

    def ResponseWifiReadCumulTimings(self):
        if len(self.ba_miso) < 17:  # Need stat1 + 16 bytes of data
            return 'WifiReadCumulTimings response (insufficient data)'

        rx_detection_us = int.from_bytes(bytearray(self.ba_miso[1:5]), 'big')
        rx_correlation_us = int.from_bytes(bytearray(self.ba_miso[5:9]), 'big')
        rx_capture_us = int.from_bytes(bytearray(self.ba_miso[9:13]), 'big')
        demodulation_us = int.from_bytes(bytearray(self.ba_miso[13:17]), 'big')

        total_us = rx_detection_us + rx_correlation_us + rx_capture_us + demodulation_us

        _str = 'WifiReadCumulTimings: '
        _str += f'detect={rx_detection_us}us '
        _str += f'corr={rx_correlation_us}us '
        _str += f'capt={rx_capture_us}us '
        _str += f'demod={demodulation_us}us '
        _str += f'total={total_us}us'

        return _str

    def WifiReadCumulTimings(self):
        self.next_transfer_response = 1
        return 'WifiReadCumulTimings'

    def WifiScan(self):
        signal_type_dict = {
            1: 'B',
            2: 'G',
            3: 'N',
            4: 'B_G_N'
        }
        scan_mode_dict = {
            1: 'BEACON',
            2: 'BEACON_AND_PKT',
            4: 'FULL_BEACON',
            5: 'UNTIL_SSID'
        }

        signal_type = self.ba_mosi[2]
        channels = int.from_bytes(bytearray(self.ba_mosi[3:5]), 'big')
        scan_mode = self.ba_mosi[5]
        max_results = self.ba_mosi[6]
        nb_scan_per_channel = self.ba_mosi[7]
        timeout_ms = int.from_bytes(bytearray(self.ba_mosi[8:10]), 'big')
        abort_on_timeout = self.ba_mosi[10]

        # Decode channel mask
        channel_list = []
        for i in range(14):
            if channels & (1 << i):
                channel_list.append(str(i + 1))
        channels_str = ','.join(channel_list) if channel_list else 'none'

        _str = 'WifiScan '
        _str += signal_type_dict.get(signal_type, f'?{signal_type}?') + ' '
        _str += f'ch:[{channels_str}] '
        _str += scan_mode_dict.get(scan_mode, f'mode{scan_mode}') + ' '
        _str += f'max:{max_results} '
        _str += f'scans/ch:{nb_scan_per_channel} '
        _str += f'timeout:{timeout_ms}ms '
        _str += 'abort' if abort_on_timeout else 'no-abort'

        return _str

    def WifiScanTimeLimit(self):
        signal_type_dict = {
            1: 'B',
            2: 'G',
            3: 'N',
            4: 'B_G_N'
        }
        scan_mode_dict = {
            1: 'BEACON',
            2: 'BEACON_AND_PKT',
            4: 'FULL_BEACON',
            5: 'UNTIL_SSID'
        }

        signal_type = self.ba_mosi[2]
        channels = int.from_bytes(bytearray(self.ba_mosi[3:5]), 'big')
        scan_mode = self.ba_mosi[5]
        max_results = self.ba_mosi[6]
        timeout_per_channel_ms = int.from_bytes(bytearray(self.ba_mosi[7:9]), 'big')
        timeout_per_scan_ms = int.from_bytes(bytearray(self.ba_mosi[9:11]), 'big')

        # Decode channel mask
        channel_list = []
        for i in range(14):
            if channels & (1 << i):
                channel_list.append(str(i + 1))
        channels_str = ','.join(channel_list) if channel_list else 'none'

        _str = 'WifiScanTimeLimit '
        _str += signal_type_dict.get(signal_type, f'?{signal_type}?') + ' '
        _str += f'ch:[{channels_str}] '
        _str += scan_mode_dict.get(scan_mode, f'mode{scan_mode}') + ' '
        _str += f'max:{max_results} '
        _str += f'timeout/ch:{timeout_per_channel_ms}ms '
        _str += f'timeout/scan:{timeout_per_scan_ms}ms'

        return _str

    def WifiCountryCode(self):
        channels = int.from_bytes(bytearray(self.ba_mosi[2:4]), 'big')
        max_results = self.ba_mosi[4]
        nb_scan_per_channel = self.ba_mosi[5]
        timeout_ms = int.from_bytes(bytearray(self.ba_mosi[6:8]), 'big')
        abort_on_timeout = self.ba_mosi[8]

        # Decode channel mask
        channel_list = []
        for i in range(14):
            if channels & (1 << i):
                channel_list.append(str(i + 1))
        channels_str = ','.join(channel_list) if channel_list else 'none'

        _str = 'WifiCountryCode '
        _str += f'ch:[{channels_str}] '
        _str += f'max:{max_results} '
        _str += f'scans/ch:{nb_scan_per_channel} '
        _str += f'timeout:{timeout_ms}ms '
        _str += 'abort' if abort_on_timeout else 'no-abort'

        return _str

    def WifiCountryCodeTimeLimit(self):
        channels = int.from_bytes(bytearray(self.ba_mosi[2:4]), 'big')
        max_results = self.ba_mosi[4]
        timeout_per_channel_ms = int.from_bytes(bytearray(self.ba_mosi[5:7]), 'big')
        timeout_per_scan_ms = int.from_bytes(bytearray(self.ba_mosi[7:9]), 'big')

        # Decode channel mask
        channel_list = []
        for i in range(14):
            if channels & (1 << i):
                channel_list.append(str(i + 1))
        channels_str = ','.join(channel_list) if channel_list else 'none'

        _str = 'WifiCountryCodeTimeLimit '
        _str += f'ch:[{channels_str}] '
        _str += f'max:{max_results} '
        _str += f'timeout/ch:{timeout_per_channel_ms}ms '
        _str += f'timeout/scan:{timeout_per_scan_ms}ms'

        return _str

    def WifiResetCumulTimings(self):
        return 'WifiResetCumulTimings'

    def ResponseWifiGetNbCountryCodeResults(self):
        nb_results = self.ba_miso[1]
        return f'WifiGetNbCountryCodeResults nb={nb_results}'

    def WifiGetNbCountryCodeResults(self):
        self.next_transfer_response = 1
        return 'WifiGetNbCountryCodeResults (request)'

    def ResponseWifiReadCountryCodeResults(self):
        data_len = len(self.ba_miso) - 1  # Exclude stat1 byte
        result_size = 10  # Each country code result is 10 bytes
        nb_results = data_len // result_size

        if nb_results == 0:
            return 'WifiReadCountryCodeResults (no results)'

        _str = f'WifiReadCountryCodeResults {nb_results} results: '
        offset = 1  # Start after stat1

        for i in range(nb_results):
            if offset + result_size > len(self.ba_miso):
                break

            # Extract fields
            country_code_0 = chr(self.ba_miso[offset + 0]) if 32 <= self.ba_miso[offset + 0] <= 126 else '?'
            country_code_1 = chr(self.ba_miso[offset + 1]) if 32 <= self.ba_miso[offset + 1] <= 126 else '?'
            io_regulation = self.ba_miso[offset + 2]
            channel_info = self.ba_miso[offset + 3]

            # MAC address is in reverse order (bytes 4-9)
            mac = ':'.join(f'{self.ba_miso[offset + 9 - j]:02x}' for j in range(6))

            _str += f'[{country_code_0}{country_code_1} IO={io_regulation} CH=0x{channel_info:02x} MAC={mac}] '
            offset += result_size

        return _str.rstrip()

    def ResponseWifiReadVersion(self):
        major = self.ba_miso[1]
        minor = self.ba_miso[2]
        return f'WifiReadVersion v{major}.{minor}'

    cmdResponseDict = {
        0x0305: ResponseWifiGetNbResults,
        0x0306: ResponseWifiReadResults,
        0x0308: ResponseWifiReadCumulTimings,
        0x0309: ResponseWifiGetNbCountryCodeResults,
        0x030a: ResponseWifiReadCountryCodeResults,
        0x0320: ResponseWifiReadVersion,
    }

    def WifiReadCountryCodeResults(self):
        self.next_transfer_response = 1
        start_index = self.ba_mosi[2]
        nb_results = self.ba_mosi[3]
        return f'WifiReadCountryCodeResults index={start_index} nb={nb_results}'

    def WifiCfgTimestampAPphone(self):
        ts = int.from_bytes(bytearray(self.ba_mosi[2:6]), 'big')
        return 'WifiCfgTimestampAPphone ' + str(ts) + ' seconds'

    def WifiReadVersion(self):
        self.next_transfer_response = 1
        return 'WifiReadVersion (request)'

    cmdDict = {
        0x0300: WifiScan, # LR11XX_WIFI_SCAN_OC
        0x0301: WifiScanTimeLimit, # 
        0x0302: WifiCountryCode, # LR11XX_WIFI_SEARCH_COUNTRY_CODE_OC
        0x0303: WifiCountryCodeTimeLimit, # LR11XX_WIFI_COUNTRY_CODE_TIME_LIMIT_OC
        0x0305: WifiGetNbResults, # LR11XX_WIFI_GET_RESULT_SIZE_OC
        0x0306: WifiReadResults, # LR11XX_WIFI_READ_RESULT_OC
        0x0307: WifiResetCumulTimings, # LR11XX_WIFI_RESET_CUMUL_TIMING_OC
        0x0308: WifiReadCumulTimings, # LR11XX_WIFI_READ_CUMUL_TIMING_OC
        0x0309: WifiGetNbCountryCodeResults, # LR11XX_WIFI_GET_SIZE_COUNTRY_RESULT_OC
        0x030a: WifiReadCountryCodeResults, # LR11XX_WIFI_READ_COUNTRY_CODE_OC
        0x030b: WifiCfgTimestampAPphone, # LR11XX_WIFI_CONFIGURE_TIMESTAMP_AP_PHONE_OC
        0x0320: WifiReadVersion, # LR11XX_WIFI_GET_VERSION_OC
    }
