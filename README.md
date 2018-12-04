# tix-time-system-test
Repository containing the scripts to perform the Calibration Test on the TiX System.

## Getting Started

This repository contains all the tools necessary to perform calibration tests on your system. The tests were designed to run in Debian based distributions, in particular Ubuntu and Raspbian.

### Prerequisites

In order to run the tests, the systems needs to be able to run the tix-time-client. Therefore, the dependencies required are:

* Java 8
* Gradle 3

### Installing

To install the system test, run the following script:

```bash
git clone https://github.com/eduardoneira/tix-time-system-test
cd tix-time-system-test
./setup.sh
```

The setup.sh script installs Python 3, PyYaml and downloads the tix-time-client repository.

### Running

To run the test, use the following script:

```bash
./calibration_test.py -u user -p password -i installation -P 4500 -l logs_directory -tfc test_file_configuration
```

All the arguments must be specified to run the script. The result after the test finishes is saved in the logs_directory with the following structure:


```
./logs_directory/
  |
  |__ client.log
  |__ network_usage.log
  |__ torrent_client.log
  |__ description.yml
  |__ tix-time-client-logs/
      |__ 1-tix-log.json
      |__ 2-tix-log.json
      |__ ...
```

* client.log : Log with stdout of tix-time-client spawned during calibration test
* network_usage.log : Log with the estimated download speed from the local interface
* torrent_client.log : Log with stdout of torrent client spawned during calibration test
* description.yml : Test configuration file used during test
* tix-time-client-logs/ : Directory for tix-time-client log files

### Test Configuration

The test uses a torrent client to simulate the usage of network. At the beginning of the test, the torrent client adds all the torrent files specified in [torrents](torrents). By default, the following 8 torrent files are included in the folder but its contents can be modified but the user depending on the tests to run.

```
./torrents/
  |
  |__ linuxmint-17-cinnamon-32bit-v2.iso.torrent
  |__ linuxmint-17-cinnamon-64bit-v2.iso.torrent
  |__ linuxmint-17-cinnamon-nocodecs-32bit-v2.iso.torrent
  |__ linuxmint-17-cinnamon-nocodecs-64bit-v2.iso.torrent
  |__ linuxmint-17-cinnamon-oem-64bit-v2.iso.torrent
  |__ linuxmint-17-kde-dvd-32bit.iso.torrent
  |__ linuxmint-17-kde-dvd-64bit.iso.torrent
  |__ linuxmint-17-mate-32bit-v2.iso.torrent
  |__ linuxmint-17-mate-64bit-v2.iso.torrent
  |__ ubuntu-14.04.5-desktop-amd64.iso.torrent
  |__ ubuntu-14.04.5-desktop-i386.iso.torrent
  |__ ubuntu-14.04.5-server-amd64.iso.torrent
  |__ ubuntu-14.04.5-server-i386.iso.torrent
  |__ ubuntu-16.04.5-desktop-amd64.iso.torrent
  |__ ubuntu-16.04.5-desktop-i386.iso.torrent
  |__ ubuntu-16.04.5-server-amd64.iso.torrent
  |__ ubuntu-16.04.5-server-i386.iso.torrent
  |__ ubuntu-18.04.1-desktop-amd64.iso.torrent
  |__ ubuntu-18.04.1-live-server-amd64.iso.torrent
  |__ ubuntu-18.10-desktop-amd64.iso.torrent
  |__ ubuntu-18.10-live-server-amd64.iso.torrent
```

On the other hand, the user can select which test file configuration to use in each test. The configuration file has the following structure:

```yaml
max_speed_kbps : 12000
network_interface: 'wlan0'
start_time : '00:00'
intervals :
  - duration_minutes : 60
    speed_percentage : 0
 
  - duration_minutes : 60
    speed_percentage : 25
 
  - duration_minutes : 60
    speed_percentage : 50 
 
  - duration_minutes : 60
    speed_percentage : 75

  - duration_minutes : 60
    speed_percentage : 100
 
  - duration_minutes : 60
    speed_percentage : 0
```

#### Considerations

* The speed is measured in kilobits per second
* The start time corresponds to the time in the current or following day, but it never exceeds 24 hours
* The intervals should be in ascending order in terms of the speed percentage to guarantee that the torrent speed is stable