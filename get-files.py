#!/usr/bin/python

import urllib2
import json
import os

# Get Sample Ids based on project ID
projID = '18785778'
accessToken = '<add your basespace Access Token Here>'

fileList = []

def getSampleList(projectID, accToken):
    intOffset = 0
    sampleCount = 0
    sampleList = []
    url = 'https://api.basespace.illumina.com/v1pre3/projects/'+projectID+'/samples?SortBy=Id&SortDir=Desc&Offset=0&Limit=10&access_token='+accToken
    response = urllib2.urlopen(url)
    #List of Sample IDs
    data = json.load(response)

    #Check for Total Results

    totCount = data["Response"].get('TotalCount')
    
    while sampleCount != totCount:
        # Send request
        url = 'https://api.basespace.illumina.com/v1pre3/projects/'+projectID+'/samples?SortBy=Id&SortDir=Desc&Offset='+str(intOffset)+'&Limit=10&access_token='+accToken
        resp = urllib2.urlopen(url)    
        d = json.load(resp)

        items = data["Response"].get('Items')

        for item in items:
            sampleList.append(item.get('Id'))
            sampleCount += 1
        
        intOffset += 10
    
    return sampleList

def getFileIDs(sampleID, accToken):
    intOffset = 0
    fileCount = 0
    url = 'https://api.basespace.illumina.com/v1pre3/samples/'+sampleID+'/files?Extensions=gz&Offset=0&Limit=10&SortDir=Asc&access_token='+accToken
    response = urllib2.urlopen(url)
    #List of Sample IDs
    data = json.load(response)

    #Check for Total Results

    items = data["Response"].get('Items')

    for item in items:
        dic ={"filename":item.get('Name'),"id":item.get('Id')}
        fileList.append(item)        

# Get the list of Samples for the listed Project ID
sampleList = getSampleList(projID,accessToken)

# Get FileIds
for sample in sampleList:
    getFileIDs(sample,accessToken)

fileCount = 0

# Parse the fileList and download files
for fil in fileList:

    # Download File
    fileName = fil['Path']
    fileID =  fil['Id']
    url = 'https://api.basespace.illumina.com/v1pre3/files/'+fileID+'/content?access_token='+accessToken

    os.system('wget -O '+fileName+' '+url)

    # dataFile = urllib2.urlopen(url)
    # chunk = 4096

    # print "Downloading FileID: "+fileName+" --- Please be patient"

    # f = open(fileName, "w")
    # while 1:
    #     data = dataFile.read(chunk)
    #     if not data:
    #         print "done."
    #         break
    #     f.write(data)
    
    print "File: "+fileName+" Succesfully Downloaded"
    fileCount += 1

print str(fileCount) + " Files Downloaded"



