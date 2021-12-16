import datetime
from abc import ABC, abstractmethod
from enum import Enum
from typing import Tuple, List

from utils.input import load_input


def hex_to_binary(hex_string: str) -> str:
    conv_dict = {
        "0": "0000",
        "1": "0001",
        "2": "0010",
        "3": "0011",
        "4": "0100",
        "5": "0101",
        "6": "0110",
        "7": "0111",
        "8": "1000",
        "9": "1001",
        "A": "1010",
        "B": "1011",
        "C": "1100",
        "D": "1101",
        "E": "1110",
        "F": "1111",
    }
    result = hex_string
    for key, val in conv_dict.items():
        result = result.replace(key, val)
    return result


def parse_packet(bit_stream: str) -> Tuple["Packet", str]:
    version, remaining = bit_stream[:3], bit_stream[3:]
    version = int(version, base=2)
    type_id, remaining = remaining[:3], remaining[3:]
    type_id = int(type_id, base=2)
    if type_id == 4:
        packet_cls = LiteralValuePacket
    else:
        packet_cls = OperatorPacket
    return packet_cls.parse_stream(version, type_id, remaining)


def parse_packets(bit_stream: str) -> List["Packet"]:
    packets = []
    remaining = bit_stream
    while remaining and remaining != "0" * len(remaining):
        packet, remaining = parse_packet(remaining)
        packets.append(packet)
    return packets


class LengthType(Enum):
    BIT_LENGTH = "0"
    SUB_PACKETS_NUMBER = "1"


class Packet(ABC):

    def __init__(self, version: int, type_id: int) -> None:
        self.version = version
        self.type_id = type_id

    @abstractmethod
    def total_version(self) -> int:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def parse_stream(cls, version: int, type_id: int, bit_stream: str) -> Tuple["Packet", str]:
        raise NotImplementedError


class LiteralValuePacket(Packet):

    def __init__(self, version: int, type_id: int, value: int) -> None:
        super().__init__(version, type_id)
        self.value = value

    def total_version(self) -> int:
        return self.version

    @classmethod
    def parse_stream(cls, version: int, type_id: int, bit_stream: str) -> Tuple["LiteralValuePacket", str]:
        value_bits = ""
        remaining = bit_stream
        while True:
            next_bits, remaining = remaining[:5], remaining[5:]
            value_bits += next_bits[1:]
            if next_bits[0] == "0":
                return cls(version, type_id, int(value_bits, base=2)), remaining

    def __repr__(self) -> str:
        return f"LiteralValuePacketV{self.version}(value={self.value})"


class OperatorPacket(Packet):

    def __init__(self, version: int, type_id: int, length_type: LengthType, sub_packets: List[Packet]):
        super().__init__(version, type_id)
        self.length_type = length_type
        self.sub_packets = sub_packets

    def total_version(self) -> int:
        return self.version + sum(packet.total_version() for packet in self.sub_packets)

    @classmethod
    def parse_stream(cls, version: int, type_id: int, bit_stream: str) -> Tuple["Packet", str]:
        length_type_id, remaining = bit_stream[:1], bit_stream[1:]
        length_type = LengthType(length_type_id)
        if length_type == LengthType.BIT_LENGTH:
            bit_length, remaining = int(remaining[:15], base=2), remaining[15:]
            sub_stream, remaining = remaining[:bit_length], remaining[bit_length:]
            sub_packets = parse_packets(sub_stream)
            return OperatorPacket(version, type_id, length_type, sub_packets), remaining
        packet_count, remaining = int(remaining[:11], base=2), remaining[11:]
        sub_packets = []
        for packet_num in range(packet_count):
            packet, remaining = parse_packet(remaining)
            sub_packets.append(packet)
        return OperatorPacket(version, type_id, length_type, sub_packets), remaining

    def __repr__(self) -> str:
        return (
            f"OperatorPacketV{self.version}("
            f"type_id={self.type_id}, "
            f"sub_packets=[{','.join(repr(p) for p in self.sub_packets)}]"
            f")"
        )


def _main() -> str:
    my_input = load_input()
    bit_stream = hex_to_binary(my_input)
    packets = parse_packets(bit_stream)
    print(packets)
    return str(sum(p.total_version() for p in packets))


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    print(_main())
    print(f"Time taken: {(datetime.datetime.now() - start_time).total_seconds()}s")
