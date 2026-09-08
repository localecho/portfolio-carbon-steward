"""What a committee gives the agent once: who they are, what they hold, how much."""
from __future__ import annotations

from dataclasses import dataclass, field

import yaml


@dataclass
class PortfolioProfile:
    name: str                 # e.g. "Maple Street Community Foundation"
    org_type: str             # e.g. "community foundation", "PTA reserve fund", "congregation endowment", "401(k) committee"
    holdings_text: str        # pasted statement / ticker list / sentence; parsed by the agent
    amount_usd: float | None = None   # total dollars; None if the holdings_text is in dollars
    share_link: str | None = None     # optional: a carbon-footprint-calc share link instead of holdings_text
    scope3: bool = False              # False = Scope 1+2 like-for-like (default)
    max_shift_points: float = 10      # largest reallocation the committee would consider, in points
    who_decides: str = ""             # e.g. "5-person volunteer finance committee, meets quarterly"
    notes: str = ""

    @classmethod
    def from_yaml(cls, path: str) -> "PortfolioProfile":
        with open(path) as f:
            data = yaml.safe_load(f)
        return cls(**data)

    def as_prompt_block(self) -> str:
        lines = [f"Organization: {self.name}", f"Type: {self.org_type}"]
        if self.who_decides:
            lines.append(f"Who decides: {self.who_decides}")
        if self.share_link:
            lines.append(f"Calculator share link: {self.share_link}")
        lines.append("Holdings as pasted by the treasurer:\n" + self.holdings_text.strip())
        if self.amount_usd:
            lines.append(f"Total amount: ${self.amount_usd:,.0f}")
        lines.append(f"Scope basis requested: {'Scope 1+2 + estimated Scope 3' if self.scope3 else 'Scope 1+2'}")
        lines.append(f"Largest reallocation the committee would consider: {self.max_shift_points} points")
        if self.notes:
            lines.append(f"Notes: {self.notes}")
        return "\n".join(lines)
