from parser import Parser
import getopt
import sys

def print_help():
    print("usage:")
    print("python main.py --help")
    print("python main.py --cfg_file aaa --sub_cfg_file bbb")

def main():
    sub_cfg_file_var = ""
    cfg_file_var = ""
    output_file_var = ""

    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["cfg_file=", "sub_cfg_file=", "output_file=", "help"])
    except getopt.GetoptError as e:
        print("error:", e)
        sys.exit(1)

    for opt, arg in opts:
        if opt == "--cfg_file":
            cfg_file_var = arg;
        elif opt == "--sub_cfg_file":
            sub_cfg_file_var = arg
        elif opt == "--help":
            print_help()
        elif opt == "--output_file":
            output_file_var = arg

    
    parser = Parser()
    parser.init(sub_cfg_file_var)
    parser.parse(cfg_file_var, output_file_var)

if __name__ == "__main__":
    main()