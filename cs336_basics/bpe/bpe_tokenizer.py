import os
import regex as re
from math import inf
from typing import Iterable

# vocab = [(0, b"\x00"), (1, b"\x01")..., (256, b"123"), (257, b"444")]
# merges = [(b"\x00", b"\x01"), (b"123", b"444")]
PAT = r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""

class BPETokenizer:
    def __init__(self,
                 vocab: dict[int, bytes],
                 merges: list[tuple[bytes, bytes]],
                 special_tokens: list[str] | None = None):
        self.vocab = vocab
        self.merges = merges
        self.special_tokens = special_tokens

        self.bytes2tokenID = {v:k for k, v in vocab.items()}
        self.merges2rank = {t: i for i, t in enumerate(merges)}

    @classmethod
    def from_files(cls, vocab_filepath, merges_filepath, special_tokens=None):
        return

    def encode(self, text: str) -> list[int]:
        if self.special_tokens is None:
            return self.encode_single(text)
        tks = BPETokenizer.gpt2_split(self.special_tokens, text)
        res = []
        for tk in tks:
            if not tk:
                continue

            if tk in self.special_tokens:
                res.append(self.find_tokenID_from_bytes(tk.encode(encoding="utf-8")))
                continue

            res.extend(self.encode_single(tk))

        return res

    def encode_single(self, text: str) -> list[int]:
        if text == "":
            return []
        bs: list[bytes] = [bytes([b]) for b in text.encode("utf-8")]
        while True:
            tmp: list[bytes] = []
            i = 0
            mergedPair = (len(bs), len(bs))
            rank = len(self.merges)

            while i + 1 < len(bs):
                searched = self.merges2rank.get((bs[i], bs[i+1]), inf)
                cur_rank = searched
                if cur_rank < rank:
                    mergedPair = (i, i + 1)
                    rank = cur_rank
                i = i + 1

            if mergedPair == (len(bs), len(bs)): # nothing to merge
                break
            pr = (bs[mergedPair[0]], bs[mergedPair[1]])
            if pr[0] == b"\n" or pr[1] == b"\n":
                pass
            i = 0
            while i < len(bs): # implement **real** merge, very ugly
                if i + 1 < len(bs) and bs[i] == pr[0] and bs[i+1] == pr[1]:
                    tmp.append(bs[i] + bs[i + 1])
                    i = i + 1
                else:
                    tmp.append(bs[i])
                i = i + 1
            bs = tmp
        return [self.find_tokenID_from_bytes(b) for b in bs]

    def find_tokenID_from_bytes(self, bs: bytes) -> int:
        return self.bytes2tokenID[bs]

    def encode_iterable(self, iterable: Iterable[str]) -> list[int]:
        t = "" # simple implement here. It's more complex to support real stream handling.
        for text in iterable:
            t += text
        return self.encode(t)

    def decode(self, ids: list[int]) -> str:
        return b"".join(self.vocab[i] for i in ids).decode(encoding="utf-8", errors="replace")

    @staticmethod
    def bpe_run_train_impl(input_path: str | os.PathLike,
                           vocab_size: int,
                           special_tokens: list[str],
                           **kwargs, ) -> tuple[dict[int, bytes], list[tuple[bytes, bytes]]]:

        vocab = {i: bytes([i]) for i in range(0, 256)}
        for idx, tk in enumerate(special_tokens):
            vocab[vocab_size-idx] = tk.encode(encoding="utf-8")


        f = open(input_path, mode="r", encoding="utf-8")
        text = f.read()
        tks = BPETokenizer.gpt2_split(special_tokens, text)
        pass

        f.close()
        raise NotImplementedError

    @staticmethod
    def gpt2_split(special_tokens: list[str], text: str) -> list[str]:
        tks = []
        sorted_tokens = sorted(special_tokens, key=len, reverse=True)
        pattern = re.compile("(" + "|".join(map(re.escape, sorted_tokens)) + ")")
        contents = pattern.split(text)
        for c in contents:
            if c in special_tokens:
                tks.append(c)
                continue
            tks.extend([m.group(0) for m in re.finditer(PAT, c)])
        return tks