#!/usr/bin/env python3
import argparse


def main():
    parser = argparse.ArgumentParser(description="CLI app with examples of argparse options")

    # ============================================================================
    # POSITIONAL ARGUMENTS (required, no dash prefix)
    # ============================================================================
    parser.add_argument('name', 
                       help='Your name (required positional argument)')

    # ============================================================================
    # BOOLEAN FLAGS (action='store_true' or 'store_false')
    # ============================================================================
    parser.add_argument('-u', '--uppercase',
                       action='store_true',  # Becomes True when flag is present
                       help='Convert to uppercase (boolean flag)')

    parser.add_argument('-q', '--quiet',
                       action='store_false',  # Becomes False when flag is present
                       dest='verbose_mode',   # Store in different attribute name
                       help='Disable verbose mode (store_false example)')

    # ============================================================================
    # COUNT ACTION (counts how many times flag appears)
    # ============================================================================
    parser.add_argument('-v', '--verbose',
                       action='count',        # Returns integer: 0, 1, 2, 3...
                       default=0,             # Start at 0 (use int, not string)
                       help='Increase verbosity (-v, -vv, -vvv)')

    # ============================================================================
    # STORE CONSTANT (store a specific value when flag is present)
    # ============================================================================
    parser.add_argument('-f', '--format',
                       action='store_const',  # Store const value when present
                       const='JSON',          # Value to store when flag used
                       default='TEXT',        # Value when flag NOT used
                       help='Output in JSON format (default: TEXT)')

    # ============================================================================
    # APPEND CONSTANT (build a list by adding const each time)
    # ============================================================================
    parser.add_argument('--add-tag',
                       action='append_const', # Appends to a list
                       const='important',     # Value to append
                       dest='tags',           # Store list in 'tags' attribute
                       help='Add "important" tag (can use multiple times)')

    # ============================================================================
    # FLAGS WITH ARGUMENTS (takes a value after the flag)
    # ============================================================================
    parser.add_argument('-r', '--repeat',
                       type=int,              # Convert argument to integer
                       default=1,             # Default if not provided
                       help='Number of times to repeat (default: 1)')

    parser.add_argument('-c', '--color',
                       type=str,              # String type (default anyway)
                       choices=['red', 'green', 'blue'],  # Limit valid options
                       help='Choose a color (red, green, or blue)')

    parser.add_argument('-n', '--numbers',
                       nargs='+',             # Accept 1 or more values
                       type=int,              # Each value converted to int
                       help='List of numbers (e.g., -n 1 2 3 4)')

    # ============================================================================
    # OPTIONAL ARGUMENT WITH SPECIAL BEHAVIOR
    # ============================================================================
    parser.add_argument('-o', '--output',
                       nargs='?',             # 0 or 1 argument
                       const='output.txt',    # Value if flag given without argument
                       default=None,          # Value if flag not used at all
                       help='Output file (default: output.txt if flag used)')

    # ============================================================================
    # APPEND ACTION (build a list from multiple uses)
    # ============================================================================
    parser.add_argument('-e', '--exclude',
                       action='append',       # Each use adds to list
                       help='Exclude pattern (can use multiple times)')

    # Parse all arguments
    args = parser.parse_args()

    # ============================================================================
    # USING THE ARGUMENTS
    # ============================================================================
    print("=" * 60)
    print("PARSED ARGUMENTS:")
    print("=" * 60)
    
    # Process name
    name = args.name
    if args.uppercase:
        name = name.upper()
    
    # Display all parsed values
    print(f"Name: {name}")
    print(f"Uppercase flag: {args.uppercase}")
    print(f"Verbose mode: {args.verbose_mode}")
    print(f"Verbosity level: {args.verbose}")
    print(f"Format: {args.format}")
    print(f"Tags: {args.tags}")
    print(f"Repeat: {args.repeat}")
    print(f"Color: {args.color}")
    print(f"Numbers: {args.numbers}")
    print(f"Output: {args.output}")
    print(f"Exclude patterns: {args.exclude}")
    print("=" * 60)
    
    # Demonstrate verbosity levels
    if args.verbose >= 3:
        print("🔊 VERY VERBOSE MODE")
    elif args.verbose >= 2:
        print("🔉 VERBOSE MODE")
    elif args.verbose >= 1:
        print("🔈 DEBUG MODE")
    
    # Repeat greeting
    for i in range(args.repeat):
        greeting = f"Hello, {name}!"
        if args.color:
            greeting = f"[{args.color.upper()}] {greeting}"
        print(greeting)


if __name__ == '__main__':
    main()