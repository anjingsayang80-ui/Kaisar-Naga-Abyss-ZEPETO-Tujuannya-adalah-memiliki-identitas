# Blender preview helper

`prepare_preview.py` builds a simple three-quarter studio render of the current OBJ blockout.

## Use

1. Download the repository and keep the `assets` and `blender` folders together.
2. Open Blender and switch to the **Scripting** workspace.
3. Open `blender/prepare_preview.py`.
4. Change `OBJ_PATH` near the top if your downloaded folder is somewhere else.
5. Run the script. It writes `kaisar_naga_abyss_preview.png` to the configured output path.

The script is only for inspecting the concept mesh. It does not make the robe ZEPETO-ready: the official avatar base, fit corrections, UV unwrap, rigging, weight transfer, pose tests, and export validation are still required.