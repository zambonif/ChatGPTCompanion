# Development

## Build and tests

Python 3.11 or newer; standard library only.

```
python -m unittest discover -s tests -v
python build.py
```

On Windows, BUILD.cmd runs the tests and build. Output is dist/ChatGPTCompanion-0.1.3.nvda-addon. The package contains addon/ contents directly at its root, including the English manifest.ini. The internal name fzChatGPTCompanion remains stable across upgrades.

## Files

- addon/globalPlugins/fzChatGPTCompanion/__init__.py: NVDA settings, gestures, field tokenisation, context selection and timer.
- engine.py: author-heading parsing, footer filter and announcement state.
- reading.py: document-end range selection and line-based fallback.
- docs/*.md: user help in five languages; English also supplies the repository README content.
- translations/ui.json: language maps keyed by English gettext strings. build.py rejects missing/extra strings and mismatched placeholders.
- addon/locale and addon/doc: generated translations and help, retained in source for inspection.
- tests/: synthetic provider, state-machine and plugin lifecycle tests; see TESTING.md for their limits.

## Recent-text retrieval

The reader constructs a TextInfo range and collapses it at document end without retrieving the whole story text. For browse-mode providers it uses NVDA's _iterNodesByType heading index backwards, looking for the latest two author headings (up to 512 headings). This internal interface is a compatibility risk to review for future NVDA releases. It expands from that heading to the end and retrieves structured text only for that range.

Providers without that index use successively larger windows of 160, 640 and 2560 lines from the document end. Character-by-character movement and the previous 250,000-character cutoff are avoided. This is not DOM scraping and does not force-refresh the web page, scroll, move focus or use private ChatGPT endpoints. If ChatGPT fails to expose recent messages, there is no way for this implementation to reconstruct them; a missing latest response must be reported rather than substituted with cached text.

Headings retain accessible uniqueID/runtimeID values where provided. These identify user turns when the recent window shifts. Without IDs, turn counts and role transitions provide a conservative fallback. New author headings reset the editable-region boundary so an old embedded editor cannot hide later turns. Literal author headings inside a response and rebuilt accessibility IDs remain potential ambiguities requiring live testing.

## Context and speech

Up to eight in-memory trackers are keyed by process, document window handle and URL. Returning to an already observed conversation compares its new tail with the prior snapshot. Other windows are not polled or spoken while inactive. Different URLs/windows do not share a last-answer cache. The new-chat URL transition can retain the current tracker when the same document gains a /c/ identifier.

The repeat command reads a fresh snapshot, even with automatic monitoring disabled. A trailing user turn, missing messages or provider failure clears its output instead of reusing a prior answer. A request that finds only stale content supplied by the accessibility provider cannot establish that the provider is out of date.

No network operations, cookies, clipboard access or persistence of conversation content are used by the add-on. Secure screens are excluded. Settings are stored by NVDA. The tail text and previous snapshots are held in memory until eviction/reset/termination. Answer deduplication uses text hashes; sender IDs and answer fingerprints are bounded.

## Manifest and release

The review did not identify a malformed manifest field. Version 0.1.3 makes the description user-facing, updates the homepage to the repository, and narrows the minimum API to 2026.2, the known tester environment, instead of claiming unverified 2025.1 compatibility. lastTestedNVDAVersion remains 2026.2 based on the author's prior real-use reports; the new release still needs the acceptance checks in TESTING.md before resubmission. Do not relabel the new code as human-tested on the strength of unit tests alone.

Publish source and the matching immutable release asset after validation; do not replace the contents of a previously published version's asset. The current Store submission needs revision/resubmission, not a claim of approval. Independent projects may offer overlapping functionality; no exclusive-feature claim is made.
