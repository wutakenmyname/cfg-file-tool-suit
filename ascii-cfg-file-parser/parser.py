import sub_cfgs
import sub_cfgs_parser






def main():
   sub_cfgs_parser.Sub_cfgs_parser.parse_file("sub_cfgs.conf")
   sub_cfgs.Sub_cfgs().dump()

if __name__ == "__main__":
    main()