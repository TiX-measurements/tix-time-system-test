# tix-time-system-test
Repository containing the scripts to perform the Calibration Test on the TiX System.

## Getting Started

This repository contains all the tools necessary to perform calibration tests on your system. The tests were designed to run in Debian based distributions, in particular Ubuntu and Raspbian.

### Prerequisites

In order to run the tests, the systems needs to be able to run the [tix-time-client](https://github.com/TiX-measurements/tix-time-client). Therefore, the dependencies required are:

* Java 8
* Gradle 3

### Installing

To install the system test, run the following script:

```bash
git clone https://github.com/TiX-measurements/tix-time-system-test.git
cd tix-time-system-test
./setup.sh
```

The setup.sh script installs Python 3, PyYaml and downloads the `tix-time-client` repository.

### Running

To run the test, use the following script:

```bash
./calibration_test.py -u username -p password -i installation -P port -l logs_directory -tcf test_configuration_file
```

All the arguments must be specified to run the script. During the test, the ouput will look like the following lines:

```bash
Test will start in 0.19360786666666666 minutes
Starting tix time client
Starting calibration test
2018-12-08 13:45:00.020179  =>  Torrent started
2018-12-08 13:45:08.031301  =>  Changed speed to 0
2018-12-08 13:47:13.131312  =>  Changed speed to 7500
2018-12-08 13:49:18.264643  =>  Changed speed to 15000
2018-12-08 13:51:21.367613  =>  Changed speed to 22500
2018-12-08 13:53:24.508206  =>  Changed speed to 30000
2018-12-08 13:55:27.622741  =>  Changed speed to 0
2018-12-08 13:57:32.764442  =>  Stopping Torrent
2018-12-08 13:57:35.693646  =>  Torrent Stopped
Stopping tix time client
Tix time client Stopped
```

After the test finishes, the results are stored in the logs_directory with the following structure:

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
* network_usage.log : Log with the estimated download speed in kbps from the local interface
* torrent_client.log : Log with stdout of torrent client spawned during calibration test
* description.yml : Test configuration file used during test
* tix-time-client-logs/ : Directory for tix-time-client log files

### Test Configuration

The test uses a torrent client to simulate the usage of network. At the beginning of the test, the torrent client adds all the torrent files specified in [torrents](torrents). By default, the following torrent files are included in the folder but its contents can be modified but the user depending on the tests to run. All downloads are sent do `/dev/null` every minute so space should not be a limitation for the calibration test.

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

On the other hand, the user can select which test configuration file to use in each test. The configuration file has the following structure:

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

* The max_speed is measured in kilobits per second
* The start time convention is 'HH:MM' using a 24-hour clock. It corresponds to the time in the current or following day, but it never exceeds 24 hours
* The intervals should be in ascending order in terms of the speed percentage to guarantee that the torrent speed is stable when it changes the speed