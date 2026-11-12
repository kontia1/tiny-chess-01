# tiny-chess-01

A 4,096-byte-limit Python chess engine entry.

`main.py` is the whole engine: it unpacks an lzma payload (allowed by the rules; payload and
unpacker both count toward the byte limit) containing board representation, legal move
generation (castling, en passant, promotion), negamax alpha-beta with quiescence, MVV-LVA move
ordering and piece-square-table evaluation, driven by a fixed node budget (deterministic: no
clock, no randomness).
