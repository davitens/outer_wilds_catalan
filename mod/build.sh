#!/usr/bin/env bash
# Build the Catalan translation mod with Mono (no .NET SDK required) and deploy to OWML/Mods.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OWML="${OWML:-$HOME/.local/share/OuterWildsModManager/OWML}"
PROJ="$ROOT/mod"
OUT="$ROOT/bin"
DEPLOY="$OWML/Mods/davitens.CatalanTranslation"

ASSEMBLY="CatalanTranslation.dll"

mkdir -p "$OUT" "$DEPLOY/assets"

echo "Compiling $ASSEMBLY ..."
mcs -target:library -langversion:latest -out:"$OUT/$ASSEMBLY" \
  -r:"$OWML/OWML.ModHelper.dll" \
  -r:"$OWML/OWML.Common.dll" \
  -r:"$OWML/OWML.Utils.dll" \
  -r:"$OWML/Assembly-CSharp.dll" \
  -r:"$OWML/UnityEngine.CoreModule.dll" \
  -r:"$OWML/UnityEngine.TextRenderingModule.dll" \
  -r:"$OWML/netstandard.dll" \
  -r:"$OWML/0Harmony.dll" \
  "$PROJ"/*.cs

echo "Deploying to $DEPLOY ..."
cp "$OUT/$ASSEMBLY" "$DEPLOY/$ASSEMBLY"
cp "$PROJ/manifest.json" "$PROJ/default-config.json" "$DEPLOY/"
cp "$PROJ/assets/"*.xml "$DEPLOY/assets/"
[ -f "$DEPLOY/config.json" ] || printf '{ "enabled": true }\n' > "$DEPLOY/config.json"

echo "Done: $DEPLOY"
ls -R "$DEPLOY"
