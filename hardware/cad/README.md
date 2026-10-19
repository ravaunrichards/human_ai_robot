# Hardware / CAD

**Status: PARAMETRIC LAYOUT SCRIPT (not a manufacturing model).**

`skeleton_layout.py` generates a reproducible, schematic skeleton: the standing
envelope and joint-frame positions as a simple point/segment model, exported to
JSON. It is a **layout aid** to reason about proportions and joint placement —
NOT a solid CAD model and NOT manufacturable geometry.

## Why a script instead of binary CAD
Binary CAD files cannot be reviewed in text or regenerated deterministically.
The script is version-controllable and reproducible. For real parts, import the
joint-frame coordinates into FreeCAD/SolidWorks/Fusion and build solids with
proper materials and tolerances.

## Run
```bash
python hardware/cad/skeleton_layout.py --out hardware/cad/skeleton.json
```
