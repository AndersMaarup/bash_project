def main(): Unit \ IO =
    // Sample size, iterations
    // HUSK AT ÆNDRE I RUNTEST FØR DU KØRER!!!
    runTest(1000000,50, "Pipeline2")

def runTest(sampleSize: Int32, iterations: Int32, pipeline: String): Unit \IO =
    genClientListAndSave(sampleSize);

    println("Runtests");
    println("pipeline: ${pipeline}, sample size: ${sampleSize}");

    let resultList = List.empty();
    let range = List.range(0,iterations);

    let start_time = Time.Epoch.nanoseconds();
    // ÆNDRING HER
    let _pipeline = List.map(pipeline2, range);
    let end_time = Time.Epoch.nanoseconds();
    let total_elapsed_time = (end_time - start_time);
    let resultList1 = List.append(resultList, List#{"${pipeline}, sample size: ${sampleSize}, total time with ${iterations} iterations: ${total_elapsed_time} \n"});
    
    let writeResult = Files.writeLines("./results/testResults${pipeline}_${sampleSize}", resultList1);
    println(writeResult)

def cat(files: List[String]): (List[String], List[String]) \ IO =
    // files => Result
    let read = List.map(Files.read, files);
    // Result => String
    let pair = List.map(matchedLines, read);
    // Pair = (Line as string, err)
    // Splitting into accepted and errors
    let acceptedLines = List.map(fst, pair);
    let stdError = List.map(snd, pair);
    // Taking first, splitting into items in a list
    let stdOut = acceptedLines |> index(0) |> String.split(regex = "\n");
    // Returning (stdOut, error)
    (stdOut, stdError)

def matchedLines(r: Result[IOError, String]): (String, String) =
    match r {
        case Result.Ok(l) => (l, "")
        case Result.Err(e) => ("", "File does not exist: ${e}")
    }

def catMiddle(l: (List[String], List[String])): (List[String], List[String]) \ IO =
    let (stdIn, stdErr) = l;
    let (linesRead, newErrors) = cat(stdIn);
    let totalErrors = List.append(newErrors, stdErr);
    (linesRead, totalErrors)

def catNew(files: List[String], l: (List[String], List[String])): (List[String], List[String]) \ IO =
    let (_stdIn, stdErr) = l;
    // files => Result
    let read = List.map(Files.read, files);
    // Result => String
    let pair = List.map(matchedLines, read);
    // Pair = (Line as string, err)
    // Splitting into accepted and errors
    let acceptedLines = List.map(fst, pair);
    let newErrors = List.map(snd, pair);
    // Taking first, splitting into items in a list
    let stdOut = acceptedLines |> index(0) |> String.split(regex = "\n");
    let totalErrors = List.append(stdErr, newErrors);
    // Returning (stdOut, error)
    (stdOut, totalErrors)

// CUT
def cut(n: List[Int32], l: (List[String], List[String])): (List[String], List[String]) =
    let (stdIn, stdErr) = l;
    (stdIn |> List.map(s -> {
        let columns = String.split(regex = ",", s);
        columns |> indices(n)
    }), stdErr)

// ECHO
def echo(l: (List[String], List[String])): (List[String], List[String]) \ IO =
    let (stdIn, stdErr) = l;
    foreach (line <- stdIn)
        println(line);
    println("Standard Error: ${stdErr}");
    (stdIn, stdErr)

// FIND NAME: Find all with specific name
def findName(directory: String, name: String): (List[String], List[String]) \ IO =
    // Does directory exist?
    let x = Files.list(directory);
    let (exists, errors) = match x {
        case Result.Ok(t) => (t, List.empty())
        case Result.Err(_e) => (List.empty(), List#{"Error: Directory trying to be accessed through 'findName', '${directory}' doesn't exist"})
    };
    let filtered = List.filter(a -> String.contains(substr = name, a), exists);
    (filtered, errors)

// GREP
def grep(pattern: String, l: (List[String], List[String])): (List[String], List[String]) =
    let (stdIn, stdErr) = l;
    let res: List[String] = stdIn |> List.filter(line -> String.contains(substr = pattern, line));
    (res, stdErr)

// def grepBegin(files: List[String], pattern: String): (List[String], List[String]) =
//     let (readFiles, stdErr) = catBegin(files);
//     let (result, newError) = grep(pattern, readFiles);
//     let errors = List.append(newError, stdErr);
//     (result, errors)

// HEAD
// Returns n first elements
def head(n: Int32, l: (List[String], List[String])): (List[String], List[String]) =
    let (stdIn, stdErr) = l;
    let listLength = List.length(stdIn);
    let newList = List.slice(start = 0, end = n, stdIn);
    if (n < listLength) (newList, stdErr)
    else (newList, List.append(List#{"Notice! Head-function trying to take ${n} items, but there are only ${listLength} items in the list!"}, stdErr))

// LS
def ls(path: String): (List[String], List[String]) \ IO =
    let list = Files.list(path);
    let stdErr = List#{"Errors"};
    match list {
        case Result.Ok(l) => (l, stdErr)
        case Result.Err(_e) => (Nil, List.append(stdErr, List#{"Function 'ls' cannot find the listed item '${path}'."}))
    }

def shift(l: (List[String], List[String])): (List[String], List[String]) =
    let (stdIn, stdErr) = l;
    let listLength = List.length(stdIn);
    if (listLength <= 0) (stdIn, List.append(stdErr, List#{"Shift tried to remove an element from an empty list"}))
    else
        let newList = List.drop(1, stdIn);
        (newList, stdErr)

// SORT
def sort(l: (List[String], List[String])): (List[String], List[String]) =
    let (list, error) = l;
    let sorted = List.sort(list);
    (sorted, error)

// SORT
def sortReverse(l: (List[String], List[String])): (List[String], List[String]) =
    let (list, error) = l;
    let sorted = List.sort(list);
    let sortReversed = List.reverse(sorted);
    (sortReversed, error)

// TAIL
// Returns n last elements
def tail(n: Int32, l: (List[String], List[String])): (List[String], List[String]) =
    let (stdIn, stdErr) = l;
    let listLength = List.length(stdIn);
    let newList = List.slice(start = listLength - n, end = listLength, stdIn);
    if (n < listLength) (newList, stdErr)
    else (newList, List.append(List#{"Notice! Tail-function trying to take the last ${n} items, but there are only ${listLength} items in the list!"}, stdErr))

def tee(file_name: String, directory: String, l: (List[String], List[String])): (List[String], List[String]) \ IO =
    let (stdIn, stdErr) = l;
    let filePath = "${directory}/${file_name}";
    let overwrite = exists(filePath);
    let stdErr2: List[String] =
        match overwrite {
            case true => List.append(stdErr, List#{"Notice! Tee overwrote the already existing file '${filePath}'!"})
            case false => stdErr
        };
    let result = Files.writeLines(filePath, stdIn);
    match result {
        case Result.Ok(_b) => (stdIn, stdErr2)
        case Result.Err(_e) => (stdIn, List.append(stdErr2, List#{"Tee could not write to ${filePath}"}))
    }

def exists(filePath: String): Bool \ IO =
    let exist = Files.exists(filePath);
    match exist {
        case Result.Ok(b) => b
        case Result.Err(_e) => false
    }

// TRANS
// def trans(command: String, l: (List[String], List[String])): (List[String], List[String]) =
//     let (stdIn, stdErr) = l;
//     match command {
//         case "toLowerCase" => (transToLowerCase(stdIn), stdErr)
//         case "toUpperCase" => (transToUpperCase(stdIn), stdErr)
//         case _ => (stdIn, List.append(List#{"trans command ${command} not existing"}, stdErr))
//     }

def transDelete(_chars: String, l: (List[String], List[String])): (List[String], List[String]) =
    let (stdIn, stdErr) = l;
    (stdIn, stdErr)

def transToLowerCase(l: (List[String], List[String])): (List[String], List[String]) =
    let (stdIn, stdErr) = l;
    region rc {
        let myList = MutList.empty(rc);
        foreach(line <- stdIn)
            MutList.push!(String.toLowerCase(line), myList);
        (MutList.toList(myList), stdErr)
    }

def transToUpperCase(l: (List[String], List[String])): (List[String], List[String]) =
    let (stdIn, stdErr) = l;
    region rc {
        let myList = MutList.empty(rc);
        foreach(line <- stdIn)
            MutList.push!(String.toUpperCase(line), myList);
        (MutList.toList(myList), stdErr)
    }

// UNIQUE
def uniq(l: (List[String], List[String])): (List[String], List[String]) =
    let (stdIn, stdErr) = l;
    let unique = List.distinct(stdIn);
    (unique, stdErr)

// WC
def wc(l: (List[String], List[String])): (List[String], List[String]) =
    let (stdIn, stdErr) = l;
    // Join to one string
    let oneString = List.join("\n", stdIn);
    // Make a list of each word
    let oneList = String.words(oneString);
    // Count number by length of words
    let result = List.length(oneList);
    let resultToString = Int32.toString(result);
    let output = List#{resultToString};
    (output, stdErr)

// Helper function: Find element at given index
def index(index: Int32, l: List[String]): String =
    List.drop(index, l) |> List.head |> Option.getWithDefault("")

def indices(n: List[Int32], l: List[String]): String =
    // Gets a list of words, each representing a column
    // Extract the relevant indices via index function
    let return: List[String] =
        foreach(ind <- n)
            yield index(ind, l);
    // List[return] -> String
    String.flatten(return)

/// List of first names
def firstNameList(): List[String] = 
    List#{"John", "Jane", "Alex"
    }

// /// List of last names
def lastNameList(): List[String] = 
    List#{"Smith", "Johnson"}

// /// List of corporation names
def corporationList(): List[String] = 
    List#{"TechSolutions Inc.", "GreenEnergy Corp."
    }

def genClientListAndSave(int: Int32): Unit \IO =
    let clientList = genClientList(int);
    let filePath = "./test/clientList.txt";
    let result = Files.writeLines(filePath, clientList);
    println(result)


def genClientList(length: Int32): List[String] \IO=
    let range = List.range(0, length); 
    let clientList = List.map(genClient, range);
    clientList

def genClient(_int: Int32): String \IO =
    let firstName = randomFromList(firstNameList());
    let lastName = randomFromList(lastNameList());
    let corporation = randomFromList(corporationList());
    let phoneNumber = genPhoneNumber();
    let clientAsList = List#{firstName, lastName, corporation, phoneNumber};
    List.join(", ", clientAsList)

def genPhoneNumber(): String \IO= 
        let rand = Random.fresh() |> Random.nextInt32 |> Int32.abs; 
        Int32.modulo(rand, 100000000) |> Int32.toString

def randomFromList(l: List[String]): String \IO=
    let r = Random.fresh();
    let listLength = List.length(l);
    let intRan = Random.nextInt32(r);
    let intMod = Int32.modulo(intRan, listLength);
    let ind = index(intMod, l);
    ind



// def runAllTests(clients: Int32, iterations: Int32): Unit \IO =
//     genClientListAndSave(clients);
//     allTests(clients, iterations)

// Simple test
def pipeline1(_int: Int32): (List[String], List[String]) \IO= 
    let result = cat(List#{"./test/clientList.txt"}) |> cut(List#{1});
    result
// More commands
def pipeline2(_int: Int32): (List[String], List[String]) \IO= 
    let result = cat(List#{"./test/clientList.txt"}) |> transDelete(",") |> transToLowerCase |> tee("pipeline2.txt", "./results");
    result
// Many commands, no bottleneck
def pipeline3(_int: Int32): (List[String], List[String]) \IO= 
    let result = findName("./test", "client") |> catMiddle |> grep("John") |> cut(List#{4}) |> transToLowerCase |> transToUpperCase;
    result
// Many commands, bottleneck
def pipeline4(_int: Int32): (List[String], List[String]) \IO= 
    let result = findName("./test", "client") |> catMiddle |> grep("Zeta") |> cut(List#{4}) |> uniq |> sort |> tee("pipeline4.txt", "./results") |> wc;
    result
// Only bottlenecks
def pipeline5(_int: Int32): (List[String], List[String]) \IO= 
    let result = cat(List#{"./test/clientList.txt"}) |> sort |> sortReverse |> sort |> sortReverse;
    result



// def allTests(sampleSize: Int32, iterations: Int32): Unit \IO =
//     let resultList = List.empty();
//     let range = List.range(0,iterations);

//     let start_time1 = Time.Epoch.nanoseconds();
//     let _pipeline1 = List.map(pipeline1, range);
//     let end_time1 = Time.Epoch.nanoseconds();
//     let total_elapsed_time1 = (end_time1 - start_time1);
//     let resultList2 = List.append(resultList, List#{"Pipeline 1, sample size: ${sampleSize}, total time with ${iterations} iterations: ${total_elapsed_time1} \n"});

//     let start_time2 = Time.Epoch.nanoseconds();
//     let _pipeline2 = List.map(pipeline2, range);
//     let end_time2 = Time.Epoch.nanoseconds();
//     let total_elapsed_time2 = (end_time2 - start_time2);
//     let resultList3 = List.append(resultList2, List#{"Pipeline 2, sample size: ${sampleSize}, total time with ${iterations} iterations: ${total_elapsed_time2} \n"});
    
//     let start_time3 = Time.Epoch.nanoseconds();
//     let _pipeline3 = List.map(pipeline3, range);
//     let end_time3 = Time.Epoch.nanoseconds();
//     let total_elapsed_time3 = (end_time3 - start_time3);
//     let resultList4 = List.append(resultList3, List#{"Pipeline 3, sample size: ${sampleSize}, total time with ${iterations} iterations: ${total_elapsed_time3} \n"});
    
//     let start_time4 = Time.Epoch.nanoseconds();
//     let _pipeline4 = List.map(pipeline4, range);
//     let end_time4 = Time.Epoch.nanoseconds();
//     let total_elapsed_time4 = (end_time4 - start_time4);
//     let resultList5 = List.append(resultList4, List#{"Pipeline 4, sample size: ${sampleSize}, total time with ${iterations} iterations: ${total_elapsed_time4} \n"});

//     let start_time5 = Time.Epoch.nanoseconds();
//     let _pipeline5 = List.map(pipeline7, range);
//     let end_time5 = Time.Epoch.nanoseconds();
//     let total_elapsed_time5 = (end_time5 - start_time5);
//     let resultList6 = List.append(resultList5, List#{"Pipeline 5, sample size: ${sampleSize}, total time with ${iterations} iterations: ${total_elapsed_time5} \n"});

//     let total_time = Add.add(total_elapsed_time1, total_elapsed_time2) |> Add.add(total_elapsed_time3)|> Add.add(total_elapsed_time4)|> Add.add(total_elapsed_time5);
//     let resultList7 = List.append(resultList6, List#{"Total time: ${total_time}"});

//     let writeResult = Files.writeLines("./results/testResults${sampleSize}", resultList7);
//     println(writeResult)
