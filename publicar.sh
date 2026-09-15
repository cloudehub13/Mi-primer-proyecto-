#!/usr/bin/env sh
# Publica el catalogo. Sube docs/ a la rama gh-pages, que es la que sirve
# https://cloudehub13.github.io/Mi-primer-proyecto-/
# Uso:  ./publicar.sh
set -e
# sello de version: obliga al navegador a recargar fotos y fichas cambiadas
SELLO=$(date +%Y%m%d%H%M)
sed -i "s/const VER=\"[^\"]*\"/const VER=\"$SELLO\"/" docs/index.html
git add docs/index.html
git diff --cached --quiet || git commit -q -m "Sello de version $SELLO"
git push origin main
git push origin "$(git subtree split --prefix docs main)":refs/heads/gh-pages --force
echo
echo "Publicado. En 1-2 minutos:"
echo "https://cloudehub13.github.io/Mi-primer-proyecto-/"
