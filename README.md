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
sub-cfg-object-1 will be a int64 number you have configured in sub_cfgs.conf, little endian   
and there will be another int64 number indicate the length of cfg data following, little endian  
the last to come is cfg data, depending on the type int64, double, hex, string or other type  
for int64 it would be little endian


and for the objects which composed of other objects there won't be any data expressing it  
only those objects carrying real cfg data would exit in bin file 

