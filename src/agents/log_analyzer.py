import sys
from pathlib import Path
import json
from datetime import datetime
from src.core import chat, pick_log_file

# Project paths
ROOT = Path(__file__).resolve().parents[2]
LOG_DIR = ROOT / "data" / "logs"
OUT_DIR = ROOT / "outputs" / "log_analyzer"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SYSTEM_PROMPT = """You are a senior DevOps engineer analyzing system logs.

Your task:
1. Identify all errors and warnings
2. Find patterns and root causes
3. Assess severity and impact
4. Provide actionable recommendations

First, provide detailed technical analysis in this format:
- Summary: Brief overview of issues found
- Critical Errors: List with timestamps
- Root Cause: What caused the issues
- Impact: Which systems/users affected
- Recommendations: Step-by-step fixes
- Prevention: How to avoid in future

Then, provide structured JSON summary. Start the JSON block with exactly:
```json
and end it with exactly:
```
Do not add any text between the JSON block markers.
Use this structure:
{
  "summary": "Brief one-line summary",
  "error_count": 5,
  "critical_errors": [
    {"timestamp": "2026-01-04 10:24:12", "message": "Payment timeout", "severity": "high"}
  ],
  "root_causes": ["Cause 1", "Cause 2"],
  "affected_systems": ["payment", "database", "api"],
  "recommendations": ["Fix 1", "Fix 2"],
  "severity": "high"
}

Finally, provide executive summary after exactly this marker on its own line:
---EXECUTIVE---
Write in simple, non-technical language:
- What happened (in plain English)
- Business impact (users affected, downtime)
- What we're doing to fix it
- When it will be resolved
Keep it brief (3-5 sentences). No technical jargon.

Be technical in analysis but simple in executive summary."""


def main():
    """Run the log analyzer agent."""

    # 0. Generate timestamp once — used for all output files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 1. Pick log file
    file_arg = sys.argv[1] if len(sys.argv) > 1 else None
    log_file = pick_log_file(file_arg, LOG_DIR)
    log_content = log_file.read_text(encoding="utf-8")

    print(f"📄 Analyzing: {log_file.name}")
    print(f"📏 Log size: {len(log_content)} characters")
    print(f"🕐 Run timestamp: {timestamp}")

    # 2. Build messages
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Analyze this log file:\n\n{log_content}"}
    ]

    # 3. Call LLM
    print("🤖 Running analysis...")
    response = chat(messages)

    # 4. Save raw response for debugging
    raw_file = OUT_DIR / f"{log_file.stem}_raw_{timestamp}.txt"
    raw_file.write_text(response, encoding="utf-8")
    print(f"📝 Raw output saved: {raw_file.relative_to(ROOT)}")

    # 5. Split response into 3 parts: text, JSON, executive
    text_report = response
    json_text = '{"error": "No JSON generated"}'
    exec_summary = "Executive summary not generated."

    # Extract JSON block
    if "```json" in response:
        parts = response.split("```json")
        text_report = parts[0].strip()
        remainder = parts[1]

        if "```" in remainder:
            json_block = remainder.split("```")[0].strip()
            json_text = json_block

            # Extract executive summary
            after_json = remainder.split("```", 1)[1]
            if "---EXECUTIVE---" in after_json:
                exec_parts = after_json.split("---EXECUTIVE---")
                exec_summary = exec_parts[1].strip()

    # 6. Save text report
    report_file = OUT_DIR / f"{log_file.stem}_analysis_{timestamp}.txt"
    report_file.write_text(text_report, encoding="utf-8")

    # 7. Save JSON
    json_file = OUT_DIR / f"{log_file.stem}_analysis_{timestamp}.json"
    try:
        json_data = json.loads(json_text)
        json_file.write_text(json.dumps(json_data, indent=2), encoding="utf-8")
        print(f"📊 JSON saved: {json_file.relative_to(ROOT)}")
    except json.JSONDecodeError as e:
        print(f"⚠️  JSON parsing failed: {e}")
        print(f"   Raw JSON text was: {json_text[:200]}")
        # Save raw json_text anyway for debugging
        json_file.write_text(json_text, encoding="utf-8")

    # 8. Save executive summary
    exec_file = OUT_DIR / f"{log_file.stem}_executive_{timestamp}.txt"
    exec_file.write_text(exec_summary, encoding="utf-8")

    print(f"✅ Analysis complete!")
    print(f"📝 Technical report : {report_file.relative_to(ROOT)}")
    print(f"📊 JSON report      : {json_file.relative_to(ROOT)}")
    print(f"👔 Executive summary: {exec_file.relative_to(ROOT)}")
    print(f"🗂  Raw output       : {raw_file.relative_to(ROOT)}")


if __name__ == "__main__":
    main()