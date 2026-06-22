from collections import Counter
from pathlib import Path

from src.core.base.io.writer import BaseResultWriter
from src.core.schemas import RequestAnalysis


class MarkdownResultWriter(BaseResultWriter):
    """Writes a Markdown summary report of classification results."""

    def __init__(self, file_path: str) -> None:
        self._file_path = file_path

    def write(self, results: list[RequestAnalysis]) -> None:
        """Generate and write the Markdown report to the configured file path."""
        result_md = self._generate(results=results)

        path = Path(self._file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(result_md, encoding="utf-8")

    def _generate(self, results: list[RequestAnalysis]) -> str:
        """Build the full Markdown report content from results."""
        lines = ["# Classification Report\n"]

        lines.append("## By Category")
        for cat, count in sorted(Counter(r.category for r in results if r.category).items()):
            lines.append(f"- {cat}: {count}")

        lines.append("\n## By Priority")
        for pri in ["high", "medium", "low"]:
            lines.append(f"- {pri}: {sum(1 for r in results if r.priority == pri)}")

        lines.append("\n## By Department")
        dept_counts = Counter(r.target_department for r in results if r.target_department)
        for dept, count in sorted(dept_counts.items()):
            lines.append(f"- {dept}: {count}")
        if not dept_counts:
            lines.append("- (none identified)")

        clarifications = [r for r in results if r.needs_clarification]
        lines.append(f"\n## Needs Clarification ({len(clarifications)})")
        for r in clarifications:
            lines.append(f"- **{r.source.id}**: {r.short_summary or '—'}")
            lines.append(f"  > [{r.source.channel}] {r.source.raw_text}")

        errors = [r for r in results if r.error]
        if errors:
            lines.append(f"\n## Parse Errors ({len(errors)})")
            for r in errors:
                lines.append(f"- **{r.source.id}**: {r.error}")

        return "\n".join(lines)
