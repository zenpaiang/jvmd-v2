import colorama
import platform
import sys

colorama.init()

if not sys.maxsize > pow(2, 32):
    print("jvmd-v2 has dropped support for 32-bit systems.")
    print("please download jvmd-v1 from https://github.com/ZenpaiAng/jvmd.")
    sys.exit()
    
def menu(options: list[str]) -> str:
    print("\n".join([f"{index + 1}. {option}" for index, option in enumerate(options)]))
    validInputs = [str(i + 1) for i in range(len(options))]
    validInput = False
    
    while not validInput:
        userInput = input(f"Select a version ({validInputs[0]}-{validInputs[-1]}): ")
        
        if userInput in validInputs:
            validInput = True
        else:
            print("Please enter a valid input.")
            
    return options[int(userInput) - 1]
    
if platform.system() == "Windows":
    pass
elif platform.system() == "Linux":
    pass
else:
    print("jvmd: unknown os detected")
    sys.exit()