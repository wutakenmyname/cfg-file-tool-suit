# cfg-file-tool-suit
1)
cfg file format:
###############begin###########################
{
// biggest cfg object
    {sub-cfg-object-1 data-type-1 data-value-1}
    {
        sub-cfg-object-2
        {
          {sub-cfg-object-3 data-type-2 data-value-2}
          {sub-cfg-object-4 data-type-3 data-value-3}
        }
    }
}
###############end#############################
sub-cfg-object-x is configuable
data-type-x is not configurable
data-value-x is obviously configurable

2) data encode
finally 
there will be a number assigned to sub-cfg-object-x, and I would say it would be a uint64
also there will be a number assigned to data-type-x, and I would say it would be a uint8
for data-value-x, it maybe a int64, double or hex, string these data sequence

for hex for string, no endian things, so they are just writed to bin file from low address to high address
for these uint64, int64 double, they maybe big endian or little endian depending on the host
to generized it, they would be converted to little endian and writed to bin file

so the layout of bin file would be
[8 byte uint8 number little endian][1 byte uint8 number][8 byte uint8 number little endian or data sequence from low address to high address]...