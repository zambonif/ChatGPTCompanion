# Testing record

## Human testing already reported

Tester: Fernando de Paula Zamboni, using NVDA in Windows. The reported environment is NVDA 2026.2. The observations below come from the author's interactive testing on September 26–27, 2026, not from simulated tests.

| Area | Observed result in earlier builds |
| --- | --- |
| Chrome, sent-message reading | Initial repetition reproduced by the author; 0.1.1 changed send detection. |
| Chrome, completion detection | No generation control detected; silence fallback at 8 seconds worked, then 3 seconds worked. |
| Chrome, long generated answer | Author confirmed the answer was read successfully with 3-second fallback. |
| Windows ChatGPT app | Author confirmed automatic answer reading and disabling sent-message reading. |
| Footer text | Author reported the disclaimer/latest-response footer being read; 0.1.2 introduced an optional filter. No separate formal pass recorded for every footer case. |
| Previous-answer replay | Author reported one sequential replay in Chrome; manual repeat subsequently read only the current answer. |
| Long history / focus situations | Author later reported missing automatic responses and manual repeat reading an earlier answer. This is the reason for 0.1.3. |

These observations do not certify every feature, every browser, every ChatGPT interface or the new 0.1.3 implementation.

## Automated checks for 0.1.3

The suite runs on Linux with Python and synthetic NVDA dependencies. It covers parser boundaries, sent-message suppression, footer matching, progressive reading, empty snapshots, rolling message IDs, historical deduplication, returning after focus changes, and the real plugin methods for manual repeat and failure handling.

The range-selection test uses more than 300,000 characters of simulated history and asserts that historical text is never requested while the latest answer is extracted. This verifies the algorithm, not the behaviour of Windows accessibility providers. The plugin tests simulate separate window handles with identical URLs and fresh/manual reads.

Build checks compile the translation catalogs, verify translated placeholders and help languages, and inspect the package's English root manifest. No automated test is described as human acceptance testing.

## Pending human checks on 0.1.3

Record the result and exact NVDA/browser/app versions after each check:

1. Install 0.1.3 over 0.1.2; verify preserved preferences and successful NVDA restart.
2. In Chrome, use the same long conversation that failed. Send a new question, wait and verify only the new answer is announced.
3. Press NVDA+Control+Shift+R. Verify the current answer; while a new question is still unanswered, verify an older answer is not substituted.
4. Leave an already recognised conversation for another window during generation. Return after completion and check the new answer is announced once.
5. Open two ChatGPT conversations/windows. Verify their answers do not get mixed and returning to unchanged history does not replay it.
6. Repeat the reading and repeat-command checks in the Windows app. Record any provider-specific failures.
7. Exercise an old editable message/code field followed by later messages; confirm parsing reaches the latest turn.
8. Verify sending options, footer option, manual progress, diagnostics and disabled automatic reading.
9. Confirm settings persistence, add-on reload/removal and both complete and progressive modes as used.

If a check fails, report diagnostic output and reproduction steps without private conversation content. The count now represents the recent slice, so a small number in a long conversation is expected.
