#!/bin/bash

downloadLink=`/usr/bin/osascript << EOT
--•• # extract the name of the latest major "Tivoli Storage Manager" version e.g. v6r3,v6r4,v7r1 -> v7r1
set ftpServer to "ftp://public.dhe.ibm.com"
set ftpDirectory to "/storage/tivoli-storage-management/maintenance/client/"
set shellCommand to "curl " & quoted form of (ftpServer & ftpDirectory)
set folderNames to paragraphs of (do shell script shellCommand)
set varMajorVersion to last word of last item of folderNames --as string

--•• # add this info to the URL and go two levels deeper to extract the minor "Tivoli Storage Manager" version e.g. v713,v714,v716 - v716
set ftpDirectory to "/storage/tivoli-storage-management/maintenance/client/" & varMajorVersion & "/Mac/"
set shellCommand to "curl " & quoted form of (ftpServer & ftpDirectory)
set folderNames to paragraphs of (do shell script shellCommand)
set varMinorVersion to last word of last item of folderNames --as string

--•• # add this info to the URL and go one levels deeper and extract the file name e.g. 7.1.6.0-TIV-TSMBAC-Mac.dmg
set ftpDirectory to "/storage/tivoli-storage-management/maintenance/client/" & varMajorVersion & "/Mac/" & varMinorVersion & "/"
set shellCommand to "curl " & quoted form of (ftpServer & ftpDirectory)
set folderNames to paragraphs of (do shell script shellCommand)

--•• # extract line containing file name info "-rw-r--r--    1 102004493 209       156000727 Jun 17 10:41 7.1.6.0-TIV-TSMBAC-Mac.dmg"
set AppleScript's text item delimiters to {space}
set delimitedList to every text item of folderNames
set fileNameWholeLine to text item 3 of delimitedList

--•• # extract the file name from the line conating it e.g. 7.1.6.0-TIV-TSMBAC-Mac.dmg
set AppleScript's text item delimiters to {space}
set delimitedList to every text item of fileNameWholeLine
set fileName to last text item of delimitedList

--•• # create download link
set downloadLink to ftpServer & "/storage/tivoli-storage-management/maintenance/client/" & varMajorVersion & "/Mac/" & varMinorVersion & "/" & fileName
EOT`

# echo $downloadLink
return $downloadLink
