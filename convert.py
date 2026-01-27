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


# Conversion maps for all supported formats
# TO converts any format to an intermediate (int)
TO = {
    'binary': lambda x: int(x.replace(' ', '').replace('_', ''), 2),
    'decimal': lambda x: int(x),
    'hex': lambda x: int(x.replace(' ', '').replace('_', ''), 16),
}

# FROM converts from intermediate (int) to any format
FROM = {
    'binary': lambda x: bin(x)[2:],
    'decimal': lambda x: str(x),
    'hex': lambda x: hex(x)[2:].upper(),
}


def to_intermediate(value, from_format):
    """Convert any supported format to intermediate integer format"""
    try:
        converter = TO.get(from_format)
        if converter is None:
            raise ValueError(f"Unknown format: {from_format}")
        return converter(value)
    except ValueError as e:
        if "invalid literal" in str(e):
            raise ValueError(f"Invalid {from_format} number: {value}")
        raise

def from_intermediate(int_value, to_format):
    """Convert intermediate integer format to any supported format"""
    try:
        if int_value < 0:
            raise ValueError("Negative numbers not supported yet")
        
        converter = FROM.get(to_format)
        if converter is None:
            raise ValueError(f"Unknown format: {to_format}")
        return converter(int_value)
    except ValueError:
        raise

def convert(value, from_format, to_format):
    """Convert from one format to another via intermediate integer"""
    int_value = to_intermediate(value, from_format)
    return from_intermediate(int_value, to_format)




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


    args = parser.parse_args()

    # Determine which argument has a value (input) and which is just a flag (output)
    input_type = None
    input_value = None
    output_type = None

    formats = {
        'binary': args.bin,
        'decimal': args.dec,
        'hex': args.hex
    }

    for format_name, value in formats.items():
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

    try:
        # Perform conversion using generic convert function
        result = convert(input_value, input_type, output_type)

        # Format output with proper capitalization
        input_display = input_type.capitalize()
        output_display = output_type.capitalize()

        print(f"{input_display} {input_value} = {output_display} {result}")

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
    

    
