# Automated-Insect-Monitoring-Ontology
Working towards a data standard or data schema for devices that try to image arthropods automatically in nature by creating a shared vocabulary

> [!NOTE]  
> Nerds who are good at computers and organizing stuff might have better suggestions for formatting this list of terms and definitions. If that's you, please change this however makes sense!

# creature
abstract term for living thing that is of interest for this work. Could be an insect or an arthopod or a gecko sneaking in.

# detection
a specific subset from a source image that ideally shows only 1 creature
## Attributes
- taxa (e.g. kingdom, Class, )
- source image coordinates (center and bounding box)
- Human_ID
- Machine_ID

# Track
a sequence of continuous detections

# Source Image
This is a photograph that can have different types of backgrounds and may contain one or more target species
## Assumtions
- static camera

# Session
a continuous series of Source Images

# Deployment
a collection of sessions that starts when a device is left in a location and ends when the device is removed from that location

# Device Location 
a very specific spot where a device is deployed (likely has attributes like a GPS coordinate and maybe a description of its exact spot like "left palm tree next to lake" or values like like "height above ground")

# Site
area being surveyed by a device. Might have a gps coordinate and a radius?

