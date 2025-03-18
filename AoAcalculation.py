#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Angle Of Arrival
# Author: bimapancara
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
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
import AoAcalculation_epy_block_0 as epy_block_0  # embedded python block
import sip
import threading



class AoAcalculation(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Angle Of Arrival", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Angle Of Arrival")
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "AoAcalculation")

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
        self.freq = freq = 5e9
        self.c = c = 3e8
        self.wavelength = wavelength = c/freq
        self.samp_rate = samp_rate = 64000
        self.array_space = array_space = 0.5*wavelength

        ##################################################
        # Blocks
        ##################################################

        self.zeromq_sub_source_2 = zeromq.sub_source(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:49204', 100, False, (-1), '', False)
        self.zeromq_sub_source_1 = zeromq.sub_source(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:49202', 100, False, (-1), '', False)
        self.zeromq_sub_source_0 = zeromq.sub_source(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:49200', 100, False, (-1), '', False)
        self.epy_block_0 = epy_block_0.blk(frequency=freq, array_spacing=array_space)
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_float*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_null_sink_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_complex_to_magphase_0_0_0 = blocks.complex_to_magphase(1)
        self.blocks_complex_to_magphase_0_0 = blocks.complex_to_magphase(1)
        self.blocks_complex_to_magphase_0 = blocks.complex_to_magphase(1)
        self.AoA = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.AoA.set_update_time(0.10)
        self.AoA.set_title("Angle of Arrival")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.AoA.set_min(i, -100)
            self.AoA.set_max(i, 100)
            self.AoA.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.AoA.set_label(i, "Data {0}".format(i))
            else:
                self.AoA.set_label(i, labels[i])
            self.AoA.set_unit(i, units[i])
            self.AoA.set_factor(i, factor[i])

        self.AoA.enable_autoscale(True)
        self._AoA_win = sip.wrapinstance(self.AoA.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._AoA_win)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_magphase_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_complex_to_magphase_0, 1), (self.epy_block_0, 0))
        self.connect((self.blocks_complex_to_magphase_0_0, 0), (self.blocks_null_sink_0_0, 0))
        self.connect((self.blocks_complex_to_magphase_0_0, 1), (self.epy_block_0, 1))
        self.connect((self.blocks_complex_to_magphase_0_0_0, 0), (self.blocks_null_sink_0_0_0, 0))
        self.connect((self.blocks_complex_to_magphase_0_0_0, 1), (self.epy_block_0, 2))
        self.connect((self.blocks_throttle2_0, 0), (self.AoA, 0))
        self.connect((self.epy_block_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.zeromq_sub_source_0, 0), (self.blocks_complex_to_magphase_0, 0))
        self.connect((self.zeromq_sub_source_1, 0), (self.blocks_complex_to_magphase_0_0, 0))
        self.connect((self.zeromq_sub_source_2, 0), (self.blocks_complex_to_magphase_0_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "AoAcalculation")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.set_wavelength(self.c/self.freq)
        self.epy_block_0.frequency = self.freq

    def get_c(self):
        return self.c

    def set_c(self, c):
        self.c = c
        self.set_wavelength(self.c/self.freq)

    def get_wavelength(self):
        return self.wavelength

    def set_wavelength(self, wavelength):
        self.wavelength = wavelength
        self.set_array_space(0.5*self.wavelength)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)

    def get_array_space(self):
        return self.array_space

    def set_array_space(self, array_space):
        self.array_space = array_space
        self.epy_block_0.array_spacing = self.array_space




def main(top_block_cls=AoAcalculation, options=None):

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
