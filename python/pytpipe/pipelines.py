# Test functions
def pipeline1(output=False):
    # Define pipeline
    pipeline = Pipeline()
    # Define steps
    steps = [
        cat("./test/clientList.txt"),
        cut(1)
    ]
    # Run pipeline
    result = pipeline.run(*steps)
    if output:
        print(result)

def pipeline2(output=False):
    # Define pipeline
    pipeline = Pipeline()
    # Define steps
    steps = [
        cat("./test/clientList.txt"),
        tr("delete", ","),
        tr("A-Z", "a-z"),
        tee("pipeline2.txt", "./resultater")
    ]
    # Run pipeline
    result = pipeline.run(*steps)
    if output:
        print(result)

def pipeline3(output=False):
    # Define pipeline
    pipeline = Pipeline()
    # Define steps
    steps = [
        ls("./test/lsTest1"),
        sort(),
        uniq(),
        tee("pipeline3.txt", "./resultater"),
        grep("client"),
        wc()
    ]
    # Run pipeline
    result = pipeline.run(*steps)
    if output:
        print(result)

def pipeline4(output=False):
    # Define pipeline
    pipeline = Pipeline()
    # Define steps
    steps = [
        find("./test", "-name", "client"),
        catMiddle(),
        grep("Zeta"),
        cut(4),
        uniq(),
        sort(),
        tee("pipeline4.txt", "./resultater"),
        wc()
    ]
    # Run pipeline
    result = pipeline.run(*steps)
    if output:
        print(result)

def pipeline5(output=False):
    # Define pipeline
    pipeline = Pipeline()
    # Define steps
    steps = [
        mkdir("temp"),
        ls("./test/lsTest1", directory=True),
        grep("client"),
        catMiddle(),
        grep("Gamma"),
        uniq(),
        sort(),
        tee("pipeline5_output1.txt", "temp"),
        ls("./test/lsTest2", directory=True),
        grep("client"),
        catMiddle(),
        grep("Gamma"),
        uniq(),
        sort(),
        tee("pipeline5_output2.txt", "temp"),
        cat("./temp/pipeline5_output1.txt", "./temp/pipeline5_output2.txt"),
        uniq(),
        tee("finalOutput.txt", "temp"),
        mv("temp/finalOutput.txt", "./resultater/finalOutput.txt"),
        rm("temp", recursive=True)
    ]
    # Run pipeline
    result = pipeline.run(*steps)
    if output:
        print(result)

def pipeline6(output=False):
       # Define pipeline
    pipeline = Pipeline()
    # Define steps
    steps = [
        cat("./test/clientList.txt", "./test/clientList.txt", "./test/clientList.txt", "./test/clientList.txt", "./test/clientList.txt", "./test/clientList.txt", "./test/clientList.txt", "./test/clientList.txt"),
        uniq(),
        sort()
    ]
    # Run pipeline
    result = pipeline.run(*steps)
    if output:
        print(result) 

def pipeline7(output=False):
       # Define pipeline
    pipeline = Pipeline()
    # Define steps
    steps = [
        cat("./test/clientList.txt", "./test/clientList.txt", "./test/clientList.txt", "./test/clientList.txt", "./test/clientList.txt"),
        grep("Zeta"),
        uniq(),
        sort()
    ]
    # Run pipeline
    result = pipeline.run(*steps)
    if output:
        print(result)   

def pipeline8(output=False):
       # Define pipeline
    pipeline = Pipeline()
    # Define steps
    steps = [
        cat("./test/clientList.txt"),
        sort(),
        sort(reverse=True),
        sort(),
        sort(reverse=True)
    ]
    # Run pipeline
    result = pipeline.run(*steps)
    if output:
        print(result) 