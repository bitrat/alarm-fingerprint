#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Top Block
# Generated: Sat Nov 14 03:38:27 2015
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import wx
# Added
from datetime import datetime
import time

class top_block(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Top Block")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.symb_rate = symb_rate = 30000
        self.samp_rate = samp_rate = 10e6
        self.decimation = decimation = 300
        self.symb_rate_slider = symb_rate_slider = 4000
        self.samp_per_sym = samp_per_sym = int((samp_rate/(decimation)) / symb_rate)
        self.freq_offset = freq_offset = 1.8e6
        self.freq = freq = 433.92e6
        self.channel_trans = channel_trans = 1.2e6
        self.channel_spacing = channel_spacing = 3000000+2000000

        # Added
        self.addconst = addconst = 0

        # Changed
        # Changed from the original Yale_FileInput_BinaryOutput GNURadio Flowgraph export
        self.initpathprefix = initpathprefix = "/home/user/alarm-fingerprint/AlarmGnuRadioFiles/"
        self.pathprefix = pathprefix = "/home/user/alarm-fingerprint/AlarmGnuRadioFiles/Captured/"
        # Same as external hard drive processing code variables
        self.finput = finput = initpathprefix+"Capture_init.cap"
        self.foutput = foutput = pathprefix+finput.rsplit("/", 1)[1] 

        # Added
        self.recfile4 = recfile4 = initpathprefix+"/init/_AddConst"+str(addconst)+ "_Yale.dat"

        ##################################################
        # Blocks
        ##################################################
        _channel_trans_sizer = wx.BoxSizer(wx.VERTICAL)
        self._channel_trans_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_channel_trans_sizer,
        	value=self.channel_trans,
        	callback=self.set_channel_trans,
        	label='channel_trans',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._channel_trans_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_channel_trans_sizer,
        	value=self.channel_trans,
        	callback=self.set_channel_trans,
        	minimum=0,
        	maximum=1.8e6,
        	num_steps=10,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_channel_trans_sizer)
        _symb_rate_slider_sizer = wx.BoxSizer(wx.VERTICAL)
        self._symb_rate_slider_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_symb_rate_slider_sizer,
        	value=self.symb_rate_slider,
        	callback=self.set_symb_rate_slider,
        	label='symb_rate_slider',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._symb_rate_slider_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_symb_rate_slider_sizer,
        	value=self.symb_rate_slider,
        	callback=self.set_symb_rate_slider,
        	minimum=0,
        	maximum=10e3,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_symb_rate_slider_sizer)
        self.low_pass_filter_0 = filter.fir_filter_fff(decimation, firdes.low_pass(
        	1, samp_rate, 600e3, 5e3, firdes.WIN_BLACKMAN, 6.76))
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(1, (firdes.low_pass(1, samp_rate, channel_spacing, channel_trans, firdes.WIN_BLACKMAN,6.76)), -freq_offset, samp_rate)
        self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_ff(samp_per_sym*(1+0.0), 0.25*0.175*0.175, 0.5, 0.175, 0.005)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, finput, False)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_char*1, recfile4, False)
        self.blocks_file_sink_0_0.set_unbuffered(False)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.blocks_add_const_vxx_0 = blocks.add_const_vff((addconst, ))

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.digital_clock_recovery_mm_xx_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.blocks_file_sink_0_0, 0))



    def get_pathprefix(self):
        return self.pathprefix

    def set_pathprefix(self, pathprefix):
        self.pathprefix = pathprefix
        # Changed
        self.set_finput(self.pathprefix+"Capture_init.cap")

    def get_finput(self):
        return self.finput

    def set_finput(self, finput):
        self.finput = finput
        # Changed
        self.set_foutput("/home/user/alarm-fingerprint/AlarmGnuRadioFiles/Captured/"+finput.rsplit("/", 1)[1])
        #
        self.blocks_file_source_0.open(self.finput, False)

    def get_symb_rate(self):
        return self.symb_rate

    def set_symb_rate(self, symb_rate):
        self.symb_rate = symb_rate
        self.set_samp_per_sym(int((self.samp_rate/(self.decimation)) / self.symb_rate))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_samp_per_sym(int((self.samp_rate/(self.decimation)) / self.symb_rate))
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1, self.samp_rate, self.channel_spacing, self.channel_trans, firdes.WIN_BLACKMAN,6.76)))
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 600e3, 5e3, firdes.WIN_BLACKMAN, 6.76))

    def get_foutput(self):
        return self.foutput

    def set_foutput(self, foutput):
        self.foutput = foutput
        # Changed
        self.set_recfile4(self.foutput+"_AddConst"+str(self.addconst)+ "_Yale.dat")

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self.set_samp_per_sym(int((self.samp_rate/(self.decimation)) / self.symb_rate))

    def get_addconst(self):
        return self.addconst

    def set_addconst(self, addconst):
        self.addconst = addconst
        # Changed
        self.set_recfile4(self.foutput+"_AddConst"+str(self.addconst)+ "_Yale.dat")
        self.blocks_add_const_vxx_0.set_k((self.addconst, ))

    def get_symb_rate_slider(self):
        return self.symb_rate_slider

    def set_symb_rate_slider(self, symb_rate_slider):
        self.symb_rate_slider = symb_rate_slider
        self._symb_rate_slider_slider.set_value(self.symb_rate_slider)
        self._symb_rate_slider_text_box.set_value(self.symb_rate_slider)

    def get_samp_per_sym(self):
        return self.samp_per_sym

    def set_samp_per_sym(self, samp_per_sym):
        self.samp_per_sym = samp_per_sym
        self.digital_clock_recovery_mm_xx_0.set_omega(self.samp_per_sym*(1+0.0))

    # Added
    def get_recfile4(self):
        return self.recfile4

    def set_recfile4(self, recfile4):
        self.recfile4 = recfile4
        self.blocks_file_sink_0_0.open(self.recfile4)
    #
 
    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(-self.freq_offset)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq

    def get_channel_trans(self):
        return self.channel_trans

    def set_channel_trans(self, channel_trans):
        self.channel_trans = channel_trans
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1, self.samp_rate, self.channel_spacing, self.channel_trans, firdes.WIN_BLACKMAN,6.76)))
        self._channel_trans_slider.set_value(self.channel_trans)
        self._channel_trans_text_box.set_value(self.channel_trans)

    def get_channel_spacing(self):
        return self.channel_spacing

    def set_channel_spacing(self, channel_spacing):
        self.channel_spacing = channel_spacing
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1, self.samp_rate, self.channel_spacing, self.channel_trans, firdes.WIN_BLACKMAN,6.76)))

if __name__ == '__main__':
    import sys
    if (len(sys.argv) < 3):
        sys.stderr.write("Error: usage: " + sys.argv[0] + " <constant> <fileinput> "+"\n")
        sys.stderr.flush()
        exit(2) 
    else:
        const = float(sys.argv[1])
        finput = sys.argv[2]
    # Changed - local or external hard drive
    foutput = "/home/user/alarm-fingerprint/AlarmGnuRadioFiles/Captured/"+finput.rsplit("/", 1)[1]
    tb = top_block()
    tb.Start(True)
    tb.set_addconst(const)
    tb.set_finput(finput)
    print ("Processing file ....Add Const is "+str(const)+"\n")
    print ("Processing file "+str(finput)+"\n")
    time.sleep(30)
    tb.stop()
