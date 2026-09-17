import numpy as np
import argparse
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import simulator

def sigma(color_idx, mag, labels, color_ub):
    while True:
        count = len(mag)
        p = np.polyfit(color_idx, mag, 3)
        fitted_mag = np.polyval(p, color_idx)
        residuals = mag - fitted_mag
        std = np.std(residuals)
        m = np.abs(residuals) <= (3 * std)
        color_idx, mag, labels, color_ub = color_idx[m], mag[m], labels[m], color_ub[m]
        if count == len(mag):
            break
    return color_idx, mag, labels, color_ub

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_stars",
                        type=int,
                        default=1000,
                        help="Number of stars in the cluster")

    parser.add_argument("--field",
                        type=int,
                        default=50,
                        help="Number of field stars")

    parser.add_argument("--seed",
                        type=int,
                        default=4,
                        help="seed value")

    args = parser.parse_args()

    teff, mag_v, labels, ub, bv = simulator.generate_cluster(n_stars=args.n_stars,
                                                             expected_field_stars=args.field,
                                                             seed=args.seed)

    initial_field_stars = np.sum(~labels)
    cleaned_bv, cleaned_mag_v, cleaned_labels, cleaned_ub = sigma(bv, mag_v, labels, ub)

    remaining_field_stars = np.sum(~cleaned_labels)
    rejected_field_stars = initial_field_stars - remaining_field_stars
    cleaning_efficiency = (rejected_field_stars / initial_field_stars) * 100

    n_field_c = args.n_stars
    field_c = args.field
    seed_v = args.seed

    print(f"Seed value: {seed_v}")
    print(f"Number of cluster stars: {n_field_c}")
    print(f"Number of expected field stars: {field_c}")
    print(f"Detected Field Stars: {initial_field_stars}")
    print(f"Cleared Field Stars: {rejected_field_stars}")
    print(f"Remaining Field Stars: {remaining_field_stars}")
    print(f"Efficiency: %{cleaning_efficiency:.2f}")

    fig, (ax1, ax2, ax3) = plt.subplots(1,
                                        3,
                                        figsize=(18, 6))

    ax1.scatter(bv,
                mag_v,
                s=2,
                c="gray",
                alpha=0.5)

    ax1.set_title("Raw H-R Diagram")
    ax1.set_xlabel("B - V")
    ax1.set_ylabel("Mag_v")
    ax1.grid(True,
             linestyle="--",
             alpha=0.7)
    
    ax1.xaxis.set_minor_locator(AutoMinorLocator())
    ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax1.tick_params(which="both", direction="in", top=True, right=True)
    ax1.grid(which="major", linestyle="--", alpha=0.5)
    ax1.grid(which="minor", linestyle=":", alpha=0.5)
    ax1.invert_yaxis()

    ax2.scatter(cleaned_bv,
                cleaned_mag_v,
                s=2,
                c="blue")

    ax2.set_title("Cleaned H-R Diagram (3-Sigma)")
    ax2.set_xlabel("B - V")
    ax2.set_ylabel("Mag_v")
    ax2.grid(True,
             linestyle="--",
             alpha=0.7)

    ax2.xaxis.set_minor_locator(AutoMinorLocator())
    ax2.yaxis.set_minor_locator(AutoMinorLocator())
    ax2.tick_params(which="both", direction="in", top=True, right=True)
    ax2.grid(which="major", linestyle="--", alpha=0.5)
    ax2.grid(which="minor", linestyle=":", alpha=0.5)
    ax2.invert_yaxis()

    ax3.scatter(cleaned_bv,
                cleaned_ub,
                s=2,
                c="purple")

    ax3.set_title("Two-Color Diagram (U-B  B-V)")
    ax3.set_xlabel("B - V")
    ax3.set_ylabel("U - B")
    ax3.grid(True,
             linestyle="--",
             alpha=0.7)
    
    ax3.xaxis.set_minor_locator(AutoMinorLocator())
    ax3.yaxis.set_minor_locator(AutoMinorLocator())
    ax3.tick_params(which="both", direction="in", top=True, right=True)
    ax3.grid(which="major", linestyle="--", alpha=0.5)
    ax3.grid(which="minor", linestyle=":", alpha=0.5)
    ax3.invert_yaxis()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()