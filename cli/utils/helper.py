import sys
import os
import platform
import click
from importlib import import_module
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn, MofNCompleteColumn


def detect_terminal_type():
    """Detect the terminal type and return optimal configuration."""
    if platform.system() == "Windows":
        if "powershell" in os.environ.get("PSModulePath", "").lower():
            return "powershell"
        elif os.environ.get("WT_SESSION"):
            return "windows_terminal"
        elif os.environ.get("PROMPT"):
            return "cmd"
    term = os.environ.get("TERM", "").lower()
    if "xterm" in term or "screen" in term or "tmux" in term:
        return "unix_advanced"
    return "unix_basic"


def create_optimized_console(terminal_type):
    """Create console optimized for the detected terminal type."""
    if terminal_type == "powershell":
        return Console(
            force_terminal=True,
            legacy_windows=True,
            width=120,
            record=True,
            color_system="windows",
            no_color=True
        )
    elif terminal_type == "windows_terminal":
        return Console(
            force_terminal=True,
            width=120,
            record=True,
            color_system="truecolor"
        )
    else:
        return Console(
            force_terminal=True,
            record=True,
            color_system="auto"
        )


class AdaptiveProgressManager:
    """Cross-platform progress manager that adapts to terminal capabilities."""

    def __init__(self, total_steps, initial_description="Starting..."):
        self.terminal_type = detect_terminal_type()
        self.console = create_optimized_console(self.terminal_type)
        self.total_steps = total_steps
        self.current_step = 0
        self.use_rich_progress = self.terminal_type in ["unix_advanced", "unix_basic", "windows_terminal"]

        self.console.print(f"[dim]Detected terminal: {self.terminal_type}[/]")
        self.console.print(f"[dim]Using rich progress: {self.use_rich_progress}[/]")

        if self.use_rich_progress:
            self._setup_rich_progress(initial_description)
        else:
            self._setup_simple_progress()

    def _setup_rich_progress(self, initial_description):
        """Setup Rich progress bar for compatible terminals."""
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=self.console,
            refresh_per_second=20,
            transient=True,
            expand=True
        )
        self.progress.start()
        self.task = self.progress.add_task(initial_description, total=self.total_steps)

    def _setup_simple_progress(self):
        """Setup simple step-by-step progress for PowerShell."""
        self.console.print("[bold green]🚀 Starting SmartDoc Generation[/]")
        self.console.print()

    def update_step(self, description, advance=True):
        """Update progress with new step description."""
        if self.use_rich_progress:
            self.progress.update(self.task, description=description)
            if advance:
                self.progress.advance(self.task)
            self.progress.refresh()
        else:
            if advance:
                self.current_step += 1
            step_indicator = f"[bold cyan]Step {self.current_step}/{self.total_steps}:[/]"
            self.console.print(f"{step_indicator} {description}")

    def complete_step(self, success_message=None):
        """Mark current step as completed."""
        if not self.use_rich_progress:
            message = success_message or "✓ Completed"
            self.console.print(f"[green]{message}[/]")
            self.console.print()
        else:
            message = success_message or "✓ Completed"
            self.console.print(f"[green]{message}[/]")

    def error_step(self, error_message):
        """Mark current step as failed."""
        if self.use_rich_progress:
            self.progress.stop()
        self.console.print(f"[red]❌ {error_message}[/]")

    def finish(self, final_message="All steps completed successfully!"):
        """Finish progress tracking."""
        if self.use_rich_progress:
            self.progress.stop()
        self.console.print(f"[bold green]{final_message}[/]")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self, 'progress') and self.progress:
            self.progress.stop()
