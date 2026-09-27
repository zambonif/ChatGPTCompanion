# Copyright (C) 2026 Fernando de Paula Zamboni
# SPDX-License-Identifier: GPL-2.0-or-later
"""Read the document tail without fetching all historical text."""
import textInfos
from .engine import ASSISTANT_HEADINGS, USER_HEADINGS, normalized, parse_tokens


class LatestTextUnavailable(Exception):
    """No reliable latest turn was found; callers must clear cached speech."""


def read_snapshot(reader, tokenize, ignore_interface=True):
    end = reader.makeTextInfo(textInfos.POSITION_ALL)
    end.collapse(end=True)  # Range construction/collapse does not retrieve text.
    iterator = getattr(reader, '_iterNodesByType', None)
    if iterator:
        try:
            selected = None
            count = 0
            for index, item in enumerate(iterator('heading', direction='previous', pos=end)):
                if index >= 512:
                    break
                if normalized(item.textInfo.text) in USER_HEADINGS | ASSISTANT_HEADINGS:
                    selected = item.textInfo.copy()
                    count += 1
                    if count == 2:
                        break
            if selected is not None:
                selected.setEndPoint(end, 'endToEnd')
                return parse_tokens(tokenize(selected.getTextWithFields()), ignore_interface)
        except (AttributeError, NotImplementedError, LookupError):
            # UIA providers do not all implement browse-mode quick navigation.
            pass
    # Providers without a heading index: extend backwards by lines, not by
    # characters (character movement in a virtual buffer can loop per character).
    # Stop at the first window containing an author boundary; there is never a
    # fallback to some cached earlier answer if the newest text is unavailable.
    for lines in (160, 640, 2560):
        tail = end.copy()
        moved = tail.move(textInfos.UNIT_LINE, -lines, endPoint='start')
        snapshot = parse_tokens(tokenize(tail.getTextWithFields()), ignore_interface)
        if snapshot.messages:
            return snapshot
        if abs(moved) < lines:
            return snapshot
    raise LatestTextUnavailable()
