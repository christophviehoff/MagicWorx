#!/usr/bin/python
import sys, atexit,time
import requests, json
# GUI stuff
from PyQt5 import QtCore, QtWidgets
#link to GUI
from relays import Ui_Controller


#QThread
from PyQt5.QtCore import *

class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        `tuple` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing, anything

    '''
    pass
    #finished = pyqtSignal()
    #result = pyqtSignal(object)

class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        #self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        result = self.fn(*self.args, **self.kwargs)
        #self.signals.result.emit(result)  # Return the result of the processing
        #self.signals.finished.emit()  # Done

class specializedWorker(QRunnable):

    '''
    Worker thread
    '''

    @pyqtSlot()
    def run(self):
        '''
        Your code goes in this function
        '''
        print("Thread start")
        url = 'http://PiPlates-1.local:5000/api/v1/gpio/TB6600/test'
        r = requests.get(url)
        response = r.json()
        print (json.dumps(r.json(), indent=4, sort_keys=True))
        #time.sleep(5)
        print("Thread complete")

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

     # Hellp functions
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
            self.counter=0
            self.cnt0 = 0
            self.cnt1 = 0
            # register 0 to 1 'rising edge'  edge detector callback
            self.detector_pin_0 = EdgeTrigger(self.cb_i2c_pin_0)
            self.detector_bb = EdgeTrigger(self.cb_break_beam)

            # setup a reoccuring timee
            self.timer1 = QTimer()
            self.timer1.setInterval(1000)
            self.timer1.timeout.connect(self.watchdog)
            self.timer1.start()

            self.timer2 = QTimer()
            self.timer2.setInterval(100)
            self.timer2.timeout.connect(self.io_polling)
            self.timer2.start()


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

            #conveyor controls
            #self.pb_fwd.clicked.connect(self.cb_conveyor_fwd)
            #self.pb_rev.clicked.connect(self.cb_conveyor_rev)
            self.pb_tb6600_MCR.clicked.connect(self.cb_post_tb6600_MCR)

            #thread callback
            self.pb_tb6600_test.clicked.connect(self.t_get_tb6600_test)#(self.cb_get_tb6600_test)

            self.pb_tb6600_move_cw.clicked.connect(self.t_post_tb6600_move_cw)
            self.pb_tb6600_move_ccw.clicked.connect(self.t_post_tb6600_move_ccw)

            self.threadpool = QThreadPool()
            print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

            #known state. client starts out with all relays off
            self.pb_relay_all_off.setChecked(True)


            #conveyor controls
            self.pb_conv_start.clicked.connect(self.cb_post_conv_start)
            self.pb_conv_stop.clicked.connect(self.cb_post_conv_stop)
            self.pb_conv_shutdown.clicked.connect(self.cb_post_conv_shutdown)

            #thread
            self.pb_conv_start.clicked.connect(self.t_post_conv_enable)
            #TOD didnt connect pb_conv_enable at all

        # Step 2a :  write callback function for threads

        def cb_post_tb6600_MCR(self):

            url = 'http://PiPlates-1.local:5000/api/v1/relay/7'
            if self.pb_tb6600_MCR.isChecked():
                r = requests.post(url, json={"value": 1})
            else:
                r = requests.post(url, json={"value": 0})

            # use response to manage button status, currently done in QT although
            response = r.json()
            if response["new_value"]:
                self.pb_tb6600_MCR.setChecked(True)  # ON
            else:
                self.pb_tb6600_MCR.setChecked(False)  # ON


        def thread_complete(self):
            print("THREAD COMPLETE!")

        def t_get_tb6600_test(self):
            # Pass the function to execute
            worker = Worker(self.cb_get_tb6600_test)  # Any other args, kwargs are passed to the run function
            #worker.signals.finished.connect(self.thread_complete)
            # Execute
            self.threadpool.start(worker)

        def t_post_tb6600_move_cw(self):
            # Pass the function to execute
            worker = Worker(self.cb_post_tb6600_move_cw)  # Any other args, kwargs are passed to the run function
            #worker.signals.finished.connect(self.thread_complete)
            # Execute
            self.threadpool.start(worker)

        def t_post_tb6600_move_ccw(self):
            # Pass the function to execute
            worker = Worker(self.cb_post_tb6600_move_ccw)  # Any other args, kwargs are passed to the run function
            #worker.signals.finished.connect(self.thread_complete)
            # Execute
            self.threadpool.start(worker)

        #conveyor threads

        def t_post_conv_enable(self):
            # Pass the function to execute
            worker = Worker(self.cb_post_conv_enable)  # Any other args, kwargs are passed to the run function
            #worker.signals.finished.connect(self.thread_complete)
            # Execute
            self.threadpool.start(worker)

        # Step 2b :  write callback function for button events
        def cb_post_conv_enable(self):
            url='http://PiPlates-1.local:5000/api/v1/conv'
            self.pb_conv_enable.setEnabled(False)
            r = requests.post(url)
            response = r.json()

        def cb_post_conv_start(self):
            url = 'http://PiPlates-1.local:5000/api/v1/conv/mode'
            r = requests.post(url, json={"fsm": "enable", "motion": "enable"})
            # use response to manage button status, currently done in QT although
            response = r.json()
            if response["ack"]:
                self.pb_conv_start.setChecked(True)
                self.pb_conv_stop.setChecked(False)

        def cb_post_conv_stop(self):
            url='http://PiPlates-1.local:5000/api/v1/conv/mode'
            r = requests.post(url, json={"fsm": "enable", "motion": "disable"})

            # use response to manage button status, currently done in QT although
            response = r.json()
            if response["ack"]:
                self.pb_conv_stop.setChecked(True)
                self.pb_conv_start.setChecked(False)

        def cb_post_conv_shutdown(self):
            url='http://PiPlates-1.local:5000/api/v1/conv/mode'
            r = requests.post(url,json={"fsm":"shutdown","motion":"disable"})
            response = r.json()
            if response["ack"]:
                self.pb_conv_stop.setChecked(False)  # ON
                self.pb_conv_start.setChecked(False)  # ON
                self.pb_conv_shutdown.setChecked(False)
                self.pb_conv_enable.setChecked(False)
                self.pb_conv_enable.setEnabled(True)

        #convevor controls:
        def cb_conveyor_fwd(self):
            url='http://PiPlates-1.local:5000/api/v1/gpio/4'
            if self.pb_fwd.isChecked():
                r = requests.post(url, json={"value": 1})
            else:
                r = requests.post(url, json={"value": 0})

            # use response to manage button status, currently done in QT although
            response = r.json()
            if response["new_value"] :
                self.pb_fwd.setChecked(True) #ON
            else:
                self.pb_fwd.setChecked(False)#OFF

            #debug outputs
            print (r.status_code)
            print (response["new_value"])
            print (json.dumps(r.json(), indent=4, sort_keys=True))

        def cb_conveyor_rev(self):
            url='http://PiPlates-1.local:5000/api/v1/gpio/27'
            if self.pb_rev.isChecked():
                r = requests.post(url, json={"value": 1})
            else:
                r = requests.post(url, json={"value": 0})

            # use response to manage button status, currently done in QT although
            response = r.json()
            if response["new_value"] :
                self.pb_rev.setChecked(True) #ON
            else:
                self.pb_rev.setChecked(False)#OFF

            #debug outputs
            print (r.status_code)
            print (response["new_value"])
            print (json.dumps(r.json(), indent=4, sort_keys=True))

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

        #moved to a Qthread class
        def cb_get_tb6600_test(self):
            url = 'http://PiPlates-1.local:5000/api/v1/gpio/TB6600/test'
            r = requests.get(url)
            response = r.json()
            # debug outputs
            if response["Stepper test"] == "done":
                self.pb_tb6600_test.setChecked(False)
                #print ("results: ",json.dumps(r.json(), indent=4, sort_keys=True))

        def cb_post_tb6600_move_cw(self):
            url = 'http://PiPlates-1.local:5000/api/v1/gpio/TB6600/test'
            r = requests.post(url,json={"dir": "CW","steps":self.lcd_tb6600_steps.intValue(),"speed":2})
            response = r.json()
            if response["Stepper move"] == "done":
                self.pb_tb6600_move_cw.setChecked(False)
                #print("results: ", json.dumps(r.json(), indent=4, sort_keys=True))

        def cb_post_tb6600_move_ccw(self):
            url = 'http://PiPlates-1.local:5000/api/v1/gpio/TB6600/test'
            r = requests.post(url, json={"dir": "CCW", "steps":self.lcd_tb6600_steps.intValue(), "speed":2})
            response = r.json()
            if response["Stepper move"] == "done":
                self.pb_tb6600_move_ccw.setChecked(False)
                #print("results: ", json.dumps(r.json(), indent=4, sort_keys=True))

        # Step 2c :  FALLING edge detector callbacks for screen updates
        def cb_i2c_pin_0(self, oldVal, newVal):
            self.cnt0 = self.cnt0+1

        def cb_break_beam(self, oldVal, newVal):
            self.cnt1 = self.cnt1 + 1

        #Qtimers:

        def watchdog(self):
            global toggle
            toggle ^= True
            if toggle:
                self.heartbeat.setEnabled(1)
            else:
                self.heartbeat.setEnabled(0)

        # Step 3b : update QT lcd led displays
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
            self.lcd_0.display(self.cnt0)

            #GPIO 16 is interupt enabled break beam sensor
            url = 'http://PiPlates-1.local:5000/api/v1/gpio/16'
            r = requests.get(url)
            response = r.json()
            # print response["value"]
            if response["value"]:
                self.led_1.setEnabled(True)
            else:
                self.led_1.setEnabled(False)

            # update status :count and queue
            url = 'http://PiPlates-1.local:5000/api/v1/conv'
            r = requests.get(url)
            response = r.json()
            self.lcd_1.display(response["count"])
            self.lbl_state.setText(response["state"])

            # update queue tracking positions

            if response["queue"][0] == "card":
                self.pos_0.setEnabled(0)
            else:
                self.pos_0.setEnabled(1)

            if response["queue"][1]== "card":
                self.pos_1.setEnabled(0)
            else:
                self.pos_1.setEnabled(1)

            if response["queue"][2] == "card":
                self.pos_2.setEnabled(0)
            else:
                self.pos_2.setEnabled(1)

            if response["queue"][3] == "card":
                self.pos_3.setEnabled(0)
            else:
                self.pos_3.setEnabled(1)

            if response["queue"][4] == "card":
                self.pos_4.setEnabled(0)
            else:
                self.pos_4.setEnabled(1)

            if response["queue"][5] == "card":
                self.pos_5.setEnabled(0)
            else:
                self.pos_5.setEnabled(1)

            if response["queue"][6] == "card":
                self.pos_6.setEnabled(0)
            else:
                self.pos_6.setEnabled(1)

            if response["queue"][7] == "card":
                self.pos_7.setEnabled(0)
            else:
                self.pos_7.setEnabled(1)

            if response["queue"][8] == "card":
                self.pos_8.setEnabled(0)
            else:
                self.pos_8.setEnabled(1)

            if response["queue"][9] == "card":
                self.pos_9.setEnabled(0)
            else:
                self.pos_9.setEnabled(1)

            if response["queue"][10] == "card":
                self.pos_10.setEnabled(0)
            else:
                self.pos_10.setEnabled(1)

            if response["queue"][11] == "card":
                self.pos_11.setEnabled(0)
            else:
                self.pos_11.setEnabled(1)

            if response["queue"][12] == "card":
                self.pos_12.setEnabled(0)
            else:
                self.pos_12.setEnabled(1)

            if response["queue"][13] == "card":
                self.pos_13.setEnabled(0)
            else:
                self.pos_13.setEnabled(1)

            if response["queue"][14] == "card":
                self.pos_14.setEnabled(0)
            else:
                self.pos_14.setEnabled(1)

            if response["queue"][15] == "card":
                self.pos_15.setEnabled(0)
            else:
                self.pos_15.setEnabled(1)

            if response["queue"][16] == "card":
                self.pos_16.setEnabled(0)
            else:
                self.pos_16.setEnabled(1)

            if  response["queue"][17] == "card":
                self.pos_17.setEnabled(0)
            else:
                self.pos_17.setEnabled(1)

            if response["queue"][18] == "card":
                self.pos_18.setEnabled(0)
            else:
                self.pos_18.setEnabled(1)

            if response["queue"][19] == "card":
                self.pos_19.setEnabled(0)
            else:
                self.pos_19.setEnabled(1)

            if response["queue"][20] == "card":
                self.pos_20.setEnabled(0)
            else:
                self.pos_20.setEnabled(1)

            if response["queue"][21] == "card":
                self.pos_21.setEnabled(0)
            else:
                self.pos_21.setEnabled(1)

            if response["queue"][22] == "card":
                self.pos_22.setEnabled(0)
            else:
                self.pos_22.setEnabled(1)

            if response["queue"][23] == "card":
                self.pos_23.setEnabled(0)
            else:
                self.pos_23.setEnabled(1)

            if response["queue"][24] == "card":
                self.pos_24.setEnabled(0)
            else:
                self.pos_24.setEnabled(1)

            if response["queue"][25] == "card":
                self.pos_25.setEnabled(0)
            else:
                self.pos_25.setEnabled(1)

            if response["queue"][26] == "card":
                self.pos_26.setEnabled(0)
            else:
                self.pos_26.setEnabled(1)




    # main program start

    #  initalize the io hardware interfaces

    # create user interface
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QTabWidget()
    prog = MyRelays(dialog)

    dialog.show()

    # regsiter software e-stop
    atexit.register(terminate)

    # start the whole thing
    sys.exit(app.exec_())