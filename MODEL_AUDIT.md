# Static OBJ audit — current blockout

Audit performed on `assets/kaisar_naga_abyss.obj` using `tools/audit_obj.py`.

| Check | Result |
|---|---:|
| Vertices | 408 |
| Polygon faces | 288 |
| Estimated triangles after triangulation | 728 |
| UV coordinates (`vt`) | 0 — missing |
| Explicit vertex normals (`vn`) | 0 — missing |
| BlackSilk faces | 146 |
| Crimson faces | 50 |
| Gold faces | 92 |

## What this means

- The mesh is a small static concept blockout by polygon count, but polygon count alone does not establish ZEPETO compliance.
- **UV mapping is the next concrete modeling blocker.** The OBJ currently contains no UV coordinates, so a designed texture atlas cannot be applied correctly yet.
- No explicit normals are stored. Recalculate/inspect normals in Blender after topology cleanup.
- This audit does not check avatar proportions, intersections, mesh manifoldness, deformation, rigging, texture sizes, or Studio validation.

Run the audit again after editing:

```bash
python tools/audit_obj.py assets/kaisar_naga_abyss.obj
```

Do not treat a passing static audit as proof that the item is upload-ready.