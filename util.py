
import argparse

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=False,
                    help="path to the input image")
    ap.add_argument("-d", "--directory", required=False,
                    help="path to the directory with input images")
    ap.add_argument("-p", "--plate_size", required=False,
                    help="plate size (mm)")
    ap.add_argument("-small", "--small_plaque", required=False,
                    help="for processing small plaques", action = "store_true")
    ap.add_argument("-debug", "--debug", required=False, action = "store_true")
    args = vars(ap.parse_args())
    if args['image'] ==  None and args['directory'] == None:
        raise Exception('Either -i or -d flags must be provided!')
        
    return args