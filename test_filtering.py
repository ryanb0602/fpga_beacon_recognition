#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import sip
import threading



class test_filtering(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "test_filtering")

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
        self.samp_rate = samp_rate = 1966080000
        self.interpolation_factor = interpolation_factor = samp_rate // 1024000

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_waterfall_sink_x_1 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_1.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_1.enable_grid(False)
        self.qtgui_waterfall_sink_x_1.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_1.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_1.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_1.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_1_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_1.qwidget(), Qt.QWidget)

        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_1_win)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_f(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            (samp_rate/8), #bw
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)


        self.qtgui_waterfall_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.qwidget(), Qt.QWidget)

        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1.enable_tags(True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(False)
        self.qtgui_time_sink_x_1.enable_grid(False)
        self.qtgui_time_sink_x_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1.enable_control_panel(False)
        self.qtgui_time_sink_x_1.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_1.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_1.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_1_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.low_pass_filter_0 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                64000000,
                5000000,
                window.WIN_HAMMING,
                6.76))
        self.fir_filter_xxx_0_0_1 = filter.fir_filter_fff(10, [-2.21595576e-06, -5.42064383e-06, -9.34629496e-06,
                -1.34910721e-05, -1.71442015e-05, -1.94531899e-05,
                -1.95311881e-05, -1.65957434e-05, -1.01235121e-05,
                 1.84967063e-19,  1.33598816e-05,  2.89448722e-05,
                 4.51550627e-05,  5.98981689e-05,  7.07779380e-05,
                 7.53655741e-05,  7.15315430e-05,  5.78025205e-05,
                 3.36985013e-05, -1.47685266e-19, -4.11037363e-05,
                -8.60267091e-05, -1.29984840e-04, -1.67387229e-04,
                -1.92401317e-04, -1.99647401e-04, -1.84953999e-04,
                -1.46087047e-04, -8.33558775e-05,  3.22162463e-19,
                 9.77257687e-05,  2.00824376e-04,  2.98207613e-04,
                 3.77700731e-04,  4.27328807e-04,  4.36768375e-04,
                 3.98811523e-04,  3.10667460e-04,  1.74922865e-04,
                -5.93320870e-19, -2.00009027e-04, -4.06194369e-04,
                -5.96355604e-04, -7.47111069e-04, -8.36416206e-04,
                -8.46248457e-04, -7.65167449e-04, -5.90439122e-04,
                -3.29426459e-04,  9.69121292e-19,  3.70193881e-04,
                 7.45655839e-04,  1.08606534e-03,  1.35020322e-03,
                 1.50042147e-03,  1.50721718e-03,  1.35340836e-03,
                 1.03740086e-03,  5.75084211e-04, -1.44113997e-18,
                -6.38417149e-04, -1.27853142e-03, -1.85192169e-03,
                -2.29010068e-03, -2.53193129e-03, -2.53099765e-03,
                -2.26212161e-03, -1.72623118e-03, -9.52891703e-04,
                 1.98194664e-18,  1.04959729e-03,  2.09448934e-03,
                 3.02368849e-03,  3.72750064e-03,  4.10929335e-03,
                 4.09699185e-03,  3.65305828e-03,  2.78175982e-03,
                 1.53271360e-03, -2.54634687e-18, -1.68346077e-03,
                -3.35610459e-03, -4.84183852e-03, -5.96696011e-03,
                -6.57838330e-03, -6.56141445e-03, -5.85522269e-03,
                -4.46423115e-03, -2.46392349e-03,  3.07679072e-18,
                 2.71960348e-03,  5.43965134e-03,  7.87861712e-03,
                 9.75422339e-03,  1.08114149e-02,  1.08502795e-02,
                 9.75125753e-03,  7.49505133e-03,  4.17497003e-03,
                -3.51218800e-18, -4.71235686e-03, -9.55355279e-03,
                -1.40509099e-02, -1.77022129e-02, -2.00154198e-02,
                -2.05503378e-02, -1.89587768e-02, -1.50196582e-02,
                -8.66584054e-03,  3.79841664e-18,  1.07022512e-02,
                 2.30028026e-02,  3.63246999e-02,  4.99875470e-02,
                 6.32521509e-02,  7.53710675e-02,  8.56411375e-02,
                 9.34538641e-02,  9.83395949e-02,  1.00001936e-01,
                 9.83395949e-02,  9.34538641e-02,  8.56411375e-02,
                 7.53710675e-02,  6.32521509e-02,  4.99875470e-02,
                 3.63246999e-02,  2.30028026e-02,  1.07022512e-02,
                 3.79841664e-18, -8.66584054e-03, -1.50196582e-02,
                -1.89587768e-02, -2.05503378e-02, -2.00154198e-02,
                -1.77022129e-02, -1.40509099e-02, -9.55355279e-03,
                -4.71235686e-03, -3.51218800e-18,  4.17497003e-03,
                 7.49505133e-03,  9.75125753e-03,  1.08502795e-02,
                 1.08114149e-02,  9.75422339e-03,  7.87861712e-03,
                 5.43965134e-03,  2.71960348e-03,  3.07679072e-18,
                -2.46392349e-03, -4.46423115e-03, -5.85522269e-03,
                -6.56141445e-03, -6.57838330e-03, -5.96696011e-03,
                -4.84183852e-03, -3.35610459e-03, -1.68346077e-03,
                -2.54634687e-18,  1.53271360e-03,  2.78175982e-03,
                 3.65305828e-03,  4.09699185e-03,  4.10929335e-03,
                 3.72750064e-03,  3.02368849e-03,  2.09448934e-03,
                 1.04959729e-03,  1.98194664e-18, -9.52891703e-04,
                -1.72623118e-03, -2.26212161e-03, -2.53099765e-03,
                -2.53193129e-03, -2.29010068e-03, -1.85192169e-03,
                -1.27853142e-03, -6.38417149e-04, -1.44113997e-18,
                 5.75084211e-04,  1.03740086e-03,  1.35340836e-03,
                 1.50721718e-03,  1.50042147e-03,  1.35020322e-03,
                 1.08606534e-03,  7.45655839e-04,  3.70193881e-04,
                 9.69121292e-19, -3.29426459e-04, -5.90439122e-04,
                -7.65167449e-04, -8.46248457e-04, -8.36416206e-04,
                -7.47111069e-04, -5.96355604e-04, -4.06194369e-04,
                -2.00009027e-04, -5.93320870e-19,  1.74922865e-04,
                 3.10667460e-04,  3.98811523e-04,  4.36768375e-04,
                 4.27328807e-04,  3.77700731e-04,  2.98207613e-04,
                 2.00824376e-04,  9.77257687e-05,  3.22162463e-19,
                -8.33558775e-05, -1.46087047e-04, -1.84953999e-04,
                -1.99647401e-04, -1.92401317e-04, -1.67387229e-04,
                -1.29984840e-04, -8.60267091e-05, -4.11037363e-05,
                -1.47685266e-19,  3.36985013e-05,  5.78025205e-05,
                 7.15315430e-05,  7.53655741e-05,  7.07779380e-05,
                 5.98981689e-05,  4.51550627e-05,  2.89448722e-05,
                 1.33598816e-05,  1.84967063e-19, -1.01235121e-05,
                -1.65957434e-05, -1.95311881e-05, -1.94531899e-05,
                -1.71442015e-05, -1.34910721e-05, -9.34629496e-06,
                -5.42064383e-06, -2.21595576e-06])
        self.fir_filter_xxx_0_0_1.declare_sample_delay(0)
        self.fir_filter_xxx_0_0_0_0 = filter.fir_filter_fff(6, [-6.00944756e-06, -1.56264496e-05, -2.54570081e-05,
                -2.98324609e-05, -2.26099147e-05,  2.84158774e-19,
                 3.65024236e-05,  7.83801618e-05,  1.10764985e-04,
                 1.16107327e-04,  8.03610345e-05, -2.33963161e-19,
                -1.12689701e-04, -2.28702509e-04, -3.07533978e-04,
                -3.08417800e-04, -2.05144597e-04,  5.18520614e-19,
                 2.68534641e-04,  5.28821747e-04,  6.91637229e-04,
                 6.76033201e-04,  4.39059293e-04, -9.64750320e-19,
                -5.50517214e-04, -1.06320843e-03, -1.36534787e-03,
                -1.31178278e-03, -8.38265091e-04,  1.58726198e-18,
                 1.02032732e-03,  1.94393641e-03,  2.46452966e-03,
                 2.33934864e-03,  1.47794354e-03, -2.37307449e-18,
                -1.76182449e-03, -3.32500531e-03, -4.17830667e-03,
                -3.93353766e-03, -2.46623156e-03,  3.27688263e-18,
                 2.90080862e-03,  5.44316575e-03,  6.80531464e-03,
                 6.37848372e-03,  3.98443447e-03, -4.22292584e-18,
                -4.66299909e-03, -8.73903212e-03, -1.09229838e-02,
                -1.02458690e-02, -6.41273506e-03,  5.11404509e-18,
                 7.56503656e-03,  1.42691993e-02,  1.79852826e-02,
                 1.70512931e-02,  1.08158284e-02, -5.84666882e-18,
                -1.32429278e-02, -2.56236755e-02, -3.33366957e-02,
                -3.28861921e-02, -2.19386285e-02,  6.32879520e-18,
                 3.12569825e-02,  6.81187892e-02,  1.05411856e-01,
                 1.37433376e-01,  1.59041240e-01,  1.66668824e-01,
                 1.59041240e-01,  1.37433376e-01,  1.05411856e-01,
                 6.81187892e-02,  3.12569825e-02,  6.32879520e-18,
                -2.19386285e-02, -3.28861921e-02, -3.33366957e-02,
                -2.56236755e-02, -1.32429278e-02, -5.84666882e-18,
                 1.08158284e-02,  1.70512931e-02,  1.79852826e-02,
                 1.42691993e-02,  7.56503656e-03,  5.11404509e-18,
                -6.41273506e-03, -1.02458690e-02, -1.09229838e-02,
                -8.73903212e-03, -4.66299909e-03, -4.22292584e-18,
                 3.98443447e-03,  6.37848372e-03,  6.80531464e-03,
                 5.44316575e-03,  2.90080862e-03,  3.27688263e-18,
                -2.46623156e-03, -3.93353766e-03, -4.17830667e-03,
                -3.32500531e-03, -1.76182449e-03, -2.37307449e-18,
                 1.47794354e-03,  2.33934864e-03,  2.46452966e-03,
                 1.94393641e-03,  1.02032732e-03,  1.58726198e-18,
                -8.38265091e-04, -1.31178278e-03, -1.36534787e-03,
                -1.06320843e-03, -5.50517214e-04, -9.64750320e-19,
                 4.39059293e-04,  6.76033201e-04,  6.91637229e-04,
                 5.28821747e-04,  2.68534641e-04,  5.18520614e-19,
                -2.05144597e-04, -3.08417800e-04, -3.07533978e-04,
                -2.28702509e-04, -1.12689701e-04, -2.33963161e-19,
                 8.03610345e-05,  1.16107327e-04,  1.10764985e-04,
                 7.83801618e-05,  3.65024236e-05,  2.84158774e-19,
                -2.26099147e-05, -2.98324609e-05, -2.54570081e-05,
                -1.56264496e-05, -6.00944756e-06])
        self.fir_filter_xxx_0_0_0_0.declare_sample_delay(0)
        self.fir_filter_xxx_0_0_0 = filter.fir_filter_fff(6, [-6.00944756e-06, -1.56264496e-05, -2.54570081e-05,
                -2.98324609e-05, -2.26099147e-05,  2.84158774e-19,
                 3.65024236e-05,  7.83801618e-05,  1.10764985e-04,
                 1.16107327e-04,  8.03610345e-05, -2.33963161e-19,
                -1.12689701e-04, -2.28702509e-04, -3.07533978e-04,
                -3.08417800e-04, -2.05144597e-04,  5.18520614e-19,
                 2.68534641e-04,  5.28821747e-04,  6.91637229e-04,
                 6.76033201e-04,  4.39059293e-04, -9.64750320e-19,
                -5.50517214e-04, -1.06320843e-03, -1.36534787e-03,
                -1.31178278e-03, -8.38265091e-04,  1.58726198e-18,
                 1.02032732e-03,  1.94393641e-03,  2.46452966e-03,
                 2.33934864e-03,  1.47794354e-03, -2.37307449e-18,
                -1.76182449e-03, -3.32500531e-03, -4.17830667e-03,
                -3.93353766e-03, -2.46623156e-03,  3.27688263e-18,
                 2.90080862e-03,  5.44316575e-03,  6.80531464e-03,
                 6.37848372e-03,  3.98443447e-03, -4.22292584e-18,
                -4.66299909e-03, -8.73903212e-03, -1.09229838e-02,
                -1.02458690e-02, -6.41273506e-03,  5.11404509e-18,
                 7.56503656e-03,  1.42691993e-02,  1.79852826e-02,
                 1.70512931e-02,  1.08158284e-02, -5.84666882e-18,
                -1.32429278e-02, -2.56236755e-02, -3.33366957e-02,
                -3.28861921e-02, -2.19386285e-02,  6.32879520e-18,
                 3.12569825e-02,  6.81187892e-02,  1.05411856e-01,
                 1.37433376e-01,  1.59041240e-01,  1.66668824e-01,
                 1.59041240e-01,  1.37433376e-01,  1.05411856e-01,
                 6.81187892e-02,  3.12569825e-02,  6.32879520e-18,
                -2.19386285e-02, -3.28861921e-02, -3.33366957e-02,
                -2.56236755e-02, -1.32429278e-02, -5.84666882e-18,
                 1.08158284e-02,  1.70512931e-02,  1.79852826e-02,
                 1.42691993e-02,  7.56503656e-03,  5.11404509e-18,
                -6.41273506e-03, -1.02458690e-02, -1.09229838e-02,
                -8.73903212e-03, -4.66299909e-03, -4.22292584e-18,
                 3.98443447e-03,  6.37848372e-03,  6.80531464e-03,
                 5.44316575e-03,  2.90080862e-03,  3.27688263e-18,
                -2.46623156e-03, -3.93353766e-03, -4.17830667e-03,
                -3.32500531e-03, -1.76182449e-03, -2.37307449e-18,
                 1.47794354e-03,  2.33934864e-03,  2.46452966e-03,
                 1.94393641e-03,  1.02032732e-03,  1.58726198e-18,
                -8.38265091e-04, -1.31178278e-03, -1.36534787e-03,
                -1.06320843e-03, -5.50517214e-04, -9.64750320e-19,
                 4.39059293e-04,  6.76033201e-04,  6.91637229e-04,
                 5.28821747e-04,  2.68534641e-04,  5.18520614e-19,
                -2.05144597e-04, -3.08417800e-04, -3.07533978e-04,
                -2.28702509e-04, -1.12689701e-04, -2.33963161e-19,
                 8.03610345e-05,  1.16107327e-04,  1.10764985e-04,
                 7.83801618e-05,  3.65024236e-05,  2.84158774e-19,
                -2.26099147e-05, -2.98324609e-05, -2.54570081e-05,
                -1.56264496e-05, -6.00944756e-06])
        self.fir_filter_xxx_0_0_0.declare_sample_delay(0)
        self.fir_filter_xxx_0_0 = filter.fir_filter_fff(10, [-2.21595576e-06, -5.42064383e-06, -9.34629496e-06,
                -1.34910721e-05, -1.71442015e-05, -1.94531899e-05,
                -1.95311881e-05, -1.65957434e-05, -1.01235121e-05,
                 1.84967063e-19,  1.33598816e-05,  2.89448722e-05,
                 4.51550627e-05,  5.98981689e-05,  7.07779380e-05,
                 7.53655741e-05,  7.15315430e-05,  5.78025205e-05,
                 3.36985013e-05, -1.47685266e-19, -4.11037363e-05,
                -8.60267091e-05, -1.29984840e-04, -1.67387229e-04,
                -1.92401317e-04, -1.99647401e-04, -1.84953999e-04,
                -1.46087047e-04, -8.33558775e-05,  3.22162463e-19,
                 9.77257687e-05,  2.00824376e-04,  2.98207613e-04,
                 3.77700731e-04,  4.27328807e-04,  4.36768375e-04,
                 3.98811523e-04,  3.10667460e-04,  1.74922865e-04,
                -5.93320870e-19, -2.00009027e-04, -4.06194369e-04,
                -5.96355604e-04, -7.47111069e-04, -8.36416206e-04,
                -8.46248457e-04, -7.65167449e-04, -5.90439122e-04,
                -3.29426459e-04,  9.69121292e-19,  3.70193881e-04,
                 7.45655839e-04,  1.08606534e-03,  1.35020322e-03,
                 1.50042147e-03,  1.50721718e-03,  1.35340836e-03,
                 1.03740086e-03,  5.75084211e-04, -1.44113997e-18,
                -6.38417149e-04, -1.27853142e-03, -1.85192169e-03,
                -2.29010068e-03, -2.53193129e-03, -2.53099765e-03,
                -2.26212161e-03, -1.72623118e-03, -9.52891703e-04,
                 1.98194664e-18,  1.04959729e-03,  2.09448934e-03,
                 3.02368849e-03,  3.72750064e-03,  4.10929335e-03,
                 4.09699185e-03,  3.65305828e-03,  2.78175982e-03,
                 1.53271360e-03, -2.54634687e-18, -1.68346077e-03,
                -3.35610459e-03, -4.84183852e-03, -5.96696011e-03,
                -6.57838330e-03, -6.56141445e-03, -5.85522269e-03,
                -4.46423115e-03, -2.46392349e-03,  3.07679072e-18,
                 2.71960348e-03,  5.43965134e-03,  7.87861712e-03,
                 9.75422339e-03,  1.08114149e-02,  1.08502795e-02,
                 9.75125753e-03,  7.49505133e-03,  4.17497003e-03,
                -3.51218800e-18, -4.71235686e-03, -9.55355279e-03,
                -1.40509099e-02, -1.77022129e-02, -2.00154198e-02,
                -2.05503378e-02, -1.89587768e-02, -1.50196582e-02,
                -8.66584054e-03,  3.79841664e-18,  1.07022512e-02,
                 2.30028026e-02,  3.63246999e-02,  4.99875470e-02,
                 6.32521509e-02,  7.53710675e-02,  8.56411375e-02,
                 9.34538641e-02,  9.83395949e-02,  1.00001936e-01,
                 9.83395949e-02,  9.34538641e-02,  8.56411375e-02,
                 7.53710675e-02,  6.32521509e-02,  4.99875470e-02,
                 3.63246999e-02,  2.30028026e-02,  1.07022512e-02,
                 3.79841664e-18, -8.66584054e-03, -1.50196582e-02,
                -1.89587768e-02, -2.05503378e-02, -2.00154198e-02,
                -1.77022129e-02, -1.40509099e-02, -9.55355279e-03,
                -4.71235686e-03, -3.51218800e-18,  4.17497003e-03,
                 7.49505133e-03,  9.75125753e-03,  1.08502795e-02,
                 1.08114149e-02,  9.75422339e-03,  7.87861712e-03,
                 5.43965134e-03,  2.71960348e-03,  3.07679072e-18,
                -2.46392349e-03, -4.46423115e-03, -5.85522269e-03,
                -6.56141445e-03, -6.57838330e-03, -5.96696011e-03,
                -4.84183852e-03, -3.35610459e-03, -1.68346077e-03,
                -2.54634687e-18,  1.53271360e-03,  2.78175982e-03,
                 3.65305828e-03,  4.09699185e-03,  4.10929335e-03,
                 3.72750064e-03,  3.02368849e-03,  2.09448934e-03,
                 1.04959729e-03,  1.98194664e-18, -9.52891703e-04,
                -1.72623118e-03, -2.26212161e-03, -2.53099765e-03,
                -2.53193129e-03, -2.29010068e-03, -1.85192169e-03,
                -1.27853142e-03, -6.38417149e-04, -1.44113997e-18,
                 5.75084211e-04,  1.03740086e-03,  1.35340836e-03,
                 1.50721718e-03,  1.50042147e-03,  1.35020322e-03,
                 1.08606534e-03,  7.45655839e-04,  3.70193881e-04,
                 9.69121292e-19, -3.29426459e-04, -5.90439122e-04,
                -7.65167449e-04, -8.46248457e-04, -8.36416206e-04,
                -7.47111069e-04, -5.96355604e-04, -4.06194369e-04,
                -2.00009027e-04, -5.93320870e-19,  1.74922865e-04,
                 3.10667460e-04,  3.98811523e-04,  4.36768375e-04,
                 4.27328807e-04,  3.77700731e-04,  2.98207613e-04,
                 2.00824376e-04,  9.77257687e-05,  3.22162463e-19,
                -8.33558775e-05, -1.46087047e-04, -1.84953999e-04,
                -1.99647401e-04, -1.92401317e-04, -1.67387229e-04,
                -1.29984840e-04, -8.60267091e-05, -4.11037363e-05,
                -1.47685266e-19,  3.36985013e-05,  5.78025205e-05,
                 7.15315430e-05,  7.53655741e-05,  7.07779380e-05,
                 5.98981689e-05,  4.51550627e-05,  2.89448722e-05,
                 1.33598816e-05,  1.84967063e-19, -1.01235121e-05,
                -1.65957434e-05, -1.95311881e-05, -1.94531899e-05,
                -1.71442015e-05, -1.34910721e-05, -9.34629496e-06,
                -5.42064383e-06, -2.21595576e-06])
        self.fir_filter_xxx_0_0.declare_sample_delay(0)
        self.fir_filter_xxx_0 = filter.fir_filter_fff(8,  [9.49889021e-06,  1.03383495e-05,  7.58177160e-06,
                -3.17864516e-20, -1.26888383e-05, -2.93671118e-05,
                -4.73005830e-05, -6.22848169e-05, -6.92244940e-05,
                -6.31239657e-05, -4.03593638e-05,  1.36303765e-19,
                 5.51245288e-05,  1.17931368e-04,  1.77430747e-04,
                 2.20048546e-04,  2.31873646e-04,  2.01560110e-04,
                 1.23407922e-04, -3.56128437e-19, -1.56268583e-04,
                -3.23341113e-04, -4.71669050e-04, -5.68390383e-04,
                -5.83088897e-04, -4.94297704e-04, -2.95595024e-04,
                 7.30034939e-19,  3.58529515e-04,  7.27344718e-04,
                 1.04136627e-03,  1.23289059e-03,  1.24370707e-03,
                 1.03763387e-03,  6.11178236e-04, -1.27527875e-18,
                -7.20733813e-04, -1.44317978e-03, -2.04074430e-03,
                -2.38768775e-03, -2.38172653e-03, -1.96599818e-03,
                -1.14632930e-03,  1.97423867e-18,  1.32682113e-03,
                 2.63417169e-03,  3.69505708e-03,  4.29083059e-03,
                 4.25020897e-03,  3.48563261e-03,  2.02030658e-03,
                -2.76848035e-18, -2.31445923e-03, -4.57527020e-03,
                -6.39425910e-03, -7.40253983e-03, -7.31491752e-03,
                -5.98891968e-03, -3.46802129e-03,  3.56385918e-18,
                 3.97563977e-03,  7.87292944e-03,  1.10341087e-02,
                 1.28254153e-02,  1.27415099e-02,  1.05034271e-02,
                 6.13442967e-03, -4.24696248e-18, -7.19768172e-03,
                -1.44745008e-02, -2.06652012e-02, -2.45600204e-02,
                -2.50610191e-02, -2.13379741e-02, -1.29624024e-02,
                 4.70933148e-18,  1.69535859e-02,  3.68017265e-02,
                 5.80401381e-02,  7.89054427e-02,  9.75620567e-02,
                 1.12304839e-01,  1.21752223e-01,  1.25005279e-01,
                 1.21752223e-01,  1.12304839e-01,  9.75620567e-02,
                 7.89054427e-02,  5.80401381e-02,  3.68017265e-02,
                 1.69535859e-02,  4.70933148e-18, -1.29624024e-02,
                -2.13379741e-02, -2.50610191e-02, -2.45600204e-02,
                -2.06652012e-02, -1.44745008e-02, -7.19768172e-03,
                -4.24696248e-18,  6.13442967e-03,  1.05034271e-02,
                 1.27415099e-02,  1.28254153e-02,  1.10341087e-02,
                 7.87292944e-03,  3.97563977e-03,  3.56385918e-18,
                -3.46802129e-03, -5.98891968e-03, -7.31491752e-03,
                -7.40253983e-03, -6.39425910e-03, -4.57527020e-03,
                -2.31445923e-03, -2.76848035e-18,  2.02030658e-03,
                 3.48563261e-03,  4.25020897e-03,  4.29083059e-03,
                 3.69505708e-03,  2.63417169e-03,  1.32682113e-03,
                 1.97423867e-18, -1.14632930e-03, -1.96599818e-03,
                -2.38172653e-03, -2.38768775e-03, -2.04074430e-03,
                -1.44317978e-03, -7.20733813e-04, -1.27527875e-18,
                 6.11178236e-04,  1.03763387e-03,  1.24370707e-03,
                 1.23289059e-03,  1.04136627e-03,  7.27344718e-04,
                 3.58529515e-04,  7.30034939e-19, -2.95595024e-04,
                -4.94297704e-04, -5.83088897e-04, -5.68390383e-04,
                -4.71669050e-04, -3.23341113e-04, -1.56268583e-04,
                -3.56128437e-19,  1.23407922e-04,  2.01560110e-04,
                 2.31873646e-04,  2.20048546e-04,  1.77430747e-04,
                 1.17931368e-04,  5.51245288e-05,  1.36303765e-19,
                -4.03593638e-05, -6.31239657e-05, -6.92244940e-05,
                -6.22848169e-05, -4.73005830e-05, -2.93671118e-05,
                -1.26888383e-05, -3.17864516e-20,  7.58177160e-06,
                 1.03383495e-05,  9.49889021e-06])
        self.fir_filter_xxx_0.declare_sample_delay(0)
        self.blocks_vector_source_x_0 = blocks.vector_source_f([-1, -1, -1, 1, -1, 1, 1, -1, 1, 1, 1, -1, 1, -1, -1, -1, -1, -1, 1, 1, 1, 1, -1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, 1, -1, -1, 1, -1, -1, 1, 1, 1, -1, -1, 1, 1, -1, 1, 1, 1, 1, -1, 1, -1, -1, 1, -1, 1, -1, -1, 1, -1, -1, 1, 1, 1, 1, 1, 1, 1, -1, 1, -1, 1, 1, -1, 1, 1, 1, -1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1, 1, 1, -1, -1, 1, -1, -1, 1, -1, -1, -1, 1, 1, 1, -1, -1, -1, 1, -1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1, 1, -1, -1, -1, 1, -1, 1, 1, 1, -1, 1, -1, -1, 1, -1, 1, 1, 1, 1, -1, 1, -1, -1, -1, 1, -1, -1, -1, -1, 1, 1, 1, 1, -1, -1, -1, 1, 1, -1, 1, 1, -1, -1, -1, -1, -1, 1, 1, 1, -1, -1, -1, 1, -1, 1, 1, 1, -1, -1, 1, -1, 1, 1, 1, -1, -1, -1, 1, 1, 1, -1, 1, -1, 1, -1, -1, 1, -1, 1, 1, 1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, 1, 1, 1, -1, 1, 1, -1, 1, 1, 1, 1, -1, 1, 1, -1, -1, -1, 1, 1, -1, 1, -1, 1, -1, 1, 1, -1, -1, 1, -1, -1, -1, 1, 1, -1, 1, 1, 1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1, 1, 1, -1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, -1, -1, 1, 1, 1, -1, 1, 1, -1, 1, 1, -1, 1, -1, -1, 1, 1, 1, 1, 1, -1, -1, -1, 1, 1, -1, -1, -1, -1, -1, -1, 1, -1, 1, 1, 1, 1, -1, -1, -1, 1, 1, 1, 1, 1, -1, -1, -1, -1, 1, 1, -1, 1, 1, -1, 1, 1, 1, -1, -1, 1, 1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, -1, 1, -1, 1, -1, -1, -1, 1, 1, -1, 1, -1, -1, -1, -1, -1, -1, -1, 1, 1, 1, 1, 1, -1, -1, -1, -1, 1, -1, 1, -1, -1, 1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, 1, -1, -1, 1, -1, 1, -1, 1, -1, -1, 1, -1, 1, 1, 1, -1, 1, -1, -1, 1, -1, 1, -1, -1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, -1, 1, 1, -1, -1, 1, 1, 1, 1, -1, -1, -1, 1, 1, -1, -1, 1, 1, 1, -1, 1, 1, 1, 1, 1, -1, -1, 1, -1, -1, 1, -1, 1, -1, 1, 1, -1, -1, 1, 1, 1, -1, -1, 1, 1, -1, 1, 1, -1, 1, 1, 1, -1, -1, -1, -1, 1, 1, -1, -1, 1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1, -1, 1, 1, -1, 1, -1, -1, -1, -1, -1, -1, -1, 1, 1, -1, -1, 1, 1, 1, -1, -1, 1, -1, 1, 1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1, 1, -1, -1, 1, 1, -1, -1, 1, -1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, -1, 1, 1, -1, -1, 1, -1, -1, -1, -1, -1, 1, 1, 1, -1, -1, 1, -1, -1, 1, -1, -1, -1, -1, -1, 1, 1, 1, 1, -1, -1, 1, 1, 1, 1, -1, 1, -1, -1, -1, -1, -1, -1, -1, 1, -1, 1, -1, -1, -1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1, 1, -1, -1, -1, -1, -1, 1, -1, 1, -1, -1, 1, 1, -1, 1, 1, 1, 1, -1, 1, -1, 1, 1, 1, -1, 1, 1, -1, 1, 1, -1, -1, -1, -1, -1, -1, 1, 1, -1, 1, -1, -1, -1, 1, -1, 1, 1, -1, -1, 1, -1, -1, 1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1, -1, -1, 1, 1, 1, -1, 1, 1, -1, 1, 1, 1, -1, -1, 1, 1, -1, 1, 1, 1, 1, 1, 1, -1, -1, -1, 1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, 1, 1, -1, 1, 1, -1, 1, -1, 1, 1, 1, 1, 1, 1, -1, 1, 1, -1, -1, 1, -1, -1, -1, -1, -1, -1, 1, -1, -1, 1, 1, -1, 1, -1, -1, 1, -1, 1, -1, -1, -1, -1, -1, -1, -1, 1, 1, 1, 1, -1, -1, -1, -1, 1, 1, -1, 1, 1, 1, -1, 1, 1, -1, 1, 1, 1, 1, -1, -1, 1, -1, -1, -1, 1, 1, -1, 1, -1, -1, -1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1, 1, 1, 1, -1, 1, 1, 1, 1, -1, -1, 1, -1, 1, 1, 1, -1, 1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1, 1, 1, -1, -1, -1, 1, 1, -1, -1, 1, 1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, -1, -1, -1, 1, -1, 1, -1, 1, -1, -1, 1, -1, -1, 1, -1, 1, -1, 1, -1, -1, -1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, 1, -1, 1, -1, 1, -1, -1, -1, 1, 1, -1, 1, 1, -1, -1, -1, -1, 1, 1, -1, 1, 1, -1, -1, 1, 1, 1, 1, -1, 1, -1, -1, -1, 1, 1, -1, 1, -1, 1, -1, -1, -1, 1, -1, 1, 1, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, 1, 1, -1, 1, 1, 1, -1, 1, -1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, 1, -1, -1, -1, 1, -1, -1, 1, 1, -1, -1, -1, 1, -1, -1, -1, 1, -1, 1, -1, 1, -1]
        , True, 1, [])
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_float*1, interpolation_factor)
        self.blocks_multiply_xx_0_1 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0_0_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff((-1))
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_float*1, 50000)
        self.analog_sig_source_x_0_1 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 3705000000, 1, 0, 0)
        self.analog_sig_source_x_0_0_0 = analog.sig_source_f((samp_rate/8), analog.GR_SIN_WAVE, 5000000, 1, 0, 0)
        self.analog_sig_source_x_0_0 = analog.sig_source_f((samp_rate/8), analog.GR_COS_WAVE, 5000000, 1, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 3700000000, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.analog_sig_source_x_0_0_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.analog_sig_source_x_0_1, 0), (self.blocks_multiply_xx_0_1, 1))
        self.connect((self.blocks_delay_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.qtgui_time_sink_x_1, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.qtgui_waterfall_sink_x_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_multiply_xx_0_0_0, 1))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_multiply_xx_0_1, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.fir_filter_xxx_0_0_1, 0))
        self.connect((self.blocks_multiply_xx_0_0_0, 0), (self.fir_filter_xxx_0_0, 0))
        self.connect((self.blocks_multiply_xx_0_1, 0), (self.fir_filter_xxx_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.fir_filter_xxx_0, 0), (self.blocks_multiply_xx_0_0_0, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.fir_filter_xxx_0_0, 0), (self.fir_filter_xxx_0_0_0_0, 0))
        self.connect((self.fir_filter_xxx_0_0_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.fir_filter_xxx_0_0_0_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.fir_filter_xxx_0_0_1, 0), (self.fir_filter_xxx_0_0_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_time_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "test_filtering")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_interpolation_factor(self.samp_rate // 1024000)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq((self.samp_rate/8))
        self.analog_sig_source_x_0_0_0.set_sampling_freq((self.samp_rate/8))
        self.analog_sig_source_x_0_1.set_sampling_freq(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 64000000, 5000000, window.WIN_HAMMING, 6.76))
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, (self.samp_rate/8))
        self.qtgui_waterfall_sink_x_1.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_1.set_samp_rate(self.samp_rate)

    def get_interpolation_factor(self):
        return self.interpolation_factor

    def set_interpolation_factor(self, interpolation_factor):
        self.interpolation_factor = interpolation_factor
        self.blocks_repeat_0.set_interpolation(self.interpolation_factor)




def main(top_block_cls=test_filtering, options=None):

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
