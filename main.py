# tiny-chess-01 -- launcher stub.
#
# Nothing in this file plays chess. All the actual chess logic is stashed in engine.b85, which is
# Python source that was first squashed with lzma and then wrapped in base85 so it could live in a
# text file. Per RULES.txt this is legal: a compressed payload is allowed, and because this loader
# is what makes that payload run, the loader is measured together with it against the 4,096-byte
# ceiling for a single file. Even counted that way the entry stays comfortably under the cap.
#
# Expand the payload and you get one self-contained chess engine that pulls in nothing outside the
# standard library. It stores the board as a flat 64-character list, reads and writes FEN, and
# generates fully legal moves -- castling rights, en passant targets and promotions included. Search
# is negamax with alpha-beta pruning plus a quiescence pass at the leaves, moves are tried in
# MVV-LVA order, and the position is scored with piece-square tables. Node counting is capped at a
# fixed budget, and that is deliberate: no wall clock and no random seed means the same position
# always yields the same answer, and whatever move comes back is guaranteed to be one of the legal
# moves handed to it.
import base64,lzma,os
P=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"engine.b85"),"rb").read()
exec(compile(lzma.decompress(base64.b85decode(P)),"engine","exec"))
