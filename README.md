# Movix UGC

[![CI: UGC](https://github.com/stranded-in-python/movix-ugc/actions/workflows/ci.yml/badge.svg)](https://github.com/stranded-in-python/movix-ugc/actions/workflows/ci.yml)

## What is this?

This is a project of 7th group of 24th stream of Yandex Practicum for Middle Python Developers. The goal of the project is to build a online streaming platform.

This repository contains User Generated Content Service (UGC).

Features of UGC service:

-   watching progress

## What is under the hood?

Fastapi, Kafka, ClickHouse, MongoDB

ClickHouse was chosen as distributed storage due to its perfomance in synthetic tests. Other options included Vertica and Greenplum.

To launch benchmarks: 
* cd /benchmark 
* choose and cd to folder with a db you are intested in
* In the root of db folder: docker compose -f up -d --build
* While waiting for containters to launch install requirements at requirements/local.txt in the root of db folder
* In the root of db folder run "run.py"

<details>
<summary>Greenplum and Vertica</summary>

## Greenplum

* Greenplum's docker-compose is located in "docker" folder: docker compose -f up -d --build
* Greenplum's "run.py" is located in greenplum/src/

## Vertica

* Vertica's "run.py" is named "main.py" and located in vertica/src/

</details>

Note: You can also edit generating content scripts at utils.py. It is also crucial to edit pre-test scripts concerning all dbs except MongoDB

<details>
<summary>Benchmark results</summary>

## Output

Created database, table, inserted 10000000 rows

### Clickhouse

#### Write
func:'check_write' took: 0.0220 sec
#### Read
Selected 1000 rows
Sample Data: ['1509', '218846485', '6402693977', '2007-03-26 21:33:32']
func:'check_read' took: 0.0809 sec

#### Read And Write on Load
Selected 1000 rows
Sample Data: ['1509', '218846485', '6402693977', '2007-03-26 21:33:32']
func:'check_read' took: 0.0135 sec
func:'check_write' took: 0.0205 sec

### Vertica

#### Write
func:'check_write' took: 472.5615 sec

#### Read
Selected 10000000 rows
Sample Data:
['1698400264', '6350138181', '2329006959', '1997-01-21 15:24:22']
func:'chech_read' took: 0.3870 sec

#### Read And Write on Load

Selected 10000000 rows
Sample Data: ['8497188662', '2435800366', '5013646629', '2015-12-13 04:44:03']
func:'chech_read' took: 0.0625 sec


### Greenplum

#### Write
func:'check_write' took: 472.5615 sec

#### Read
Selected 10000000 rows
Sample Data:
['1698400264', '6350138181', '2329006959', '1997-01-21 15:24:22']
func:'chech_read' took: 0.3870 sec

#### Read And Write on Load

Selected 10000000 rows
Sample Data: ['8497188662', '2435800366', '5013646629', '2015-12-13 04:44:03']
func:'chech_read' took: 0.0625 sec

### MongoDB

#### Write
Inserted 1000 rows
func:'check_write_likes' took: 0.1114 sec
func:'check_write_bookmarks' took: 0.2343 sec
func:'check_write_reviews' took: 1.9533 sec

#### Read
Selected 1000 rows
func:'check_read_likes' took: 0.0039 sec
func:'check_read_bookmarks' took: 0.0033 sec
func:'check_read_reviews' took: 0.0149 sec

#### Read And Write on Load
Selected 1000 rows
func:'check_read_likes' took: 0.0130 sec
func:'check_read_bookmarks' took: 0.0030 sec
func:'check_read_reviews' took: 0.0119 sec
Inserted 1000 rows
func:'check_write_likes' took: 0.1235 sec
func:'check_write_bookmarks' took: 0.2437 sec
func:'check_write_reviews' took: 1.9946 sec

### PostgreSQL

#### Write
Inserted 1000 rows
func:'check_write_likes' took: 4.6993 sec
func:'check_write_bookmarks' took: 4.9062 sec
func:'check_write_reviews' took: 4.6401 sec

#### Read
Selected 1000 rows
func:'check_read_likes' took: 0.0504 sec
func:'check_read_bookmarks' took: 0.0102 sec
func:'check_read_reviews' took: 0.0626 sec

#### Read And Write on Load
Selected 1000 rows
func:'check_read_likes' took: 0.0064 sec
func:'check_read_bookmarks' took: 0.0047 sec
func:'check_read_reviews' took: 0.0377 sec
Inserted 1000 rows
func:'check_write_likes' took: 2.4458 sec
func:'check_write_bookmarks' took: 2.9509 sec
func:'check_write_reviews' took: 3.6189 sec

### Summary
We chose MongoDB due to its perfomance in read/write benchmark including the perfomance on load even on relatively weak machine for our ugc endpoints.
The reading is outstanding and the writing is decent compared to other dbs. Pros: MongoDB is easy to deploy, its collections are flexible,
almost no preparations needed to use it out of box. Cons: unusual syntax for those who is used to relational DBs.

</details>

### Project Architecture

<details>
<summary>Scheme of UGC service</summary>

![movix-ugc](https://github.com/stranded-in-python/movix/blob/main/media/movix-ugc.png)

</details>

## How to install && deploy

Go to the main repo [movix](https://github.com/stranded-in-python/movix) for instructions.
