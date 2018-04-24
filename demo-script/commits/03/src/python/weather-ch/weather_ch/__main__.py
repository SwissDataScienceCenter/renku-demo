import sys
from .reader import read_data
from .preprocess import to_standardized

cmd = sys.argv[1]
if cmd == "preprocess":
    input = sys.argv[2]
    output = sys.argv[3]
    print("Preprocessing {} to {}".format(input, output))
    df = read_data(input)
    to_standardized(df, output)
