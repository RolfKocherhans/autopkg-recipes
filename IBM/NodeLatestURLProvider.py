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


__all__ = ["NodeLatestURLProvider"]


class NodeLatestURLProvider(Processor):
    description = "Returns url to the latest Tivoli Storage Manager package."
    input_variables = {
        "type": {
            "required": False,
            "description": "type of download; either 'LTS' or 'Stable', default: 'Stable'.",
        }
    }
    output_variables = {
        "url": {
            "description": "download URL.",
        }
    }
    
    __doc__ = description
    

    def main(self):
        url = subprocess.check_output(['osascript', '-e', r'''
        -- extract the name of the latest major "Tivoli Storage Manager" version e.g. v6r3,v6r4,v7r1 -> v7r1
        set ftpServer to "ftp://public.dhe.ibm.com"
        set ftpDirectory to "/storage/tivoli-storage-management/maintenance/client/"
        set shellCommand to "curl " & quoted form of (ftpServer & ftpDirectory)
        set folderNames to paragraphs of (do shell script shellCommand)
        set varMajorVersion to last word of last item of folderNames --as string
        -- add this info to the URL and go two levels deeper to extract the minor "Tivoli Storage Manager" version e.g. v713,v714,v716 - v716
        set ftpDirectory to "/storage/tivoli-storage-management/maintenance/client/" & varMajorVersion & "/Mac/"
        set shellCommand to "curl " & quoted form of (ftpServer & ftpDirectory)
        set folderNames to paragraphs of (do shell script shellCommand)
        set varMinorVersion to last word of last item of folderNames --as string
        -- add this info to the URL and go one levels deeper and extrct the file name e.g. 7.1.6.0-TIV-TSMBAC-Mac.dmg
        set ftpDirectory to "/storage/tivoli-storage-management/maintenance/client/" & varMajorVersion & "/Mac/" & varMinorVersion & "/"
        set shellCommand to "curl " & quoted form of (ftpServer & ftpDirectory)
        set folderNames to paragraphs of (do shell script shellCommand)
        -- extract line containing file name info "-rw-r--r--    1 102004493 209       156000727 Jun 17 10:41 7.1.6.0-TIV-TSMBAC-Mac.dmg"
        set AppleScript's text item delimiters to {space}
        set delimitedList to every text item of folderNames
        set fileNameWholeLine to text item 3 of delimitedList
        -- extract the file name from the line conating it e.g. 7.1.6.0-TIV-TSMBAC-Mac.dmg
        set AppleScript's text item delimiters to {space}
        set delimitedList to every text item of fileNameWholeLine
        set fileName to last text item of delimitedList
        -- create download link
        set downloadLink to ftpServer & "/storage/tivoli-storage-management/maintenance/client/" & varMajorVersion & "/Mac/" & varMinorVersion & "/" & fileName
        '''])
        url = url[:-1]
        self.env["url"] = url

if __name__ == '__main__':
    processor = NodeLatestURLProvider()
    processor.execute_shell()
