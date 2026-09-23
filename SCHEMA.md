# Dashboard data schema

Send data in this shape and it drops straight into the dashboard. One sheet/tab per section, or one JSON file — either works.

Everything is plain text unless marked. Dates as `YYYY-MM-DD`. Leave a field blank rather than guessing.

---

## 1. Calendar

| Column | Required | Values / example |
| --- | --- | --- |
| `date` | yes | 2026-09-09 |
| `time` | yes | `09:30`, or `—` for all-day |
| `title` | yes | EPR programme management meeting |
| `meta` | no | Teams · programme leads |
| `cadence` | yes | Weekly / Monthly / One-off / Mission / Programme |
| `kind` | yes | `statutory` · `upcoming` · `conference` · `mission` |
| `hub` | no | Nairobi / Dakar / Brazzaville / RD office — blank = personal |
| `open_to_all` | no | yes / no — shows it on the cluster shared calendar |

## 2. Strategic documents

| Column | Required | Values / example |
| --- | --- | --- |
| `title` | yes | Q3 Emergency Response Performance Report |
| `type` | yes | Concept note / Report / Brief / Assessment |
| `origin` | yes | `Drafted by PAMS` or `Requested by RD` |
| `due` | yes | 2026-09-12 |
| `status` | yes | Not started / Drafting / In review / Cleared |
| `link` | no | Full SharePoint URL |
| `path` | no | SharePoint › EPR › Reports › Q3 |

## 3. Missions

| Column | Required | Values / example |
| --- | --- | --- |
| `place` | yes | Islamabad, Pakistan |
| `start` / `end` | yes | 2026-09-21 / 2026-09-24 |
| `purpose` | yes | Country office readiness assessment |
| `tr_approved` | yes | yes / no |
| `report_submitted` | yes | yes / no |
| `claim_submitted` | yes | yes / no |

A mission counts as closed only when all three are `yes`.

## 4. Conferences

| Column | Required | Values / example |
| --- | --- | --- |
| `title` | yes | Global Health Security Forum, Doha |
| `start` / `end` | yes | 2026-11-18 / 2026-11-18 |
| `role` | yes | Keynote speaker / Panellist / Attendee / Chair |
| `confirmed` | yes | yes / no |
| `abstract_sent` | yes | yes / no |
| `slides_ready` | yes | yes / no |
| `brief_read` | yes | yes / no |

## 5. Memos

| Column | Required | Values / example |
| --- | --- | --- |
| `origin` | yes | `CO` · `HQ` · `Internal` |
| `title` | yes | Pakistan CO — request for surge deployment support |
| `meta` | no | For clearance · 2 attachments |
| `date` | yes | 2026-09-08 |
| `link` | no | SharePoint or mail URL |

## 6. Inbox triage rules

Not a table — a short list from RED:

- **Categories** she wants mail sorted into (current set: Invitation to conference, Document to review, Decision to make, Needs response, For information).
- **Urgency rules** — e.g. "anything from the RD front office is urgent", "requests with a date inside 48 hours are urgent".
- **Reminder lead time** — 1 day before / 2 hours before / on the day.

## 7. Hubs

| Column | Required | Values / example |
| --- | --- | --- |
| `hub` | yes | Nairobi / Dakar / Brazzaville / RD office |
| `lead_text` | yes | Emergency operations · 22 staff |
| `activity_title` | yes | Horn of Africa cholera response — operational review |
| `activity_meta` | no | With WCO Kenya |
| `due` | yes | 2026-09-18 |
| `status` | yes | Not started / Drafting / In review / Cleared |

## 8. Directory

| Column | Required | Values / example |
| --- | --- | --- |
| `name` | yes | Dr Chamla |
| `role` | yes | Director, EPR |
| `hub` | no | Brazzaville |
| `mutual_access` | yes | yes / no |

---

## 9. Dashboard extras (`data.json` only)

These keys sit alongside the sections above in `data.json`. They hold content the dashboard needs that the schema does not cover yet. Every key is optional; leave one out and its panel shows empty.

### Fields added to the sections above

| Section | Extra field | Values / example |
| --- | --- | --- |
| Calendar | `id` | `c1` — any unique text |
| Calendar | `duration` | minutes, e.g. `90` (default 60) |
| Documents, memos | `topic` | `q3` — links items that are about the same thing (see `topics`) |
| Missions, conferences | `id` | `isl` — any unique text |
| Memos | `action` | `sign` (needs your signature or clearance) or `read` |
| Hubs | `open_missions`, `missions_note` | `3`, `2 awaiting expense claims` |
| Hubs | `meetings_this_week`, `meetings_note` | `6`, `2 open to other hubs` |
| Hubs | `extra_stat` | `{ "label": "Graded emergencies", "value": 2, "unit": "active", "note": "Cholera" }` |
| Hubs | `people` | `[{ "name": "Hub lead", "role": "Missions and surge" }]` |
| Hubs | `pending` | Text shown while the hub calendar is awaited |
| Hub activities | `due` | a date, or `today` |

### New keys

| Key | What it holds |
| --- | --- |
| `owner` | Name shown in the greeting, e.g. `RED` |
| `recurring` | Statutory series: `weekday` (`Tuesday`), `week` (`every`, `1`–`4` or `last`), `time`, `duration`, `title`, `meta`, `cadence`, `kind` |
| `mails` | Inbox until the mailbox is connected: `id`, `topic`, `short`, `category` (one of the triage categories), `action`, `urgent`, `subject`, `sender`, `received` (date-time) or `received_hours_ago`, `responded`, `summary`, `attachment` |
| `requests` | Ad-hoc asks: `id`, `topic`, `from`, `title`, `urgency` (`Today`, `This week`, `No date`), `received` or `received_hours_ago` |
| `todos` | Daily to-do: `id`, `topic`, `text`, `kind`, `due` (date-time) or `due_in_hours`, `done` |
| `topics` | `{ "q3": "Q3 performance report — clear section 4" }` — the title shown when several items share a topic |
| `shared_files` | `title`, `owner`, `updated` (date), `scope` |
| `setup` | Setup checklist: `name`, `status` (`Awaiting`, `Partial`, `Setup session`, `Confirmed`), `need` (`{owner}` is replaced by the owner's name), `target` |
| `monthly_report` | `stats` (`value`, `label`) and `sections` (`title`, `page`, `lines`) until the activity log arrives |

`received_hours_ago` and `due_in_hours` place sample items relative to the moment the page opens, so a demo stays current. Real exports should use `received` / `due` date-times such as `2026-09-23T14:00`.

---

## Easiest way to send it

1. One Excel workbook, one tab per section above, headers exactly as written — **or**
2. `data.json` in this repo, filled in following the same field names.

Send either to the repo (Add file → Upload files) or by mail. No formatting or tidying needed — raw exports are fine.
