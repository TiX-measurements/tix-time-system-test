# tix-time-system-test
Repository containing the scripts and queries needed to perform the System Test on the TiX System.

## How to use this repo
This repo contains many tools to perform various System tests. But the most important one are the following instructions.

### How to perform a System Test
To perform a System test first you must download a Bittorrent client. We prefer to use [Vuze](https://www.vuze.com/), 
given its GUI and its very customizable scheduler. The next instructions are meant for that client.

You must create various profiles, throttling the speed at which the client will download the torrents. Once done this,
schedule the client to use them. We like to use the following setup.
```
daily pause_all from 00:00 to 01:00
daily unlimited from 01:00 to 02:00
daily 75_pct_speed from 02:00 to 03:00
daily half_speed from 03:00 to 04:00
daily 25_pct_speed from 04:00 to 05:00
daily pause_all from 05:00 to 23:59
```
Once done this, you must put some torrents to download. Make sure that the total of the files will be enough for all 
the test. We recommend using many Linux distro torrents for this (i.e.: Linux Mint, Linux Ubuntu, etc.)

Turn on the TiX Client, and let the torrent download during the night.

The next morning you only need to collect the data and see if the measurements are correct.

### How to use this test to collect samples for the tix-time-processor analysis notebook
