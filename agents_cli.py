#!/usr/bin/env python3
"""
Multi-Agent Collaboration CLI Tool

Usage:
    agents init [--template TEMPLATE]
    agents start [AGENTS...]
    agents add <name>
    agents list
    agents task status
"""

import os
import sys
import subprocess
import yaml
import click
from pathlib import Path


AGENTS_DIR = ".agents"
TEMPLATE_REPO = "https://github.com/loboking/agents-template"

DEFAULT_AGENTS = {
    "claude": {
        "cli_command": "claude",
        "name": "Claude Code"
    },
    "gemini": {
        "cli_command": "gemini", 
        "name": "Gemini CLI"
    },
    "opencode": {
        "cli_command": "opencode",
        "name": "OpenCode"
    }
}


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """🤖 Multi-Agent Collaboration CLI"""
    pass


@cli.command()
@click.option("--template", "-t", default="python", help="Language template (python, javascript)")
@click.option("--force", "-f", is_flag=True, help="Force overwrite existing .agents folder")
def init(template, force):
    """Initialize .agents folder structure"""
    agents_path = Path(AGENTS_DIR)
    
    if agents_path.exists() and not force:
        click.echo(click.style("⚠️  .agents folder already exists. Use --force to overwrite.", fg="yellow"))
        return
    
    click.echo("🚀 Initializing Multi-Agent Collaboration System...")
    
    # Clone template
    if agents_path.exists() and force:
        import shutil
        shutil.rmtree(agents_path)
    
    result = subprocess.run(
        ["git", "clone", TEMPLATE_REPO, AGENTS_DIR],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        # Fallback: create structure manually
        click.echo("📁 Creating folder structure...")
        create_structure_manually(template)
    else:
        # Remove .git from cloned repo
        git_dir = agents_path / ".git"
        if git_dir.exists():
            import shutil
            shutil.rmtree(git_dir)
    
    # Copy template to project.yaml
    template_file = agents_path / "templates" / f"{template}.yaml"
    project_file = agents_path / "project.yaml"
    
    if template_file.exists():
        import shutil
        shutil.copy(template_file, project_file)
        click.echo(f"📄 Created project.yaml from {template} template")
    
    # Auto-detect project info
    detect_and_update_project(project_file)
    
    click.echo(click.style("✅ Initialization complete!", fg="green"))
    click.echo("\n📋 Next steps:")
    click.echo("  1. Edit .agents/project.yaml with your project settings")
    click.echo("  2. Run: agents start")
    click.echo("  3. Give each agent the protocol instruction")


def create_structure_manually(template):
    """Create .agents structure without git clone"""
    dirs = [
        ".agents",
        ".agents/discussions",
        ".agents/workspace/claude",
        ".agents/workspace/gemini", 
        ".agents/workspace/opencode",
        ".agents/templates"
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    
    # Create minimal files
    Path(".agents/current_task.md").write_text("""---
id: null
title: null
status: idle
---

# No active task
""")
    
    Path(".agents/PROTOCOL.md").write_text("""# Multi-Agent Collaboration Protocol

See: https://github.com/loboking/agents-template
""")


def detect_and_update_project(project_file):
    """Auto-detect project settings"""
    if not project_file.exists():
        return
    
    cwd = Path.cwd()
    project_name = cwd.name
    
    # Detect language
    language = "python"
    if (cwd / "package.json").exists():
        language = "javascript"
    elif (cwd / "tsconfig.json").exists():
        language = "typescript"
    elif (cwd / "pyproject.toml").exists() or (cwd / "setup.py").exists():
        language = "python"
    
    click.echo(f"🔍 Detected: {project_name} ({language})")


@cli.command()
@click.argument("agents", nargs=-1)
@click.option("--tmux/--no-tmux", default=True, help="Use tmux for terminals (default: True)")
def start(agents, tmux):
    """Start agent terminals
    
    Examples:
        agents start              # Start all agents with tmux
        agents start claude       # Start only Claude
        agents start --no-tmux    # Use Terminal.app instead
    """
    if not agents:
        agents = list(DEFAULT_AGENTS.keys())
    
    click.echo(f"🚀 Starting agents: {', '.join(agents)}")
    
    # Check .agents folder exists
    if not Path(AGENTS_DIR).exists():
        click.echo(click.style("⚠️  .agents folder not found. Run 'agents init' first.", fg="yellow"))
        return
    
    if tmux:
        # Check if tmux is installed
        result = subprocess.run(["which", "tmux"], capture_output=True)
        if result.returncode != 0:
            click.echo("📦 tmux not found. Installing...")
            install_result = subprocess.run(["brew", "install", "tmux"], capture_output=False)
            if install_result.returncode != 0:
                click.echo(click.style("❌ Failed to install tmux. Please install manually: brew install tmux", fg="red"))
                return
            click.echo(click.style("✅ tmux installed!", fg="green"))
        start_with_tmux(agents)
    else:
        start_with_osascript(agents)


def start_with_osascript(agents):
    """Start terminals using macOS osascript (Terminal.app or iTerm)"""
    cwd = os.getcwd()
    
    for agent in agents:
        if agent not in DEFAULT_AGENTS:
            click.echo(f"⚠️  Unknown agent: {agent}")
            continue
        
        cmd = DEFAULT_AGENTS[agent]["cli_command"]
        name = DEFAULT_AGENTS[agent]["name"]
        
        # AppleScript to open new Terminal tab and run command
        script = f'''
        tell application "Terminal"
            activate
            do script "cd {cwd} && {cmd}"
        end tell
        '''
        
        try:
            subprocess.run(["osascript", "-e", script], check=True, capture_output=True)
            click.echo(f"  ✅ Started {name}")
        except subprocess.CalledProcessError:
            click.echo(f"  ❌ Failed to start {name}")


def start_with_tmux(agents):
    """Start terminals using tmux"""
    session_name = "agents"
    cwd = os.getcwd()
    
    # Create new tmux session
    subprocess.run(["tmux", "new-session", "-d", "-s", session_name], capture_output=True)
    
    for i, agent in enumerate(agents):
        if agent not in DEFAULT_AGENTS:
            continue
        
        cmd = DEFAULT_AGENTS[agent]["cli_command"]
        
        if i == 0:
            # First pane (already created)
            subprocess.run([
                "tmux", "send-keys", "-t", f"{session_name}:0",
                f"cd {cwd} && {cmd}", "Enter"
            ])
        else:
            # Create new pane
            subprocess.run(["tmux", "split-window", "-t", session_name, "-h"])
            subprocess.run([
                "tmux", "send-keys", "-t", session_name,
                f"cd {cwd} && {cmd}", "Enter"
            ])
    
    # Attach to session
    click.echo(f"\n📺 Attach to tmux session: tmux attach -t {session_name}")


@cli.command()
@click.argument("name")
@click.option("--command", "-c", help="CLI command to run")
@click.option("--model", "-m", help="Model name")
def add(name, command, model):
    """Add a new agent"""
    roles_file = Path(AGENTS_DIR) / "roles.yaml"
    
    if not roles_file.exists():
        click.echo(click.style("⚠️  roles.yaml not found. Run 'agents init' first.", fg="yellow"))
        return
    
    with open(roles_file, "r") as f:
        content = f.read()
        roles = yaml.safe_load(content)
    
    if "agents" not in roles:
        roles["agents"] = {}
    
    roles["agents"][name] = {
        "name": name.capitalize(),
        "model": model or "unknown",
        "cli_command": command or name,
        "capabilities": ["coding"]
    }
    
    with open(roles_file, "w") as f:
        yaml.dump(roles, f, allow_unicode=True, default_flow_style=False)
    
    # Create workspace
    workspace = Path(AGENTS_DIR) / "workspace" / name
    workspace.mkdir(parents=True, exist_ok=True)
    (workspace / "README.md").write_text(f"# {name.capitalize()} Workspace\n")
    
    click.echo(click.style(f"✅ Added agent: {name}", fg="green"))


@cli.command("list")
def list_agents():
    """List all registered agents"""
    roles_file = Path(AGENTS_DIR) / "roles.yaml"
    
    if not roles_file.exists():
        click.echo(click.style("⚠️  roles.yaml not found.", fg="yellow"))
        return
    
    with open(roles_file, "r") as f:
        roles = yaml.safe_load(f)
    
    agents = roles.get("agents", {})
    
    click.echo("\n🤖 Registered Agents:\n")
    for name, info in agents.items():
        capabilities = ", ".join(info.get("capabilities", [])[:3])
        click.echo(f"  {name}")
        click.echo(f"    Model: {info.get('model', 'N/A')}")
        click.echo(f"    Command: {info.get('cli_command', name)}")
        click.echo(f"    Capabilities: {capabilities}")
        click.echo()


@cli.group()
def task():
    """Task management commands"""
    pass


@task.command("status")
def task_status():
    """Show current task status"""
    task_file = Path(AGENTS_DIR) / "current_task.md"
    
    if not task_file.exists():
        click.echo(click.style("⚠️  current_task.md not found.", fg="yellow"))
        return
    
    content = task_file.read_text()
    
    # Parse YAML frontmatter
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                meta = yaml.safe_load(parts[1])
                click.echo("\n📋 Current Task:\n")
                click.echo(f"  ID: {meta.get('id', 'N/A')}")
                click.echo(f"  Title: {meta.get('title', 'N/A')}")
                click.echo(f"  Status: {meta.get('status', 'N/A')}")
                click.echo(f"  Pattern: {meta.get('pattern', 'N/A')}")
                return
            except:
                pass
    
    click.echo("No active task")


if __name__ == "__main__":
    cli()
