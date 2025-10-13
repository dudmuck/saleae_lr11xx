# High Level Analyzer
# For more information and documentation, please go to https://support.saleae.com/extensions/high-level-analyzer-extensions
# for LR11xx --- https://www.semtech.com/products/wireless-rf/lora-edge/lr1110

from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame, StringSetting, NumberSetting, ChoicesSetting
import ctypes
from enum import Enum
from lr_gnss import LrGnss
from lr_wifi import LrWifi
c_uint8 = ctypes.c_uint8
c_uint32 = ctypes.c_uint32

lr_gnss = LrGnss()
lr_wifi = LrWifi()

class PacketType(Enum): # lr11xx_radio_pkt_type_t
    NONE = 0
    FSK = 1
    LORA = 2
    BPSK = 3
    FHSS = 4
    RTTOF = 5

class RxStatus_bits( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("PktSent", c_uint32, 1 ),  # 0
        ("PktRcvd", c_uint32, 1 ),  # 1
        ("AbortErr", c_uint32, 1 ),  # 2
        ("Lenen", c_uint32, 1 ),  # 3
        ("Crcerr", c_uint32, 1 ),  # 4
        ("Adrserr", c_uint32, 1 ),  # 5
        ("rfu", c_uint32, 2 ),  # 6, 7
        ("RxLen", c_uint32, 8 ),  # 8 - 15
        ("RssiAvg", c_uint32, 8 ),  # 16 - 23
        ("RssiSync", c_uint32, 8 ),  # 24 - 31
    ]

class RxStatus( ctypes.Union ):
     _anonymous_ = ("bit",)
     _fields_ = [
        ("bit",    RxStatus_bits),
        ("asWord", c_uint32    )
    ]

class IrqFlags_bits( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("rfu01", c_uint32, 2 ),  # 0, 1
        ("TxDone", c_uint32, 1 ),  # 2 Packet transmission completed
        ("RxDone", c_uint32, 1 ),  # 3 Packet received
        ("PreambleDetected", c_uint32, 1 ),  # 4 Preamble detected
        ("SyncWordValid", c_uint32, 1 ),  # 5 sync word / LoRa® header detected
        ("HeaderErr", c_uint32, 1 ),  # 6 LoRa header CRC error
        ("Err", c_uint32, 1 ),  # 7 Packet received with error.  LoRa: Wrong CRC received (G)FSK: CRC error
        ("CadDone", c_uint32, 1 ),  # 8 LoRa Channel activity detection finished
        ("CadDetected", c_uint32, 1 ),  # 9 LoRa Channel activity detected
        ("Timeout", c_uint32, 1 ),  # 10 RX or TX timeout
        ("LrFhssHop", c_uint32, 1 ),  # 11 LR-FHSS intra-packet hopping
        ("res12_18", c_uint32, 7 ),  # 12, 13, 14, 15, 16, 17, 18
        ("GNSSDone", c_uint32, 1 ),  # 19 GNSS Scan finished
        ("WifiDone", c_uint32, 1 ),  # 20 Wi-Fi Scan finished
        ("LBD", c_uint32, 1 ),  # 21 Low Battery Detection
        ("CmdError", c_uint32, 1 ),  # 22 Host command error
        ("Error", c_uint32, 1 ),  # 23 An error other than a command error occurred (see GetErrors)
        ("FskLenError", c_uint32, 1 ),  # 24 the packet was received with a length error
        ("FskAddrError", c_uint32, 1 ),  # 25 the packet was received with an address error
        ("rfu", c_uint32, 5 ),  # 26, 27, 28, 29, 31
    ]

class IrqFlags( ctypes.Union ):
     _anonymous_ = ("bit",)
     _fields_ = [
        ("bit",    IrqFlags_bits),
        ("asWord", c_uint32    )
    ]

class Stat1_bits( ctypes.LittleEndianStructure ):
    _fields_ = [
                ("intActive",      c_uint8, 1 ),  # 
                ("cmdStatus", c_uint8, 3 ),  # 
                ("RFU",      c_uint8, 4 ),  # 
               ]

class Stat1( ctypes.Union ):
     _anonymous_ = ("bit",)
     _fields_ = [
                 ("bit",    Stat1_bits ),
                 ("asByte", c_uint8    )
                ]

class Stat2_bits( ctypes.LittleEndianStructure ):
    _fields_ = [
                ("bootLoader",  c_uint8, 1 ),  # 
                ("chipMode",    c_uint8, 3 ),  # 
                ("resetStatus", c_uint8, 4 ),  # 
               ]

class Stat2( ctypes.Union ):
     _anonymous_ = ("bit",)
     _fields_ = [
                 ("bit",    Stat2_bits ),
                 ("asByte", c_uint8    )
                ]

class SleepConfig_bits( ctypes.LittleEndianStructure ):
    _fields_ = [
                ("retention", c_uint8, 1 ),  #
                ("wakeup",    c_uint8, 1 ),  #
                ("RFU",       c_uint8, 6 ),  #
               ]

class SleepConfig( ctypes.Union ):
     _anonymous_ = ("bit",)
     _fields_ = [
                 ("bit",    SleepConfig_bits ),
                 ("asByte", c_uint8    )
                ]

class CalibParams_bits( ctypes.LittleEndianStructure ):
    _fields_ = [
                ("LF_RC",  c_uint8, 1 ),  # 
                ("HF_RC",  c_uint8, 1 ),  # 
                ("PLL",    c_uint8, 1 ),  # 
                ("ADC",    c_uint8, 1 ),  # 
                ("IMG",    c_uint8, 1 ),  # 
                ("PLL_TX", c_uint8, 1 ),  # 
                ("RFU",    c_uint8, 2 ),  # 
               ]

class CalibParams( ctypes.Union ):
     _anonymous_ = ("bit",)
     _fields_ = [
                 ("bit",    CalibParams_bits),
                 ("asByte", c_uint8    )
                ]

class LfClkConfig_bits( ctypes.LittleEndianStructure ):
    _fields_ = [
                ("clkSel",      c_uint8, 2 ),  # 
                ("releaseBusy", c_uint8, 1 ),  # 
                ("RFU",         c_uint8, 5 ),  # 
               ]

class LfClkConfig( ctypes.Union ):
     _anonymous_ = ("bit",)
     _fields_ = [
                 ("bit",    LfClkConfig_bits),
                 ("asByte", c_uint8    )
                ]

# High level analyzers must subclass the HighLevelAnalyzer class.
class Hla(HighLevelAnalyzer):
    fsk_bwDict = {
        0x1f: 4800,
        0x17: 5800,
        0x0f: 7300,
        0x1e: 9700,
        0x16: 11700,
        0x0e: 14600,
        0x1d: 19500,
        0x15: 23400,
        0x0d: 29300,
        0x1c: 39000,
        0x14: 46900,
        0x0c: 58600,
        0x1b: 78200,
        0x13: 93800,
        0x0b: 117300,
        0x1a: 156200,
        0x12: 187200,
        0x0a: 234300,
        0x19: 312000,
        0x11: 373600,
        0x09: 476000,
    }

    regDict = {
        0x0080036c: 'RegulatorMode',
        0x008003b8: 'GnssConst',
        0x008004b4: 'GnssMode',
        0x008008ec: 'GnssAssistLat',
        0x008008f0: 'GnssAssistLon',
        0x00f0003c: 'Txco',
        0x00f03018: 'Dio5',
        0x00f0301c: 'Dio6',
        0x00f03020: 'Dio7',
        0x00f03024: 'Dio8',
        0x00f0302c: 'Dio10',
        0x00f04014: 'Counter',
        0x00f20124: 'FskBWF',
        0x00f20314: 'FskCfg0',
        0x00f20338: 'FskBitrate',
        0x00f2033c: 'FskFdev',
        0x00f2034c: 'FskCfg1', # gfsk preambleDetect, gfsk preambleLength
        0x00f20350: 'FskCfg2', # gfsk sync word length (in bits)
        0x00f20354: 'FskSyncLo', # gfsk sync word lo
        0x00f20358: 'FskSyncHi', # gfsk sync word hi
        0x00f2035c: 'FskCfg3',   # gfsk fixlen/varlen
        0x00f20360: 'PayloadLengthLo', # lowest 8bits  todo:tx-or-rx?
        0x00f20368: 'PayloadLengthHi', # payload-length-bits[27:20], addrComp:[17:16]
        0x00f20370: 'FskCfg5',  # gfsk whitening, crcType
        0x00f20374: 'FskCrcPoly',
        0x00f20378: 'FskCrcInit',
        0x00f20414: 'LoRaCfg0',
        0x00f2041c: 'LoRaCfg1',
        0x00f20420: 'LoRaCfgA',
        0x00f20428: 'LoRaCfgB',
        0x00f20460: 'LoRaSync',
        0x00f30058: 'RfFreq',
        0x00f30074: 'TxParamsA',
        0x00f30078: 'TxParamsB',
        0x00f30080: 'TxParamsC',
        0x00f30088: 'TxParamsD',
        0x00F20384: 'rxAddrPtr',
        0x00F20368: 'payloadLength',
    }

    lora_bws = {
        0x00: '7.81',
        0x08: '10.42',
        0x01: '15.63',
        0x09: '20.8',
        0x02: '31.25',
        0x0a: '41.67',
        0x03: '62.5',
        0x04: '125',
        0x05: '250',
        0x06: '500',
    }

    crs = {
        0x01: 'short-CR4/5',
        0x02: 'short-CR4/6',
        0x03: 'short-CR4/7',
        0x04: 'short-CR4/8',
        0x05: 'long-CR4/5',
        0x06: 'long-CR4/6',
        0x07: 'long-CR4/8',
    }

    def parseStatus(self, half):
        stat1 = Stat1()
        stat1.asByte = self.ba_miso[0]
        if stat1.cmdStatus == 0:
            cmdStatStr = 'CMD_FAIL'
        elif stat1.cmdStatus == 1:
            cmdStatStr = 'CMD_PERR'
        elif stat1.cmdStatus == 2:
            cmdStatStr = 'CMD_OK'
        elif stat1.cmdStatus == 3:
            cmdStatStr = 'CMD_DAT'
        else:
            cmdStatStr = '?' + str(stat1.cmdStatus) + '?'

        if stat1.intActive == 1:
            my_str = 'intActive  '
        else:
            my_str = ''

        my_str = my_str + cmdStatStr
        if half == 1:
            return my_str

        stat2 = Stat2()
        stat2.asByte = self.ba_miso[1]
        if stat2.resetStatus == 0:
            resetStr = 'no-reset'
        elif stat2.resetStatus == 1:
            resetStr = 'analog-reset'
        elif stat2.resetStatus == 2:
            resetStr = 'NRESET-pin'
        elif stat2.resetStatus == 3:
            resetStr = 'system-reset'
        elif stat2.resetStatus == 4:
            resetStr = 'watchdog-reset'
        elif stat2.resetStatus == 5:
            resetStr = 'nSS-wakeup'
        elif stat2.resetStatus == 6:
            resetStr = 'RTC-restart'
        else:
            resetStr = '?' + str(stat2.resetStatus) + '?'

        if stat2.chipMode == 0:
            cmStr = 'sleep'
        elif stat2.chipMode == 1:
            cmStr = 'STBY_RC'
        elif stat2.chipMode == 2:
            cmStr = 'STBY_XOSC'
        elif stat2.chipMode == 3:
            cmStr = 'FS'
        elif stat2.chipMode == 4:
            cmStr = 'RX'
        elif stat2.chipMode == 5:
            cmStr = 'TX'
        elif stat2.chipMode == 6:
            cmStr = 'sniff'
        else:
            cmStr = '?' + str(stat2.chipMode) + '?'

        my_str = my_str + ' ' + resetStr + '  ' + cmStr 
        if stat2.bootLoader == 0:
            my_str = my_str + ' BOOT'
        return my_str

    def parseIrqs(self, word):
        f = IrqFlags()
        f.asWord = word
        mystr = ''
        if f.rfu01 == 1:
            mystr = mystr + 'rfu01 '
        if f.TxDone == 1:
            mystr = mystr + 'TxDone '
        if f.RxDone == 1:
            mystr = mystr + 'RxDone '
        if f.PreambleDetected == 1:
            mystr = mystr + 'PreambleDetected '
        if f.SyncWordValid == 1:
            mystr = mystr + 'SyncWordValid '
        if f.HeaderErr == 1:
            mystr = mystr + 'HeaderErr '
        if f.Err == 1:
            mystr = mystr + 'Err '
        if f.CadDone == 1:
            mystr = mystr + 'CadDone '
        if f.CadDetected == 1:
            mystr = mystr + 'CadDetected '
        if f.Timeout == 1:
            mystr = mystr + 'Timeout '
        if f.LrFhssHop == 1:
            mystr = mystr + 'LrFhssHop '
        if f.res12_18 == 1:
            mystr = mystr + 'res12_18 '
        if f.GNSSDone == 1:
            mystr = mystr + 'GNSSDone '
        if f.WifiDone == 1:
            mystr = mystr + 'WifiDone '
        if f.LBD == 1:
            mystr = mystr + 'LBD '
        if f.CmdError == 1:
            mystr = mystr + 'CmdError '
        if f.Error == 1:
            mystr = mystr + 'Error '
        if f.FskLenError == 1:
            mystr = mystr + 'FskLenError '
        if f.FskAddrError == 1:
            mystr = mystr + 'FskAddrError '
        if f.rfu == 1:
            mystr = mystr + 'rfu '

        if len(mystr) > 80: # too much text for one line (TODO find newline character)
            return hex(f.asWord)
        else:
            return mystr

    def GetRxBufferStatus(self):
        self.next_transfer_response = 1
        return 'GetRxBufferStatus'

    def GetPacketStatus(self):
        self.next_transfer_response = 1
        return 'GetPacketStatus'

    def GetRssiInst(self):
        self.next_transfer_response = 1
        return 'GetRssiInst'

    def SetGfskSyncWord(self):
        syncWord = int.from_bytes(bytearray(self.ba_mosi[2:10]), 'big')
        return 'SetGfskSyncWord ' + hex(syncWord)

    def SetLoRaPublicNetwork(self):
        # lr11xx_radio_lora_network_type_t
        ntDict = { 0: 'PRIVATE', 1: 'PUBLIC' }
        return 'SetLoRaPublicNetwork ' + ntDict.get(self.ba_mosi[2], hex(self.ba_mosi[2])+'?')

    def SetRx(self):
        timeout = int.from_bytes(bytearray(self.ba_mosi[2:5]), 'big')
        if timeout == 0xffffff:
            _str = 'continuous'
        elif timeout == 0:
            _str = 'single'
        else:
            us = timeout * .03052
            _str = ('%.3f' % us) + 'ms' # 'μs'
        return 'SetRx ' + _str

    def SetTx(self):
        timeout = int.from_bytes(bytearray(self.ba_mosi[2:5]), 'big')
        _str = ''
        if timeout != 0:
            us = timeout * .03052
            _str = ('%.3f' % us) + 'ms' # 'μs'
        return 'SetTx ' + _str

    def SetRfFrequency(self):
        hz = int.from_bytes(bytearray(self.ba_mosi[2:6]), 'big')
        return 'SetRfFrequency %.3f' % (hz / 1000000) + 'MHz'

    def AutoTxRx(self):
        im = {
            0: 'SLEEP',
            1: 'STANDBY_RC',
            2: 'STANDBY_XOSC',
            3: 'FS',
        }
        delay = int.from_bytes(bytearray(self.ba_mosi[2:5]), 'big')
        intermediary_mode = self.ba_mosi[5] # lr11xx_radio_intermediary_mode_t
        timeout = int.from_bytes(bytearray(self.ba_mosi[6:9]), 'big')
        return 'AutoTxRx delay ' + str(delay) + ', intermediary ' + im.get(intermediary_mode, hex(intermediary_mode)+'?') + ', timeout ' + str(timeout)

    def SetSleep(self):
        cfg = SleepConfig()
        cfg.asByte = self.ba_mosi[1]
        my_str = 'SetSleep '
        if cfg.rtc_wakeup == 1:
            my_str = 'RTC wakeup '
        if cfg.warm_start == 1:
            my_str = my_str + 'warm-start' # device config retention
        else:
            my_str = my_str + 'cold-start'
        return my_str

    tuneDict = {
        0: 1.6,
        1: 1.7,
        2: 1.8,
        3: 2.2,
        4: 2.4,
        5: 2.7,
        6: 3.0,
        7: 3.3,
    }

    def GetStatus(self):
        return 'GetStatus'

    def GetVersion(self):
        self.next_transfer_response = 1
        return 'GetVersion (request)'

    def WriteRegMem32(self):
        addr = int.from_bytes(bytearray(self.ba_mosi[2:6]), 'big')
        _len = len(self.ba_mosi) - 6 # two byte command, four byte address
        return 'WriteRegMem32 '+ hex(addr)+', ' + str(_len) + ' data bytes'

    def WriteRegMem8(self):
        addr = int.from_bytes(bytearray(self.ba_mosi[2:6]), 'big')
        _len = len(self.ba_mosi) - 6 # two byte command, four byte address
        return 'WriteRegMem8 '+ hex(addr)+', ' + str(_len) + ' data bytes'

    def ReadRegMem32(self):
        self.next_transfer_response = 1
        addr = int.from_bytes(bytearray(self.ba_mosi[2:6]), 'big')
        l = self.ba_mosi[6]
        return 'ReadRegMem32 ' + hex(addr) + ', ' + str(l);

    def ReadRegMem8(self):
        self.next_transfer_response = 1
        addr = int.from_bytes(bytearray(self.ba_mosi[2:6]), 'big')
        l = self.ba_mosi[6]
        return 'ReadRegMem8 ' + hex(addr) + ', ' + str(l);

    def ClearRxBuffer(self):
        return 'ClearRxBuffer'

    def ReadBuffer8(self):
        self.next_transfer_response = 1
        offset = self.ba_mosi[2]
        Len = self.ba_mosi[3]
        return 'ReadBuffer8 ' + str(Len) + 'bytes at ' + hex(offset)

    def WriteBuffer8(self):
        return 'WriteBuffer8 ' + str(len(self.ba_mosi)-2)

    def WriteRegMemMask32(self):
        addr = int.from_bytes(bytearray(self.ba_mosi[2:6]), 'big')
        mask = int.from_bytes(bytearray(self.ba_mosi[6:10]), 'big')
        data = int.from_bytes(bytearray(self.ba_mosi[10:14]), 'big')
        return 'WriteRegMemMask32 ' + hex(addr) + ', ' + hex(mask) + ', ' + hex(data)

    def GetErrors(self):
        self.next_transfer_response = 1
        return 'GetErrors (request)'

    def ClearErrors(self):
        return 'ClearErrors'

    def Calibrate(self):
        cal = CalibParams()
        cal.asByte = self.ba_mosi[2]
        my_str = ''
        if cal.PLL_TX == 1:
            my_str = my_str + 'PLL_TX '
        if cal.IMG == 1:
            my_str = my_str + 'IMG '
        if cal.ADC == 1:
            my_str = my_str + 'ADC '
        if cal.PLL == 1:
            my_str = my_str + 'PLL '
        if cal.HF_RC == 1:
            my_str = my_str + 'HF_RC '
        if cal.LF_RC == 1:
            my_str = my_str + 'LF_RC '
        return 'Calibrate ' + my_str

    def SetRegMode(self):
        regMode = self.ba_mosi[2]
        if regMode == 0:
            my_str = 'LDO'
        elif regMode == 1:
            my_str = 'DC-DC'
        else:
            my_str = '?' + hex(regMode) + '?'
        return 'SetRegMode ' + my_str

    def ClearIrq(self):
        return 'ClearIrq ' + self.parseIrqs(int.from_bytes(bytearray(self.ba_mosi[2:6]), 'big'))

    def CalibImage(self):
        freq1 = self.ba_mosi[2]
        if freq1 == 0x6b:
            str1 = '430-440'
        elif freq1 == 0x75:
            str1 = '470-510'
        elif freq1 == 0xc1:
            str1 = '779-787'
        elif freq1 == 0xd7:
            str1 = '863-870'
        elif freq1 == 0xe1:
            str1 = '902-928'
        else:
            str1 = hex(freq1)
        freq2 = self.ba_mosi[3]
        if freq2 == 0x6e:
            str2 = '430-440'
        elif freq2 == 0x81:
            str2 = '470-510'
        elif freq2 == 0xc5:
            str2 = '779-787'
        elif freq2 == 0xd8:
            str2 = '863-870'
        elif freq2 == 0xe9:
            str2 = '902-928'
        else:
            str2 = hex(freq2)
        return 'CalibImage '  + str1 + ', ' + str2

    def SetDioAsRfSwitch(self):
        enable = self.ba_mosi[2]
        standby = self.ba_mosi[3]
        rx = self.ba_mosi[4]
        tx = self.ba_mosi[5]
        tx_hp = self.ba_mosi[6] # high power transmit
        tx_hf = self.ba_mosi[7] # high frequency transmit
        gnss = self.ba_mosi[8]
        wifi = self.ba_mosi[9]
        return f'SetDioAsRfSwitch enable=0x{enable:02x} standby=0x{standby:02x} rx=0x{rx:02x} tx=0x{tx:02x} tx_hp=0x{tx_hp:02x} tx_hf=0x{tx_hf:02x} gnss=0x{gnss:02x} wifi=0x{wifi:02x}'

    def SetDioIrqParams(self):
        irq1 = int.from_bytes(bytearray(self.ba_mosi[2:6]), 'big')
        irq2 = int.from_bytes(bytearray(self.ba_mosi[6:10]), 'big')
        return 'SetDioIrqParams ' + hex(irq1) + ', ' + hex(irq2)

    def ConfigLfClock(self):
        cfg = LfClkConfig()
        cfg.asByte = self.ba_mosi[2]
        if cfg.clkSel == 0:
            my_str = 'use 32KHz_RC'
        elif cfg.clkSel == 1:
            my_str = 'use 32KHz_xtal'
        elif cfg.clkSel == 2:
            my_str = 'use DIO11_32KHz'
        else:
            my_str = '?' + hex(cfg.clkSel) + '?'

        if cfg.releaseBusy == 1:
            my_str = my_str + ' ready-before-nBUSY'

        return 'ConfigLfClock ' + my_str

    def SetTcxoMode(self):
        tune = self.ba_mosi[2]
        delay = int.from_bytes(bytearray(self.ba_mosi[3:6]), 'big')
        volts = self.tuneDict[tune]
        return 'SetTcxoMode ' + str(volts) + 'v %.3f' % (delay * 0.03052) + 'ms'

    def Reboot(self):
        stay_in_bootloader = self.ba_mosi[2]
        _str = ''
        if stay_in_bootloader == 3:
            _str = 'stay_in_bootloader'
        elif stay_in_bootloader != 0:
            _str = hex(stay_in_bootloader) + '?'
        return 'Reboot ' + _str

    def GetVbat(self):
        self.next_transfer_response = 1
        return 'GetVbat (request)'

    def GetTemp(self):
        self.next_transfer_response = 1
        return 'GetTemp (request)'

    def SetSleep(self):
        cfg = SleepConfig()
        cfg.asByte = self.ba_mosi[2]
        my_str = 'SetSleep '
        if cfg.retention == 1:
            my_str = my_str + 'retention '
        if cfg.wakeup == 1:
            my_str = my_str + 'wakeup '
        sleepTime = int.from_bytes(bytearray(self.ba_mosi[3:7]), 'big')
        my_str = my_str + ' %.3f' % (sleepTime * .03052) + 'ms'
        return my_str

    def SetStandby(self):
        cfg = self.ba_mosi[2]
        if cfg == 0:
            my_str = 'STBY_RC'
        elif cfg == 1:
            my_str = 'STBY_XOSC'
        else:
            my_str = '?' + hex(cfg) + '?'
        return 'SetStandby ' + my_str

    def SetFs(self):
        return 'SetFs'

    def GetRandomNumber(self):
        self.next_transfer_response = 1
        return 'GetRandomNumber (request)'

    def EraseFlash(self):
        return 'EraseFlash'

    def WriteFlashEncrypted(self):
        offset = int.from_bytes(bytearray(self.ba_mosi[2:6]), 'big')
        length_bytes = len(self.ba_mosi) - 6
        length_words = length_bytes // 4
        return f'WriteFlashEncrypted offset=0x{offset:08x} length={length_words} words ({length_bytes} bytes)'

    def GetPin(self):
        self.next_transfer_response = 1
        return 'GetPin (request)'

    def ReadChipEui(self):
        self.next_transfer_response = 1
        return 'ReadChipEui (request)'

    def ReadJoinEui(self):
        self.next_transfer_response = 1
        return 'ReadJoinEui (request)'

    def EraseInfoPage(self):
        ipDict = { 0: 'INFOPAGE_0', 1: 'INFOPAGE_1' }
        infopage_id = self.ba_mosi[2]
        return 'EraseInfoPage ' + ipDict.get(infopage_id, hex(infopage_id)+'?')

    def WriteInfoPage(self):
        ipDict = { 0: 'INFOPAGE_0', 1: 'INFOPAGE_1' }
        infopage_id = self.ba_mosi[2]
        address = int.from_bytes(bytearray(self.ba_mosi[3:5]), 'big')
        length_bytes = len(self.ba_mosi) - 5
        length_words = length_bytes // 4
        return f'WriteInfoPage {ipDict.get(infopage_id, hex(infopage_id)+"?")} address=0x{address:04x} length={length_words} words ({length_bytes} bytes)'

    def ReadInfoPage(self):
        ipDict = { 0: 'INFOPAGE_0', 1: 'INFOPAGE_1' }
        self.next_transfer_response = 1
        infopage_id = self.ba_mosi[2] # lr11xx_system_infopage_id_t
        address = int.from_bytes(bytearray(self.ba_mosi[3:5]), 'big')
        length = self.ba_mosi[5]
        return 'ReadInfoPage infopage_id ' + ipDict.get(infopage_id, hex(infopage_id)+'?') + ', address ' + hex(address) + ', length ' + str(length)

    def GetChipEui(self):
        self.next_transfer_response = 1
        return 'GetChipEui (request)'

    def GetSemtechJoinEui(self):
        self.next_transfer_response = 1
        return 'GetSemtechJoinEui (request)'

    def DeriveRootKeysAndGetPin(self):
        self.next_transfer_response = 1
        if len(self.ba_mosi) > 2:
            dev_eui = int.from_bytes(bytearray(self.ba_miso[2:10]), 'big')
            join_eui = int.from_bytes(bytearray(self.ba_miso[10:18]), 'big')
            _str = 'dev_eui ' + hex(dev_eui) + ', join_eui ' + hex(join_eui)
        else:
            _str = '(request)'

        return 'DeriveRootKeysAndGetPin ' + _str

    def EnableSpiCrc(self):
        ed = { 0: 'disable', 1: 'enable_crc' }
        return 'EnableSpiCrc ' + ed.get(self.ba_mosi[2], hex(self.ba_mosi[2])+'?')

    def DriveDiosInSleepMode(self):
        ena = self.ba_mosi[2]
        _str = 'DriveDiosInSleepMode '
        if ena:
            _str = _str + 'pulled'
        else:
            _str = _str + 'floating'
        return _str

    def ResetStats(self):
        return 'ResetStats'

    def GetStats(self):
        self.next_transfer_response = 1
        return 'GetStats (request)'

    def GetPacketType(self):
        self.next_transfer_response = 1
        return 'GetPacketType (request)'

    def SetCadParams(self):
        my_str = str(self.ba_mosi[2]) + ' symbols'
        my_str = my_str + ' peak:' + str(self.ba_mosi[3])
        my_str = my_str + ' min:' + str(self.ba_mosi[4])
        ce = self.ba_mosi[5]
        if ce == 0:
            cadStr = 'CAD_ONLY'
        elif ce == 1:
            cadStr = 'CAD_RX'
        elif ce == 16:
            cadStr = 'CAD_LBT'
        else:
            cadStr = '?' + hex(ce) + '?'
        my_str = my_str + ' exit:' + cadStr
        cadTimeout = int.from_bytes(bytearray(self.ba_mosi[6:8]), 'big')
        my_str = my_str + ' ' + hex(cadTimeout)
        return 'SetCadParams ' + my_str

    rampDict = {
        0: 16,
        1: 32,
        2: 48,
        3: 64,
        4: 80,
        5: 96,
        6: 112,
        7: 128,
        8: 144,
        9: 160,
        10: 176,
        11: 192,
        12: 208,
        13: 240,
        14: 272,
        15: 304,
    }

    def SetPacketType(self):
        self.pt = PacketType(self.ba_mosi[2])
        return 'SetPacketType ' + self.pt.name

    def SetModulationParams(self):
        if self.pt == PacketType.FSK:
            _len = len(self.ba_mosi)
            if _len < 12:
                return 'SetModulationParams error, need 12 mosi bytes, have ' + str(_len)
            br = int.from_bytes(bytearray(self.ba_mosi[2:6]), 'big')
            my_str = str(br) + 'bps '
            bt = self.ba_mosi[6]
            if bt == 0:
                my_str = my_str + 'BT-OFF'
            elif bt == 8:
                my_str = my_str + 'BT0.3'
            elif bt == 9:
                my_str = my_str + 'BT0.5'
            elif bt == 10:
                my_str = my_str + 'BT0.7'
            elif bt == 11:
                my_str = my_str + 'BT1.0'
            else:
                my_str = my_str + '?' + hex(bt) + '?'
            bw = self.fsk_bwDict.get(self.ba_mosi[7], self.ba_mosi[7])
            my_str = my_str + ' rxbw:' + str(bw) + 'Hz '
            fdev = int.from_bytes(bytearray(self.ba_mosi[8:12]), 'big')
            my_str = my_str + 'fdev:' + str(fdev) + 'Hz'
        elif self.pt == PacketType.LORA or self.pt == PacketType.RTTOF:
            sf = self.ba_mosi[2]
            my_str = 'SF' + str(sf)
            bw = self.ba_mosi[3]
            my_str = my_str + ' bw ' + self.lora_bws.get(bw, hex(bw)+'?') + 'KHz'
            cr = self.ba_mosi[4]
            my_str = my_str + ' ' + self.crs.get(cr, hex(cr)+'?') + ' '
            ldro = self.ba_mosi[5]
            if ldro == 0:
                my_str = my_str + 'LDRO_OFF'
            elif ldro == 1:
                my_str = my_str + 'LDRO_ON'
            else:
                my_str = my_str + '?' + hex(ldro) + '?'
        elif self.pt == PacketType.BPSK:
            # lr11xx_radio_mod_params_bpsk_t
            br_in_bps = int.from_bytes(bytearray(self.ba_mosi[2:6]), 'big')
            pulse_shape = self.ba_mosi[6] #  lr11xx_radio_bpsk_pulse_shape_t
            my_str = str(br_in_bps) + ' bps '
            if pulse_shape == 0x16: # LR11XX_RADIO_DBPSK_PULSE_SHAPE
                my_str = my_str + ' Double OSR / RRC / BT 0.7'
            else:
                my_str = my_str + hex(pulse_shape) + '?'
        else:
            my_str = 'TODO pktType ' + self.pt.name
        return 'SetModulationParams ' + my_str

    def SetPacketParams(self):
        if self.pt == PacketType.FSK:
            preambleLength = int.from_bytes(bytearray(self.ba_mosi[2:4]), 'big')
            my_str = 'preamble TX ' + str(preambleLength)
            detect = self.ba_mosi[4]
            if detect == 0:
                n_bits = 'OFF'
            elif detect == 4:
                n_bits = '8'
            elif detect == 5:
                n_bits = '16 '
            elif detect == 6:
                n_bits = '24'
            elif detect == 7:
                n_bits = '32'
            else:
                n_bits = '?' + hex(detect) + '?'
            my_str = my_str + ' detect ' + n_bits + 'bits '
            syncWordBits = self.ba_mosi[5]
            my_str = my_str + ' syncWord ' + str(syncWordBits) + 'bits '
            addrComp = self.ba_mosi[6]
            if addrComp == 0:
                addrFilt = 'OFF'
            elif addrComp == 1:
                addrFilt = 'node'
            elif addrComp == 2:
                addrFilt = 'node & bcast'
            else:
                addrFilt = '?'
            my_str = my_str + ' addrFilt ' + addrFilt
            pktType = self.ba_mosi[7]
            if pktType == 0:
                my_str = my_str + ' fixLen'
            elif pktType == 1:
                my_str = my_str + ' varLen-8bit'
            elif pktType == 2:
                my_str = my_str + ' varLen-9bit'
            else:
                my_str = my_str + '?' + hex(pktType) + '?'
            payLen = self.ba_mosi[8]
            my_str = my_str + ' payLen ' + str(payLen)
            crcType = self.ba_mosi[9]
            if crcType == 1:
                crc = 'OFF'
            elif crcType == 0:
                crc = '1_BYTE'
            elif crcType == 2:
                crc = '2_BYTE'
            elif crcType == 4:
                crc = '1_BYTE_INV'
            elif crcType == 6:
                crc = '2_BYTE_INV'
            else:
                crc = hex(crcType)
            my_str = my_str + ' CRC ' + str(crc)
            dcFree = self.ba_mosi[10]
            if dcFree == 1:
                my_str = my_str + ' dcFree'
        elif self.pt == PacketType.LORA or self.pt == PacketType.RTTOF:
            preambleLength = int.from_bytes(bytearray(self.ba_mosi[2:4]), 'big')
            my_str = 'preamble ' + str(preambleLength)
            headerType = self.ba_mosi[4]
            if headerType == 0:
                hdrStr = 'varLen'
            elif headerType == 1:
                hdrStr = 'fixrLen'
            else:
                hdrStr = hex(headerType)
            my_str = my_str + ' header ' + hdrStr
            payLen = self.ba_mosi[5]
            my_str = my_str + ' payLen' + str(payLen)
            crcOn = self.ba_mosi[6]
            if crcOn == 0:
                crcStr = 'ON'
            elif crcOn == 1:
                crcStr = 'OFF'
            else:
                crcStr = hex(crcOn)
            my_str = my_str + ' CRC_' + crcStr
            iqInv= self.ba_mosi[7]
            if iqInv == 0:
                iqStr = 'STD'
            elif iqInv == 1:
                iqStr = 'INV'
            else:
                iqStr = hex(iqInv)
            my_str = my_str + ' IQ ' + iqStr
        elif self.pt == PacketType.BPSK:
            # lr11xx_radio_pkt_params_bpsk_t
            pld_len_in_bytes = self.ba_mosi[2]
            ramp_up_delay = int.from_bytes(bytearray(self.ba_mosi[3:5]), 'big')
            ramp_down_delay = int.from_bytes(bytearray(self.ba_mosi[5:7]), 'big')
            pld_len_in_bits = int.from_bytes(bytearray(self.ba_mosi[7:9]), 'big')
            my_str = 'payload length ' + str(pld_len_in_bytes) + ' bytes ' +str(pld_len_in_bits)+ ' bits, '
            my_str = my_str + 'ramp_up_delay ' +str(ramp_up_delay)+', ramp_down_delay '+str(ramp_down_delay)
        else:
            my_str = 'TODO pktType ' + self.pt.name
        return 'SetPacketParams ' + my_str

    def SetTxParams(self):
        txp = self.ba_mosi[2]
        if txp > 127:
            dBm = txp - 256
        else:
            dBm = txp
        return 'SetTxParams ' + str(dBm) + 'dBm ' + str(self.rampDict[self.ba_mosi[3]]) + 'μs'

    def SetPacketAdrs(self):
        node_address = self.ba_mosi[2]
        broadcast_address = self.ba_mosi[3]
        return 'SetPacketAdrs node_address ' + hex(node_address) + ', broadcast_address ' + hex(broadcast_address)

    def SetRxTxFallbackMode(self):
        mode = self.ba_mosi[2]
        if mode == 1:
            my_str = 'STBY_RC'
        elif mode == 2:
            my_str = 'STBY_XOSC'
        elif mode == 3:
            my_str = 'FS'
        else:
            my_str = '?' + hex(mode) + '?'
        return 'SetRxTxFallbackMode ' + my_str

    def SetRxDutyCycle(self):
        dcModeDict = { 0: 'RX', 1: 'CAD' } # lr11xx_radio_rx_duty_cycle_mode_t
        rx_period_in_rtc_step = int.from_bytes(bytearray(self.ba_mosi[2:5]), 'big')
        sleep_period_in_rtc_step = int.from_bytes(bytearray(self.ba_mosi[5:8]), 'big')
        mode = self.ba_mosi[8]
        return 'SetRxDutyCycle rx_period ' + str(rx_period_in_rtc_step) + ', sleep_period ' + str(sleep_period_in_rtc_step) + ', mode ' + dcModeDict.get(mode, hex(mode)+'?')

    def SetPaConfig(self):
        paSel = self.ba_mosi[2]
        paSupply = self.ba_mosi[3]
        paDuty= self.ba_mosi[4]
        hpSel = self.ba_mosi[4]
        if paSel == 0:
            my_str = 'low-power '
        if paSel == 1:
            my_str = 'hi-power '
        else:
            my_str = '?' + hex(paSel) + '? '
        if paSupply == 0:
            my_str = my_str + 'int-reg'
        if paSupply == 1:
            my_str = my_str + 'VBAT'
        else:
            my_str = my_str + '?' + hex(paSupply) + '?'
        my_str = my_str + ' duty ' + str(paDuty)
        my_str = my_str + ' hpSel ' + str(hpSel)
        return 'SetPaConfig ' + my_str

    def StopTimeoutOnPreamble(self):
        stop = self.ba_mosi[2]
        if stop == 0:
            my_str = 'stop-on-sync/header'
        elif stop == 1:
            my_str = 'stop-on-preamble'
        else:
            my_str = '?' + hex(stop) + '?'
        return 'StopTimeoutOnPreamble ' + my_str

    def SetCad(self):
        return 'SetCad'

    def SetTxCw(self):
        return 'SetTxCw'

    def SetTxInfinitePreamble(self):
        return 'SetTxInfinitePreamble'

    def SetLoRaSynchTimeout(self):
        return 'SetLoRaSynchTimeout ' + str(self.ba_mosi[2]) + ' symbols'

    def SetRangingAddr(self):
        address = int.from_bytes(bytearray(self.ba_mosi[2:6]), 'big')
        return 'SetRangingAddr address ' + hex(address) + ', check_length ' + str(self.ba_mosi[6])

    def SetRangingReqAddr(self):
        request_address = int.from_bytes(bytearray(self.ba_mosi[2:6]), 'big')
        return 'SetRangingReqAddr request_address ' + hex(request_address)

    def GetRangingResult(self):
        self.next_transfer_response = 1
        rt = { 0: 'RAW', 1: 'RSSI' } # lr11xx_rttof_result_type_t
        self.ranging_result_type = self.ba_mosi[2]
        return 'GetRangingResult ' + rt.get(self.ba_mosi[2], hex(self.ba_mosi[2])+'?')

    def SetRangingTxRxDelay(self):
        delay_indicator = int.from_bytes(bytearray(self.ba_mosi[2:6]), 'big')
        return 'SetRangingTxRxDelay ' + str(delay_indicator)

    def GnssReadRssiTest(self):
        self.next_transfer_response = 1
        path = self.ba_mosi[2]
        return f'GnssReadRssiTest path=0x{path:02x}'

    def SetGfskCrcParams(self):
        seed = int.from_bytes(bytearray(self.ba_mosi[2:6]), 'big')
        polynomial = int.from_bytes(bytearray(self.ba_mosi[6:10]), 'big')
        return f'SetGfskCrcParams seed=0x{seed:08x} polynomial=0x{polynomial:08x}'

    def SetGfskWhiteningParams(self):
        seed = int.from_bytes(bytearray(self.ba_mosi[2:4]), 'big')
        return f'SetGfskWhiteningParams seed=0x{seed:04x}'

    def SetRxBoosted(self):
        en = self.ba_mosi[2]
        if en == 0:
            my_str = 'OFF'
        elif en == 1:
            my_str = 'DN'
        else:
            my_str = '?' + hex(en) + '?'
        return 'SetRxBoosted ' + my_str

    def SetRangingParameter(self):
        nb_symbols = self.ba_mosi[3]
        return 'SetRangingParameter nb_symbols ' + str(nb_symbols)

    def SetRssiCalibration(self):
        print('SetRssiCalibration:')
        g5 = self.ba_mosi[2] >> 4
        g4 = self.ba_mosi[2] & 0x0f
        g7 = self.ba_mosi[3] >> 4
        g6 = self.ba_mosi[3] & 0x0f
        print(f'g4: {g4}, g5: {g5}, g6: {g6}, g7: {g7}')

        g9 = self.ba_mosi[4] >> 4
        g8 = self.ba_mosi[4] & 0x0f

        g11 = self.ba_mosi[5] >> 4
        g10 = self.ba_mosi[5] & 0x0f
        print(f'g8: {g8}, g9: {g9}, g10: {g10}, g11: {g11}')

        g13 = self.ba_mosi[6] >> 4
        g12 = self.ba_mosi[6] & 0x0f
        print(f'g12: {g12}, g13: {g13}')

        g13hp2 = self.ba_mosi[7] >> 4
        g13hp1 = self.ba_mosi[7] & 0x0f
        print(f'g13hp1: {g13hp1}, g13hp2: {g13hp2}')

        g13hp4 = self.ba_mosi[8] >> 4
        g13hp3 = self.ba_mosi[8] & 0x0f
        print(f'g13hp3: {g13hp3}, g13hp4: {g13hp4}')

        g13hp6 = self.ba_mosi[9] >> 4
        g13hp5 = self.ba_mosi[9] & 0x0f
        print(f'g13hp5: {g13hp5}, g13hp6: {g13hp6}')

        g13hp7 = self.ba_mosi[10] & 0x0f #( uint8_t ) ( rssi_cal_table->gain_tune.g13hp7 & 0x0F ),
        gain_offset = int.from_bytes(bytearray(self.ba_mosi[11:13]), 'big')
        print(f'g13hp7: {g13hp7}, gain_offset: {gain_offset}')
        return 'SetRssiCalibration (see terminal)'

    def SetLoraSyncWord(self):
        return 'SetLoraSyncWord ' + hex(self.ba_mosi[2])

    def LrFhssBuildFrame(self):
        enDict = { 0: 'ENABLE', 1: 'DISABLE' }
        crDict = { 0: '5_6', 1: '2_3', 2: '1_2', 3: '2_3' }
        gridDict = { 0: '25391', 1: '3906' }
        modDict = { 0: 'GMSK_488' }
        bwDict = {
            0x00: '39063',
            0x01: '85938',
            0x02: '136719',
            0x03: '183594',
            0x04: '335938',
            0x05: '386719',
            0x06: '722656',
            0x07: '773438',
            0x08: '1523438',
            0x09: '1574219',
        }
        # lr11xx_lr_fhss_params_t
        header_count = self.ba_mosi[2] # uint8_t
        cr = self.ba_mosi[3] # lr_fhss_v1_cr_t
        modulation_type = self.ba_mosi[4] # 
        grid = self.ba_mosi[5] # lr_fhss_v1_grid_t
        enable_hopping = self.ba_mosi[6] # 
        bw = self.ba_mosi[7] # lr_fhss_v1_bw_t
        hop_sequence_id = int.from_bytes(bytearray(self.ba_mosi[8:10]), 'big')
        device_offset = self.ba_mosi[10]
        return 'LrFhssBuildFrame header_count ' + str(header_count) + ', CR_' + crDict.get(cr, hex(cr)+'?') + ', moulation '+modDict.get(modulation_type, hex(modulation_type)+'?')+ ', hopping ' + enDict.get(enable_hopping, hex(enable_hopping)+'?') + ', bw '+bwDict.get(bw, hex(bw)+'?')+'Hz, hop_sequence_id '+str(hop_sequence_id)+', device_offset ' + str(device_offset)

    def LrFhssSetSyncWord(self):
        return 'LrFhssSetSyncWord TODO'

    def ConfigBleBeacon(self):
        channel_id = self.ba_mosi[2]
        # the rest is advertising channel PDU
        return 'ConfigBleBeacon channel_id '+str(channel_id)

    def GetLoRaRxHeaderInfos(self):
        self.next_transfer_response = 1
        return 'GetLoRaRxHeaderInfos (request) '

    def BleBeaconSend(self):
        channel_id = self.ba_mosi[2]
        data_len = len(self.ba_mosi) - 3  # 2 byte opcode + 1 byte channel_id
        return 'BleBeaconSend channel=' + str(channel_id) + ', ' + str(data_len) + ' data bytes'

    cmdDict = {
        0x0100: GetStatus, # LR11XX_BL_GET_STATUS_OC, LR11XX_SYSTEM_GET_STATUS_OC
        0x0101: GetVersion, # LR11XX_BL_GET_VERSION_OC, LR11XX_SYSTEM_GET_VERSION_OC
        0x0105: WriteRegMem32, # LR11XX_REGMEM_WRITE_REGMEM32_OC
        0x0106: ReadRegMem32, # LR11XX_REGMEM_READ_REGMEM32_OC
        0x0107: WriteRegMem8, # LR11XX_REGMEM_WRITE_MEM8_OC
        0x0108: ReadRegMem8, # LR11XX_REGMEM_READ_MEM8_OC
        0x0109: WriteBuffer8, # LR11XX_REGMEM_WRITE_BUFFER8_OC
        0x010B: ClearRxBuffer, # LR11XX_REGMEM_CLEAR_RXBUFFER_OC
        0x010a: ReadBuffer8, # LR11XX_REGMEM_READ_BUFFER8_OC
        0x010c: WriteRegMemMask32, # LR11XX_REGMEM_WRITE_REGMEM32_MASK_OC
        0x010d: GetErrors, # LR11XX_SYSTEM_GET_ERRORS_OC
        0x010e: ClearErrors, # LR11XX_SYSTEM_CLEAR_ERRORS_OC
        0x010f: Calibrate, # LR11XX_SYSTEM_CALIBRATE_OC
        0x0110: SetRegMode, # LR11XX_SYSTEM_SET_REGMODE_OC
        0x0111: CalibImage, # LR11XX_SYSTEM_CALIBRATE_IMAGE_OC
        0x0112: SetDioAsRfSwitch, # LR11XX_SYSTEM_SET_DIO_AS_RF_SWITCH_OC
        0x0113: SetDioIrqParams, # LR11XX_SYSTEM_SET_DIOIRQPARAMS_OC
        0x0114: ClearIrq, # LR11XX_SYSTEM_CLEAR_IRQ_OC
        0x0116: ConfigLfClock, # LR11XX_SYSTEM_CFG_LFCLK_OC
        0x0117: SetTcxoMode, # LR11XX_SYSTEM_SET_TCXO_MODE_OC
        0x0118: Reboot, # LR11XX_SYSTEM_REBOOT_OC
        0x0119: GetVbat, # LR11XX_SYSTEM_GET_VBAT_OC
        0x011a: GetTemp, # LR11XX_SYSTEM_GET_TEMP_OC
        0x011b: SetSleep, # LR11XX_SYSTEM_SET_SLEEP_OC
        0x011c: SetStandby, # LR11XX_SYSTEM_SET_STANDBY_OC
        0x011d: SetFs, # LR11XX_SYSTEM_SET_FS_OC
        0x0120: GetRandomNumber, # LR11XX_SYSTEM_GET_RANDOM_OC
        0x0121: EraseInfoPage, # LR11XX_SYSTEM_ERASE_INFOPAGE_OC
        0x0122: WriteInfoPage, # LR11XX_SYSTEM_WRITE_INFOPAGE_OC
        0x0123: ReadInfoPage, # LR11XX_SYSTEM_READ_INFOPAGE_OC
        0x0125: GetChipEui, # LR11XX_SYSTEM_READ_UID_OC
        0x0126: GetSemtechJoinEui, # LR11XX_SYSTEM_READ_JOIN_EUI_OC
        0x0127: DeriveRootKeysAndGetPin, # LR11XX_SYSTEM_READ_PIN_OC
        0x0128: EnableSpiCrc, # LR11XX_SYSTEM_ENABLE_SPI_CRC_OC
        0x012a: DriveDiosInSleepMode, # LR11XX_SYSTEM_DRIVE_DIO_IN_SLEEP_MODE_OC 
        0x0200: ResetStats, # LR11XX_RADIO_RESET_STATS_OC
        0x0201: GetStats, # LR11XX_RADIO_GET_STATS_OC
        0x0202: GetPacketType, # LR11XX_RADIO_GET_PKT_TYPE_OC
        0x0203: GetRxBufferStatus, # LR11XX_RADIO_GET_RXBUFFER_STATUS_OC
        0x0204: GetPacketStatus, # LR11XX_RADIO_GET_PKT_STATUS_OC
        0x0205: GetRssiInst, # LR11XX_RADIO_GET_RSSI_INST_OC
        0x0206: SetGfskSyncWord, # LR11XX_RADIO_SET_GFSK_SYNC_WORD_OC
        0x0208: SetLoRaPublicNetwork, # LR11XX_RADIO_SET_LORA_PUBLIC_NETWORK_OC
        0x0209: SetRx, # LR11XX_RADIO_SET_RX_OC
        0x020a: SetTx, # LR11XX_RADIO_SET_TX_OC
        0x020b: SetRfFrequency, # LR11XX_RADIO_SET_RF_FREQUENCY_OC
        0x020c: AutoTxRx, # LR11XX_RADIO_AUTOTXRX_OC
        0x020d: SetCadParams, # LR11XX_RADIO_SET_CAD_PARAMS_OC
        0x020e: SetPacketType, # LR11XX_RADIO_SET_PKT_TYPE_OC
        0x020f: SetModulationParams, # LR11XX_RADIO_SET_MODULATION_PARAM_OC
        0x0210: SetPacketParams, # LR11XX_RADIO_SET_PKT_PARAM_OC
        0x0211: SetTxParams, # LR11XX_RADIO_SET_TX_PARAMS_OC
        0x0212: SetPacketAdrs, # LR11XX_RADIO_SET_PKT_ADRS_OC
        0x0213: SetRxTxFallbackMode, # LR11XX_RADIO_SET_RX_TX_FALLBACK_MODE_OC
        0x0214: SetRxDutyCycle, # LR11XX_RADIO_SET_RX_DUTY_CYCLE_OC
        0x0215: SetPaConfig, # LR11XX_RADIO_SET_PA_CFG_OC
        0x0217: StopTimeoutOnPreamble, # LR11XX_RADIO_STOP_TIMEOUT_ON_PREAMBLE_OC
        0x0218: SetCad, # LR11XX_RADIO_SET_CAD_OC
        0x0219: SetTxCw, # LR11XX_RADIO_SET_TX_CW_OC
        0x021a: SetTxInfinitePreamble, # LR11XX_RADIO_SET_TX_INFINITE_PREAMBLE_OC
        0x021b: SetLoRaSynchTimeout, # LR11XX_RADIO_SET_LORA_SYNC_TIMEOUT_OC
        0x021c: SetRangingAddr, # LR11XX_RTTOF_SET_ADDRESS
        0x021d: SetRangingReqAddr, # LR11XX_RTTOF_SET_REQUEST_ADDRESS
        0x021e: GetRangingResult, # LR11XX_RTTOF_GET_RESULT
        0x021f: SetRangingTxRxDelay, # LR11XX_RTTOF_SET_RX_TX_DELAY
        0x0222: GnssReadRssiTest, # LR11XX_GNSS_READ_GNSS_RSSI_TEST_OC
        0x0224: SetGfskCrcParams, # LR11XX_RADIO_SET_GFSK_CRC_PARAMS_OC
        0x0225: SetGfskWhiteningParams, # LR11XX_RADIO_SET_GFSK_WHITENING_PARAMS_OC
        0x0227: SetRxBoosted, # LR11XX_RADIO_SET_RX_BOOSTED_OC
        0x0228: SetRangingParameter, # LR11XX_RTTOF_SET_PARAMETERS
        0x0229: SetRssiCalibration, # LR11XX_RADIO_SET_RSSI_CALIBRATION_OC
        0x022b: SetLoraSyncWord, # LR11XX_RADIO_SET_LORA_SYNC_WORD_OC
        0x022c: LrFhssBuildFrame, # LR11XX_LR_FHSS_BUILD_FRAME_OC
        0x022d: LrFhssSetSyncWord, # LR11XX_RADIO_SET_LR_FHSS_SYNC_WORD_OC
        0x022e: ConfigBleBeacon, # LR11XX_RADIO_CFG_BLUETOOTH_LOW_ENERGY_BEACONNING_COMPATIBILITY_OC
        0x0230: GetLoRaRxHeaderInfos, # LR11XX_RADIO_GET_LORA_RX_INFO_OC
        0x0231: BleBeaconSend, # LR11XX_RADIO_BLUETOOTH_LOW_ENERGY_BEACONNING_COMPATIBILITY_SEND_OC
        #0x03xx was here, moved to LrWifi
        #0x04xx was here, moved to LrGnss

# 0x0500: LR11XX_CRYPTO_SELECT_OC
# 0x0502: LR11XX_CRYPTO_SET_KEY_OC
# 0x0503: LR11XX_CRYPTO_DERIVE_KEY_OC
# 0x0504: LR11XX_CRYPTO_PROCESS_JOIN_ACCEPT_OC
# 0x0505: LR11XX_CRYPTO_COMPUTE_AES_CMAC_OC
# 0x0506: LR11XX_CRYPTO_VERIFY_AES_CMAC_OC
# 0x0507: LR11XX_CRYPTO_ENCRYPT_AES_01_OC
# 0x0508: LR11XX_CRYPTO_ENCRYPT_AES_OC
# 0x0509: LR11XX_CRYPTO_DECRYPT_AES_OC
# 0x050A: LR11XX_CRYPTO_STORE_TO_FLASH_OC
# 0x050B: LR11XX_CRYPTO_RESTORE_FROM_FLASH_OC
# 0x050D: LR11XX_CRYPTO_SET_PARAMETER_OC
# 0x050E: LR11XX_CRYPTO_GET_PARAMETER_OC
# 0x050F: LR11XX_CRYPTO_CHECK_ENCRYPTED_FW_IMAGE_OC
# 0x0510: LR11XX_CRYPTO_GET_CHECK_ENCRYPTED_FW_IMAGE_RESULT_OC

        0x8000: EraseFlash, # LR11XX_BL_ERASE_FLASH_OC
        0x8003: WriteFlashEncrypted, # LR11XX_BL_WRITE_FLASH_ENCRYPTED_OC
# 0x8005: LR11XX_BL_REBOOT_OC
        0x800b: GetPin, # LR11XX_BL_GET_PIN_OC
        0x800c: ReadChipEui, # LR11XX_BL_READ_CHIP_EUI_OC
        0x800d: ReadJoinEui, # LR11XX_BL_READ_JOIN_EUI_OC
    }

    def ResponseGetVersion(self):
        hwVer = self.ba_miso[1]
        useCase = self.ba_miso[2]
        if useCase == 1:
            useStr = 'LR1110'
        elif useCase == 0xdf:
            useStr = 'bootloader'
        else:
            useStr = '?' + hex(useCase) + '?'
        fwMajor = self.ba_miso[3]
        fwMinor = self.ba_miso[4]
        return 'GetVersion HW ' + hex(hwVer) + ' ' + useStr + ', v' + str(fwMajor) + '.' + str(fwMinor)

    def ResponseReadRegMem32(self):
        return 'ReadRegMem32 ' + str(len(self.ba_miso)-1) + 'bytes'

    def ResponseReadRegMem8(self):
        return 'ReadRegMem8 ' + str(len(self.ba_miso)-1) + 'bytes'

    def ResponseReadBuffer8(self):
        return 'ReadBuffer8 ' + str(len(self.ba_miso)-1) + 'bytes'

    def ResponseGetErrors(self):
        errorStat = int.from_bytes(bytearray(self.ba_miso[1:2]), 'big')
        _str = 'GetErrors '
        if errorStat == 0:
            return _str + ' no errors'
        if errorStat & 1:
            _str = _str + 'LF_RC_CALIB_ERR '
        if errorStat & 2:
            _str = _str + 'HF_RC_CALIB_ERR '
        if errorStat & 4:
            _str = _str + 'ADC_CALIB_ERR '
        if errorStat & 8:
            _str = _str + 'PLL_CALIB_ERR '
        if errorStat & 0x10:
            _str = _str + 'IMG_CALIB_ERR '
        if errorStat & 0x20:
            _str = _str + 'HF_XOSC_START_ERR '
        if errorStat & 0x40:
            _str = _str + 'LF_XOSC_START_ERR '
        if errorStat & 0x80:
            _str = _str + 'PLL_LOCK_ERR '
        if errorStat & 0x100:
            _str = _str + 'RX_ADC_OFFSET_ERR '
        return _str

    def ResponseGetVbat(self):
        vbat = self.ba_miso[1]
        volts = (((5*vbat)/255)-1)*1.35
        _str = f"{volts:.2f}"
        return 'GetVbat ' + _str + ' volts'

    def ResponseGetTemp(self):
        temp = int.from_bytes(bytearray(self.ba_miso[0:2]), 'big')
        return 'GetTemp ' + hex(temp)

    def ResponseGetRandomNumber(self):
        rnd = int.from_bytes(bytearray(self.ba_miso[1:5]), 'big')
        return 'GetRandomNumber ' + str(rnd)

    def ResponseReadInfoPage(self):
        _len = len(self.ba_miso)
        print('ReadInfoPage:')
        for i in range(1, _len, 4):
            val = int.from_bytes(bytearray(self.ba_miso[i:i+4]), 'big')
            print(hex(val))
        return 'ReadInfoPage (see terminal)'

    def ResponseGetChipEui(self):
        uid = int.from_bytes(bytearray(self.ba_miso[1:]), 'big')
        _len = len(self.ba_miso)-1
        _str = f'{uid:0{_len}x}'
        return 'GetChipEui ' + _str

    def ResponseGetSemtechJoinEui(self):
        join_eui = int.from_bytes(bytearray(self.ba_miso[1:]), 'big')
        _len = len(self.ba_miso)-1
        _str = f'{join_eui:0{_len}x}'
        return 'GetSemtechJoinEui ' + _str

    def ResponseDeriveRootKeysAndGetPin(self):
        pin = int.from_bytes(bytearray(self.ba_miso[1:5]), 'big')
        return 'DeriveRootKeysAndGetPin pin ' + hex(pin)

    def ResponseGetPin(self):
        pin = int.from_bytes(bytearray(self.ba_miso[1:5]), 'big')
        return 'GetPin pin ' + hex(pin)

    def ResponseReadChipEui(self):
        chip_eui = int.from_bytes(bytearray(self.ba_miso[1:9]), 'big')
        _len = len(self.ba_miso)-1
        _str = f'{chip_eui:0{_len*2}x}'
        return 'ReadChipEui ' + _str

    def ResponseReadJoinEui(self):
        join_eui = int.from_bytes(bytearray(self.ba_miso[1:9]), 'big')
        _len = len(self.ba_miso)-1
        _str = f'{join_eui:0{_len*2}x}'
        return 'ReadJoinEui ' + _str

    def ResponseGetStats(self):
        # TODO need to disable parseIrqs?
        if self.pt == PacketType.FSK:
            nb_pkt_received = int.from_bytes(bytearray(self.ba_miso[1:3]), 'big')
            nb_pkt_crc_error = int.from_bytes(bytearray(self.ba_miso[3:5]), 'big')
            nb_pkt_len_error = int.from_bytes(bytearray(self.ba_miso[5:7]), 'big')
            _str = f'FSK nb_pkt_received={nb_pkt_received} nb_pkt_crc_error={nb_pkt_crc_error} nb_pkt_len_error={nb_pkt_len_error}'
        elif self.pt == PacketType.LORA:
            nb_pkt_received = int.from_bytes(bytearray(self.ba_miso[1:3]), 'big')
            nb_pkt_crc_error = int.from_bytes(bytearray(self.ba_miso[3:5]), 'big')
            nb_pkt_header_error = int.from_bytes(bytearray(self.ba_miso[5:7]), 'big')
            nb_pkt_falsesync = int.from_bytes(bytearray(self.ba_miso[7:9]), 'big')
            _str = f'LORA nb_pkt_received={nb_pkt_received} nb_pkt_crc_error={nb_pkt_crc_error} nb_pkt_header_error={nb_pkt_header_error} nb_pkt_falsesync={nb_pkt_falsesync}'
        else:
            _str = 'for unknown pktType:' + self.pt.name
        return 'GetStats ' + _str

    def ResponseGetPacketType(self):
        self.pt = PacketType(self.ba_miso[1])
        return 'GetPacketType ' + self.pt.name

    def ResponseGetRxBufferStatus(self):
        payLen = self.ba_miso[1]
        bufPtr = self.ba_miso[2]
        return 'GetRxBufferStatus ' + str(payLen) + 'bytes at ' + hex(bufPtr)

    def ResponseGetPacketStatus(self):
        if self.pt == PacketType.FSK:
            # GFSK packet status: 4 bytes [rssi_sync, rssi_avg, rx_len, status]
            rxStatus = RxStatus()
            rxStatus.asWord = int.from_bytes(bytearray(self.ba_miso[1:5]), 'little')
            my_str = str(rxStatus.RxLen) + 'bytes '
            rssiAvg = rxStatus.RssiAvg >> 1
            rssiSync = rxStatus.RssiSync >> 1
            my_str = my_str + '-' + str(rssiAvg) + 'dBm '
            my_str = my_str + '-' + str(rssiSync) + 'dBm '
            if rxStatus.PktSent == 1:
                my_str = my_str + 'PktSent '
            if rxStatus.PktRcvd == 1:
                my_str = my_str + 'PktRcvd '
            if rxStatus.AbortErr == 1:
                my_str = my_str + 'AbortErr '
            if rxStatus.Lenen == 1:
                my_str = my_str + 'Lenen '
            if rxStatus.Crcerr == 1:
                my_str = my_str + 'Crcerr '
            if rxStatus.Adrserr == 1:
                my_str = my_str + 'Adrserr '
            if rxStatus.rfu != 0:
                my_str = my_str + 'rfu '
        elif self.pt == PacketType.LORA:
            # LoRa packet status: 3 bytes [rssi_pkt, snr_pkt, signal_rssi_pkt]
            # rssi_pkt_in_dbm = -(rbuffer[0] >> 1)
            RssiPkt = -(self.ba_miso[1] >> 1)
            # snr_pkt_in_db = ((rbuffer[1] + 2) >> 2) - signed 8-bit
            snr_raw = self.ba_miso[2]
            if snr_raw > 127:
                snr_raw -= 256
            SnrPkt = (snr_raw + 2) >> 2
            # signal_rssi_pkt_in_dbm = -(rbuffer[2] >> 1)
            SignalRssiPkt = -(self.ba_miso[3] >> 1)
            my_str = str(RssiPkt) + 'dBm ' + str(SnrPkt) + 'dB ' + str(SignalRssiPkt) + 'dBm'
        else:  # only existing is get_get_lora_pkt_status() and get_gfsk_pkt_status()
            my_str = 'pktType ' + str(self.pt)
        return 'GetPacketStatus ' + my_str

    def ResponseGetRssiInst(self):
        return 'GetRssiInst -' + str(self.ba_miso[1]/2) + 'dBm'

    def ResponseGetRangingResult(self):
        # LR11XX_RTTOF_RESULT_LENGTH = 4 bytes
        result_type = getattr(self, 'ranging_result_type', None)
        if result_type == 0:  # LR11XX_RTTOF_RESULT_TYPE_RAW
            # Extract raw distance as 32-bit little-endian value
            raw_distance = int.from_bytes(bytearray(self.ba_miso[1:5]), 'little')
            return f'GetRangingResult RAW raw_distance=0x{raw_distance:08x}'
        elif result_type == 1:  # LR11XX_RTTOF_RESULT_TYPE_RSSI
            # Only byte 4 (index 4) is meaningful, shift right by 1 and negate
            rssi_raw = self.ba_miso[4]
            rssi_dbm = -(rssi_raw >> 1)
            return f'GetRangingResult RSSI rssi={rssi_dbm} dBm'
        else:
            # Unknown type, just show raw bytes
            raw_hex = ' '.join([f'{b:02x}' for b in self.ba_miso[1:5]])
            return f'GetRangingResult type={result_type} data=[{raw_hex}]'

    def ResponseGetLoRaRxHeaderInfos(self):
        if self.ba_miso[1] & 0x10:
            my_str = "CRC_ON"
        else:
            my_str = "CRC_OFF"
        cr = self.ba_miso[1] & 0x07
        my_str = my_str + ' ' + str(self.crs[cr]) + ' '
        return 'GetLoRaRxHeaderInfos ' + my_str

    def ResponseGnssReadRssiTest(self):
        rssi_gnss_dbm = int.from_bytes(bytearray(self.ba_miso[1:2]), 'big', signed=True)
        return f'GnssReadRssiTest rssi={rssi_gnss_dbm} dBm'

    cmdResponseDict = {
        0x0101: ResponseGetVersion,
        0x0106: ResponseReadRegMem32,
        0x0108: ResponseReadRegMem8,
        0x010a: ResponseReadBuffer8,
        0x010d: ResponseGetErrors,
        0x0119: ResponseGetVbat,
        0x011a: ResponseGetTemp,
        0x0120: ResponseGetRandomNumber,
        0x0123: ResponseReadInfoPage,
        0x0125: ResponseGetChipEui,
        0x0126: ResponseGetSemtechJoinEui,
        0x0127: ResponseDeriveRootKeysAndGetPin,
        0x800b: ResponseGetPin,
        0x800c: ResponseReadChipEui,
        0x800d: ResponseReadJoinEui,
        0x0201: ResponseGetStats,
        0x0202: ResponseGetPacketType,
        0x0203: ResponseGetRxBufferStatus,
        0x0204: ResponseGetPacketStatus,
        0x0205: ResponseGetRssiInst,
        0x021e: ResponseGetRangingResult,
        0x0222: ResponseGnssReadRssiTest,
        0x0230: ResponseGetLoRaRxHeaderInfos,
    }

    result_types = {
        'mytype': {
            'format': 'Output type: {{type}}, Input type: {{data.input_type}}'
        },
        'match': { 'format': '{{data.string}}'}
    }

    def __init__(self):
        self.idx = 0
        self.pt = PacketType.NONE
        self.cmd_direct_read = 0
        self.next_transfer_response = 0

    def decode(self, frame: AnalyzerFrame):
        if frame.type == 'result':
            if self.idx == 0:
                self.ba_mosi = frame.data['mosi']
                self.ba_miso = frame.data['miso']
            else:
                self.ba_mosi += frame.data['mosi']
                self.ba_miso += frame.data['miso']
            self.idx += 1
        elif frame.type == 'enable':   # falling edge of nSS
            self.ba_mosi = b''
            self.ba_miso = b''
            self.nss_fall_time = frame.start_time
            self.idx = 0
        elif frame.type == 'disable':   # rising edge of nSS
            self.idx = -1
            if len(self.ba_mosi) > 0:
                if self.cmd_direct_read == 0:
                    try:
                        cmd = int.from_bytes(bytearray(self.ba_mosi[0:2]), 'big')
                        if self.ba_mosi[0] == 0x04:
                            my_str = lr_gnss.cmdDict[cmd](self)
                        elif self.ba_mosi[0] == 0x04:
                            my_str = lr_wifi.cmdDict[cmd](self)
                        else:
                            my_str = self.cmdDict[cmd](self)
                        if self.next_transfer_response == 1:
                            self.cmd_direct_read = cmd  # save it for later
                            self.next_transfer_response = 0
                        self.len = len(self.ba_mosi) # save this length
                    except Exception as error:
                        if self.ba_mosi[0] == 0:
                            xferLen = len(self.ba_mosi)
                            if xferLen > 2:
                                my_str = self.parseIrqs(int.from_bytes(bytearray(self.ba_miso[2:6]), 'big'))
                            else:
                                my_str = type(self.ba_mosi).__name__ + ' xferLen' + str(len(self.ba_mosi)) + ', ' + str(frame.end_time - self.nss_fall_time)
                        else:
                            my_str = hex(cmd) + ', dict-error:' + str(error)
                    half_status = 0
                else:
                    try:
                        if (self.cmd_direct_read >> 8) == 0x04:
                            my_str = lr_gnss.cmdResponseDict[self.cmd_direct_read](self)
                        elif (self.cmd_direct_read >> 8) == 0x03:
                            my_str = lr_wifi.cmdResponseDict[self.cmd_direct_read](self)
                        else:
                            my_str = self.cmdResponseDict[self.cmd_direct_read](self)
                    except Exception as error:
                        my_str = hex(self.cmd_direct_read) + ', response-dict-error:' + str(error)

                    half_status = 1
                    self.cmd_direct_read = 0

                if len(self.ba_mosi) > 1:
                    my_str = my_str + ' (' + self.parseStatus(half_status) + ')'
                #print('--> ', my_str)
            else:
                my_str = 'wakeup ' + str(frame.end_time - self.nss_fall_time)
            return AnalyzerFrame('match', self.nss_fall_time, frame.end_time, {'string':my_str})
        elif frame.type == 'error':
            print('error');

