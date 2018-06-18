#!/usr/bin/python
import sys, atexit
import requests, json
# GUI stuff
from PyQt5 import QtCore, QtWidgets
#link to GUI
from relays import Ui_Controller

class EdgeTrigger(object):
    def __init__(self, callback):
        self.value = 0
        self.callback = callback

    def __call__(self, value):
        # if value != self.value:
        # this one will trigger a 0 to 1 transition only
        if value < self.value:
            self.callback(self.value, value)
        self.value = value

if __name__ == "__main__":

     # Help functions
    def terminate():
       print ('Program terminated by user via emergency stop')

    toggle = False
    flip=False

    # main bin test GUI program class
    class MyRelays(Ui_Controller):

        def __init__(self, dialog):
            Ui_Controller.__init__(self)
            self.setupUi(dialog)
            self.running=False
            self.cnt=0

            # register 0 to 1 'rising edge'  edge detector callback
            self.detector_pin_0 = EdgeTrigger(self.cb_i2c_pin_0)

        # Step 1a :  register callbacks for user interface events and sensors
            self.pb_relay_1.clicked.connect(self.cb_post_relay_1)
            self.pb_relay_2.clicked.connect(self.cb_post_relay_2)
            self.pb_relay_3.clicked.connect(self.cb_post_relay_3)
            self.pb_relay_4.clicked.connect(self.cb_post_relay_4)
            self.pb_relay_5.clicked.connect(self.cb_post_relay_5)
            self.pb_relay_6.clicked.connect(self.cb_post_relay_6)
            self.pb_relay_7.clicked.connect(self.cb_post_relay_7)
            self.pb_relay_8.clicked.connect(self.cb_post_relay_8)
            self.pb_relay_9.clicked.connect(self.cb_post_relay_9)
            self.pb_relay_10.clicked.connect(self.cb_post_relay_10)
            self.pb_relay_11.clicked.connect(self.cb_post_relay_11)
            self.pb_relay_12.clicked.connect(self.cb_post_relay_12)
            self.pb_relay_13.clicked.connect(self.cb_post_relay_13)
            self.pb_relay_14.clicked.connect(self.cb_post_relay_14)
            self.pb_relay_all_on.clicked.connect(self.cb_post_relay_all_on)
            self.pb_relay_all_off.clicked.connect(self.cb_post_relay_all_off)

            #thread callback
            self.pb_tb6600_test.clicked.connect(self.cb_get_tb6600_test)
            self.pb_tb6600_move_cw.clicked.connect(self.cb_post_tb6600_move_cw)
            self.pb_tb6600_move_ccw.clicked.connect(self.cb_post_tb6600_move_ccw)

            #known state. clinet starts out with all relays off
            self.pb_relay_all_off.setChecked(True)

        # Step 2a :  write callback function for threads


        # Step 2b :  write callback function for button events

        ####### RestFul implementation ######

        def cb_post_relay_1(self):
            url='http://PiPlates-1.local:5000/api/v1/relay/1'
            if self.pb_relay_1.isChecked():
                r = requests.post(url, json={"value": 1})
            else:
                r = requests.post(url, json={"value": 0})

            # use response to manage button status, currently done in QT although
            response = r.json()
            if response["new_value"] :
                self.pb_relay_1.setChecked(True) #ON
            else:
                self.pb_relay_1.setChecked(False)#OFF

            #debug outputs
            #print r.status_code
            #print response["new_value"]
            #print json.dumps(r.json(), indent=4, sort_keys=True)

        def cb_post_relay_2(self):
            url = 'http://PiPlates-1.local:5000/api/v1/relay/2'
            if self.pb_relay_2.isChecked():
                r = requests.post(url, json={"value": 1})
            else:
                r = requests.post(url, json={"value": 0})

        def cb_post_relay_3(self):

            url = 'http://PiPlates-1.local:5000/api/v1/relay/3'
            if self.pb_relay_3.isChecked():
                r = requests.post(url, json={"value": 1})
            else:
                r = requests.post(url, json={"value": 0})

        def cb_post_relay_4(self):

            url = 'http://PiPlates-1.local:5000/api/v1/relay/4'
            if self.pb_relay_4.isChecked():
                r = requests.post(url, json={"value": 1})
            else:
                r = requests.post(url, json={"value": 0})

        def cb_post_relay_5(self):

            url = 'http://PiPlates-1.local:5000/api/v1/relay/5'
            if self.pb_relay_5.isChecked():
                r = requests.post(url, json={"value": 1})
            else:
                r = requests.post(url, json={"value": 0})

        def cb_post_relay_6(self):

            url = 'http://PiPlates-1.local:5000/api/v1/relay/6'
            if self.pb_relay_6.isChecked():
                r = requests.post(url, json={"value": 1})
            else:
                r = requests.post(url, json={"value": 0})

        def cb_post_relay_7(self):

            url = 'http://PiPlates-1.local:5000/api/v1/relay/7'
            if self.pb_relay_7.isChecked():
                r = requests.post(url, json={"value": 1})
            else:
                r = requests.post(url, json={"value": 0})

        # second relay board

        def cb_post_relay_8(self):

            url = 'http://PiPlates-1.local:5000/api/v1/relay/8'
            if self.pb_relay_8.isChecked():
                r = requests.post(url, json={"value": 1})
            else:
                r = requests.post(url, json={"value": 0})

        def cb_post_relay_9(self):

            url = 'http://PiPlates-1.local:5000/api/v1/relay/9'
            if self.pb_relay_9.isChecked():
                r = requests.post(url, json={"value": 1})
            else:
                r = requests.post(url, json={"value": 0})

        def cb_post_relay_10(self):

            url = 'http://PiPlates-1.local:5000/api/v1/relay/10'
            if self.pb_relay_10.isChecked():
                r = requests.post(url, json={"value": 1})
            else:
                r = requests.post(url, json={"value": 0})

        def cb_post_relay_11(self):

            url = 'http://PiPlates-1.local:5000/api/v1/relay/11'
            if self.pb_relay_11.isChecked():
                r = requests.post(url, json={"value": 1})
            else:
                r = requests.post(url, json={"value": 0})

        def cb_post_relay_12(self):

            url = 'http://PiPlates-1.local:5000/api/v1/relay/12'
            if self.pb_relay_12.isChecked():
                r = requests.post(url, json={"value": 1})
            else:
                r = requests.post(url, json={"value": 0})

        def cb_post_relay_13(self):

            url = 'http://PiPlates-1.local:5000/api/v1/relay/13'
            if self.pb_relay_13.isChecked():
                r = requests.post(url, json={"value": 1})
            else:
                r = requests.post(url, json={"value": 0})

        def cb_post_relay_14(self):

            url = 'http://PiPlates-1.local:5000/api/v1/relay/14'
            if self.pb_relay_14.isChecked():
                r = requests.post(url, json={"value": 1})
            else:
                r = requests.post(url, json={"value": 0})

        def cb_post_relay_all_on(self):
            if self.pb_relay_all_on.isChecked():
                url = 'http://PiPlates-1.local:5000/api/v1/relay/all-high'
                r = requests.post(url, json={"value": 0})
                # update individual button state as well
                self.pb_relay_1.setChecked(True)
                self.pb_relay_2.setChecked(True)
                self.pb_relay_3.setChecked(True)
                self.pb_relay_4.setChecked(True)
                self.pb_relay_5.setChecked(True)
                self.pb_relay_6.setChecked(True)
                self.pb_relay_7.setChecked(True)
                self.pb_relay_8.setChecked(True)
                self.pb_relay_9.setChecked(True)
                self.pb_relay_10.setChecked(True)
                self.pb_relay_11.setChecked(True)
                self.pb_relay_12.setChecked(True)
                self.pb_relay_13.setChecked(True)
                self.pb_relay_14.setChecked(True)

        def cb_post_relay_all_off(self):
            if self.pb_relay_all_off.isChecked():
                url = 'http://PiPlates-1.local:5000/api/v1/relay/all-low'
                r = requests.post(url, json={"value": 0})
                # update individual button state as well
                self.pb_relay_1.setChecked(False)
                self.pb_relay_2.setChecked(False)
                self.pb_relay_3.setChecked(False)
                self.pb_relay_4.setChecked(False)
                self.pb_relay_5.setChecked(False)
                self.pb_relay_6.setChecked(False)
                self.pb_relay_7.setChecked(False)
                self.pb_relay_8.setChecked(False)
                self.pb_relay_9.setChecked(False)
                self.pb_relay_10.setChecked(False)
                self.pb_relay_11.setChecked(False)
                self.pb_relay_12.setChecked(False)
                self.pb_relay_13.setChecked(False)
                self.pb_relay_14.setChecked(False)

        def cb_get_tb6600_test(self):
            url = 'http://PiPlates-1.local:5000/api/v1/gpio/TB6600/test'
            r = requests.get(url)
            response = r.json()
            # debug outputs
            if response["Stepper test"] == "starting...":
                self.pb_tb6600_test.setChecked(False)
                #print json.dumps(r.json(), indent=4, sort_keys=True)

        def cb_post_tb6600_move_cw(self):
            url = 'http://PiPlates-1.local:5000/api/v1/gpio/TB6600/test'
            r = requests.post(url,json={"dir": "CW","steps":self.lcd_tb6600_steps.intValue(),"speed":1})
            response = r.json()
            if response["Stepper move"] == "executed":
                self.pb_tb6600_move_cw.setChecked(False)

        def cb_post_tb6600_move_ccw(self):
            url = 'http://PiPlates-1.local:5000/api/v1/gpio/TB6600/test'
            r = requests.post(url, json={"dir": "CCW", "steps":self.lcd_tb6600_steps.intValue(), "speed":1})
            response = r.json()
            if response["Stepper move"] == "done":
                self.pb_tb6600_move_ccw.setChecked(False)

        # Step 2c :  FALLING edge detector callbacks
        def cb_i2c_pin_0(self, oldVal, newVal):
            self.cnt  = self.cnt+1

        def watchdog(self):
            global toggle
            toggle ^= True
            if toggle:
                self.heartbeat.setEnabled(1)
            else:
                self.heartbeat.setEnabled(0)

        def io_polling(self):

            url = 'http://PiPlates-1.local:5000/api/v1/i2c/0'
            r = requests.get(url)
            response = r.json()
            #print response["value"]
            if response["value"]:
              self.led_0.setEnabled(True)
            else:
              self.led_0.setEnabled(False)

            # Step 3c : register edge detection status changes for all sensors
            self.detector_pin_0(response["value"])

            #update counter
            self.lcd_0.display(self.cnt)

        # Step 3b : update lcd/led displays


    # main program start

    #  initalize the io hardware interfaces

    # create user interface
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QTabWidget()
    prog = MyRelays(dialog)

    dialog.show()

    # setup timers to run heartbeat every 1/2 sec
    timer = QtCore.QTimer()
    timer.timeout.connect(prog.watchdog)
    timer.start(500)

    # interface input/output updates every 50 ms
    iotimer = QtCore.QTimer()
    iotimer.timeout.connect(prog.io_polling)
    iotimer.start(100)

    # regsiter software e-stop
    atexit.register(terminate)

    # start the whole thing
    sys.exit(app.exec_())