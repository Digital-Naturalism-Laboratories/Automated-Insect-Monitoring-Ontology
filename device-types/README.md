# Device types

[device-types.json](device-types.json) lists the built-in [device types](../README.md#device-type): Standard Mothbox Pro, Standard Mothbox DIY and AMI Device. The Mothbox tools and Antenna should all read their defaults from this one file, so they agree on what each type means. Tools copy it in; they don't edit it in place.

**Status:** skeleton. `null` means "not filled in yet", not "none".
- **Mothbox entries:** the camera, lens and computer come from the Mothbox Unified firmware (`mothbox_hw.py`, `mothbox_exif.py`). The attractor types, power, and target size and distance still need filling in.
- **AMI Device:** to be filled in by the Antenna / AMI team.

## Fields

Field names are camelCase, because this is a shared file (see [Field Names](../README.md#field-names)). Units are part of the name (`powerW`, `targetDistanceCm`), so a number is never ambiguous.

| Field | Meaning |
|---|---|
| `deviceTypeID` | Short stable ID for the type, e.g. `mothbox-pro`. Never changes, even if the name does. |
| `deviceType` | The type's name, as shown to people. |
| `derivedFrom` | The `deviceTypeID` this type was customized from, or `null` for a built-in type. |
| `maker` | Who makes or designs it. |
| `firmware.family` | The firmware line it runs. |
| `firmware.hardwareID` | How the firmware names this hardware (Mothbox: `pro` / `diy`, detected from the I2C chips on the board). |
| `attractors[]` | One entry per [attractor](../README.md#attractor). A device can run several at once. |
| `attractors[].channel` | The firmware output that switches it (`ATTRACT_A`, `ATTRACT_B`). |
| `attractors[].attractorType` | What it is, e.g. a UV LED light of a stated wavelength. |
| `attractors[].attractorLocation` | Where it sits, e.g. `internal`, `external`. |
| `attractors[].powerW` | Power in watts. |
| `target` | The [target](../README.md#target): `targetType` (e.g. sheet), `targetWidthCm`, `targetHeightCm`, and `targetDistanceCm` from the sensor. |
| `sensors[]` | One entry per [sensor](../README.md#sensor): `sensorType` (`camera`, `infrared`, `lidar`, …), `model`, `lens`, `resolutionMegapixels`, `effectiveResolutionPxPerMm`, `sensitivityRange`, `orientation`. |
| `computer` | The computer that runs it. |
| `customFields` | Anything else people want to record, as name–value pairs. |

## Customizing a type

A customized type has its own `deviceTypeID`, sets `derivedFrom` to the type it changes, and lists only the fields it changes. Every other field comes from the parent type. For example, a Mothbox Pro with an external attractor instead of its internal one:

```json
{
  "deviceTypeID": "mothbox-pro-external-uv",
  "deviceType": "Mothbox Pro, external UV attractor",
  "derivedFrom": "mothbox-pro",
  "attractors": [
    { "channel": "ATTRACT_A", "attractorType": "UV LED", "attractorLocation": "external", "powerW": null }
  ]
}
```

Customized types belong in a project's or dataset's own settings, not in this file. This file holds only the built-in types.

## Individual devices

A [device](../README.md#device) (`deviceID`, e.g. `SnappySloth`) names its `deviceTypeID` and its firmware version. It can override any field of its type, for example a different target distance at one deployment. The Mothbox firmware already writes the device's name and firmware version into every photo's EXIF.
