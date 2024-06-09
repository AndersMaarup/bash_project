def main(): Unit \ IO = 
    region rc {
        let (outerTx, outerRx) = Channel.buffered(rc, 100);
        let pipeline = cat |||> cat;
        pipeline((rc, outerRx, outerTx));
        Channel.send("hello", outerTx);
        Channel.recv(outerRx) |> println
    }

// def cat(arg: (Region[r], Receiver[String, r],Sender[String, r])): Unit \ r = checked_ecast(???)

def |||>(f: ((Region[r], Receiver[String, r], Sender[String, r])) -> Unit \ r, 
            g: ((Region[r], Receiver[String, r], Sender[String, r])) -> Unit \ r): 
             ((Region[r], Receiver[String, r], Sender[String, r])) -> Unit \ r = {
                match (rc, stdIn, stdOut) -> 
                    let (tx, rx) = Channel.buffered(rc, 100);
                    unchecked_cast(spawn f((rc, stdIn, tx)) @ rc as _ \ {r});
                    g((rc, rx, stdOut))
             }
// Parameter standard: 
// (stdIn: Receiver[String, r], stdOut: Sender[String, r], _errIn: Receiver[String, r], errOut: Sender[String, r]): Unit \ IO + r =

// CAT
def cat(arg: (Region[r], Receiver[String, r], Sender[String, r])): Unit \ IO + IO + r = 
    let files = collectChannel(List.empty(), stdIn);
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

def matchedLines(r: Result[IOError, String]): (String, String) =
    match r {
        case Result.Ok(l) => (l, "")
        case Result.Err(e) => ("", "File does not exist: ${e}")
    }        

// WC
def wc(stdIn: Receiver[String, r], stdOut: Sender[String, r], _errIn: Receiver[String, r], errOut: Sender[String, r]): Unit \ IO + r =
    let list = collectChannel(List.empty(), stdIn);
    // Number of lines
    let lineCount = List.length(list);
    // Number of words
    let oneString = List.join("", list);
    let words = String.words(oneString);
    let wordCount = List.length(words);
    Channel.send("Linecount: ${lineCount}. Wordcount: ${wordCount}", stdOut);
    Channel.send("Last Line", stdOut);
    Channel.send("Last Line", errOut)


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
    // TODO: Error if overwrite
    // TODO: Error if not writing
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
def uniq(rx: Receiver[String, r], tx: Sender[String, r]): Unit \ IO + r =
    let list = collectChannel(List.empty(), rx);
    let unique = List.distinct(list);
    foreach(line <- unique) 
        Channel.send(line, tx);
    Channel.send("Last Line", tx)

// SORT
def sort(rx: Receiver[String, r], tx: Sender[String, r]): Unit \ IO + r =
    let list = collectChannel(List.empty(), rx);
    let sortedList = List.sort(list);
    foreach(line <- sortedList)
        {
        Channel.send(line, tx)
        };
    Channel.send("Last Line", tx)





// GREP
def grep(pattern: String, rx: Receiver[String, r], tx: Sender[String, r]): Unit \ IO + r = 
    let stdin = Channel.recv(rx);
    if (stdin == "Last Line")
        Channel.send(stdin, tx)
    else if (stdin == pattern) {
        Channel.send(stdin, tx);
        grep(pattern, rx, tx)
        }
    else {
        grep(pattern, rx, tx)
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