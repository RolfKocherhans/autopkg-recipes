#!/usr/bin/python
# 
# Copyright 2016 Rolf Kocherhans
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from autopkglib import Processor, ProcessorError
import subprocess
import os


__all__ = ["TivoliStorageManagerURLProvider"]


class TivoliStorageManagerURLProvider(Processor):
    description = "Returns url to the latest Tivoli Storage Manager package."
    input_variables = {
    }
    output_variables = {
        "version": {
            "description": "Version of the product.",
        },
        "url": {
            "description": "Download URL.",
        }
    }
    
    __doc__ = description


    def main(self):
        url = subprocess.check_output(['osascript', '-e', r'''
        -- ######### Start of the AppleScript part #########
        -- # extract the name of the latest major "Tivoli Storage Manager" version e.g. v6r3,v6r4,v7r1 -> v7r1
        set tHTTPServer to "https://public.dhe.ibm.com"
        set tFTPServer to "ftp://public.dhe.ibm.com"
        set tFTPDirectory to "/storage/tivoli-storage-management/maintenance/client/"
        set tShellCommand to "curl " & quoted form of (tFTPServer & tFTPDirectory)
        set tFoundFolderNames to paragraphs of (do shell script tShellCommand)
        set tMajorVersion to last word of last item of tFoundFolderNames

        -- # add above info to the FTP-URL and go two levels deeper to extract the minor "Tivoli Storage Manager" version e.g. v713,v714,v716 - v716
        set tFTPDirectory to "/storage/tivoli-storage-management/maintenance/client/" & tMajorVersion & "/Mac/"
        set tShellCommand to "curl " & quoted form of (tFTPServer & tFTPDirectory)
        set tFoundFolderNames to paragraphs of (do shell script tShellCommand)
        set tMinorVersion to last word of last item of tFoundFolderNames

        -- # add above info to the FTP-URL and go one level deeper and extract the file name e.g. 7.1.6.0-TIV-TSMBAC-Mac.dmg
        set tFTPDirectory to "/storage/tivoli-storage-management/maintenance/client/" & tMajorVersion & "/Mac/" & tMinorVersion & "/"
        set tShellCommand to "curl " & quoted form of (tFTPServer & tFTPDirectory)
        set tFoundFolderNames to paragraphs of (do shell script tShellCommand)

        -- # extract line containing the download file name -> "-rw-r--r--   1 102004493 209           124 Dec  9 18:41 8.1.0.0-TIV-TSMBAC-Mac.dmg.checksum.txt"
        set AppleScript's text item delimiters to {space}
        set tDelimitedList to every text item of tFoundFolderNames
        set tFileNameOnWholeLineLong to text item 3 of tDelimitedList

        -- remove the last two extensions -> "-rw-r--r--   1 102004493 209           124 Dec  9 18:41 8.1.0.0-TIV-TSMBAC-Mac.dmg"
        set AppleScript's text item delimiters to {"."}
        set tDelimitedList to every text item of tFileNameOnWholeLineLong
        set tFileNameOnWholeLine to items 1 thru -3 of tDelimitedList as string


        -- # extract the file name from the above line -> 8.1.0.0-TIV-TSMBAC-Mac.dmg
        set AppleScript's text item delimiters to {space}
        set tDelimitedList to every text item of tFileNameOnWholeLine
        set tFileName to last text item of tDelimitedList

        -- # create download link
        set tURL to tHTTPServer & "/storage/tivoli-storage-management/maintenance/client/" & tMajorVersion & "/Mac/" & tMinorVersion & "/" & tFileName
        -- #########  End of the AppleScript part #########
        '''])
        url = url[:-1]
        self.env["url"] = url
        
        version=url.rsplit("/")[-1].rsplit("-")[0]
        self.env["version"] = version

if __name__ == '__main__':
    processor = TivoliStorageManagerURLProvider()
    processor.execute_shell()
