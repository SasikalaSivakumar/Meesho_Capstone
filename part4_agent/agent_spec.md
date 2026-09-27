# Part 4 — Monitoring Agent Specification

## 4.1 — Agent Specification

### Goal

Keep Meesho category managers informed of any category whose month-on-month revenue moves beyond the 8% threshold, with a human approving every drafted message before it goes out.

### Tools

The agent uses these concrete functions from the earlier Parts:

- `validate_feed()` from Part 2 to validate the monthly revenue feed.
- `mom_growth()` from Part 2 to calculate month-on-month revenue change.
- `is_flagged()` from Part 2 to classify each growth result.
- Part 3's narrative prompt-pack template-fill logic to draft stakeholder messages.

### Memory / State

Between runs, the agent must retain the previous month's revenue for each category so that the next run can calculate month-on-month growth. The current and previous monthly revenue values come from the validated Part 1 revenue feed.

### Planner

The agent follows these ordered subtasks:

1. Load the monthly revenue feed and run `validate_feed`.
2. If the feed is invalid, Hard Stop and report errors.
3. If the feed is valid, compute `mom_growth` for every category against the previous month.
4. Run `is_flagged` on every category.
5. Sort flagged categories by `abs(mom_pct)` descending.
6. Draft a message using Part 3's prompt template for at most the top 3 flagged categories by magnitude.
7. Log any remaining flagged categories beyond the cap as `suppressed, review manually` without drafting a message for them.
7b. Separately, log any category whose `is_flagged` result is `escalate_exact_boundary` into `escalated_categories`, without drafting a message for it.
8. Emit one structured JSON object per run.

### Feedback Loop

Every drafted message is held for human approval before it is considered sent. The mock runner only drafts and holds messages; it does not send email or make any external network call.

### Input Guardrail

`validate_feed` must pass before any other agent processing runs. If validation fails, the agent must stop immediately.

### Action Guardrail

No message is ever automatically sent. Messages are only drafted and held for human approval.

### Output Guardrail

Every number in a drafted message must trace directly to a Part 1 or Part 2 value. No invented figures may appear.

### Success and Error Stopping Conditions

**Success:** Drafts are produced for flagged categories, or correctly zero drafts are produced if no category crosses the threshold, and every number in every draft is traceable to Part 1 or Part 2.

**Error:** If `validate_feed` returns `False`, the run is a Hard Stop. The validation errors must be surfaced and no MoM computation or message drafting is attempted.

## 4.1 — Given-When-Then Agent Specifications

### Specification 1 — April to May Ethnic Wear

**Given** April Ethnic Wear revenue is INR 104520.77 and May Ethnic Wear revenue is INR 185107.61,

**When** the monitoring agent computes the MoM growth and applies the 8% threshold,

**Then** the agent records 77.1% growth and classifies the category as `flagged`.

### Specification 2 — May to June Beauty & Personal Care

**Given** May Beauty & Personal Care revenue is INR 35542.11 and June Beauty & Personal Care revenue is INR 37559.07,

**When** the monitoring agent computes the MoM growth and applies the 8% threshold,

**Then** the agent records 5.67% growth and classifies the category as `not_flagged`.

### Specification 3 — Exact 8% Boundary

**Given** the previous revenue is 100000 and the current revenue is 108000,

**When** the monitoring agent computes the MoM growth and applies the 8% threshold,

**Then** the agent records exactly 8.0% growth and classifies the category as `escalate_exact_boundary`.

### Specification 4 — Corrupted Feed

**Given** the current-month feed contains a negative revenue, a missing category, and a missing revenue,

**When** the monitoring agent runs `validate_feed`,

**Then** the agent performs a Hard Stop and surfaces these validation errors:

- `line 3: negative revenue (-4200.0) for category=Western Wear`
- `line 4: missing category (month=July)`
- `line 6: missing revenue (category=Home & Kitchen)`

No MoM computation or message drafting is performed.