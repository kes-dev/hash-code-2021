import os.path
import numpy as np
from multiprocessing import Pool

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import datautil as du

# estimate arrival time of each car, use the most dominant frequency as period
class Synchronise:
    def __init__(self, map_data, cfg, result_dir):
        self.map_data = map_data
        self.cfg = cfg
        self.result_dir = result_dir

    def validate(self):
        assert ('est_wait_factor' in self.cfg.keys())
        assert self.cfg['est_wait_factor'] > 0.0
        assert self.cfg['est_wait_factor'] < 1.0

        assert ('max_period' in self.cfg.keys())
        assert self.cfg['max_period'] > 0
        print('valid self.cfg')

    # estimate wait time at intersection i
    def est_wait(self, inter):
        return float(self.cfg['est_wait_factor']) * len(inter.outgoing)

    def build_hist(self, hist_input):
        i, inter, bins = hist_input
        inter_hist = {}
        inter_hist_freq = {}
        freq_bin = np.fft.fftfreq(len(bins) - 1)

        for st_name, st_eta in inter.items():
            hist, _ = np.histogram(st_eta, bins=bins)
            inter_hist[st_name] = hist
            ft = np.fft.fft(hist)
            inter_hist_freq[st_name] = sqrt(np.real(ft) * np.real(ft) + np.imag(ft) * np.imag(ft))

        fig = make_subplots(rows=2, cols=1)
        for st_name, hist in inter_hist.items():
            fig.add_trace(go.Scattergl(x=bins[:-1], y=hist, mode="lines", name=st_name+'_hist'), row=1, col=1)

        for st_name, freq in inter_hist_freq.items():
            fig.add_trace(go.Scattergl(x=freq_bin, y=freq, mode="lines", name=st_name+'_freq'), row=2, col=1)

        fig.update_layout(title_text='intersection: {}'.format(i))
        plot_filename = 'inter-{}.html'.format(i)
        fig.write_html(os.path.join(self.result_dir, plot_filename))

        print('hist: {}, done'.format(i))
        return i, inter_hist

    def gen_schedule(self):
        eta = []
        eta_hist = []
        ewait = []

        for i in range(0, self.map_data.misc.int_count):
            eta.append({})
            eta_hist.append({})

        # estimate wait time
        for inter in self.map_data.intersection:
            ewait.append(self.est_wait(inter))

        # estimate arrival time
        for c in self.map_data.trip:
            acc_length = 0
            for st_name in c.path:
                st = self.map_data.street[st_name]
                acc_length += st.length + ewait[st.end]
                if st_name in eta[st.end]:
                    eta[st.end][st_name].append(int(round(acc_length)))
                else:
                    eta[st.end][st_name] = [int(round(acc_length))]

        bins = list(range(0, self.map_data.misc.d + 1, 1))

        hist_input_list = []
        for i, inter in enumerate(eta):
            hist_input_list.append((i, inter, bins))

        try:
            pool = Pool(12)
            hists = pool.imap_unordered(self.build_hist, hist_input_list, 10)
        finally:
            pool.close()
            pool.join()

        for i, inter_hist in hists:
            eta_hist[i] = inter_hist

