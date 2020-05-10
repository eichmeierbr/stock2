import kDayClassifier
import stock_market as sm

def array2dataset(inArray, windowSize):
    data = []
    for i in range(0,len(inArray)-windowSize):
        features = inArray[i:i + windowSize]
        target = inArray[i+windowSize]
        data.append([features,target])
    return data


def evaluateClassifier(classifier, numDays, endDay, which='Open'):
    inputSize = classifier.inputSize
    numDays = classifier.days+numDays
    data = sm.dayToDayDiffPercent(classifier.ticker,which=which, numDays = numDays, endDay = endDay)

    split_data = array2dataset(data, inputSize)
    actions = []
    percentDiff = 0
    for day in split_data:
        action = classifier.predict(day[0])
        if action: percentDiff += day[1]
        actions.append(action)
    a=4    
    return percentDiff