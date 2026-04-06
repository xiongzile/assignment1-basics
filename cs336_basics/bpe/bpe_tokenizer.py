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
        return

    def encode_iterable(self, iterable: Iterable[str]) -> Iterator[int]:
        return

    def decode(self, ids: list[int]) -> str:
        return

    @staticmethod
    def bpe_run_train_impl(input_path: str | os.PathLike,
                           vocab_size: int,
                           special_tokens: list[str],
                           **kwargs, ) -> tuple[dict[int, bytes], list[tuple[bytes, bytes]]]:
        raise NotImplementedError
        return tuple(dict())

