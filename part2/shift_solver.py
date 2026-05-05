from __future__ import annotations

import argparse
from collections import Counter, deque
from copy import deepcopy
from pathlib import Path


class Shift_Solver:
""" Days, shifts and max number of shifts """
    DAYS = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    SHIFTS = ["Morning", "Afternoon", "Night"]
    MAX_SHIFTS_PER_NURSE = 5

    def __init__(self, staff_file:str|Path):
        self.staff_file = Path(staff_file)
        self.staff_leaves = self._load_staff(self.staff_file)
        self.nurses = sorted(self.staff_leaves.keys())
        self.variables = [
            f"{day}_{shift}" for day in self.DAYS for shift in self.SHIFTS
        ]
        self.domains = {variable: set(self.nurses) for variable in self.variables}
        self.neighbors = {variable: set() for variable in self.variables}
        self._build_neighbors()

    def _load_staff(self, staff_file: Path) -> dict[str, set[int]]:
        staff_leaves: dict[str, set[int]] = {}

        for raw_line in staff_file.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line:
                continue
        
        parts = [part.strip() for part in line.split(",")]
        nurse = parts[0]
        leave_days = {
            int(day)
            for day in parts[1:]
            if day and day != "0"
        }
        staff_leaves[nurse] = leave_days
        
        return staff_leaves

    def _build_neighbors(self) -> None:
        for day_index in range(len(self.DAYS) - 1):
            night_var = f"{self.DAYS[day_index]}_Night"
            morning_var = f"{self.DAYS[day_index + 1]}_Morning"
            self.neighbors[night_var].add(morning_var)
            self.neighbors[morning_var].add(night_var)
    def _parse_variable(self, variable: str) -> tuple[int, str]:
        day_name, shift_name = variable.split("_", 1)
        return self.DAYS.index(day_name) + 1, shift_name
    def _violates_rest_constraint(self, variable_x: str, nurse_x: str, variable_y: str, nurse_y: str)-> bool:
        if nurse_x != nurse_y:
            return False

        day_x, shift_x = self._parse_variable(variable_x)
        day_y, shift_y = self._parse_variable(variable_y)

        return (
            shift_x == "Night"
            and shift_y == "Morning"
            and day_y == day_x + 1
        ) or (
            shift_y == "Night"
            and shift_x == "Morning"
            and day_x == day_y + 1
        )
    def enforce_node_consistency(self) -> None:
        """
        Remove nurses from a shift's domain if they are on leave that day.
        """
        for variable in self.variables:
            day_number, _ = self._parse_variable(variable)
            self.domains[variable] = {
            nurse
            for nurse in self.domains[variable]
            if day_number not in self.staff_leaves[nurse]
            }
    def revise(self, x: str, y: str) -> bool:
        
        if y not in self.neighbors[x]:
            return False

        revised = False
        removable: set[str] = set()
    def ac3(self, arcs: list[tuple[str, str]] | None = None) -> bool:
    def assignment_complete(self, assignment: dict[str, str]) -> bool:
    def consistent(self, assignment: dict[str, str]) -> bool:
    def select_unassigned_variable(self, assignment: dict[str, str]) -> str:
    def order_domain_values(self, variable: str, assignment: dict[str, str]) -> list[str]:
    def _forward_check(self, variable: str, nurse: str, assignment: dict[str, str]) -> bool:
        """
        Prune domains after an assignment.

        1. Remove the same nurse from the next morning / previous night if rest is violated.
        2. If a nurse reaches the 5-shift cap, remove them from all other unassigned domains.
        """
        for neighbor in self.neighbors[variable]:
            if neighbor in assignment:
                continue
            if nurse in self.domains[neighbor] and self._violates_rest_constraint(
                variable, nurse, neighbor, nurse
        ):
                self.domains[neighbor].remove(nurse)
                if not self.domains[neighbor]:
                    return False
                
                counts = Counter(assignment.values())
                if counts[nurse] >= self.MAX_SHIFTS_PER_NURSE:
                    for other in self.variables:
                        if other in assignment:
                            continue
                        if nurse in self.domains[other]:
                            self.domains[other].remove(nurse)
                            if not self.domains[other]:
                                return False
        
            return True
        
    def backtrack(self, assignment: dict[str, str]) -> dict[str, str] | None:
        if self.assignment_complete(assignment):
            return assignment

        variable = self.select_unassigned_variable(assignment)

        for nurse in self.order_domain_values(variable, assignment):
            local_assignment = dict(assignment)
            local_assignment[variable] = nurse

            if not self.consistent(local_assignment):
                continue

        saved_domains = deepcopy(self.domains)
        self.domains[variable] = {nurse}

        if self._forward_check(variable, nurse, local_assignment):
            neighbor_arcs = [(neighbor, variable) for neighbor in self.neighbors[variable]]
            if self.ac3(neighbor_arcs):
                result = self.backtrack(local_assignment)
                if result is not None:
                    return result
        self.domains = saved_domains
        
    return None

    def solve(self) -> dict[str, str] | None:
    def format_schedule(self, assignment: dict[str, str]) -> str:
    def main() -> None:

