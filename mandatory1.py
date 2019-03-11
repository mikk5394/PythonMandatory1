import sys
import os
import subprocess
import glob
from urllib.request import urlopen
from urllib.error import HTTPError

#Step 1
#Collects everything from the API and saves it in a html variable
api = urlopen('https://api.github.com/orgs/python-elective-1-spring-2019/repos?per_page=100')
#Converts it to a String so we can work with it
findCloneUrls = api.read().decode('utf-8')

#Finds the last index where the clone_url occurs
lastIndex = findCloneUrls.rfind('"clone_url"')

index = 0
urlList = []

while True:

    index = findCloneUrls.find('"clone_url"', index+1)

    #Adds the url to the list
    cloneUrl = findCloneUrls[index+13:findCloneUrls.find(',', index)-1]
    urlList.append(cloneUrl)

    #Breaks the while loop after the last clone_url has been found
    if index == lastIndex:
        break


#step 2
#Creates a directory if it hasn't been done already
if not os.path.exists('ClonedRepos'):
    os.makedirs('ClonedRepos')

#Goes into the newly created directory
os.chdir('ClonedRepos')

#Clones all repos and make a directory for each repo
#If a repo directoy already exist, no new directory is made and the repo is pulled instead
for n in urlList:
    
    #Jumps 49 chars into the url to make "pretty" directory names
    dirName = n[49:-4]
    if not os.path.exists(dirName):
        subprocess.run(['git', 'clone', n])
        print('cloned')
    else:
        os.chdir(dirName)
        subprocess.run(['git', 'pull'])
        os.chdir('..')
        print('pulled')


#step 3

readMeList = []
#Uses glob to try and get a readme file in every directory if there is any - note the star
for readMe in glob.glob('/Users/mikkel/Desktop/Python/Mandatory/ClonedRepos/*/readme.md'):
    readmefile = open(readMe).read()
    readMeList.append(readmefile)


#step 4

requiredReadingList = []

for c in readMeList:

    index = c.find('## Required reading')
    #Checks for a required reading paragrahp inside every readme file - not every file has one
    if index != -1:
        required = c[index+19:c.find('##', index+19)]
        requiredReadingList.append(required)
      

#step 5
#Samme principle as in step 2
os.chdir("..")
if not os.path.exists('Pensum'):
    os.makedirs('Pensum')
os.chdir('Pensum')

pensum = open('required_reading.md', 'w')

requiredReadingListSplit = []

#Removes whitespaces by taking every char between * and * and then inserting that
#String into a new list where it fills only one line

for c in requiredReadingList:
    index = 1
    while True:
        oneLineRequiredReading = c[index:c.find('*', index+1)-1] + '\n'
        requiredReadingListSplit.append(oneLineRequiredReading)
        index = c.find('*', index+1)

        if index == c.rfind('*'):
            break

  

for index, value in enumerate(requiredReadingListSplit):
    for idx, val in enumerate(value):
        if val.isalpha() and val.isupper():
            break
        if val.isalpha and val.islower():
            requiredReadingListSplit[index] = value[:idx] + value.upper() + value[idx+1:]
            break

#Removes duplicates since keys are unique
requiredReadingListSplit = list(dict.fromkeys(requiredReadingListSplit))

#Sorting to make the list alphabetical
requiredReadingListSplit.sort()

for c in requiredReadingListSplit:
    pensum.write(c)

subprocess.run(['open', 'required_reading.md'])


# step 6
os.chdir('..')
subprocess.run(['git', 'pull', '--rebase', 'https://github.com/mikk5394/PythonMandatory1.git', 'master'])
subprocess.run(['git', 'init'])
subprocess.run(['git', 'add', '--all'])
commit = input('Enter commit:')
subprocess.run(['git', 'commit', '-am', commit])
subprocess.run(['git', 'remote', 'add', 'origin', 'https://github.com/mikk5394/PythonMandatory1.git'])
subprocess.run(['git', 'remote', '-v'])
subprocess.run(['git', 'push', '--set-upstream', 'origin', 'master'])
