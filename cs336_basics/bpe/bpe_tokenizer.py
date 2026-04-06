import os
from typing import Iterable, Iterator


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
        return list(text.encode(encoding="utf-8"))

    def encode_iterable(self, iterable: Iterable[str]) -> Iterator[int]:
        return

    def decode(self, ids: list[int]) -> str:
        return b"".join(self.vocab[i] for i in ids).decode(encoding="utf-8")

    @staticmethod
    def bpe_run_train_impl(input_path: str | os.PathLike,
                           vocab_size: int,
                           special_tokens: list[str],
                           **kwargs, ) -> tuple[dict[int, bytes], list[tuple[bytes, bytes]]]:
        f = open(input_path, mode="r", encoding="utf-8")
        # assume the text is not too long
        text = f.read()

        f.close()
        return tuple(dict())

