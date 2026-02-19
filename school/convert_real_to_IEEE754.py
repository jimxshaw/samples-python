#!/usr/bin/env python3
"""
convert_real_to_IEEE754.py - Convert a real number to IEEE 754 half-precision (binary16) and
convert a binary16 back to a real number.

Usage:
  python3 half.py <number>
    e.g. python3 half.py -250.75

  python3 half.py --frombits <16-bit-binary-or-hex>
    e.g. python3 half.py --frombits 1101110111011000
         python3 half.py --frombits 0xDEDC
"""

import sys
import math

# ---- Helpers: formatting ----

def bits_to_str(bits: int, width: int) -> str:
    return format(bits & ((1 << width) - 1), f"0{width}b")


def parse_bits_arg(s: str) -> int:
    s = s.strip().lower()

    if s.startswith("0x"):
        val = int(s, 16)

        if not (0 <= val <= 0xFFFF):
            raise ValueError("hex value must fit in 16 bits")
        
        return val
    
    # Allow underscores in binary.
    s2 = s.replace("_", "")

    if all(c in "01" for c in s2) and len(s2) == 16:
        return int(s2, 2)
    
    raise ValueError("Expected 16-bit binary (e.g. 0101...16 bits) or hex (e.g. 0x3C00)")


# ---- Float -> Half (binary16) ----
#
# Half format: 1 sign, 5 exponent (bias 15), 10 fraction.
# Value (normal): (-1)^s * 2^(e-bias) * (1.fraction)
# Subnormal when e==0 and fraction!=0: (-1)^s * 2^(1-bias) * (0.fraction)
# Special: e==31: fraction==0 => inf, else NaN

HALF_EXP_BITS = 5
HALF_FRAC_BITS = 10
HALF_EXP_BIAS = 15
HALF_EXP_MAX = (1 << HALF_EXP_BITS) - 1  # 31


def float_to_half_bits(x: float) -> int:
    # Handle NaN.
    if math.isnan(x):
        # Quiet NaN: exponent all ones, non-zero fraction
        return (HALF_EXP_MAX << HALF_FRAC_BITS) | (1 << (HALF_FRAC_BITS - 1))

    # Sign.
    sign = 1 if math.copysign(1.0, x) < 0 else 0
    ax = abs(x)

    # Handle infinities.
    if math.isinf(ax):
        return (sign << 15) | (HALF_EXP_MAX << HALF_FRAC_BITS)

    # Handle zero (preserve signed zero).
    if ax == 0.0:
        return (sign << 15)

    # Compute unbiased exponent e such that: ax = m * 2^e, with m in [1,2).
    m, e = math.frexp(ax)  # ax = m * 2^e, m in [0.5, 1).

    # Convert to [1,2) mantissa:
    m *= 2.0
    e -= 1

    # Half exponent field for normal numbers:
    exp_field = e + HALF_EXP_BIAS

    # Normal range for half: exp_field in [1..30].
    if exp_field >= 1 and exp_field <= HALF_EXP_MAX - 1:
        # Fraction = round((m - 1) * 2^10)
        frac = int(round((m - 1.0) * (1 << HALF_FRAC_BITS)))

        # Rounding can push frac to 1024, which means mantissa became 2.0 -> adjust exponent.
        if frac == (1 << HALF_FRAC_BITS):
            frac = 0
            exp_field += 1
            if exp_field >= HALF_EXP_MAX:
                # overflow to infinity.
                return (sign << 15) | (HALF_EXP_MAX << HALF_FRAC_BITS)

        return (sign << 15) | (exp_field << HALF_FRAC_BITS) | frac

    # Too large -> infinity.
    if exp_field > HALF_EXP_MAX - 1:
        return (sign << 15) | (HALF_EXP_MAX << HALF_FRAC_BITS)

    # Subnormal range: exp_field <= 0.
    # For subnormals: value = 2^(1-bias) * (fraction / 2^10).
    # We want fraction = round(ax / 2^(1-bias) * 2^10).
    # ax * 2^(bias-1+10).
    frac = int(round(ax * (2.0 ** (HALF_EXP_BIAS - 1 + HALF_FRAC_BITS))))

    # Clamp: if rounding gives 1024, it becomes the smallest normal number.
    if frac >= (1 << HALF_FRAC_BITS):
        # smallest normal: exp_field=1, frac=0.
        return (sign << 15) | (1 << HALF_FRAC_BITS)

    # Underflow to zero if too tiny.
    if frac == 0:
        return (sign << 15)

    return (sign << 15) | frac


# ---- Half -> Float ----

def half_bits_to_float(h: int) -> float:
    sign = (h >> 15) & 0x1
    exp = (h >> HALF_FRAC_BITS) & ((1 << HALF_EXP_BITS) - 1)
    frac = h & ((1 << HALF_FRAC_BITS) - 1)

    if exp == HALF_EXP_MAX:
        if frac == 0:
            return float("-inf") if sign else float("inf")
        return float("nan")

    if exp == 0:
        if frac == 0:
            # Signed zero.
            return -0.0 if sign else 0.0
        
        # Subnormal: (-1)^s * 2^(1-bias) * (frac / 2^10).
        val = (2.0 ** (1 - HALF_EXP_BIAS)) * (frac / (1 << HALF_FRAC_BITS))

        return -val if sign else val

    # Normal: (-1)^s * 2^(exp-bias) * (1 + frac/2^10).
    val = (2.0 ** (exp - HALF_EXP_BIAS)) * (1.0 + frac / (1 << HALF_FRAC_BITS))

    return -val if sign else val


def print_half(h: int) -> None:
    sign = (h >> 15) & 0x1
    exp = (h >> HALF_FRAC_BITS) & ((1 << HALF_EXP_BITS) - 1)
    frac = h & ((1 << HALF_FRAC_BITS) - 1)

    print(f"half bits (bin): {bits_to_str(h, 16)}")
    print(f"half bits (hex): 0x{h:04X}")
    print(f"sign     : {sign}  (bit 15)")
    print(f"exponent : {bits_to_str(exp, HALF_EXP_BITS)}  (bias {HALF_EXP_BIAS})")
    print(f"fraction : {bits_to_str(frac, HALF_FRAC_BITS)}")
    print(f"as float : {half_bits_to_float(h)}")


def main(argv: list[str]) -> int:
    if len(argv) == 3 and argv[1] == "--frombits":
        try:
            h = parse_bits_arg(argv[2])
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)

            return 2
        
        print_half(h)

        return 0

    if len(argv) != 2:
        print(__doc__.strip(), file=sys.stderr)

        return 2

    try:
        x = float(argv[1])
    except ValueError:
        print("Error: <number> must be a real number (e.g. -250.75)", file=sys.stderr)

        return 2

    h = float_to_half_bits(x)

    print(f"input    : {x}")
    print_half(h)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

