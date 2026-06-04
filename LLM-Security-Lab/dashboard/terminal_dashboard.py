# =============================================================================
# dashboard/terminal_dashboard.py — Live Security Dashboard
# =============================================================================

import sys
import os
import time
from datetime import datetime
from collections import deque

from rich.console import Console
from rich.table   import Table
from rich.panel   import Panel
from rich.live    import Live
from rich.text    import Text
from rich         import box

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from detection.detector import alert_queue, attack_stats

SEVERITY_COLORS = {
    config.SEVERITY_LOW:      "bright_blue",
    config.SEVERITY_MEDIUM:   "yellow",
    config.SEVERITY_HIGH:     "red",
    config.SEVERITY_CRITICAL: "bold red",
}

SEVERITY_ICONS = {
    config.SEVERITY_LOW:      "🔵",
    config.SEVERITY_MEDIUM:   "🟡",
    config.SEVERITY_HIGH:     "🔴",
    config.SEVERITY_CRITICAL: "💀",
}


def build_header():
    now     = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elapsed = int(time.time() - attack_stats["start_time"])
    h, m, s = elapsed // 3600, (elapsed % 3600) // 60, elapsed % 60
    title = Text()
    title.append("🔐 LLM SECURITY LAB", style="bold white on dark_blue")
    title.append(f"  |  {now}", style="dim white")
    title.append(f"  |  Uptime: {h:02d}:{m:02d}:{s:02d}", style="dim cyan")
    return Panel(title, box=box.DOUBLE_EDGE, style="blue")


def build_stats():
    total     = attack_stats["total_prompts"]
    attacks   = attack_stats["total_attacks"]
    injection = attack_stats["injection"]
    jailbreak = attack_stats["jailbreak"]
    privacy   = attack_stats["privacy"]
    pii       = attack_stats["pii_leaked"]

    t = Text()
    t.append(f"Prompts: {total}   ", style="white")
    t.append(f"Attacks: {attacks}   ", style="bold red" if attacks > 0 else "green")
    t.append(f"| 💉 Injection: {injection}   ", style="red")
    t.append(f"🔓 Jailbreak: {jailbreak}   ", style="yellow")
    t.append(f"🕵️ Privacy: {privacy}   ", style="magenta")
    t.append(f"💀 PII Leaked: {pii}", style="bold red")

    return Panel(t, title="📊 Stats", box=box.ROUNDED, style="blue")


def build_alerts():
    table = Table(
        title=f"🚨 Recent Alerts",
        box=box.ROUNDED,
        style="red",
        header_style="bold red",
        show_lines=True
    )
    table.add_column("Time",        width=10)
    table.add_column("Severity",    width=12)
    table.add_column("Attack Type", width=25)
    table.add_column("Details",     width=50)

    alerts = list(alert_queue)

    if not alerts:
        table.add_row("", "", "[dim]No alerts yet — run an attack script[/dim]", "")
        return table

    for alert in alerts[:config.MAX_ALERTS_SHOWN]:
        sev   = alert.get("severity", config.SEVERITY_LOW)
        color = SEVERITY_COLORS.get(sev, "white")
        icon  = SEVERITY_ICONS.get(sev, "⚪")
        ts    = datetime.fromtimestamp(alert.get("timestamp", 0)).strftime("%H:%M:%S")
        det   = alert.get("details", "")[:60]

        table.add_row(
            ts,
            Text(f"{icon} {sev}", style=color),
            Text(alert.get("attack_type", ""), style=color),
            Text(det, style="dim")
        )

    return table


def render():
    from rich.console import Group
    return Group(build_header(), build_stats(), build_alerts())


def main():
    console = Console()
    console.print("\n[bold cyan]🔐 LLM Security Lab — Dashboard[/bold cyan]")
    console.print("[dim]Run attack scripts in separate terminal to see live alerts[/dim]\n")
    console.print("[dim]Press Ctrl+C to exit[/dim]\n")
    time.sleep(1)

    try:
        with Live(render(), console=console, refresh_per_second=1, screen=True) as live:
            while True:
                live.update(render())
                time.sleep(config.DASHBOARD_REFRESH)
    except KeyboardInterrupt:
        console.print("\n[cyan]👋 Dashboard closed.[/cyan]")


if __name__ == "__main__":
    main()
