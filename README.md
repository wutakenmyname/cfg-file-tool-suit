# cfg-file-tool-suit  
1)  
cfg file format:  
###############begin###########################  
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
###############end#############################  
sub-cfg-object-x is configuable    
data-value-x is obviously configurable
  
2) data encode  
finally   
there will be a number assigned to sub-cfg-object-x, and I would say it would be a uint32 but for expandability it seems it won't be a fixed uint32 but a unfixed thing we cann't get around a length of this type to indicate the length for [type]
so for sub-cfg-object-x there will be a structure [type][length][value]  
also there will be a number assigned to data-type-x, and I would say it would be a uint8  
for data-value-x, it maybe a int64, double or hex, string these data sequence  
  
for hex for string, no endian things, so they are just writed to bin file from low address to high address  
for these uint64, int64 double, they maybe big endian or little endian depending on the host  
to generized it, they would be converted to little endian and writed to bin file  

and also obviously, length for data-value-x is unavoidable  
  
so the layout of bin file would be  
[1 byte uint8 type A][1 byte uint8 type-length B][ n byte type-value C ][1 byte uint8 data-type D ][8 byte uint64 or double number little endian or data sequence from low address to high address E]...  

