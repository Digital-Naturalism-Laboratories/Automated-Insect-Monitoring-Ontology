# Automated-Insect-Monitoring-Ontology
Working towards a data standard or data schema for devices that try to image arthropods automatically in nature by creating a shared vocabulary.


The reasoning behind each decision, the questions still open, and what we want to ask other groups (such as the Antenna / AMI team) are kept in [NOTES.md](NOTES.md). Agendas and outcomes of meetings with other groups are in [meetings/](meetings/). The plan for bringing the Mothbox tools in line with these terms is in [mothbox-conformance-plan.md](mothbox-conformance-plan.md).

## How to read this glossary

Each term has a **Status**:

- **Decided with Antenna**: agreed jointly with the Antenna / AMI team (the date says which meeting).
- **Decided**: agreed for this ontology; not yet discussed with Antenna, or not affecting them.
- **Decided, pending Antenna**: agreed here; to be put to the Antenna / AMI team, who may adopt it or suggest a change.
- **Draft**: wording that has not been reviewed yet.
- **Open**: still under discussion (see [NOTES.md](NOTES.md)).

**Also called** lists the names other tools use for the same thing, so data can be translated between them.

## Contents

- [How the pieces fit together](#how-the-pieces-fit-together)
- [Projects](#projects): Project
- [Creatures and records](#creatures-and-records): Creature, Occurrence, Track, Cluster
- [Evidence and identifications](#evidence-and-identifications): Source File, Detection, Identification, Agree, Determination, Determination Algorithm, Score, Non-Target
- [Taxonomy](#taxonomy): Taxa List, Species List, Morphospecies, Taxon Keys
- [Events](#events): Deployment, Session, Capture Window, Capture
- [Places](#places): Site, Location
- [Hardware](#hardware): Device, Device Type, Attractor, Target (Stage), Sensor
- [Methods](#methods): Protocol
- [Conventions](#conventions): Field Names, Box Formats
- [Terms without definition (yet)](#terms-without-definition-yet)
- [Crosswalk](#crosswalk): the same terms in the Mothbox tools, Antenna, Darwin Core and Camtrap DP

## How the pieces fit together

**Events** nest, each inside the one above it:

```
Deployment                 a device left at a site until a person retrieves it
 └─ Session                a period someone wants to study (default: one night)
     └─ Capture Window     continuous captures at a regular interval
         └─ Capture        one instant of sensor data → one or more source files
```

**A deployment** also records where it was and what was deployed. Users can add their own fields at any level.

```
Deployment
 ├─ Site                   a named place (site description, land-use type, ...)
 │   └─ Location           GPS, height above ground, facing direction
 └─ Device                 one physical machine (deviceID, e.g. SnappySloth)
     ├─ Device Type        e.g. Standard Mothbox Pro, customizable
     ├─ Firmware version
     ├─ Attractors         one or more, each with type, location and power level
     ├─ Target             size, distance from the sensor
     ├─ Sensor             type (camera, infrared, lidar) and attributes (resolution)
     └─ { fields people define for their own devices }
```

**Evidence** builds up from sensor data to an answer:

```
Source File  →  Detection  →  Occurrence  ←  Identifications (by machines and people)
                                   ↑
                             Determination (chosen from the identifications
                                            by a determination algorithm)
```

## Glossary of terms

### Projects

#### Project
- **Status:** Decided
- **Definition:** A collection of data that someone wants to process.
- **Explanation:** A project is the top-level container: it holds one or more [deployments](#deployment) and everything made from their data. We use “project” rather than “dataset”.
- **Example:** all the Mothbox deployments from the 2026 Panama survey, processed and identified together
- **Also called:** Project (Antenna); dataset, dataset package (Mothbot Classify; its folder holds a `dataset.json`); `datasetID`, `datasetName` (Darwin Core)

### Creatures and records

#### Creature
- **Status:** Decided
- **Definition:** Abstract term for a living thing that is of interest for this work.
- **Explanation:** Could be an insect, an arthropod, or another small animal.
- **Example:** gecko, beetle, bat

#### Occurrence
- **Status:** Decided with Antenna (2026-11-19)
- **Definition:** One particular individual creature.
- **Explanation:** Every detection belongs to one occurrence, and an occurrence has one or more detections. Identifications and determinations attach to the occurrence.
    - **Antenna** tends to leave out small insects and tracks the larger ones as individuals across many captures, so one occurrence can hold many detections.
    - **Mothbox** data usually includes even the smallest creatures. On photos with thousands of tiny, similar-looking creatures, tracking can be impossible or meaningless, so most Mothbox occurrences hold a single detection. Tracking can later merge several of them into one larger occurrence.
- **Example:** Sam the beetle, seen in 14 captures as it walks across the target
- **Also called:** Occurrence (Antenna, Darwin Core); `organismID` (Darwin Core); `individualID` (Camtrap DP)

#### Track
- **Status:** Decided
- **Definition:** A series of detections of one specific occurrence, linked across time.
- **Explanation:** Every detection in a track shows the same individual, not only the same kind of creature. An occurrence with more than one detection is followed through them by its track. Detections that only look alike form a [Cluster](#cluster).
- **Example:** a beetle walking over a screen, a bumble bee visiting close by flowers
- **Attributes:**
    - duration
- **Also called:** sequence (AMI Data Companion app); temporal sub-cluster (older Mothbot data)

#### Cluster
- **Status:** Decided
- **Definition:** A group of detections grouped by a common feature, such as how they look.
- **Explanation:** The detections in a cluster are not necessarily the same occurrence. A cluster often holds many individuals of one kind of creature seen over a night. Visual clusters look for detections that are very similar, so a cluster can be evidence that some detections might be the same occurrence, but it is not an occurrence itself.
- **Example:** all the detections of small brown moths that a visual-similarity model puts together
- **Attributes:**
    - the feature or method used to group them (e.g. DINOv2 visual similarity)

### Evidence and identifications

#### Source File
- **Status:** Draft
- **Definition:** A media file that can have different types of backgrounds and may contain one or more target species.
- **Explanation:** any computer readable file format generated by the machine that might contain unprocessed detections. Each source file comes from a [Capture](#capture).
- **Example:** photograph, video, or audio track (or combined).
- **Assumptions:**
	- Static device.
- **Also called:** Capture (Antenna screens, which use one word for the moment and the file); `SourceImage` (Antenna code); source image, raw photo (Mothbot)

#### Detection
- **Status:** Decided with Antenna (2026-11-19)
- **Definition:** The evidence of a creature in the sensor data at one particular moment.
- **Explanation:** A detection can be created by a machine (a detection model) or by a human (for example by drawing a box). It is usually a region of a source file, such as a box in a photo or a stretch of time in an audio file, together with its cropped image or clip. Each detection belongs to one [Occurrence](#occurrence).
- **Example:** a box around a moth in a photo, and the cropped image of that moth
- **Attributes:**
	- Date and time stamp
	- Source file name
	- the box, with a label saying what format it is in (see [Box Formats](#box-formats)), or start timestamp + length
	- `creatorType`: `machine` or `human`
	- `creatorName`: the specific model or person that made the detection (e.g. `Mothbot Detect 1.2`, `A. Quitmeyer`)
	- detection score, when a machine made it (see [Score](#score))
	- the occurrence it belongs to
- **Also called:** Detection (Antenna); patch, shape, bot detection, human detection (Mothbot)

#### Identification
- **Status:** Decided with Antenna (2026-11-19)
- **Definition:** One claim, by a machine or a person, about what taxon an occurrence is.
- **Explanation:** An occurrence can collect many identifications, from different machines and people at different times. Each one is kept as evidence, and none of them is the answer on its own: the answer is the [Determination](#determination). Each identification records what kind of thing made it and exactly who or what that was. Identifications can be used in training data sets or while and after validating AI results. This entry replaces the earlier term “Annotation”.
- **Example:** a machine identification of *Apis* sp. made by BioCLIP 2.5 using a taxa list with DOI 10.15468/dl.4j8kfb; a human identification of *Apis mellifera* made by A. Quitmeyer
- **Attributes:**
    - taxon: name and rank, with taxon keys when known (see [Taxon Keys](#taxon-keys))
    - `identifierType`: `machine` or `human`
    - `identifierName`: the specific model or person (e.g. `BioCLIP 2.5`, `A. Quitmeyer`); a person can be recorded by full name or by initials
    - the detection it was made from, when it was made from one
    - taxa list used, with its DOI (see [Taxa List](#taxa-list)); this is the reference catalogue that avoids synonyms
    - identification score, when a machine made it (see [Score](#score))
    - date and time it was made
- **Also called:** Classification or Machine prediction (Antenna, for machine identifications); Identification (Antenna, for human identifications); classification (Mothbot Classify)

#### Agree
- **Status:** Decided
- **Definition:** An identification that endorses an existing identification.
- **Explanation:** When a reviewer confirms a machine's or another person's answer, the agreement is recorded as a new identification that points to the one it agrees with, so the record shows who checked what.
- **Example:** A. Quitmeyer agrees with BioCLIP 2.5's identification of a detection as Noctuidae.
- **Also called:** Agree (Antenna); Accept (older Mothbot Classify)

#### Determination
- **Status:** Decided with Antenna (2026-11-19)
- **Definition:** The flagged best guess of what an occurrence is, chosen from its identifications.
- **Short form:** det
- **Explanation:** This is the main answer a record carries, and what the Mothbox tools and Antenna show and export. An occurrence can have many identifications. A [Determination Algorithm](#determination-algorithm) picks one of them as the determination, and it is picked again when new identifications arrive. The other identifications stay in the record as its history, so people can see how the answer changed, and can choose a different one from the history if they disagree.
- **Example:** an occurrence with a BioCLIP identification of Erebidae and a later human identification of *Hypena scabra* has the determination *Hypena scabra*.
- **Attributes:**
    - taxon (as in the chosen identification)
    - the identification it was taken from
    - the determination algorithm that chose it, with its version
    - date and time it was made
- **Also called:** Determination (Antenna, `Occurrence.determination`); current classification (Mothbot Classify)

#### Determination Algorithm
- **Status:** Decided with Antenna (2026-11-19)
- **Definition:** The rule that picks an occurrence's determination from its identifications.
- **Explanation:** It can be very simple, such as always taking the latest identification, or more complex, such as weighing identification scores or how many people agree. Each determination records which algorithm made it, so data from tools with different rules can still be compared.
- **Example:** The Mothbox default rule:
    1. If the occurrence has any human identifications, use the latest human identification.
    2. Otherwise, use the latest machine identification.

#### Score
- **Status:** Decided
- **Definition:** A number from 0 to 1 that a machine gives for how sure it is.
- **Explanation:** Always say what the score is about: a **detection score** (how sure a model is that a detection holds a creature) or an **identification score** (how sure it is of a taxon). Use “score” rather than “confidence”.
- **Example:** detection score 0.91; identification score 0.62
- **Also called:** confidence (older Mothbot data: `confidence_detection`, `confidence_ID`); score (Antenna)

#### Non-Target
- **Status:** Decided with Antenna (2026-11-19)
- **Definition:** The top-level category for detections we aren't interested in, that are too distorted to use, or that come from an error in detection.
- **Explanation:** Labelling a detection Non-Target leaves it out of counts and identifications without deleting it. Below Non-Target, users can build their own hierarchy, as specific as they like. Two subcategories come built in:
    - **Error:** something went wrong, such as a blurry image or a box around nothing.
    - **Abiotic:** a non-living thing mistaken for a creature, such as camera glare, a raindrop or dust.

    A user can stop at Non-Target, use a built-in subcategory, or add their own, such as Non-Target › Plantae for plants, or Non-Target › Error › Blur.
- **Example:** a blurry photo labelled Non-Target › Error; camera glare labelled Non-Target › Abiotic; a leaf labelled just Non-Target, or Non-Target › Plantae; insect droppings labelled just Non-Target, or Non-Target › Frass
- **Attributes:**
    - its path in the hierarchy (e.g. Non-Target › Error › Blur)
- **Also called:** Non-target label (earlier in this ontology); error label (Mothbot Classify: `ERROR`, `ERROR_Blur`, `ERROR_Frass`); non-moth (Antenna's moth / non-moth classifier)

### Taxonomy

#### Taxa List
- **Status:** Decided with Antenna (2026-11-19)
- **Definition:** A list of taxa that limits or describes which identifications are possible.
- **Explanation:** A taxa list can hold taxa of any rank: species, families, orders, or a mix. It is used to restrict what a model can answer and to record which reference list an identification was made against. Every taxa list says where it came from and which style of taxon key it uses, because a key can't be read without knowing its style.
- **Example:** the insects of Panama and Costa Rica downloaded from GBIF; a list of the moth families expected at a site
- **Attributes:**
    - source, with its DOI when there is one (e.g. a GBIF download)
    - key style: which kind of [taxon key](#taxon-keys) its entries carry (e.g. `col`, `gbif`)
    - date created
- **Also called:** Taxa list (Antenna); species list (older Mothbot)

#### Species List
- **Status:** Decided
- **Definition:** A taxa list whose entries are species.
- **Explanation:** GBIF calls its checklist downloads “species lists”, which is where the Mothbox tools got the name. Use [Taxa List](#taxa-list) as the general term.
- **Example:** a GBIF species list download for Insecta in Panama

#### Morphospecies
- **Status:** Decided
- **Definition:** A group of creatures sharing certain features, judged to be the same type of thing.
- **Explanation:** Usually made by a person organizing creatures whose exact designations are not known, but which seem to be the same sort of thing. It is often a placeholder until the official species can be found. The same idea works at other ranks, such as a morphogenus or a morphofamily.
- **Example:** “brown moth with white kidney spot A”, used for every detection of that kind until it is identified to species
- **Attributes:**
    - rank it stands in for (morphospecies, morphogenus, morphofamily, ...)
- **Also called:** morphospecies (Mothbot Classify); unknown species (an unmerged Antenna branch)

#### Taxon Keys
- **Status:** Decided with Antenna (2026-11-19)
- **Definition:** Identifiers that tie a taxon name to an entry in a published checklist or reference database.
- **Explanation:** Both the Mothbox tools and Antenna will support several key styles. Each key is stored with its style, because a key from one source can't be looked up in another. Always send the taxon name and rank as well.
- **Key styles:**
    - `gbif`: GBIF Backbone Taxonomy key (a whole number)
    - `col`: Catalogue of Life key (letters and digits, e.g. `B6L67`), which newer GBIF species list downloads use
    - `bold`: BOLD BIN (e.g. `BOLD:AAA1234`)
    - `inat`: iNaturalist taxon ID
    - `fieldguide`: Fieldguide UUID
- **Attributes:**
    - the key
    - its style (one of the above)
- **Also called:** `gbif_taxon_key`, `bold_taxon_bin`, `inat_taxon_id`, `fieldguide_id` (Antenna); `taxonID` with `taxonIDSource` (Mothbot Classify; Catalogue of Life keys since October 2026); `taxonID` (Darwin Core)

### Events

Events nest: deployment, session, capture window, capture. Darwin Core links nested events with `parentEventID`. See [What “event” means elsewhere](NOTES.md#what-event-means-elsewhere).

#### Deployment
- **Status:** Decided with Antenna (2026-11-19)
- **Definition:** The top-level event, which users can define for themselves.
- **Explanation:** By default, a deployment is a device left at a specific site to operate until a person retrieves it. That can be a couple of hours, or weeks, or years. It holds one or more [sessions](#session), and records the [site](#site), [location](#location) and [device](#device) (see [How the pieces fit together](#how-the-pieces-fit-together)).
- **Example:** SnappySloth left at Les Beach Palm from 2026-07-27 to 2026-08-10
- **Also called:** Deployment (Antenna code, Camtrap DP); Station (Antenna screens)

#### Session
- **Status:** Decided with Antenna (2026-11-19)
- **Definition:** A user-defined event inside a deployment: a period of time someone is interested in studying.
- **Explanation:** For Mothbox devices it defaults to one night, from noon to 11:59 the next morning. Antenna's AMI devices have their own default sessions (Antenna starts a new session after a gap of more than 2 hours, by default). A session holds one or more [capture windows](#capture-window).

    Both the Mothbox tools and Antenna let people define and edit sessions. A tool that receives data with sessions already defined keeps them as they are: for example, Mothbox data with the default nightly sessions keeps those sessions when imported into Antenna, instead of being regrouped by Antenna's gap rule. People can still regroup sessions by hand afterwards.
- **Example:** one night (noon to 11:59 the next morning); one afternoon; only dusk
- **Attributes:**
    - start and end time
    - how it was defined (a default rule such as `nightly-noon-to-noon`, or by hand)
- **Also called:** Session (Antenna screens); `Event` (Antenna code, roughly one night); night (Mothbot); Event (Darwin Core)

#### Capture Window
- **Status:** Decided with Antenna (2026-11-19)
- **Definition:** An event inside a session in which source files are captured continuously at a regular interval.
- **Explanation:** The attractor, if there is one, is usually on during a capture window. A Mothbox session usually has several capture windows, because the device runs on a schedule (by default five stretches of 59 minutes a night). An AMI session usually has one, because AMI traps run all night.
- **Example:** photos taken every minute from 19:00 to 19:59
- **Attributes:**
    - start and end time
    - capture interval (time between captures)
- **Also called:** session (older Mothbox firmware settings)

#### Capture
- **Status:** Decided with Antenna (2026-11-19)
- **Definition:** The lowest-level event: one instant in which the sensor records data of the target.
- **Explanation:** A capture produces one or more [source files](#source-file), such as a photo, or a photo plus its sensor readings.
- **Example:** the photo taken at 19:42:00
- **Attributes:**
    - date and time
- **Also called:** Capture (Antenna screens, also used for the file itself)

### Places

#### Site
- **Status:** Decided with Antenna (2026-11-19, 2026-11-22)
- **Definition:** A place that a human has given a name, where one or more devices are deployed.
- **Explanation:** A site is identified by its name and an optional description, not by coordinates (those are the [Location](#location)). Users can add further metadata, such as land-use type. Automated Insect Monitoring Symposium participants indicated a site is likely a zone 10–100 meters wide. We do not use “station”, because it suggests a fixed spot and Mothbox devices move often. Antenna may keep “Station” on its screens, but its data will follow this site, location and deployment structure, so the two stay compatible.
- **Example:** `siteName`: Les Beach Palm; `siteDescription`: creek near the big tree
- **Attributes:**
    - `siteName`: the name a human gives to a specific place
    - `siteDescription`: a brief optional description (e.g. creek near big tree, retired farmland)
    - land-use type
    - Canopy height
    - Habitat type
- **Also called:** Site (Antenna); Station (Antenna screens, for a deployment)

#### Location
- **Status:** Decided with Antenna (2026-11-19)
- **Definition:** The actual GPS coordinates of where a thing is, and how it sits there.
- **Explanation:** A location is kept separate from any name for the place, because Mothbox devices move often and the same named site can have devices at several exact spots.
- **Example:** 5.094, -80.34, 1.5 m above ground, facing north-east
- **Attributes:**
    - latitude and longitude (GPS)
    - coordinate uncertainty, if known
    - height above ground
    - facing direction
- **Also called:** Station latitude and longitude (Antenna); latitude and longitude on the Mothbox field sheet. Replaces the earlier entry “Device Location”.

### Hardware

#### Device
- **Status:** Decided with Antenna (2026-11-19)
- **Definition:** One physical machine that performs some kind of automated observation task.
- **Explanation:** Every device has its own ID, so one unit can be followed across deployments. We avoid the word “camera” for devices, because future devices may sense in other ways (lidar, radar or other sensors).
- **Example:** SnappySloth, a Standard Mothbox Pro
- **Attributes:**
	- `deviceID`: the specific name of one unique device (e.g. `SnappySloth`)
	- [Device Type](#device-type)
	- firmware version
	- [attractors](#attractor): one or more, used at the same time
	- [target](#target) size and distance from the sensor
	- [sensor](#sensor) type and attributes
	- any fields people define for their own devices
- **Also called:** Device type (Antenna, for the kind of hardware; Antenna has no record of individual devices yet)

#### Device Type
- **Status:** Decided with Antenna (2026-11-19)
- **Definition:** A named kind of device, with a set of standard features.
- **Explanation:** There are three built-in device types, listed with their features in [device-types/](device-types/). Users can define their own, or customize a built-in one, for example a Mothbox Pro with an external attractor instead of its internal one. A device's own record can override any of its type's features.
- **Example:**
    - Standard Mothbox Pro
    - Standard Mothbox DIY
    - AMI Device
- **Attributes:**
    - `deviceType`: its name
    - its default features (attractors, target, sensor, ...)
    - the device type it was customized from, if any
- **Also called:** Device type (Antenna screens); `Device` (“Device Configuration”, Antenna code); `cameraModel` (Camtrap DP)

#### Attractor
- **Status:** Decided with Antenna (2026-11-19)
- **Definition:** specific stimulus used to lure creatures.
- **Explanation:** This might not be visible/ audible in the Source files. A device can have several attractors working at the same time.
- **Example:** chemical (smell), visual (UV, false flowers), or auditory (mating call).
- **Attributes:**
    - attractor type (e.g. the light type)
    - attractor location (where it sits on or around the device)
    - power level
- **Also called:** `attractor`, `attractor1`–`attractor3` (Mothbox field sheet); `baitUse` (Camtrap DP)

#### Target
- **Status:** Decided
- **Also called:** Stage. “Target” and “stage” can be used interchangeably for now.
- **Definition:** The part of a device being directly observed where insects are intended to go for observation.
- **Explanation:**
- **Example:** a target sheet, a tube, or an artificial flower.
- **Attributes:**
    - size
    - distance from the sensor

#### Sensor
- **Status:** Decided with Antenna (2026-11-19)
- **Definition:** The part of a device that records data.
- **Example:** a 64 MP camera
- **Attributes:**
    - `sensorType`: e.g. `camera`, `infrared`, `lidar`
    - sensor attributes, such as resolution, lens, effective resolution (px/mm), sensitivity range (IR, RGB, UV, infrasonic, ultrasonic)
    - orientation (vertical vs horizontal)

### Methods

#### Protocol
- **Status:** Draft
- **Definition:** The method in which a task was carried out.
- **Explanation:** The description needs to include all necessary information to deploy the device in the same maner for a follow up survey.
- **Example:** checklist, bullet points, might include photodocumentary. Can be applied to a deployment, session, capture, or detection.

### Conventions

#### Field Names
- **Status:** Decided with Antenna (2026-11-19)
- **Rule:** Use the style that is normal where the name is written.
    - **In code:** use that language's style, e.g. snake_case in Python (`device_id`, `gbif_taxon_key`) and camelCase in TypeScript.
    - **In files:** anything written to a file uses camelCase: CSV exports, JSON and NDJSON, including the tools' own dataset files. This matches Darwin Core and Camtrap DP (`deviceID`, `siteName`, `parentEventID`), and is the most common style for JSON.
- **Explanation:** The same field can be `device_id` inside Python code and `deviceID` in a file. The glossary gives the file (camelCase) form. Tools keep reading files written with older snake_case names.

#### Box Formats
- **Status:** Decided with Antenna (2026-11-19); Mothbox format decided 2026-11-22
- **Rules:**
    - Every box is stored with a label saying what format it is in, so readers never have to guess.
    - New boxes use **relative** coordinates: fractions (0–1) of the source file's width and height, measured from the top-left corner.
    - Pixel boxes from data already processed by the Mothbox tools stay readable.
    - Boxes can be **oriented** (rotated). Antenna will add support for them; see [Antenna issue #1421](https://github.com/RolnickLab/antenna/issues/1421).
- **Mothbox format:** oriented boxes are written as **four relative corner points**, `x1, y1, x2, y2, x3, y3, x4, y4`, listed in order around the box. Each value is a fraction (0–1) of the image's width or height, after the image's EXIF orientation is applied. There is no angle, so there are no questions about units or direction. The upright box is the minimum and maximum of the corners. This is also how Ultralytics writes OBB training labels.
- **Format labels:**

    | Label | Meaning |
    |---|---|
    | `obb-corners-rel` | four relative corner points (the Mothbox format) |
    | `xyxy-rel` | upright box: top-left and bottom-right corners, relative |
    | `xyxy-px` | upright box: top-left and bottom-right corners, in pixels (Antenna today) |
    | `xyxyr` | Antenna's proposed oriented box: two opposite corners of an upright rectangle, plus a rotation of that rectangle around its centre |
    | `xanylabeling-rotation-px` | X-AnyLabeling rotation shape: four corners in pixels, plus a `direction` angle. Kept as is in X-AnyLabeling files for hand-labelling, and converted to `obb-corners-rel` when needed |

    A Mothbox box with no label is read as `xanylabeling-rotation-px`.
- **Explanation:** Relative boxes stay correct when an image is resized or shown at a different size, and can be compared between images of different resolutions.
- **Also called:** shape, `points` (Mothbot, X-AnyLabeling); `bbox` (Antenna)

### Terms without definition (yet)
These might help to describe or distinguish things:
- appearance
- localisation
- record
- capture set: a chosen subset of source files (Antenna's “Capture set”)
- algorithm and pipeline: one model, and a chain of models (Antenna)

## Crosswalk

How each term maps onto the names used by the Mothbox tools and Antenna, and onto the fields of the two publishing standards. "—" means there is no equivalent. Antenna often shows a different word on screen from the one in its code, so both are listed. Antenna's names were checked against its `main` branch on 2026-11-19.

| This ontology | Mothbox tools | Antenna (screen) | Antenna (code) | Darwin Core | Camtrap DP |
|---|---|---|---|---|---|
| Creature | creature | — | — | — | — |
| Occurrence | — | Occurrence | `Occurrence` | `occurrenceID`, `organismID` | `individualID` |
| Track | temporal sub-cluster (older data) | — | sequence (AMI Data Companion) | — | — |
| Cluster | cluster | — | — | — | — |
| Source File | source image, raw photo | Capture | `SourceImage` | Audubon Core media record | media (`mediaID`, `filePath`) |
| Detection | patch, shape, bot / human detection | Detection | `Detection` (`bbox`) | Audubon Core region of interest | observation with `bboxX`, `bboxY`, `bboxWidth`, `bboxHeight` |
| Identification | classification | Machine prediction / Identification | `Classification` / `Identification` | `identifiedBy`, `dateIdentified` | `classificationMethod`, `classifiedBy`, `classificationTimestamp` |
| `identifierType` | `classifier_type` (`bot` / `human`) | — | which model holds it | — | `classificationMethod` (`human` / `machine`) |
| Agree | Accept | Agree | `agreed_with_identification`, `agreed_with_prediction` | — | — |
| Determination | current classification | Determination | `Occurrence.determination` | `scientificName`, `taxonRank` on the occurrence | `scientificName` |
| Determination Algorithm | classification resolver | — | — | — | — |
| Score | `confidence_detection`, `confidence_ID` | Score | `score`, `determination_score` | — | `classificationProbability` |
| Non-Target | error label (`ERROR_Blur`, …) | non-moth | moth / non-moth classifier, `Tag` | — | `observationType` (`blank`, `unknown`, `unclassified`) |
| Taxa List | species list | Taxa list | `TaxaList` | — | `taxonomic` (package metadata) |
| Morphospecies | morphospecies | — | unknown species (unmerged branch) | `verbatimIdentification` (partly) | — |
| Taxon Keys | `taxonID` + `taxonIDSource` | — | `gbif_taxon_key`, `bold_taxon_bin`, `inat_taxon_id`, `fieldguide_id` | `taxonID` | `taxonID` |
| Deployment | deployment | Station | `Deployment` | parent event (`parentEventID`) | deployment (`deploymentID`, `deploymentStart`, `deploymentEnd`) |
| Session | night | Session | `Event` | event (`eventID`, `eventDate`) | — |
| Capture Window | session (firmware settings) | — | — | child event (`parentEventID`) | `captureMethod` (`timeLapse`) |
| Capture | photo timestamp | Capture | `SourceImage.timestamp` | child event | media `timestamp` |
| Site | site | Site | `Site` ("Research Site") | `locationID`, `locality` | `locationID`, `locationName` |
| Location | latitude / longitude (field sheet) | Station latitude / longitude | `Deployment.latitude`, `.longitude` | `decimalLatitude`, `decimalLongitude`, `coordinateUncertaintyInMeters` | `latitude`, `longitude`, `coordinateUncertainty` |
| Location: height above ground | `height_above_ground`, `ground_height` | — | — | `minimumDistanceAboveSurfaceInMeters` | `cameraHeight` |
| Location: facing direction | — | — | — | — | `cameraHeading` |
| Device (`deviceID`) | `device` (field sheet), `mothbox` (CSV export), `device_id` (package) | — | — | — | `cameraID` |
| Device Type | — (not recorded yet) | Device type | `Device` ("Device Configuration") | — | `cameraModel` |
| Attractor | `attractor`, `attractor1`–`3`, `attractor_location` | — | — | — | `baitUse` |
| Target (Stage) | `sheet` (field sheet) | — | — | — | — |
| Protocol | — | — | fixed text in the draft export | `samplingProtocol`, `samplingEffort` | — |
| Project | dataset, dataset package | Project | `Project` | `datasetID`, `datasetName` | package |
