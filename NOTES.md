# Naming notes

Rolling notes on how terms in this ontology were chosen: what was discussed, why each decision went the way it did, what is still open, and what we want to ask other groups. The glossary itself is in [README.md](README.md).

Add new entries at the top of the log, with a date. When a decision changes, add a new entry instead of editing the old one, so the history stays readable.

## Requests for the Antenna / AMI team

A living list. Status moves from “To ask” to “Asked” to the answer. The agenda for the 2026-11-19 meeting, with the current Antenna behaviour for each item, is in [meetings/2026-11-19-antenna.md](meetings/2026-11-19-antenna.md).

| Topic | What we are asking | Status |
|---|---|---|
| Identification vs classification | One word for both machine and human answers, told apart with `identifierType` and `identifierName`. | Decided 2026-11-19: the main term is **determination**, picked from identifications by a determination algorithm. Each claim is an identification; Antenna's machine `Classification` counts as a machine identification. To confirm: whether Antenna renames anything on screen. |
| Site and station | Adopt “site”, used interchangeably with “station” on screen if they prefer, and keep coordinates in a separate “location”. | Decided 2026-11-22: Antenna may keep “Station” on screen, but its data will follow the agreed site, location and deployment structure. |
| Device type and device ID | Record individual devices (`deviceID`) as well as device types. | Decided 2026-11-19: every device has its own ID; device types are user-definable, with three defaults (Standard Mothbox Pro, Standard Mothbox DIY, AMI Device). |
| Catalogue of Life keys | Store `col_taxon_key` beside `gbif_taxon_key`. | Decided 2026-11-19: both tools will support several key styles (GBIF, COL, BOLD, iNaturalist, Fieldguide), and each taxa list records its source (e.g. DOI) and key style. |
| Rotated boxes | Accept an optional rotated box on detections. | Decided 2026-11-19: Antenna will add oriented boxes ([issue #1421](https://github.com/RolnickLab/antenna/issues/1421)); every box carries a format label; new boxes are relative. The Mothbox format (decided 2026-11-22) is four relative corner points (`obb-corners-rel`). Antenna's “x1, y1, x2, y2 + rotation” means two corners of an upright rectangle, rotated around its centre (`xyxyr`); the tools convert between the two. |
| Field-name style | camelCase or snake_case. | Decided 2026-11-19: each language's own style in code (snake_case in Python); camelCase in exported files, following Darwin Core. |
| Where identifications attach | Allow a human identification on a single detection as well as on an occurrence. | Decided 2026-11-19: every detection belongs to an occurrence, and identifications and determinations attach to the occurrence. Mothbox occurrences usually hold one detection. |
| Taxa list source | Record a taxa list's source and DOI. | Decided 2026-11-19 (with the taxon keys decision). |
| Session gap for Mothbox nights | Antenna's 2-hour default gap splits a default Mothbox night in two. | Decided 2026-11-22: the 2-hour gap is only Antenna's default. Both tools will let people define and edit sessions, and keep sessions already defined in data they import. Mothbox data with default nightly sessions (noon to 11:59 the next morning) keeps them in Antenna. To ask: Antenna support for importing session definitions. |
| Non-target labels | A shared way to mark detections that are not creatures of interest. | Decided 2026-11-19: top-level **Non-Target** with a user-defined hierarchy below it, starting with Error and Abiotic. |

## Open questions

None at the moment.

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

Moved to [mothbox-conformance-plan.md](mothbox-conformance-plan.md), which covers every decided term. The tools are still not to be changed until that plan is agreed.

## Log

### 2026-11-22: Follow-up decisions

Made by Andrew after the Antenna meeting.

- **Target and stage** can be used interchangeably for now.
- **Project, not dataset.** A project is a collection of data that someone wants to process. “Dataset” is no longer a separate term; Mothbot Classify's “dataset” becomes “project”.
- **Field names in files.** Anything written to a file is camelCase: CSV, JSON and NDJSON, including the Mothbox tools' own dataset files. snake_case stays only inside Python code. camelCase is the most common style for JSON and matches Darwin Core and Camtrap DP.
- **Session files.** Sessions are written down explicitly, in one file per deployment next to the processed data. Mothbot Process creates it automatically with the default nightly sessions (noon to 11:59 the next morning), in `_processed/<deployment>/sessions.json`. This is what lets Antenna keep Mothbox sessions on import instead of regrouping them.
- **Box format.** Mothbox oriented boxes are four relative corner points (`obb-corners-rel`). X-AnyLabeling files stay as they are; their format gets its own label (`xanylabeling-rotation-px`), so it can be converted when needed.
- **Antenna's oriented box.** “x1, y1, x2, y2 + rotation” means two opposite corners of an upright rectangle, rotated around its centre. It gets the format label `xyxyr` and converts to and from four corners.
- **Names of people.** An identification can record a person by full name or by initials.
- **Frass** is plain Non-Target, or the user's own Non-Target › Frass subcategory. It is not built in.
- **Device types.** A device-type list (skeleton) is now in [device-types/](device-types/), with the three built-in types.
- **Station.** Antenna may keep “Station” on its screens; its data will follow the agreed site, location and deployment structure.
- **Sessions.** Antenna's 2-hour gap is only its default. Both tools will let people define and edit sessions, and keep sessions already defined in data they import. Mothbox's default nightly session runs from noon to 11:59 the next morning, and a Mothbox night imported into Antenna keeps that session, unless someone regroups it by hand.

### 2026-11-19: Decisions at the Antenna meeting

Made jointly with the Antenna / AMI team. Full notes per agenda item are in [meetings/2026-11-19-antenna.md](meetings/2026-11-19-antenna.md).

- **Determination is the main term.** The determination (det) is the flagged best guess of what an occurrence is, chosen from its identifications by a determination algorithm. The algorithm can be simple (latest identification wins) or complex (weighing scores). The Mothbox default: if there are human identifications, use the latest one; otherwise use the latest machine identification. Classify shows the determination and, in a detection's details, its history of identifications, from which a person can choose a different one.
- **Detection and occurrence.** A detection is the evidence of a creature in the sensor data at one moment. An occurrence is one individual creature. Every detection belongs to an occurrence, and identifications and determinations attach to the occurrence. Antenna leaves out small insects and tracks larger ones across captures, so its occurrences can hold many detections. Mothbox keeps even tiny creatures, where tracking is often impossible, so most Mothbox occurrences hold one detection; tracking can merge them later. Clusters stay separate: they group detections that look alike, which can be evidence toward a shared occurrence.
- **Events.** Deployment (user-definable; default: a device left at a site until a person retrieves it) › session (user-defined period of interest; Mothbox default one night, AMI has its own defaults) › capture window (continuous captures at a regular interval, usually with the attractor on) › capture (one instant of sensor data). Capture is new.
- **Devices.** Each device has its own ID (e.g. SnappySloth). Device types are user-definable and customizable, with three defaults: Standard Mothbox Pro, Standard Mothbox DIY and AMI Device (e.g. a Mothbox Pro with an external instead of an internal attractor). A deployment records the site (with metadata such as land-use type), the location (GPS, height above ground, facing direction) and the device (type, firmware version, one or more attractors with type, location and power level, target size and distance, sensor type and attributes, and user-defined fields).
- **Taxon keys.** Both tools will support several key styles (BOLD, iNaturalist, Fieldguide UUID, Catalogue of Life, GBIF). Each taxa list records its source (e.g. a DOI) and the style of its keys.
- **Field names.** Each language's own style in code (snake_case in Python); camelCase in exported CSVs and similar, following Darwin Core.
- **Boxes.** Antenna will add oriented bounding boxes ([issue #1421](https://github.com/RolnickLab/antenna/issues/1421); Antenna suggested x1, y1, x2, y2 plus a rotation, all floats). Every box carries a label naming its format. New boxes are relative to the image size, and Mothbox data already processed with pixel boxes stays readable. The Mothbox tools still need to choose one rotated format; today they mix X-AnyLabeling's and YOLO OBB's.
- **Non-Target.** Mothbot's catch-all “error” category becomes **Non-Target**: things we aren't interested in, too distorted to use, or produced by a detection error. Users can build their own hierarchy below it, with two built-in subcategories, Error (e.g. blur) and Abiotic (e.g. camera glare). They can go as specific as they want (e.g. Non-Target › Plantae) or stop at Non-Target.
- **Not discussed:** the word “Station” on Antenna's screens; Antenna's 2-hour default session gap.

### 2026-11-19: Preparing for the Antenna meeting

- Checked the Nov 2 comparison against Antenna's current `main` (2026-11-13). Its names have not changed: Station for Deployment, Session for Event, Capture for SourceImage, Device type for Device, and separate `Classification` / `Identification` models.
- New findings:
    - Antenna's human identifications attach only to occurrences.
    - Its taxa lists have no source or DOI.
    - Its taxa store `bold_taxon_bin` and `inat_taxon_id` but no Catalogue of Life key.
    - Its 2-hour session gap splits a default Mothbox night in two.
    - Its draft Darwin Core export writes `samplingProtocol` as fixed text.
- Both publishing standards use one word for human and machine answers, with a field for which made it: Darwin Core says identification (`identifiedBy`), Camtrap DP says classification (`classificationMethod`: `human` / `machine`). This supports one shared term; the open choice is which word.
- Added a [crosswalk](README.md#crosswalk) to the README, mapping each term onto the Mothbox tools, Antenna (screen and code), Darwin Core and Camtrap DP.
- Wrote the meeting agenda: [meetings/2026-11-19-antenna.md](meetings/2026-11-19-antenna.md). No terms were decided today.

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
