from enum import Enum
from dataclasses import dataclass


class Direction(str, Enum):
    L = "L"
    R = "R"


@dataclass
class Rotation:
    direction: Direction
    clicks: int

    @staticmethod
    def create_rotation(raw_rotation: str) -> "Rotation":
        if not isinstance(raw_rotation, str):
            raise ValueError(f"{raw_rotation} is not str!")

        if len(raw_rotation) < 2:
            raise ValueError(f"{raw_rotation} legth is too short!")

        if len(raw_rotation) > 4:
            raise ValueError(f"{raw_rotation} legth is too long!")

        if raw_rotation[0] not in list(Direction):
            raise ValueError(f"{raw_rotation} direction can only be R or L!")

        direction = Direction(raw_rotation[0])
        raw_clicks = raw_rotation[1:]

        if not str.isdigit(raw_clicks):
            raise ValueError(f"{raw_rotation} clicks should be a int!")

        clicks = int(raw_clicks)

        return Rotation(direction=direction, clicks=clicks)


@dataclass
class Safe:
    dial_point: int = 50

    def turn_dial(self, rotation: Rotation) -> "Safe":
        operator = 1
        if rotation.direction == Direction.L:
            operator = -1

        raw_new_dial_point: int = self.dial_point + (operator * rotation.clicks)
        new_dial_point: int = raw_new_dial_point % 100
        return Safe(dial_point=new_dial_point)


@dataclass
class PasswordDiscoverState:
    safe_state: Safe = Safe()
    how_many_times_dial_zero: int = 0

    def execute_rotation(self, rotation: Rotation) -> "PasswordDiscoverState":
        new_safe_state: Safe = self.safe_state.turn_dial(rotation=rotation)
        new_how_many_times_dial_zero: int = self.how_many_times_dial_zero

        if new_safe_state.dial_point == 0:
            new_how_many_times_dial_zero += 1

        return PasswordDiscoverState(
            safe_state=new_safe_state,
            how_many_times_dial_zero=new_how_many_times_dial_zero,
        )


if __name__ == "__main__":
    password_discover_state = PasswordDiscoverState()

    while True:
        try:
            rotation: Rotation = Rotation.create_rotation(raw_rotation=input().strip())
            password_discover_state: PasswordDiscoverState = (
                password_discover_state.execute_rotation(rotation=rotation)
            )
        except EOFError:
            break
        except ValueError as err:
            print(err)

    print(password_discover_state)
