# ZEPETO Avatar Fitting — Kaisar Naga Abyss

This document records the next production stage for the original robe blockout.

## 1. Official creator base
Download the current ZEPETO creator base set and the TOP/BTM dummy from the official Studio Guide:
https://docs.zepeto.me/studio-guide/prepare-for-3d-modeling

Do not guess the avatar scale or invent a replacement skeleton. Use the official base armature and mask so the expected object and bone names are preserved.

## 2. Fit the robe
1. Import the creator base FBX into Blender.
2. Import `assets/kaisar_naga_abyss.obj` with its MTL file in the same folder.
3. Align the robe to the official avatar in the required rest pose (T-pose or A-pose as specified by the current item guide).
4. Adjust torso, waist, collar, sleeves, and robe hem so they do not intersect the avatar or leave visible gaps.
5. Keep shoulder and elbow topology suitable for bending. Add supporting edge loops where needed.
6. Check the waist boundary and garment intersections from front, side, and back.

## 3. Rigging workflow
Follow the official ZEPETO rigging guide:
https://docs.zepeto.me/studio-guide/rigging

General sequence:
1. Keep the supplied base armature and mask.
2. Parent the clothing mesh to the armature with empty weights.
3. Transfer weights from the supplied mask to the clothing mesh using the documented **By Name** option.
4. Inspect and correct weight paint around shoulders, elbows, waist, and sleeves.
5. Test deformations with the avatar's poses before export.

## 4. Optimization checks
Check the current official category guide before submission:
https://docs.zepeto.me/studio-guide/3d-modeling-optimization-guide-by-category

The current guide search result lists these clothing triangle limits:
- Single outfit / Dress (DR): 10,000 triangles maximum.
- Top (TOP) / Outerwear (OTR): 6,000 triangles maximum.
- Bottom (BTM): 5,000 triangles maximum.

Also check texture size, material count, bone count, naming, and export requirements in the current Studio documentation. Do not assume these values replace the full submission rules.

## 5. Current project status
- [x] Original static OBJ blockout created.
- [x] Black, crimson, and gold MTL materials created.
- [x] Design avoids copying a named donghua/game character or franchise symbol.
- [ ] Official ZEPETO creator base FBX added and alignment completed.
- [ ] Garment fitted to the avatar.
- [ ] UV unwrap and texture atlas created.
- [ ] Armature binding and weight transfer completed.
- [ ] Pose/deformation tests completed.
- [ ] Exported and validated in the current ZEPETO Studio pipeline.

## Important
The OBJ is a **static concept blockout**, not a finished wearable. It is not yet rigged, UV-unwrapped, avatar-fitted, or approved by ZEPETO. Do not upload it as a finished item until every required validation step is complete.
