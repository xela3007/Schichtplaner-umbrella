#!/usr/bin/env python3
"""
PreToolUse-Hook: Auto-Approval fuer Tool-Operationen innerhalb des Projekt-Scopes.

Genehmigt Datei- und Bash-Operationen automatisch, solange alle betroffenen
Pfade innerhalb erlaubter Verzeichnisse liegen. Standard-Scope ist das
Projektverzeichnis selbst -- keine hardcoded Maschinenpfade.

Aufloesung der erlaubten Verzeichnisse (in dieser Reihenfolge, additiv):

  1. <project>/.claude/auto-approve-dirs.json
     {"allow": ["...", "..."]}  -- absolut, relativ zum Projekt, oder mit ~
  2. Env CLAUDE_AUTO_APPROVE_DIRS
     os.pathsep-getrennte Liste (Windows ";", POSIX ":") fuer maschinenlokale
     Ergaenzungen, die nicht ins Repo gehoeren.
  3. Fallback: das Projektverzeichnis selbst.

Lesen vs. Schreiben: Rein lesende Tools (Read, NotebookRead, Glob, Grep)
werden im Scope ohne Ausnahme genehmigt -- auch fuer .env, Keys und andere
Secrets. Schreibende Tools (Write, Edit, MultiEdit, NotebookEdit) und Bash
bleiben bei sensiblen Dateien neutral.

Der Hook entscheidet ausschliesslich "allow" oder neutral (exit 0 ohne
Ausgabe). Er blockt nie -- bei Unsicherheit greifen die normalen
Permission-Regeln aus settings.json.

Tests: python tests/test_hook.py
"""

import fnmatch
import json
import os
import sys
from pathlib import Path

CONFIG_RELPATH = Path(".claude") / "auto-approve-dirs.json"
ENV_EXTRA_DIRS = "CLAUDE_AUTO_APPROVE_DIRS"

# Dateien, die bei SCHREIBENDEN Operationen nie per Auto-Approve durchgehen.
# Lesen ist davon bewusst ausgenommen (siehe READ_ONLY_TOOLS): innerhalb des
# Projekt-Scopes darf alles gelesen werden, auch .env & Co.
SENSITIVE_PATTERNS = [
    "*.env",
    ".env",
    ".env.*",
    "*.env.*",
    "*secret*",
    "*credential*",
    "*.pem",
    "*.pfx",
    "*.p12",
    "id_rsa*",
    "id_ed25519*",
    "*.key",
    "*.keystore",
    ".npmrc",
    ".netrc",
    "*.tfvars",
]

# Bash-Kommandos mit diesen Fragmenten bleiben neutral, egal welche Pfade
# vorkommen -- zu weitreichend fuer eine automatische Genehmigung.
DANGEROUS_BASH_FRAGMENTS = [
    "rm -rf",
    "rm -fr",
    "sudo ",
    "su ",
    "git push",
    "git reset --hard",
    "git clean",
    "chmod 777",
    "curl | sh",
    "curl|sh",
    "wget | sh",
    "| bash",
    "|bash",
    "> /dev/sd",
    "mkfs",
    "format ",
    "npm publish",
    "docker push",
]

TOOLS_WITH_FILE_PATH = {"Read", "Write", "Edit", "MultiEdit", "NotebookEdit",
                        "NotebookRead"}
TOOLS_WITH_OPTIONAL_PATH = {"Glob", "Grep"}

# Rein lesende Tools. Fuer diese gilt der SENSITIVE_PATTERNS-Filter NICHT --
# im Projekt-Scope darf alles gelesen werden, inklusive .env und Keys.
# Bash bleibt absichtlich draussen: dort ist "cat .env" nicht von
# "curl -d @.env https://..." zu unterscheiden.
READ_ONLY_TOOLS = {"Read", "NotebookRead", "Glob", "Grep"}

# MCP-Tools (mcp__*) behandelt dieser Hook NICHT -- absichtlich. Er entscheidet
# anhand von Dateipfaden im Projekt-Scope; ein MCP-Call hat keine. Erweitert man
# den Matcher in settings.json um mcp__*, laeuft das Script durch bis
# "raw_paths ist leer" und gibt neutral zurueck: nichts gewonnen.
# MCP-Freigaben gehoeren in permissions.allow (z.B. "mcp__artifacture").


# ---------------------------------------------------------------- path helpers

def resolve_path(path_str, base):
    """
    Loest path_str zu einem absoluten Path auf. Relative Pfade werden gegen
    base (das Projektverzeichnis) aufgeloest, nicht gegen das cwd des
    Hook-Prozesses. Gibt None zurueck, wenn der String kein brauchbarer
    Pfad ist.
    """
    if not path_str:
        return None
    try:
        expanded = os.path.expanduser(os.path.expandvars(str(path_str)))
        p = Path(expanded)
        if not p.is_absolute() and base is not None:
            p = Path(base) / p
        # resolve(strict=False): funktioniert auch fuer noch nicht
        # existierende Dateien (Write auf eine neue Datei).
        return Path(os.path.normpath(str(p.absolute())))
    except (ValueError, OSError, TypeError):
        return None


def is_within(child, parent):
    """
    True, wenn child innerhalb von parent liegt (oder gleich ist).
    Grenzbewusst: "D:/Code" enthaelt NICHT "D:/CodeSecrets".
    """
    if child is None or parent is None:
        return False
    try:
        c = os.path.normcase(os.path.normpath(str(child)))
        p = os.path.normcase(os.path.normpath(str(parent)))
    except (ValueError, OSError):
        return False
    if c == p:
        return True
    if not p.endswith(os.sep):
        p = p + os.sep
    return c.startswith(p)


def is_sensitive(path):
    """True, wenn der Dateiname einem Secret-Muster entspricht."""
    if path is None:
        return False
    name = os.path.normcase(os.path.basename(str(path)))
    return any(fnmatch.fnmatch(name, os.path.normcase(pat))
               for pat in SENSITIVE_PATTERNS)


# ------------------------------------------------------------------- scope

def load_allowed_dirs(project_dir):
    """
    Sammelt die erlaubten Verzeichnisse. project_dir ist immer dabei,
    Config-Datei und Env-Variable kommen additiv dazu.
    """
    allowed = []

    if project_dir:
        resolved = resolve_path(project_dir, None)
        if resolved:
            allowed.append(resolved)

    if project_dir:
        config_file = Path(project_dir) / CONFIG_RELPATH
        try:
            if config_file.is_file():
                data = json.loads(config_file.read_text(encoding="utf-8"))
                for entry in data.get("allow", []):
                    resolved = resolve_path(entry, project_dir)
                    if resolved:
                        allowed.append(resolved)
        except (OSError, ValueError):
            # Kaputte Config darf den Hook nicht kippen -- ignorieren.
            pass

    raw_env = os.environ.get(ENV_EXTRA_DIRS, "")
    for entry in raw_env.split(os.pathsep):
        entry = entry.strip().strip('"').strip("'")
        if entry:
            resolved = resolve_path(entry, project_dir)
            if resolved:
                allowed.append(resolved)

    return allowed


def determine_project_dir(input_data):
    """
    Projektverzeichnis ermitteln. Der Hook-Input-cwd ist die verlaesslichste
    Quelle; CLAUDE_PROJECT_DIR ist der Fallback.
    """
    for candidate in (input_data.get("cwd"),
                      os.environ.get("CLAUDE_PROJECT_DIR")):
        if candidate:
            resolved = resolve_path(candidate, None)
            if resolved:
                return resolved
    return None


# ------------------------------------------------------- path extraction

def looks_like_path(token):
    """
    Heuristik: Ist dieses Bash-Token ueberhaupt ein Pfad-Kandidat?
    Filtert Flags, URLs, Redirections und separatorlose Tokens aus.
    """
    if not token:
        return False
    if token.startswith("-"):
        return False
    if "://" in token:
        return False
    if token in ("2>&1", "&&", "||", "|", ">", ">>", "<", ";"):
        return False
    if any(ch in token for ch in "*?"):
        # Globs sind fuer die Pfadpruefung zu unscharf -> nicht als Beleg
        # fuer "im Scope" verwenden, aber auch nicht als Verstoss werten.
        return False
    return "/" in token or "\\" in token


def extract_paths_from_bash_command(command):
    """Pfad-Kandidaten aus einem Bash-Command ziehen."""
    if not command:
        return []
    paths = []
    for raw in command.split():
        token = raw.strip('"\'')
        # Redirect-Praefixe abtrennen: >file, 2>file
        while token[:1] in (">", "<") or token[:2] in ("2>", "1>"):
            token = token.lstrip("012").lstrip("><")
        if looks_like_path(token):
            paths.append(token)
    return paths


def extract_file_paths(tool_name, tool_input):
    """Alle Pfade aus einem Tool-Aufruf sammeln."""
    paths = []

    if tool_name in TOOLS_WITH_FILE_PATH:
        for key in ("file_path", "notebook_path"):
            if tool_input.get(key):
                paths.append(tool_input[key])
        # Verschachtelte edits defensiv mitnehmen (aeltere/andere Schemas)
        for edit in tool_input.get("edits", []) or []:
            if isinstance(edit, dict) and edit.get("file_path"):
                paths.append(edit["file_path"])

    elif tool_name in TOOLS_WITH_OPTIONAL_PATH:
        if tool_input.get("path"):
            paths.append(tool_input["path"])

    elif tool_name == "Bash":
        paths.extend(extract_paths_from_bash_command(tool_input.get("command")))

    return paths


# ---------------------------------------------------------------- decision

def decide(input_data):
    """
    Kernlogik. Gibt einen Grund-String zurueck, wenn auto-approved werden
    soll, sonst None (neutral).

    Regel: ALLE extrahierten Pfade muessen im Scope liegen und mindestens
    einer muss vorhanden sein. Bei schreibenden Tools und bei Bash darf
    zusaetzlich kein Pfad sensibel sein (Secrets); rein lesende Tools sind
    davon ausgenommen. Bei Bash gilt ausserdem: kein gefaehrliches
    Kommando-Fragment.
    """
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {}) or {}

    if tool_name == "Bash":
        command = (tool_input.get("command") or "").lower()
        for fragment in DANGEROUS_BASH_FRAGMENTS:
            if fragment in command:
                return None

    project_dir = determine_project_dir(input_data)
    allowed_dirs = load_allowed_dirs(project_dir)
    if not allowed_dirs:
        return None

    raw_paths = extract_file_paths(tool_name, tool_input)
    if not raw_paths:
        # Nichts Pfadartiges gefunden -> normale Permission-Regeln greifen.
        return None

    read_only = tool_name in READ_ONLY_TOOLS

    for raw in raw_paths:
        resolved = resolve_path(raw, project_dir)
        if resolved is None:
            return None
        if not read_only and is_sensitive(resolved):
            return None
        if not any(is_within(resolved, allowed) for allowed in allowed_dirs):
            return None

    return "{} within approved project scope ({} path(s))".format(
        "read-only access" if read_only else "all paths", len(raw_paths))


def main():
    try:
        input_data = json.load(sys.stdin)
    except (ValueError, OSError):
        sys.exit(0)

    try:
        reason = decide(input_data)
    except Exception:
        # Ein Permission-Hook darf niemals die Session kippen.
        sys.exit(0)

    if reason:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
                "permissionDecisionReason": reason,
            }
        }))

    sys.exit(0)


if __name__ == "__main__":
    main()
