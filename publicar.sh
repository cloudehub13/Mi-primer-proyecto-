#!/usr/bin/env sh
# Publica el catalogo. Sube docs/ a la rama gh-pages, que es la que sirve
# https://cloudehub13.github.io/Mi-primer-proyecto-/
# Uso:  ./publicar.sh
set -e
git push origin main
git push origin "$(git subtree split --prefix docs main)":refs/heads/gh-pages --force
echo
echo "Publicado. En 1-2 minutos:"
echo "https://cloudehub13.github.io/Mi-primer-proyecto-/"
