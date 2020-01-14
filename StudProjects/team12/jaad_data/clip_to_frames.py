from jaad_data import JAAD
import argparse
parser = argparse.ArgumentParser(description='Convert video clips to frames.')
parser.add_argument('location', metavar='loc', type=str, help='the path of the jaad folder')
args = parser.parse_args()

print(args.location.split("=")[1])
jaad_path = args.location.split("=")[1]
imdb = JAAD(data_path=jaad_path)
imdb.extract_and_save_images()
