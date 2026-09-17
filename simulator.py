import numpy as np
import constants

def planck_function(wavelength, temperature):
    spectral_radiance = (((2 * constants.Planck_constant * (constants.Speed_of_light ** 2)) / wavelength ** 5) *
                         (1 / (np.exp((constants.Planck_constant * constants.Speed_of_light) / (
                                 wavelength * constants.Boltzmann_constant * temperature)) - 1)))
    return spectral_radiance

def generate_cluster(n_stars=1000, expected_field_stars=50, seed=4):
    np.random.seed(seed)
    p = 1.0 - constants.Alpha
    u = np.random.random(n_stars)
    mass = ((constants.M_min ** p) + u * ((constants.M_max ** p) - (constants.M_min ** p))) ** (1.0 / p)
    t_eff = 5778.0 * (mass ** 0.505)
    flux_u = planck_function(constants.Lambda_u, t_eff)
    flux_b = planck_function(constants.Lambda_b, t_eff)
    flux_v_t = planck_function(constants.Lambda_v, t_eff)
    u_b = -2.5 * np.log10(flux_u / flux_b)
    b_v = -2.5 * np.log10(flux_b / flux_v_t)

    clean_flux = []
    for temp in t_eff:
        raw_spectrum = planck_function(constants.Wav, temp)
        filtered_spectrum = raw_spectrum * constants.SYSTEM_THROUGHPUT
        integrated_spectrum = np.trapezoid(filtered_spectrum, constants.Wav)
        clean_flux.append(integrated_spectrum)
    clean_flux_array = np.array(clean_flux)

    plate_scale = (constants.Pixel_Size / constants.Focal_Length) * 206265.0
    fwhm_pix = constants.Seeing_Arcsec / plate_scale
    r_aperture = 1.5 * fwhm_pix
    npix = int(np.pi * (r_aperture ** 2))

    distance_m = constants.Cluster_distance_PC * constants.PC_to_M
    collecting_area = np.pi * ((constants.Telescope_Diameter / 2.0) ** 2)
    photon_energy = (constants.Planck_constant * constants.Speed_of_light) / constants.Lambda_v
    radius = constants.R_sun * (mass ** 0.74)
    solid_angle = np.pi * ((radius / distance_m) ** 2)

    c_array = (solid_angle * collecting_area) / photon_energy
    n_photons = clean_flux_array * c_array * constants.Exp_time

    n_sky = constants.Sky_rate * npix * constants.Exp_time
    n_dark = constants.Dark_rate * npix * constants.Exp_time
    n_read = npix * (constants.Read_noise_RMS ** 2)

    sigma = np.sqrt(n_photons + n_sky + n_dark + n_read)
    observed_photons = np.random.normal(n_photons, sigma)

    safe_photons = np.clip(observed_photons, 1.0, None)
    flux_rate = safe_photons / constants.Exp_time
    m_v = -2.5 * np.log10(flux_rate) + constants.Zero_point

    n_field = np.random.poisson(expected_field_stars)
    field_teff = np.random.uniform(3500.0, 9500.0, n_field)
    field_m_v = np.random.uniform(np.min(m_v) - 1.0, np.max(m_v) + 2.0, n_field)
    field_u_b = np.random.uniform(-1.0, 2.0, n_field)
    field_b_v = np.random.uniform(-0.5, 2.0, n_field)

    cluster_labels = np.ones(n_stars, dtype=bool)
    field_labels = np.zeros(n_field, dtype=bool)

    all_teff = np.concatenate([t_eff, field_teff])
    all_mag_v = np.concatenate([m_v, field_m_v])
    all_labels = np.concatenate([cluster_labels, field_labels])
    all_ub = np.concatenate([u_b, field_u_b])
    all_bv = np.concatenate([b_v, field_b_v])

    return all_teff, all_mag_v, all_labels, all_ub, all_bv

if __name__ == "__main__":
    teff, mag_v, labels, ub, bv = generate_cluster()
    print(f"Total Stars: {len(teff)}")
    print(f"Genuine Cluster Members: {np.sum(labels)}")
    print(f"Field Stars: {np.sum(~labels)}")