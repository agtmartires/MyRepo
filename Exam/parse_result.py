import sys

def parse_result():
    resultFile = sys.argv[1] 

    for line in open(resultFile, 'r'):
       if ("route_table_id" in line):
            lineSplit = line.split("\"route_table_id\": \"")
            rtid = lineSplit[1][0:lineSplit[1].find("\"")]
            # print(rtid)
            lineSplit = line.split("\"vpc_id\": \"")
            vpcid = lineSplit[1][0:lineSplit[1].find("\"")]
            # print(vpcid)
       elif ("instance_ids" in line):
            lineSplit = line.split("\"instance_ids\": [\"")
            ec2id = lineSplit[1][0:lineSplit[1].find("\"")]
            # print(ec2id)
            lineSplit = line.split("\"public_ip\": \"")
            ip = lineSplit[1][0:lineSplit[1].find("\"")]
            # print(ip)

    f = open(".resources", "a")
    f.write(vpcid + " " + ec2id + " " + rtid + " " + ip + "\n")
    f.close()


if __name__ == '__main__':
    parse_result()
