from datetime import datetime

HEADER = """# Crown of Tyme Codex
This document is auto-generated from manifests and scrolls.
"""

def generate_index():
    now = datetime.utcnow().isoformat()
    content = HEADER
    content += f"\n_Last generated: {now} UTC_\n\n"
    content += "## Contents\n"
    content += "- Manifest overview\n"
    content += "- Module index\n"
    content += "- Chronicle logs\n"
    return content

if __name__ == "__main__":
    print(generate_index())
