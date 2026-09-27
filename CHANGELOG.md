# Change history

## 0.1.3 — beta

- Read recent turns from the document end instead of rejecting histories above 250,000 characters.
- Resume parsing at later author headings after editable regions in older messages.
- Carry accessible heading identities through parsing so rolling windows can recognise new turns.
- Refresh the current text for manual repeat and clear stale output on missing/currently unanswered messages or provider errors.
- Retain up to eight separate contexts across focus changes; announce newly detected answers after returning to a previously observed conversation.
- Rewrite the root README and all five user manuals. Separate development details and test records.
- Update the manifest homepage/description and minimum NVDA version to 2026.2. Keep the internal add-on ID for upgrades.
- Use named gettext translation entries instead of position-based lists.

## 0.1.2

Optional interface-footer filtering, improved historical replay protection and a three-second silence fallback for new installations.

## 0.1.1

Prevent repeated sent-message announcements and confirmations during page updates.

## 0.1.0

Initial experimental release.
