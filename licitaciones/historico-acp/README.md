# Histórico de licitaciones ACP — precios por renglón

La ACP repite los mismos renglones acto tras acto. Esta carpeta guarda lo que
pagó o cotizó cada competidor, para fijar precio en la siguiente convocatoria
sin adivinar.

## Qué hay aquí

| Archivo | Qué es |
|---|---|
| `datos.py` | Las actas-cuadro resumen transcritas: cada propuesta con su precio unitario por renglón. Precio `0` = ese proponente no ofertó el renglón. |
| `ranking.py` | Saca el más bajo de cada renglón y en qué puesto quedamos. `python3 ranking.py` o `python3 ranking.py 215088`. |
| `actas/` | Los PDF originales del SLI, por si hay que verificar. |

La transcripción está cuadrada: los 42 montos totales que calcula `datos.py`
coinciden al centavo con los que imprime el acta.

## Cómo usarlo antes de cotizar

1. `python3 ranking.py` para ver el piso histórico de cada renglón.
2. Buscar el renglón equivalente por código ACP (`PPE-GLO-…`, `PPE-EYE-…`),
   que es lo que se repite entre actos, no el número de renglón.
3. Contrastar contra el costo propio. Si el piso histórico está por debajo del
   costo, ese renglón no se gana por precio: o se consigue otra fuente o no se
   oferta.

## Lo que hay que tener presente al leerlo

**Precio más bajo no es adjudicación.** La ACP evalúa primero el cumplimiento
técnico; solo entre las propuestas que cumplen escoge el precio más bajo por
renglón (numeral 1.5). Varios de los precios de abajo son tan bajos que
difícilmente corresponden al producto que pide la descripción, y suelen caerse
en la evaluación técnica. El piso real de adjudicación tiende a estar por
encima del piso de la tabla.

**Una empresa puede presentar varias propuestas.** Fastenal presentó tres en la
215088 y Pemco tres en la 215116. Cada una se evalúa aparte.

## Actos registrados

### 215088 — Guantes (conocimiento 12-oct-2026, 19 propuestas, enmienda 3)

| R | Código | Descripción | Cant. | Más bajo | P/U | Elite Guard |
|---|---|---|---|---|---|---|
| 1 | PPE-GLO-00009 | Guante dieléctrico baja tensión | 24 | Fastenal | 62.45 | no ofertamos |
| 2 | PPE-GLO-00012 | Guante químico industrial, t.9 | 1,500 | **ELITE GUARD** | **1.14** | **1.º de 9** |
| 3 | PPE-GLO-00020 | Guante punteado Kevlar®, t.10 | 960 | RR Industrial | 0.75 | 6.º de 6 — 7.69 |
| 4 | PPE-GLO-00022 | Examen nitrilo, mediano (caja) | 1,000 | Pro Custumer | 3.43 | 8.º de 11 — 9.60 |
| 5 | PPE-GLO-00031 | Anticorte A4 / EN 388 4-X-4-2-C, t.9 | 5,000 | Sondel | 1.25 | 12.º de 14 — 4.69 |
| 6 | PPE-GLO-00033 | Tejido palma y yemas PU, t.11 | 900 | CISA | 0.56 | 7.º de 10 — 2.89 |

### 215116 — Lentes de protección personal (conocimiento 13-oct-2026, 23 propuestas, enmienda 2)

| R | Código | Descripción | Cant. | Más bajo | P/U | Elite Guard |
|---|---|---|---|---|---|---|
| 1 | PPE-EYE-00026 | Lente de seguridad, claro | 15,840 | Master Industrial | 0.99 | 15.º de 23 — 4.59 |
| 2 | PPE-EYE-00027 | Lente de seguridad, oscuro | 10,800 | Master Industrial | 0.99 | 15.º de 23 — 4.59 |
| 3 | PPE-EYE-00028 | Lente protector, claro | 5,200 | Master Industrial | 1.479 | no ofertamos |
| 4 | PPE-EYE-00029 | Lente protector, gris/humo | 7,200 | Saf-T-Gard | 1.3007 | no ofertamos |
| 5 | PPE-EYE-00015 | Filtro tipo copa 50 mm, sombra 5 | 60 | José David Nieto | 4.99 | no ofertamos |

## Cómo agregar el próximo acto

Copiar el PDF del acta a `actas/`, añadir una entrada a `ACTOS` en `datos.py`
con sus renglones y propuestas, y correr `ranking.py` para que cuadre.
