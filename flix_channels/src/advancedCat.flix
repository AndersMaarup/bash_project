// // CAT
// def catBegin(files: List[String], stdOut: Sender[String, r], errOut: Sender[String, r]): Unit \ IO + IO + r = 
//     // files=>Result
//     let read = List.map(Files.read, files);
//     // Result => String
//     let pair = List.map(matchedLines, read);
//     // Pair = (Line as string, err)
//     let accept = List.map(fst, pair);
//     let joined = List.join("\n", accept);
//     let lines = String.split(regex = "\n", joined);
//     let errors = List.map(snd, pair);
//     foreach(line <- lines)
//         Channel.send(line, stdOut);
//     Channel.send("Last Line", stdOut);
//     foreach(line <- errors)
//         Channel.send(line, errOut);
//     Channel.send("Last Line", errOut)

// // CAT
// def cat2(files: Option[List[String]], stdIn: Option[Receiver[String, r]], stdOut: Sender[String, r], errOut: Sender[String, r]): Unit \ IO + IO + r = 
//     match files {
//         case Some(file) => catBegin(file, stdOut, errOut)
//         case None => catMiddle(stdIn, stdOut, errOut)
//     }

// def catMiddle(stdIn: Option[Receiver[String, r]], stdOut: Sender[String, r], errOut: Sender[String, r]): Unit \ IO + r =    
//     match stdIn{
//         case Some(rec) => catMiddleUnpack(rec, stdOut, errOut)
//         case None => Channel.send("Error: Cat called with wrong channel!", errOut)
//     }

// def catMiddleUnpack(stdIn: Receiver[String, r], stdOut: Sender[String, r], errOut: Sender[String, r]): Unit \ IO + r = 
//     let files = collectChannel(List.empty(), stdIn);
//     // files=>Result
//     let read = List.map(Files.read, files);
//     // Result => String
//     let pair = List.map(matchedLines, read);
//     // Pair = (Line as string, err)
//     let accept = List.map(fst, pair);
//     let joined = List.join("\n", accept);
//     let lines = String.split(regex = "\n", joined);
//     let errors = List.map(snd, pair);
//     foreach(line <- lines)
//         Channel.send(line, stdOut);
//     foreach(line <- errors)
//         Channel.send(line, errOut);
//     Channel.send("Last Line", stdOut);
//     Channel.send("Last Line", errOut)