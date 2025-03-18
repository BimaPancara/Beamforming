#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: DoA Peak Transmit
# Author: bimapancara
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq
import numpy as np
import scipy as sc
import sip
import threading



class DirectionArrivalPeakTransmit(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "DoA Peak Transmit", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("DoA Peak Transmit")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "DirectionArrivalPeakTransmit")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.freq_center = freq_center = 2.3e9
        self.c = c = sc.constants.c
        self.wavelength = wavelength = c / freq_center
        self.incident_wave = incident_wave = 0
        self.d = d = wavelength * 0.5
        self.signal_freq = signal_freq = 2000e3
        self.samp_rate = samp_rate = 64e3
        self.phi1 = phi1 = 1 * ((360 * d / wavelength) * np.sin(np.deg2rad(incident_wave)))
        self.phi0 = phi0 = 0 * ((360 * d / wavelength) * np.sin(np.deg2rad(incident_wave)))
        self.gain_tx = gain_tx = 50
        self.gain = gain = 50
        self.d_m = d_m = d*1000
        self.bandwidth = bandwidth = 2000e3 * 3

        ##################################################
        # Blocks
        ##################################################

        self.zeromq_pub_sink_1 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:49202', 100, False, (-1), '', True, True)
        self.zeromq_pub_sink_0 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:49200', 100, False, (-1), '', True, True)
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(False)


        labels = ['Element 0 I', 'Element 0 Q', 'Element 1 I', 'Element 1 Q', 'Element 2 I',
            'Element 2 Q', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'green', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(4):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_win)
        self._incident_wave_range = qtgui.Range(-90, 90, 5, 0, 200)
        self._incident_wave_win = qtgui.RangeWidget(self._incident_wave_range, self.set_incident_wave, "Angle of Incident", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._incident_wave_win)
        self.blocks_throttle2_0_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_phase_shift_0_0 = blocks.phase_shift(phi1, False)
        self.blocks_phase_shift_0 = blocks.phase_shift(phi0, False)
        self.analog_sig_source_x_0_1 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, signal_freq, 1, 0, 0)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, signal_freq, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_phase_shift_0, 0))
        self.connect((self.analog_sig_source_x_0_1, 0), (self.blocks_phase_shift_0_0, 0))
        self.connect((self.blocks_phase_shift_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_phase_shift_0_0, 0), (self.blocks_throttle2_0_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.zeromq_pub_sink_0, 0))
        self.connect((self.blocks_throttle2_0_0, 0), (self.qtgui_time_sink_x_0_0, 1))
        self.connect((self.blocks_throttle2_0_0, 0), (self.zeromq_pub_sink_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "DirectionArrivalPeakTransmit")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_freq_center(self):
        return self.freq_center

    def set_freq_center(self, freq_center):
        self.freq_center = freq_center
        self.set_wavelength(self.c / self.freq_center)

    def get_c(self):
        return self.c

    def set_c(self, c):
        self.c = c
        self.set_wavelength(self.c / self.freq_center)

    def get_wavelength(self):
        return self.wavelength

    def set_wavelength(self, wavelength):
        self.wavelength = wavelength
        self.set_d(self.wavelength * 0.5)
        self.set_phi0(0 * ((360 * self.d / self.wavelength) * np.sin(np.deg2rad(self.incident_wave))))
        self.set_phi1(1 * ((360 * self.d / self.wavelength) * np.sin(np.deg2rad(self.incident_wave))))

    def get_incident_wave(self):
        return self.incident_wave

    def set_incident_wave(self, incident_wave):
        self.incident_wave = incident_wave
        self.set_phi0(0 * ((360 * self.d / self.wavelength) * np.sin(np.deg2rad(self.incident_wave))))
        self.set_phi1(1 * ((360 * self.d / self.wavelength) * np.sin(np.deg2rad(self.incident_wave))))

    def get_d(self):
        return self.d

    def set_d(self, d):
        self.d = d
        self.set_d_m(self.d*1000)
        self.set_phi0(0 * ((360 * self.d / self.wavelength) * np.sin(np.deg2rad(self.incident_wave))))
        self.set_phi1(1 * ((360 * self.d / self.wavelength) * np.sin(np.deg2rad(self.incident_wave))))

    def get_signal_freq(self):
        return self.signal_freq

    def set_signal_freq(self, signal_freq):
        self.signal_freq = signal_freq
        self.analog_sig_source_x_0_0.set_frequency(self.signal_freq)
        self.analog_sig_source_x_0_1.set_frequency(self.signal_freq)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_1.set_sampling_freq(self.samp_rate)
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle2_0_0.set_sample_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.samp_rate)

    def get_phi1(self):
        return self.phi1

    def set_phi1(self, phi1):
        self.phi1 = phi1
        self.blocks_phase_shift_0_0.set_shift(self.phi1)

    def get_phi0(self):
        return self.phi0

    def set_phi0(self, phi0):
        self.phi0 = phi0
        self.blocks_phase_shift_0.set_shift(self.phi0)

    def get_gain_tx(self):
        return self.gain_tx

    def set_gain_tx(self, gain_tx):
        self.gain_tx = gain_tx

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain

    def get_d_m(self):
        return self.d_m

    def set_d_m(self, d_m):
        self.d_m = d_m

    def get_bandwidth(self):
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth




def main(top_block_cls=DirectionArrivalPeakTransmit, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
