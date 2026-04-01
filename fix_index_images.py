# -*- coding: utf-8 -*-
"""
Einmal ausführen (Doppelklick oder: python fix_index_images.py):
1. Kopiert die 6 PNGs in den Ordner images/ (kurze Dateinamen)
2. Ersetzt in index (9).html die Base64-Bilder durch images/... (funktioniert auf dem Server)

Danach: index (9).html UND den Ordner images/ zusammen per FTP auf bau-adam.de hochladen.
"""
import re
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
HTML = HERE / "index (9).html"
SRC_DIR = Path(
    r"C:\Users\save1\.cursor\projects\C-Users-save1-AppData-Local-Temp-6c672918-8890-447a-9185-ba91d1e72619\assets"
)

COPIES = [
    (
        "c__Users_save1_AppData_Roaming_Cursor_User_workspaceStorage_1774995621034_images_image__1_-9e33cbb7-797d-4081-b879-c3c50ebe24ee.png",
        "malerarbeiten.png",
    ),
    (
        "c__Users_save1_AppData_Roaming_Cursor_User_workspaceStorage_1774995621034_images_image-9f6d1afd-6c9c-4172-9d66-f17f03ff028b.png",
        "trockenbau.png",
    ),
    (
        "c__Users_save1_AppData_Roaming_Cursor_User_workspaceStorage_1774995621034_images_image__5_-d973724e-0c7a-4392-b554-702ad719097f.png",
        "reinigung.png",
    ),
    (
        "c__Users_save1_AppData_Roaming_Cursor_User_workspaceStorage_1774995621034_images_image__3_-db2e2f8f-ca3a-4a89-870a-8773da88a682.png",
        "stuckateur-innen.png",
    ),
    (
        "c__Users_save1_AppData_Roaming_Cursor_User_workspaceStorage_1774995621034_images_image__4_-671b7d11-c0e3-477d-afc0-cfb0b0983be4.png",
        "fliesen.png",
    ),
    (
        "c__Users_save1_AppData_Roaming_Cursor_User_workspaceStorage_1774995621034_images_image__2_-6c369cf2-805e-4083-8662-1653ba0e59b0.png",
        "stuckateur-fassade.png",
    ),
]

# Reihenfolge wie in der Galerie: maler, trocken, reinigung, stuck innen, fliesen, stuck fassade
IMG_ORDER = [
    "images/malerarbeiten.png",
    "images/trockenbau.png",
    "images/reinigung.png",
    "images/stuckateur-innen.png",
    "images/fliesen.png",
    "images/stuckateur-fassade.png",
]


def main():
    img_dir = HERE / "images"
    img_dir.mkdir(parents=True, exist_ok=True)

    for long_name, short_name in COPIES:
        src = SRC_DIR / long_name
        dst = img_dir / short_name
        if not src.is_file():
            print(f"FEHLT (Quelle): {src}")
            continue
        shutil.copy2(src, dst)
        print(f"OK kopiert: {short_name} ({dst.stat().st_size} Bytes)")

    text = HTML.read_text(encoding="utf-8")

    idx = 0

    def repl(m):
        nonlocal idx
        if idx >= len(IMG_ORDER):
            return m.group(0)
        new_src = IMG_ORDER[idx]
        idx += 1
        return m.group(1) + new_src + m.group(3)

    # src="data:image..." oder src="images/..." erneut ersetzen
    new_text, n = re.subn(
        r'(<img class="project-card-img" src=")([^"]+)(")',
        repl,
        text,
        count=6,
    )
    if n != 6:
        raise SystemExit(f"Erwartet 6 Galerie-Bilder, ersetzt: {n}")

    if idx != 6:
        raise SystemExit("Interner Fehler: Zähler")

    HTML.write_text(new_text, encoding="utf-8")
    print(f"\nFertig: {HTML}")
    print("Bitte index (9).html und Ordner images/ zusammen auf den Webspace laden.")


if __name__ == "__main__":
    main()
