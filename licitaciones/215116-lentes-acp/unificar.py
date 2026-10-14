#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Une, por cada renglón, la propuesta técnica con la ficha del fabricante ya
rotulada y resaltada, en un solo PDF. Así cada renglón viaja al SLI como un
documento único: la matriz de cumplimiento primero y su evidencia detrás.
"""
import os
import pymupdf

PARES = [
 ("pdf/01-RENGLON-1-PPE-EYE-00026.pdf",
  "fichas-rotuladas/ANEXO-A-R1-PPE-EYE-00026-MCR-MP110AF.pdf",
  "final/RENGLON-1-PPE-EYE-00026-MCR-MP110AF.pdf"),
 ("pdf/02-RENGLON-2-PPE-EYE-00027.pdf",
  "fichas-rotuladas/ANEXO-A-R2-PPE-EYE-00027-MCR-MP112PF.pdf",
  "final/RENGLON-2-PPE-EYE-00027-MCR-MP112PF.pdf"),
]

def unir(propuesta, ficha, salida):
    doc = pymupdf.open(propuesta)
    doc.insert_file(ficha)
    doc.save(salida, garbage=3, deflate=True)
    paginas = doc.page_count
    doc.close()
    return salida, paginas

if __name__ == "__main__":
    os.makedirs("final", exist_ok=True)
    for propuesta, ficha, salida in PARES:
        ruta, n = unir(propuesta, ficha, salida)
        print("%-52s %d páginas" % (ruta, n))
