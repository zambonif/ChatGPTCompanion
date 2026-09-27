# ChatGPT Companion

By Fernando de Paula Zamboni. Version 0.1.3 (beta).

ChatGPT Companion is an NVDA add-on for reading new messages in the existing ChatGPT website and Windows app. It can announce answers automatically, read or confirm your sent messages, and announce accessible progress updates without moving keyboard focus.

## Why this add-on?

The goal is to follow a conversation without repeatedly navigating back from the message box to find the latest answer. You continue using your normal ChatGPT account and interface. There is no separate chat client, API key or additional API charge. Speech and braille use NVDA's current configuration.

Other add-ons may offer overlapping features. This project focuses on automatic announcements in the existing interface, with independent controls for sent messages, answers and progress. It is an optional accessibility aid, not a replacement for accessibility improvements in ChatGPT itself.

## Install

Download ChatGPTCompanion-0.1.3.nvda-addon, open it while NVDA is running, confirm installation and restart NVDA. NVDA 2026.2 or later is required; the declared tested API version is 2026.2. Later NVDA versions may require compatibility review.

Downloads: https://github.com/zambonif/ChatGPTCompanion/releases

Source and issue reports: https://github.com/zambonif/ChatGPTCompanion

## Start using it

Open ChatGPT in Chrome or the Windows app, leave the conversation active for a moment and send a question. Reading was confirmed by the author in both environments during tests of earlier releases. Version 0.1.3 includes further fixes that still need real-world testing. Edge, Firefox and Brave are additional experimental targets.

An existing conversation opens silently. The add-on monitors only the active conversation. It remembers up to eight recently visited contexts during the NVDA session. If you leave a recognised conversation and return after an answer arrives, it can announce that new answer on return; it does not speak in the background. Restarting NVDA or toggling monitoring with its shortcut clears this memory.

## Settings

Open NVDA menu, Preferences, Settings, ChatGPT Companion. Existing preferences are preserved on upgrade. Save NVDA's configuration if automatic saving is disabled.

- Enable automatic reading: switch monitoring on or off.
- Read sent messages: read your message after it appears in the conversation.
- Confirm sending: say only “Message sent” when reading sent messages is disabled. Disable both options for silent sending.
- Read answers and Read progress updates: control these announcements independently.
- Ignore interface notices and footer text: enabled by default; filters recognised trailing disclaimer blocks. Disable it if a literal footer example at the end of an answer is removed.
- Complete answer: waits for a recognised completion control and stable text. New paragraphs is an experimental alternative for reading during generation.
- Wait after completion: 1–10 seconds, default 2.
- Fallback after silence: 0–60 seconds, default 3 for new installations. Used when no generation control is recognised. A long pause can be mistaken for completion; increase the value if reading starts too early. Set 0 to disable this fallback.

## Keyboard commands

NVDA means Insert or Caps Lock, depending on your keyboard settings. Reassign these commands in NVDA's Input gestures dialog, under ChatGPT Companion.

- NVDA+Control+Shift+G: toggle automatic reading.
- NVDA+Control+Shift+R: read the latest available answer. If a newer question is waiting for a response, the previous answer is not substituted. A response still being generated may be partial.
- NVDA+Control+Shift+P: read the latest accessible progress update.
- NVDA+Control+Shift+D: refresh and report diagnostics for the recent messages and generation control.
- Control: stop current speech using NVDA's usual behaviour. Use the G shortcut to stop subsequent automatic announcements.

## Troubleshooting and limitations

If nothing is read, check Read answers, try the R and D commands, and check the silence fallback. The message count in diagnostics refers to the recent portion being inspected, not the whole conversation. Try browse mode with NVDA+Space if no conversation is recognised.

The add-on reads accessible author headings and text. It cannot retrieve content which ChatGPT has not exposed to NVDA. If the current answer is unavailable, it reports no available answer instead of deliberately using a cached older one. Interface changes can still affect detection. It does not interpret attachments, images or formulas specially. Progress means visible, accessible status information, not internal reasoning.

Version 0.1.3 reads recent turns from the document end instead of rejecting histories over 250,000 characters. Extremely large individual responses or providers without heading navigation can still be slow or incomplete. The fallback search covers up to 2,560 lines from the end.

Native page announcements may duplicate speech; disabling this add-on's progress announcements can help. Report your NVDA version, browser/app version, interface language, diagnostic output and steps to reproduce. Private conversation text is not required.

## Changes in 0.1.3

Improved reading of long conversations and histories containing editable fields. The repeat command requests fresh text. Recent conversation state is retained across temporary focus changes. Documentation now separates user instructions from development and test records. The manifest homepage points to the project and its minimum NVDA version is 2026.2.

## Privacy and licence

The add-on does not make network requests or access passwords, cookies or the clipboard. It temporarily holds accessible conversation text in memory, without saving or sending it. NVDA stores preferences. It is disabled on secure Windows screens.

Free software under GNU GPL version 2 or later, without warranty. Independent project, not affiliated with OpenAI or NV Access. Interface and help are available in English, Brazilian Portuguese, Spanish, French and Italian.
