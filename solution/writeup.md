# [Storyline](https://github.com/joelleoqiyi/BBCS-X-NoSQL/blob/master/Part2/storyline.md)... solved

## Downloading/Installing Packages...

Before we start to do anything, we realise that the only way to get any data whatsoever is through the database. And hence, we probably would need to use the **pymongo package**. But before we can use `import pymongo` in our program, we would need to install pymongo through the terminal/command line.
```
pip3 install pymongo
```
After installing pymongo on your computer or in gitpod, you realise that the connection string given starts with the following string of characters: `mongodb+srv://`, this means that the dnspython module also needs to be install in order for us to use the connection string (to connect to the database). Hence, we can install the dnspython module through the terminal/command line as such:
```
pip3 install dnspython
```

That should be all the packages you need to install for this game/stage.

---

## Importing pymongo and connecting to cluster -> database -> collection...

Before we start analysing the password to the safe, we first need to gain access to BuildingBloCS Land's MongoDB cluster. Given the URI/connection string to the database, as well as the names of the database and collection. We first need to import the `pymongo` module and its corresponding `MongoClient()` method.
```
import pymongo
from pymongo import MongoClient
```
Next, we need to connect to the MongoDB cluster, we can do this through the `MongoClient()` method we imported earlier. By passing the connection string into the `MongoClient()` method as a parameter, we have gained access to the cluster!
```
connectionString = "mongodb+srv://bbcs:amazingrace@cluster0-d9jjq.mongodb.net/test?retryWrites=true&w=majority"
cluster = MongoClient(connectionString)
```
Currently, we have only accessed the cluster but we have not accessed to the database and collection that stores our suspect's information. Remembering that a database is a subset of a cluster and a collection is a subset of a database.The relationship between a cluster,database and collection (in the context of the BuildingBloCS Land's Cluster) can be illustrated in the following diagram:
![](../img/MongoDB_structure.jpg)
So how can we access our database and collection? We could use the `.get_database()` method on our cluster. By passing the name of the database (in our case, we need to access the database called: `suspects_database`) into the `.get_database()` method as a parameter, we would have accessed the database!
```
db = cluster.get_database("suspects_database")
```
We would then do the same with the `.get_collection()` method on our database, to get from our database to our collection by passing the name of the collection into the `.get_collection()` method as a parameter.
```
collection = db.get_collection("suspects_collection")
```

---

## Now we need to analyse the structure of our document data...
Before we do anything else, we need to see how our data documents is structured in the collection. We can do that by arbitrarily printing out one of the documents. And, we can do that by using the `.find_one()` method on our collection. We would need to pass in an empty dictionary into the `.find_one()` method as we don't want anything to be filtered and want the entire document to be printed out.
```
print(collection.find_one({}))
```
Executing the code (and prettifying it a little) we get the following document,
```
{
  "_id":"5eb56f6e54d860f3bb3cbbff",
  "name":"Wilma Austin",
  "age":"27",
  "eyeColor":"green",
  "gender":"female",
  "company":"APEXTRI",
  "email":"wilmaaustin@apextri.com",
  "phone":"+1 (943) 478-3318",
  "address":"977 Dean Street, Thatcher, Massachusetts, 832",
  "registered":"2016-02-13T05:47:31 -08:00",
  "friends":[
    {
      "id":"0",
      "name":"Finch Contreras"
    },{
      "id":"1",
      "name":"Catalina Gonzalez"
    },{
      "id":"2",
      "name":"Browning Mcguire"
    }],
  "favoriteFruit":"strawberry"
}
```
All though, it might look quite confusing, but we do not need to understand everything and focus on what we need (which we will analyse later)

---

## Now let's analyse what do we need to find...
Quoting from the clues:
```
- the first 2 characters/numbers are the total number of people who are registered between 2017 to 2019 (inclusive)
- the next 2 characters/numbers are the total number of people whose company's name has the letter `E` as the second letter
- the last 2 characters/numbers are the **3rd and 4th character of the _id field of a person that fits the following criteria:
  1) likes either banana or strawberry or apple
  2) between the age of 30 to 50
  3) either female or male (no judgements...)
```
We then realise that the password needed can be split into 3 main steps each finding 2 characters of the password.

## So let's find the first 2 characters...
Quoting from clues again,`the first 2 characters/numbers are the total number of people who are registered between 2017 to 2019 (inclusive)`, we can see that we first need to find the *total number of people who are registered on 2017, 2018, 2019*
And upon inspecting our data structure, we realise that there is this field (in the documents) called `registered`, and the value of `registered` is a date-time string. The `registered` field and value looks something like this:
```
"registered":"2016-02-13T05:47:31 -08:00"
```
We then realise that the year at which the person is registered on can be deduced from the first 4 characters of the date-time string (the rest of the string is useless to us). Hence all we need to do is check through **all** the documents' `registered` field and check whether the value of that field has the first 4 characters as either `2017` or `2018` or `2019`.

But how do we check through the first 4 characters only? Well, one of the methods is to use the [$regex](https://docs.mongodb.com/manual/reference/operator/query/regex/) evaluation query operator. Regex is short form for *regular expressions*. We can craft "pattern" using regex and pass all the values of `registered` fields through the "pattern" to check if the value satisfy the "pattern". This allows us to check if the first 4 character is either `2017` or `2018` or `2019` as we can craft a "pattern" to do so. To craft the pattern needed, we need to first know a few simple syntax of regex,
the character column in the table below is the special metacharacters you can use in your "pattern" to check certain aspects of the string (being passed into it).

|Characters  |Description  |Examples|
|--|--|--|
|[ ] | A set of characters |"[A-M]"|
|\\ |Signals a special sequence (can also be used to escape special characters)|"\d"|
|.|Any character (except newline character)|"he..o"|
|^|Starts with|"^hello"|
|$|Ends with|"world$"|
|*|Zero or more occurrences|"aix*"|
|+|One or more occurrences|"aix+"|
|{ }|Exactly the specified number of occurrences|"al{2}"|
|\||Either or|"falls\|stays"|
|( )|Capture and group|**similar to parentheses

As such, if we want to check whether the first 4 characters are either `2017` or `2018` or `2019`, we could use the `^` metacharacters to check for the start parts of the string to see if it contains the substring of characters of either `2017` or `2018` or `2019`, and make 3 regex patterns to check for each of the years:
- `"^2017"`
- `"^2018"`
- `"^2019"`

We would then need to look at the `$regex` evaluation query operator's syntax (we are going to ignore the `$options` parameter as we will not use it):
```
{ <field>: { $regex: 'pattern', $options: '<options>' } }
```
We need to pass the value of the `registered` field into the regex pattern, hence we would replace `<field>` with the field we want to check aka `registered`, we would then replace `'pattern'` with our regex patterns. As such we can create our `$regex` evaluation query expression (for the year 2017) as such:
```
{"registered": {"$regex": "^2017"}}
```
We then realise the problem that each `$regex` evaluation query operator only accepts on pattern string (by default). Hence, how do we check for all 3 years at one go? One method is to use the [$or](https://docs.mongodb.com/manual/reference/operator/query/or/) logical query operator to query all 3 regex strings against the value of the `registered` field. The `$or` logical query operator has the following syntax:
```
{ $or: [ { <expression1> }, { <expression2> }, ... , { <expressionN> } ] }
```
We realise that all we need to do is to input our previously made `$regex` evaluation query expression in place of  `{<expression1> }, { <expression2> }, ... , { <expressionN> }` in the syntax string above to form our `$or` logical query expression:
```
{"$or": [
      {"registered": {"$regex": "^2017"}},
      {"registered": {"$regex": "^2018"}},
      {"registered": {"$regex": "^2019"}},
]}
```
After which, we can place the expression above into the filter parameter of the `.find()` method and apply it on our collection, this would filter all the documents within the collection, and find any document that has the value of its `registered` field starting with either `2017` or `2018` or `2019`:
```
result = collection.find({"$or": [
    {"registered": {"$regex": "^2017"}},
    {"registered": {"$regex": "^2018"}},
    {"registered": {"$regex": "^2019"}},
]})
for i in result:
  print(i)
```
If we run the above code, we realise that it does print out all the documents that fulfils the criteria we want. One of the documents printed out is as such (who is registered in 2019!!):
```
{
  '_id': '5eb56f6e5bc7cdd3eae844b1',
  'name': 'Jolene Weeks',
  'age': 20,
  'eyeColor': 'green',
  'gender': 'female',
  'company': 'DIGIRANG',
  'email': 'joleneweeks@digirang.com',
  'phone': '+1 (825) 446-3032',
  'address': '256 Seaview Avenue, Delshire, Alaska, 1439',
  'registered': '2019-10-20T09:32:22 -08:00',
  'friends': [
    {
      'id': 0,
      'name': 'Cole Walters'
    }, {
      'id': 1,
      'name': 'Mcdaniel Fitzpatrick'
    }, {
      'id': 2,
      'name': 'Rivers Wise'
    }],
  'favoriteFruit': 'strawberry'
}
```
But what we want, is not the documents themselves, but rather the number of documents, we can do this by using the [`collection.count_documents({...})`](https://docs.mongodb.com/manual/reference/method/db.collection.countDocuments/) method instead our `collection.find({...})` to count the number of documents that fulfils our criteria. Looking at the syntax of   `collection.count_documents()`:
```
collection.countDocuments( <query>, <options> )
```
We can replace `<query>` with the `$or` logical query expression we made previously (and ignore `<options>`) and changing our code:
```
result1 = collection.count_documents({"$or": [
    {"registered": {"$regex": "^2017"}},
    {"registered": {"$regex": "^2018"}},
    {"registered": {"$regex": "^2019"}},
]})
print(result1)
```
And if we run the code above, we get our the number of people who is registered from 2017-2019 (inclusive) to be 32. Therefore the first 2 characters of the password is `32`!!!

## Next, let's find the 3rd and 4th characters...
Quoting from clues again,`the next 2 characters/numbers are the total number of people whose company's name has the letter `E` as the second letter`, we can first see that we need to check out and analyse on the company names of the suspects to find those companies that have the letter "E" as the second character so a person working in `APEXTRI` would not be counted, and a person working in `ZENCO` would be counted in the total count. We then analyse the structure of the document in our collection, and realise that there is the field aptly called: `company`. Hence, we would have to analyse the `company` field to get our 3rd and 4th character.
```
"company":"APEXTRI"
```
Note: the company name is in all CAPS, this means that when we query later, we also need to keep this in mind and place our query in CAPS as well such that we can get a result (an empty dictionary would be returned if you use small characters because none of the values in the `company` field has small characters in it)

We then realise that since we need to check a string (value of `company` field) for a *certain kind of pattern*, we can use regex (again)! And looking back at the regex metacharacter above, we realise that we need to use the metacharacter `.` and `^` to form our regex "pattern".
- Why do we use the `.` metacharacter? This because the `.` allows `Any character (except newline character)` to pass through the regex pattern. Hence, it would be very suitable for using it to check for the presence of a first character since `.` can represent any character.
- Why do we use the `^` metacharacter? This is because our character to find is in the starting parts of the string hence we use `^` to search through the front parts of the string to see whether our string matches with the "pattern"/criteria given.
This leads us to form the following regex pattern (which would check to see if the string passed through it has the second character as `E`):
```
"^.E"
```
We then did what we did last time, and input the regex pattern into the `$regex` evaluation query operator in the `<pattern>` and replacing `<field>` with the field we want to check aka `company`:
```
{"company": {"$regex": "^.E"}}
```
But since, we also need to find the total number of people/document's that have the 2nd characters in its `company` field as `E`, hence we would be using (same as above), `.count_documents()` instead of `.find()`. Adding our `$regex` evaluation query expression and printing out the result, we get:
```
result2 = collection.count_documents({
    "company": {"$regex": "^.E"}
})
print(result2)
```
And if we run the code above, we get our the number of people who is working in a company that has the 2nd letter of its name to be `E` to be 13. Therefore the 3rd and 4th characters of the password is `13`!!!

## Next, let's find the last 2 characters...
Quoting from clues again,`3rd and 4th character of the _id field of a person....`, once again, your first instinct might be to read out and analyse all of the different criteria in order to find the person that fulfils those criteria.

**BUT**, if you decided to print out all of the documents, or in this case, we will just print out 2 of the documents:
```
{
  '_id': '5eb56f6e5bc7cdd3eae844b1',
  'name': 'Jolene Weeks',
  'age': 20,
  'eyeColor': 'green',
  'gender': 'female',
  'company': 'DIGIRANG',
  'email': 'joleneweeks@digirang.com',
  'phone': '+1 (825) 446-3032',
  'address': '256 Seaview Avenue, Delshire, Alaska, 1439',
  'registered': '2019-10-20T09:32:22 -08:00',
  'friends': [
    {
      'id': 0,
      'name': 'Cole Walters'
    }, {
      'id': 1,
      'name': 'Mcdaniel Fitzpatrick'
    }, {
      'id': 2,
      'name': 'Rivers Wise'
    }],
  'favoriteFruit': 'strawberry'
},
{
  "_id":"5eb56f6e54d860f3bb3cbbff",
  "name":"Wilma Austin",
  "age":"27",
  "eyeColor":"green",
  "gender":"female",
  "company":"APEXTRI",
  "email":"wilmaaustin@apextri.com",
  "phone":"+1 (943) 478-3318",
  "address":"977 Dean Street, Thatcher, Massachusetts, 832",
  "registered":"2016-02-13T05:47:31 -08:00",
  "friends":[
    {
      "id":"0",
      "name":"Finch Contreras"
    },{
      "id":"1",
      "name":"Catalina Gonzalez"
    },{
      "id":"2",
      "name":"Browning Mcguire"
    }],
  "favoriteFruit":"strawberry"
}
```
You should take a closer look at the `_id` of each of the documents and experiment a little with regex patterns and the collection itself. For example, using the following code:
```
result3 = collection.count_documents({
    "_id": {"$regex": "^5eb56f6e"}
})
print(result3)
```
We were able to run the code above, and realise that it prints out 80. Upon checking the number of documents there are in total (by running `print(collection.count_documents({}))` which essentially just counts all documents, since no filter is passed through the `<query>` parameter in the `.count_documents()`), we realise that there is 80 documents in the collection, which means that, **EVERY SINGLE** suspect's \_id start with the characters `5eb56f6e` which is way past our needed 3rd or 4th character of the \_id.

Knowing this *interesting* fact... we analyse the criterias given:
1) likes either banana or strawberry or apple
2) between the age of 30 to 50
3) either female or male (no judgements...)
which... you haven't noticed is literally the criteria which almost everyone (except for those of age younger than 30) fulfils, and since every single one of those potential people have the same starting \_id of `5eb56f6e`, we simply just take the 3rd and 4th character which is `b5` and that is our last 2 characters of our password.

*This teaches us to always briefly look through our data and find interesting similarities or differences before actually diving in to solve whatever problem we are solving*

---

## Piecing it together...

- The first 2 characters of the password is `32`
- The 3rd and 4th character of the password is `13`
- The last 2 characters of the password is `b5`

Concatenating them together, we get the password to be `3213b5` :laughing:

**Check out the python file nopipeline.py for a nosql solution to the problem above**

**Check out the python file pipeline.py for a nosql solution USING PIPE AGGREGATION to the problem above**

---

## Check out the workshop materials at [https://tinyurl.com/bbcs20nosql](https://tinyurl.com/bbcs20nosql)
