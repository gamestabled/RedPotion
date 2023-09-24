
def convert_functions():
    with open("converted_Unnamed.sym", 'w') as converted:
        with open("../../oot3d_cmake/function_addresses.txt", 'r') as function_address:
            lines = function_address.readlines()
            for line in lines:
                name = line.split(",")[0].strip()
                startAddressStr = line.split(",")[1].strip()
                startAddress = int(line.split(",")[1].strip(), 16)
                endAddress = int(line.split(",")[2].strip(), 16)
                size = endAddress - startAddress
                converted.write(name + ',' + startAddressStr + ',' + str(size) + ",U\n")


def convert_data_chunks():
    with open("converted_Data.sym", 'w') as converted:
        with open("../../oot3d_cmake/data_chunks.txt", 'r') as data_chunks:
            lines = data_chunks.readlines()
            for line in lines:
                name = line.split(",")[0].strip()
                startAddressStr = line.split(",")[1].strip()
                startAddress = int(line.split(",")[1].strip(), 16)
                endAddress = int(line.split(",")[2].strip(), 16)
                size = endAddress - startAddress
                converted.write(name + ',' + startAddressStr + ',' + str(size) + ",U\n")

def convert_rodata_chunks():
    with open("converted_Rodata.sym", 'w') as converted:
        with open("../../oot3d_cmake/rodata_chunks.txt", 'r') as rodata_chunks:
            lines = rodata_chunks.readlines()
            for line in lines:
                name = line.split(",")[0].strip()
                startAddressStr = line.split(",")[1].strip()
                startAddress = int(line.split(",")[1].strip(), 16)
                endAddress = int(line.split(",")[2].strip(), 16)
                size = endAddress - startAddress
                converted.write(name + ',' + startAddressStr + ',' + str(size) + ",U\n")

convert_data_chunks()
convert_rodata_chunks()

