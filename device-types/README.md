# Device types

[device-types.json](device-types.json) lists the built-in [device types](../README.md#device-type): Standard Mothbox Pro, Standard Mothbox DIY and AMI Device. The Mothbox tools and Antenna should all read their defaults from this one file, so they agree on what each type means. Tools copy it in; they don't edit it in place.

**After editing it**, run `python3 device-types/sync-copies.py` to copy it into Classify (`src/config/device-types.json`), Process (`assets/device-types.json`) and the firmware settings editor (embedded in `mothbox_settings_editor.html`). `--check` only reports which copies differ.

**Built-in types:**
- **Standard Mothbox Pro:** Andrew's measured profile.
    - **Hardware:** version 5.0.6, firmware 6.1.2.
    - **Attractors:** a Mothbeam (UV) and a Mothbeam (Visible), both internal, at `1 switch` (2 W).
    - **Target:** a felt sheet, 28.9 × 20.5 cm, 24.5 cm from the camera.
    - **Camera:** OwlSight 64 MP on a Raspberry Pi 5.
- **Standard Mothbox DIY:** still a skeleton. `null` means "not filled in yet", not "none".
- **AMI Device, DIOPSIS, Entocam, LepiSense:** filled in from the [InsectAI COST Action hardware database](https://insectai-cost-action.github.io/hardware-db/) (2026-11-23).
    - **Where the database's facts go:** what it states maps onto the usual fields. Its description goes in `description`. Size, weight, IP rating, temperatures, autonomy and links go in `customFields`, with `source`.
    - **Left as `null`:** anything the database doesn't state, such as the AMI's attractor and camera, and most target details.
    - **Corrections:** the AMI and LepiSense teams can correct their entries.

## Fields

Format version 3 (2026-11-23):
- **Attractors:** gained `hardwareVersion` and `configuration`.
- **Targets:** gained `color`.
- **Devices:** gained `powerSources` and `description`.
- **New `choices` section:** suggested values for the editors.

Format version 2 (2026-11-23): `targets` became a list, sensors gained `resolution` (text) and `notes`, and `hardwareVersion` and `firmware.version` were added. Field names are camelCase, because this is a shared file (see [Field Names](../README.md#field-names)). Units are part of the name (`powerW`, `targetDistanceCm`), so a number is never ambiguous.

| Field | Meaning |
|---|---|
| `deviceTypeID` | Short stable ID for the type, e.g. `mothbox-pro`. Never changes, even if the name does. |
| `deviceType` | The type's name, as shown to people. |
| `derivedFrom` | The `deviceTypeID` this type was customized from, or `null` for a built-in type. |
| `maker` | Who makes or designs it. |
| `hardwareVersion` | The hardware (board / enclosure) version, e.g. `5.1.0`. |
| `firmware.family` | The firmware line it runs. |
| `firmware.version` | The firmware version, e.g. `6.1.2`. |
| `firmware.hardwareID` | How the firmware names this hardware (Mothbox: `pro` / `diy`, detected from the I2C chips on the board). |
| `attractors[]` | Zero or more [attractors](../README.md#attractor), used at the same time. |
| `attractors[].channel` | The firmware output that switches it (`ATTRACT_A`, `ATTRACT_B`). |
| `attractors[].attractorType` | What it is, e.g. `Mothbeam (UV)`, `Mothbeam (Visible)`, or a UV LED light of a stated wavelength. |
| `attractors[].hardwareVersion` | Optional. The attractor's own hardware version, e.g. Mothbeam `5.0.3`. |
| `attractors[].attractorLocation` | Where it sits: `internal`, `external` or `in target`. |
| `attractors[].configuration` | Optional. Which of its switches are on, e.g. Mothbeam `1 and 2 switches` (see `choices.attractorPowerOptions`). |
| `attractors[].powerW` | Power in watts. |
| `targets[]` | Zero or more [targets](../README.md#target): `targetType` (e.g. sheet, tube), `material` (e.g. felt, canvas, vinyl), optional `color` (e.g. white, yellow), `widthCm`, `heightCm`, and `distanceCm` from the sensor. |
| `sensors[]` | One or more [sensors](../README.md#sensor): `sensorType` (`camera`, `infrared`, `lidar`, …), `model`, `lens`, `resolution` (e.g. `64 MP`), `effectiveResolutionPxPerMm`, `sensitivityRange`, `orientation`, `notes`. |
| `powerSources[]` | Optional, one or more: `powerSourceType` (`battery`, `grid`, `solar`) and `model` (e.g. `Standard TalentCell PB120B1`). |
| `powerSources[].capacityWh` | Batteries: energy capacity in watt hours. |
| `powerSources[].nominalVoltageV` | Batteries: the voltage printed on the battery. |
| `powerSources[].voltageAt80PercentV`, `voltageAt20PercentV` | Batteries: the voltage when about 80% and 20% full, which calibrates a battery gauge. |
| `computer` | The computer that runs it. |
| `description` | Notes about the whole device. |
| `customFields` | Anything else people want to record, as name–value pairs. |

## Choices

`choices` lists suggested values that the editors offer: attractor types and locations, target types, materials and colors, sensor types, power source types, and known batteries with their capacity and voltages. The Standard TalentCell PB120B1 values (142 Wh, 11.1 V, 12.0 V at 80%, 10.5 V at 20%) are also the Mothbox firmware's battery defaults. Any other value is still allowed.

`choices.attractorPowerOptions` gives the power of each light configuration for attractors that have them. These are Mothbeam 5.0.3, measured at 12 V and rounded to the nearest half watt, except `0 switches`, which stays at 0.2 W. `measured` keeps the measured value.

| Configuration | Measured | `powerW` |
|---|---|---|
| 0 switches | 17 mA / 0.20 W | 0.2 |
| 1 switch | 165 mA / 1.98 W | 2 |
| 1 and 2 switches | 303 mA / 3.64 W | 3.5 |
| 1, 2 and 3 switches | 463 mA / 5.56 W | 5.5 |
| 3 and 4 switches | 379 mA / 4.55 W | 4.5 |
| 1, 3 and 4 switches | 478 mA / 5.74 W | 5.5 |
| All 4 switches | 570 mA / 6.84 W | 7 |

The table was measured on the visible Mothbeam. `Mothbeam (UV)` uses the same numbers, which are close enough (`measuredOn` says so).

## Customizing a type

A customized type has its own `deviceTypeID`, sets `derivedFrom` to the type it changes, and lists only the fields it changes. Every other field comes from the parent type. For example, a Mothbox Pro with an external attractor instead of its internal one:

```json
{
  "deviceTypeID": "mothbox-pro-external-uv",
  "deviceType": "Mothbox Pro, external UV attractor",
  "derivedFrom": "mothbox-pro",
  "attractors": [
    { "channel": "ATTRACT_A", "attractorType": "UV LED", "attractorLocation": "external", "powerW": 10 }
  ]
}
```

Customized types belong in a project's or dataset's own settings, not in this file. This file holds only the built-in types. Where they live today:

- **Firmware settings editor:** "Customize" on the Device section saves the whole description in the settings file's `device_type` row, and every photo's EXIF carries it (`UserComment` → `device`).
- **Process, Insert Metadata tab:** "Check photos" shows what the photos say. Keep it, or choose a built-in type to correct it. The choice is written to each detection file as `deviceTypeID`, `deviceType` and `deviceTypeDefinition`.
- **Classify:** a project's custom types are in `02_records/device-types.ndjson`. New ones found in detection files are added when a project is made or sessions are added. Edit them in the dataset menu → Devices…

## Individual devices

A [device](../README.md#device) (`deviceID`, e.g. `SnappySloth`) names its `deviceTypeID` and its firmware version. It can override any field of its type, for example a different target distance at one deployment. The Mothbox firmware already writes the device's name and firmware version into every photo's EXIF.
