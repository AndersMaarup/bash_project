def main(): Unit \ IO =
    // Sample size, iterations
    // HUSK AT ÆNDRE I RUNTEST FØR DU KØRER!!!
    runTest(100000,50, "Pipeline1")

def runTest(sampleSize: Int32, iterations: Int32, pipeline: String): Unit \IO =
    genClientListAndSave(sampleSize);

    println("Runtests");
    println("pipeline: ${pipeline}, sample size: ${sampleSize}");

    let resultList = List.empty();
    let range = List.range(0,iterations);

    let start_time = Time.Epoch.nanoseconds();
    // ÆNDRING HER
    let _pipeline = List.map(pipeline1, range);
    println("returned to 'runTest'!");
    let end_time = Time.Epoch.nanoseconds();
    let total_elapsed_time = (end_time - start_time);
    let resultList1 = List.append(resultList, List#{"${pipeline}, sample size: ${sampleSize}, total time with ${iterations} iterations: ${total_elapsed_time} \n"});
    
    let writeResult = Files.writeLines("./results/testResults${pipeline}_${sampleSize}", resultList1);
    println(writeResult)

def pipeline1(_int: Int32): Unit \IO =
    region rc{
        let (stdSend1, stdRec1) = Channel.buffered(rc, 100);
        let (errSend1, errRec1) = Channel.buffered(rc, 100);
        let (stdSend2, stdRec2) = Channel.buffered(rc, 100);
        let (errSend2, errRec2) = Channel.buffered(rc, 100);

        spawn cat(List#{"./test/clientList.txt"}, stdSend1, errSend1) @ rc;
        spawn cut(List#{1}, stdRec1, stdSend2, errRec1, errSend2) @ rc;

        let (_result, _error) = collectAndEnd(stdRec2, errRec2);
        println("Ran pipeline1")
        }

def pipeline2(_int: Int32): Unit \IO =
    region rc{
        let (stdSend1, stdRec1) = Channel.buffered(rc, 100);
        let (errSend1, errRec1) = Channel.buffered(rc, 100);
        let (stdSend2, stdRec2) = Channel.buffered(rc, 100);
        let (errSend2, errRec2) = Channel.buffered(rc, 100);
        let (stdSend3, stdRec3) = Channel.buffered(rc, 100);
        let (errSend3, errRec3) = Channel.buffered(rc, 100);
        let (stdSend4, stdRec4) = Channel.buffered(rc, 100);
        let (errSend4, errRec4) = Channel.buffered(rc, 100);

        spawn cat(List#{"./test/clientList.txt"}, stdSend1, errSend1) @ rc;
        spawn trans("toLowerCase", stdRec1, stdSend2, errRec1, errSend2) @ rc;
        spawn trans("toUpperCase", stdRec2, stdSend3, errRec2, errSend3) @ rc;
        spawn tee("./results/pipeline2", stdRec3, stdSend4, errRec3, errSend4) @ rc;
        
        let (_result, _error) = collectAndEnd(stdRec4, errRec4);
        println("Ran pipeline2")
        }

def pipeline3(_int: Int32): Unit \IO =
    region rc{
        println("Starting 3 again");
        let (stdSend1, stdRec1) = Channel.buffered(rc, 100);
        let (errSend1, errRec1) = Channel.buffered(rc, 100);
        let (stdSend2, stdRec2) = Channel.buffered(rc, 100);
        let (errSend2, errRec2) = Channel.buffered(rc, 100);
        let (stdSend3, stdRec3) = Channel.buffered(rc, 100);
        let (errSend3, errRec3) = Channel.buffered(rc, 100);
        let (stdSend4, stdRec4) = Channel.buffered(rc, 100);
        let (errSend4, errRec4) = Channel.buffered(rc, 100);
        let (stdSend5, stdRec5) = Channel.buffered(rc, 100);
        let (errSend5, errRec5) = Channel.buffered(rc, 100);
        let (stdSend6, stdRec6) = Channel.buffered(rc, 100);
        let (errSend6, errRec6) = Channel.buffered(rc, 100);   

        spawn findName("/test", "client", stdSend1, errSend1) @ rc;
        spawn catMiddle(stdRec1, stdSend2, errRec1, errSend2) @ rc;
        spawn grep("John", stdRec2, stdSend3, errRec2, errSend3) @ rc;
        spawn cut(List#{4}, stdRec3, stdSend4, errRec3, errSend4) @ rc;
        spawn trans("toLowerCase", stdRec4, stdSend5, errRec4, errSend5) @ rc;
        spawn trans("toUpperCase", stdRec5, stdSend6, errRec5, errSend6) @ rc;

        
        let (_result, _error) = collectAndEnd(stdRec6, errRec6);
        println("Ran pipeline3")
        }

def pipeline4(_int: Int32): Unit \IO =
    region rc{
        println("Starting 4 again");
        let (stdSend1, stdRec1) = Channel.buffered(rc, 100);
        let (errSend1, errRec1) = Channel.buffered(rc, 100);
        let (stdSend2, stdRec2) = Channel.buffered(rc, 100);
        let (errSend2, errRec2) = Channel.buffered(rc, 100);
        let (stdSend3, stdRec3) = Channel.buffered(rc, 100);
        let (errSend3, errRec3) = Channel.buffered(rc, 100);
        let (stdSend4, stdRec4) = Channel.buffered(rc, 100);
        let (errSend4, errRec4) = Channel.buffered(rc, 100);
        let (stdSend5, stdRec5) = Channel.buffered(rc, 100);
        let (errSend5, errRec5) = Channel.buffered(rc, 100);
        let (stdSend6, stdRec6) = Channel.buffered(rc, 100);
        let (errSend6, errRec6) = Channel.buffered(rc, 100);      

        spawn findName("/test", "client", stdSend1, errSend1) @ rc;
        spawn catMiddle(stdRec1, stdSend2, errRec1, errSend2) @ rc;
        spawn grep("John", stdRec2, stdSend3, errRec2, errSend3) @ rc;
        spawn cut(List#{4}, stdRec3, stdSend4, errRec3, errSend4) @ rc;
        spawn uniq(stdRec4, stdSend5, errRec4, errSend5) @ rc;
        spawn sort(stdRec5, stdSend6, errRec5, errSend6) @ rc;

        
        let (_result, _error) = collectAndEnd(stdRec6, errRec6);
        println("Ran pipeline4")
        }

def pipeline5(_int: Int32): Unit \IO =
    region rc{
        let (stdSend1, stdRec1) = Channel.buffered(rc, 100);
        let (errSend1, errRec1) = Channel.buffered(rc, 100);
        let (stdSend2, stdRec2) = Channel.buffered(rc, 100);
        let (errSend2, errRec2) = Channel.buffered(rc, 100);
        let (stdSend3, stdRec3) = Channel.buffered(rc, 100);
        let (errSend3, errRec3) = Channel.buffered(rc, 100);
        let (stdSend4, stdRec4) = Channel.buffered(rc, 100);
        let (errSend4, errRec4) = Channel.buffered(rc, 100);
        let (stdSend5, stdRec5) = Channel.buffered(rc, 100);
        let (errSend5, errRec5) = Channel.buffered(rc, 100);        

        spawn cat(List#{"./test/clientList.txt"}, stdSend1, errSend1) @ rc;
        spawn sort(stdRec1, stdSend2, errRec1, errSend2) @ rc;
        spawn sortReverse(stdRec2, stdSend3, errRec2, errSend3) @ rc;
        spawn sort(stdRec3, stdSend4, errRec3, errSend4) @ rc;
        spawn sortReverse(stdRec4, stdSend5, errRec4, errSend5) @ rc;

        let (_result, _error) = collectAndEnd(stdRec5, errRec5);
        println("Ran pipeline5")
        }

// Parameter standard: 
// (stdIn: Receiver[String, r], stdOut: Sender[String, r], _errIn: Receiver[String, r], errOut: Sender[String, r]): Unit \ IO + r =

// CAT
def cat(files: List[String], stdOut: Sender[String, r], errOut: Sender[String, r]): Unit \ IO + IO + r = 
    // files=>Result
    let read = List.map(Files.read, files);
    // Result => String
    let pair = List.map(matchedLines, read);
    // Pair = (Line as string, err)
    let accept = List.map(fst, pair);
    let joined = List.join("\n", accept);
    let lines = String.split(regex = "\n", joined);
    let errors = List.map(snd, pair);
    foreach(line <- lines)
        Channel.send(line, stdOut);
    foreach(line <- errors)
        Channel.send(line, errOut);
    Channel.send("Last Line", stdOut);
    Channel.send("Last Line", errOut)


def catMiddle(stdIn: Receiver[String, r], stdOut: Sender[String, r], _errIn: Receiver[String, r], errOut: Sender[String, r]): Unit \ IO + r =
    let filePath = Channel.recv(stdIn);
    cat(List#{filePath}, stdOut, errOut)

def matchedLines(r: Result[IOError, String]): (String, String) =
    match r {
        case Result.Ok(l) => (l, "")
        case Result.Err(e) => ("", "File does not exist: ${e}")
    }        

// WC
def wc(stdIn: Receiver[String, r], stdOut: Sender[String, r], errIn: Receiver[String, r], errOut: Sender[String, r]): Unit \ IO + r =
    let list = collectChannel(List.empty(), stdIn);
    // Number of lines
    let lineCount = List.length(list);
    // Number of words
    let oneString = List.join("", list);
    let words = String.words(oneString);
    let wordCount = List.length(words);
    Channel.send("Linecount: ${lineCount}. Wordcount: ${wordCount}", stdOut);
    Channel.send("Last Line", stdOut);
    Channel.send("Last Line", errOut);
    wc(stdIn, stdOut, errIn, errOut)


// CUT
def cut(n: List[Int32], stdIn: Receiver[String, r], stdOut: Sender[String, r], errIn: Receiver[String, r], errOut: Sender[String, r]): Unit \ r =
    let input = Channel.recv(stdIn);
    if(input == "Last Line"){
        Channel.send(input, stdOut);
        Channel.send("Last Line", errOut)
    }
    else {
        let columns = String.split(regex = ",", input);
        let extraction: String = 
            columns |> indices(n);
        Channel.send(extraction, stdOut);
        cut(n, stdIn, stdOut, errIn, errOut)
    }

// Helper-function: Find element at given index
def index(index: Int32, l: List[String]): String =
    List.drop(index, l) |> List.head |> Option.getWithDefault("")

def indices(n: List[Int32], l: List[String]): String =
    // Gets a list of words, each representing a column
    // Extract the relevant indices via index-function
    let columns: List[String] =
        foreach(ind <- n)
            yield index(ind, l);
    // List[return]->String
    let result = List.join(",", columns);
    result

// ECHO
def echo(stdIn: Receiver[String, r], stdOut: Sender[String, r], errIn: Receiver[String, r], errOut: Sender[String, r]): Unit \ IO + IO + r =
    // println("Started echo");
    let input = Channel.recv(stdIn);
    println("stdIn at echo:  ${input}");
    if(input == "Last Line") {
        Channel.send(input, stdOut);
        Channel.send("Last Line", errOut)
    }
    else {
        Channel.send(input, stdOut);
        echo(stdIn, stdOut, errIn, errOut)}

// FIND NAME: Find all with specific name
def findName(directory: String, name: String, stdOut: Sender[String, r], errOut: Sender[String, r]): Unit \  IO + r =
    // Does directory exist?
    let x = Files.list(directory);
    match x {
        case Result.Ok(t) => let result = List.filter(a -> String.contains(substr = name, a), t);
                            foreach(line <- result)
                                Channel.send(line, stdOut)
        case Result.Err(_e) => Channel.send("findName couldn't find directory ${directory}", errOut)
    };
    Channel.send("Last Line", stdOut);
    Channel.send("Last Line", errOut)


def ls(path: String, stdOut: Sender[String, r], errOut: Sender[String, r]): Unit \ IO + IO + r =
    let list = Files.list(path);
    match list {
            case Result.Ok(lines) => {
                foreach(line <- lines)
                    Channel.send(line, stdOut)
            }
            case Result.Err(_e) => Channel.send("ls could not find results for ${path}", errOut)
        };
    Channel.send("Last Line", stdOut);
    Channel.send("Last Line", errOut)

// TRANS
def trans(command: String, stdIn: Receiver[String, r], stdOut: Sender[String, r], errIn: Receiver[String, r], errOut: Sender[String, r]): Unit \  r =
    let input = Channel.recv(stdIn);
    if(input == "Last Line"){
        Channel.send(input, stdOut);
        Channel.send("Last Line", errOut)
    }
    else {
        match command{
                case "toLowerCase" => Channel.send(String.toLowerCase(input), stdOut)
                case "toUpperCase" => Channel.send(String.toUpperCase(input), stdOut)   
                case _ => Channel.send("Error! Trans-function called with function ${command}, which is not a known command", errOut)                            
        };
        trans(command, stdIn, stdOut, errIn, errOut)
    }

// Tail
def tail(n: Int32,  stdIn: Receiver[String, r], stdOut: Sender[String, r], _errIn: Receiver[String, r], errOut: Sender[String, r]): Unit \ IO + r =
    // Wait and collect all items in list
    let list = collectChannel(List.empty(), stdIn);
    let listLength = List.length(list);
    if(1 >= n){
        endWithError("Error! Tail was called with argument *${n}*, but needs at least 1", stdOut, errOut)
    }
    else {
        // Cut out all items, except n last items
        let newList = List.slice(start = listLength - (n), end = listLength, list);
        // Send them individualy
        foreach(line <- newList)
            Channel.send(line, stdOut);
        Channel.send("Last Line", stdOut);
        Channel.send("Last Line", errOut)
        // if (n > listLength)
        //     Channel.send("OBS! Tail was called with argument ${n}, but there was only ${listLength} items in the list", errOut)
    }

// TEE
def tee(path: String, stdIn: Receiver[String, r], stdOut: Sender[String, r], errIn: Receiver[String, r], errOut: Sender[String, r]): Unit \ IO + r =
    let line = Channel.recv(stdIn);
    let _result = Files.append(path, line);
    if(line == "Last Line")
        {
        let err = Channel.recv(errIn);
        Channel.send(line, stdOut);
        Channel.send(err, errOut)
        }
    else {
        Channel.send(line, stdOut);
        tee(path, stdIn, stdOut, errIn, errOut)
    }

// Helper-function for "Tee"
def exists(s: String): Bool \ IO=
    let exist = Files.exists(s);
    match exist {
        case Result.Ok(b) => b 
        case Result.Err(_e) => false
    }

// UNIQ
def uniq(stdIn: Receiver[String, r], stdOut: Sender[String, r], _errIn: Receiver[String, r], errOut: Sender[String, r]): Unit \ IO + r =
    let list = collectChannel(List.empty(), stdIn);
    let unique = List.distinct(list);
    foreach(line <- unique) 
        Channel.send(line, stdOut);
    Channel.send("Last Line", stdOut);
    Channel.send("Last Line", errOut)

// SORT
def sort(stdIn: Receiver[String, r], stdOut: Sender[String, r], _errIn: Receiver[String, r], errOut: Sender[String, r]): Unit \ IO + r =
    let list = collectChannel(List.empty(), stdIn);
    let sortedList = List.sort(list);
    foreach(line <- sortedList; if Eq.neq(line, "Last Line"))
        {
        Channel.send(line, stdOut)
        };
    Channel.send("Last Line", stdOut);
    Channel.send("Last Line", errOut)

// SORTREVERSE
def sortReverse(stdIn: Receiver[String, r], stdOut: Sender[String, r], _errIn: Receiver[String, r], errOut: Sender[String, r]): Unit \ IO + r =
    let list = collectChannel(List.empty(), stdIn);
    let sortedList = List.sort(list);
    let sortReversed = List.reverse(sortedList);
    foreach(line <- sortReversed; if Eq.neq(line, "Last Line"))
        {
        Channel.send(line, stdOut)
        };
    Channel.send("Last Line", stdOut);
    Channel.send("Last Line", errOut)

// GREP
def grep(pattern: String, stdIn: Receiver[String, r], stdOut: Sender[String, r], errIn: Receiver[String, r], errOut: Sender[String, r]): Unit \ IO + r =
    let line = Channel.recv(stdIn);
    if (line == "Last Line"){
        Channel.send(line, stdOut);
        Channel.send(line, errOut)}
    else if (line == pattern) {
        Channel.send(line, stdOut);
        grep(pattern, stdIn, stdOut, errIn, errOut)
        }
    else {
        grep(pattern, stdIn, stdOut, errIn, errOut)
        }

// HEAD
def head(n: Int32, rx: Receiver[String, r], tx: Sender[String, r]): Unit \ IO + r =
    let stdin = Channel.recv(rx); 
    // TODO: Should "5 first" just be first three, if only three exist?
    if (stdin == "Last Line")
        Channel.send(stdin, tx)
    else if (n == 1){
        Channel.send(stdin, tx);
        Channel.send("Last Line", tx)}
    // If not enough input, call again
    else {
        Channel.send(stdin, tx);
        head(n-1, rx, tx)}
        // (newList, List.append(List#{"Notice! Head-function trying to take ${n} items, but their are only ${listLength} items in the list!"}, stdErr))

// Helper functions
// Last action in pipeline
def collectAndEnd(stdIn: Receiver[String, r], errIn: Receiver[String, r]): (String, List[String]) \ IO + r =
    let output = collectChannel(List.empty(), stdIn);
    let outputJoined = List.join("\n", output);
    let errors = collectChannel(List.empty(), errIn);
    let uniqueErrors = List.distinct(errors);
    (outputJoined, uniqueErrors)

// OBS!!! REMOVES "LAST LINE"!!!
// Functions using this will need to append it again!
def collectChannel(acc: List[String], rx: Receiver[String, r]): List[String] \ IO + r =
    let newString = Channel.recv(rx);
    // Stop when "Last Line" received 
    if (newString == "Last Line")
        acc
    else {
        // Make new string as list and append to accumulator
        let newStringAsList = List#{newString};
        let newList = List.append(acc, newStringAsList);
        // Call recursively with new list
        collectChannel(newList, rx)
    }

    // End with error
def endWithError(errMessage: String, stdOut: Sender[String, r], errOut: Sender[String, r]): Unit \ r =
    Channel.send(errMessage, errOut);
    Channel.send("Last Line", errOut);
    Channel.send("Last Line", stdOut)


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