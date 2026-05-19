"""Main entry point for the contract review multi-agent pipeline."""
import argparse
import os

from rich.console import Console
from agents.supervisor import SupervisorAgent

console = Console()


def main():
    parser = argparse.ArgumentParser(
        description="Legal Contract Review Agent - Multi-Agent AI System"
    )
    parser.add_argument(
        "--contract", required=True, help="Path to contract PDF/DOCX file"
    )
    args = parser.parse_args()

    if not os.path.exists(args.contract):
        console.print(f"[red]File not found: {args.contract}[/]")
        return

    console.print(f"[bold blue]Starting contract review pipeline for: {args.contract}[/]")

    supervisor = SupervisorAgent()
    report = supervisor.run_pipeline(args.contract)

    console.print(f"[bold green]Pipeline finished. Report saved to: {report}[/]")


if __name__ == "__main__":
    main()
