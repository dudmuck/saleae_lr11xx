# High Level Analyzer
# For more information and documentation, please go to https://support.saleae.com/extensions/high-level-analyzer-extensions
# for LR11xx --- https://www.semtech.com/products/wireless-rf/lora-edge/lr1110

from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame, StringSetting, NumberSetting, ChoicesSetting
import ctypes
from enum import Enum
c_uint8 = ctypes.c_uint8
c_uint32 = ctypes.c_uint32


class PacketType(Enum):
    NONE = 0 
    LORA = 1,
    FSK = 2,
    FHSS = 3

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
        0x00: 7.81,
        0x08: 10.42,
        0x01: 15.63,
        0x09: 20.8,
        0x02: 31.25,
        0x0a: 41.67,
        0x03: 62.5,
        0x04: 125,
        0x05: 250,
        0x06: 500,
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

    def SetPacketParams(self):
        if self.pt == PacketType.FSK:
            preambleLength = int.from_bytes(bytearray(self.ba_mosi[1:3]), 'big')
            my_str = 'preamble TX ' + str(preambleLength)
            detect = self.ba_mosi[3]
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
                n_bits = '?'
            my_str = my_str + ' detect ' + n_bits + 'bits '

            syncWordBits = self.ba_mosi[4]
            my_str = my_str + ' syncWord ' + str(syncWordBits) + 'bits '

            addrComp = self.ba_mosi[5]
            if addrComp == 0:
                addrFilt = 'OFF'
            elif addrComp == 1:
                addrFilt = 'node'
            elif addrComp == 2:
                addrFilt = 'node & bcast'
            else:
                addrFilt = '?'
            my_str = my_str + ' addrFilt ' + addrFilt

            varLen = self.ba_mosi[6]
            if varLen == 0:
                my_str = my_str + ' fixLen'
            else:
                my_str = my_str + ' varLen'

            payLen = self.ba_mosi[7]
            my_str = my_str + ' payLen ' + str(payLen )

            crcType = self.ba_mosi[8]
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
        elif self.pt == PacketType.LORA:
            preambleLength = int.from_bytes(bytearray(self.ba_mosi[1:3]), 'big')
            my_str = 'preamble ' + str(preambleLength)
            headerType = self.ba_mosi[3]
            if headerType == 0:
                hdrStr = 'varLen'
            elif headerType == 1:
                hdrStr = 'fixrLen'
            else:
                hdrStr = hex(headerType)
            my_str = my_str + ' header ' + hdrStr
            payLen = self.ba_mosi[4]
            my_str = my_str + ' payLen' + str(payLen)
            crcOn = self.ba_mosi[5]
            if crcOn == 0:
                crcStr = 'ON'
            elif crcOn == 1:
                crcStr = 'OFF'
            else:
                crcStr = hex(crcOn)
            my_str = my_str + ' CRC_' + crcStr
            iqInv= self.ba_mosi[6]
            if iqInv == 0:
                iqStr = 'STD'
            elif iqInv == 1:
                iqStr = 'INV'
            else:
                iqStr = hex(iqInv)
            my_str = my_str + ' IQ ' + iqStr
        else:
            my_str = 'TODO pktType ' + str(self.pt)

        return 'SetPacketParams ' + my_str

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

    def GetVersion(self):
        self.next_transfer_response = 1
        return 'GetVersion (request)'

    def ReadRegMem32(self):
        self.next_transfer_response = 1
        addr = int.from_bytes(bytearray(self.ba_mosi[2:6]), 'big')
        l = self.ba_mosi[6]
        return 'ReadRegMem32 ' + hex(addr) + ', ' + str(l);

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
        return 'GetErrors'

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
        #TODO what is the new-line character
        return 'SetDioAsRfSwitch '

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

    def DriveDiosInSleepMode(self):
        ena = self.ba_mosi[2]
        _str = 'DriveDiosInSleepMode '
        if ena:
            _str = _str + 'pulled'
        else:
            _str = _str + 'floating'
        return _str

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
        if self.ba_mosi[2] == 0:
            self.pt = PacketType.NONE
            my_str = 'NONE'
        elif self.ba_mosi[2] == 1:
            self.pt = PacketType.FSK
            my_str = 'FSK'
        elif self.ba_mosi[2] == 2:
            self.pt = PacketType.LORA
            my_str = 'LoRa'
        elif self.ba_mosi[2] == 4:
            self.pt = PacketType.FHSS
            my_str = 'FHSS'
        else:
            self.pt = PacketType.NONE
            my_str = '?' + hex(self.ba_mosi[2]) + '?'
        return 'SetPacketType ' + my_str

    def SetModulationParams(self):
        if self.pt == PacketType.FSK:
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
            bw = self.fsk_bwDict[self.ba_mosi[7]]
            my_str = my_str + ' rxbw:' + str(bw) + 'Hz '
            fdev = int.from_bytes(bytearray(self.ba_mosi[8:12]), 'big')
            my_str = my_str + 'fdev:' + str(fdev) + 'Hz'
        elif self.pt == PacketType.LORA:
            sf = self.ba_mosi[2]
            my_str = 'SF' + str(sf)
            bw = self.ba_mosi[3]
            my_str = my_str + ' bw ' + str(self.lora_bws[bw]) + 'KHz'
            cr = self.ba_mosi[4]
            my_str = my_str + ' ' + str(self.crs[bw]) + ' '
            ldro = self.ba_mosi[5]
            if ldro == 0:
                my_str = my_str + 'LDRO_OFF'
            elif ldro == 1:
                my_str = my_str + 'LDRO_ON'
            else:
                my_str = my_str + '?' + hex(ldro) + '?'
        else:
            my_str = 'TODO pktType ' + str(self.pt)
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
        elif self.pt == PacketType.LORA:
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
        else:
            my_str = 'TODO pktType ' + str(self.pt)
        return 'SetPacketParams ' + my_str

    def SetTxParams(self):
        txp = self.ba_mosi[2]
        if txp > 127:
            dBm = txp - 256
        else:
            dBm = txp
        return 'SetTxParams ' + str(dBm) + 'dBm ' + str(self.rampDict[self.ba_mosi[3]]) + 'μs'

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

    def SetLoRaSynchTimeout(self):
        return 'SetLoRaSynchTimeout ' + str(self.ba_mosi[2]) + ' symbols'

    def SetRxBoosted(self):
        en = self.ba_mosi[2]
        if en == 0:
            my_str = 'OFF'
        elif en == 1:
            my_str = 'DN'
        else:
            my_str = '?' + hex(en) + '?'
        return 'SetRxBoosted ' + my_str

    def SetLoraSyncWord(self):
        return 'SetLoraSyncWord ' + hex(self.ba_mosi[2])

    def GetLoRaRxHeaderInfos(self):
        self.next_transfer_response = 1
        return 'GetLoRaRxHeaderInfos (request) '

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

    def ResponseWifiReadResults(self):
        return 'TODO ResponseWifiReadResults'

    def WifiScanTimeLimit(self):
        return 'WifiScanTimeLimit TODO'

    def WifiGetNbResults(self):
        self.next_transfer_response = 1
        return 'WifiGetNbResults'

    def ResponseWifiGetNbResults(self):
        return 'wifi NBresults:' + str(self.ba_miso[1])

    def WifiReadResults(self):
        _str = "index:" + str(self.ba_mosi[2])
        _str = _str +  " NbResults:" + str(self.ba_mosi[3])
        _format = self.ba_mosi[4]
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
        return 'TODO ResponseWifiReadCumulTimings'

    def WifiReadCumulTimings(self):
        self.next_transfer_response = 1
        return 'WifiReadCumulTimings'

    def WifiCfgTimestampAPphone(self):
        ts = int.from_bytes(bytearray(self.ba_mosi[2:6]), 'big')
        return 'WifiCfgTimestampAPphone ' + str(ts) + ' seconds'

    def WifiResetCumulTimings(self):
        return 'WifiResetCumulTimings'

    def GnssSetConstellationToUse(self):
        bit_mask = self.ba_mosi[2]
        _str = 'GnssSetConstellationToUse '
        if bit_mask & 1:
            _str = _str + 'GPS '
        if bit_mask & 2:
            _str = _str + 'BeiDou '
        return _str

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

    def GnssGetResultSize(self):
        self.next_transfer_response = 1
        return 'GnssGetResultSize'

    def GnssSetAssistancePosition(self):
        _lat = int.from_bytes(bytearray(self.ba_mosi[2:4]), 'big')
        lat = _lat / (2048/90)
        _lon = int.from_bytes(bytearray(self.ba_mosi[4:6]), 'big')
        if _lon > 0x7fff:
            _lon -= 0x10000
        lon = _lon / (2048/180)
        return 'GnssSetAssistancePosition ' + str(lat) + ', ' + str(lon)

    def GnssReadAssistancePosition(self):
        self.next_transfer_response = 1
        return 'GnssReadAssistancePosition'

    def GnssGetContextStatus(self):
        self.next_transfer_response = 1
        return 'GnssGetContextStatus'

    def GnssGetNbSvDetected(self):
        self.next_transfer_response = 1
        return 'GnssGetNbSvDetected'

    def GnssGetSvDetected(self):
        self.next_transfer_response = 1
        return 'GnssGetSvDetected'

    def GnssReadLastScanModeLaunched(self):
        self.next_transfer_response = 1
        return 'GnssReadLastScanModeLaunched'

    def ResponseGnssReadTime(self):
        errorCode = self.ba_miso[1]
        _str = 'errorCode '
        if errorCode == 0:
            _str = _str + 'Tow is available'
        elif errorCode == 1:
            _str = _str + 'no 32KHz'
        elif errorCode == 2:
            _str = _str + 'time not available'
        else:
            _str = _str + hex(errorCode)
        return 'TODO ResponseGnssReadTime ' + _str

    def ResponseGnssReadCumulTiming(self):
        return 'GnssReadCumulTiming response'

    def ResponseGnssReadAlmanacStatus(self):
        return 'ReadAlmanacStatus response'

    def GnssReadTime(self):
        self.next_transfer_response = 1
        return 'GnssReadTime'

    def GnssReadCumulTiming(self):
        self.next_transfer_response = 1
        return 'GnssReadCumulTiming'

    def GnssReadAlmanacStatus(self):
        self.next_transfer_response = 1
        return 'GnssReadAlmanacStatus '

    def GnssReadResults(self):
        self.next_transfer_response = 1
        return 'GnssReadResults'

    cmdDict = {
        0x0101: GetVersion,
        0x0106: ReadRegMem32,
        0x0109: WriteBuffer8,
        0x010a: ReadBuffer8,
        0x010c: WriteRegMemMask32,
        0x010d: GetErrors,
        0x010e: ClearErrors,
        0x010f: Calibrate,
        0x0110: SetRegMode,
        0x0111: CalibImage,
        0x0112: SetDioAsRfSwitch,
        0x0113: SetDioIrqParams,
        0x0114: ClearIrq,
        0x0116: ConfigLfClock,
        0x0117: SetTcxoMode,
        0x011b: SetSleep,
        0x011c: SetStandby,
        0x012a: DriveDiosInSleepMode,
        0x0203: GetRxBufferStatus,
        0x0204: GetPacketStatus,
        0x0205: GetRssiInst,
        0x0206: SetGfskSyncWord,
        0x0209: SetRx,
        0x020a: SetTx,
        0x020b: SetRfFrequency,
        0x020d: SetCadParams,
        0x020e: SetPacketType,
        0x020f: SetModulationParams,
        0x0210: SetPacketParams,
        0x0211: SetTxParams,
        0x0213: SetRxTxFallbackMode,
        0x0215: SetPaConfig,
        0x0217: StopTimeoutOnPreamble,
        0x021b: SetLoRaSynchTimeout,
        0x0227: SetRxBoosted,
        0x022b: SetLoraSyncWord,
        0x0230: GetLoRaRxHeaderInfos,
        0x0301: WifiScanTimeLimit,
        0x0305: WifiGetNbResults,
        0x0306: WifiReadResults,
        0x0307: WifiResetCumulTimings,
        0x0308: WifiReadCumulTimings,
        0x030b: WifiCfgTimestampAPphone,
        0x0400: GnssSetConstellationToUse,
        0x0409: GnssAutonomous,
        0x040a: GnssAssisted,
        0x040b: GnssScan,
        0x040c: GnssGetResultSize,
        0x040d: GnssReadResults,
        0x0410: GnssSetAssistancePosition,
        0x0411: GnssReadAssistancePosition,
        0x0416: GnssGetContextStatus,
        0x0417: GnssGetNbSvDetected,
        0x0418: GnssGetSvDetected,
        0x0426: GnssReadLastScanModeLaunched,
        0x0434: GnssReadTime,
        0x044a: GnssReadCumulTiming,
        0x0457: GnssReadAlmanacStatus,
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

    def ResponseReadBuffer8(self):
        return 'ReadBuffer8 ' + str(len(self.ba_miso)-1) + 'bytes'

    def ResponseGetErrors(self):
        errorStat = int.from_bytes(bytearray(self.ba_miso[1:2]), 'big')
        _str = ''
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

    def ResponseGetRxBufferStatus(self):
        payLen = self.ba_miso[1]
        bufPtr = self.ba_miso[2]
        return 'GetRxBufferStatus ' + str(payLen) + 'bytes at ' + hex(bufPtr)

    def ResponseGetPacketStatus(self):
        if self.pt == PacketType.FSK:
            rxStatus = RxStatus()
            rxStatus.asWord = int.from_bytes(bytearray(self.ba_miso[1:5]), 'big')
            my_str = str(rxStatus.RxLen) + 'bytes '
            rssiAvg = rxStatus.RssiAvg
            rssiSync = rxStatus.RssiSync
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
                RssiPkt = self.ba_miso[1] / -2
                foo = self.ba_miso[2] / 4
                if foo > 127:
                    foo -= 256
                SnrPkt = foo / 4
                SignalRssiPkt = self.ba_miso[3] / -2
                my_str = str(RssiPkt) + 'dBm ' + str(SnrPkt) + 'dB ' + str(SignalRssiPkt) + 'dBm'
        else:
            my_str = 'TODO pktType ' + str(self.pt)
        return 'GetPacketStatus ' + my_str

    def ResponseGetRssiInst(self):
        return 'GetRssiInst -' + str(self.ba_miso[1]/2) + 'dBm'

    def ResponseGetLoRaRxHeaderInfos(self):
        if self.ba_miso[1] & 0x10:
            my_str = "CRC_ON"
        else:
            my_str = "CRC_OFF"
        cr = self.ba_miso[1] & 0x07
        my_str = my_str + ' ' + str(self.crs[cr]) + ' '
        return 'GetLoRaRxHeaderInfos ' + my_str

    def ResponseGnssGetResultSize(self):
        return 'GetResultSize ' + str(int.from_bytes(bytearray(self.ba_miso[1:3]), 'big'))

    def ResponseGnssReadResults(self):
        return 'GnssReadResults '

    def ResponseGnssReadAssistancePosition(self):
        _lat = int.from_bytes(bytearray(self.ba_miso[1:3]), 'big')
        lat = _lat / (2048/90)
        _lon = int.from_bytes(bytearray(self.ba_miso[3:5]), 'big')
        if _lon > 0x7fff:
            _lon -= 0x10000
        lon = _lon / (2048/180)
        return 'assistance position ' + str(lat) + ', ' + str(lon)

    def ResponseGnssGetContextStatus(self):
        return 'TODO GnssGetContextStatus response'

    def ResponseGnssGetNbSvDetected(self):
        return 'GnssGetNbSvDetected ' + str(self.ba_miso[1])

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

    def ResponseGnssGetSvDetected(self):
        return 'GnssGetSvDetected '

    cmdResponseDict = {
        0x0101: ResponseGetVersion,
        0x0106: ResponseReadRegMem32,
        0x010a: ResponseReadBuffer8,
        0x010d: ResponseGetErrors,
        0x0203: ResponseGetRxBufferStatus,
        0x0204: ResponseGetPacketStatus,
        0x0205: ResponseGetRssiInst,
        0x0230: ResponseGetLoRaRxHeaderInfos,
        0x0305: ResponseWifiGetNbResults,
        0x0306: ResponseWifiReadResults,
        0x0308: ResponseWifiReadCumulTimings,
        0x040c: ResponseGnssGetResultSize,
        0x040d: ResponseGnssReadResults,
        0x0411: ResponseGnssReadAssistancePosition,
        0x0416: ResponseGnssGetContextStatus,
        0x0417: ResponseGnssGetNbSvDetected,
        0x0418: ResponseGnssGetSvDetected,
        0x0426: ResponseGnssReadLastScanModeLaunched,
        0x0434: ResponseGnssReadTime,
        0x044a: ResponseGnssReadCumulTiming,
        0x0457: ResponseGnssReadAlmanacStatus,
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
                            my_str = hex(cmd) + ', error:' + str(error)
                    half_status = 0
                else:
                    my_str = self.cmdResponseDict[self.cmd_direct_read](self)
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

