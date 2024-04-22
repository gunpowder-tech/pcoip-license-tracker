# pcoip license tracker tracker

the script here has been adapted from a conversation on the AWS Thinkbox forums: https://forums.thinkboxsoftware.com/t/a-script-to-list-available-licenses-from-ubl-servers/30039/4. 

the script has been modified to run in a continuous loop and instrumented with prometheus metrics that can be scraped by prometheus.

## build container image

see Dockerfile for specifics, but
```
docker build . -t <repository_build_info>
```

NOTE**: if you're building on an M1 mac but running the container on a linux x86_64 based system, make sure you set `--platform x86_64` when you build the container.

## grafana dashboard

a grafana dashboard can be found at `ubl.json`. this dashboard is compatible with grafana 8+
the variables need tweaking to properly repeat, PRs welcome

## prometheus alerting rules

PRs welcome

## usage / orchestration information

you need to set:

FNO_SERVER, FNO_PASSWORD and LISTEN_PORT (optional, defaults to 9666) when running this script or the built container.

NOTE**: if you plan to run this outside of docker you'll need to `pip install prometheus_client requests`.

example:

```
docker build . -t teradici_oss_test
docker run -it --rm -e "FNO_PASSWORD=<your password>" -e "FNO_SERVER=<your server id>" -e "LISTEN_PORT=35666" -p 35666:35666  teradici_oss_test
```

should show you something similar to this in a browser (localhost:35666)
```
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 363.0
python_gc_objects_collected_total{generation="1"} 0.0
python_gc_objects_collected_total{generation="2"} 0.0
# HELP python_gc_objects_uncollectable_total Uncollectable object found during GC
# TYPE python_gc_objects_uncollectable_total counter
python_gc_objects_uncollectable_total{generation="0"} 0.0
python_gc_objects_uncollectable_total{generation="1"} 0.0
python_gc_objects_uncollectable_total{generation="2"} 0.0
# HELP python_gc_collections_total Number of times this generation was collected
# TYPE python_gc_collections_total counter
python_gc_collections_total{generation="0"} 66.0
python_gc_collections_total{generation="1"} 5.0
python_gc_collections_total{generation="2"} 0.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="6",patchlevel="8",version="3.6.8"} 1.0
# HELP process_virtual_memory_bytes Virtual memory size in bytes.
# TYPE process_virtual_memory_bytes gauge
process_virtual_memory_bytes 3.88173824e+08
# HELP process_resident_memory_bytes Resident memory size in bytes.
# TYPE process_resident_memory_bytes gauge
process_resident_memory_bytes 2.3498752e+07
# HELP process_start_time_seconds Start time of the process since unix epoch in seconds.
# TYPE process_start_time_seconds gauge
process_start_time_seconds 1.7135718952e+09
# HELP process_cpu_seconds_total Total user and system CPU time spent in seconds.
# TYPE process_cpu_seconds_total counter
process_cpu_seconds_total 246.95
# HELP process_open_fds Number of open file descriptors.
# TYPE process_open_fds gauge
process_open_fds 7.0
# HELP process_max_fds Maximum number of open file descriptors.
# TYPE process_max_fds gauge
process_max_fds 1024.0
# HELP pcoip pcoip license usage as reported by teradici
# TYPE pcoip gauge
pcoip{entitlement="used",feature="pcoip_licenses"} 4.0
pcoip{entitlement="entitled",feature="pcoip_licenses"} 25.0
# HELP pcoip_client Presence of PCoIP active session
# TYPE pcoip_client gauge
pcoip_client{hostname="nuke-01"} 1.0
pcoip_client{hostname="nuke-06"} 1.0
pcoip_client{hostname="nuke-04"} 1.0
pcoip_client{hostname="flame-03"} 1.0
```