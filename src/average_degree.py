import sys
from datetime import datetime

def calculateAvg(mapping):
    #function that calculate avg
    global outputFile
    finalMap = {}
    for i in mapping.keys():
        hash_tag = mapping[i]
        for k in hash_tag.keys():
            if k in finalMap.keys():
                finalMap[k] = finalMap[k]+hash_tag[k]
            else:
                finalMap[k] = hash_tag[k]
    counter = len(finalMap)
    sum = 0
    for j in finalMap.keys():
        sum += finalMap[j]
    if counter == 0:
        outputFile.write("%.2f" % 0.0)
	outputFile.write("\n")
    else:
        outputFile.write("%.2f" % (sum*1.0/counter))
	outputFile.write("\n")
def retriveHashtag(tags):
        #funtion that returns hashtags given the raw data
        global mainMap
        hashtagMap = {}
        if len(tags)==0:
                return hashtagMap
        else:
             	tempList = tags.split('{"text":"')
                if len(tempList)==2:
                        return hashtagMap
                else:
                     	for tempItem in tempList:
                                if tempItem != "":
                                        tempHashtag = tempItem.split('","indices"')[0]
                                        hashtagMap[tempHashtag]=0
                        if len(hashtagMap) == 1:
                            return {}
                        else:
                            tempKeys = hashtagMap.keys()
                            for j in tempKeys:
                                position = tempKeys.index(j)
                                for k in tempKeys[position+1:]:
                                    counter = 0
                                    if len(mainMap) > 0:
                                        for m in mainMap.keys():
                                            if ((j not in mainMap[m].keys()) and (k not in mainMap[m].keys())):
                                                counter += 1
                                        if counter == len(mainMap):
                                            hashtagMap[j] = hashtagMap[j] + 1
                                            hashtagMap[k] = hashtagMap[k] + 1
                                    else:
                                        hashtagMap[j] = hashtagMap[j] + 1
                                        hashtagMap[k] = hashtagMap[k] + 1
                            for n in hashtagMap.keys():
                                if hashtagMap[n] == 0:
                                    del hashtagMap[n]
                            return hashtagMap
def main():
        global mainMap
        global outputFile
	tweet = open(sys.argv[1],'r')
	outputFile = open(sys.argv[2],'w')
	mainMap = {} ### main hashtag mapping list
        maxTime = '1900-01-01 00:00:00'
        for line in tweet.readlines():
            if '{"limit"' not in line:
                        newTimeStamp = datetime.strptime(line[15:45],'%a %b %d %H:%M:%S +0000 %Y')
                        if (newTimeStamp - datetime.strptime(maxTime,'%Y-%m-%d %H:%M:%S')).days >= 0 :
                                ### update maxTime and delete outof 60s range entries and calculate avg
                                maxTime = str(newTimeStamp)
                                for item in mainMap.keys():
                                        if (datetime.strptime(maxTime,'%Y-%m-%d %H:%M:%S') - datetime.strptime(item,'%Y-%m-%d %H:%M:%S')).seconds > 60:
                                                #### delete nodes that are outof range 
                                                del mainMap[item]
                                ## retrieve and add hashtags
                                hashtagList = retriveHashtag(line.split('hashtags":[')[1].split('],"urls')[0])
                                for hashtag in hashtagList.keys():
                                        if maxTime in mainMap.keys():
                                                if hashtag in mainMap[maxTime].keys():
                                                        mainMap[maxTime][hashtag] = mainMap[maxTime][hashtag] + hashtagList[hashtag]
                                                else:
                                                        mainMap[maxTime][hashtag] = hashtagList[hashtag]
                                        else:
                                                mainMap[maxTime] = {hashtag:hashtagList[hashtag]}
                                ## calculate Avg
                                calculateAvg(mainMap)
                        elif (datetime.strptime(maxTime,'%Y-%m-%d %H:%M:%S') - newTimeStamp).seconds > 60:
                                ## new tweet comes late and is out side 60s range, just ignore and calculate Avg
                                calculateAvg(mainMap)
                        else:
                                ## new tweet comes late and is inside the 60s range
                                hashtagList = retriveHashtag(line.split('hashtags":[')[1].split('],"urls')[0])
                                for hashtag in hashtagList.keys():
                                        if maxTime in mainMap.keys():
                                                if hashtag in mainMap[maxTime].keys():
                                                        mainMap[maxTime][hashtag] = mainMap[maxTime][hashtag] + hashtagList[hashtag]
                                                else:
                                                        mainMap[maxTime][hashtag] = hashtagList[hashtag]
                                        else:
                                                mainMap[maxTime] = {hashtag:hashtagList[hashtag]}
                                ## calculate
                                calculateAvg(mainMap)
        tweet.close()
main()
