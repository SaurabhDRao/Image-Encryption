from utils import convertNumToBinary, convertBinaryToNum, convertCharToBinary, splitIntoParts, mergeParts
from DES import applyDES
import cv2
import numpy

# ---DES Key---
# create a des key using a list of numbers (should be 8 numbers) or a string with 8 characters
print(("-" * 30) + "MENU" + ("-" * 30))
print("1-List of 8 numbers \n2-A string with 8 characters\n" + ("-" *  64))
choice = int(input("Enter your preferred format (1 or 2): "))
deskey = ""
# check if any number other than 1 and 2 is entered
if((choice != 1) and (choice != 2)):
    print("Invalid choice format!")
    exit(0)
else:
    # take the input
    print("Enter the key:", end = " ")
    # check if format is list of numbers
    if(choice == 1):
        k = [int(x) for x in input().split()]
        # check if key length in not 8 numbers
        if(len(k) != 8):
            print("\nYou need to enter a list of 8 numbers!")
            exit(0)
        # convert the list of numbers into binary string
        deskey = convertNumToBinary(k)
    # take the string as input
    else:
        k = input()
        # check if key is not 8 characters
        if(len(k) != 8):
            print("\nYou need to enter a string of 8 characters!")
            exit(0)
        # convert the text string into binary string
        deskey = convertCharToBinary(k)
print("-" * 64)
ENCRYPT = "ENCRYPT"
DECRYPT = "DECRYPT"

# ---Encryption---
# read the image
imgPath = "./geass-gray-img.jpg"
img = cv2.imread(imgPath, 0)
# get the width and height of the image
w, h = img.shape
print("Encrypting...")
# iterate through each row
for i in range(h):
    # first split the row values into groups of 8
    imgListIntoParts = splitIntoParts(img[i], 8)
    # then iterate through each group
    for k in range(len(imgListIntoParts)):
        # convert the list into a binary string
        pltxt = convertNumToBinary(imgListIntoParts[k])
        # apply the DES for the binary string in encryption mode
        cipher = applyDES(pltxt, deskey, ENCRYPT)
        # convert the binary string into number list and create a list of type uint8 for the encrypted binary string
        cipherList = numpy.array(convertBinaryToNum(cipher), dtype=numpy.uint8)
        # replace the original value with the cipher value
        imgListIntoParts[k] = cipherList
    # replace the original row value with the new ciphered value
    img[i] = mergeParts(imgListIntoParts)
print("Encryption done!")
# show the encrypted image
cv2.imshow("encrypted image", img)
cv2.waitKey(0)
# save the encrypted image to this directory
cv2.imwrite("./encrypted.png", img)
print("Saved the encrypted image into current directory!")
cv2.destroyAllWindows()

print("-" * 64)

# ---Decryption---
# read the encrypted image
imgPath = "./encrypted.png"
img = cv2.imread(imgPath, 0)
# get the width and height of the image
w, h = img.shape
print("Decrypting...")
# iterate through each row
for i in range(h):
    # first split the row values into groups of 8
    imgListIntoParts = splitIntoParts(img[i], 8)
    # then iterate through each group
    for k in range(len(imgListIntoParts)):
        # convert the list into a binary string
        cipher = convertNumToBinary(imgListIntoParts[k])
        # apply the DES for the binary string in decryption mode
        decrypted = applyDES(cipher, deskey, DECRYPT)
        # convert the binary string into number list and create a list of type uint8 for the decrypted binary string
        decryptedList = numpy.array(convertBinaryToNum(decrypted), dtype=numpy.uint8)
        # replace the original value with the decrypted value
        imgListIntoParts[k] = decryptedList
    # replace the original row value with the new decrypted value
    img[i] = mergeParts(imgListIntoParts)
print("Decryption done!")
# show the decrypted image
cv2.imshow("decrypted image", img)
cv2.waitKey(0)
# save the decrypted image to this directory
cv2.imwrite("./decrypted.jpg", img)
print("Saved the decrypted image to current directory!")
cv2.destroyAllWindows()

print("-" * 64)