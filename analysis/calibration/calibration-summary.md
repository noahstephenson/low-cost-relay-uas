# Carrier calibration summary

The five-point NASA full-vehicle hover fit gives an effective `FM * eta_d / k_env` of 0.447676. With motor/controller efficiency fixed at 0.83 and the declared reference environment multiplier fixed at 1.15, the fitted rotor figure of merit is 0.620274. The fit uses each test article's measured supported thrust and rotor disk area, not the relay model's fixed disk loading.

The NASA component-mass anchor gives `structure_base_mass_kg = 0.163173` while retaining the declared structural growth, disk-area, avionics, power-electronics, mount, propulsion-specific-power, and thrust-margin terms.

Fit residual range: -18.56% to +14.64%. Held-out hover-endurance error range: -6.74% to +3.17%. No held-out vehicle misses the +/-20% target.

The endurance check uses the manufacturers' published discharge condition and therefore does not apply the relay mission's 20% reserve or 90% depth-of-discharge policy. Forward-flight-only endurance is excluded.
