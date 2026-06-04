import serial
import time

DIGITS_3x5 = {
    "0": [0b0111110, 0b0100010, 0b0111110],
    "1": [0b0000000, 0b0111110, 0b0000000],
    "2": [0b0111010, 0b0101010, 0b0101110],
    "3": [0b0101010, 0b0101010, 0b0111110],
    "4": [0b0001110, 0b0001000, 0b0111110],
    "5": [0b0101110, 0b0101010, 0b0111010],
    "6": [0b0111110, 0b0101010, 0b0111010],
    "7": [0b0000010, 0b0000010, 0b0111110],
    "8": [0b0111110, 0b0101010, 0b0111110],
    "9": [0b0101110, 0b0101010, 0b0111110],
}

COLON = 0b00010100

def build_mmhhmm_columns(day: int, hour: int, minute: int) -> list[int]:
    dd = f"{day:02d}"
    hh = f"{hour:02d}"
    mi = f"{minute:02d}"

    cols = []

    cols += [0x00]
    cols += DIGITS_3x5[dd[0]]
    cols += [0x00]
    cols += DIGITS_3x5[dd[1]]
    cols += [0x00, 0x00]

    cols += DIGITS_3x5[hh[0]]
    cols += [0x00]
    cols += DIGITS_3x5[hh[1]]
    cols += [0x00]

    cols += [COLON]
    cols += [0x00]

    cols += DIGITS_3x5[mi[0]]
    cols += [0x00]
    cols += DIGITS_3x5[mi[1]]
    cols += [0x00]

    if len(cols) != 28:
        raise ValueError("column length is not 28")

    return cols

def send_columns(cols: list[int]):
    packet = bytearray([0x80, 0x83, 0xFF])
    packet += bytearray(cols)
    packet += bytearray([0x8F])

    with serial.Serial("/dev/serial0", 9600) as srl:
        srl.write(packet)

def main():
    last_min = None

    while True:
        now = time.localtime()

        if now.tm_min != last_min:
            last_min = now.tm_min
            cols = build_mmhhmm_columns(
                now.tm_mday,
                now.tm_hour,
                now.tm_min
            )
            send_columns(cols)

        time.sleep(1)

if __name__ == "__main__":
    main()