# ChatGPT Companion 0.1.2 — experimental release

By Fernando de Paula Zamboni. https://www.blog.fernandozamboni.com

Reads sent messages, answers and accessible progress updates in the active ChatGPT conversation without moving focus. Uses NVDA speech and braille. Interface and documentation are available in Brazilian Portuguese, English, Spanish, French and Italian.

## Changes in version 0.1.2

Ignore interface notices and footer text is enabled by default. It removes the known trailing mistake disclaimer followed by “Latest response”, from both automatic reading and the repeat command. This is not a global text replacement: isolated sentences, quoted examples and mid-answer references remain intact. Matching is textual; if an answer literally ends with that entire block, disable the option to hear it. Other unrecognised footers may remain.

An old answer is no longer requeued when a new user turn appears or when an already announced answer disappears and returns in the accessibility tree. New installations default to a 3-second silence fallback; existing settings are preserved. The user confirmed automatic reading with this fallback in Chrome and the Windows app using 0.1.1. This update still needs testing in both environments before publication.

## Version 0.1.1 change

Fixed repeated sent-message announcements during page updates. Each new send is announced once; changes to the same text or temporary disappearance do not trigger another announcement. A new send with identical text is still recognised. For silent sending, disable both Read sent messages and Confirm sending. Editing an existing message without adding a new one does not trigger automatic sent-message reading.

## Installation and first test
Open fzChatGPTCompanion-0.1.2.nvda-addon, confirm installation and restart NVDA when prompted. Declared compatibility: NVDA 2025.1 through 2026.2. Actual Windows testing is still required. The lastTestedNVDAVersion field is the compatibility target of this experimental package, not a claim of completed runtime testing.

Start with a short conversation in Chrome at https://chatgpt.com. Wait about two seconds, then send a simple question. Expect your message, recognised progress updates and the completed answer to be read. Existing history is not announced. Switching tabs, conversations or applications establishes a new baseline; updates received while away are not announced on return. Keep the conversation active during testing.

Edge, Firefox, Brave and the ChatGPT Windows app are experimental targets. The app must expose a document with structured accessible text. Support requires validation in each environment. No ChatGPT API key or additional API payment is required.

## Settings
Open NVDA menu, Preferences, Settings, ChatGPT Companion. Use Tab, Space and arrow keys, then OK. Save NVDA settings if saving on exit is disabled.

- Enable automatic reading: turn monitoring on or off.
- Read sent messages: read the content after it appears in the conversation, not merely when Enter is pressed.
- Confirm sending: if sent-message reading is disabled, announce only “Message sent”. Disable both for silent sending.
- Read answers and Read progress updates: independent switches.
- Complete answer: default; requires a recognised send control and two seconds without text changes.
- New paragraphs: experimental; reads completed paragraphs during generation. Website text revisions may cause repetition. Text without paragraph breaks may wait until completion.
- Wait after completion: 1 to 10 seconds; default 2.
- Fallback after silence: 0 to 60 seconds; 0 disables it and new installations default to 3. If no generation control is recognised, a value such as 8 infers completion after silence. A pause may cause premature reading; this is not a reliable completion signal.

## Commands
NVDA means Insert or Caps Lock, according to your configuration. Reassign commands under Preferences, Input gestures, ChatGPT Companion.

- NVDA+Control+Shift+G: toggle automatic reading.
- NVDA+Control+Shift+R: read the latest available answer, which may still be partial. Works with automatic reading disabled.
- NVDA+Control+Shift+P: read the latest available progress update.
- NVDA+Control+Shift+D: report recognised message count and generation control status.
- Control: stop current speech using normal NVDA behaviour. Use the G command to prevent subsequent announcements.

## Limitations and troubleshooting
“Thinking” means only a status or summary exposed by the interface. The add-on cannot retrieve internal reasoning, hidden text or content unavailable to NVDA. It recognises author headings and controls in five languages; interface changes may require updates. Images, attachments and formulas have no special interpretation.

If diagnostics report zero messages, confirm that a message was sent and try browse mode with NVDA+Space. Try Chrome or Edge if needed. If messages are recognised but the generation control is not, use manual reading or the optional silence fallback. Conversations above 250,000 characters are skipped to limit processing; long conversations below that limit can still affect performance.

Native live-region announcements from the page/NVDA may duplicate speech. Disable the add-on’s progress reading if necessary; it does not globally suppress native announcements. Report browser/app version, NVDA version, interface language and the diagnostic message; conversation content is not required. Test tab switching, installation, removal, settings persistence and all four commands before release.

## Privacy, licence and distribution
No network, cookies, passwords, clipboard or conversation files are accessed. Accessible text is processed in memory while the conversation is active, without saving or sending its content. Secure Windows screens are excluded. NVDA stores the settings.

GNU GPL version 2 or later, without warranty; see COPYING.txt. Independent project, not affiliated with OpenAI or NV Access. The root manifest.ini is in English; translations are under locale. Before Store submission, test on Windows, verify declared compatibility and publish source code plus a direct HTTPS package download. Package structure does not guarantee Store approval.
