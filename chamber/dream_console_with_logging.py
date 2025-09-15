"""Dream Console with Logging and Q&A interface.

This module expands the previous DreamConsole architecture by adding
persistent logging and interactive question‑and‑answer capabilities.
Each breath cycle is recorded in an internal log that can be queried
and displayed. The Archivist now not only stores cycle data but can
render a summary of all recorded cycles and search logs for keywords.

Example usage:

    console = DreamConsole()
    console.breathe({"prompt": "hello"})
    console.breathe({"prompt": "world"})
    # display all cycle logs
    console.archivist.display_logs()
    # ask a question about the cycles
    answer = console.ask("What were the scenes created?")
    print(answer)

This example would log two cycles and then display a summary of the
logs and answer a user question by summarizing the scenes created.

Note: This is a conceptual prototype meant to illustrate how the
DreamConsole architecture could incorporate logging and interaction.
In a real implementation, you might replace the naive keyword search
with more sophisticated natural language processing.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Guardian:
    """Guardian oversees the perception–prediction–reflection cycle."""

    def filter(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        # Simple example: return the inputs as perception
        return {"signals": inputs}

    def process(self, perception: Dict[str, Any]) -> (Dict[str, Any], Dict[str, Any]):
        # Predict and compute error; here we pretend prediction matches perception
        prediction = {"predicted": perception["signals"]}
        error = {"delta": 0}  # no error in this simple example
        return prediction, error

    def reflect(self, error: Dict[str, Any]) -> Dict[str, Any]:
        # Reflection could adjust parameters; here we just return the negative delta
        return {"refinement": -error["delta"]}


@dataclass
class Archivist:
    """Archivist logs cycle data and supports queries over the logs."""

    logs: List[Dict[str, Any]] = field(default_factory=list)

    def log(self, cycle_id: int, perception: Dict[str, Any], creation: Dict[str, Any], error: Dict[str, Any], vibe: Dict[str, Any]) -> None:
        self.logs.append({
            "cycle": cycle_id,
            "perception": perception,
            "creation": creation,
            "error": error,
            "vibe": vibe,
        })

    def display_logs(self) -> None:
        """Display a summary of all logged cycles."""
        if not self.logs:
            print("No cycles have been logged yet.")
            return
        print("Cycle logs:")
        for entry in self.logs:
            cycle = entry["cycle"]
            creation = entry["creation"]
            print(f"- Cycle {cycle}: scene={creation.get('scene')}, glyph={creation.get('glyph')}")

    def search(self, keyword: str) -> List[Dict[str, Any]]:
        """Return all logs containing the keyword in any field."""
        results = []
        keyword_lower = keyword.lower()
        for entry in self.logs:
            for value in entry.values():
                # Flatten nested dictionaries by converting to string
                if isinstance(value, dict):
                    value_str = str(value)
                else:
                    value_str = str(value)
                if keyword_lower in value_str.lower():
                    results.append(entry)
                    break
        return results


@dataclass
class Fabricator:
    """Fabricator generates digital artifacts (scenes and glyphs)."""

    def create(self, prediction: Dict[str, Any], error: Dict[str, Any]) -> Dict[str, str]:
        # Generate simple mock outputs; use length of prediction as an index
        scene = f"Scene with content: {prediction['predicted']}"
        glyph = f"Glyph-{abs(hash(str(prediction))) % 10000}"
        return {"scene": scene, "glyph": glyph}


@dataclass
class Navigator:
    """Navigator explores the generated artifacts and feeds back data."""

    def explore(self, creation: Dict[str, Any]) -> Dict[str, str]:
        # Example exploration: echo back the scene name
        return {"echo": f"Explored {creation['scene']}"}


@dataclass
class Harmonizer:
    """Harmonizer aligns outputs and manages vibes."""

    def align(self, creation: Dict[str, Any], exploration: Dict[str, Any]) -> Dict[str, str]:
        # Example vibe: combine creation and exploration names
        return {"vibe": f"Vibe = {creation['scene']} + {exploration['echo']}"}


class DreamConsole:
    """DreamConsole orchestrates the breath cycles with logging and Q/A."""

    def __init__(self) -> None:
        self.guardian = Guardian()
        self.archivist = Archivist()
        self.fabricator = Fabricator()
        self.navigator = Navigator()
        self.harmonizer = Harmonizer()
        self.cycle_count = 0

    def breathe(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Run one cycle: inhale → process → exhale → explore → harmonize → log."""
        self.cycle_count += 1
        cycle_id = self.cycle_count

        # Inhale and perceive
        perception = self.guardian.filter(inputs)

        # Process (prediction + error)
        prediction, error = self.guardian.process(perception)

        # Exhale (create)
        creation = self.fabricator.create(prediction, error)

        # Explore
        exploration = self.navigator.explore(creation)

        # Harmonize
        vibe = self.harmonizer.align(creation, exploration)

        # Log the cycle
        self.archivist.log(cycle_id, perception, creation, error, vibe)

        # Reflection (we could optionally refine guardian)
        refinement = self.guardian.reflect(error)

        return {
            "cycle": cycle_id,
            "perception": perception,
            "prediction": prediction,
            "error": error,
            "creation": creation,
            "exploration": exploration,
            "vibe": vibe,
            "refinement": refinement,
        }

    def ask(self, question: str) -> str:
        """Respond to a user question by searching logs and summarizing matches."""
        # Simple heuristic: search by keyword extraction (split question into words and search logs)
        keywords = [word.strip("?!.,:;\"\' ").lower() for word in question.split() if len(word) > 3]
        matched_entries = []
        for keyword in keywords:
            results = self.archivist.search(keyword)
            matched_entries.extend(results)
        if not matched_entries:
            return "I couldn't find anything relevant in the logs."
        # Summarize matched entries; for simplicity, list scenes and glyphs
        summaries = []
        for entry in matched_entries:
            creation = entry.get("creation", {})
            summaries.append(f"Cycle {entry['cycle']}: scene={creation.get('scene')}, glyph={creation.get('glyph')}")
        # Remove duplicates
        summaries = list(dict.fromkeys(summaries))
        return "\n".join(summaries)


def demo() -> None:
    """Demonstration of logging and Q/A functionality."""
    console = DreamConsole()
    console.breathe({"prompt": "First cycle"})
    console.breathe({"prompt": "Second cycle"})
    console.archivist.display_logs()
    print("\nQuestion: What were the scenes created?")
    print("Answer:\n" + console.ask("What were the scenes created?"))


if __name__ == "__main__":
    demo()