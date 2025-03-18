"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""
import scipy.constants as const
import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    """Calculate Theta from Phase Difference"""

    def __init__(self, antenna_space=1.0, center_frequency=1.0):
        gr.sync_block.__init__(
            self,
            name='Calculate Theta',
            in_sig=[np.complex64, np.complex64],  # Expecting two complex signals
            out_sig=[np.float32]  # Output theta in degrees
        )
        self.antenna_space = antenna_space
        self.center_frequency = center_frequency

    def work(self, input_items, output_items):
        """Compute Theta from Phase Difference"""
        # Extract Rx0 and Rx1
        Rx0 = input_items[0]
        Rx1 = input_items[1]

        # Compute Phase Difference
        phase_diff = np.angle(Rx1) - np.angle(Rx0)  # Phase difference in radians

        # Convert phase difference to degrees
        phase_diff_deg = np.rad2deg(phase_diff)

        # Compute arcsin argument
        d = self.antenna_space
        f = self.center_frequency
        arcsin_arg = np.deg2rad(phase_diff_deg) * const.c / (2 * np.pi * f * d)

        # Clip values to avoid invalid arcsin inputs
        arcsin_arg = np.clip(arcsin_arg, -1, 1)

        # Compute Theta
        output_items[0][:] = np.rad2deg(np.arcsin(arcsin_arg))
        return len(output_items[0])




