import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
args = parser.parse_args()
if args.verbose:
    print("verbosity turned on")