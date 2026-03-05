import typer
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from pathlib import Path

from graph.review_graph import review_graph
from graph.state import CodeReviewState
from utils.helpers import save_report
from config.settings import MAX_CODE_LENGTH

app = typer.Typer()
console = Console()

def run_review(code: str, save: bool = False) -> str:
    if len(code) > MAX_CODE_LENGTH:
        code = code[:MAX_CODE_LENGTH]

    initial_state: CodeReviewState = {
        "raw_code":         code,
        "language":         "",
        "style_issues":     [],
        "bug_issues":       [],
        "security_issues":  [],
        "fix_suggestions":  "",
        "final_report":     "",
        "error":            None,
    }

    console.print(Panel(
        "🚀 Running: Router → Style + Bug + Security → Fix → Report",
        title="[bold cyan]Code Review Assistant[/bold cyan]",
        border_style="cyan"
    ))

    result = review_graph.invoke(initial_state)
    report = result.get("final_report", "No report generated.")

    console.print(Panel(Markdown(report), title="[bold green]✅ Review Complete[/bold green]", border_style="green"))

    if save:
        filepath = save_report(report, result.get("language", "unknown"))
        console.print(f"\n💾 Report saved to: [bold]{filepath}[/bold]")

    return report

@app.command()
def main(
    file: str  = typer.Option(None,  "--file", "-f", help="Path to code file"),
    save: bool = typer.Option(False, "--save", "-s", help="Save report to output_reports/"),
):
    if file:
        path = Path(file)
        if not path.exists():
            console.print(f"[red]❌ File not found: {file}[/red]")
            raise typer.Exit(1)
        code = path.read_text(encoding="utf-8")
    else:
        console.print("[bold]Paste your code. Type END on a new line when done.[/bold]\n")
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        code = "\n".join(lines)
        if not code.strip():
            console.print("[red]❌ No code provided.[/red]")
            raise typer.Exit(1)

    run_review(code, save=save)

if __name__ == "__main__":
    app()