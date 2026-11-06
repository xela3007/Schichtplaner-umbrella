# Source code lives here as sub-repos with their own git history.
# The umbrella tracks documentation and decisions only — not the source.
# IMPORTANT: AI tooling (e.g. the extract-umbrella skill) deliberately
# bypasses this rule when scanning code; that's expected.
src/*
!src/.gitkeep

# Local Claude configuration (shared .claude/settings.json IS tracked)
.claude/settings.local.json

# OS / editor noise
.DS_Store
Thumbs.db
*.swp
.vscode/
.idea/

# Local-only configuration / secrets
.mcp.json
.env
.env.local
*.local.md
