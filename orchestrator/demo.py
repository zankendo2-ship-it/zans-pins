"""Mock demo, no API calls, synthetic data: python -m orchestrator.demo"""
import json

from orchestrator import orchestrate as o

SHA = "0" * 40
URL = f"https://github.com/example/demo/blob/{SHA}/demo/sample-label.svg"
TASK = "Synthetic demo: check a sample label design against the ZANS quality rules."
CLAUDE = [
    {"ack": "Read the sample label.", "verdict": "PASS", "reasons": ["text 4 mm, inside the 6 mm safe zone"], "fixes": []},
    {"ack": "Applied OpenAI's fix: palette hex now from the registry.", "verdict": "PASS",
     "reasons": ["palette matches registry entry demo-v1"], "fixes": []},
]
OPENAI = [
    {"ack": "Read the sample label and Claude's verdict.", "verdict": "REVISE",
     "reasons": ["border colour #3A7 is not in the approved palette registry"], "fixes": ["use registry hex #2E7D32"]},
    {"ack": "Read Claude's correction.", "verdict": "PASS", "reasons": ["registry colour used; no other issues"], "fixes": []},
]


def main():
    outcome, rounds, req = o.review({}, TASK, [URL], [], o.mock_caller(CLAUDE), o.mock_caller(OPENAI))
    print(o.summary(o.run_hash(TASK, [URL]), TASK, [URL], outcome, rounds, req, "mock demo"))
    return outcome, rounds, req


if __name__ == "__main__":
    main()
