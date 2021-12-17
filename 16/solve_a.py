#!/usr/bin/env python3
# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring
"""

    Packets:
        3: Version
        3: Packet Type

        Operator (Packet Type != 4):
            1: Length Type
            Subpackets (Length Type == 1):
                11: Number of subpackets
            Bits (Length Type == 0):
                15: Total length in bits
"""

import sys
from itertools import islice
from typing import Iterable


def ascii_hex_to_bin(hex_byte: str) -> str:
    return "{0:#06b}".format(int(hex_byte, base=16))[2:]


def hex_strings_as_binary(input_file) -> Iterable[str]:
    """Read a file as text-hex and convert to text-bin."""

    while buffer := input_file.read(64).strip():
        for byte in buffer:
            yield from ascii_hex_to_bin(byte)


def iterable_bin_to_int(iterable: Iterable, count: int) -> int:
    binary_string = "".join(islice(iterable, count))
    # print("--", binary_string)
    return int(binary_string, base=2)


LITERAL_VALUE_TYPE_ID = 0x4


def next_packet(data: Iterable[str]):
    version = iterable_bin_to_int(data, 3)
    print("Version:", version)

    packet_type_id = iterable_bin_to_int(data, 3)
    is_literal = packet_type_id == LITERAL_VALUE_TYPE_ID
    print("Type ID:", packet_type_id, 'literal' if is_literal else 'operator')

    if not is_literal:
        length_type_id = iterable_bin_to_int(data, 1)
        print("Length: ", length_type_id, 'subpackets' if length_type_id else 'bits')

        if length_type_id:
            subpacket_count = iterable_bin_to_int(data, 11)
            print("Packets:", subpacket_count)

        else:
            bit_count = iterable_bin_to_int(data, 15)
            print("Bits:   ", bit_count)

    else:
        value = 0
        while iterable_bin_to_int(data, 1):
            value = (value << 4) + iterable_bin_to_int(data, 4)

        # Get the last packet of bits
        value = (value << 4) + iterable_bin_to_int(data, 4)
        print("Value:  ", value)


    return (version, packet_type_id)


def main() -> None:
    data = hex_strings_as_binary(sys.stdin)

    version_sum = 0
    while packet := next_packet(data):
        version_sum += packet[0]
        print("SUBTOTAL:", version_sum)
        print("-" * 80)


if __name__ == "__main__":
    main()
