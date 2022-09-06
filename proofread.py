# Take in a text file and output a corrected version of it

from absl import app 
from absl import flags 
from tqdm import tqdm
import difflib
import lmproof
import sys
import warnings

FLAGS = flags.FLAGS

flags.DEFINE_string("input_file", "", "Path to text file with the input content")
flags.DEFINE_bool("print_diff", False, "If true, so unified diff of changes")


# text is a list of strings and lang is a 2-character string representing
# the language of the given text: RFC 5646 
def proofread(text, lang):
    if lang != "en":
        raise RuntimeError(f"Language {lang} is not supported.")
    warnings.simplefilter("ignore")
    # Only english is supported
    proofread = lmproof.load("en")
    output_lines = []
    for line in tqdm(text):
        output_lines.append(proofread.proofread(line))
    return output_lines

# old and new are lists of strings, each string is one line of the text file
def print_diff(old, new):
    sys.stdout.writelines(difflib.unified_diff(old, new))

def main(argv):
    # We are assuming that the text files are on multiple lines.
    # We will split by line break about allow proofread to 
    # read one line at a time. This will also help with print_diff
    input_lines = []
    with open(FLAGS.input_file, 'r') as input_file:
        for line in input_file.readlines():
            input_lines.append(line)
    
    output_lines = proofread(input_lines, "en")
    input_file_split = FLAGS.input_file.split(".")
    output_file = input_file_split[0] + "_corrected." + "".join(input_file_split[1:])
    with open(output_file, 'w') as output:
        output.writelines(output_lines)
    if FLAGS.print_diff:
        print_diff(input_lines, output_lines)
    print()

if __name__ == "__main__":
    app.run(main)
