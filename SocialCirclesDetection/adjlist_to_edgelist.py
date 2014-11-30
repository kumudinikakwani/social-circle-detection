import sys

def convert(file_name):
    with open(file_name + ".edgelist", "w") as outputfile, open(file_name, "r") as inputfile:
        for line in inputfile:
            source = line.split(":")[0]
            dests = line.split(":")[1].split(" ")
	    for dest in dests:
                if(dest.strip() != "" and source.strip() != ""):
            	    outputfile.write(source + " " + dest.strip() + "\n")
	   

if __name__ == "__main__":
	convert(sys.argv[1]) 
