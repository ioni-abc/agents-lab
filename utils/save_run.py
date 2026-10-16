from datetime import datetime
from pathlib import Path

from anthropic.types import Message

RUNS_DIR = Path(__file__).resolve().parent.parent / "runs"


def save_run(stage: str, prompt: str, response: Message) -> None:
    RUNS_DIR.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base = RUNS_DIR / f"{stage}_{stamp}"

    # Exact API response, for reference
    json_path = Path(f"{base}.json")
    json_path.write_text(response.model_dump_json(indent=2), encoding="utf-8")

    # Readable version with space for notes
    usage = response.usage
    details = getattr(usage, "output_tokens_details", None)
    thinking_tokens = getattr(details, "thinking_tokens", 0) if details else 0

    lines = [
        f"# {stage} — {stamp}",
        "",
        f"- model: {response.model}",
        f"- stop_reason: {response.stop_reason}",
        f"- tokens: input={usage.input_tokens}, output={usage.output_tokens} "
        f"(of which thinking={thinking_tokens})",
        "",
        "## Prompt",
        prompt,
        "",
    ]
    for block in response.content:
        if block.type == "thinking":
            lines += ["## Thinking", block.thinking or "(thinking happened, text not returned)", ""]
        elif block.type == "text":
            lines += ["## Answer", block.text, ""]
    lines += ["## My notes", "- ", ""]

    md_path = Path(f"{base}.md")
    md_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"Saved: {md_path}\n       {json_path}")