import os
import re
from typing import Iterable, Iterator

# vocab = [(0, b"\x00"), (1, b"\x01")..., (256, b"123"), (257, b"444")]
# merges = [(b"\x00", b"\x01"), (b"123", b"444")]

class BPETokenizer:
    def __init__(self,
                 vocab: dict[int, bytes],
                 merges: list[tuple[bytes, bytes]],
                 special_tokens: list[str] | None = None):
        self.vocab = vocab
        self.merges = merges
        self.special_tokens = special_tokens

    @classmethod
    def from_files(cls, vocab_filepath, merges_filepath, special_tokens=None):
        return

    def encode(self, text: str) -> list[int]:
        if self.special_tokens is None:
            return self.encode_single(text)

        sorted_tokens = sorted(self.special_tokens, key=len, reverse=True)
        pattern = re.compile("(" + "|".join(map(re.escape, sorted_tokens)) + ")")
        contents = pattern.split(text)
        res: list[int] = list()
        for content in contents:
            if not content in self.special_tokens:
                res = res + self.encode_single(content)
            else:
                res.append(self.find_tokenID_from_bytes(content.encode(encoding="utf-8")))

        return res

    def encode_single(self, text: str) -> list[int]:
        if text == "":
            return []
        bs: list[bytes] = [bytes([b]) for b in text.encode("utf-8")]
        while True:
            tmp: list[bytes] = list()
            i = 0
            mergedPair = (len(bs), len(bs))
            rank = len(self.merges)

            while i + 1 < len(bs):
                searched = self.search_tuple_in_merges((bs[i], bs[i+1]))
                cur_rank = searched[0]
                if searched[2] and cur_rank < rank:
                    mergedPair = (i, i + 1)
                    rank = cur_rank
                i = i + 1

            if mergedPair == (len(bs), len(bs)): # nothing to merge
                break

            i = 0
            while i < len(bs): # implement **real** merge, very ugly
                if i != mergedPair[0]:
                    tmp.append(bs[i])
                else:
                    tmp.append(bs[i]+bs[i+1])
                    i = i + 1
                i = i + 1
            bs = tmp
        return [self.find_tokenID_from_bytes(b) for b in bs]


    def find_tokenID_from_bytes(self, bs: bytes) -> int:
        # TODO: optimize
        for i, v in self.vocab.items():
            if v == bs:
                return i
        raise FUCK_YOU

    def search_tuple_in_merges(self, tmp_tuple: tuple[bytes, bytes]) -> tuple[int, int, bool]:
        for i, v in enumerate(self.merges):
            if v == tmp_tuple:
                return i, i + 1, True
        return -1, -1, False

    def encode_iterable(self, iterable: Iterable[str]) -> Iterator[int]:
        return

    def decode(self, ids: list[int]) -> str:
        return b"".join(self.vocab[i] for i in ids).decode(encoding="utf-8", errors="replace")

    @staticmethod
    def bpe_run_train_impl(input_path: str | os.PathLike,
                           vocab_size: int,
                           special_tokens: list[str],
                           **kwargs, ) -> tuple[dict[int, bytes], list[tuple[bytes, bytes]]]:
        f = open(input_path, mode="r", encoding="utf-8")
        # assume the text is not too long
        text = f.read()

        f.close()
        raise NotImplementedError
        return tuple(dict())

class FUCK_YOU(Exception):
    pass