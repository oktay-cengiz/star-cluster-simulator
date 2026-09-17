import numpy as np

Planck_constant = 6.62607004e-34
Speed_of_light = 3.0e8
Boltzmann_constant = 1.3806488e-23
R_sun = 6.9634e8
PC_to_M = 3.0857e16

Wav = np.linspace(300e-9, 1000e-9, 1000)
Lambda_v = 550e-9
Lambda_b = 440e-9
Lambda_u = 365e-9

T_i = 0.80
T_e = 0.82 * (Wav / 550e-9) ** 0.1
T_t = 0.85
T_s = 0.85 * np.exp(-0.5 * ((Wav - 550e-9) / 37.4e-9) ** 2)
T_r = 0.80

SYSTEM_THROUGHPUT = T_i * T_e * T_t * T_s * T_r

Telescope_Diameter = 0.40
Focal_Length = 2.0
Pixel_Size = 9e-6
Seeing_Arcsec = 1.8

Sky_rate = 10.0
Dark_rate = 0.5
Read_noise_RMS = 5.0
Zero_point = 25.0

Cluster_distance_PC = 135.0
Exp_time = 60.0
Alpha = 2.35
M_min = 0.5
M_max = 3.0