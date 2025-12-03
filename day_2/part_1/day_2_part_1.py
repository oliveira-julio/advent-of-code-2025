from typing import Iterator
from dataclasses import dataclass


@dataclass
class ElfId:
    value: int

    @staticmethod
    def create_id(id_value: str) -> "ElfId":
        if not isinstance(id_value, str):
            raise ValueError(f"{id_value} is not str!")

        if not str.isdigit(id_value):
            raise ValueError(f"{id_value} id_value should be a int!")

        return ElfId(value=int(id_value))

    @staticmethod
    def is_id_mirrored(elf_id: "ElfId") -> bool:
        str_value = str(elf_id.value)

        if len(str_value) % 2 == 1:
            return False

        half: int = len(str_value)//2
        first_half_id: str = str_value[:half]
        last_half_id: str = str_value[half:]

        return first_half_id == last_half_id


@dataclass
class PairIds:
    first_id: ElfId
    last_id: ElfId

    @staticmethod
    def create_pair_ids(raw_pair: str) -> "PairIds":
        if not isinstance(raw_pair, str):
            raise ValueError(f"{raw_pair} is not str!")

        if "-" not in raw_pair:
            raise ValueError(f"{raw_pair} is not a pair!")

        splitted_pair = raw_pair.split("-")
        if len(splitted_pair) != 2:
            raise ValueError(f"{raw_pair} is not a valid pair!")

        raw_first_id, raw_last_id = splitted_pair
        first_id = ElfId.create_id(id_value=raw_first_id)
        last_id = ElfId.create_id(id_value=raw_last_id)

        if first_id.value > last_id.value:
            first_id, last_id = last_id, first_id

        return PairIds(first_id=first_id, last_id=last_id)

    def generate_range(self) -> Iterator[int]:
        yield from (ElfId(value=value) for value in range(self.first_id.value, self.last_id.value+1))


@dataclass
class TotalInvalidIdsState:
    total: int = 0

    def add_pair_to_total(self, pair: PairIds) -> "TotalInvalidIdsState":
        invalids = filter(ElfId.is_id_mirrored, pair.generate_range())
        total_pair = sum(invalid.value for invalid in invalids)
        return TotalInvalidIdsState(total=self.total + total_pair)


if __name__ == "__main__":
    total_invalid_ids_state = TotalInvalidIdsState()

    raw_pairs = input().split(",")

    for raw_pair in raw_pairs:
        try:
            pair = PairIds.create_pair_ids(raw_pair=raw_pair)
            total_invalid_ids_state = total_invalid_ids_state.add_pair_to_total(pair=pair)
        except ValueError as err:
            print(err)

    print(total_invalid_ids_state)
