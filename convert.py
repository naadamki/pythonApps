#!/usr/bin/env python3

"""
Convert - A CLI tool for number base conversions
Currently supports: binary ↔ decimal ↔ hexadecimal

Usage:
    convert --bin 101 --dec     (converts binary to decimal)
    convert --dec 100 --bin     (converts decimal to binary)
    convert --dec 255 --hex     (converts decimal to hex)
"""


import argparse
import sys


# Conversion functions
def binary_to_decimal(binary_str):
    """Convert binary string to decimal"""
    try:
        binary_str = binary_str.replace(' ', '').replace('_', '')
        return int(binary_str, 2)
    except ValueError:
        raise ValueError(f"Invalid binary number: {binary_str}")

def decimal_to_binary(decimal_str):
    """Convert decimal string to binary"""
    try:
        decimal = int(decimal_str)
        if decimal < 0:
            raise ValueError("Negative numbers are not supported yet")
        return bin(decimal)[2:]
    except ValueError as e:
        if "invalid literal" in str(e):
            raise ValueError(f"Invalid decimal number: {decimal_str}")
        raise

def decimal_to_hex(decimal_str):
    """Convert decimal string to hexadecimal"""
    try:
        decimal = int(decimal_str)
        if decimal < 0:
            raise ValueError("Negative numbers not supported yet")
        return hex(decimal)[2:].upper()
    except ValueError as e:
        if "invalid literal" in str(e):
            raise ValueError(f"Invalid decimal number: {decimal_str}")
        raise

def hex_to_decimal(hex_str):
    """Convert hexadecimal string to decimal"""
    try:
        hex_str = hex_str.replace(' ', '').replace('_', '')
        return int(hex_str, 16)
    except ValueError:
        raise ValueError(f"Invalid hexadecimal number: {hex_str}")

def binary_to_hex(binary_str):
    """Convert binary to hexadecimal"""
    decimal = binary_to_decimal(binary_str)
    return hex(decimal)[2:].upper()

def hex_to_binary(hex_str):
    """Convert hexadecimal to binary"""
    decimal = hex_to_decimal(hex_str)
    return bin(decimal)[2:]




def main():
    parser = argparse.ArgumentParser(
        description='Convert between different number bases',
        epilog='Examples:\n'
            '   convert --bin 10101 --dec\n'
            '   convert --dec 100 --bin\n'
            '   convert --dec 255 --hex\n'
            '   convert --hex FF --dec\n',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # All format flags can be used as input (with value) or output (without value)
    parser.add_argument(
        '--bin',
        nargs='?',
        const='OUTPUT',
        metavar='VALUE',
        help='Binary format (with value as input, without value as output)'
    )

    parser.add_argument(
        '--dec',
        nargs='?',
        const='OUTPUT',
        metavar='VALUE',
        help='Decimal format (with value as input, without value as output)'
    )

    parser.add_argument(
        '--hex',
        nargs='?',
        const='OUTPUT',
        metavar='VALUE',
        help='Hexadecimal format (with value as input, without value as output)'
    )

    # Determine which argument has a value (input) and which is just a flag (output)
    input_type = None
    input_value = None
    output_type = None

    formats = {
        'binary': args.bin,
        'decimal': args.dec,
        'hex': args.hex
    }

    for format_name, value in formats.items()
        if value is not None:
            if value == 'OUTPUT':
                # This is the output format (flag without value)
                if output_type is not None:
                    parser.error("Multiple output formats specified")
                output_type = format_name
            else:
                # This is the input format (flag with value)
                if input_type is not None:
                    parser.error("Multiple input values specified")
                input_type = format_name
                input_value = value

    # Validate we have both input and output
    if input_type is None:
        parser.error("No input value specified")
    if output_type is None:
        parser.error("No output format specified")

    # Prevent converting to same format
    if input_type == output_type:
        print(f"Input and output are both {input_type}. No conversion needed.")
        print(f"{input_type.capitalize()}: {input_value}")
        return

    # Conversion table: (input_type, output_type) -> conversion_function
    conversions = {
        ('binary', 'decimal'): binary_to_decimal,
        ('decimal', 'binary'): decimal_to_binary,
        ('decimal', 'hex'): decimal_to_hex,
        ('hex', 'decimal'): hex_to_decimal,
        ('binary', 'hex'): binary_to_hex,
        ('hex', 'binary'): hex_to_binary,
    }


    try:
        # Look up the conversion function
        conversion_key = (input_type, output_type)
        conversion_func = conversions.get(conversion_key)

        if conversion_func is None:
            print(f"Conversion from {input_type} to {output_type} not yet implemented")
            sys.exit(1)

        # Perform the conversion
        result = conversion_fun(input_value)

        # Format output with proper capitalization
        input_display = input_type.capitalize()
        output_display = output_type.capitalize()

        print(f"{input_display} {input_value} = {output_display} {result}")

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
    

    
