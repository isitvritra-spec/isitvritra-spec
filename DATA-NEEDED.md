# Data needed to populate the dashboard

Everything below is already wired into the interface. Each input replaces sample content in the place named.

| Input | Status | What is needed | Lands in |
| --- | --- | --- | --- |
| **Calendars** | Awaiting | Outlook export for RED, plus the statutory meeting series for each hub | Calendar · shared calendar |
| **Activity log** | Awaiting | Meetings attended, documents drafted and missions taken since January — seeds the monthly report | Activity report drawer |
| **Document library** | Partial | SharePoint folder paths for concept notes, reports and memos, so titles link straight through | Strategic documents |
| **Missions & conferences** | Awaiting | Mission list with TR / report / expense-claim status; conference invitations with RED's role in each | Missions · Conferences |
| **Mailbox connection** | Setup session | Remote session to connect the mailbox and set triage categories and urgency rules | Inbox · read for you |
| **Colour scheme** | Confirmed | WHO blue ground; pink statutory, green upcoming, mandarin conference, purple mission, mandarin-to-red ageing | Whole dashboard |

## Where content lives in the source

Open `source/EPR Command Dashboard v3 WHO blue.dc.html` and find these tables in the `<script>` block:

- `EVENTS` — calendar entries by day of month
- `DOCS` — strategic documents table
- `MAILS` — inbox items, their category and AI summary
- `HUB_DETAIL` — Nairobi, Dakar, Brazzaville and RD office drill-downs
- `state.todos` — the daily to-do list
- `missionSpec` / `confSpec` — mission and conference follow-up tracking

## Open questions

1. Report format — is the three-page monthly summary the right length, and who else receives it?
2. Which colleagues get mutual dashboard access in the directory?
3. Should the hub views be editable by hub leads, or read-only to everyone but them?
