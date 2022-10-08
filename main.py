import agent
import prueba
import display

def main():
    print("=============Filling album - Simulation based agents================================")
    print("How many agents should be simulated?")
    try:
        agents = abs(int(input()))
    except:
        print("Enter a valid number of agents")
    print("How many stickers have the album?")
    try:
        agents = abs(int(input()))
    except:
        print("Enter a valid number of stickers")
    
    Error = 0
    prueba.initialize()
    End = False
    while(not End and Error == 0):
        i = prueba.manageTimeAndSpace()
        if i == 1:
            prueba.event_1()
        if i == 2:
            prueba.event_2()
        if i == 3:
            prueba.event_3()
        if i == 4:
            prueba.event_4()
            
    prueba.generateReport()

if __name__ == "__main__":
    main()