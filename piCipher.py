with open("pi1000000.txt", "r") as fileObj:
        PI = fileObj.read()
PI = PI[:1] + '0' + PI[2:(len(PI)-1)]
MAX_PI_SIZE = len(PI)

def getMode():
    while True:
        print('Do you wish to encrypt or decrypt a message?')
        mode = input().lower()
        if mode in ['encrypt', 'e', 'decrypt', 'd']:
            return mode
        else:
            print('Enter either "encrypt" or "e" or "decrypt" or "d".')

def getMessage():
    
    print('Enter your message:')
    return input()

def getKey():
    key = 0
    while True:
        print('Enter the key number:')
        try:
            key = int(input())
        except ValueError:
        	continue
        if (key >= 0 and key <= MAX_PI_SIZE):
            return key

def getTranslatedMessage(mode, message, key):
    messageLenght = len(message)
    
    translated = ''
    index = 0
    for symbol in message:
        symbolUniCode = ord(symbol)
        if mode[0] == 'e':
            symbolUniCode += int(PI[key+index])
            index += 1
        elif mode[0] == 'd':
        	symbolUniCode -= int(PI[key+index])
        	index += 1
        
        if symbolUniCode > 1114111:
            symbolUniCode -= 1114111
        elif symbolUniCode < 0:
                symbolUniCode += 1114111

        translated += chr(symbolUniCode)
        
    with open("translatedMessage.txt", "w") as fileObj:
        fileObj.write(translated)

    return translated
    
def main():
    mode = getMode()
    message = getMessage()
    key = getKey()

    translatedMessage = getTranslatedMessage(mode, message, key)

    print('Your translated text is:')
    print(translatedMessage)
    
if __name__ == '__main__':
	main()