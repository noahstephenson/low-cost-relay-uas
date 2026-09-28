# Paper 2784 numerical review audit

Date: 2026-09-25. This audit records the independent placement and hover-stress calculations used to check selected results in the author-supplied final PDF. The PDF is the current paper; the earlier Word and LaTeX review editions have been superseded.

## Independent placement calculation

Inputs held from the paper: 10 km endpoint separation; G at 0 m, relay at 120 m, U at 100 m; an 80 m screen 4 km from G; 2400 MHz; 30 dBm ground transmit level; 1.6 W relay RF output; 6 dBi endpoint and 2 dBi relay gains; 6 dB other loss; -90 dBm receive threshold. Free-space loss is `32.44 + 20 log10(f_MHz) + 20 log10(d_km)` dB. The slant ranges are `sqrt(x^2 + 0.120^2)` and `sqrt((D-x)^2 + 0.020^2)` km. A hop margin is transmit level plus gains minus free-space and other losses minus the receive threshold. First-hop height at the screen is `120(4/x)` m for this geometry.

| Placement | x from G (km) | Ground-to-relay margin (dB) | Relay-to-U margin (dB) | Weaker hop (dB) | First-hop height at screen (m) | Carrier mass at 30 min (kg) |
|---|---:|---:|---:|---:|---:|---:|
| Midpoint | 5.000 | 7.9739 | 10.0175 | 7.9739 | 96.000 | 4.7747 |
| Rounded offset, 0.442D | 4.420 | 9.0441 | 9.0642 | 9.0441 | 108.597 | 4.7747 |
| Exact margin balance | 4.41429 | 9.05535 | 9.05535 | 9.05535 | 108.738 | 4.7747 |

The rounded offset improves the weaker-hop margin by 1.0703 dB and screen-crossing height by 12.597 m. It does not change the modeled carrier mass or 0.4984 m rotor diameter because horizontal placement is absent from the hover calculation. At fixed midpoint placement, the zero-margin separation boundary is 25.0495 km. Holding the rounded 0.442 fraction gives 28.3365 km; the exact balanced fraction gives 28.3642 km. The paper rounds this as roughly 25 to 28 km, without treating it as installed range or a validated site.

## Combined hover-stress calculation

The 2018 NASA hover observations are fitted one point at a time, exactly as in analysis/calibration/sensitivity.py. Each fit changes the effective rotor figure of merit while the structural intercept and other reference inputs stay fixed. The separate 15% allowance multiplies the environment-power factor by 1.15, so both stresses act on the same hover-power coefficient. The existing analytical carrier solver then bisects the rotor-size boundary and evaluates the 30-minute mass and rotor diameter. No new physical model is introduced.

| Single-point fit paired with 15% hover-power allowance | Rotor boundary (min) | Mass at 30 min (kg) | Rotor at 30 min (m) | 30-min size screen |
|---|---:|---:|---:|---|
| 3DR SOLO | 34.858 | 6.791 | 0.594 | pass |
| DJI Phantom 3 | 27.735 | 16.151 | 0.917 | fail |
| 3DR Iris+ | 36.838 | 6.017 | 0.559 | pass |
| Drone America DAx8 | 35.187 | 6.644 | 0.588 | pass |
| SUI Endurance | 41.962 | 4.801 | 0.500 | pass |

The Phantom 3 pairing gives a 27.735-minute rotor boundary, a 16.151 kg mass, and a 0.917 m rotor at 30 minutes. The other four pairings have boundaries from 34.858 to 41.962 minutes. The manuscript rounds these to near 28 minutes, about 16 kg, a 0.92 m rotor, and about 35 to 42 minutes. This is a deterministic sensitivity to selected calibration points and an added allowance, not a probability bound or installed endurance result.

## Verification

- 35 unit tests passed.
- The generated-baseline check passed: 90 primary mission cases and 1,890 row-level results are current.
- The independent manuscript checker examined all 1,890 records without discrepancy.
- The author-supplied final PDF is 15 letter-size pages and is byte-for-byte identical to submission/relay_uas_aeroconf.pdf.

These checks support the numerical baseline; they do not establish installed link performance, hover power, command-fault behavior, or operational service.

## Current PDF SHA-256

E2A2C93A2F38501F13FB161A7F50258D2AE99BBD22E2F8CC0AFA7D96C0FBB7C8
