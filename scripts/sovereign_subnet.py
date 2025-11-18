"""Generate the Sovereign Subnet architecture and Aurelius deployment assets."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.sovereign_subnet import generate_sovereign_subnet_outputs

DEFAULT_ARCHITECTURE = Path("chronicle/sovereign_subnet_architecture.json")
DEFAULT_GOVERNANCE = Path("chronicle/sovereign_subnet_governance.json")
DEFAULT_DEPLOY_SCRIPT = Path("manifest/aurelius_subnet_deploy.sh")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--architecture",
        type=Path,
        default=DEFAULT_ARCHITECTURE,
        help="Where to write the Sovereign Subnet architecture manifest.",
    )
    parser.add_argument(
        "--governance",
        type=Path,
        default=DEFAULT_GOVERNANCE,
        help="Where to write the governance binding manifest.",
    )
    parser.add_argument(
        "--deploy-script",
        type=Path,
        default=DEFAULT_DEPLOY_SCRIPT,
        help="Where to write the Aurelius Subnet deployment script.",
    )
    return parser.parse_args()


def main() -> Dict[str, Any]:
    args = parse_args()
    outputs = generate_sovereign_subnet_outputs(
        architecture_path=args.architecture,
        deployment_script_path=args.deploy_script,
        governance_path=args.governance,
    )
    print(json.dumps(outputs, indent=2))
    return outputs


if __name__ == "__main__":
    main()
