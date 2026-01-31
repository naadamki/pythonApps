#!/usr/bin/env python3
import argparse
import sys

# SINGLE SOURCE OF TRUTH (display name, conversion to, conversion from)
UNIT_DATA = {
    'number': {
        'bin': ('binary',       lambda x: int(str(x).replace(' ', ''), 2),  lambda x: bin(x)[2:]),
        'dec': ('decimal',      lambda x: int(x),                           lambda x: str(x)),
        'hex': ('hexadecimal',  lambda x: int(str(x).replace(' ', ''), 16), lambda x: hex(x)[2:].upper()),
        'oct': ('octal',        lambda x: int(str(x).replace(' ', ''), 8),  lambda x: oct(x)[2:]),
    },
    'temperature': {
        'F': ('Fahrenheit',     lambda x: (float(x) - 32) * 5/9,            lambda x: round((x * 9/5) + 32, 2)),
        'C': ('Celsius',        lambda x: float(x),                         lambda x: round(x, 2)),
        'K': ('Kelvin',         lambda x: float(x) - 273.15,                lambda x: round(x + 273.15, 2)),
    },
    'length': {
        # Metric (descending)
        'km':  ('kilometer',    lambda x: float(x) * 1000,                  lambda x: round(x / 1000, 4)),
        'm':   ('meter',        lambda x: float(x),                         lambda x: round(x, 4)),
        'cm':  ('centimeter',   lambda x: float(x) / 100,                   lambda x: round(x * 100, 4)),
        'mm':  ('millimeter',   lambda x: float(x) / 1000,                  lambda x: round(x * 1000, 4)),
        'um':  ('micrometer',   lambda x: float(x) / 1_000_000,             lambda x: round(x * 1_000_000, 4)),
        'nm':  ('nanometer',    lambda x: float(x) / 1_000_000_000,         lambda x: round(x * 1_000_000_000, 4)),
        # Imperial (descending)
        'mi':  ('mile',         lambda x: float(x) * 1609.34,               lambda x: round(x / 1609.34, 4)),
        'yd':  ('yard',         lambda x: float(x) * 0.9144,                lambda x: round(x / 0.9144, 4)),
        'ft':  ('foot',         lambda x: float(x) * 0.3048,                lambda x: round(x / 0.3048, 4)),
        'in':  ('inch',         lambda x: float(x) * 0.0254,                lambda x: round(x / 0.0254, 4)),
    },
    'weight': {
        # Metric (descending)
        't':   ('metric ton',   lambda x: float(x) * 1000,                  lambda x: round(x / 1000, 4)),
        'kg':  ('kilogram',     lambda x: float(x),                         lambda x: round(x, 4)),
        'g':   ('gram',         lambda x: float(x) / 1000,                  lambda x: round(x * 1000, 4)),
        'mg':  ('milligram',    lambda x: float(x) / 1_000_000,             lambda x: round(x * 1_000_000, 4)),
        'ug':  ('microgram',    lambda x: float(x) / 1_000_000_000,         lambda x: round(x * 1_000_000_000, 4)),
        # Imperial (descending)
        'ton': ('US ton',       lambda x: float(x) * 907.185,               lambda x: round(x / 907.185, 4)),
        'st':  ('stone',        lambda x: float(x) * 6.35029,               lambda x: round(x / 6.35029, 4)),
        'lb':  ('pound',        lambda x: float(x) * 0.453592,              lambda x: round(x / 0.453592, 4)),
        'oz':  ('ounce',        lambda x: float(x) * 0.0283495,             lambda x: round(x / 0.0283495, 4)),
    },
    'liquid': {
        # Metric (descending)
        'kl':  ('kiloliter',    lambda x: float(x) * 1000,                  lambda x: round(x / 1000, 4)),
        'l':   ('liter',        lambda x: float(x),                         lambda x: round(x, 4)),
        'dl':  ('deciliter',    lambda x: float(x) / 10,                    lambda x: round(x * 10, 4)),
        'cl':  ('centiliter',   lambda x: float(x) / 100,                   lambda x: round(x * 100, 4)),
        'ml':  ('milliliter',   lambda x: float(x) / 1000,                  lambda x: round(x * 1000, 4)),
        # Imperial/US (descending)
        'gal': ('gallon',       lambda x: float(x) * 3.78541,               lambda x: round(x / 3.78541, 4)),
        'qt':  ('quart',        lambda x: float(x) * 0.946353,              lambda x: round(x / 0.946353, 4)),
        'pt':  ('pint',         lambda x: float(x) * 0.473176,              lambda x: round(x / 0.473176, 4)),
        'cup': ('cup',          lambda x: float(x) * 0.236588,              lambda x: round(x / 0.236588, 4)),
        'floz':('fluid ounce',  lambda x: float(x) * 0.0295735,             lambda x: round(x / 0.0295735, 4)),
        'tbsp':('tablespoon',   lambda x: float(x) * 0.0147868,             lambda x: round(x / 0.0147868, 4)),
        'tsp': ('teaspoon',     lambda x: float(x) * 0.00492892,            lambda x: round(x / 0.00492892, 4)),
    },
    'area': {
        # Metric (descending)
        'km2': ('square kilometer', lambda x: float(x) * 1_000_000,         lambda x: round(x / 1_000_000, 4)),
        'ha':  ('hectare',      lambda x: float(x) * 10_000,                lambda x: round(x / 10_000, 4)),
        'm2':  ('square meter', lambda x: float(x),                         lambda x: round(x, 4)),
        'cm2': ('square centimeter', lambda x: float(x) / 10_000,           lambda x: round(x * 10_000, 4)),
        'mm2': ('square millimeter', lambda x: float(x) / 1_000_000,        lambda x: round(x * 1_000_000, 4)),
        # Imperial (descending)
        'mi2': ('square mile',  lambda x: float(x) * 2_589_988,             lambda x: round(x / 2_589_988, 4)),
        'ac':  ('acre',         lambda x: float(x) * 4046.86,               lambda x: round(x / 4046.86, 4)),
        'yd2': ('square yard',  lambda x: float(x) * 0.836127,              lambda x: round(x / 0.836127, 4)),
        'ft2': ('square foot',  lambda x: float(x) * 0.092903,              lambda x: round(x / 0.092903, 4)),
        'in2': ('square inch',  lambda x: float(x) * 0.00064516,            lambda x: round(x / 0.00064516, 4)),
    },
    'volume': {
        # Metric (descending)
        'km3': ('cubic kilometer', lambda x: float(x) * 1_000_000_000,      lambda x: round(x / 1_000_000_000, 4)),
        'm3':  ('cubic meter',  lambda x: float(x),                         lambda x: round(x, 4)),
        'cm3': ('cubic centimeter', lambda x: float(x) / 1_000_000,         lambda x: round(x * 1_000_000, 4)),
        'mm3': ('cubic millimeter', lambda x: float(x) / 1_000_000_000,     lambda x: round(x * 1_000_000_000, 4)),
        # Imperial (descending)
        'mi3': ('cubic mile',   lambda x: float(x) * 4_168_181_825,         lambda x: round(x / 4_168_181_825, 4)),
        'yd3': ('cubic yard',   lambda x: float(x) * 0.764555,              lambda x: round(x / 0.764555, 4)),
        'ft3': ('cubic foot',   lambda x: float(x) * 0.0283168,             lambda x: round(x / 0.0283168, 4)),
        'in3': ('cubic inch',   lambda x: float(x) * 0.0000163871,          lambda x: round(x / 0.0000163871, 4)),
    },
    'time': {
        'yr':  ('year',         lambda x: float(x) * 31_536_000,            lambda x: round(x / 31_536_000, 4)),
        'mo':  ('month',        lambda x: float(x) * 2_592_000,             lambda x: round(x / 2_592_000, 4)),
        'wk':  ('week',         lambda x: float(x) * 604_800,               lambda x: round(x / 604_800, 4)),
        'd':   ('day',          lambda x: float(x) * 86_400,                lambda x: round(x / 86_400, 4)),
        'hr':  ('hour',         lambda x: float(x) * 3600,                  lambda x: round(x / 3600, 4)),
        'min': ('minute',       lambda x: float(x) * 60,                    lambda x: round(x / 60, 4)),
        's':   ('second',       lambda x: float(x),                         lambda x: round(x, 4)),
        'ms':  ('millisecond',  lambda x: float(x) / 1000,                  lambda x: round(x * 1000, 4)),
        'us':  ('microsecond',  lambda x: float(x) / 1_000_000,             lambda x: round(x * 1_000_000, 4)),
    },
    'speed': {
        # Metric (descending)
        'km/h': ('kilometer/hour', lambda x: float(x) / 3.6,                lambda x: round(x * 3.6, 4)),
        'm/s':  ('meter/second', lambda x: float(x),                        lambda x: round(x, 4)),
        # Imperial (descending)
        'mph': ('mile/hour',    lambda x: float(x) * 0.44704,               lambda x: round(x / 0.44704, 4)),
        'fps': ('foot/second',  lambda x: float(x) * 0.3048,                lambda x: round(x / 0.3048, 4)),
        # Other
        'kn':  ('knot',         lambda x: float(x) * 0.514444,              lambda x: round(x / 0.514444, 4)),
    },
    'data': {
        'tb':  ('terabyte',     lambda x: float(x) * 8 * 1024**4,           lambda x: round(x / (8 * 1024**4), 2)),
        'gb':  ('gigabyte',     lambda x: float(x) * 8 * 1024**3,           lambda x: round(x / (8 * 1024**3), 2)),
        'mb':  ('megabyte',     lambda x: float(x) * 8 * 1024**2,           lambda x: round(x / (8 * 1024**2), 2)),
        'kb':  ('kilobyte',     lambda x: float(x) * 8 * 1024,              lambda x: round(x / (8 * 1024), 2)),
        'byte':('byte',         lambda x: float(x) * 8,                     lambda x: round(x / 8, 2)),
        'bit': ('bit',          lambda x: float(x),                         lambda x: round(x, 2)),
    },
    'pressure': {
        # Metric (descending)
        'bar': ('bar',          lambda x: float(x) * 100_000,               lambda x: round(x / 100_000, 4)),
        'kpa': ('kilopascal',   lambda x: float(x) * 1000,                  lambda x: round(x / 1000, 4)),
        'pa':  ('pascal',       lambda x: float(x),                         lambda x: round(x, 4)),
        # Imperial/Other (descending)
        'psi': ('pound/sq inch', lambda x: float(x) * 6894.76,              lambda x: round(x / 6894.76, 4)),
        'atm': ('atmosphere',   lambda x: float(x) * 101_325,               lambda x: round(x / 101_325, 4)),
        'mmhg':('mmHg',         lambda x: float(x) * 133.322,               lambda x: round(x / 133.322, 4)),
    },
    'energy': {
        # Metric (descending)
        'kj':  ('kilojoule',    lambda x: float(x) * 1000,                  lambda x: round(x / 1000, 4)),
        'j':   ('joule',        lambda x: float(x),                         lambda x: round(x, 4)),
        # Imperial/Other (descending)
        'kwh': ('kilowatt-hour', lambda x: float(x) * 3_600_000,            lambda x: round(x / 3_600_000, 4)),
        'cal': ('calorie',      lambda x: float(x) * 4.184,                 lambda x: round(x / 4.184, 4)),
        'kcal':('kilocalorie',  lambda x: float(x) * 4184,                  lambda x: round(x / 4184, 4)),
        'btu': ('BTU',          lambda x: float(x) * 1055.06,               lambda x: round(x / 1055.06, 4)),
    },
}


# Special pluralization rules
PLURAL_EXCEPTIONS = {
    'foot': 'feet',
    'inch': 'inches',
}


def pluralize(unit_name, value):
    """Convert unit name to plural form if value != 1"""
    # Handle special cases that don't change (already plural or invariant)
    if unit_name in ['Celsius', 'Fahrenheit', 'Kelvin', 'binary', 'decimal', 
                     'hexadecimal', 'octal', 'stone', 'mmHg', 'BTU']:
        return unit_name
    
    # Check if value is exactly 1 (or -1)
    try:
        num_val = float(value)
        if abs(num_val) == 1:
            return unit_name
    except (ValueError, TypeError):
        # For non-numeric values (like binary strings), just add 's'
        pass
    
    # Check for special plural forms
    if unit_name in PLURAL_EXCEPTIONS:
        return PLURAL_EXCEPTIONS[unit_name]
    
    # Default: add 's' for plural
    return unit_name + 's'


# Lookup: { 'unit_key': (category, display_name, to_func, from_func) }
FLAT_MAP = {
    unit: (cat, data[0], data[1], data[2])
    for cat, units in UNIT_DATA.items()
    for unit, data in units.items()
}

def main():
    parser = argparse.ArgumentParser(
        description="Converter",
        formatter_class=argparse.RawTextHelpFormatter,
        prefix_chars='-/'
    )
    
    for cat_name, units in UNIT_DATA.items():
        group = parser.add_argument_group(f"{cat_name.upper()} OPTIONS")
        for unit_key, data in units.items():
            group.add_argument(f'-{unit_key}', nargs='?', const='OUTPUT', 
                               metavar='VAL', help=f"Convert from/to {data[0]}")

    args_dict = vars(parser.parse_args())
    active_args = {k: v for k, v in args_dict.items() if v is not None}
    
    inputs = [(k, v) for k, v in active_args.items() if v != 'OUTPUT']
    outputs = [k for k, v in active_args.items() if v == 'OUTPUT']

    if not inputs or not outputs:
        parser.print_help()
        sys.exit(1)

    # Use only the first provided input
    in_key, in_val = inputs[0]
    in_cat, in_name, to_inter, _ = FLAT_MAP[in_key]
    
    for out_key in outputs:
        out_cat, out_name, _, from_inter = FLAT_MAP[out_key]

        if in_cat != out_cat:
            print(f"Error: Cannot convert {in_name} to {out_name}")
            continue

        try:
            result = from_inter(to_inter(in_val))
            
            # Pluralize the unit names based on their values
            in_display = pluralize(in_name, in_val)
            out_display = pluralize(out_name, result)
            
            # Format: "1 hour = 60 minutes" or "2 hours = 120 minutes"
            print(f"{in_val} {in_display} = {result} {out_display}")
        except ValueError:
            print(f"Error: '{in_val}' is not a valid {in_name} value.")

if __name__ == "__main__":
    main()