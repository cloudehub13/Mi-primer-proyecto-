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
 ("pdf/02-RENGLON-2-PPE-GLO-00012.pdf",
  "fichas-rotuladas/ANEXO-A-R2-PPE-GLO-00012-ELITE-GUARD-J710.pdf",
  "final/RENGLON-2-PPE-GLO-00012-ELITE-GUARD-J710.pdf"),
 ("pdf/03-RENGLON-3-PPE-GLO-00020.pdf",
  "fichas-rotuladas/ANEXO-A-R3-PPE-GLO-00020-MCR-9366.pdf",
  "final/RENGLON-3-PPE-GLO-00020-MCR-9366.pdf"),
 ("pdf/04-RENGLON-4-PPE-GLO-00022.pdf",
  "fichas-rotuladas/ANEXO-A-R4-PPE-GLO-00022-MCR-6008.pdf",
  "final/RENGLON-4-PPE-GLO-00022-MCR-6008.pdf"),
 ("pdf/05-RENGLON-5-PPE-GLO-00031.pdf",
  "fichas-rotuladas/ANEXO-A-R5-PPE-GLO-00031-MCR-92754BP.pdf",
  "final/RENGLON-5-PPE-GLO-00031-MCR-92754BP.pdf"),
 ("pdf/06-RENGLON-6-PPE-GLO-00033.pdf",
  "fichas-rotuladas/ANEXO-A-R6-PPE-GLO-00033-MCR-92852PU.pdf",
  "final/RENGLON-6-PPE-GLO-00033-MCR-92852PU.pdf"),
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
        print("%-54s %d páginas" % (ruta, n))
