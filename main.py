import requests
import platform
import hashlib
import zipfile
import json
import sys
import os

if not sys.maxsize > pow(2, 32): 
    print("jvmd-v2 has dropped support for 32-bit systems.")
    print("please download jvmd-v1 from https://github.com/zenpaiang/jvmd.")
    sys.exit()
    
def menu(options: list[str]) -> int:
    print("\n".join([f"{index + 1}. {option}" for index, option in enumerate(options)]))
    validInputs = [str(i + 1) for i in range(len(options))]
    validInput = False
    
    while not validInput:
        userInput = input(f"select a version ({validInputs[0]}-{validInputs[-1]}): ")
        
        if userInput in validInputs:
            validInput = True
        else:
            print("please enter a valid input.")
            
    return int(userInput) - 1

def download(url: str) -> tuple[bytes, bool]:
    try:
        return requests.get(url).text, True
    except:
        return b"", False

def downloadVerify(url: str, sha1: str) -> tuple[bytes, bool, bool]:
    try:
        data = requests.get(url)
        
        return data.content, hashlib.sha1(data.content).hexdigest() == sha1, True
    except:
        return b"", hashlib.sha1(data.content).hexdigest() == sha1, False

# Download runtimes index

runtimesIndexResp = download("https://raw.githubusercontent.com/zenpaiang/jvmd-v2/main/runtimes.json")

if runtimesIndexResp[1]:
    runtimesIndex = json.loads(runtimesIndexResp[0])
else:
    print("error downloading runtimes index")
    sys.exit()
    
if platform.system() == "Windows":
    runtimeIndexType = "win-x64"
elif platform.system() == "Linux" and platform.machine() in ["aarch64_be", "aarch64", "armv8b", "armv8l"]:
    runtimeIndexType = "linux-arm64"
elif platform.system() == "Linux" and platform.machine() == "x86_64":
    runtimeIndexType = "linux-x64"
else:
    print("jvmd: unsupported operating system")
    sys.exit()
    
version = menu([runtime["friendlyName"] for runtime in runtimesIndex[runtimeIndexType]])

print()

url = runtimesIndex[runtimeIndexType][version]["path"]
sha1 = runtimesIndex[runtimeIndexType][version]["sha1"]

print("downloading java runtime...")

downloadResp = downloadVerify(url, sha1)

print("java runtime downloaded.")

if downloadResp[2]:
    if downloadResp[1]:
        f = open("java.zip", "wb")
        f.write(downloadResp[0])
        f.close()
        
        print("extracting runtime...")
        
        zipf = zipfile.ZipFile("java.zip", "r")
        zipf.extractall("java")
        zipf.close()
        
        print("runtime extracted.")
            
        os.remove("java.zip")
    else:
        print("error verifying download")
else:
    print("error downloading runtime")