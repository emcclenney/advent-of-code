import argparse
import traceback

def init_arg_parser():
    '''
    Initialize the argument parser for this script
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str,
                        help="An input text file containing a series of spinlock combination entries.")
    parser.add_argument('-v', "--verbose", action="store_true",
                        help="Include verbose output")
    
    return parser


def parse_combo_turn(combo_entry):
    '''
    Process a combo entry string into a formatted tuple

    :param combo_entry: The combo entry string to be processed

    :return: A formatted tuple in the format (direction, turn_len)
    '''
    return (combo_entry[0], int(combo_entry[1:]) % 100)


def get_spinlock_password(input_file, verbose=False):
    '''
    Parse the provided spinlock combination input file and calculate the door password

    :param input_file: Path to an input data file containing spinlock combo values

    :param verbose: Flag used to include verbose output
    '''

    # Read the combination data from the given input file, if found
    try:
        with open(input_file) as f:
            combo = f.read()
    except FileNotFoundError:
        print(f"Error: Unable to open combo file '{input_file}' - file not found.")
        return

    # Iterate through the combination entries and track the current position
    turns = combo.split('\n')
    if (not len(turns)):
        print(f"Error: No combo data found in the given file. Please input a valid combo file.")
        return

    curr_pos = 50 # Dial starts at position 50
    passwd = 0

    for turn in turns:
        if not turn:
            continue

        turn_info = parse_combo_turn(turn)

        # Determine if this value should be added or subtracked from the current
        # position, then update the current lock position
        match turn_info[0]:
            case 'R':
                new_pos = curr_pos + turn_info[1]
                curr_pos = new_pos if new_pos < 100 else new_pos - 100
            case 'L':
                new_pos = curr_pos - turn_info[1]
                curr_pos = new_pos if new_pos >= 0 else 100 + new_pos
            case _:
                print(f"Error: Unknown turn type '{turn_info[0]}'.")
                return
        
        # Increment the password each time 0 is reached
        if curr_pos == 0:
            passwd += 1

        if verbose:
            print(f"Turn: {turn_info}  New pos: {curr_pos}  Passwd: {passwd}")
    
    return passwd


if __name__ == "__main__":
    args = init_arg_parser().parse_args()

    passwd = get_spinlock_password(args.filename, verbose=args.verbose)
    print(f"Final password: {passwd}")

    
