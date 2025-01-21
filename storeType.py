stores = ["kiriana shop", "clothing store", "handicraft shop", "restuarant"]
storesIndexed = ["1. kiriana shop", "2. clothing store", "3. handicraft shop", "4. restuarant"]

def selectStoreType():
    options = "what is your store type: \n" + "\n".join(storesIndexed)
    return options

def askData(inputList, messageFunction):
    for data in inputList:
        message = messageFunction(data)
        yield message

def optionSelected(storeType):
    match storeType:
        case '1' | 'kiriana shop':
            import kirianaRegistration
            askdataGenerator = askData(kirianaRegistration.inputDataKiriana, kirianaRegistration.send_message_kiriana)
            return askdataGenerator
        case '2' | 'clothing store':
            import clothingRegistration
            askdataGenerator = askData(clothingRegistration.inputDataClothing, clothingRegistration.send_message_clothing)
            return askdataGenerator
        case '3' | 'handicraft shop':
            import handicraftRegistration
            askdataGenerator = askData(handicraftRegistration.inputDataHandicraft, handicraftRegistration.send_message_handicraft)
            return askdataGenerator
        case '4' | 'restuarant':
            import resturantRegistration
            askdataGenerator = askData(resturantRegistration.inputDataresturant, resturantRegistration.send_message_resturant)
            return askdataGenerator
        case _:
            print("Invalid option selected")
