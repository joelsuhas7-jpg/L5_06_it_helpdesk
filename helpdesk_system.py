"""IT Helpdesk Ticket Allocator for Lab 5 static analysis."""

import json
import os
import platform
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

tickets: dict[int, dict[str, Any]] = {}
ticket_counter = 100
ADMIN_PASSWORD_ENV = "HELPDESK_ADMIN_PASSWORD"


def _validated_ticket_id(ticket_id: int) -> dict[str, Any]:
    """Return a ticket or raise ValueError when it does not exist."""
    if ticket_id not in tickets:
        raise ValueError(f"Ticket #{ticket_id} does not exist.")
    return tickets[ticket_id]


def _validated_urgency(urgency: int | str) -> int:
    """Convert urgency to an integer and enforce the supported 1–5 range."""
    try:
        priority = int(urgency)
    except (TypeError, ValueError) as exc:
        raise ValueError("Urgency must be an integer from 1 to 5.") from exc
    if not 1 <= priority <= 5:
        raise ValueError("Urgency must be between 1 and 5.")
    return priority


def raise_ticket(
    user: str,
    issue_type: str,
    urgency: int | str = 3,
    audit_trail: list[str] | None = None,
) -> int:
    """Create a helpdesk ticket and optionally record its audit event."""
    global ticket_counter

    if not user.strip() or not issue_type.strip():
        raise ValueError("User and issue type must not be empty.")

    priority = _validated_urgency(urgency)
    ticket_counter += 1
    tickets[ticket_counter] = {
        "user": user.strip(),
        "issue": issue_type.strip(),
        "priority": priority,
        "tech": None,
        "notes": [],
    }

    if audit_trail is not None:
        audit_trail.append(
            f"{user.strip()} raised #{ticket_counter} at "
            f"{datetime.now().isoformat(timespec='seconds')}"
        )
    return ticket_counter


def assign_ticket(ticket_id: int, technician: str) -> None:
    """Assign a ticket to a named technician."""
    ticket = _validated_ticket_id(ticket_id)
    if not technician.strip():
        raise ValueError("Technician name must not be empty.")
    ticket["tech"] = technician.strip()


def add_note(ticket_id: int, note: str) -> None:
    """Add a note to an existing ticket."""
    ticket = _validated_ticket_id(ticket_id)
    if not note.strip():
        raise ValueError("Note must not be empty.")
    ticket["notes"].append(note.strip())


def close_ticket(ticket_id: int, password: str) -> bool:
    """Close a ticket only when the configured administrator password matches."""
    expected_password = os.environ.get(ADMIN_PASSWORD_ENV)
    if not expected_password:
        raise RuntimeError(
            f"Set the {ADMIN_PASSWORD_ENV} environment variable before closing tickets."
        )
    if password != expected_password:
        return False
    _validated_ticket_id(ticket_id)
    del tickets[ticket_id]
    return True


def unresolved_high_priority() -> list[int]:
    """Return unassigned tickets with priority 4 or 5."""
    return [
        ticket_id
        for ticket_id, ticket in tickets.items()
        if ticket["priority"] >= 4 and ticket["tech"] is None
    ]


def ping_user_machine(hostname: str) -> int:
    """Ping a validated hostname/IP without invoking a command shell."""
    if not isinstance(hostname, str) or not hostname.strip():
        raise ValueError("Hostname must not be empty.")

    hostname = hostname.strip()
    # Accept ordinary hostnames and IPv4-style strings; reject shell metacharacters.
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9.-]{0,252}", hostname):
        raise ValueError("Hostname contains invalid characters.")

    ping_flag = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        completed = subprocess.run(
            ["ping", ping_flag, "1", hostname],
            check=False,
            shell=False,
            timeout=5,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise RuntimeError(f"Unable to ping {hostname}: {exc}") from exc
    return completed.returncode


def save_tickets(file: str | Path = "tickets.json") -> None:
    """Save tickets as JSON using a context manager."""
    destination = Path(file)
    serializable_tickets = {str(key): value for key, value in tickets.items()}
    try:
        with destination.open("w", encoding="utf-8") as output_file:
            json.dump(serializable_tickets, output_file, indent=2)
            output_file.write("\n")
    except OSError as exc:
        raise OSError(f"Could not save tickets to {destination}: {exc}") from exc


def main() -> None:
    """Run a short demonstration of the ticket allocator."""
    ticket_one = raise_ticket("anil", "printer", 5)
    ticket_two = raise_ticket("meera", "wifi", 4)
    ticket_three = raise_ticket("joe", "vpn", 2)

    assign_ticket(ticket_one, "Tech-Kiran")
    add_note(ticket_one, "Called user")

    print("Unassigned high priority:", unresolved_high_priority())
    level = input("Urgency for a new laptop ticket (1-5, Enter for 3): ").strip() or "3"

    try:
        raise_ticket("sana", "laptop", level)
    except ValueError as exc:
        print(f"Ticket not created: {exc}")

    admin_password = os.environ.get(ADMIN_PASSWORD_ENV, "")
    if admin_password:
        close_ticket(ticket_three, admin_password)
    else:
        print(f"Ticket #{ticket_three} left open: configure {ADMIN_PASSWORD_ENV} to enable closing.")

    save_tickets()
    print("Open tickets:", list(tickets.keys()))


if __name__ == "__main__":
    main()
