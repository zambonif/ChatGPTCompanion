# ChatGPT Companion — 0.1.2 experimental
Author: Fernando de Paula Zamboni.

Build: `python build.py` (Python 3.11 or newer, no third-party dependencies).
Test: `python -m unittest discover -s tests -v`.
Windows shortcut: run `BUILD.cmd`. Output: dist/fzChatGPTCompanion-0.1.2.nvda-addon.

The installable archive contains manifest.ini at its root, not inside an extra folder.
Root metadata and source identifiers are English. English is the fallback UI language.
Translations include pt_BR, es, fr and it (.po and compiled .mo); docs include all five
languages as accessible HTML and UTF-8 text. Build source is under docs/ and translations/.
UI translations are ordered according to the sorted gettext strings extracted by build.py;
when adding strings, update all language lists. Generated PO files are included for review.

Licence: GPL-2.0-or-later (see LICENSE-NOTICE.txt and addon/COPYING.txt).
No network dependencies, installer hooks, telemetry, clipboard access or browser extension.
Only foreground conversations are monitored. Global plug-in is disabled on secure screens.

## Changes in 0.1.2
New enabled-by-default ignoreInterface setting filters only known disclaimer + latest-response suffix pairs, before both Tracker processing and manual repeat. This is a textual heuristic, not a semantic guarantee: identical literal blocks at answer end can also match; the option is reversible. No global phrase replacement. Completed answer fingerprints and ignoring answers before the latest user turn reduce historical replays. Existing preferences remain untouched; the default silence fallback for new profiles is now 3 seconds.

## Changes in 0.1.1
Sent-message announcements are keyed to newly observed user-turn ordinals, not mutable text or absolute message positions. A high-water mark survives transient empty/shrunk snapshots. Six regression tests cover these failures and the speech settings. Editing an existing user turn does not announce another send.

## Architecture
engine.py: pure token parser and state machine; silent baseline; sent-message detection;
paragraph deltas; progress throttling; explicit send-control completion; optional silence fallback.
__init__.py: NVDA/wx integration, settings, keyboard scripts, structured TextInfo field adapter.
ChatGPT scoping uses a parsed exact HTTPS host (chatgpt.com or chat.openai.com), or a document
in the chatgpt Windows process. No arbitrary title-only matches. No DOM/network scraping.
Only role=heading author boundaries are accepted, so ordinary message text saying “You said”
does not split conversations. Native NVDA announcements are preserved.

## Validation status
Automated tests cover simulated accessible fields and conversation transitions, NOT the live
ChatGPT page or the Windows app. No Windows NVDA runtime is available in the build environment. The user reported working automatic reading in Chrome and the Windows app with 0.1.1 and a 3-second silence fallback; 0.1.2 still requires a user acceptance test.
The manifest declares API target 2026.2 and minimum 2025.1; actual compatibility is unverified.
Do not describe this package as Windows-tested or submit it as stable before hands-on testing.
Both Chat and Work interfaces may differ. The adapter is intentionally conservative and may
report zero recognised messages or an unknown generation control rather than guess.

## Windows acceptance checks before release
1. Install on NVDA 2026.2 and confirm startup, translations and all settings.
2. Test a short foreground Chrome conversation: sent text once, progress changes, complete answer.
3. Test same prompt twice, failed send, regenerated answer, cancellation and multi-paragraph streaming.
4. Test disabled readSent + enabled confirmSent; disable both; answers/status independently.
5. Test complete mode with long thinking pauses. New installs use a 3-second silence fallback; test disabled fallback separately.
6. Test progressive mode, manual repeat, status, diagnostics, toggle and reassignable gestures.
7. Switch tabs and conversations; no old history or unrelated website content should be announced.
8. Verify settings persist across restart; test uninstall and global plug-in reload.
9. Test NVDA 2025.1 before claiming minimum-version compatibility, plus browsers/app individually.
10. For problems record diagnostic text, app/browser/NVDA versions and UI language. Do not include private chat text.

## Store preparation (not submitted)
Read https://github.com/nvaccess/addon-datastore/blob/master/docs/submitters/submissionGuide.md
Publish the source repository and a direct HTTPS .nvda-addon download, verify name uniqueness,
choose beta for the initial test release and validate the requested API versions against the
Store API version list. Set lastTestedNVDAVersion according to actual completed Windows tests.
English manifest and multilingual documentation alone do not guarantee Store acceptance.
The current homepage is the author's blog; set an add-on-specific page when one exists.
