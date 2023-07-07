# Movix UGC

[![CI: UGC](https://github.com/stranded-in-python/movix-ugc/actions/workflows/ci.yml/badge.svg)](https://github.com/stranded-in-python/movix-ugc/actions/workflows/ci.yml)

## What is this?

This is a project of 7th group of 24th stream of Yandex Practicum for Middle Python Developers. The goal of the project is to build a online streaming platform.

This repository contains User Generated Content Service (UGC).

Features of UGC service:

-   watching progress

## What is under the hood?

Fastapi, Kafka, ClickHouse

ClickHouse was chosen as distributed storage due to its perfomance in synthetic tests. Other options included Vertica and Greenplum.

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
func:'check_read_while_write' took: 207.7469 sec

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
func:'chech_read' took: 0.0625 sec## Output

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

</details>

### Project Architecture

<details>
<summary>Scheme of UGC service</summary>

![movix-ugc](https://github.com/stranded-in-python/movix/blob/main/media/movix-ugc.png)

</details>

## How to install && deploy

Go to the main repo [movix](https://github.com/stranded-in-python/movix) for instructions.
