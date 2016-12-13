# NN
NTechLab assignment

## Description
* Rest service to find kNN in R radius among 1M records.
* Service supports CRUD operations with records
 
## Requirements
* Python language
* virtualenv for reproduction

## Implementation details
* Flask framework to process http requests
* SQLAlchemy and sqlite for storing data
* Unit and inegration tests

## Server deployment/cleanup

### Install project
* pip install virtualenv
* git clone https://github.com/DrNecromant/NN
* virtualenv NN
* cd NN
* . bin/activate
* pip install -r requirements.txt

### Start application
* python main.py

### Stop application
* CTRL+C

### Exit and remove project
* deactivate
* cd ..
* rm -r NN

## Usage and examples

### API usage

### Unittests
```
$python unittests.py
testDBUser (__main__.TestDB) ... ok
testDBUserStats (__main__.TestDB) ... ok
testAddInvalidUser (__main__.TestUserList) ... ok
testAddUser (__main__.TestUserList) ... ok
testAddiExistedUser (__main__.TestUserList) ... ok
testEmptyUserList (__main__.TestUserList) ... ok
testFullUserList (__main__.TestUserList) ... ok
testUserListPages (__main__.TestUserList) ... ok
testDeleteUser (__main__.TestUser) ... ok
testGetUser (__main__.TestUser) ... ok
testUpdateUser (__main__.TestUser) ... ok
testGetInfo (__main__.TestInfo) ... ok
testGetKnn (__main__.TestKnn) ... ok

----------------------------------------------------------------------
Ran 13 tests in 0.475s
OK
```

### Integration tests
```
$python integrationtests.py 
Generage 10000 users...
Get kNN by binary algorythm...
Get kNN by calculating all distances...
Results are equal 2559 2559

----------------------------------------------------------------------
Ran 1 test in 185.561s
OK
```

### Benchmark tests
```
$python benchmark.py 

test | attempt_id | radius | knn | exec_time

testBinarySearch 1 10 14 0.586269855499 
testBinarySearch 2 10 18 0.828803062439 
testBinarySearch 3 10 15 0.549397945404 
testBinarySearch 1 50 322 3.55142521858 
testBinarySearch 2 50 309 4.53496789932 
testBinarySearch 3 50 320 3.75467896461 
testBinarySearch 1 100 1264 5.76161003113 
testBinarySearch 2 100 1267 6.04228281975 
testBinarySearch 3 100 1243 5.056016922 
testBinarySearch 1 500 29780 4.59962797165 
testBinarySearch 2 500 31216 5.4956099987 
testBinarySearch 3 500 25684 3.68939399719 
testBinarySearch 1 1000 93543 5.79501605034 
testBinarySearch 2 1000 119628 6.90547990799 
testBinarySearch 3 1000 80905 3.77246212959 
testAllDistanceSearch 1 10 14 14.5994999409 
testAllDistanceSearch 2 10 18 14.5038819313 
testAllDistanceSearch 3 10 15 14.7285120487 
testAllDistanceSearch 1 50 322 14.439538002 
testAllDistanceSearch 2 50 309 14.9254710674 
testAllDistanceSearch 3 50 320 14.4932551384 
testAllDistanceSearch 1 100 1264 14.7746219635 
testAllDistanceSearch 2 100 1267 14.5922350883 
testAllDistanceSearch 3 100 1243 14.7975559235 
testAllDistanceSearch 1 500 29780 14.7092351913 
testAllDistanceSearch 2 500 31216 15.002371788 
testAllDistanceSearch 3 500 25684 14.5927751064 
testAllDistanceSearch 1 1000 93543 15.8682169914 
testAllDistanceSearch 2 1000 119628 15.1586270332 
testAllDistanceSearch 3 1000 80905 14.8813381195 

RESULTS:
	testAllDistanceSearch: 14.8044756889
	testBinarySearch: 4.06153618495
```

## License
Feel free to use my code on production environments and good luck. =)
