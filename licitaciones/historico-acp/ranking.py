# -*- coding: utf-8 -*-
"""Quien va mas bajo en cada renglon, y donde quedamos nosotros."""
import importlib.util, os, sys
_d = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("datos", os.path.join(_d, "datos.py"))
D = importlib.util.module_from_spec(spec); spec.loader.exec_module(D)

def ofertas(acto, i):
    """(precio, monto, razon, propuesta) de quienes SI ofertaron el renglon i."""
    cant = acto["renglones"][i][1]
    return sorted([(p[i], p[i]*cant, razon, num)
                   for num, razon, _, _, p in acto["propuestas"] if p[i] > 0])

def informe(clave):
    acto = D.ACTOS[clave]
    print("=" * 78)
    print("LICITACIÓN %s — %s   ·   %d propuestas   ·   %s"
          % (clave, acto["titulo"], len(acto["propuestas"]), acto["conocimiento"]))
    print("=" * 78)
    for i, (n, cant, desc) in enumerate(acto["renglones"]):
        o = ofertas(acto, i)
        print("\nRENGLÓN %s — %s   (%s unidades, %d ofertas)" % (n, desc, "{:,}".format(cant), len(o)))
        if not o:
            print("   desierto: nadie ofertó"); continue
        pu, monto, razon, num = o[0]
        print("   MÁS BAJO:  %-33s US$ %-9s → US$ %s   (prop. %s)"
              % (razon, "{:,.4f}".format(pu).rstrip("0").rstrip("."), "{:,.2f}".format(monto), num))
        if len(o) > 1:
            pu2, m2, r2, n2 = o[1]
            print("   2.º:       %-33s US$ %-9s → US$ %s   (prop. %s)"
                  % (r2, "{:,.4f}".format(pu2).rstrip("0").rstrip("."), "{:,.2f}".format(m2), n2))
        nuestras = [(k, x) for k, x in enumerate(o, 1) if x[2] == D.NOSOTROS]
        if nuestras:
            k, (pu_n, m_n, _, num_n) = nuestras[0]
            dif = (pu_n / pu - 1) * 100 if pu else 0
            print("   NOSOTROS:  puesto %d de %d   US$ %s   (%+.0f%% vs el más bajo)"
                  % (k, len(o), "{:,.2f}".format(pu_n), dif))
        else:
            print("   NOSOTROS:  no ofertamos este renglón")

if __name__ == "__main__":
    for c in sys.argv[1:] or sorted(D.ACTOS):
        informe(c); print()
