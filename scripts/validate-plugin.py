#!/usr/bin/env python3
"""Validate the BKM Agent Plugin before it is published.

Checks, in order:
  1. plugin/plugin.json against the Agent Plugins 1.0.0 manifest schema (vendored copy).
  2. plugin/mcp.json, when present, against the Agent Plugins 1.0.0 MCP schema; HTTPS only;
     no Authorization header or other credential may be embedded.
  3. Every skill under plugin/skills/ against the Agent Skills specification (skills-ref).
  4. The Codex and Claude Code marketplace files point at the plugin directory and agree on
     the plugin name, and plugin/.claude-plugin/plugin.json agrees with plugin/plugin.json.

Exit status is non-zero on the first failure. Requires: jsonschema, skills-ref.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT if (ROOT / "plugin.json").is_file() else ROOT / "plugin"
SCHEMAS = ROOT / "scripts" / "agent-plugins-schemas"
REL = str(PLUGIN.relative_to(ROOT)) if PLUGIN != ROOT else "."
PLUGIN_SCHEMA_ID = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_SCHEMA_ID = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
SECRET_HEADERS = {"authorization", "x-api-key", "api-key", "cookie", "proxy-authorization"}
CANONICAL_MCP_URL = "https://sidekick.benjaminknowledgemodels.com/v1/mcp"


def fail(message: str) -> None:
    print(f"FAIL  {message}")
    sys.exit(1)


def ok(message: str) -> None:
    print(f"ok    {message}")


def load(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"{path.relative_to(ROOT)} is missing")
    except json.JSONDecodeError as err:
        fail(f"{path.relative_to(ROOT)} is not valid JSON: {err}")
    raise AssertionError("unreachable")


def validate_against(instance: dict, schema_file: str, label: str) -> None:
    try:
        import jsonschema
    except ImportError:
        fail("the jsonschema package is required (pip install jsonschema)")
    schema = json.loads((SCHEMAS / schema_file).read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
    if errors:
        for err in errors:
            where = "/".join(str(p) for p in err.path) or "(root)"
            print(f"      {where}: {err.message}")
        fail(f"{label} does not conform to {schema_file}")
    ok(f"{label} conforms to {schema_file}")


def check_manifest() -> dict:
    manifest = load(PLUGIN / "plugin.json")
    if manifest.get("$schema") != PLUGIN_SCHEMA_ID:
        fail(f"plugin.json $schema must be {PLUGIN_SCHEMA_ID}")
    validate_against(manifest, "plugin.schema.json", f"{REL}/plugin.json")
    return manifest


def check_mcp() -> None:
    path = PLUGIN / "mcp.json"
    if not path.exists():
        print(f"note  {REL}/mcp.json is absent: this package does not configure a hosted MCP server")
        return
    mcp = load(path)
    if mcp.get("$schema") != MCP_SCHEMA_ID:
        fail(f"mcp.json $schema must be {MCP_SCHEMA_ID}")
    validate_against(mcp, "mcp.schema.json", f"{REL}/mcp.json")
    for name, server in mcp.get("mcpServers", {}).items():
        url = server.get("url", "")
        if server.get("type") in {"streamable-http", "sse"} and not url.startswith("https://"):
            fail(f"mcp.json server {name!r} must use an https URL")
        for header in server.get("headers", {}) or {}:
            if header.lower() in SECRET_HEADERS:
                fail(f"mcp.json server {name!r} embeds a credential header ({header}); the client"
                     " must obtain credentials itself")
        for key in ("env", "args"):
            for value in (server.get(key) or {}).values() if isinstance(server.get(key), dict) else (server.get(key) or []):
                if "Bearer " in str(value) or "token=" in str(value).lower():
                    fail(f"mcp.json server {name!r} appears to embed a secret in {key}")
        if name == "bkm":
            auth = server.get("extensions", {}).get("com.openai", {}).get("auth", {})
            if url != CANONICAL_MCP_URL:
                fail(f"mcp.json server 'bkm' must use the canonical Sidekick URL {CANONICAL_MCP_URL}")
            if auth.get("type") != "oauth" or auth.get("client") != {"mode": "cimd"}:
                fail("mcp.json server 'bkm' must declare OAuth with CIMD preference")
            if auth.get("resource") != url:
                fail("mcp.json server 'bkm' OAuth resource must exactly match its MCP URL")
            if auth.get("baseScopes") != ["mcp:tools"]:
                fail("mcp.json server 'bkm' must request exactly the mcp:tools base scope")
            if not str(auth.get("authorizationServerBase", "")).startswith("https://"):
                fail("mcp.json server 'bkm' authorization server must use HTTPS")
    ok(f"{REL}/mcp.json carries no credentials and uses HTTPS")

    claude_path = PLUGIN / ".mcp.json"
    if claude_path.exists():
        claude = load(claude_path)
        if set(claude) != {"mcpServers"} or not isinstance(claude["mcpServers"], dict):
            fail(f"{REL}/.mcp.json must contain only an mcpServers object")
        for name, server in claude["mcpServers"].items():
            if not isinstance(server, dict) or server.get("type") != "http":
                fail(f"{REL}/.mcp.json server {name!r} must use Claude Code's http transport")
            if not str(server.get("url", "")).startswith("https://"):
                fail(f"{REL}/.mcp.json server {name!r} must use an https URL")
            for header in (server.get("headers") or {}):
                if header.lower() in SECRET_HEADERS:
                    fail(f"{REL}/.mcp.json server {name!r} embeds a credential header ({header})")
        ok(f"{REL}/.mcp.json carries no credentials and uses HTTPS")


def check_skills(expected_plugin_name: str) -> None:
    try:
        from skills_ref import validate as validate_skill
    except ImportError:
        fail("the skills-ref package is required (pip install skills-ref)")
    skills_dir = PLUGIN / "skills"
    skill_dirs = sorted(p for p in skills_dir.iterdir() if (p / "SKILL.md").is_file()) if skills_dir.is_dir() else []
    if not skill_dirs:
        fail(f"{REL}/skills/ holds no skill with a SKILL.md")
    for skill_dir in skill_dirs:
        errors = validate_skill(skill_dir)
        if errors:
            for err in errors:
                print(f"      {err}")
            fail(f"skill {skill_dir.name} fails the Agent Skills specification")
        lines = (skill_dir / "SKILL.md").read_text(encoding="utf-8").splitlines()
        if len(lines) > 500:
            fail(f"skill {skill_dir.name}: SKILL.md has {len(lines)} lines; the specification asks for under 500")
        ok(f"skill {skill_dir.name} is a valid Agent Skill ({len(lines)} lines)")
    if expected_plugin_name not in {d.name for d in skill_dirs}:
        print(f"note  no skill is named after the plugin ({expected_plugin_name}); allowed, but unusual")


def check_marketplaces(manifest: dict) -> None:
    name = manifest["name"]
    if not (ROOT / ".agents" / "plugins" / "marketplace.json").exists():
        print("note  no marketplace files here; they live in the published plugin repository")
        cc = load(PLUGIN / ".claude-plugin" / "plugin.json")
        for field in ("name", "version", "description"):
            if cc.get(field) != manifest.get(field):
                fail(f"{REL}/.claude-plugin/plugin.json {field} differs from {REL}/plugin.json")
        ok(f"{REL}/.claude-plugin/plugin.json agrees with {REL}/plugin.json")
        return
    codex = load(ROOT / ".agents" / "plugins" / "marketplace.json")
    entries = [p for p in codex.get("plugins", []) if p.get("name") == name]
    if not entries:
        fail(f".agents/plugins/marketplace.json lists no plugin named {name!r}")
    source = entries[0].get("source", {})
    if source.get("source") != "local" or (ROOT / source.get("path", "")).resolve() != PLUGIN.resolve():
        fail(".agents/plugins/marketplace.json does not point at the plugin directory")
    policy = entries[0].get("policy", {})
    if policy.get("installation") not in {"AVAILABLE", "INSTALLED_BY_DEFAULT", "NOT_AVAILABLE"}:
        fail(".agents/plugins/marketplace.json: policy.installation is not a known value")
    ok(".agents/plugins/marketplace.json (Codex) points at the plugin directory")

    claude = load(ROOT / ".claude-plugin" / "marketplace.json")
    entries = [p for p in claude.get("plugins", []) if p.get("name") == name]
    if not entries or (ROOT / entries[0].get("source", "")).resolve() != PLUGIN.resolve():
        fail(".claude-plugin/marketplace.json does not list the plugin directory")
    ok(".claude-plugin/marketplace.json (Claude Code) points at the plugin directory")

    cc = load(PLUGIN / ".claude-plugin" / "plugin.json")
    for field in ("name", "version", "description"):
        if cc.get(field) != manifest.get(field):
            fail(f"{REL}/.claude-plugin/plugin.json {field} differs from {REL}/plugin.json")
    ok(f"{REL}/.claude-plugin/plugin.json agrees with {REL}/plugin.json")


def main() -> None:
    manifest = check_manifest()
    check_mcp()
    check_skills(manifest["name"])
    check_marketplaces(manifest)
    print(f"\nplugin {manifest['name']} {manifest.get('version', '')} is ready")


if __name__ == "__main__":
    main()
