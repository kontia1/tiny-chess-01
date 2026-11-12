# tiny-chess-01 entry.
#
# The engine lives in engine.b85: lzma-compressed, base85-encoded Python source. RULES.txt lets a
# main.py unpack and exec a compressed payload, counting both the payload and this unpacker toward
# the 4,096-byte limit; the whole entry still fits the 8,192-byte snapshot cap.
#
# The unpacked source is a single-file chess engine, no imports beyond the standard library:
# board as a 64-char list, FEN parsing, legal move generation (castling rights, en passant,
# promotions), negamax alpha-beta with quiescence search, MVV-LVA move ordering, piece-square-table
# evaluation, and a fixed node budget so play is deterministic: no clock, no randomness, and the
# move it returns is always one of the legal moves the environment listed.
import base64,lzma,os
P=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"engine.b85"),"rb").read()
exec(compile(lzma.decompress(base64.b85decode(P)),"engine","exec"))
