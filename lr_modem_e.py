# Modem-E (LR1121 Modem-E firmware) command decoding
# from https://github.com/Lora-net/lr1121_modemE_driver
# command groups (modem_e_common.h):
#   0x0600 BSP, 0x0601 MODEM, 0x0602 LORAWAN, 0x0603 RELAY
# wire format per the modem_e_hal_impl.c reference HAL:
#   command frame:  MOSI [group_hi, group_lo, cmd, params..., CRC]
#   write commands are followed by a 2-byte RC read-back: MOSI [00 00], MISO [RC, CRC(0xFF,[RC])]
#   read responses: MOSI all-zero, MISO [RC, data..., CRC(0xFF, RC+data)]
# cmdDict keys are the full 3-byte header: (group << 8) | cmd

rcDict = {
    0x00: 'OK',
    0x01: 'UNKNOWN',
    0x02: 'NOT_IMPLEMENTED',
    0x03: 'NOT_INITIALIZED',
    0x04: 'INVALID',
    0x05: 'BUSY',
    0x06: 'FAIL',
    0x08: 'BAD_CRC',
    0x0A: 'BAD_SIZE',
    0x0F: 'FRAME_ERROR',
    0x10: 'NO_TIME',
    0x12: 'NO_EVENT',
}

eventDict = {  # modem_e_lorawan_event_type_t
    0x00: 'RESET',
    0x01: 'ALARM',
    0x02: 'JOINED',
    0x03: 'JOIN_FAIL',
    0x04: 'TX_DONE',
    0x05: 'DOWN_DATA',
    0x06: 'LINK_CHECK',
    0x07: 'LORAWAN_MAC_TIME',
    0x08: 'CLASS_B_PING_SLOT_INFO',
    0x09: 'CLASS_B_STATUS',
    0x0A: 'NEW_MULTICAST_SESSION_CLASS_C',
    0x0B: 'NEW_MULTICAST_SESSION_CLASS_B',
    0x0C: 'NO_MORE_MULTICAST_SESSION_CLASS_C',
    0x0D: 'NO_MORE_MULTICAST_SESSION_CLASS_B',
    0x0E: 'RELAY_TX_DYNAMIC',
    0x0F: 'RELAY_TX_MODE',
    0x10: 'RELAY_TX_SYNC',
    0x11: 'ALC_SYNC_TIME',
    0x12: 'FUOTA_DONE',
    0x13: 'TEST_MODE',
    0x14: 'REGIONAL_DUTY_CYCLE',
    0x15: 'DR_BACKOFF_LIMIT',
    0x16: 'RESET_REQUEST',
}

regionDict = {  # modem_e_regions_t
    0x01: 'EU868',
    0x02: 'AS923_GRP1',
    0x03: 'US915',
    0x04: 'AU915',
    0x05: 'CN470',
    0x06: 'WW2G4',
    0x07: 'AS923_GRP2',
    0x08: 'AS923_GRP3',
    0x09: 'IN865',
    0x0A: 'KR920',
    0x0B: 'RU864',
    0x0C: 'CN470_RP_1_0',
    0x0D: 'AS923_GRP4',
}

classDict = {0: 'A', 1: 'B', 2: 'C'}  # modem_e_classes_t

adrProfileDict = {  # modem_e_adr_profiles_t
    0x00: 'NETWORK_SERVER_CONTROLLED',
    0x01: 'MOBILE_LONG_RANGE',
    0x02: 'MOBILE_LOW_POWER',
    0x03: 'CUSTOM',
}

windowDict = {  # modem_e_downlink_window_t
    0x01: 'RX1',
    0x02: 'RX2',
    0x03: 'RXC',
    0x04: 'RXC_MC_GRP0',
    0x05: 'RXC_MC_GRP1',
    0x06: 'RXC_MC_GRP2',
    0x07: 'RXC_MC_GRP3',
    0x08: 'RXB',
    0x09: 'RXB_MC_GRP0',
    0x0A: 'RXB_MC_GRP1',
    0x0B: 'RXB_MC_GRP2',
    0x0C: 'RXB_MC_GRP3',
    0x0D: 'RXBEACON',
    0x0E: 'RXRELAY',
}

tstLoraBwDict = {  # modem_e_tst_mode_lora_bw_t
    0x01: '10kHz', 0x02: '15kHz', 0x03: '20kHz', 0x04: '31kHz',
    0x05: '41kHz', 0x06: '62kHz', 0x07: '125kHz', 0x08: '200kHz',
    0x09: '250kHz', 0x0A: '400kHz', 0x0B: '500kHz', 0x0C: '800kHz',
}

tstLoraCrDict = {  # modem_e_tst_mode_lora_cr_t
    0x01: '4/5', 0x02: '4/6', 0x03: '4/7', 0x04: '4/8',
    0x05: '4/5LI', 0x06: '4/6LI', 0x07: '4/8LI',
}

tstFhssBwDict = {  # modem_e_tst_mode_lr_fhss_bw_t
    0x00: '39063Hz', 0x01: '85938Hz', 0x02: '136719Hz', 0x03: '183594Hz',
    0x04: '335938Hz', 0x05: '386719Hz', 0x06: '722656Hz', 0x07: '773438Hz',
    0x08: '1523438Hz', 0x09: '1574219Hz',
}

tstFhssGridDict = {0x00: '25391Hz', 0x01: '3906Hz'}
tstFhssCrDict = {0x01: '2/3', 0x03: '1/3'}

paSelDict = {0x00: 'LP', 0x01: 'HP', 0x02: 'HF'}

def _rc(ba_miso):
    return 'RC=' + rcDict.get(ba_miso[0], hex(ba_miso[0]) + '?')

def crc8(init, data):
    # modem_e_modem_compute_crc from modem_e_modem_hal.h (poly 0x65 reflected)
    crc = init
    for b in data:
        extract = b
        for _ in range(8):
            s = (crc ^ extract) & 0x01
            crc >>= 1
            if s:
                crc ^= 0x65
            extract >>= 1
    return crc

def modem_e_rc_crc_ok(ba_miso):
    return len(ba_miso) >= 2 and ba_miso[1] == crc8(0xFF, [ba_miso[0]])

def modem_e_rc_readback(hla):
    # 2 dummy MOSI bytes after a write command; MISO = [RC, CRC(0xFF,[RC])]
    rc = hla.ba_miso[0]
    crc_expected = crc8(0xFF, [rc])
    if rc == 0x00 and hla.ba_miso[1] == 0x00:
        return 'ModemE RC read-back: no response'
    if hla.ba_miso[1] == crc_expected:
        return 'ModemE ' + _rc(hla.ba_miso)
    return 'ModemE ' + _rc(hla.ba_miso) + f' [crc BAD: got 0x{hla.ba_miso[1]:02x} expected 0x{crc_expected:02x}]'

def modem_e_resp_crc_note(hla):
    # read responses end with CRC(0xFF, RC+data); flag when it doesn't validate
    if len(hla.ba_miso) < 2:
        return ''
    if hla.ba_miso[-1] == crc8(0xFF, hla.ba_miso[0:-1]):
        return ''
    return ' [crc BAD]'

def modem_e_orphan_read(hla):
    # all-zero-MOSI read that isn't paired with a decoded command: [RC, payload..., CRC]
    return ('ModemE response (unpaired command) ' + _rc(hla.ba_miso) + ', '
            + str(max(0, len(hla.ba_miso) - 2)) + ' payload bytes' + modem_e_resp_crc_note(hla))

def _u16(ba, o):
    return int.from_bytes(bytearray(ba[o:o+2]), 'big')

def _u32(ba, o):
    return int.from_bytes(bytearray(ba[o:o+4]), 'big')

def _u64(ba, o):
    return int.from_bytes(bytearray(ba[o:o+8]), 'big')

def _i8(v):
    return v - 256 if v > 127 else v

def _hexstr(ba, o, n):
    return ''.join(f'{b:02x}' for b in ba[o:o+n])


class LrModemE:
    def __init__(self):
        pass

    ####################################################################
    # group 0x0600 BSP
    ####################################################################

    def BspGetTxPowerOffset(self):
        self.next_transfer_response = 1
        return 'BspGetTxPowerOffset (request)'

    def ResponseBspGetTxPowerOffset(self):
        return 'BspGetTxPowerOffset ' + str(_i8(self.ba_miso[1])) + 'dB (' + _rc(self.ba_miso) + ')'

    def BspSetTxPowerOffset(self):
        return 'BspSetTxPowerOffset ' + str(_i8(self.ba_mosi[3])) + 'dB'

    def BspGetOutputPowerConfig(self):
        self.next_transfer_response = 1
        return 'BspGetOutputPowerConfig (request)'

    def ResponseBspGetOutputPowerConfig(self):
        return 'BspGetOutputPowerConfig ' + str(max(0, len(self.ba_miso)-2)) + ' bytes (' + _rc(self.ba_miso) + ')'

    def BspSetOutputPowerConfig(self):
        return 'BspSetOutputPowerConfig ' + str(len(self.ba_mosi)-3) + ' bytes'

    def BspGetRfOutput(self):
        self.next_transfer_response = 1
        return 'BspGetRfOutput (request)'

    def ResponseBspGetRfOutput(self):
        pa = self.ba_miso[1]
        return 'BspGetRfOutput ' + paSelDict.get(pa, hex(pa)+'?') + ' (' + _rc(self.ba_miso) + ')'

    def BspSetRfOutput(self):
        pa = self.ba_mosi[3]
        return 'BspSetRfOutput ' + paSelDict.get(pa, hex(pa)+'?')

    def BspGetCrystalError(self):
        self.next_transfer_response = 1
        return 'BspGetCrystalError (request)'

    def ResponseBspGetCrystalError(self):
        return 'BspGetCrystalError ' + str(_u32(self.ba_miso, 1)) + 'ppm (' + _rc(self.ba_miso) + ')'

    def BspSetCrystalError(self):
        return 'BspSetCrystalError ' + str(_u32(self.ba_mosi, 3)) + 'ppm'

    def BspGetXoscCapaTrimAB(self):
        self.next_transfer_response = 1
        return 'BspGetXoscCapaTrimAB (request)'

    def ResponseBspGetXoscCapaTrimAB(self):
        return 'BspGetXoscCapaTrimAB A=' + hex(self.ba_miso[1]) + ' B=' + hex(self.ba_miso[2]) + ' (' + _rc(self.ba_miso) + ')'

    def BspSetXoscCapaTrimAB(self):
        return 'BspSetXoscCapaTrimAB A=' + hex(self.ba_mosi[3]) + ' B=' + hex(self.ba_mosi[4])

    def BspGetTxPowerConsumption(self):
        self.next_transfer_response = 1
        return 'BspGetTxPowerConsumption (request)'

    def ResponseBspGetTxPowerConsumption(self):
        return 'BspGetTxPowerConsumption ' + str(max(0, len(self.ba_miso)-2)) + ' bytes (' + _rc(self.ba_miso) + ')'

    def BspSetTxPowerConsumption(self):
        return 'BspSetTxPowerConsumption ' + str(len(self.ba_mosi)-3) + ' bytes'

    def _rx_consumption_str(self, name):
        # 8 bytes: consumption_rx_boosted_off_ua u32, consumption_rx_boosted_on_ua u32
        if len(self.ba_miso) >= 9:
            off_ua = _u32(self.ba_miso, 1)
            on_ua = _u32(self.ba_miso, 5)
            return name + ' boostedOff=' + str(off_ua) + 'uA boostedOn=' + str(on_ua) + 'uA (' + _rc(self.ba_miso) + ')'
        return name + ' (' + _rc(self.ba_miso) + ')'

    def BspGetLoraRxPowerConsumption(self):
        self.next_transfer_response = 1
        return 'BspGetLoraRxPowerConsumption (request)'

    def ResponseBspGetLoraRxPowerConsumption(self):
        return LrModemE._rx_consumption_str(self, 'BspGetLoraRxPowerConsumption')

    def BspSetLoraRxPowerConsumption(self):
        return 'BspSetLoraRxPowerConsumption boostedOff=' + str(_u32(self.ba_mosi, 3)) + 'uA boostedOn=' + str(_u32(self.ba_mosi, 7)) + 'uA'

    def BspGetGfskRxPowerConsumption(self):
        self.next_transfer_response = 1
        return 'BspGetGfskRxPowerConsumption (request)'

    def ResponseBspGetGfskRxPowerConsumption(self):
        return LrModemE._rx_consumption_str(self, 'BspGetGfskRxPowerConsumption')

    def BspSetGfskRxPowerConsumption(self):
        return 'BspSetGfskRxPowerConsumption boostedOff=' + str(_u32(self.ba_mosi, 3)) + 'uA boostedOn=' + str(_u32(self.ba_mosi, 7)) + 'uA'

    ####################################################################
    # group 0x0601 MODEM
    ####################################################################

    def ModemFactoryReset(self):
        return 'ModemFactoryReset'

    def ModemGetVersion(self):
        self.next_transfer_response = 1
        return 'ModemGetVersion (request)'

    def ResponseModemGetVersion(self):
        # rbuffer: [0]=use_case, [1..3]=modem M.m.p, [5..7]=lbm M.m.p
        if len(self.ba_miso) >= 9:
            use_case = self.ba_miso[1]
            modem_v = f'{self.ba_miso[2]}.{self.ba_miso[3]}.{self.ba_miso[4]}'
            lbm_v = f'{self.ba_miso[6]}.{self.ba_miso[7]}.{self.ba_miso[8]}'
            return 'ModemGetVersion useCase=' + hex(use_case) + ' modem v' + modem_v + ' lbm v' + lbm_v + ' (' + _rc(self.ba_miso) + ')'
        return 'ModemGetVersion (' + _rc(self.ba_miso) + ')'

    def ModemGetStatus(self):
        self.next_transfer_response = 1
        return 'ModemGetStatus (request)'

    def ResponseModemGetStatus(self):
        status = self.ba_miso[1]
        _str = ''
        if status & 0x02:
            _str += 'CRASH '
        if status & 0x08:
            _str += 'JOINED '
        if status & 0x10:
            _str += 'SUSPEND '
        if status & 0x40:
            _str += 'JOINING '
        if _str == '':
            _str = 'idle '
        return 'ModemGetStatus ' + _str + '(' + _rc(self.ba_miso) + ')'

    def ModemGetCharge(self):
        self.next_transfer_response = 1
        return 'ModemGetCharge (request)'

    def ResponseModemGetCharge(self):
        return 'ModemGetCharge ' + str(max(0, len(self.ba_miso)-2)) + ' bytes (' + _rc(self.ba_miso) + ')'

    def ModemGetEvent(self):
        self.next_transfer_response = 1
        return 'ModemGetEvent (request)'

    def ResponseModemGetEvent(self):
        if self.ba_miso[0] == 0x12:  # NO_EVENT
            return 'ModemGetEvent no event'
        if len(self.ba_miso) >= 5:
            ev = self.ba_miso[1]
            missed = self.ba_miso[2]
            data = _u16(self.ba_miso, 3)
            return 'ModemGetEvent ' + eventDict.get(ev, hex(ev)+'?') + ' missed=' + str(missed) + ' data=' + hex(data) + ' (' + _rc(self.ba_miso) + ')'
        return 'ModemGetEvent (' + _rc(self.ba_miso) + ')'

    def ModemGetSuspend(self):
        self.next_transfer_response = 1
        return 'ModemGetSuspend (request)'

    def ResponseModemGetSuspend(self):
        return 'ModemGetSuspend ' + ('suspended' if self.ba_miso[1] else 'resumed') + ' (' + _rc(self.ba_miso) + ')'

    def ModemSetSuspend(self):
        return 'ModemSetSuspend ' + ('suspend' if self.ba_mosi[3] else 'resume')

    def ModemSetAlarmTimer(self):
        return 'ModemSetAlarmTimer ' + str(_u32(self.ba_mosi, 3)) + 's'

    def ModemClearAlarmTimer(self):
        return 'ModemClearAlarmTimer'

    def ModemGetAlarmRemainingTime(self):
        self.next_transfer_response = 1
        return 'ModemGetAlarmRemainingTime (request)'

    def ResponseModemGetAlarmRemainingTime(self):
        return 'ModemGetAlarmRemainingTime ' + str(_u32(self.ba_miso, 1)) + 's (' + _rc(self.ba_miso) + ')'

    def ModemGetCrashlog(self):
        self.next_transfer_response = 1
        return 'ModemGetCrashlog (request)'

    def ResponseModemGetCrashlog(self):
        status = 'new' if self.ba_miso[1] else 'none'
        return 'ModemGetCrashlog status=' + status + ' ' + str(max(0, len(self.ba_miso)-3)) + ' bytes (' + _rc(self.ba_miso) + ')'

    def ModemStoreStateSnapshotToNvm(self):
        self.next_transfer_response = 1
        return 'ModemStoreStateSnapshotToNvm (request)'

    def ResponseModemStoreStateSnapshotToNvm(self):
        return 'ModemStoreStateSnapshotToNvm nvmWriteCounter=' + str(_u32(self.ba_miso, 1)) + ' (' + _rc(self.ba_miso) + ')'

    def ModemRestoreStateSnapshotFromNvm(self):
        return 'ModemRestoreStateSnapshotFromNvm elapsed=' + str(_u64(self.ba_mosi, 3)) + 'ms'

    # test mode (MODEM_E_TEST_CMD 0x05, sub-command in 4th byte)

    def _TestStart(self):
        return 'TestModeStart'

    def _TestExit(self):
        return 'TestModeExit'

    def _TestNop(self):
        return 'TestNop'

    def _TestTxLora(self):
        freq = _u32(self.ba_mosi, 4)
        power = _i8(self.ba_mosi[8])
        payload_len = self.ba_mosi[9]
        sf = self.ba_mosi[10]
        bw = self.ba_mosi[11]
        cr = self.ba_mosi[12]
        iq = self.ba_mosi[13]
        crc = self.ba_mosi[14]
        hdr = self.ba_mosi[15]
        preamble = _u32(self.ba_mosi, 16)
        nb_tx = _u32(self.ba_mosi, 20)
        delay = _u32(self.ba_mosi, 24)
        syncword = self.ba_mosi[28]
        return ('TestTxLora ' + str(freq) + 'Hz ' + str(power) + 'dBm len' + str(payload_len)
                + ' SF' + str(sf) + ' ' + tstLoraBwDict.get(bw, hex(bw)+'?')
                + ' CR' + tstLoraCrDict.get(cr, hex(cr)+'?')
                + (' iqInv' if iq else '') + (' crcOn' if crc else ' crcOff')
                + (' implicit' if hdr else ' explicit')
                + ' preamble=' + str(preamble) + ' nbTx=' + str(nb_tx)
                + ' delay=' + str(delay) + 'ms sync=' + hex(syncword))

    def _TestTxFsk(self):
        freq = _u32(self.ba_mosi, 4)
        power = _i8(self.ba_mosi[8])
        payload_len = self.ba_mosi[9]
        nb_tx = _u32(self.ba_mosi, 10)
        delay = _u32(self.ba_mosi, 14)
        return ('TestTxFsk ' + str(freq) + 'Hz ' + str(power) + 'dBm len' + str(payload_len)
                + ' nbTx=' + str(nb_tx) + ' delay=' + str(delay) + 'ms')

    def _TestTxLrFhss(self):
        freq = _u32(self.ba_mosi, 4)
        power = _i8(self.ba_mosi[8])
        payload_len = self.ba_mosi[9]
        grid = self.ba_mosi[10]
        bw = self.ba_mosi[11]
        cr = self.ba_mosi[12]
        nb_tx = _u32(self.ba_mosi, 13)
        delay = _u32(self.ba_mosi, 17)
        hopping = self.ba_mosi[21]
        return ('TestTxLrFhss ' + str(freq) + 'Hz ' + str(power) + 'dBm len' + str(payload_len)
                + ' grid=' + tstFhssGridDict.get(grid, hex(grid)+'?')
                + ' bw=' + tstFhssBwDict.get(bw, hex(bw)+'?')
                + ' CR' + tstFhssCrDict.get(cr, hex(cr)+'?')
                + ' nbTx=' + str(nb_tx) + ' delay=' + str(delay) + 'ms'
                + (' hopping' if hopping else ''))

    def _TestTxCw(self):
        return 'TestTxCw ' + str(_u32(self.ba_mosi, 4)) + 'Hz ' + str(_i8(self.ba_mosi[8])) + 'dBm'

    def _TestRxLoraCont(self):
        freq = _u32(self.ba_mosi, 4)
        sf = self.ba_mosi[8]
        bw = self.ba_mosi[9]
        cr = self.ba_mosi[10]
        return ('TestRxLoraCont ' + str(freq) + 'Hz SF' + str(sf)
                + ' ' + tstLoraBwDict.get(bw, hex(bw)+'?')
                + ' CR' + tstLoraCrDict.get(cr, hex(cr)+'?'))

    def _TestRxFskCont(self):
        return 'TestRxFskCont ' + str(_u32(self.ba_mosi, 4)) + 'Hz'

    def _TestReadPacketCounterRxCont(self):
        self.next_transfer_response = 1
        return 'TestReadPacketCounterRxCont (request)'

    def _TestRssiSubghz(self):
        freq = _u32(self.ba_mosi, 4)
        time_ms = _u16(self.ba_mosi, 8)
        bw_hz = _u32(self.ba_mosi, 10)
        return 'TestRssiSubghz ' + str(freq) + 'Hz ' + str(time_ms) + 'ms bw=' + str(bw_hz) + 'Hz'

    def _TestReadRssi(self):
        self.next_transfer_response = 1
        return 'TestReadRssi (request)'

    def _TestRadioRst(self):
        return 'TestRadioRst'

    def _TestReadRegister(self):
        return 'TestReadRegister'

    def _TestWriteRegister(self):
        return 'TestWriteRegister'

    testDict = {
        0x00: _TestStart,
        0x01: _TestExit,
        0x02: _TestNop,
        0x03: _TestTxLora,
        0x04: _TestTxFsk,
        0x05: _TestTxLrFhss,
        0x06: _TestTxCw,
        0x07: _TestRxLoraCont,
        0x08: _TestRxFskCont,
        0x09: _TestReadPacketCounterRxCont,
        0x0A: _TestRssiSubghz,
        0x0B: _TestReadRssi,
        0x0E: _TestRadioRst,
        0x0F: _TestReadRegister,
        0x10: _TestWriteRegister,
    }

    def ModemTest(self):
        sub = self.ba_mosi[3]
        self.modem_e_test_sub = sub
        if sub in LrModemE.testDict:
            return LrModemE.testDict[sub](self)
        return 'ModemTest sub-command ' + hex(sub) + '?'

    def ResponseModemTest(self):
        sub = getattr(self, 'modem_e_test_sub', None)
        if sub == 0x09:
            return 'TestReadPacketCounterRxCont ' + str(_u32(self.ba_miso, 1)) + ' packets (' + _rc(self.ba_miso) + ')'
        if sub == 0x0B:
            return 'TestReadRssi ' + str(_i8(self.ba_miso[1]) - 64) + 'dBm (' + _rc(self.ba_miso) + ')'
        return 'ModemTest response (' + _rc(self.ba_miso) + ')'

    ####################################################################
    # group 0x0602 LORAWAN
    ####################################################################

    def LorawanGetVersion(self):
        self.next_transfer_response = 1
        return 'LorawanGetVersion (request)'

    def ResponseLorawanGetVersion(self):
        if len(self.ba_miso) >= 9:
            lw = f'{self.ba_miso[1]}.{self.ba_miso[2]}.{self.ba_miso[3]}.{self.ba_miso[4]}'
            rp = f'{self.ba_miso[5]}.{self.ba_miso[6]}.{self.ba_miso[7]}.{self.ba_miso[8]}'
            return 'LorawanGetVersion lorawan v' + lw + ' rp v' + rp + ' (' + _rc(self.ba_miso) + ')'
        return 'LorawanGetVersion (' + _rc(self.ba_miso) + ')'

    def LorawanGetDevEui(self):
        self.next_transfer_response = 1
        return 'LorawanGetDevEui (request)'

    def ResponseLorawanGetDevEui(self):
        return 'LorawanGetDevEui ' + _hexstr(self.ba_miso, 1, 8) + ' (' + _rc(self.ba_miso) + ')'

    def LorawanSetDevEui(self):
        return 'LorawanSetDevEui ' + _hexstr(self.ba_mosi, 3, 8)

    def LorawanGetJoinEui(self):
        self.next_transfer_response = 1
        return 'LorawanGetJoinEui (request)'

    def ResponseLorawanGetJoinEui(self):
        return 'LorawanGetJoinEui ' + _hexstr(self.ba_miso, 1, 8) + ' (' + _rc(self.ba_miso) + ')'

    def LorawanSetJoinEui(self):
        return 'LorawanSetJoinEui ' + _hexstr(self.ba_mosi, 3, 8)

    def LorawanSetNwkKey(self):
        return 'LorawanSetNwkKey ' + _hexstr(self.ba_mosi, 3, 16)

    def LorawanSetAppKey(self):
        return 'LorawanSetAppKey ' + _hexstr(self.ba_mosi, 3, 16)

    def LorawanDeriveKeys(self):
        return 'LorawanDeriveKeys'

    def LorawanGetClass(self):
        self.next_transfer_response = 1
        return 'LorawanGetClass (request)'

    def ResponseLorawanGetClass(self):
        c = self.ba_miso[1]
        return 'LorawanGetClass class ' + classDict.get(c, hex(c)+'?') + ' (' + _rc(self.ba_miso) + ')'

    def LorawanSetClass(self):
        c = self.ba_mosi[3]
        return 'LorawanSetClass class ' + classDict.get(c, hex(c)+'?')

    def LorawanGetRegion(self):
        self.next_transfer_response = 1
        return 'LorawanGetRegion (request)'

    def ResponseLorawanGetRegion(self):
        r = self.ba_miso[1]
        return 'LorawanGetRegion ' + regionDict.get(r, hex(r)+'?') + ' (' + _rc(self.ba_miso) + ')'

    def LorawanSetRegion(self):
        r = self.ba_mosi[3]
        return 'LorawanSetRegion ' + regionDict.get(r, hex(r)+'?')

    def LorawanJoin(self):
        return 'LorawanJoin'

    def LorawanLeaveNetwork(self):
        return 'LorawanLeaveNetwork'

    def LorawanGetNextTxMaxPayload(self):
        self.next_transfer_response = 1
        return 'LorawanGetNextTxMaxPayload (request)'

    def ResponseLorawanGetNextTxMaxPayload(self):
        return 'LorawanGetNextTxMaxPayload ' + str(self.ba_miso[1]) + ' bytes (' + _rc(self.ba_miso) + ')'

    def LorawanRequestTx(self):
        port = self.ba_mosi[3]
        confirmed = self.ba_mosi[4]
        data_len = len(self.ba_mosi) - 5
        return ('LorawanRequestTx port=' + str(port)
                + (' confirmed' if confirmed else ' unconfirmed')
                + ' ' + str(data_len) + ' data bytes')

    def LorawanRequestEmptyTx(self):
        fport_populated = self.ba_mosi[3]
        port = self.ba_mosi[4]
        confirmed = self.ba_mosi[5]
        _str = 'LorawanRequestEmptyTx '
        if fport_populated:
            _str += 'port=' + str(port) + ' '
        return _str + ('confirmed' if confirmed else 'unconfirmed')

    def LorawanEmergencyTx(self):
        port = self.ba_mosi[3]
        confirmed = self.ba_mosi[4]
        data_len = len(self.ba_mosi) - 5
        return ('LorawanEmergencyTx port=' + str(port)
                + (' confirmed' if confirmed else ' unconfirmed')
                + ' ' + str(data_len) + ' data bytes')

    def LorawanGetDownlinkDataSize(self):
        self.next_transfer_response = 1
        return 'LorawanGetDownlinkDataSize (request)'

    def ResponseLorawanGetDownlinkDataSize(self):
        return ('LorawanGetDownlinkDataSize size=' + str(self.ba_miso[1])
                + ' remaining=' + str(self.ba_miso[2]) + ' (' + _rc(self.ba_miso) + ')')

    def LorawanGetDownlinkData(self):
        self.next_transfer_response = 1
        return 'LorawanGetDownlinkData (request)'

    def ResponseLorawanGetDownlinkData(self):
        data_len = max(0, len(self.ba_miso) - 2)
        return 'LorawanGetDownlinkData ' + str(data_len) + ' bytes: ' + _hexstr(self.ba_miso, 1, data_len) + ' (' + _rc(self.ba_miso) + ')'

    def LorawanGetDownlinkMetadata(self):
        self.next_transfer_response = 1
        return 'LorawanGetDownlinkMetadata (request)'

    def ResponseLorawanGetDownlinkMetadata(self):
        if len(self.ba_miso) >= 12:
            rssi = _i8(self.ba_miso[2]) - 64
            snr = _i8(self.ba_miso[3]) / 4
            window = self.ba_miso[4]
            fport = self.ba_miso[5]
            fpending = self.ba_miso[6]
            freq = _u32(self.ba_miso, 7)
            dr = self.ba_miso[11]
            return ('LorawanGetDownlinkMetadata rssi=' + str(rssi) + 'dBm snr=' + str(snr)
                    + 'dB ' + windowDict.get(window, hex(window)+'?')
                    + ' port=' + str(fport) + (' fPending' if fpending else '')
                    + ' ' + str(freq) + 'Hz DR' + str(dr) + ' (' + _rc(self.ba_miso) + ')')
        return 'LorawanGetDownlinkMetadata (' + _rc(self.ba_miso) + ')'

    def LorawanGetLostConnectionCounter(self):
        self.next_transfer_response = 1
        return 'LorawanGetLostConnectionCounter (request)'

    def ResponseLorawanGetLostConnectionCounter(self):
        return ('LorawanGetLostConnectionCounter count=' + str(_u16(self.ba_miso, 1))
                + ' since=' + str(_u32(self.ba_miso, 3)) + 's (' + _rc(self.ba_miso) + ')')

    def LorawanGetNetworkType(self):
        self.next_transfer_response = 1
        return 'LorawanGetNetworkType (request)'

    def ResponseLorawanGetNetworkType(self):
        return 'LorawanGetNetworkType ' + ('public' if self.ba_miso[1] else 'private') + ' (' + _rc(self.ba_miso) + ')'

    def LorawanSetNetworkType(self):
        return 'LorawanSetNetworkType ' + ('public' if self.ba_mosi[3] else 'private')

    def LorawanGetCertificationMode(self):
        self.next_transfer_response = 1
        return 'LorawanGetCertificationMode (request)'

    def ResponseLorawanGetCertificationMode(self):
        return 'LorawanGetCertificationMode ' + ('enabled' if self.ba_miso[1] else 'disabled') + ' (' + _rc(self.ba_miso) + ')'

    def LorawanSetCertificationMode(self):
        return 'LorawanSetCertificationMode ' + ('enable' if self.ba_mosi[3] else 'disable')

    def LorawanGetDutyCycleStatus(self):
        self.next_transfer_response = 1
        return 'LorawanGetDutyCycleStatus (request)'

    def ResponseLorawanGetDutyCycleStatus(self):
        val = _u32(self.ba_miso, 1)
        if val > 0x7fffffff:
            val -= 0x100000000
        return 'LorawanGetDutyCycleStatus ' + str(val) + 'ms (' + _rc(self.ba_miso) + ')'

    def LorawanGetAvailableDataRate(self):
        self.next_transfer_response = 1
        return 'LorawanGetAvailableDataRate (request)'

    def ResponseLorawanGetAvailableDataRate(self):
        mask = _u16(self.ba_miso, 1)
        drs = ','.join('DR' + str(i) for i in range(16) if mask & (1 << i))
        return 'LorawanGetAvailableDataRate [' + drs + '] (' + _rc(self.ba_miso) + ')'

    def LorawanGetAdrProfile(self):
        self.next_transfer_response = 1
        return 'LorawanGetAdrProfile (request)'

    def ResponseLorawanGetAdrProfile(self):
        p = self.ba_miso[1]
        return 'LorawanGetAdrProfile ' + adrProfileDict.get(p, hex(p)+'?') + ' (' + _rc(self.ba_miso) + ')'

    def LorawanSetAdrProfile(self):
        p = self.ba_mosi[3]
        _str = 'LorawanSetAdrProfile ' + adrProfileDict.get(p, hex(p)+'?')
        if p == 0x03 and len(self.ba_mosi) > 4:  # CUSTOM: 16-entry data rate list follows
            _str += ' [' + _hexstr(self.ba_mosi, 4, len(self.ba_mosi)-4) + ']'
        return _str

    def LorawanSetJoinDataRateDistribution(self):
        return 'LorawanSetJoinDataRateDistribution [' + _hexstr(self.ba_mosi, 3, len(self.ba_mosi)-3) + ']'

    def LorawanGetNbTrans(self):
        self.next_transfer_response = 1
        return 'LorawanGetNbTrans (request)'

    def ResponseLorawanGetNbTrans(self):
        return 'LorawanGetNbTrans ' + str(self.ba_miso[1]) + ' (' + _rc(self.ba_miso) + ')'

    def LorawanSetNbTrans(self):
        return 'LorawanSetNbTrans ' + str(self.ba_mosi[3])

    def LorawanGetAdrAckLimitDelay(self):
        self.next_transfer_response = 1
        return 'LorawanGetAdrAckLimitDelay (request)'

    def ResponseLorawanGetAdrAckLimitDelay(self):
        return 'LorawanGetAdrAckLimitDelay limit=' + str(self.ba_miso[1]) + ' delay=' + str(self.ba_miso[2]) + ' (' + _rc(self.ba_miso) + ')'

    def LorawanSetAdrAckLimitDelay(self):
        return 'LorawanSetAdrAckLimitDelay limit=' + str(self.ba_mosi[3]) + ' delay=' + str(self.ba_mosi[4])

    def LorawanGetLbtState(self):
        self.next_transfer_response = 1
        return 'LorawanGetLbtState (request)'

    def ResponseLorawanGetLbtState(self):
        return 'LorawanGetLbtState ' + ('enabled' if self.ba_miso[1] else 'disabled') + ' (' + _rc(self.ba_miso) + ')'

    def LorawanSetLbtState(self):
        return 'LorawanSetLbtState ' + ('enable' if self.ba_mosi[3] else 'disable')

    def LorawanGetLbtParams(self):
        self.next_transfer_response = 1
        return 'LorawanGetLbtParams (request)'

    def ResponseLorawanGetLbtParams(self):
        if len(self.ba_miso) >= 11:
            duration = _u32(self.ba_miso, 1)
            threshold = _u16(self.ba_miso, 5)
            if threshold > 0x7fff:
                threshold -= 0x10000
            bw = _u32(self.ba_miso, 7)
            return ('LorawanGetLbtParams duration=' + str(duration) + 'ms threshold=' + str(threshold)
                    + 'dBm bw=' + str(bw) + 'Hz (' + _rc(self.ba_miso) + ')')
        return 'LorawanGetLbtParams (' + _rc(self.ba_miso) + ')'

    def LorawanSetLbtParams(self):
        duration = _u32(self.ba_mosi, 3)
        threshold = _u16(self.ba_mosi, 7)
        if threshold > 0x7fff:
            threshold -= 0x10000
        bw = _u32(self.ba_mosi, 9)
        return ('LorawanSetLbtParams duration=' + str(duration) + 'ms threshold=' + str(threshold)
                + 'dBm bw=' + str(bw) + 'Hz')

    def LorawanGetCsmaState(self):
        self.next_transfer_response = 1
        return 'LorawanGetCsmaState (request)'

    def ResponseLorawanGetCsmaState(self):
        return 'LorawanGetCsmaState ' + ('enabled' if self.ba_miso[1] else 'disabled') + ' (' + _rc(self.ba_miso) + ')'

    def LorawanSetCsmaState(self):
        return 'LorawanSetCsmaState ' + ('enable' if self.ba_mosi[3] else 'disable')

    def LorawanGetCsmaParams(self):
        self.next_transfer_response = 1
        return 'LorawanGetCsmaParams (request)'

    def ResponseLorawanGetCsmaParams(self):
        return ('LorawanGetCsmaParams maxChChange=' + str(self.ba_miso[1])
                + ' backoff=' + ('on' if self.ba_miso[2] else 'off')
                + ' nbBoMax=' + str(self.ba_miso[3]) + ' (' + _rc(self.ba_miso) + ')')

    def LorawanSetCsmaParams(self):
        return ('LorawanSetCsmaParams maxChChange=' + str(self.ba_mosi[3])
                + ' backoff=' + ('on' if self.ba_mosi[4] else 'off')
                + ' nbBoMax=' + str(self.ba_mosi[5]))

    def LorawanMacRequest(self):
        mask = self.ba_mosi[3]
        _str = ''
        if mask & 0x01:
            _str += 'LINK_CHECK '
        if mask & 0x02:
            _str += 'TIME '
        if mask & 0x04:
            _str += 'PING_SLOT_INFO '
        return 'LorawanMacRequest ' + _str.rstrip()

    def LorawanGetMacTime(self):
        self.next_transfer_response = 1
        return 'LorawanGetMacTime (request)'

    def ResponseLorawanGetMacTime(self):
        return ('LorawanGetMacTime gps=' + str(_u32(self.ba_miso, 1)) + 's frac='
                + str(_u32(self.ba_miso, 5)) + ' (' + _rc(self.ba_miso) + ')')

    def LorawanGetLinkCheckData(self):
        self.next_transfer_response = 1
        return 'LorawanGetLinkCheckData (request)'

    def ResponseLorawanGetLinkCheckData(self):
        return ('LorawanGetLinkCheckData margin=' + str(self.ba_miso[1])
                + 'dB gateways=' + str(self.ba_miso[2]) + ' (' + _rc(self.ba_miso) + ')')

    def LorawanSetBatteryLevel(self):
        source = self.ba_mosi[3]
        value = self.ba_mosi[4]
        return ('LorawanSetBatteryLevel ' + ('user value=' + str(value) if source else 'from modem'))

    def LorawanGetClassBPingSlotPeriodicity(self):
        self.next_transfer_response = 1
        return 'LorawanGetClassBPingSlotPeriodicity (request)'

    def ResponseLorawanGetClassBPingSlotPeriodicity(self):
        p = self.ba_miso[1]
        return 'LorawanGetClassBPingSlotPeriodicity ' + str(1 << p) + 's (' + _rc(self.ba_miso) + ')'

    def LorawanSetClassBPingSlotPeriodicity(self):
        p = self.ba_mosi[3]
        return 'LorawanSetClassBPingSlotPeriodicity ' + str(1 << p) + 's'

    def LorawanGetMulticastGroupConfig(self):
        self.next_transfer_response = 1
        return 'LorawanGetMulticastGroupConfig group=' + str(self.ba_mosi[3])

    def ResponseLorawanGetMulticastGroupConfig(self):
        return 'LorawanGetMulticastGroupConfig addr=' + hex(_u32(self.ba_miso, 1)) + ' (' + _rc(self.ba_miso) + ')'

    def LorawanSetMulticastGroupConfig(self):
        group = self.ba_mosi[3]
        addr = _u32(self.ba_mosi, 4)
        return ('LorawanSetMulticastGroupConfig group=' + str(group) + ' addr=' + hex(addr)
                + ' nwkSKey=' + _hexstr(self.ba_mosi, 8, 16) + ' appSKey=' + _hexstr(self.ba_mosi, 24, 16))

    def LorawanStartSessionMulticastClassC(self):
        return ('LorawanStartSessionMulticastClassC group=' + str(self.ba_mosi[3])
                + ' ' + str(_u32(self.ba_mosi, 4)) + 'Hz DR' + str(self.ba_mosi[8]))

    def LorawanGetMulticastClassCSessionStatus(self):
        self.next_transfer_response = 1
        return 'LorawanGetMulticastClassCSessionStatus group=' + str(self.ba_mosi[3])

    def ResponseLorawanGetMulticastClassCSessionStatus(self):
        return ('LorawanGetMulticastClassCSessionStatus '
                + ('started' if self.ba_miso[1] else 'stopped')
                + ' ' + str(_u32(self.ba_miso, 2)) + 'Hz DR' + str(self.ba_miso[6])
                + ' (' + _rc(self.ba_miso) + ')')

    def LorawanStopSessionMulticastClassC(self):
        return 'LorawanStopSessionMulticastClassC group=' + str(self.ba_mosi[3])

    def LorawanStopAllSessionsMulticastClassC(self):
        return 'LorawanStopAllSessionsMulticastClassC'

    def LorawanStartSessionMulticastClassB(self):
        return ('LorawanStartSessionMulticastClassB group=' + str(self.ba_mosi[3])
                + ' ' + str(_u32(self.ba_mosi, 4)) + 'Hz DR' + str(self.ba_mosi[8])
                + ' pingSlot=' + str(1 << self.ba_mosi[9]) + 's')

    def LorawanGetMulticastClassBSessionStatus(self):
        self.next_transfer_response = 1
        return 'LorawanGetMulticastClassBSessionStatus group=' + str(self.ba_mosi[3])

    def ResponseLorawanGetMulticastClassBSessionStatus(self):
        if len(self.ba_miso) >= 9:
            return ('LorawanGetMulticastClassBSessionStatus '
                    + ('started' if self.ba_miso[1] else 'stopped')
                    + ' ' + str(_u32(self.ba_miso, 2)) + 'Hz DR' + str(self.ba_miso[6])
                    + (' waitingBeacon' if self.ba_miso[7] else '')
                    + ' pingSlot=' + str(1 << self.ba_miso[8]) + 's'
                    + ' (' + _rc(self.ba_miso) + ')')
        return 'LorawanGetMulticastClassBSessionStatus (' + _rc(self.ba_miso) + ')'

    def LorawanStopSessionMulticastClassB(self):
        return 'LorawanStopSessionMulticastClassB group=' + str(self.ba_mosi[3])

    def LorawanStopAllSessionsMulticastClassB(self):
        return 'LorawanStopAllSessionsMulticastClassB'

    def LorawanStartAlcSyncService(self):
        return 'LorawanStartAlcSyncService'

    def LorawanStopAlcSyncService(self):
        return 'LorawanStopAlcSyncService'

    def LorawanAlcSyncGetTime(self):
        self.next_transfer_response = 1
        return 'LorawanAlcSyncGetTime (request)'

    def ResponseLorawanAlcSyncGetTime(self):
        return 'LorawanAlcSyncGetTime gps=' + str(_u32(self.ba_miso, 1)) + 's (' + _rc(self.ba_miso) + ')'

    def LorawanAlcSyncTrigRequest(self):
        return 'LorawanAlcSyncTrigRequest'

    def LorawanFuotaGetFileSizeCrc(self):
        self.next_transfer_response = 1
        return 'LorawanFuotaGetFileSizeCrc (request)'

    def ResponseLorawanFuotaGetFileSizeCrc(self):
        return ('LorawanFuotaGetFileSizeCrc size=' + str(_u32(self.ba_miso, 1))
                + ' crc=' + hex(_u32(self.ba_miso, 5)) + ' (' + _rc(self.ba_miso) + ')')

    def LorawanFuotaGetFileFragment(self):
        self.next_transfer_response = 1
        return ('LorawanFuotaGetFileFragment offset=' + str(_u32(self.ba_mosi, 3))
                + ' size=' + str(_u32(self.ba_mosi, 7)))

    def ResponseLorawanFuotaGetFileFragment(self):
        return 'LorawanFuotaGetFileFragment ' + str(max(0, len(self.ba_miso)-2)) + ' bytes (' + _rc(self.ba_miso) + ')'

    def LorawanGetUserAdrAckLimit(self):
        self.next_transfer_response = 1
        return 'LorawanGetUserAdrAckLimit (request)'

    def ResponseLorawanGetUserAdrAckLimit(self):
        return 'LorawanGetUserAdrAckLimit limit=' + str(self.ba_miso[1]) + ' delay=' + str(self.ba_miso[2]) + ' (' + _rc(self.ba_miso) + ')'

    def LorawanSetUserAdrAckLimit(self):
        return 'LorawanSetUserAdrAckLimit limit=' + str(self.ba_mosi[3]) + ' delay=' + str(self.ba_mosi[4])

    def LorawanConnectWithAbp(self):
        devaddr = _u32(self.ba_mosi, 3)
        return ('LorawanConnectWithAbp devAddr=' + hex(devaddr)
                + ' nwkSKey=' + _hexstr(self.ba_mosi, 7, 16) + ' appSKey=' + _hexstr(self.ba_mosi, 23, 16))

    def LorawanGetChannelMask(self):
        self.next_transfer_response = 1
        return 'LorawanGetChannelMask (request)'

    def ResponseLorawanGetChannelMask(self):
        return 'LorawanGetChannelMask ' + _hexstr(self.ba_miso, 1, max(0, len(self.ba_miso)-2)) + ' (' + _rc(self.ba_miso) + ')'

    def LorawanSetChannelMask(self):
        return 'LorawanSetChannelMask ' + _hexstr(self.ba_mosi, 3, len(self.ba_mosi)-3)

    ####################################################################
    # group 0x0603 RELAY
    ####################################################################

    def _relay_config_str(self, name, ba, offset):
        wor_freq = _u32(ba, offset)
        wor_ack_freq = _u32(ba, offset+4)
        dr = ba[offset+8]
        second_ch_en = ba[offset+9]
        backoff = ba[offset+10]
        activation = ba[offset+11]
        smart_level = ba[offset+12]
        missed_ack = ba[offset+13]
        return (name + ' worFreq=' + str(wor_freq) + 'Hz worAckFreq=' + str(wor_ack_freq)
                + 'Hz DR' + str(dr) + (' 2ndChOn' if second_ch_en else ' 2ndChOff')
                + ' backoff=' + str(backoff) + ' activation=' + str(activation)
                + ' smartLevel=' + str(smart_level) + ' missedAckThresh=' + str(missed_ack))

    def RelayGetTxConfig(self):
        self.next_transfer_response = 1
        return 'RelayGetTxConfig (request)'

    def ResponseRelayGetTxConfig(self):
        if len(self.ba_miso) >= 15:
            return LrModemE._relay_config_str(self, 'RelayGetTxConfig', self.ba_miso, 1) + ' (' + _rc(self.ba_miso) + ')'
        return 'RelayGetTxConfig (' + _rc(self.ba_miso) + ')'

    def RelaySetTxConfig(self):
        return LrModemE._relay_config_str(self, 'RelaySetTxConfig', self.ba_mosi, 3)

    ####################################################################
    # dispatch tables, keyed by (group << 8) | cmd
    ####################################################################

    cmdDict = {
        # 0x0600 BSP
        0x060000: BspGetTxPowerOffset,
        0x060001: BspSetTxPowerOffset,
        0x060002: BspGetOutputPowerConfig,
        0x060003: BspSetOutputPowerConfig,
        0x060004: BspGetRfOutput,
        0x060005: BspSetRfOutput,
        0x060006: BspGetCrystalError,
        0x060007: BspSetCrystalError,
        0x060008: BspGetXoscCapaTrimAB,
        0x060009: BspSetXoscCapaTrimAB,
        0x06000A: BspGetTxPowerConsumption,
        0x06000B: BspSetTxPowerConsumption,
        0x06000C: BspGetLoraRxPowerConsumption,
        0x06000D: BspSetLoraRxPowerConsumption,
        0x06000E: BspGetGfskRxPowerConsumption,
        0x06000F: BspSetGfskRxPowerConsumption,
        # 0x0601 MODEM
        0x060100: ModemFactoryReset,
        0x060101: ModemGetVersion,
        0x060102: ModemGetStatus,
        0x060103: ModemGetCharge,
        0x060104: ModemGetEvent,
        0x060105: ModemTest,
        0x060106: ModemGetSuspend,
        0x060107: ModemSetSuspend,
        0x060108: ModemSetAlarmTimer,
        0x060109: ModemClearAlarmTimer,
        0x06010A: ModemGetAlarmRemainingTime,
        0x06010B: ModemGetCrashlog,
        0x06010C: ModemStoreStateSnapshotToNvm,
        0x06010D: ModemRestoreStateSnapshotFromNvm,
        # 0x0602 LORAWAN
        0x060200: LorawanGetVersion,
        0x060201: LorawanGetDevEui,
        0x060202: LorawanSetDevEui,
        0x060203: LorawanGetJoinEui,
        0x060204: LorawanSetJoinEui,
        0x060205: LorawanSetNwkKey,
        0x060206: LorawanSetAppKey,
        0x060207: LorawanDeriveKeys,
        0x060208: LorawanGetClass,
        0x060209: LorawanSetClass,
        0x06020B: LorawanGetRegion,
        0x06020C: LorawanSetRegion,
        0x06020D: LorawanJoin,
        0x06020E: LorawanLeaveNetwork,
        0x060211: LorawanGetNextTxMaxPayload,
        0x060212: LorawanRequestTx,
        0x060213: LorawanRequestEmptyTx,
        0x060214: LorawanEmergencyTx,
        0x060215: LorawanGetDownlinkDataSize,
        0x060216: LorawanGetDownlinkData,
        0x060217: LorawanGetDownlinkMetadata,
        0x060218: LorawanGetLostConnectionCounter,
        0x060219: LorawanGetNetworkType,
        0x06021A: LorawanSetNetworkType,
        0x06021B: LorawanGetCertificationMode,
        0x06021C: LorawanSetCertificationMode,
        0x06021D: LorawanGetDutyCycleStatus,
        0x06021F: LorawanGetAvailableDataRate,
        0x060220: LorawanGetAdrProfile,
        0x060221: LorawanSetAdrProfile,
        0x060222: LorawanSetJoinDataRateDistribution,
        0x060223: LorawanGetNbTrans,
        0x060224: LorawanSetNbTrans,
        0x060225: LorawanGetAdrAckLimitDelay,
        0x060226: LorawanSetAdrAckLimitDelay,
        0x060227: LorawanGetLbtState,
        0x060228: LorawanSetLbtState,
        0x060229: LorawanGetLbtParams,
        0x06022A: LorawanSetLbtParams,
        0x06022B: LorawanGetCsmaState,
        0x06022C: LorawanSetCsmaState,
        0x06022D: LorawanGetCsmaParams,
        0x06022E: LorawanSetCsmaParams,
        0x06022F: LorawanMacRequest,
        0x060230: LorawanGetMacTime,
        0x060231: LorawanGetLinkCheckData,
        0x060232: LorawanSetBatteryLevel,
        0x060234: LorawanGetClassBPingSlotPeriodicity,
        0x060235: LorawanSetClassBPingSlotPeriodicity,
        0x060236: LorawanGetMulticastGroupConfig,
        0x060237: LorawanSetMulticastGroupConfig,
        0x060238: LorawanStartSessionMulticastClassC,
        0x060239: LorawanGetMulticastClassCSessionStatus,
        0x06023A: LorawanStopSessionMulticastClassC,
        0x06023B: LorawanStopAllSessionsMulticastClassC,
        0x06023C: LorawanStartSessionMulticastClassB,
        0x06023D: LorawanGetMulticastClassBSessionStatus,
        0x06023E: LorawanStopSessionMulticastClassB,
        0x06023F: LorawanStopAllSessionsMulticastClassB,
        0x060242: LorawanStartAlcSyncService,
        0x060243: LorawanStopAlcSyncService,
        0x060244: LorawanAlcSyncGetTime,
        0x060245: LorawanAlcSyncTrigRequest,
        0x060246: LorawanFuotaGetFileSizeCrc,
        0x060247: LorawanFuotaGetFileFragment,
        0x060248: LorawanGetUserAdrAckLimit,
        0x060249: LorawanSetUserAdrAckLimit,
        0x06024A: LorawanConnectWithAbp,
        0x06024B: LorawanGetChannelMask,
        0x06024C: LorawanSetChannelMask,
        # 0x0603 RELAY
        0x060300: RelayGetTxConfig,
        0x060301: RelaySetTxConfig,
    }

    cmdResponseDict = {
        0x060000: ResponseBspGetTxPowerOffset,
        0x060002: ResponseBspGetOutputPowerConfig,
        0x060004: ResponseBspGetRfOutput,
        0x060006: ResponseBspGetCrystalError,
        0x060008: ResponseBspGetXoscCapaTrimAB,
        0x06000A: ResponseBspGetTxPowerConsumption,
        0x06000C: ResponseBspGetLoraRxPowerConsumption,
        0x06000E: ResponseBspGetGfskRxPowerConsumption,
        0x060101: ResponseModemGetVersion,
        0x060102: ResponseModemGetStatus,
        0x060103: ResponseModemGetCharge,
        0x060104: ResponseModemGetEvent,
        0x060105: ResponseModemTest,
        0x060106: ResponseModemGetSuspend,
        0x06010A: ResponseModemGetAlarmRemainingTime,
        0x06010B: ResponseModemGetCrashlog,
        0x06010C: ResponseModemStoreStateSnapshotToNvm,
        0x060200: ResponseLorawanGetVersion,
        0x060201: ResponseLorawanGetDevEui,
        0x060203: ResponseLorawanGetJoinEui,
        0x060208: ResponseLorawanGetClass,
        0x06020B: ResponseLorawanGetRegion,
        0x060211: ResponseLorawanGetNextTxMaxPayload,
        0x060215: ResponseLorawanGetDownlinkDataSize,
        0x060216: ResponseLorawanGetDownlinkData,
        0x060217: ResponseLorawanGetDownlinkMetadata,
        0x060218: ResponseLorawanGetLostConnectionCounter,
        0x060219: ResponseLorawanGetNetworkType,
        0x06021B: ResponseLorawanGetCertificationMode,
        0x06021D: ResponseLorawanGetDutyCycleStatus,
        0x06021F: ResponseLorawanGetAvailableDataRate,
        0x060220: ResponseLorawanGetAdrProfile,
        0x060223: ResponseLorawanGetNbTrans,
        0x060225: ResponseLorawanGetAdrAckLimitDelay,
        0x060227: ResponseLorawanGetLbtState,
        0x060229: ResponseLorawanGetLbtParams,
        0x06022B: ResponseLorawanGetCsmaState,
        0x06022D: ResponseLorawanGetCsmaParams,
        0x060230: ResponseLorawanGetMacTime,
        0x060231: ResponseLorawanGetLinkCheckData,
        0x060234: ResponseLorawanGetClassBPingSlotPeriodicity,
        0x060236: ResponseLorawanGetMulticastGroupConfig,
        0x060239: ResponseLorawanGetMulticastClassCSessionStatus,
        0x06023D: ResponseLorawanGetMulticastClassBSessionStatus,
        0x060244: ResponseLorawanAlcSyncGetTime,
        0x060246: ResponseLorawanFuotaGetFileSizeCrc,
        0x060247: ResponseLorawanFuotaGetFileFragment,
        0x060248: ResponseLorawanGetUserAdrAckLimit,
        0x06024B: ResponseLorawanGetChannelMask,
        0x060300: ResponseRelayGetTxConfig,
    }
