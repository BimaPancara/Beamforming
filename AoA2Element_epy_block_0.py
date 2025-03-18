"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr



class blk(gr.sync_block):  
    """Angle of Arrival Estimation for a 2-element ULA"""

    def __init__(self, frequency=2.4e9, array_spacing=0.5):  
        """Initialize parameters"""
        gr.sync_block.__init__(
            self,
            name='Angle of Arrival Estimation (2-Element ULA)',
            in_sig=[np.float32, np.float32],  # Two phase inputs (already in radians)
            out_sig=[np.float32]  # Output AoA in degrees
        )
        self.frequency = frequency
        self.array_spacing = array_spacing
        self.wavelength = 3e8 / frequency  # Speed of light / frequency

    def work(self, input_items, output_items):
        """Process incoming phase signals"""
        phi_0 = input_items[0]  # Already in radians
        phi_1 = input_items[1]

        num_samples = len(phi_0)
        theta_deg = np.zeros(num_samples, dtype=np.float32)

        for i in range(num_samples):
            # Compute phase differences (with proper wrapping)
            delta_phi_1 = np.angle(np.exp(1j * (phi_1[i] - phi_0[i])))  # Between Antenna 0 & 1
            
            # Take the average phase difference for robustness
            delta_phi_avg = delta_phi_1 

            # Estimate AoA
            sin_theta = (self.wavelength * delta_phi_avg) / (2 * np.pi * self.array_spacing)
            sin_theta = np.clip(sin_theta, -1, 1)  # Prevent NaN errors

            theta_rad = np.arcsin(sin_theta)
            theta_deg[i] = np.degrees(theta_rad)

        output_items[0][:] = theta_deg
        return len(output_items[0])
