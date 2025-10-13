
class LrGnss:
    def __init__(self):
        self.foo = 'bar'

    def gnss_scan(self, label):
        time = int.from_bytes(bytearray(self.ba_mosi[2:6]), 'big')
        effort = self.ba_mosi[6]
        if effort == 0:
            estr = 'lowPower'
        elif effort == 1:
            estr = 'bestEffort'
        else:
            estr = '?' + hex(effort) + '?'
        resultMask = self.ba_mosi[7]
        nbSvMax = self.ba_mosi[8]
        return label + ' ' + str(time) + ' ' + estr + ' resultMask=' + hex(resultMask) + ' nbSvMax=' + str(nbSvMax)

    def GnssSetConstellationToUse(self):
        bit_mask = self.ba_mosi[2]
        _str = 'GnssSetConstellationToUse '
        if bit_mask & 1:
            _str = _str + 'GPS '
        if bit_mask & 2:
            _str = _str + 'BeiDou '
        return _str

    def ResponseGnssReadConstellationToUse(self):
        bit_mask = self.ba_miso[1]
        _str = 'GnssReadConstellationToUse '
        if bit_mask & 1:
            _str = _str + 'GPS '
        if bit_mask & 2:
            _str = _str + 'BeiDou '
        if bit_mask == 0:
            _str = _str + '(none)'
        return _str.rstrip()

    def GnssReadConstellationToUse(self):
        self.next_transfer_response = 1
        return 'GnssReadConstellationToUse (request)'

    def GnssSetAlmanacUpdate(self):
        bit_mask = self.ba_mosi[2]
        _str = 'GnssSetAlmanacUpdate '
        if bit_mask & 1:
            _str = _str + 'GPS '
        if bit_mask & 2:
            _str = _str + 'BeiDou '
        if bit_mask == 0:
            _str = _str + '(none)'
        return _str.rstrip()

    def ResponseGnssReadAlmanacUpdate(self):
        bit_mask = self.ba_miso[1]
        _str = 'GnssReadAlmanacUpdate '
        if bit_mask & 1:
            _str = _str + 'GPS '
        if bit_mask & 2:
            _str = _str + 'BeiDou '
        if bit_mask == 0:
            _str = _str + '(none)'
        return _str.rstrip()

    def GnssReadAlmanacUpdate(self):
        self.next_transfer_response = 1
        return 'GnssReadAlmanacUpdate (request)'

    def GnssSetFreqSearchSpace(self):
        return 'GnssSetFreqSearchSpace TODO'

    def GnssReadFreqSearchSpace(self):
        return 'GnssReadFreqSearchSpace TODO'

    def ResponseGnssReadVersion(self):
        gnss_firmware = self.ba_miso[1]
        gnss_almanac = self.ba_miso[2]
        return f'GnssReadVersion firmware=0x{gnss_firmware:02x} almanac=0x{gnss_almanac:02x}'

    def GnssReadVersion(self):
        self.next_transfer_response = 1
        return 'GnssReadVersion (request)'

    def GnssReadSupportedConstellations(self):
        return 'GnssReadSupportedConstellations TODO'

    def GnssSetMode(self):
        scan_mode_dict = {
            0x00: 'SINGLE_SCAN_LEGACY',
            0x03: 'SINGLE_SCAN_AND_5_FAST_SCANS'
        }
        scan_mode = self.ba_mosi[2]
        scan_mode_str = scan_mode_dict.get(scan_mode, f'UNKNOWN_0x{scan_mode:02x}')
        return f'GnssSetMode {scan_mode_str}'

    def GnssAutonomous(self):
        return self.gnss_scan('GnssAutonomous')

    def GnssAssisted(self):
        return self.gnss_scan('GnssAssisted')

    def GnssScan(self):
        effort = self.ba_mosi[2]
        resultMask = self.ba_mosi[3]
        NbSvMax = self.ba_mosi[4]
        _str = 'effort '
        if effort == 0:
            _str = _str + 'low'
        elif effort == 1:
            _str = _str + 'middle'
        else:
            _str = _str + hex(effort)
        _str = _str + ' resultMask:' + hex(resultMask)
        _str = _str + ' NbSvMax:' + str(NbSvMax)
        return 'GnssScan ' + _str

    def ResponseGnssGetResultSize(self):
        return 'GetResultSize ' + str(int.from_bytes(bytearray(self.ba_miso[1:3]), 'big'))

    def GnssGetResultSize(self):
        self.next_transfer_response = 1
        return 'GnssGetResultSize'

    def ResponseGnssReadResults(self):
        return 'GnssReadResults TODO'

    def GnssReadResults(self):
        self.next_transfer_response = 1
        return 'GnssReadResults'

    def GnssAlmanacFullUpdate(self):
        _len = len(self.ba_mosi) - 2
        block_size = 20
        return 'GnssAlmanacFullUpdate _len ' + str(_len) + ', blocks ' + str(_len/block_size)

    def ResponseGnssAlmanacRead(self):
        address = int.from_bytes(bytearray(self.ba_miso[1:5]), 'big')
        size = int.from_bytes(bytearray(self.ba_miso[5:7]), 'big')
        return 'GnssAlmanacRead address ' + hex(address) + ', size ' + hex(size)

    def GnssAlmanacRead(self):
        self.next_transfer_response = 1
        return 'GnssAlmanacRead (request)'

    def GnssSetAssistancePosition(self):
        _lat = int.from_bytes(bytearray(self.ba_mosi[2:4]), 'big')
        lat = _lat / (2048/90)
        _lon = int.from_bytes(bytearray(self.ba_mosi[4:6]), 'big')
        if _lon > 0x7fff:
            _lon -= 0x10000
        lon = _lon / (2048/180)
        return 'GnssSetAssistancePosition ' + str(lat) + ', ' + str(lon)

    def ResponseGnssReadAssistancePosition(self):
        _lat = int.from_bytes(bytearray(self.ba_miso[1:3]), 'big')
        lat = _lat / (2048/90)
        _lon = int.from_bytes(bytearray(self.ba_miso[3:5]), 'big')
        if _lon > 0x7fff:
            _lon -= 0x10000
        lon = _lon / (2048/180)
        return 'assistance position ' + str(lat) + ', ' + str(lon)

    def GnssReadAssistancePosition(self):
        self.next_transfer_response = 1
        return 'GnssReadAssistancePosition'

    def GnssPushSolverMsg(self):
        data_len = len(self.ba_mosi) - 2  # Exclude 2-byte opcode
        return f'GnssPushSolverMsg {data_len} bytes'

    def GnssPushDmMsg(self):
        data_len = len(self.ba_mosi) - 2  # Exclude 2-byte opcode
        return f'GnssPushDmMsg {data_len} bytes'

    def ResponseGnssGetContextStatus(self):
        if len(self.ba_miso) < 10:  # Need stat1 + 9 bytes of context status
            return 'GnssGetContextStatus (insufficient data)'

        # Parse context status (9 bytes after stat1)
        firmware_version = self.ba_miso[3]

        # Global almanac CRC (32-bit little-endian)
        global_almanac_crc = int.from_bytes(bytearray(self.ba_miso[4:8]), 'little')

        # Byte 8 contains error code and flags
        byte_8 = self.ba_miso[8]
        error_code = byte_8 >> 4  # Upper 4 bits
        almanac_update_gps = (byte_8 & 0x02) != 0  # Bit 1
        almanac_update_beidou = (byte_8 & 0x04) != 0  # Bit 2
        freq_msb = byte_8 & 0x01  # Bit 0

        # Byte 9 contains LSB of frequency search space
        byte_9 = self.ba_miso[9]
        freq_lsb = (byte_9 & 0x80) >> 7  # Bit 7
        freq_search_space = (freq_msb << 1) | freq_lsb

        # Error code dictionary
        error_code_dict = {
            0: 'NO_ERROR',
            1: 'ALMANAC_TOO_OLD',
            2: 'UPDATE_CRC_MISMATCH',
            3: 'UPDATE_FLASH_INTEGRITY',
            4: 'ALMANAC_UPDATE_NOT_ALLOWED'
        }
        error_str = error_code_dict.get(error_code, f'UNKNOWN_{error_code}')

        # Frequency search space dictionary
        freq_dict = {
            0: '250Hz',
            1: '500Hz',
            2: '1kHz',
            3: '2kHz'
        }
        freq_str = freq_dict.get(freq_search_space, f'UNKNOWN_{freq_search_space}')

        # Build almanac update string
        almanac_strs = []
        if almanac_update_gps:
            almanac_strs.append('GPS')
        if almanac_update_beidou:
            almanac_strs.append('BeiDou')
        almanac_str = ','.join(almanac_strs) if almanac_strs else 'none'

        _str = 'GnssGetContextStatus: '
        _str += f'fw=0x{firmware_version:02x} '
        _str += f'almanac_crc=0x{global_almanac_crc:08x} '
        _str += f'error={error_str} '
        _str += f'alm_update={almanac_str} '
        _str += f'freq={freq_str}'

        return _str

    def GnssGetContextStatus(self):
        self.next_transfer_response = 1
        return 'GnssGetContextStatus'

    def ResponseGnssGetNbSvDetected(self):
        return 'GnssGetNbSvDetected ' + str(self.ba_miso[1])

    def GnssGetNbSvDetected(self):
        self.next_transfer_response = 1
        return 'GnssGetNbSvDetected'

    def ResponseGnssGetSvDetected(self):
        data_len = len(self.ba_miso) - 1  # Exclude stat1 byte
        sv_length = 4  # Each satellite: 1 byte ID + 1 byte CNR + 2 bytes doppler
        nb_satellites = data_len // sv_length

        if nb_satellites == 0:
            return 'GnssGetSvDetected (no satellites)'

        _str = f'GnssGetSvDetected {nb_satellites} SVs: '
        offset = 1  # Start after stat1

        for i in range(nb_satellites):
            if offset + sv_length > len(self.ba_miso):
                break

            satellite_id = self.ba_miso[offset]
            cnr_raw = self.ba_miso[offset + 1]
            cnr = cnr_raw + 31  # LR11XX_GNSS_SNR_TO_CNR_OFFSET
            doppler_raw = int.from_bytes(bytearray(self.ba_miso[offset + 2:offset + 4]), 'big')
            # Convert to signed 16-bit
            if doppler_raw > 0x7fff:
                doppler = doppler_raw - 0x10000
            else:
                doppler = doppler_raw

            _str += f'[SV{satellite_id} CNR={cnr}dB dop={doppler}Hz] '
            offset += sv_length

        return _str.rstrip()

    def GnssGetSvDetected(self):
        self.next_transfer_response = 1
        return 'GnssGetSvDetected'

    def ResponseGnssReadAlmanacPerSatellite(self):
        data_len = len(self.ba_miso) - 1  # Exclude stat1 byte
        almanac_size = 22  # Each almanac is 22 bytes
        nb_almanacs = data_len // almanac_size

        if nb_almanacs == 0:
            return 'GnssReadAlmanacPerSatellite (no almanacs)'

        return f'GnssReadAlmanacPerSatellite {nb_almanacs} almanacs, {data_len} bytes'

    def GnssReadAlmanacPerSatellite(self):
        sv_id_init = self.ba_mosi[2]
        n_sv = self.ba_mosi[3]
        self.next_transfer_response = 1
        return f'GnssReadAlmanacPerSatellite sv_id={sv_id_init} n_sv={n_sv}'

    def GnssGetSvVisible(self):
        return 'GnssGetSvVisible TODO'

    def GnssGetSvVisibleDoppler(self):
        return 'GnssGetSvVisibleDoppler TODO'

    def ResponseGnssReadLastScanModeLaunched(self):
        lsm = self.ba_miso[1]
        _str = 'last scan mode: '
        if lsm == 3:
            _str = _str + 'assisted'
        elif lsm == 4:
            _str = _str + 'cold start, no time'
        elif lsm == 5:
            _str = _str + 'cold start, with time'
        elif lsm == 6:
            _str = _str + 'fetchtime or 2d'
        elif lsm == 7:
            _str = _str + 'almanac update command, no save'
        elif lsm == 8:
            _str = _str + 'keep sync'
        elif lsm == 9:
            _str = _str + 'almanac update command, 1 saved'
        elif lsm == 10:
            _str = _str + 'almanac update command, 2 saved'
        else:
            _str = _str + '0x'+hex(lsm)
        return _str

    def GnssReadLastScanModeLaunched(self):
        self.next_transfer_response = 1
        return 'GnssReadLastScanModeLaunched'

    def GnssFetchTime(self):
        effort_mode_dict = {
            0x00: 'LOW_EFFORT',
            0x01: 'MID_EFFORT',
            0x02: 'HIGH_EFFORT'
        }
        option_dict = {
            0: 'SEARCH_TOW',
            1: 'SEARCH_TOW_WN',
            2: 'SEARCH_TOW_WN_ROLLOVER'
        }
        effort_mode = self.ba_mosi[2]
        option = self.ba_mosi[3]
        effort_str = effort_mode_dict.get(effort_mode, f'UNKNOWN_0x{effort_mode:02x}')
        option_str = option_dict.get(option, f'UNKNOWN_0x{option:02x}')
        return f'GnssFetchTime effort={effort_str} option={option_str}'

    def ResponseGnssReadTime(self):
        error_code_dict = {
            0: 'NO_ERROR',
            1: '32K_STOPPED',
            2: 'WN_TOW_NOT_SET'
        }
        error_code = self.ba_miso[1]
        gps_time_s = int.from_bytes(bytearray(self.ba_miso[2:6]), 'big')
        nb_us_in_s_raw = int.from_bytes(bytearray(self.ba_miso[6:9]), 'big')
        nb_us_in_s = nb_us_in_s_raw // 16
        time_accuracy_raw = int.from_bytes(bytearray(self.ba_miso[9:13]), 'big')
        time_accuracy = time_accuracy_raw // 16
        error_str = error_code_dict.get(error_code, f'UNKNOWN_0x{error_code:02x}')
        return f'GnssReadTime error={error_str} gps_time_s={gps_time_s} nb_us_in_s={nb_us_in_s} time_accuracy={time_accuracy}'

    def GnssReadTime(self):
        self.next_transfer_response = 1
        return 'GnssReadTime'

    def GnssResetTime(self):
        return 'GnssResetTime' # no arguments, no response

    def GnssResetPosition(self):
        return 'GnssResetPosition' # no arguments, no response

    def ResponseGnssReadWeekNumberRollover(self):
        status_dict = {
            0: 'NEVER_SET',
            1: 'SET_BY_SCAN'
        }
        wn_rollover_status = self.ba_miso[1]
        wn_number_rollover = self.ba_miso[2]

        status_str = status_dict.get(wn_rollover_status, f'UNKNOWN_0x{wn_rollover_status:02x}')
        return f'GnssReadWeekNumberRollover status={status_str} wn={wn_number_rollover}'

    def GnssReadWeekNumberRollover(self):
        self.next_transfer_response = 1
        return 'GnssReadWeekNumberRollover (request)'

    def ResponseGnssReadDemodStatus(self):
        if len(self.ba_miso) < 3:  # Need stat1 + 2 bytes
            return 'GnssReadDemodStatus (insufficient data)'

        # Parse demod_status (signed 8-bit)
        demod_status_raw = self.ba_miso[1]
        if demod_status_raw > 127:
            demod_status = demod_status_raw - 256
        else:
            demod_status = demod_status_raw

        # Demod status dictionary
        demod_status_dict = {
            -21: 'NO_DEMOD_BDS_ALMANAC_SV31_43',
            -20: 'SV_SELECTED_FOR_DEMOD_LOST',
            -19: 'ALMANAC_DEMOD_ERROR',
            -18: 'WAKE_UP_AFTER_PREAMBLE',
            -17: '20MS_REAL_TIME_FAILURE',
            -16: 'WAKE_UP_SYNC_FAILURE',
            -15: 'WEEK_NUMBER_NOT_VALIDATED',
            -14: 'NO_ACTIVATED_SAT_IN_SV_LIST',
            -13: 'SLEEP_TIME_TOO_LONG',
            -12: 'WRONG_TIME_OF_WEEK_DEMOD',
            -11: 'PREAMBLE_NOT_VALIDATED',
            -10: 'DEMOD_DISABLE',
            -9: 'DEMOD_EXTRACTION_FAILURE',
            -8: 'NO_BIT_CHANGE_FOUND_DURING_START_DEMOD',
            -7: 'NO_BIT_CHANGE_FOUND_DURING_MULTISCAN',
            -6: 'NO_SAT_FOUND',
            -5: 'WORD_SYNC_LOST',
            -3: 'NOT_ENOUGH_PARITY_CHECK_FOUND',
            -2: 'TOO_MANY_PARITY_CHECK_FOUND',
            -1: 'NO_PARITY_CHECK_FOUND',
            0: 'WORD_SYNC_SEARCH_NOT_STARTED',
            1: 'WORD_SYNC_POTENTIALLY_FOUND',
            2: 'WORD_SYNC_FOUND',
            3: 'TIME_OF_WEEK_FOUND',
            4: 'WEEK_NUMBER_FOUND',
            5: 'ALMANAC_FOUND_BUT_NO_SAVED',
            6: 'HALF_ALMANAC_FOUND_AND_SAVED',
            7: 'ALMANAC_FOUND_AND_SAVED'
        }

        # Parse demod_info flags (byte 2)
        demod_info = self.ba_miso[2]
        word_sync_found = (demod_info & 0x01) != 0
        first_tow_found = (demod_info & 0x02) != 0
        wn_demodulated = (demod_info & 0x04) != 0
        wn_found = (demod_info & 0x08) != 0
        sub1_found = (demod_info & 0x10) != 0
        sub4_found = (demod_info & 0x20) != 0

        status_str = demod_status_dict.get(demod_status, f'UNKNOWN_{demod_status}')

        # Build flags string
        flags = []
        if word_sync_found:
            flags.append('word_sync')
        if first_tow_found:
            flags.append('first_tow')
        if wn_demodulated:
            flags.append('wn_demod')
        if wn_found:
            flags.append('wn_found')
        if sub1_found:
            flags.append('sub1')
        if sub4_found:
            flags.append('sub4')
        flags_str = ','.join(flags) if flags else 'none'

        return f'GnssReadDemodStatus: {status_str} flags=[{flags_str}]'

    def GnssReadDemodStatus(self):
        self.next_transfer_response = 1
        return 'GnssReadDemodStatus'

    def ResponseGnssReadCumulTiming(self):
        if len(self.ba_miso) < 125:  # Need stat1 + 124 bytes of data
            return 'GnssReadCumulTiming response (insufficient data)'

        # Helper to read 32-bit values (big-endian)
        def read_u32(offset):
            return int.from_bytes(bytearray(self.ba_miso[offset:offset+4]), 'big')

        # Read key timing values (all in microseconds)
        total_capture = read_u32(101)
        total_process = read_u32(105)
        total_sleep_32k = read_u32(109)
        total_sleep_32m = read_u32(113)
        total = read_u32(117)

        # Optional: read GPS/BeiDou breakdown
        total_gps = read_u32(77)
        total_beidou = read_u32(97)

        _str = 'GnssReadCumulTiming: '
        _str += f'capt={total_capture}us '
        _str += f'proc={total_process}us '
        _str += f'slp32k={total_sleep_32k}us '
        _str += f'slp32m={total_sleep_32m}us '
        _str += f'GPS={total_gps}us '
        _str += f'BeiDou={total_beidou}us '
        _str += f'total={total}us'

        # more detailed result omitted, see lr11xx_gnss_read_cumulative_timing() in lr11xx_gnss.c
        return _str

    def GnssReadCumulTiming(self):
        self.next_transfer_response = 1
        return 'GnssReadCumulTiming'

    def GnssSetTime(self):
        gps_time_s = int.from_bytes(bytearray(self.ba_mosi[2:6]), 'big')
        time_accuracy = int.from_bytes(bytearray(self.ba_mosi[6:8]), 'big')
        return f'GnssSetTime gps_time={gps_time_s}s accuracy={time_accuracy}'

    def GnssConfigDelayResetAP(self):
        delay = int.from_bytes(bytearray(self.ba_mosi[2:5]), 'big')
        return f'GnssConfigDelayResetAP delay={delay}'

    def ResponseGnssReadDelayResetAP(self):
        if len(self.ba_miso) < 4:  # Need stat1 + 3 bytes
            return 'GnssReadDelayResetAP (insufficient data)'

        # Parse 24-bit delay value (3 bytes, big-endian)
        delay = (self.ba_miso[1] << 16) | (self.ba_miso[2] << 8) | self.ba_miso[3]

        return f'GnssReadDelayResetAP: delay={delay}'

    def GnssReadDelayResetAP(self):
        self.next_transfer_response = 1
        return 'GnssReadDelayResetAP'

    def ResponseGnssReadKeepSyncStatus(self):
        if len(self.ba_miso) < 6:  # Need stat1 + 5 bytes
            return 'GnssReadKeepSyncStatus (insufficient data)'

        nb_visible_sat = self.ba_miso[1]
        time_elapsed = int.from_bytes(bytearray(self.ba_miso[2:6]), 'big')

        return f'GnssReadKeepSyncStatus: nb_visible_sat={nb_visible_sat} time_elapsed={time_elapsed}s'

    def GnssReadKeepSyncStatus(self):
        constellation_mask = self.ba_mosi[2]

        # Parse constellation mask
        constellation_strs = []
        if constellation_mask & 0x01:
            constellation_strs.append('GPS')
        if constellation_mask & 0x02:
            constellation_strs.append('BeiDou')
        constellation_str = ','.join(constellation_strs) if constellation_strs else f'0x{constellation_mask:02x}'

        self.next_transfer_response = 1
        return f'GnssReadKeepSyncStatus constellation={constellation_str}'

    def ResponseGnssReadAlmanacStatus(self):
        if len(self.ba_miso) < 54:  # Need stat1 + 53 bytes
            return 'GnssReadAlmanacStatus (insufficient data)'

        # Status dictionary
        status_dict = {
            -4: 'INTERNAL_ACCURACY_TOO_LOW',
            -3: 'NO_TIME_SET',
            -2: 'IMPOSSIBLE_TO_FIND_NEXT_TIME',
            -1: 'NO_PAGE_ID_KNOWN',
            0: 'NO_SAT_TO_UPDATE',
            1: 'AT_LEAST_ONE_SAT_MUST_BE_UPDATED'
        }

        # Parse GPS status (signed 8-bit)
        status_gps_raw = self.ba_miso[1]
        status_gps = status_gps_raw if status_gps_raw < 128 else status_gps_raw - 256
        status_gps_str = status_dict.get(status_gps, f'UNKNOWN_{status_gps}')

        # Parse GPS fields
        nb_sat_gps_to_update = self.ba_miso[10]

        # Parse BeiDou status (signed 8-bit)
        status_beidou_raw = self.ba_miso[19]
        status_beidou = status_beidou_raw if status_beidou_raw < 128 else status_beidou_raw - 256
        status_beidou_str = status_dict.get(status_beidou, f'UNKNOWN_{status_beidou}')

        # Parse BeiDou fields
        nb_sat_beidou_to_update = self.ba_miso[28]

        _str = 'GnssReadAlmanacStatus: '
        _str += f'GPS[{status_gps_str} nb_to_update={nb_sat_gps_to_update}] '
        _str += f'BeiDou[{status_beidou_str} nb_to_update={nb_sat_beidou_to_update}]'

        return _str

    def GnssReadAlmanacStatus(self):
        self.next_transfer_response = 1
        return 'GnssReadAlmanacStatus '

    def GnssConfigAlmanacUpdatePeriod(self):
        constellation_mask = self.ba_mosi[2]
        sv_type = self.ba_mosi[3]
        period = int.from_bytes(bytearray(self.ba_mosi[4:6]), 'big')

        # Parse constellation mask
        constellation_strs = []
        if constellation_mask & 0x01:
            constellation_strs.append('GPS')
        if constellation_mask & 0x02:
            constellation_strs.append('BeiDou')
        constellation_str = ','.join(constellation_strs) if constellation_strs else f'0x{constellation_mask:02x}'

        # Parse sv_type
        sv_type_dict = {
            0: 'MEO',
            1: 'IGSO'
        }
        sv_type_str = sv_type_dict.get(sv_type, f'UNKNOWN_0x{sv_type:02x}')

        return f'GnssConfigAlmanacUpdatePeriod constellation={constellation_str} sv_type={sv_type_str} period={period} days'

    def ResponseGnssReadAlmanacUpdatePeriod(self):
        period = int.from_bytes(bytearray(self.ba_miso[1:3]), 'big')
        return f'GnssReadAlmanacUpdatePeriod period={period} days'

    def GnssReadAlmanacUpdatePeriod(self):
        self.next_transfer_response = 1
        constellation_mask = self.ba_mosi[2]
        sv_type = self.ba_mosi[3]

        # Parse constellation mask
        constellation_strs = []
        if constellation_mask & 0x01:
            constellation_strs.append('GPS')
        if constellation_mask & 0x02:
            constellation_strs.append('BeiDou')
        constellation_str = ','.join(constellation_strs) if constellation_strs else f'0x{constellation_mask:02x}'

        # Parse sv_type
        sv_type_dict = {
            0: 'MEO',
            1: 'IGSO'
        }
        sv_type_str = sv_type_dict.get(sv_type, f'UNKNOWN_0x{sv_type:02x}')

        return f'GnssReadAlmanacUpdatePeriod constellation={constellation_str} sv_type={sv_type_str}'

    def ResponseGnssGetSvWarmStart(self):
        n_SVs = len(self.ba_miso) - 1 # first byte is stat1
        return 'GnssGetSvWarmStart ' + str(n_SVs) + ' SVs'

    def GnssGetSvWarmStart(self):
        self.next_transfer_response = 1
        constellation_mask = self.ba_mosi[2]
        return 'GnssGetSvWarmStart constellation_mask ' + str(constellation_mask)

    cmdResponseDict = {
        0x0401: ResponseGnssReadConstellationToUse,
        0x0403: ResponseGnssReadAlmanacUpdate,
        0x0406: ResponseGnssReadVersion,
        0x040c: ResponseGnssGetResultSize,
        0x040d: ResponseGnssReadResults,
        0x040f: ResponseGnssAlmanacRead,
        0x0411: ResponseGnssReadAssistancePosition,
        0x0416: ResponseGnssGetContextStatus,
        0x0417: ResponseGnssGetNbSvDetected,
        0x0418: ResponseGnssGetSvDetected,
        0x041a: ResponseGnssReadAlmanacPerSatellite,
        0x0426: ResponseGnssReadLastScanModeLaunched,
        0x0434: ResponseGnssReadTime,
        0x0438: ResponseGnssReadWeekNumberRollover,
        0x0439: ResponseGnssReadDemodStatus,
        0x044a: ResponseGnssReadCumulTiming,
        0x0453: ResponseGnssReadDelayResetAP,
        0x0456: ResponseGnssReadKeepSyncStatus,
        0x0457: ResponseGnssReadAlmanacStatus,
        0x0464: ResponseGnssReadAlmanacUpdatePeriod,
        0x0466: ResponseGnssGetSvWarmStart,
    }

    cmdDict = {
        0x0400: GnssSetConstellationToUse, # LR11XX_GNSS_SET_CONSTELLATION_OC
        0x0401: GnssReadConstellationToUse, # LR11XX_GNSS_READ_CONSTELLATION_OC
        0x0402: GnssSetAlmanacUpdate, # LR11XX_GNSS_SET_ALMANAC_UPDATE_OC
        0x0403: GnssReadAlmanacUpdate, # LR11XX_GNSS_READ_ALMANAC_UPDATE_OC
        0x0404: GnssSetFreqSearchSpace, # LR11XX_GNSS_SET_FREQ_SEARCH_SPACE_OC
        0x0405: GnssReadFreqSearchSpace, # LR11XX_GNSS_READ_FREQ_SEARCH_SPACE_OC
        0x0406: GnssReadVersion, # LR11XX_GNSS_READ_FW_VERSION_OC
        0x0407: GnssReadSupportedConstellations, # LR11XX_GNSS_READ_SUPPORTED_CONSTELLATION_OC
        0x0408: GnssSetMode, # LR11XX_GNSS_SET_SCAN_MODE_OC
        0x0409: GnssAutonomous, #
        0x040a: GnssAssisted, #
        0x040b: GnssScan, # LR11XX_GNSS_SCAN_OC
        0x040c: GnssGetResultSize, # LR11XX_GNSS_SCAN_GET_RES_SIZE_OC
        0x040d: GnssReadResults, # LR11XX_GNSS_SCAN_READ_RES_OC
        0x040E: GnssAlmanacFullUpdate, # LR11XX_GNSS_ALMANAC_UPDATE_OC
        0x040f: GnssAlmanacRead, # LR11XX_GNSS_ALMANAC_READ_OC
        0x0410: GnssSetAssistancePosition, # LR11XX_GNSS_SET_ASSISTANCE_POSITION_OC
        0x0411: GnssReadAssistancePosition, # LR11XX_GNSS_READ_ASSISTANCE_POSITION_OC
        0x0414: GnssPushSolverMsg, # LR11XX_GNSS_PUSH_SOLVER_MSG_OC
        0x0415: GnssPushDmMsg, # LR11XX_GNSS_PUSH_DM_MSG_OC
        0x0416: GnssGetContextStatus, # LR11XX_GNSS_GET_CONTEXT_STATUS_OC
        0x0417: GnssGetNbSvDetected, # LR11XX_GNSS_GET_NB_SATELLITES_OC
        0x0418: GnssGetSvDetected, # LR11XX_GNSS_GET_SATELLITES_OC
        0x041a: GnssReadAlmanacPerSatellite, # LR11XX_GNSS_READ_ALMANAC_PER_SATELLITE_OC
        0x041f: GnssGetSvVisible, # LR11XX_GNSS_GET_SV_VISIBLE_OC
        0x0420: GnssGetSvVisibleDoppler, # LR11XX_GNSS_GET_SV_VISIBLE_DOPPLER_OC
        0x0426: GnssReadLastScanModeLaunched, # LR11XX_GNSS_READ_LAST_SCAN_MODE_LAUNCHED_OC
        0x0432: GnssFetchTime, # LR11XX_GNSS_FETCH_TIME_OC
        0x0434: GnssReadTime, # LR11XX_GNSS_READ_TIME_OC
        0x0435: GnssResetTime, # LR11XX_GNSS_RESET_TIME_OC
        0x0437: GnssResetPosition, # LR11XX_GNSS_RESET_POSITION_OC
        0x0438: GnssReadWeekNumberRollover, # LR11XX_GNSS_READ_WEEK_NUMBER_ROLLOVER_OC
        0x0439: GnssReadDemodStatus, # LR11XX_GNSS_READ_DEMOD_STATUS_OC
        0x044a: GnssReadCumulTiming, # LR11XX_GNSS_READ_CUMULATIVE_TIMING_OC
        0x044b: GnssSetTime, # LR11XX_GNSS_SET_TIME_OC
        0x044d: GnssConfigDelayResetAP, # LR11XX_GNSS_CONFIG_DELAY_RESET_AP_OC
        0x0453: GnssReadDelayResetAP, # LR11XX_GNSS_READ_DELAY_RESET_AP_OC
        0x0456: GnssReadKeepSyncStatus, # LR11XX_GNSS_READ_KEEP_SYNC_STATUS_OC
        0x0457: GnssReadAlmanacStatus, # LR11XX_GNSS_READ_ALMANAC_STATUS_OC
        0x0463: GnssConfigAlmanacUpdatePeriod, # LR11XX_GNSS_CONFIG_ALMANAC_UPDATE_PERIOD_OC
        0x0464: GnssReadAlmanacUpdatePeriod, # LR11XX_GNSS_READ_ALMANAC_UPDATE_PERIOD_OC
        0x0466: GnssGetSvWarmStart, # LR11XX_GNSS_GET_SV_SYNC_OC
    }

