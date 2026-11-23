# Bringing the Mothbox tools in line with the ontology

A plan for changing Mothbot Process, Mothbot Classify and the Mothbox firmware to match the terms decided in the [README](README.md), mostly at the [2026-11-19 Antenna meeting](meetings/2026-11-19-antenna.md).

**Status:** first draft, 2026-11-22; decisions D1–D6 all made the same day. Nothing has been changed in the tools yet. The rule from 2026-11-03 still holds: settle the terms first, then change the tools.

File references are to the repos as of 2026-11-22: Classify `main` at `7ad9eb1`, Process at `0ce9611`.

## Ground rules for every phase

- **Read old, write new.** Every tool keeps reading the old names, labels and box formats. Only new writes use the new forms. Packages people have already identified must open unchanged.
- **Never lose human identifications.** No phase may require resetting a dataset. Migrations add records; they don't rewrite or delete the files in `03_classifications/`.
- **Version the package.** Bump the `format` version in `dataset.json` when a phase changes what is written, so an older Classify can say "this package needs a newer version" instead of misreading it.
- **Measure at scale.** Several changes add records per detection. Check them on the largest nights with Classify's `scripts/chrome-harness`, not only with unit tests.

## Decisions needed before starting

| # | Question | Decision | Needed for |
|---|---|---|---|
| D1 | Which rotated box format do the Mothbox tools use? | **Decided 2026-11-22:** four relative corner points (`obb-corners-rel`) | Phase 6 |
| D2 | Do X-AnyLabeling files stay in pixels? | **Decided 2026-11-22:** yes, kept as they are, with their own format label (`xanylabeling-rotation-px`) so they can be converted when needed | Phase 6 |
| D3 | Do package files count as files that must be camelCase? Package files are what Classify writes inside a dataset folder: `dataset.json`, `02_records/*.ndjson` (patches, sources, deployments, nights) and `03_classifications/*.ndjson` (one file of identifications per person or model). Their fields are snake_case today (`patch_id`, `classifier_type`). | **Decided 2026-11-22:** yes. Anything written to a file is camelCase; snake_case stays only inside Python code. New package versions write camelCase and still read snake_case | Phase 7 |
| D4 | How should a person be named in `identifierName`? | **Decided 2026-11-22:** full name or initials, as the person prefers. Today Classify records initials only (`human-classifier-id.ts`) | Phase 1 |
| D5 | Where does frass go in the Non-Target hierarchy? | **Decided 2026-11-22:** plain Non-Target, or a user's own Non-Target › Frass subcategory; not built in | Phase 2 |
| D6 | Where does the list of default device types live? | **Decided 2026-11-22:** [device-types/device-types.json](device-types/device-types.json) in this repo (skeleton), copied into Process, Classify and the firmware | Phase 5 |

## Recommended order

1. [Identifications, determination and history](#1-identifications-determination-and-history) (Classify, small Process change). This is the core of the new model and has the most user value.
2. [Non-Target](#2-non-target) (Classify).
3. [Occurrences](#3-occurrences) (Classify, Process). Small, and it unblocks Antenna import.
4. [Taxon keys and taxa lists](#4-taxon-keys-and-taxa-lists) (Classify, Process).
5. [Deployments, devices and events](#5-deployments-devices-and-events) (Process field sheet, package, firmware).
6. [Boxes](#6-boxes) (Process, Classify).
7. [Export field names](#7-export-field-names) (Process, Classify), last, so downstream spreadsheets break only once.

The words on screen ([section 8](#8-words-on-screen)) change along with the phase that touches them.

---

## 1. Identifications, determination and history

**Ontology:** [Identification](README.md#identification), [Determination](README.md#determination), [Determination Algorithm](README.md#determination-algorithm), [Agree](README.md#agree).

**Today (Classify):**
- Each classifier has one file in `03_classifications/` (`_bot.ndjson`, `{initials}.ndjson`), holding **one row per patch**. Saving overwrites that classifier's earlier row for the patch (`mothbox-next/persist/merge-classifier-rows.ts`). So when a person changes their mind, their earlier answer is lost. History survives only across different classifiers.
- The current answer is picked by `mothbox-next/resolve-classifications.ts`: the latest `classified_at` wins, and human beats machine only on a tie or when both timestamps are missing (`resolver-spec.md`). **This differs from the new rule.** A machine identification with a later timestamp than a human one would win today. Under the new rule, any human identification wins.
- Some converted machine rows are stamped with the time they were loaded (`bot-shape-to-classification.ts`, `classified_at: classifiedAt ?? Date.now()`). Under the current rule, such a row could beat older human rows.
- "Accept" is a `classification_type` value, not a pointer to the identification being agreed with.

**Changes:**
1. **Keep every identification.** Append a new row on each save instead of replacing the classifier's row, and give each row an `identification_id`. The "latest per classifier" view becomes derived.
2. **Determination algorithm `mothbox-default/1`:** if there are human identifications, take the latest; otherwise take the latest machine identification. Withdrawn identifications are skipped. This replaces `resolveCurrentClassifications`. Record the algorithm name and the chosen `identification_id` with each determination. `02_records/current-classifications.ndjson` stays a rebuildable cache, renamed or aliased to determinations.
3. **Agree** is an identification by a person with `agreed_with` pointing at the identification it endorses. It copies that identification's taxon. Old `accept` rows keep loading as agreements with the machine row for the same patch.
4. **History in the detail view.** The detail panel opened by double-clicking a patch (`patch-grid/patch-item.tsx`, `onOpenDetail`) lists every identification: who or what made it, when, which taxa list, and its score. The determination is marked.
5. **Choosing an older identification.** This doesn't need a special override: picking one from the history records an Agree by the current person pointing at it. Since that is now the latest human identification, the default algorithm selects it, and the record shows who chose it.
6. **`identifierType` and `identifierName`** on every row. Map `classifier_type` `bot` → `machine` on read. For people, Classify asks once for a name; full name or initials are both fine (D4). For machines, record the model name and version, which Process already partly writes (`identifier_bot`, `timestamp_ID_bot`).
7. **Process** (`pipeline/identify.py`): write each machine identification with model name and version, taxa list DOI, identification score and timestamp. A re-run adds a new identification instead of overwriting the old one.

**Watch out:** append-only rows grow with every edit. Measure package load time on the largest nights.

## 2. Non-Target

**Ontology:** [Non-Target](README.md#non-target).

**Today (Classify):** `data-flow/2.identify/error-categories.ts`. Labels are `ERROR` or `ERROR_<reason>`, the built-in reasons are Frass and Blur, and custom reasons are kept in the browser's `localStorage`. So they don't travel with the dataset, and another computer won't know them.

**Changes:**
1. **A hierarchy with Non-Target at the top**, and built-in Error and Abiotic below it. Users can add subcategories at any level, such as Frass or Plantae.
2. **Store the hierarchy in the package** (e.g. `02_records/non-target-categories.ndjson`), not in `localStorage`. Import existing custom reasons from `localStorage` into it on first open.
3. **Label form:** a path, e.g. `NON_TARGET`, `NON_TARGET/Error`, `NON_TARGET/Error/Blur`. Mapping old labels on read:

    | Old label | Read as |
    |---|---|
    | `ERROR` | Non-Target |
    | `ERROR_Blur` | Non-Target › Error › Blur |
    | `ERROR_Frass` | Non-Target › Frass (a user subcategory, created on first read so the information isn't lost) |
    | `ERROR_<custom>` | Non-Target › `<custom>` |

4. **Interface:** the "Error" action and filters become "Non-Target", with a picker for the subcategory.
5. **Check** how the Darwin Core export treats Non-Target detections today, and decide whether they are left out or written with their category.

## 3. Occurrences

**Ontology:** [Occurrence](README.md#occurrence), [Detection](README.md#detection).

**Today:** there is no occurrence record. The Classify export writes `occurrenceID` from the patch ID (`4.export/darwin-csv.ts`). Process's old exporter uses the patch filename (`pipeline/export_csv.py`).

**Changes:**
1. Add `occurrence_id` to each patch record. The default is one occurrence per detection, with the occurrence ID equal to the patch ID, so existing exports keep the same values.
2. Identifications and determinations reference the `occurrence_id`, and also the `patch_id` of the detection they were made from.
3. Later, a tracking stage in Process can merge detections into one occurrence. Antenna's unmerged tracking work (PR #1272) is a model for this. Clusters stay separate and are never turned into occurrences.

## 4. Taxon keys and taxa lists

**Ontology:** [Taxon Keys](README.md#taxon-keys), [Taxa List](README.md#taxa-list).

**Today (Classify):** `TaxonRecord.taxonID` plus `taxonIDSource`, which is `'gbif-backbone' | 'col'` (`models/taxonomy/species-list-source.ts`). That is already the "key plus key style" the meeting agreed on. Taxa lists record their DOI (`speciesListDOI`).

**Changes:**
1. Add the `bold`, `inat` and `fieldguide` key styles. Use the ontology's style names (`gbif`, `col`, `bold`, `inat`, `fieldguide`) when writing, and keep reading `gbif-backbone`.
2. Allow more than one key per taxon (a map from style to key), since a BOLD BIN and a GBIF key can both be known.
3. Every taxa list records its source (DOI or URL) and key style. Process does the same for the lists in `specieslists/`.

## 5. Deployments, devices and events

**Ontology:** [Deployment](README.md#deployment), [Session](README.md#session), [Capture Window](README.md#capture-window), [Capture](README.md#capture), [Site](README.md#site), [Location](README.md#location), [Device](README.md#device), [Device Type](README.md#device-type), [Attractor](README.md#attractor), [Sensor](README.md#sensor), and the tree in [How the pieces fit together](README.md#how-the-pieces-fit-together).

**Today:**
- **Process** reads a field sheet (`pipeline/insert_metadata.py`, `FIELD_ALIASES`). `device` holds the individual unit's name (e.g. SnappySloth). The sheet also has `firmware`, `sheet`, `site`, `latitude`, `longitude`, `height_above_ground` (stored as `ground_height`), `attractor` or `attractor1`–`3` with settings, `attractor_location` and `habitat`. Columns it doesn't recognise are kept in `field_sheet_metadata`.
- **Package:** `DeploymentRecord` (`mothbox-next/records.ts`) has `site_id` and `device_id`. Nights are `camera_day_id`.
- **Export:** `parentEventID` is the deployment name and `eventID` is the photo filename (`export_csv.py`). The session and capture-window levels are missing.

**Changes:**
1. **Device types:** read the defaults from [device-types/device-types.json](device-types/device-types.json) (D6). Users can add types or customize one, stored in the dataset's own settings with `derivedFrom` (see [device-types/README.md](device-types/README.md)). First, fill in the skeleton's attractor and target values.
2. **Field sheet:**
    - Add `device_type`, `facing_direction`, target size and distance, sensor type and resolution, and site description and land-use type.
    - Describe attractors as a list, each with type, location and power level. This generalizes `attractor1`–`3` and their settings columns.
    - Keep reading every old column name.
3. **Package records:** extend `DeploymentRecord` with the site, location, device and device-type fields, so they travel with the package instead of living only in Process's per-photo JSON.
4. **Events:**
    - **Store sessions explicitly, in a session file.** Today a night is only implied, by the night folder's date and the noon split in Classify's `derive-dinalab-hierarchy.ts`.
        - Process writes `_processed/<deployment>/sessions.json`, one per deployment, next to the mirrored night folders (`core/paths.py`). It fills in the default nightly sessions, noon to 11:59 the next morning, in the deployment's local time:

            ```json
            {
              "format": "mothbox-sessions",
              "formatVersion": 1,
              "deploymentID": "SnappySloth_LesBeachPalm_2026-07-27",
              "sessions": [
                {
                  "sessionID": "SnappySloth_2026-07-27",
                  "start": "2026-07-27T12:00:00-05:00",
                  "end": "2026-07-28T11:59:59-05:00",
                  "definedBy": "nightly-noon-to-noon"
                }
              ]
            }
            ```

        - If the file already exists, Process adds sessions for new nights and never changes existing ones, so edits made by people survive re-runs.
        - Sessions are matched to captures by time, not by folder, so photos taken after midnight land in the right night.
        - Classify reads the file when it builds a package, and gives every patch a `sessionID` and a `captureWindowID`. Antenna's import can read the same file instead of applying its gap rule.
    - **Let people edit sessions** in Classify, e.g. merge two nights or split one, without touching the identifications. An edited session records `definedBy: "manual"`.
    - **Export the session start and end**, so Antenna can keep Mothbox sessions as they are instead of regrouping them with its 2-hour gap rule.
    - Process can find capture windows from capture timestamps (a gap much longer than the capture interval starts a new window), or read them from the firmware's schedule.
    - The export then writes the full `parentEventID` chain: deployment → session → capture window → capture.
5. **Firmware:**
    - Say "capture window" instead of "session" for each scheduled stretch, in the settings file and in the logs.
    - Most of the device metadata is already there. `mothbox_exif.py` writes the device name (`mothbox`), firmware version, body model (EXIF `Model`, e.g. "Mothbox Pro + Arducam 64MP OwlSight (OV64A40)") and the camera and lens into every photo. Add the `deviceTypeID` from the device-type list.
    - **Process:** read these EXIF values as the default for `deviceID`, `deviceType` and firmware version, so data carries them even without a field sheet. The field sheet still overrides them.

## 6. Boxes

**Ontology:** [Box Formats](README.md#box-formats). Background: [Ways to write a box](NOTES.md#ways-to-write-a-box).

**Today (Process, `pipeline/detect.py`):**
- Detection JSONs are X-AnyLabeling files: `shape_type: rotation`, four corner `points` in pixels, plus a `direction` angle.
- The two detection paths compute `direction` differently. The ONNX path takes the model's radians and converts them to degrees. The `.pt` path writes OpenCV `minAreaRect`'s angle in degrees. X-AnyLabeling itself writes radians.
- No box carries a format label.
- Classify ignores `direction` and works from the corners. The package's `crop_points` are in pixels.

**Options considered for D1** (A was chosen):

| | A. Four corners, relative (chosen) | B. Centre, size and angle, relative |
|---|---|---|
| Written as | `x1, y1, x2, y2, x3, y3, x4, y4`, each 0–1 | `cx, cy, w, h` (0–1) and an angle |
| Angle questions (units, direction, zero side) | none | all must be fixed in the format |
| Same as | Ultralytics OBB training labels (`xyxyxyxyn`); X-AnyLabeling corners divided by the image size | Ultralytics OBB inference output (`xywhr`) |
| Upright box | min/max of the corners | needs trigonometry |
| Weak point | four points could be entered out of order | the angle conventions; and w, h are only relative to one axis each, so the angle must be measured on the pixel grid |

Antenna's "x1, y1, x2, y2 + rotation" is a form of B: two opposite corners of an upright rectangle, rotated around its centre (format label `xyxyr`). Converting between it and four corners is a few lines of code. Mothbox exports meant for Antenna can write it under its own label.

**Changes:**
1. **Format labels** on every stored box, from the list in [Box Formats](README.md#box-formats). A box without a label is read as `xanylabeling-rotation-px`.
2. **Relative boxes in the package:** Process writes a relative box into the package records next to the existing pixel `crop_points`. Its image width and height come from `imageWidth`/`imageHeight` in the detection JSON. Relative means relative to the image after EXIF orientation is applied, which should be stated in the format.
3. **X-AnyLabeling files stay as they are (D2),** so hand-labelling keeps working. One shared function converts `xanylabeling-rotation-px` to `obb-corners-rel` and back. Separately, fix `direction` on both detection paths to X-AnyLabeling's convention (radians), so files opened in X-AnyLabeling show the right rotation.
4. **Classify** reads both labelled and unlabelled boxes.

## 7. Export field names

**Ontology:** [Field Names](README.md#field-names).

**Today:** both exports mix styles. Classify's `4.export/darwin-csv.ts` writes `species_list_doi`, `taxonID_source`, `ID_confidence`, `cluster_ID` and `original_mothbox_identifciation` (with a typo). Process's `pipeline/export_csv.py` writes `UTCOFFSET`, `ground_height` and `deployment_name`. Python code is already snake_case and TypeScript camelCase, which matches the rule.

**Package files (D3):** the next package format version writes camelCase field names in `dataset.json`, `02_records/` and `03_classifications/` (`patch_id` → `patchID`, `classifier_type` → `identifierType`, …). Readers accept both, so existing datasets and collaborators' snake_case files keep loading. Do this together with the phase 1 format change, so packages change version only once.

**Exported columns:** rename every exported column to camelCase in one release, keep Darwin Core names where Darwin Core has them, and note the change in the release notes. Main renames:

| Today | New |
|---|---|
| `species_list_doi`, `species_list_exclusions` | `taxaListDOI`, `taxaListExclusions` |
| `taxonID_source` | `taxonIDSource` |
| `identifiedBy` | `identifiedBy` (the `identifierName`), plus a new `identifierType` |
| `detectionBy` | `detectedBy` |
| `detection_confidence`, `ID_confidence` | `detectionScore`, `identificationScore` |
| `original_mothbox_identifciation` | `machineIdentification` (the latest machine identification) |
| `cluster_ID`, `temporal_subcluster_ID` | `clusterID`, `trackID` |
| `pixel_mass_pixels`, `pixel_mass_method`, … | `pixelMassPixels`, `pixelMassMethod`, … |
| `UTCOFFSET` | `utcOffset` |
| `mothbox` | `deviceID`, plus a new `deviceType` |
| `ground_height` | `minimumDistanceAboveSurfaceInMeters` (Darwin Core) |
| `deployment`, `deployment_name` | `deploymentID` |

New columns from earlier phases: `determinationAlgorithm`, `occurrenceID` (from phase 3), `sessionID`, `captureWindowID`, and the non-target category.

Anything that reads these CSVs back in, including Classify's own imports, must accept both old and new names.

## 8. Words on screen

Changed along with the phase that touches each one:

| Today | New | Phase |
|---|---|---|
| Accept | Agree (the A shortcut stays) | 1 |
| current classification / ID | Determination | 1 |
| Error | Non-Target | 2 |
| species list | taxa list (keep "species list" only for GBIF species-list downloads) | 4 |
| confidence | score (detection score, identification score) | 7 |
| night | stays "night" as the name of the default session type | 5 |
| dataset | project (in Classify's screens; the `dataset.json` file name can stay until the next package format version) | 7 |
