#!/usr/bin/env python3
"""Audit a Wavefront OBJ for basic ZEPETO clothing-prep issues.

Usage:
    python tools/audit_obj.py assets/kaisar_naga_abyss.obj

This is a static file check, not a ZEPETO validator. It does not inspect
avatar fit, deformation, texture dimensions, or Studio acceptance.
"""
from collections import Counter
from pathlib import Path
import sys


def audit(path: Path) -> int:
    if not path.is_file():
        print(f"ERROR: file not found: {path}")
        return 2

    vertices = 0
    texcoords = 0
    normals = 0
    faces = 0
    triangles = 0
    material_faces = Counter()
    current_material = "(none)"
    invalid_faces = []
    min_xyz = [float("inf")] * 3
    max_xyz = [float("-inf")] * 3

    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        kind = parts[0]
        if kind == "v" and len(parts) >= 4:
            vertices += 1
            try:
                xyz = [float(v) for v in parts[1:4]]
                for i, value in enumerate(xyz):
                    min_xyz[i] = min(min_xyz[i], value)
                    max_xyz[i] = max(max_xyz[i], value)
            except ValueError:
                invalid_faces.append((line_no, "invalid vertex coordinates"))
        elif kind == "vt":
            texcoords += 1
        elif kind == "vn":
            normals += 1
        elif kind == "usemtl":
            current_material = " ".join(parts[1:]) or "(unnamed)"
        elif kind == "f":
            faces += 1
            corners = parts[1:]
            triangles += max(0, len(corners) - 2)
            material_faces[current_material] += 1
            if len(corners) < 3:
                invalid_faces.append((line_no, "face has fewer than 3 vertices"))
            for corner in corners:
                vertex_index = corner.split("/")[0]
                try:
                    index = int(vertex_index)
                    if index == 0 or abs(index) > vertices:
                        invalid_faces.append((line_no, f"vertex index out of range: {index}"))
                except ValueError:
                    invalid_faces.append((line_no, f"invalid face corner: {corner}"))

    print(f"OBJ: {path}")
    print(f"Vertices: {vertices}")
    print(f"Faces: {faces}")
    print(f"Triangulated face estimate: {triangles}")
    print(f"UV coordinates (vt): {texcoords}")
    print(f"Vertex normals (vn): {normals}")
    if vertices:
        print("Bounds:")
        for axis, lo, hi in zip("XYZ", min_xyz, max_xyz):
            print(f"  {axis}: {lo:.5f} .. {hi:.5f} (span {hi-lo:.5f})")
    print("Faces by material:")
    for name, count in sorted(material_faces.items()):
        print(f"  {name}: {count}")

    problems = False
    if texcoords == 0:
        problems = True
        print("BLOCKER: no UV coordinates found; a texture atlas cannot be applied yet.")
    if not normals:
        print("NOTE: no explicit normals; the 3D application may need to recalculate them.")
    if invalid_faces:
        problems = True
        print(f"ERRORS: {len(invalid_faces)}")
        for line_no, message in invalid_faces[:20]:
            print(f"  line {line_no}: {message}")
    if not problems:
        print("Basic OBJ structure checks passed. This does not mean the garment is production-ready.")
    return 1 if problems else 0


if __name__ == "__main__":
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("assets/kaisar_naga_abyss.obj")
    raise SystemExit(audit(source))
