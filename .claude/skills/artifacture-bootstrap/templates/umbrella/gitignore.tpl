# Der Inhalt von src/ hat IMMER eigene Git-Historie — das Umbrella bleibt ein
# separates, code-freies Repo. AI-Tooling (z.B. extract-umbrella) liest hier
# bewusst trotzdem rein.
src/*
!src/.gitkeep

# Lokale Claude-Konfiguration
.claude/settings.local.json

# OS / Editor noise
.DS_Store
Thumbs.db
*.swp
.vscode/
.idea/

# Lokale Konfiguration / Secrets
.mcp.json
.env
.env.local
.env.*.local
*.local.md
