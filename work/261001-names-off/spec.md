# Spec

Status: approved by Ty 01/10, by shipping this PR in chat after choosing "Addresses only".

- `data/panels/ctrl.json`: the run identity becomes "tài khoản OMNI"; the three mailboxes become "3 hộp thư DB Group"; each sender handle becomes "DB Group"; the person assigned the payment procedure on 18/09 becomes "đầu mối OMNI" (review #14).
- `data/panels/exec.json`: each sender handle becomes "DB Group"; the parenthetical naming the two most recent senders reads "(mới nhất 24/09 và 23/09, đều từ DB Group)". No figure changes.
- `README.md`: the escalation row keeps the sender domain only; the section under the table says the page carries no email address, mailbox or account handle. Given names in timelines and approval chains stay as the decision record (Ty's answer, 01/10: "Addresses only").
- The routine prompt keeps the addresses (it needs them to search, and it is private); the README rule governs what it writes.
- Git history keeps the old text (same as the site-check pages, Ty 01/10).
- Promise: no account handle or email address of a person in any tracked file, this spec included (checked with a search for any word followed by an at-sign); `tools/validate-panels.py` passes; after merge the live panels hold none.
