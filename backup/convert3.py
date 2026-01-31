import argparse


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
        # Metric 
        'km':  ('kilometer',    lambda x: float(x) * 1000,                  lambda x: round(x / 1000, 4)),
        'm':   ('meter',        lambda x: float(x),                         lambda x: round(x, 4)),
        'cm':  ('centimeter',   lambda x: float(x) / 100,                   lambda x: round(x * 100, 4)),
        'mm':  ('millimeter',   lambda x: float(x) / 1000,                  lambda x: round(x * 1000, 4)),
        'um':  ('micrometer',   lambda x: float(x) / 1_000_000,             lambda x: round(x * 1_000_000, 4)),
        'nm':  ('nanometer',    lambda x: float(x) / 1_000_000_000,         lambda x: round(x * 1_000_000_000, 4)),
        # Imperial 
        'mi':  ('mile',         lambda x: float(x) * 1609.34,               lambda x: round(x / 1609.34, 4)),
        'yd':  ('yard',         lambda x: float(x) * 0.9144,                lambda x: round(x / 0.9144, 4)),
        'ft':  ('foot',         lambda x: float(x) * 0.3048,                lambda x: round(x / 0.3048, 4)),
        'in':  ('inch',         lambda x: float(x) * 0.0254,                lambda x: round(x / 0.0254, 4)),
    },
    'weight': {
        # Metric 
        't':   ('metricton',   lambda x: float(x) * 1000,                  lambda x: round(x / 1000, 4)),
        'kg':  ('kilogram',     lambda x: float(x),                         lambda x: round(x, 4)),
        'g':   ('gram',         lambda x: float(x) / 1000,                  lambda x: round(x * 1000, 4)),
        'mg':  ('milligram',    lambda x: float(x) / 1_000_000,             lambda x: round(x * 1_000_000, 4)),
        'ug':  ('microgram',    lambda x: float(x) / 1_000_000_000,         lambda x: round(x * 1_000_000_000, 4)),
        # Imperial 
        'ton': ('ton',       lambda x: float(x) * 907.185,               lambda x: round(x / 907.185, 4)),
        'st':  ('stone',        lambda x: float(x) * 6.35029,               lambda x: round(x / 6.35029, 4)),
        'lb':  ('pound',        lambda x: float(x) * 0.453592,              lambda x: round(x / 0.453592, 4)),
        'oz':  ('ounce',        lambda x: float(x) * 0.0283495,             lambda x: round(x / 0.0283495, 4)),
    },
    'liquid': {
        # Metric 
        'kl':  ('kiloliter',    lambda x: float(x) * 1000,                  lambda x: round(x / 1000, 4)),
        'l':   ('liter',        lambda x: float(x),                         lambda x: round(x, 4)),
        'dl':  ('deciliter',    lambda x: float(x) / 10,                    lambda x: round(x * 10, 4)),
        'cl':  ('centiliter',   lambda x: float(x) / 100,                   lambda x: round(x * 100, 4)),
        'ml':  ('milliliter',   lambda x: float(x) / 1000,                  lambda x: round(x * 1000, 4)),
        # Imperial/US 
        'gal': ('gallon',       lambda x: float(x) * 3.78541,               lambda x: round(x / 3.78541, 4)),
        'qt':  ('quart',        lambda x: float(x) * 0.946353,              lambda x: round(x / 0.946353, 4)),
        'pt':  ('pint',         lambda x: float(x) * 0.473176,              lambda x: round(x / 0.473176, 4)),
        'cup': ('cup',          lambda x: float(x) * 0.236588,              lambda x: round(x / 0.236588, 4)),
        'floz':('fluidounce',  lambda x: float(x) * 0.0295735,             lambda x: round(x / 0.0295735, 4)),
        'tbsp':('tablespoon',   lambda x: float(x) * 0.0147868,             lambda x: round(x / 0.0147868, 4)),
        'tsp': ('teaspoon',     lambda x: float(x) * 0.00492892,            lambda x: round(x / 0.00492892, 4)),
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
    'data': {
        'tb':  ('terabyte',     lambda x: float(x) * 8 * 1024**4,           lambda x: round(x / (8 * 1024**4), 2)),
        'gb':  ('gigabyte',     lambda x: float(x) * 8 * 1024**3,           lambda x: round(x / (8 * 1024**3), 2)),
        'mb':  ('megabyte',     lambda x: float(x) * 8 * 1024**2,           lambda x: round(x / (8 * 1024**2), 2)),
        'kb':  ('kilobyte',     lambda x: float(x) * 8 * 1024,              lambda x: round(x / (8 * 1024), 2)),
        'byte':('byte',         lambda x: float(x) * 8,                     lambda x: round(x / 8, 2)),
        'bit': ('bit',          lambda x: float(x),                         lambda x: round(x, 2)),
    },
    'pressure': {
        # Metric 
        'bar': ('bar',          lambda x: float(x) * 100_000,               lambda x: round(x / 100_000, 4)),
        'kpa': ('kilopascal',   lambda x: float(x) * 1000,                  lambda x: round(x / 1000, 4)),
        'pa':  ('pascal',       lambda x: float(x),                         lambda x: round(x, 4)),
        # Imperial/Other 
        'atm': ('atmosphere',   lambda x: float(x) * 101_325,               lambda x: round(x / 101_325, 4)),
        'mmhg':('mmHg',         lambda x: float(x) * 133.322,               lambda x: round(x / 133.322, 4)),
    },
    'energy': {
        # Metric 
        'kj':  ('kilojoule',    lambda x: float(x) * 1000,                  lambda x: round(x / 1000, 4)),
        'j':   ('joule',        lambda x: float(x),                         lambda x: round(x, 4)),
        # Imperial/Other 
        'kwh': ('kilowatt-hour', lambda x: float(x) * 3_600_000,            lambda x: round(x / 3_600_000, 4)),
        'cal': ('calorie',      lambda x: float(x) * 4.184,                 lambda x: round(x / 4.184, 4)),
        'kcal':('kilocalorie',  lambda x: float(x) * 4184,                  lambda x: round(x / 4184, 4)),
        'btu': ('BTU',          lambda x: float(x) * 1055.06,               lambda x: round(x / 1055.06, 4)),
    },
}




FLAT_MAP = {
    unit: (cat, data[0], data[1], data[2])
    for cat, units in UNIT_DATA.items()
    for unit, data in units.items()
}

def pluralize(value, unit):
    PLURAL_EXCEPTIONS = {'foot': 'feet', 'inch': 'inches'}

    if unit in ['Celsius', 'Fahrenheit', 'Kelvin', 'binary', 'decimal', 'hexadecimal', 'octal', 'stone', 'mmHg', 'BTU']:
        return unit

    try:
        num_val = float(value)
        if abs(num_val) == 1:
            return unit
    except (ValueError, TypeError):
        pass

    if unit in PLURAL_EXCEPTIONS:
        return PLURAL_EXCEPTIONS[unit]

    return unit + 's'


def main():
    custom_usage = '%(prog)s VALUE FROM -TO [-TO] [-TO]...'
    
    parser = argparse.ArgumentParser(
        description='Unit converter - units can only convert within the same category',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage=custom_usage
    )

    parser.add_argument('value',
        type=int,
        help='Value to convert')

    all_unit_keys = [unit_key for units in UNIT_DATA.values() for unit_key in units.keys()]

    all_units = [unit for unit_key, data in FLAT_MAP.items() for unit in (unit_key, data[1])]


    ## THIS ARGUMENT HERE
    parser.add_argument('from_unit',
        choices=all_units,
        help=argparse.SUPPRESS
    )

    for cat, units in UNIT_DATA.items():
        group = parser.add_argument_group(
            f"{cat.upper()}:",
            f"Available {cat} units to convert from: {', '.join(units.keys())}"
        )
        for unit_key, data in units.items():
            group.add_argument(
                f'-{unit_key}', f'--{data[0]}',
                action='append_const',
                const=f'{unit_key}',
                dest='to_units',
                help=f'convert to {data[0]}'
            )

    args = parser.parse_args()

    if args.from_unit not in FLAT_MAP.keys():
        for key, data in FLAT_MAP.items():
            if data[1] == args.from_unit:
                from_unit = key
    else:
        from_unit = args.from_unit 


    from_cat, from_name, to_inter, _ = FLAT_MAP[from_unit]

    if args.to_units:
        for unit in args.to_units:
            to_cat, to_name, _, from_inter = FLAT_MAP[unit]

            if to_cat != from_cat:
                print(f"Error: Cannot convert {from_name} to {to_name}")
                continue        

            try:
                result = from_inter(to_inter(args.value))

                from_display = pluralize(args.value, from_name)
                to_display = pluralize(result, to_name)

                print(f'{args.value} {from_display} = {result} {to_display}')
            except ValueError:
                print(f"Error: '{args.value}' is not a valid {from_name} value.")



if __name__ == '__main__':
    main()
