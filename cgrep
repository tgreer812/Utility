import argparse
import logging

def parse_args():
    # Define the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, help='the name of the file to search')
    parser.add_argument('search_string', type=str, help='the string to search for')
    parser.add_argument('num_lines', type=int, help='the number of lines to include before and after the matching line')
    parser.add_argument('--debug', action='store_true', help='enable debugging output')
    parser.add_argument('--logfile', type=str, help='the name of the log file to write to')
    return parser.parse_args()

def search_and_print(filename, search_string, num_lines):
    # Open the file and read its lines into a list
    with open(filename, 'r') as f:
        lines = f.readlines()

    # Search the list of lines for the search string
    line_num = 0
    for i, line in enumerate(lines):
        line_num += 1
        if search_string in line:
            # Print the matching line and the specified number of lines before and after it
            start = max(0, i - num_lines)
            end = min(len(lines), i + num_lines + 1)
            for j in range(start, end):
                logging.info(f'{line_num}: {lines[j]}')
                line_num += 1
            break

def main():
    # Parse the command line arguments
    args = parse_args()

    # Configure the logging module
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    elif args.logfile:
        logging.basicConfig(level=logging.INFO, filename=args.logfile)
    else:
        logging.basicConfig(level=logging.WARNING)

    # Call the search_and_print function with the command line arguments
    search_and_print(args.filename, args.search_string, args.num_lines)

# Call the main function
main()
