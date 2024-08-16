DEBUG = 1
import string, serial, time, os
import platform
import serial.tools.list_ports
import codecs

from bitstring import BitArray

# get platform type and set port variable
PCPORT = 'com3'
print('Platform = ', platform.system())
if platform.system() == 'Linux':
    PCPORT = '/dev/ttyUSB0'
elif platform.system() == 'Darwin':
    pass  # MAC
elif platform.system() == 'Windows':
    PCPORT = 'com3'


# use ls -l /dev/serial/by-id  to list usb ports on pi4


class LibK3:
    """This library is converted from C code I wrote around the mid-2000's for
    my K2.  It was modified a bit when the K3 came out, and was converted to
    python in 2017.  Probably not all functionality has been tested after
    conversion.  I.e., expect bugs.  :-)

    NOTE: A /dev/k3 unix device drive could maintain rig state.  Then, all
    computer interactions would be with the driver, avoiding conflicts with
    xlog, xdx, etc.

    Mike Markowski, mike.ab3ap@gmail.com
    Jan 1, 2018
    """

    # NOTE: variables are named using the format fn_units, where fn
    # is a hopefully descriptive function of the variable, and units
    # are the units, where needed.  For example, keyer_wpm might be the
    # keyer speed i words/minute, and vfoA_Hz might be VFO A setting in Hz.
    #
    # The underscore only separates name and units, never words within a
    # name.

    def __init__(self):
        self.modeName = {
            'lsb': 1,
            'usb': 2,
            'cw': 3,
            'fm': 4,
            'am': 5,
            'data': 6,
            'cwRev': 7,
            'dataRev': 9}
        self.modeNum = ['unknown', 'lsb', 'usb', 'cw', 'fm', 'am', 'data',
                        'cwRev', 'unknown', 'dataRev']
        self.k3 = ''
        self.ICMiscIconsStatus = []
        self.ICMiscIconsStatus_text = []
        self.ICMiscIconsStatus_lookup = [
                                            [['0 = ERROR','Normal'],
                                            ['Normal', 'BSET **'],
                                            ['Normal', 'TX TEST'],
                                            ['Normal power out', 'mW power level (xvtr or KXV3 test)'],
                                            ['MSG bank 1', 'MSG bank 2'],
                                            ['No MSG is playing', 'MSG is playing'],
                                            ['Normal', 'CONFIG:MEM0-9 = BAND SEL'],
                                            ['Normal', 'Preset #: 0=I, 1=II§']],
                                            [['0 = ERROR', 'Normal'],
                                            ['Normal', 'VFOs linked (VFO A tunes both) (K3 only)'],
                                            ['Normal', 'VFO A/B bands are independent'],
                                            ['Normal', 'Diversity mode (K3 only)'],
                                            ['Sub ant. = AUX (K3 only)', 'Sub ant. = MAIN'],
                                            ['Sub RX aux source:non-TX ATU ant (K3 only)', 'Sub RX aux source: BNC (AUX RF)'],
                                            ['Off (K3 only)', 'Sub RX NB is on'],
                                            ['Normal', 'Sub RX is on (dual watch in KX3/KX2)']],
                                            [['0 = ERROR', 'Normal'],
                                            ['Semi QSK', 'Full QSK'],
                                            ['Normal', 'Dual-passband CW or APF in use'],
                                            ['Normal', 'VOX on for CW, FSK-D, or PSK-D'],
                                            ['Normal', 'Dual-tone FSK filter in use'],
                                            ['Inverted polarity', 'Normal FSK TX polarity'],
                                            ['Normal', 'Sync DATA'],
                                            ['Normal', 'Text-to-terminal is in effect (see TT)']],
                                            [['0 = ERROR', 'Normal'],
                                            ['Normal', 'VOX on in voice, DATA A, AFSK A'],
                                            ['Normal', 'ESSB'],
                                            ['Noise gate off', 'Noise gate on'],
                                            ['Normal', 'AM Sync RX'],
                                            ['FM PL tone off', 'FM PL tone on'],
                                            ['Normal', '(+) Rptr TX ofs'],
                                            ['Normal', '(-) Rptr TX ofs']],
                                            [['0 = ERROR', 'Normal'],
                                            ['50 Hz SHIFT', '10 Hz SHIFT'],
                                            ['AM Sync LSB', 'AM Sync USB'],
                                            ['Normal', 'Main RX is squelched'],
                                            ['Normal', 'Sub RX is squelched (K3 only)'],
                                            ['Normal', 'Sub RX NR is off, Sub RX NR is on (K3 only)'],
                                            ['VFOB LED is on (KX3/KX2 only)', 'OFS LED is on'],
                                            ['Normal', 'Fast Play in effect (KX3/KX2 only)']]

                                           ]


    def connect(self, dev=PCPORT, baud=38400):
        """Connect to K3 using specified device and baud rate.

        Inputs:
          dev (string): serial port device that K3 is connected to.  Default
            is /dev/ttyUSB0.
          baud (int): baud rate for connection.  Default is 38400.

        Output: None
        """
        self.k3 = serial.Serial(dev, baud, timeout=1)

    def disconnect(self):
        """Disconnect from K3.

        Input: None
        Output: None
        """
        if self.k3 == '':
            return
        self.k3.flushInput()
        self.k3.close()

    def findSerialPorts(self):
        """Find serial ports on this machine.

        Input: None
        Output:
          (string[]): list of names of serial ports.
        """

        comlist = serial.tools.list_ports.comports()
        connected = []
        for element in comlist:
            connected.append(element.device)
        return connected

    #
    #   K 3   I n t e r a c t i o n s
    #

    def abSwap(self):
        """Swap A and B VFOs.

        Input: None
        Output: None
        """
        self.k3.write('swt11;'.encode())

    def cancelSplit(self):
        """Exit from SPLIT mode.

        Input: None
        Output: None
        """
        self.k3.write('fr0;'.encode())

    def findMode(self, hz):
        """Based on frequency, return name of probable mode.  For example,
        findMode(7030) returns 'cw', findMode(3700) returns 'lsb'.

        Input:
          hz (float): frequency in units of Hz, whose mode is wanted.
        Output:
          (string): name of mode.  One of am, cw, fm, lsb, usb.
        """
        kHz = hz / 1e3
        if 520 <= kHz <= 1610:  # Commercial AM
            mode = 'am'
        elif 1800 <= kHz <= 2000:  # 160m CW
            mode = 'cw'
        elif 3500 <= kHz <= 3600:  # 80m CW
            mode = 'cw'
        elif 3600 <= kHz <= 4000:  # 80m phone
            mode = 'lsb'
        elif kHz in [5332, 5348, 5358.5, 5373, 5405]:  # 60m CW
            mode = 'cw'
        elif 5300 <= kHz <= 5405:  # 60m phone
            mode = 'usb'
        elif 7000 <= kHz <= 7125:  # 40m CW
            mode = 'cw'
        elif 7125 <= kHz <= 7300:  # 40m phone
            mode = 'lsb'
        elif 10100 <= kHz <= 10150:  # 30m CW
            mode = 'cw'
        elif 14000 <= kHz <= 14150:  # 20m CW
            mode = 'cw'
        elif 14150 <= kHz <= 14350:  # 20m phone
            mode = 'usb'
        elif 18068 <= kHz <= 18110:  # 17m CW
            mode = 'cw'
        elif 18110 <= kHz <= 18168:  # 17m phone
            mode = 'usb'
        elif 21000 <= kHz <= 21200:  # 15m CW
            mode = 'cw'
        elif 21200 <= kHz <= 21450:  # 15m phone
            mode = 'usb'
        elif 24890 <= kHz <= 24930:  # 12m CW
            mode = 'cw'
        elif 24930 <= kHz <= 24990:  # 12m phone
            mode = 'usb'
        elif 28000 <= kHz <= 28300:  # 10m CW
            mode = 'cw'
        elif 28300 <= kHz <= 29700:  # 10m phone
            mode = 'usb'
        elif 144000 <= kHz <= 144100:  # 2m CW
            mode = 'cw'
        elif 144100 <= kHz <= 144275:  # 2m USB
            mode = 'usb'
        elif 144275 <= kHz <= 148000:  # 2m FM
            mode = 'fm'
        else:
            mode = 'usb'  # Catch all.
        return mode

    def quitCw(self):
        """Halt an ongoing CW transmission.

        Input: None
        Output: None
        """
        self.k3.write('rx;'.encode())

    def sendCw(self, msg):
        """Send a message in CW.

        Input:
          msg (string): the message to be sent.

        Output: None
        """
        n = len(msg)
        # Send full buffers of 24 characters.
        for i in range(int(n / 24)):
            cmd = 'ky %s;' % msg[i:i + 24]
            self.k3.write(cmd.encode())
        # Send final buffer of < 24 characters, if any.
        leftover = n % 24
        if leftover > 0:
            cmd = 'ky %s;' % msg[n - leftover:]
            self.k3.write(cmd.encode())

    #
    #	g e t t e r s
    #
    def getDisplay(self):
        """Retrieve current K3 display.  This is described in detail in the
        K3 Programmer's Manual but, in short, 4 lists are returned describing
        the current state of the display.

        Input: None

        Output:
          [ (chars (string[]),
            points (string[]),
            icons (string[]),
            blinks (string[]) ] where
          chars[] is a list of characters on the display,
          points[] indicates if decimal point [i] is on by char[i],
          icons[] indicates which display icons are turned on,
          blinks[] indicates if char[i] is blinking.
        """
        self.k3.write('ds;'.encode())
        display = self.k3.read(13)  # Retrieve display.
        if DEBUG: print('display raw = ', display)
        blinks = []
        chars = []
        icons = []
        points = []
        for i in range(8):
            c = display[i + 3] & 0x7f  # Strip MSB (decimal point data)
            mask = display[i + 3] & 0x7f
            c_raw = c
            c = chr(c)
            c_char = c
            print('c char =', c)
            if c == '<':
                c = 'L'
            elif c == '>':
                c = '-'
            elif c == '@':
                c = ' '
            elif c == 'K':
                c = 'H'
            elif c == 'M':
                c = 'N'
            elif c == 'Q':
                c = 'O'
            elif c == 'V':
                c = 'U'
            elif c == 'W':
                c = 'I'
            elif c == 'X':
                c = 'c-bar'
            elif c == 'Z':
                c = 'c'
            elif c == '[':
                c = 'r-bar'
            elif c == '\\':
                c = 'lambda'
            elif c == ']':
                c = 'eq4'  # Rx/tx eq level 4
            elif c == '^':
                c = 'eq5'  # Rx/tx eq level 5
            chars.append(c)
            # Save decimal point on/off data (MSB).
            points.append((display[i + 3] & 0x80) != 0)
            mask2 = display[i + 3] & 0x80
            if DEBUG: print('c raw, c value, c, mask, mask2, point, char ', c_raw, c_char, c, mask, mask2, points,
                            chars)
        for i in range(8):
            icons.append((display[10] & (1 << i)) != 0)
        for i in range(8):
            blinks.append((display[11] & (1 << i)) != 0)  # true or false !=0
        return chars, points, icons, blinks

    def eqBandNumber(self, bandIndex):
        """Convert EQ band number, 0 through 7, to K3 button number.
        """
        if not 0 <= bandIndex <= 7:
            return -1
        bn = [11, 12, 13, 24, 27, 29, 33, 34]
        return bn[bandIndex]

    def getEqBandSetting(self, bi):
        """Return EQ band setting for specified band on current EQ.

        Input:
          bi (int): band index, 0 to 7, of currently open EQ.  Index 0
            corresponds to the 50 Hz EQ band, 7 to the 3200 Hz band.

        Output:
          (int): value of specified EQ band, -16 to 16 dB.
        """

        #print('getEqBandSetting for : ', bi)
        bn = self.eqBandNumber(bi)  # Get K3 button number for EQ band.
        #print('eqBandNumber : ', bn)
        numTries = 10  # Try to read this many times from K3.
        gotIt = False
        val = 0
        for attempt in range(numTries):
            cmd = 'swt%02d;' % bn
            #print('cmd : ', cmd)
            self.k3.write(cmd.encode())  # Tap button for EQ band.
            self.k3.write('db;'.encode())  # Get VFO B text area.
            s = self.k3.read(12)
            #print('k3 reading: ', s)
            s = str(s, 'utf-8')  # Convert bytes to string.
            #print('k3 reading as string : ', s)
            start = s.rfind('+')
            if start == -1:
                start = s.rfind('-')
            semi = s.find(';')
            if start == -1 or semi == -1 or start > semi:
                continue
            try:
                val = int(s[start:semi])
                gotIt = True
            except ValueError:
                continue
            break
        if not gotIt:
            print('Couldn\'t read EQ band %d. Using 0 (wrong)!!' % bi)
        return val

    def getEqSettings(self, tx):
        """Retrieve the EQ settings for specified equalizer.

        Input:
          tx (boolean): use transmit/receive EQ if tx is True/False.

        Output:
          (int[]): list of 8 ints corresponding to settings, -16 to 16 dB, on
            the eight EQ bands, 50, 100, 200, 400, 800, 1600, 2400, 3200 Hz.
        """
        settings_dB = []
        eqCmd = 'MN009;' \
        if tx else 'MN008;'  # Open EQ for tx/rx respectively.
        self.k3.write(eqCmd.encode())
        for i in range(8):  # Eight EQ bands.
            setting_dB = self.getEqBandSetting(i)  # Get K3 EQ 'slider' value.
            settings_dB.append(setting_dB)
        self.k3.write('swt14;'.encode())  # Exit MENU mode.

        print(settings_dB)
        return settings_dB

    def getEssbMode(self):
        """Find out if K3 is in ESSB mode or not.  Only makes sense to call
        if K3 is in ssb mode.

        Input: None

        Output:
          (boolean): True/False if K3 is/isn't in ESSB mode.
        """
        self.k3.write('es;'.encode())
        essbMode = self.k3.read(3)  # EQn, n == 0/1 for ESSB off/on.
        return essbMode[2] == '1'

    def getFreq_Hz(self, vfo):
        """Get current frequency setting of specified VFO.

        Input:
          vfo (string): A or B, case insensitive, specifying VFO.

        Output:
          (int): current frequency, in Hz, that VFO is tuned to.
        """
        if not vfo.lower() in ['a', 'b']:
            print('getFreq_Hz: vfo must be A or B, not %s' % vfo)
            return 0
        cmd = 'f%c;' % vfo
        self.k3.write(cmd.encode())
        time.sleep(100e-6)  # 100 usec
        reply = self.k3.read(14)  # Should be: FA###########;
        try:
            f_Hz = int(reply[2:13])
        except ValueError:
            print('getFreq_Hz: unexpected K3 reply "%s"' % reply)
            f_Hz = -1
        return f_Hz

    def getKeyerSpeed_wpm(self):
        """Return the current keyer speed in units of words/minute.

        Input: None

        Output:
          (int): keyer speed in words/minute.
        """
        self.k3.write('ks;'.encode())
        reply = self.k3.read(6)
        try:
            speed_wpm = int(reply[2:5])
        except ValueError:
            print('getKeyerSpeed_wpm: unexpected K3 reply "%s"' % reply)
            speed_wpm = -1
        return speed_wpm

    def getMode(self):
        """Get currnet operating mode of K3.

        Input: None

        Output:
          (string): mode, one of am, cw, fm, lsb, usb, lsbEssb, usbEssb.
        """
        numTries = 10
        gotIt = False
        for i in range(numTries):
            self.k3.write('md;'.encode())
            reply = self.k3.read(10)
            reply = str(reply, 'utf-8')  # Convert bytes to string.
            reply = reply.lower()
            if reply[0:2] == 'md' and reply[3] == ';':
                gotIt = True
                break
        if not gotIt:
            print('getMode: after %d tries, unexpected K3 reply "%s"'
                  % (numTries, reply))
            return 'unknown'
        mode = self.modeNum[int(reply[2])]
        if mode in ['lsb', 'usb'] and self.getEssbMode():
            return mode + 'Essb'
        self.DictElecraftCurrentSettings['mode'] = mode
        return mode

    def getPower_W(self):
        """Return current power level in units of Watts.

        Input: None

        Output:
          (float): amplifier power level in Watts.
        """
        self.k3.write('pc;'.encode())
        reply = self.k3.read(6)
        try:
            power_W = int(reply[2:5])
        except ValueError:
            print('getPower_W: unexpected K3 reply "%s"' % reply)
            power_W = -1
        return power_W

    def getNoiseBlanker(self):
        self.k3.write('NL;'.encode())
        reply = self.k3.read(20)
        print('Rec 1 Noise Blanker = ', reply)
        self.k3.write('NL$;'.encode())
        reply = self.k3.read(20)
        print('Rec 2 Noise Blanker = ', reply)

    def getAttenuator(self):
        self.k3.write('RA;'.encode())
        reply = self.k3.read(20)
        print('Rec 1 Atten = ', reply)
        self.k3.write('RA$;'.encode())
        reply = self.k3.read(20)
        print('Rec 2 Atten = ', reply)

    def getRecSquelchLevel(self):
        self.k3.write('SQ;'.encode())
        reply = self.k3.read(20)
        print('Rec 1 SquelchLevel = ', reply)
        self.k3.write('SQ$;'.encode())
        reply = self.k3.read(20)
        print('Rec 2 SquelchLevel = ', reply)

    def getSerialNumber(self):
        """Retrieve this unit's serial number.

        Input: None

        Output:
          (int): serial number of this K3.
        """
        self.k3.write('mn026;'.encode())  # Display serial number.
        chars, points, icons, blinks = self.getDisplay()
        print("serial raw1 = ", chars, points, icons, blinks)
        self.k3.write('mn255;'.encode())  # Exit menu.
        print("serial raw2 = ", chars, points, icons, blinks)
        sn_raw = ''.join(chars)
        sn_raw = sn_raw.strip()
        sn = sn_raw[0:5]
        print(sn)

        #print('serial = ', sn)

        self.DictElecraftCurrentSettings['serial_number'] = sn
        return sn

    def getMicGain(self):
        """Retrieve this unit's Mic Gain.

         Input: None

         Output:
           (int): Mic Gain 000 - 060.
         """
        self.k3.write('MG;'.encode())
        reply = self.k3.read(20)
        encoding = 'utf-8'
        reply = reply.decode(encoding)
        print('Mic Gain = ', reply)
        return reply

    def getFequency(self):
        self.k3.write('FA;'.encode())
        reply = self.k3.read(20)
        self.DictElecraftCurrentSettings['frequency_a'] = reply.decode(encoding="utf-8")
        print('VFO A Freq = ', reply)
        self.k3.write('FB;'.encode())
        reply = self.k3.read(20)
        self.DictElecraftCurrentSettings['frequency_b'] = reply.decode(encoding="utf-8")
        print('VFO 2 Freq = ', reply)

    def getIC(self):
        """
        IC (Misc. Icons and Status; GET only)
        RSP format: ICabcde; where abcde are 8-bit ASCII characters
        See programming manual page 13
        :return:
        """
        self.ICMiscIconsStatus = []
        self.ICMiscIconsStatus_text = []
        self.k3.write('IC;'.encode())
        reply = self.k3.read(10)
        if DEBUG: print("Reply:", reply)
        if DEBUG: print("Reply Type:", type(reply))
        if DEBUG: print(str(reply))
        data=[]
        # get the binary data strings
        for x in 0,1,2,3,4,5,6:
            b_dat = '{0:08b}'.format(int(reply[x]))
            if DEBUG: print("b_dat: ", type(b_dat), x, b_dat)
            data.append(b_dat)
            self.ICMiscIconsStatus.append(b_dat)

        if DEBUG: print("IC Data = ", data)
        # make list of current state of system
        for x in 2,3,4,5,6:
            t_list = []
            for y in 0,1,2,3,4,5,6,7:
                print(x , y, 'bit is: ', int(data[x][y]))
                if int(data[x][y]):
                    t_dat = self.ICMiscIconsStatus_lookup[(x-2)][y][1]
                else:
                    t_dat = self.ICMiscIconsStatus_lookup[(x-2)][y][0]
                t_list.append(t_dat)
            self.ICMiscIconsStatus_text.append(t_list)
        if DEBUG:
            for x in 0,1,2,3,4:
                print(self.ICMiscIconsStatus[x+2], self.ICMiscIconsStatus_text[x])
        return self.ICMiscIconsStatus_text

    def getXmtNoiseGate(self):
        """
        get the AGC loud pulse suppresion (on or off)8
        :return:
        """
        pass

    def getAgcPls(self):
        """
        get the AGC loud pulse suppresion (on or off)8
        :return:
        """
        pass

    def getAgcHold(self):
        """
        get the AGC hold time
        :return:
        """
        pass

    def getAgcSlp(self):
        """
        Get the AGC Slope setting

        :return:
        """
        pass

    def getAgcThr(self):
        """
        Get the AGC Threshold setting
        :return:
        """
        pass
    #
    #	s e t t e r s
    #
    def setRxEqBand(self, bi, newVal_dB):
        """Set a Receive EQ band to a value.

        Input:
          bi (in): band index, 0 to 7, for bands 50 Hz to 3200 Hz.
          newVal_dB (int): value, -16 to 16 dB, to set band to.
        """
        self.k3.write('mn008;'.encode())  # Bring up Rx EQ.
        curVal_dB = self.getEqBandSetting(bi)
        delta_dB = newVal_dB - curVal_dB
        if delta_dB >= 0:
            for i in range(delta_dB):
                self.k3.write('up;'.encode())  # Increase by 1 dB.
        else:
            for i in range(-delta_dB):
                self.k3.write('dn;'.encode())  # Decrease by 1 dB.
        self.k3.write('swt14;'.encode())  # Exit EQ menu.

    def setEqBands(self, tx, vals_dB):
        if len(vals_dB) != 8:
            print('setEqBands: didn\'t receive 8 band settings:')
            print('  %s' % vals_dB)
            return ''

        if tx:
            # self.k3.write('mn255;'.encode()) # Exit menu.
            cmd = 'TE'
            for i in range(8):
                print('val = ', vals_dB[i])
                level = vals_dB[i]
                if level >=0:
                    level = '+%02d' % level
                else:
                    level = '%03d' % level
                cmd = cmd + level
            print(cmd)

            cmd += ';'
            self.k3.write(cmd.encode())
        else:  # Rx EQ
            for i in range(8):
                self.setRxEqBand(i, vals_dB[i])

    def setExtendedMode(self):
        """Put K3 in Extended Mode to enable newest firmware commands.
        """
        self.k3.write('k31;'.encode())
        self.k3.write('k3;'.encode())
        try:
            reply = self.k3.read(4)
        except ValueError:
            print('setExtendedMode: unexpected reply "%s"' % reply)
            reply = ''
        return reply

    def setFreq_Hz(self, vfo, freq_Hz):
        """Set frequency of specified VFO.

        Input:
          vfo (string): A or B, case insensitive, specifying VFO.
          freq_Hz (int): frequency in Hz to set VFO to.

        Output: None
        """
        if vfo.lower() != 'a' and vfo.lower() != 'b':
            print('setFreq_Hz: vfo must be A or B, not %s' % vfo)
            return
        cmd = 'f%c%011d;' % (vfo.upper(), int(freq_Hz))
        self.k3.write(cmd.encode())

    def setK2ExtendedMode(self):
        """Put K2 in Extended Mode to enable newest firmware commands.
        """
        self.k3.write('k22;'.encode())

    def setKeyerSpeed_wpm(self, speed_wpm):
        """Set the current keyer speed in units of words/minute.

        Input:
          speed_wpm (int): speed in words/minute to set keyer.  Must be from
            9 to 50 wpm.

        Output: None
        """
        if not 9 <= speed_wpm <= 50:
            print('setKeyerSpeed_wpm: requested %d wpm, but must be 9 to 50 wpm.'
                  % speed_wpm)
            return
        cmd = 'ks%03d;' % speed_wpm
        print(cmd)
        self.k3.write(cmd.encode())

    def setMode(self, mode):
        """Set K3 modulation mode.

        Input:
          mode (string): K3 mode, must be one of lsb, usb, cw, fm, am, data,
            cwRev, or dataRev.
        """
        if not mode in self.modeName.keys():
            print('setMode: unexpected mode requested, "%s"' % mode)
            print('         use: lsb, usb, cw, fm, am, data, cwRev, or dataRev.')
            return
        m = self.modeName[mode]
        cmd = 'md%d;' % m
        self.k3.write(cmd.encode())

    def setNormal(self):
        """Set K3 filter what is considered normal for current mode.

        Input: None
        Output: None
        """
        self.k3.write('swh58;'.encode())

    def setPower_W(self, power_W):
        """Set amplifier output power level in units of Watts.

        Input:
          power_W (float): amplifier power level in Watts.

        Output: None
        """
        cmd = 'k31;pc%03d;' % power_W
        print(cmd)
        if power_W <= 12:
            frac_W = power_W - int(power_W)
            print("frac_W = ", frac_W)
            if frac_W > 0:
                cmd = 'k22;pc%03d0' % int(10 * power_W)
        print(cmd)
        self.k3.write(cmd.encode())

    def setSplit_Hz(self, vfo1, rx_Hz, up_Hz):
        """Put K3 into split mode.

        Input:
          vfo1 (string): A or B, case insensitive, for receiving VFO.
          rx_Hz (int): frequency in Hz to tune vfo1 to.
          up_Hz (int): offset in Hz to tune other VFO to.  That is, receive
            on vfo1 at rx_Hz, transmit on othe VFO at rx_Hz + up_Hz.  Up_Hz
            can be negative.  If zero, K3 exits split mode.
        """
        vfo2 = 'b' if vfo1 == 'a' else 'a'
        vfoTx = '1' if vfo1 == 'a' else '0'
        cmd = 'ft%s;' % vfoTx  # Enter split mode, set tx VFO.
        self.k3.write(cmd.encode())
        self.setFreq_Hz(vfo1, rx_Hz)  # Set rx freq.
        self.setFreq_Hz(vfo2, rx_Hz + up_Hz)  # Set tx to (rx + up).

    def setTest(self):
        """Toggle between test mode on and off.  Test mode keeps the K3 power
        amplifier turned off.
        """
        cmd = 'k31;swh18;'
        self.k3.write(cmd.encode())

    def setRecNoiseBlanker(self, onoff=0, receiver=1, dd='00', ii='00'):
        """
        onoff: on/off value 1 = on, 0 = off
        receiver:  1 main receiver, 2 sub receiver
        dd: 00 - 21  (DSP NB level)
        ii: 00 - 21  (IF NB level)
        """
        if onoff == 0:
            if receiver == 1:
                self.k3.write('NB0;'.encode())
            if receiver == 2:
                self.k3.write('NB$0;'.encode())
        elif onoff == 1:
            if receiver == 1:
                self.k3.write('NB1;'.encode())
                self.k3.write(('NL' + dd + ii + ';').encode())
            if receiver == 2:
                self.k3.write('NB$1;'.encode())
                self.k3.write(('NL$' + dd + ii + ';').encode())

    def setRecAttenuator(self, receiver=1, attenuator='00'):
        """
        receiver:  1 main receiver, 2 sub receiver
        attenuator: receiver 1, 00, 05, 10, 15
                    receiver 2, 00, 10
        """

        if receiver == 1:
            self.k3.write(('RA' + attenuator + ';').encode())
        if receiver == 2:
            if attenuator == '05': attenuator = '10'
            if attenuator == '15': attenuator = '10'
            self.k3.write(('RA$' + attenuator + ';').encode())

    def setRecSquelchLevel(self, receiver=1, squelch='000'):
        """
        receiver:  1 main receiver, 2 sub receiver
        squelch:  '000' - 029
        """
        if int(squelch, base=10) > 29:
            squelch = '021'
        if receiver == 1:
            self.k3.write(('SQ' + squelch + ';').encode())
        if receiver == 2:
            self.k3.write(('SQ$' + squelch + ';').encode())


# setup 1
def setup01():
    k3s.setFreq_Hz('A', 7207000)
    k3s.setMode('lsb')


if __name__ == "__main__":
    import sys

    k3s = LibK3()

    k3s.connect()

    # # k3s.setFreq_Hz('A', 7160000)
    # k3s.setFreq_Hz('A', 7030000)
    #
    # # k3s.setMode('lsb')
    # k3s.setKeyerSpeed_wpm(15)
    #
    # var1 = 40
    # cmd = 'k31;pc%03d;' % var1
    # print(cmd)
    #
    # k3s.setPower_W(9.5)
    # # k3s.sendCw('WB6T WB6T CQ CQ WB6T CQ')
    # # k3s.setTest()
    #
    # # Noise Blanker
    # k3s.setRecNoiseBlanker(onoff=1, receiver=2, dd='03', ii='01')
    # # Attenuator
    # k3s.setRecAttenuator(receiver=1, attenuator='00')
    # k3s.setRecSquelchLevel(1, '010')
    # k3s.getAttenuator()
    # k3s.getNoiseBlanker()
    # k3s.getRecSquelchLevel()
    # k3s.getFequency()
    #
    #k3s.getEqBandSetting(3)
    # txm_eq = [-16,-16,-6,0,0,0,0,0]
    # k3s.setEqBands(1, txm_eq)
    # k3s.getEqSettings(1)
    # rcv_eq = [0,0,0,0,0,0,0,0]
    # k3s.setEqBands(0, rcv_eq)
    # k3s.getEqSettings(0)
    #k3s.getSerialNumber()
    # k3s.getMode()
    # for key, value in k3s.DictElecraftCurrentSettings.items():
    #     print(key, ' : ', value)
    k3s.getIC()
    sys.exit()
