import numpy as np

plate_scale = 0.778           # arcsec/pixel  # 0.788 arcsec/pixel for 2x2 binning
gain = 1.055                  # e-/ADU
read_noise_electrons = 12.96  # e- for 2x2 binning
dark_current = 0.0243         # e-/pixel/s for 2x2 binning

low_sky_background = 16     # e-/arcsec^2/s
med_sky_background = 100    # e-/arcsec^2/s
high_sky_background = 300   # e-/arcsec^2/s

telescope_aperture = 1      # m
scale_height = 8000         # m
C_Y = 1.3                   # m^{2/3} s^(1/2)
h_obs = 2396                #

twenty_px_zp = 24.3  # mag
ten_px_zp = 24       # mag
five_px_zp = 23.7    # mag

read_out_time = 0.993  # s


def get_aperture_noise(moon_percentage, mean_cube_airmass, bp_mag, exposure_time=30):
    if bp_mag < 14:
        aperture_size = 20
        zp = twenty_px_zp
    elif bp_mag < 18:
        aperture_size = 10
        zp = ten_px_zp
    else:
        aperture_size = 5
        zp = five_px_zp

    if moon_percentage < 25:
        sky_background = low_sky_background
    elif moon_percentage < 75:
        sky_background = med_sky_background
    else:
        sky_background = high_sky_background

    n_pixels = np.pi * aperture_size ** 2
    read_noise = read_noise_electrons * np.sqrt(n_pixels)
    dark_noise = np.sqrt(dark_current * exposure_time * n_pixels)
    signal = 10 ** ((zp - bp_mag) / 2.5) * exposure_time
    poisson_shot_noise = np.sqrt(signal)
    sky_background_noise = np.sqrt(sky_background * plate_scale ** 2 * n_pixels * exposure_time)
    scintillation_noise = np.sqrt(1e-5 * C_Y ** 2 * telescope_aperture ** (-4 / 3) * mean_cube_airmass * np.exp(
        -2 * h_obs / scale_height) / exposure_time) * signal

    total_noise = np.sqrt(read_noise**2 + dark_noise**2 + poisson_shot_noise**2 + sky_background_noise**2 + scintillation_noise**2)

    total_hour_noise_ppm = (total_noise / signal) * np.sqrt((exposure_time + read_out_time) / 3600) * 1e6
    return total_hour_noise_ppm
