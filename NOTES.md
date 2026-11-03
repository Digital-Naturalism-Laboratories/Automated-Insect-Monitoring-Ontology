# Naming notes

Rolling notes on how terms in this ontology were chosen: what was discussed, why each decision went the way it did, what is still open, and what we want to ask other groups. The glossary itself is in [README.md](README.md).

Add new entries at the top of the log, with a date. When a decision changes, add a new entry instead of editing the old one, so the history stays readable.

## Requests for the Antenna / AMI team

A living list. Status moves from “To ask” to “Asked” to the answer.

| Topic | What we are asking | Status |
|---|---|---|
| Identification vs classification | Use one word, “identification”, for both machine and human answers, and tell them apart with `identifierType` (`machine` / `human`) and `identifierName`. Antenna currently stores machine answers as `Classification` (“Machine prediction” on screen) and human answers as `Identification`. | To ask |
| Site and station | Adopt “site”, used interchangeably with “station” on screen if they prefer, and keep coordinates in a separate “location” instead of bundling them with the station. | To ask |
| Device type and device ID | Keep “Device type” for the hardware kind (`deviceType`), and consider recording individual devices (`deviceID`, e.g. `SnappySloth`). Antenna currently has no record of an individual device. | To ask |
| Catalogue of Life keys | Store `col_taxon_key` beside `gbif_taxon_key`. Newer GBIF species list downloads use Catalogue of Life keys, so taxa matched only by backbone key will stop lining up. | To ask |
| Rotated boxes | Accept an optional rotated box on detections, so oriented boxes from Mothbox detectors are not lost. | Not decided yet; ask once decided |
| Field-name style | Agree on one style for field names: camelCase (`deviceID`, `siteName`, like Darwin Core) or snake_case (`gbif_taxon_key`, like Antenna's code). | To raise at the next Antenna meeting |

## Open questions

- **How a rotated box is written.** An upright box can be written several ways, and a rotated one has even more. See [Ways to write a box](#ways-to-write-a-box) below. Proposal: always give an upright box that every tool can read, and add the rotated box as four corner points when there is one; treat any angle as a convenience copy, not the record. Not decided yet.
- **Target or stage.** “Target” (the sheet, tube or flower creatures land on) is still a draft name; “stage” is one alternative.
- **Project vs dataset.** Andrew is still thinking about whether these are two terms (the body of work and its people, and a portable package of its files) or one.

## Background

### What “event” means elsewhere

- **Darwin Core.** An Event is “an action that occurs at some location during some time”. It works at any scale: a whole survey, one night of trapping, or one camera-trap image can each be an event. Events can nest: `parentEventID` points to the larger event that contains this one. Each event has an `eventDate`, which can be a span (e.g. `2026-07-27T19:00/2026-07-28T05:00`), and can carry `samplingProtocol` and `samplingEffort`.
- **Antenna.** Its `Event` is shown as “Session” on screen. It is built automatically for each station: captures are sorted by time, a gap longer than 120 minutes (adjustable per project) starts a new event, and no event runs longer than 24 hours. Each event is named by the date of its first capture. In practice that is about one night, but a schedule with long breaks can split a night in two; the default Mothbox schedule has a 121-minute break from 23:59 to 02:00. Antenna's draft Darwin Core Archive export writes one Darwin Core event per Antenna session and reserves `parentEventID` for a later station or deployment level.
- **Camtrap DP.** “Event” is much smaller there: a burst of photos taken close together, such as one animal triggering a camera.

Because Darwin Core events nest, the session and the capture window do not compete; they are events at different levels:

```
Deployment (parent event)
 └─ Session: one night                 (Antenna's Event)
     └─ Capture window: 19:00–19:59    (Mothbox firmware "session")
         └─ Source file: one photo
```

### Ways to write a box

| Who | Shape | How it is written |
|---|---|---|
| Antenna | Upright only | Corners `x1, y1, x2, y2` in pixels |
| Camtrap DP | Upright only | `x, y, width, height` from the top-left corner, as fractions (0–1) of the photo's size |
| Mothbot detection files | Rotated | X-AnyLabeling “shapes”: four corner points in pixels, plus `direction`, an angle |
| X-AnyLabeling hand labels | Rotated | The same shape format; `direction` is in radians (0 to 2π) |
| YOLO OBB detectors (used by Mothbot) | Rotated | Centre, width, height and an angle in radians |

The Mothbox tools write X-AnyLabeling's format because people also hand-label data in X-AnyLabeling; that is where the word “shape” comes from.

The four corners already define the box completely, so `direction` repeats information the corners hold. X-AnyLabeling uses it when a shape is reopened for editing. Mothbot Classify ignores it and works out the rotation from the corners.

The repeated angle is also inconsistent today. X-AnyLabeling hand labels store it in radians (a hand-labelled shape with `direction` 4.748 has corners at −88°, and 4.748 radians is the same angle). Mothbot Process writes degrees, and its two detection paths use different conventions: OpenCV's `minAreaRect` angle for `.pt` models and the detector's own angle for ONNX models. So the corners should be treated as the record, and `direction` only as a copy for X-AnyLabeling.

An angle brings its own questions: degrees or radians, which way is positive, and which side of the box is measured from 0°. Four corner points avoid those questions, which is why the proposal above uses them for the rotated box.

## Changes needed in the Mothbox tools

To do once the terms are settled; the Mothbox tools will be conformed to the ontology then, not before. None of these are done.

- Mothbot Classify: rename the “Accept” action to “Agree” (the A shortcut can stay).
- Mothbot Classify and Process: use “taxa list” in the interface, keeping “species list” only for GBIF species list downloads.
- Record `identifierType` and `identifierName` on every identification, with the taxa list DOI for machine identifications. Classify currently records people by initials only, so a full name or stable account would be needed.
- Rename `confidence_detection` and `confidence_ID` to detection score and identification score in new exports, and keep reading the old names.
- Write `deviceID`, `deviceType`, `sensorType`, `siteName`, `siteDescription` and the location coordinates as separate fields in exports.
- Store `col_taxon_key` (the current `taxonID` values) and, where it can be looked up, `gbif_taxon_key`.
- Mothbox firmware: say “capture window” instead of “session” for each scheduled stretch of photo-taking (settings file text and logs).
- Mothbot Process: write `direction` in X-AnyLabeling's convention (radians) on both detection paths, or derive it from the corners, so hand labels and detector output agree.

## Log

### 2026-11-03: More definitions

- **Capture window** is redefined as a continuous series of source file captures made while the attractor was running. Tying it to the attractor explains why Mothbox sessions have several windows (the attractor runs on a schedule) and AMI sessions usually one (the attractor runs all night).
- **Morphospecies:** a group of creatures sharing certain features, judged to be the same type of thing, usually made by a person when the exact designation is not known. Often a placeholder until the official species is found. Other ranks work the same way: morphogenus, morphofamily.
- **Non-target label:** a label applied to detections we are not interested in, commonly subcategorized as blur, frass, debris, plant material or error.
- **Creature, Attractor and Deployment** keep their earlier wording and are now decided.
- **Target** stays a draft; “stage” might be a better name.
- **Project vs dataset:** still being considered.

### 2026-11-03: Sessions, capture windows and boxes

- **Events nest.** Deployment, session, capture window and source file are all events, each inside the one above it, as Darwin Core allows with `parentEventID`.
- **Capture window** is the Mothbox name for a small continuous event inside a session. A Mothbox session (one night on the default schedule) usually has several capture windows; an Antenna session usually has just one, because AMI traps capture continuously through the night. Both describe the same structure, so the data stays compatible.
- **Boxes.** The Mothbox tools use X-AnyLabeling's format, and its word “shape”, because people hand-label data in X-AnyLabeling. The four corners define a rotated box completely, so the `direction` angle is redundant, and it is currently written in radians by X-AnyLabeling but in degrees by Mothbot Process. See [Ways to write a box](#ways-to-write-a-box).

### 2026-11-03: Follow-up answers

- **Height above ground** is part of Location.
- **Coordinates always belong to a Location**, whatever they describe. This closes the earlier question about which thing a project's single latitude and longitude describes.
- **Field-name style** (camelCase vs snake_case) will be raised with the Antenna developers at the next meeting.
- **No changes to the Mothbox tools yet.** All terms get settled first, then the tools are conformed to them.

### 2026-11-03: First decisions

Made by Andrew Quitmeyer (Mothbox tools, AIMO), after reviewing a side-by-side comparison of Mothbot and Antenna terms.

- **Device.** `deviceID` is the specific name of one unique device (e.g. SnappySloth) and `deviceType` is what kind of device it is (e.g. MothboxPro). The word “camera” is avoided for devices because future devices might not be camera based (lidar, radar or another sensor). A separate `sensorType` (e.g. `camera`) records what the device senses with. This matches Antenna's screen label “Device type” for the kind of hardware; Antenna has nothing yet for an individual device.
- **Detection.** Evidence from a source file of (ideally) one specific creature, created by a machine or a human. In Mothbot the word had also meant the per-photo results file; it now means only the evidence itself.
- **Identification.** One word for every claim about what a creature is, whoever made it. Each identification records the type of thing that made it (`machine` or `human`) and its specific name, e.g. a machine identification by BioCLIP 2.5 using a taxa list with a DOI, or a human identification by A. Quitmeyer. This was preferred over separate words such as “prediction” for machines and “identification” for people, because one term with attached values is easier to work with and more general. Antenna uses “classification” for machine answers; we prefer “identification” and want to choose one shared term with them. This entry replaces the earlier ontology term “Annotation”.
- **Taxa list and species list.** The Mothbox tools said “species list” because that is what GBIF calls the checklist downloads. Those lists do not have to hold species; they can be lists of orders, families or anything else. “Taxa list” is the general term, and a species list is one kind of taxa list.
- **Occurrence, track and cluster.** An occurrence is one unique individual creature in the world. A track is a series of detections of one specific occurrence linked across time. A cluster is a group of detections grouped by a common feature (for example visually), not necessarily the same occurrence. The earlier wording of Track (“detections showing the same taxa”) also described a cluster, so it now says “the same occurrence”.
- **Determination.** The answer a record currently carries. Taken from Antenna's usage.
- **Location and site.** A location is the actual GPS coordinates of where a thing is. A site is described by `siteName` (the name a human gives a specific place) and `siteDescription` (a brief optional description, e.g. creek near big tree, retired farmland). We do not use “station”, because it implies a static spot. That suits the AMI / Antenna groups, who rarely move their devices, but Mothbox devices move all the time. To ask Antenna: adopt “site”, use it interchangeably with “station” if they want, and keep coordinates in “location” instead of bundling them with the site or station. The earlier entry “Device Location” is now Location.
- **Score.** Use “score” instead of “confidence”, always with a qualifier: detection score or identification score.
- **Taxon keys.** Adopt `gbif_taxon_key` (as Antenna does) and add `col_taxon_key` for Catalogue of Life keys. To ask Antenna: support Catalogue of Life keys too, since newer GBIF species list downloads use them.
- **Agree.** Mothbot Classify's “Accept” becomes “Agree”, matching Antenna.

### 2026-11-02: Comparing Mothbot and Antenna terms

A side-by-side comparison of the words used by the Mothbox firmware, Mothbot Process and Classify, and Antenna (its screens and its code), mapped onto this ontology. Main findings:

- The same word meant different things in several places. “Session” was one scheduled photo window to the Mothbox firmware and a whole night to Antenna. “Device” was one physical trap to Mothbot and a kind of hardware to Antenna. “Detection” was a results file in Mothbot and one box in Antenna. Mothbot called any claim a “classification”, while Antenna split machine “classifications” from human “identifications”.
- Antenna often shows a different word on screen from the one in its code: Station for Deployment, Session for Event, Capture for SourceImage, Capture set for SourceImageCollection, Device type for Device.
- A Mothbot cluster usually holds many individuals, while an Antenna occurrence is one. Moving clusters into Antenna as occurrences would merge different animals into one record.
- Mothbot taxon IDs became Catalogue of Life keys in October 2026, while Antenna uses integer GBIF backbone keys, so the two could not be matched by key.
- Darwin Core and Camtrap DP already have names for several of these ideas (deployment, cameraID, cameraModel, individualID, classificationProbability), which helps when publishing data outside either system.
