# cfg-file-tool-suit 
```
1)  
cfg file format:

###############begin(ignore this line)###########################
{  
// biggest cfg object  
    {sub-cfg-object-1 data-value-1}  
    {  
        sub-cfg-object-2  
        {  
            {sub-cfg-object-3 data-value-2}  
            {sub-cfg-object-4 data-value-3}
        }  
    }  
}
###############end(ignore this line)#############################   
sub-cfg-object-x is configuable    
data-value-x is  configurable
commnent line start with "//"

2) data encode    
a. sub-cfg-object-1 will be a int64 number you have configured in sub_cfgs.conf, little endian

b. there will be another int64 number indicate the length of cfg data following, little endian

c. the last to come is cfg data, depending on the type int64, double, hex, string or other type like snmpmib
and for the objects which composed of other objects there won't be any data expressing it  
only those objects carrying real cfg data would exit in bin file

d. only support non-nested tlv, embeded tlv need a special parser for embedded tlv content in value part.  


3) command  for trans your ascii format cfg file into a bin format file
python ./ascii-cfg-file-parser/main.py --cfg_file your_cfg_file --sub_cfg_file your_subcfg_file --output_file your_bin_file

example:  
    python ./ascii-cfg-file-parser/main.py --cfg_file ./ascii-cfg-file-parser/cfg_example1.sscfg --sub_cfg_file ./ascii-cfg-file-parser/sub_cfgs.conf --output_file cfg_example1.bin


4) command for parse your bin format file
a. first, compile c project.
    cd bin-cfg-file-parser
    cmake .
    make

and then you get bin_parser exec file, use it to parse a bin format file with this command
    ./bin_parser -f your_bin_file
example
    ./bin_parser -f ../cfg_example1.bin
```
