# [Storyline](https://github.com/joelleoqiyi/BBCS-X-NoSQL/blob/master/Part2/storyline.md)... continued

Our sacred BuildingBloCS logo has been stolen! In the workshop, you managed to uncover that `Jeannie Johnson` was the culprit, and the police officers in BuildingBloCS land have tracked down and caught her! :grimacing:

However, to everyone's horror, the police were unable to find the sacred BuildingBloCS logo anywhere in Jeannie Johnson's house, but they were able to find a heavily locked up safe (which police suspect the logo is in) :weary:

Based on the house CCTV footage and fingerprint evidence, the following deductions can be made about the password to the safe:
- the first 2 characters/numbers are the **total number of people who are registered between 2017 to 2019 (inclusive)**
- the next 2 characters/numbers are the **total number of people whose company's name has the letter `E` as the second letter**
- the last 2 characters/numbers are the **3rd and 4th character of the _id field of a person that fits the following criteria:**
```
1) likes either banana or strawberry or apple
2) between the age of 30 to 50
3) either female or male (no judgements...)
```

Being the ONE AND ONLY data master (and person with logic) in BuildingBloCS land. Armed with access to all information about all civilians here. Can you use the gathered evidence to find out what the password to the safe is? :sweat_smile:

To gain access to information about all civilians, you would need to access BuildingBloCS Land's MongoDB cluster using the following URI/ connection string:
```
mongodb+srv://bbcs:amazingrace@cluster0-d9jjq.mongodb.net/test?retryWrites=true&w=majority
```
and access the following database and collection:
- database: `suspects_database`
- collection: `suspects_collection`

The fate of BuildingBloCS land lies in your hands. :exclamation::exclamation::exclamation:


## Check out the workshop materials at [https://tinyurl.com/bbcs20nosql](https://tinyurl.com/bbcs20nosql)

---

## Coding Platforms:

You can choose to do this in Gitpod or local or whatever platform you wish

If you are using gitpod, follow the following steps:
1) **you would have to fork this repository!** Follow this "tutorial" to learn how to fork a repository: [https://help.github.com/en/github/getting-started-with-github/fork-a-repo](https://help.github.com/en/github/getting-started-with-github/fork-a-repo)
2) **edit README.md (which is this file you are reading now)** Follow this "tutorial" to learn how to edit a file
3) **change the `<username>` on line 41 of markdown to your Github username**
4) **commit the changes you made** by scrolling down and click the `commit` button.
5) return back to README.md and **click the button below to open Gitpod** and start coding :laughing:

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/<username>/BBCS-X-NoSQL-AmazingRace)

Once you changed README.md, click the button above.

---

## Dataset used:

For this part of the Amazing Race, you would be using the `names.json` file as your dataset which is stored in the BuildingBloCS Land's MongoDB Cluster :laughing:

## How to submit:

After you found the password, return back to the `Amazing Race Website` to submit the password to not only recover the sacred BuildingBloCS logo (and bring everlasting happiness to BuildingBloCS land) but also to proceed on to the next stage

---

## Resources:

- Check out the workshop materials at [https://tinyurl.com/bbcs20nosql](https://tinyurl.com/bbcs20nosql)
- Check out MongoDB Documentation for CRUD operations at [https://docs.mongodb.com/manual/crud/](https://docs.mongodb.com/manual/crud/)
- Check out MongoDB Documentation for Pipeline Aggregation at [https://docs.mongodb.com/manual/reference/aggregation/](https://docs.mongodb.com/manual/reference/aggregation/)

**Full answers uploaded in the Answers folder in this repository**
