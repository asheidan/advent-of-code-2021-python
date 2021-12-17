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

        Literal (Packet Type == 4):
            Repeating:
                1: Not last packet
                4: Set of bits
"""

import sys
from itertools import islice
from typing import Iterable
from pprint import pprint


def ascii_hex_to_bin(hex_byte: str) -> str:
    return "{0:#06b}".format(int(hex_byte, base=16))[2:]


def hex_strings_as_binary(input_file) -> Iterable[str]:
    """Read a file as text-hex and convert to text-bin."""

    while buffer := input_file.read(64).strip():
        for byte in buffer:
            yield from ascii_hex_to_bin(byte)


def iterable_bin_to_int(iterable: Iterable, count: int) -> int:
    binary_string = "".join(islice(iterable, count))
    if len(binary_string) < count:

        raise StopIteration

    # print("--", binary_string)
    return int(binary_string, base=2)


TYPE_ID_SUM = 0x0
TYPE_ID_LITERAL_VALUE = 0x4


def log(*message, parselevel, output=sys.stderr):
    print("| " * parselevel, *message, file=output)


def as_packets(data: Iterable[str], packetlimit=None, parselevel=0):
    operators = {
        0x0: "sum",
        0x1: "product",
        0x2: "minimum",
        0x3: "maximum",
        # 4 is a literal value
        0x5: "greater than",
        0x6: "less than",
        0x7: "equal to",
    }
    while packetlimit is None or packetlimit > 0:
        try:
            version = iterable_bin_to_int(data, 3)
            log("-" * 80, parselevel=parselevel)
            log("Version:", version, parselevel=parselevel)

            packet_type_id = iterable_bin_to_int(data, 3)
            is_literal = packet_type_id == TYPE_ID_LITERAL_VALUE
            log("Type ID:", packet_type_id, 'literal' if is_literal else 'operator:' + operators[packet_type_id], parselevel=parselevel)

            value = 0
            subpackets = []
            if not is_literal:
                length_type_id = iterable_bin_to_int(data, 1)
                log("Length: ", length_type_id, 'subpackets' if length_type_id else 'bits', parselevel=parselevel)

                if length_type_id:
                    subpacket_count = iterable_bin_to_int(data, 11)
                    log("Packets:", subpacket_count, parselevel=parselevel)
                    subpackets = list(as_packets(data, packetlimit=subpacket_count, parselevel=parselevel+1))

                else:
                    bit_count = iterable_bin_to_int(data, 15)
                    log("Bits:   ", bit_count, parselevel=parselevel)
                    subpacket_bits = islice(data, bit_count)
                    subpackets = list(as_packets(subpacket_bits, parselevel=parselevel+1))

            else:
                while iterable_bin_to_int(data, 1):
                    value = (value << 4) + iterable_bin_to_int(data, 4)

                # Get the last packet of bits
                value = (value << 4) + iterable_bin_to_int(data, 4)
                log("Value:  ", value, parselevel=parselevel)

            yield (version, packet_type_id, value or subpackets)

            if packetlimit is not None:
                packetlimit -= 1

        except StopIteration:

            break

    return


def packet_to_expression(packet):
    operators = {
        0x0: "sum",
        0x1: "product",
        0x2: "minimum",
        0x3: "maximum",
        # 4 is a literal value
        0x5: ">",
        0x6: "<",
        0x7: "=",
    }
    _version, operation, payload = packet

    if operation == 0x4:
        return payload

    return (operators[operation], *map(packet_to_expression, payload))


def gt(values) -> int:
    values = list(values)
    return int(values[0] > values[1])


def lt(values) -> int:
    values = list(values)
    return int(values[0] < values[1])

    
def eq(values) -> int:
    values = list(values)
    return int(values[0] == values[1])


def prod(values) -> int:
    import functools
    return functools.reduce(lambda acc, v: acc * v, values)


def evaluate_packet(packet) -> int:
    operators = {
        0x0: sum,
        0x1: prod,
        0x2: min,
        0x3: max,
        # 4 is a literal value
        0x5: gt,
        0x6: lt,
        0x7: eq,
    }
    _version, operation, payload = packet

    if operation == 0x4:
        return payload

    return operators[operation](map(evaluate_packet, payload))


def main() -> None:
    data = hex_strings_as_binary(sys.stdin)

    for packet in as_packets(data):
        pprint(packet_to_expression(packet))
        print(evaluate_packet(packet))


if __name__ == "__main__":
    main()
