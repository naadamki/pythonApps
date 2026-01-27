#!/usr/bin/env python3
"""
Convert - A CLI tool for number base conversions
Currently supports: binary ↔ decimal ↔ hexadecimal

Usage:
    convert --bin 10101 --dec       (converts binary to decimal)
    convert --dec 100 --bin         (converts decimal to binary)
    convert --dec 255 --hex         (converts decimal to hex)
"""

import argparse
import sys

# ============================================================================
# NUMBER BASE CONVERSIONS (via integer intermediate)
# ============================================================================
TO_INT = {
    'binary': lambda x: int(x.replace(' ', '').replace('_', ''), 2),
    'decimal': lambda x: int(x),
    'hex': lambda x: int(x.replace(' ', '').replace('_', ''), 16),
    'octal': lambda x: int(x.replace(' ', '').replace('_', ''), 8),
}

FROM_INT = {
    'binary': lambda x: bin(x)[2:],
    'decimal': lambda x: str(x),
    'hex': lambda x: hex(x)[2:].upper(),
    'octal': lambda x: oct(x)[2:],
}

# ============================================================================
# TEMPERATURE CONVERSIONS (via Celsius intermediate)
# ============================================================================
TO_CELSIUS = {
    'celsius': lambda x: float(x),
    'fahrenheit': lambda x: (float(x) - 32) * 5/9,
    'kelvin': lambda x: float(x) - 273.15,
}

FROM_CELSIUS = {
    'celsius': lambda x: round(x, 2),
    'fahrenheit': lambda x: round((x * 9/5) + 32, 2),
    'kelvin': lambda x: round(x + 273.15, 2),
}

# ============================================================================
# LENGTH CONVERSIONS (via meters intermediate)
# ============================================================================
TO_METERS = {
    'meters': lambda x: float(x),
    'kilometers': lambda x: float(x) * 1000,
    'centimeters': lambda x: float(x) / 100,
    'millimeters': lambda x: float(x) / 1000,
    'feet': lambda x: float(x) * 0.3048,
    'inches': lambda x: float(x) * 0.0254,
    'yards': lambda x: float(x) * 0.9144,
    'miles': lambda x: float(x) * 1609.34,
}

FROM_METERS = {
    'meters': lambda x: round(x, 4),
    'kilometers': lambda x: round(x / 1000, 4),
    'centimeters': lambda x: round(x * 100, 4),
    'millimeters': lambda x: round(x * 1000, 4),
    'feet': lambda x: round(x / 0.3048, 4),
    'inches': lambda x: round(x / 0.0254, 4),
    'yards': lambda x: round(x / 0.9144, 4),
    'miles': lambda x: round(x / 1609.34, 4),
}

# ============================================================================
# WEIGHT CONVERSIONS (via kilograms intermediate)
# ============================================================================
TO_KILOGRAMS = {
    'kilograms': lambda x: float(x),
    'grams': lambda x: float(x) / 1000,
    'milligrams': lambda x: float(x) / 1_000_000,
    'pounds': lambda x: float(x) * 0.453592,
    'ounces': lambda x: float(x) * 0.0283495,
    'tons': lambda x: float(x) * 1000,
}

FROM_KILOGRAMS = {
    'kilograms': lambda x: round(x, 4),
    'grams': lambda x: round(x * 1000, 4),
    'milligrams': lambda x: round(x * 1_000_000, 4),
    'pounds': lambda x: round(x / 0.453592, 4),
    'ounces': lambda x: round(x / 0.0283495, 4),
    'tons': lambda x: round(x / 1000, 4),
}

# ============================================================================
# TIME CONVERSIONS (via seconds intermediate)
# ============================================================================
TO_SECONDS = {
    'seconds': lambda x: float(x),
    'minutes': lambda x: float(x) * 60,
    'hours': lambda x: float(x) * 3600,
    'days': lambda x: float(x) * 86400,
    'weeks': lambda x: float(x) * 604800,
}

FROM_SECONDS = {
    'seconds': lambda x: round(x, 4),
    'minutes': lambda x: round(x / 60, 4),
    'hours': lambda x: round(x / 3600, 4),
    'days': lambda x: round(x / 86400, 4),
    'weeks': lambda x: round(x / 604800, 4),
}

# ============================================================================
# FORMAT CATEGORIES - Maps each format to its conversion category
# ============================================================================
FORMAT_CATEGORIES = {
    # Number bases
    'binary': 'number',
    'decimal': 'number',
    'hex': 'number',
    'octal': 'number',
    
    # Temperature
    'celsius': 'temperature',
    'fahrenheit': 'temperature',
    'kelvin': 'temperature',
    
    # Length
    'meters': 'length',
    'kilometers': 'length',
    'centimeters': 'length',
    'millimeters': 'length',
    'feet': 'length',
    'inches': 'length',
    'yards': 'length',
    'miles': 'length',
    
    # Weight
    'kilograms': 'weight',
    'grams': 'weight',
    'milligrams': 'weight',
    'pounds': 'weight',
    'ounces': 'weight',
    'tons': 'weight',
    
    # Time
    'seconds': 'time',
    'minutes': 'time',
    'hours': 'time',
    'days': 'time',
    'weeks': 'time',
}

# Category conversion tables
CATEGORY_CONVERTERS = {
    'number': (TO_INT, FROM_INT),
    'temperature': (TO_CELSIUS, FROM_CELSIUS),
    'length': (TO_METERS, FROM_METERS),
    'weight': (TO_KILOGRAMS, FROM_KILOGRAMS),
    'time': (TO_SECONDS, FROM_SECONDS),
}

def convert(value, from_format, to_format):
    """Convert from one format to another"""
    # Get categories
    from_category = FORMAT_CATEGORIES.get(from_format)
    to_category = FORMAT_CATEGORIES.get(to_format)
    
    if from_category is None:
        raise ValueError(f"Unknown format: {from_format}")
    if to_category is None:
        raise ValueError(f"Unknown format: {to_format}")
    
    # Check if formats are in the same category
    if from_category != to_category:
        raise ValueError(f"Cannot convert between {from_category} and {to_category}")
    
    # Get the appropriate converters for this category
    to_intermediate, from_intermediate = CATEGORY_CONVERTERS[from_category]
    
    try:
        # Convert to intermediate, then to target format
        intermediate_value = to_intermediate[from_format](value)
        result = from_intermediate[to_format](intermediate_value)
        return result
    except ValueError as e:
        if "invalid literal" in str(e) or "could not convert" in str(e):
            raise ValueError(f"Invalid {from_format} value: {value}")
        raise
    except KeyError:
        raise ValueError(f"Conversion from {from_format} to {to_format} not implemented")

def main():
    parser = argparse.ArgumentParser(
        description='Convert between different units and number bases',
        epilog='Examples:\n'
               '  convert --bin 10101 --dec           (binary to decimal)\n'
               '  convert --dec 100 --hex             (decimal to hex)\n'
               '  convert --f 98.6 --c                (Fahrenheit to Celsius)\n'
               '  convert --ft 10 --m                 (feet to meters)\n'
               '  convert --lb 150 --kg               (pounds to kilograms)\n'
               '  convert --h 2.5 --min               (hours to minutes)\n',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # All format flags can be used as input (with value) or output (without value)
    
    # Number bases
    parser.add_argument('--bin', nargs='?', const='OUTPUT', metavar='VALUE', 
                       help='Binary format')
    parser.add_argument('--dec', nargs='?', const='OUTPUT', metavar='VALUE',
                       help='Decimal format')
    parser.add_argument('--hex', nargs='?', const='OUTPUT', metavar='VALUE',
                       help='Hexadecimal format')
    parser.add_argument('--oct', nargs='?', const='OUTPUT', metavar='VALUE',
                       help='Octal format')
    
    # Temperature
    parser.add_argument('--c', nargs='?', const='OUTPUT', metavar='VALUE',
                       help='Celsius temperature')
    parser.add_argument('--f', nargs='?', const='OUTPUT', metavar='VALUE',
                       help='Fahrenheit temperature')
    parser.add_argument('--k', nargs='?', const='OUTPUT', metavar='VALUE',
                       help='Kelvin temperature')
    
    # Length
    parser.add_argument('--m', nargs='?', const='OUTPUT', metavar='VALUE',
                       help='Meters')
    parser.add_argument('--km', nargs='?', const='OUTPUT', metavar='VALUE',
                       help='Kilometers')
    parser.add_argument('--cm', nargs='?', const='OUTPUT', metavar='VALUE',
                       help='Centimeters')
    parser.add_argument('--mm', nargs='?', const='OUTPUT', metavar='VALUE',
                       help='Millimeters')
    parser.add_argument('--ft', nargs='?', const='OUTPUT', metavar='VALUE',
                       help='Feet')
    parser.add_argument('--in', nargs='?', const='OUTPUT', metavar='VALUE',
                       help='Inches')
    parser.add_argument('--yd', nargs='?', const='OUTPUT', metavar='VALUE',
                       help='Yards')
    parser.add_argument('--mi', nargs='?', const='OUTPUT', metavar='VALUE',
                       help='Miles')
    
    # Weight
    parser.add_argument('--kg', nargs='?', const='OUTPUT', metavar='VALUE',
                       help='Kilograms')
    parser.add_argument('--g', nargs='?', const='OUTPUT', metavar='VALUE',
                       help='Grams')
    parser.add_argument('--mg', nargs='?', const='OUTPUT', metavar='VALUE',
                       help='Milligrams')
    parser.add_argument('--lb', nargs='?', const='OUTPUT', metavar='VALUE',
                       help='Pounds')
    parser.add_argument('--oz', nargs='?', const='OUTPUT', metavar='VALUE',
                       help='Ounces')
    parser.add_argument('--t', nargs='?', const='OUTPUT', metavar='VALUE',
                       help='Metric tons')
    
    # Time
    parser.add_argument('--s', nargs='?', const='OUTPUT', metavar='VALUE',
                       help='Seconds')
    parser.add_argument('--min', nargs='?', const='OUTPUT', metavar='VALUE',
                       help='Minutes')
    parser.add_argument('--h', nargs='?', const='OUTPUT', metavar='VALUE',
                       help='Hours')
    parser.add_argument('--d', nargs='?', const='OUTPUT', metavar='VALUE',
                       help='Days')
    parser.add_argument('--w', nargs='?', const='OUTPUT', metavar='VALUE',
                       help='Weeks')
    
    args = parser.parse_args()
    
    # Determine which argument has a value (input) and which is just a flag (output)
    input_type = None
    input_value = None
    output_type = None
    
    # Map CLI argument names to internal format names
    ARG_TO_FORMAT = {
        'bin': 'binary',
        'dec': 'decimal',
        'hex': 'hex',
        'oct': 'octal',
        'c': 'celsius',
        'f': 'fahrenheit',
        'k': 'kelvin',
        'm': 'meters',
        'km': 'kilometers',
        'cm': 'centimeters',
        'mm': 'millimeters',
        'ft': 'feet',
        'in': 'inches',
        'yd': 'yards',
        'mi': 'miles',
        'kg': 'kilograms',
        'g': 'grams',
        'mg': 'milligrams',
        'lb': 'pounds',
        'oz': 'ounces',
        't': 'tons',
        's': 'seconds',
        'min': 'minutes',
        'h': 'hours',
        'd': 'days',
        'w': 'weeks',
    }
    
    # Get all argument values
    arg_values = {
        'bin': args.bin,
        'dec': args.dec,
        'hex': args.hex,
        'oct': args.oct,
        'c': args.c,
        'f': args.f,
        'k': args.k,
        'm': args.m,
        'km': args.km,
        'cm': args.cm,
        'mm': args.mm,
        'ft': args.ft,
        'in': getattr(args, 'in'),  # 'in' is a Python keyword, use getattr
        'yd': args.yd,
        'mi': args.mi,
        'kg': args.kg,
        'g': args.g,
        'mg': args.mg,
        'lb': args.lb,
        'oz': args.oz,
        't': args.t,
        's': args.s,
        'min': args.min,
        'h': args.h,
        'd': args.d,
        'w': args.w,
    }
    
    for arg_name, value in arg_values.items():
        if value is not None:
            format_name = ARG_TO_FORMAT[arg_name]
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
    
    # Display names for formats (for prettier output)
    DISPLAY_NAMES = {
        'binary': 'Binary',
        'decimal': 'Decimal',
        'hex': 'Hex',
        'octal': 'Octal',
        'celsius': 'C',
        'fahrenheit': 'F',
        'kelvin': 'K',
        'meters': 'm',
        'kilometers': 'km',
        'centimeters': 'cm',
        'millimeters': 'mm',
        'feet': 'ft',
        'inches': 'in',
        'yards': 'yd',
        'miles': 'mi',
        'kilograms': 'kg',
        'grams': 'g',
        'milligrams': 'mg',
        'pounds': 'lb',
        'ounces': 'oz',
        'tons': 't',
        'seconds': 's',
        'minutes': 'min',
        'hours': 'h',
        'days': 'd',
        'weeks': 'w',
    }
    
    try:
        # Perform conversion
        result = convert(input_value, input_type, output_type)
        
        # Format output
        input_display = DISPLAY_NAMES.get(input_type, input_type.capitalize())
        output_display = DISPLAY_NAMES.get(output_type, output_type.capitalize())
        
        print(f"{input_value} {input_display} = {result} {output_display}")
    
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
