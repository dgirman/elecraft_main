
import mysql.connector

DBUG = True
SQL_HOST_IP = "192.168.20.217"
SQL_USER="don"
SQL_PASSWORD="girman888"
SQL_DATABASE='radio'

config_dict = {'user': SQL_USER,
               'password': SQL_PASSWORD,
               'host': SQL_HOST_IP,
               'database': SQL_DATABASE,
               }
class MySqlMain:
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
        try:
            self.database = SQL_DATABASE
            self.sql_hosr_ip = SQL_HOST_IP
            self.sql_user = SQL_USER
            self.sql_password = SQL_PASSWORD
            self.sql_database = SQL_DATABASE
        except Exception as e:
            if DBUG: print("class MySql __init__  ERROR INIT", e)

    def list_radio_tables(self):
        db = mysql.connector.connect(**config_dict)
        cursor_tmp = db.cursor()
        cursor_tmp.execute("SHOW TABLES")
        if DBUG: print('\n', "List of current databases")
        for x in cursor_tmp:
            print(x)
        cursor_tmp.close()


    def make_new_radio_tables(self):

        db = mysql.connector.connect(**config_dict)
        cursor = db.cursor()

        # Make project database
        cursor.execute("DROP TABLE IF EXISTS log")
        cursor.execute("DROP TABLE IF EXISTS settings")
        db.commit()
        self.list_radio_tables()

        cursor.execute("CREATE TABLE log (mykey INTEGER(100) NOT NULL AUTO_INCREMENT PRIMARY KEY,"
                         "mydatetimestamp VARCHAR(255) DEFAULT CURRENT_TIMESTAMP, "
                         "mydata VARCHAR(300))")

        cursor.execute(
            "CREATE TABLE settings (mykey INTEGER(100) NOT NULL AUTO_INCREMENT PRIMARY KEY, mydatetimestamp VARCHAR(255) DEFAULT CURRENT_TIMESTAMP,platform VARCHAR(255), "
            "frequency_a VARCHAR(255), frequency_b VARCHAR(255), serial_number VARCHAR(255), mode VARCHAR(255), MicGain VARCHAR(255), "
            "Rec1SquelchLevel VARCHAR(255), Rec2SquelchLevel VARCHAR(255), "
            "NoiseBlanker1 VARCHAR(255), NoiseBlanker2 VARCHAR(255), NoiseBlankerLevel1 VARCHAR(255), NoiseBlankerLevel2 VARCHAR(255), OmOptionsInstalled VARCHAR(255), "
            "RecieverPreamp1 VARCHAR(255), RecieverPreamp2 VARCHAR(255), ReqPowerOut_Watts VARCHAR(255), PowerOut_Watts VARCHAR(100),"
            "RecieverAttenuator1 VARCHAR(100), RecieverAttenuator2 VARCHAR(100), TranscPowerStatus VARCHAR(255), RFGain1 VARCHAR(255), RFGain2 VARCHAR(255), "
            "HResolutionSmeter VARCHAR(255), SquelchLevel1 VARCHAR(255),SquelchLevel2 VARCHAR(255), SWR VARCHAR(255), "
            "RecievedTextCount VARCHAR(255), TransmittedTextCount VARCHAR(255), TransmitMeterMode VARCHAR(100), TransmitQuery VARCHAR(100), "
            "VOXState VARCHAR(100), XFILNumber1 VARCHAR(100), XFILNumber2 VARCHAR(100), XITControl VARCHAR(100), AgcTimeConstant VARCHAR(100))")
        db.commit()
        cursor.close()


    def update_settings_table(self, dict_list):
        db = mysql.connector.connect(**config_dict)
        cursor_tmp = db.cursor()

        #sql = "INSERT INTO settings SET platform= '" + dict_list['platform'] + "', " +  "frequency_a = '" + dict_list['frequency_a'] +  "', " +  "frequency_b = '" + dict_list['frequency_b'] + "'"


        sql = "INSERT INTO settings SET platform = '" + dict_list['platform'] + "', " \
                                                    + "frequency_a = '"         + dict_list['frequency_a'] + "', "\
                                                    + "frequency_b = '"         + dict_list['frequency_b'] + "', "\
                                                    + "serial_number = '"       + dict_list['serial_number'] +  "', "\
                                                    + "mode = '"                + dict_list['mode'] +  "', "\
                                                    + "MicGain = '"             + dict_list['MicGain'] +  "', "\
                                                    + "Rec1SquelchLevel = '"    + dict_list['Rec1SquelchLevel'] +  "', "\
                                                    + "Rec2SquelchLevel = '"    + dict_list['Rec2SquelchLevel'] +  "', " \
                                                    + "NoiseBlanker1 = '"       + dict_list['NoiseBlanker1'] +  "', " \
                                                    + "NoiseBlanker2 = '"       + dict_list['NoiseBlanker2'] +  "', " \
                                                    + "NoiseBlankerLevel1 = '"  + dict_list['NoiseBlankerLevel1'] +  "', "\
                                                    + "NoiseBlankerLevel2 = '"  + dict_list['NoiseBlankerLevel2'] +  "', " \
                                                    + "OmOptionsInstalled = '"  + dict_list['OmOptionsInstalled'] + "',"\
                                                    + "RecieverPreamp1 = '"     + dict_list['RecieverPreamp1'] + "', " \
                                                    + "RecieverPreamp2 = '"     + dict_list['RecieverPreamp2'] + "', " \
                                                    + "ReqPowerOut_Watts = '"   + dict_list['ReqPowerOut_Watts'] + "', "\
                                                    + "PowerOut_Watts = '"      + dict_list['PowerOut_Watts'] + "', " \
                                                    + "RecieverAttenuator1 = '" + dict_list['RecieverAttenuator1'] + "', " \
                                                    + "RecieverAttenuator2 = '" + dict_list['RecieverAttenuator2'] + "' "

                                                    "TranscPowerStatus = '" + dict_list['TranscPowerStatus'] + "', " +
                                                    "RFGain1 = '" + dict_list['RFGain1'] + "', " +
                                                    "RFGain2 = '" + dict_list['RFGain2'] + "', " +
                                                        "HResolutionSmeter = '" + dict_list['HResolutionSmeter'] + "', " +
                                                    "SquelchLevel1 = '" + dict_list['SquelchLevel1'] + "', " +
                                                     "SquelchLevel2 = '" + dict_list[' SquelchLevel2'] + "', " +
                                                    "SWR = '" + dict_list['SWR'] + "', " +
        "RecievedTextCount = '" + dict_list['RecievedTextCount'] + "', " +
        "TransmittedTextCount = '" + dict_list['TransmittedTextCount'] + "', "
        "TransmitMeterMode = '" + dict_list['TransmitMeterMode'] + "', " +
        "TransmitQuery = '" + dict_list['TransmitQuery'] + "', " +
        "VOXState = '" + dict_list['VOXState'] + "', " +
        "XFILNumber1 = '" + dict_list['XFILNumber1'] + "', " +
        "XFILNumber2 = '" + dict_list[' XFILNumber2'] + "', " +
        "XITControl = '" + dict_list['XITContro'] + "', " +
        "AgcTimeConstant = '" + dict_list['AgcTimeConstant'] + "' "

        if DBUG: print(sql, '\n')

        cursor_tmp .execute(sql)
        db.commit()
        cursor_tmp.close()


def main():
    pass


if __name__ == "__main__":
   mysql_db = MySqlMain()

   mysql_db.list_radio_tables()
   mysql_db.make_new_radio_tables()
   mysql_db.list_radio_tables()


   DictElecraftCurrentSettings = {'platform': '--',
                                            'frequency_a': '--',
                                            'frequency_b': '--',
                                            'serial_number': '--',
                                            'mode': '--',
                                            'MicGain': '--',
                                            'Rec1SquelchLevel': '--',
                                            'Rec2SquelchLevel': '--',
                                            'NoiseBlanker1': '--',
                                            'NoiseBlanker2': '--',
                                            'NoiseBlankerLevel1': '--',
                                            'NoiseBlankerLevel2': '--',
                                            'OmOptionsInstalled': '--',
                                            'RecieverPreamp1': '--',
                                            'RecieverPreamp2': '--',
                                            'ReqPowerOut_Watts': '--',
                                            'PowerOut_Watts': '--',
                                            'RecieverAttenuator1': '--',
                                            'RecieverAttenuator2': '--',
                                            'TranscPowerStatus': '--',
                                            'RFGain1': '--',
                                            'RFGain2': '--',
                                            'HResolutionSmeter': '--',
                                            'SquelchLevel1': '--',
                                            'SquelchLevel2': '--',
                                            'SWR': '--',
                                            'RecievedTextCount': '--',
                                            'TransmittedTextCount': '--',
                                            'TransmitMeterMode': '--',
                                            'TransmitQuery': '--',
                                            'VOXState': '--',
                                            'XFILNumber1': '--',
                                            'XFILNumber2': '--',
                                            'XITControl': '--',
                                            'AgcTimeConstant': '--'

                                            }
   mysql_db.update_settings_table(DictElecraftCurrentSettings)