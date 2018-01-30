import argparse
from process_crypto import *

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--interval', type = int, default = 60, help = 'Number of minutes')
    parser.add_argument('--top', type=int, default=0, help='Top N number of cryptos')
    args = parser.parse_args()
    process_all_cryptos(args)

if __name__ == '__main__':
    main()

