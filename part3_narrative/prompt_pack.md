# Reusable Prompt Pack — Flagged Category Narrative

## Trigger

Start this prompt when a category's `is_flagged` result is `"flagged"`.

## Input list

The prompt requires these placeholder variables:

- `{category}` — category name
- `{previous_revenue}` — revenue for the previous month
- `{current_revenue}` — revenue for the current month
- `{mom_pct}` — month-over-month growth percentage
- `{month}` — current month
- `{prev_month}` — previous month

## Prompt

Write a concise stakeholder update for a regional manager about the flagged category using the Context → Insight → Implication structure.

Use these supplied values:
- Category: [{category}]
- Previous month: [{prev_month}]
- Current month: [{month}]
- Previous revenue: [{previous_revenue}]
- Current revenue: [{current_revenue}]
- MoM percentage: [{mom_pct}]

Rules:
1. In Context, state what is being measured and the comparison period.
2. In Insight, state the supplied MoM result and label it explicitly as a fact.
3. In Implication, give one specific and actionable next step.
4. If a possible cause is suggested, label it explicitly as a hypothesis because the supplied data does not prove causation.
5. Never state a number that is not one of the supplied placeholder values.
6. Do not invent additional metrics, causes, reseller names, or business facts.

## Checklist

Before using the narrative, verify:

- [ ] Every number in the draft exactly matches a supplied placeholder value.
- [ ] The comparison names both `{month}` and `{prev_month}` correctly.
- [ ] The Insight is explicitly labeled as a fact.
- [ ] Any proposed cause is explicitly labeled as a hypothesis.
- [ ] The recommendation is specific and actionable rather than vague.
- [ ] Any reseller referenced in an external-facing narrative is identified only by coded alias, never by raw reseller name.