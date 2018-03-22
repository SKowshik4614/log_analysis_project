# Log Analysis Project
This program analyzes the log details from the given data from logs provided. This is an **internal reporting** tool that will use information from the database to discover what kind of articles the site's readers like.

#### Here we use 2 files:
1. log_analysis.py
2. Vagrantfile
3. log_analysis_output.png

### Tools required:
1. Vagrant [**(Download)**](https://www.vagrantup.com/downloads.html)
2. Virtualbox [**(Download)**](https://www.virtualbox.org/wiki/Downloads)

### Code Details:
* [log_analysis.py](https://github.com/SKowshik4614/log_analysis_project/blob/master/log_analysis.py) is the python file that calculates and displayes the required output. This contains the sql code to fetch the necessary information from databse,python code to populate and display the desired output.
* [Vagrantfile](https://github.com/SKowshik4614/log_analysis_project/blob/master/Vagrantfile) is the file that has the configuration to install and start the Virtual Machine. Using this file we can start the VM and databases.
* [log_analysis_output.png](https://github.com/SKowshik4614/log_analysis_project/blob/master/log_analysis_output.png) is the image file that displays the output after the python code is run.

### How to Execute the code:
1. Download all the files to your local machine from [repository](https://github.com/SKowshik4614/log_analysis_project.git).
2. Extract the files into a folder(make sure all required files are in same folder).
3. Open a command prompt on your computer and run **`vagrant up`** to start the VM.
4. Once the VM is up, run **`vagrant ssh`** to login to the VM.
5. Once you get into the VM command line, navigate to the shared folder from you local machine **`/vagrant`**. This will have below 4 files.
    * catalog  
    * forum 
    * tournament  
    * Vagrantfile
6. Dowload the [data set from here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) and copy the sql file into the shared folder(`/vagrant`).
7. Once the `newsdata.sql` is copied into shared folder, run below command to import Database.
    * **Command:**```psql -d news -f newsdata.sql```
8. Run `psql -d news` to login to the databse **`news`**.
9. Run `\dt` to explore or view the tables.
10. Copy the python code to your shared folder and execute as below command.
    * **Command**: **`python log_analysis.py`**
11. If the code runs without errors, below output is displayed.
```
vagrant@vagrant:/vagrant$ python log_analysis.py
==================================================
Most Popular 3 Articles:
Candidate is jerk, alleges rival ==> 338647 views
Bears love berries, alleges bear ==> 253801 views
Bad things gone, say good people ==> 170098 views
==================================================
Most Popular Article Authors of All Time:
Ursula La Multa ==> 507594 views
Rudolf von Treppenwitz ==> 423457 views
Anonymous Contributor ==> 170098 views
Markoff Chaney ==> 84557 views
==================================================
More than 1% of Requests Errors:
2016-07-17 ==> 2.26% errors
```
### Code Snippet:
##### Query:1
To fetch the `top 3 articles of all time`, below is the view created.
```sql
create or replace view popular_articles as 
select title, count(title) as views from articles,log 
where log.path = concat('/article/',articles.slug) group by title 
order by views desc limit 3;
```
##### Query:2
To fetch the `Most Popular Article Authors of All Time`, below is the view created.
```sql
create or replace view popular_authors as 
select authors.name,count(articles.author) as views from articles, log, authors where log.path = concat('/article/',articles.slug) and articles.author = authors.id group by authors.name order by views desc;
```
##### Query:3
To fetch the `More than 1% of Requests Errors`, below is the view created.
```sql
create or replace view log_status as 
select Date,Total,Error,(Error::float*100)/Total::float as Percent from 
(select time::timestamp::date as Date, count(status) as Total, sum(case when status = '404 NOT FOUND' then 1 else 0 end) as Error from log 
group by time::timestamp::date) as result 
where (Error::float*100)/Total::float > 1.0 order by Percent desc;
```
### Contribution:
Please feel free to make changes to the code and [contribute](https://github.com/SKowshik4614/log_analysis_project.git) to make the code work better.