# Lidar

## Use this to make the binary to read the lidar

```
g++ -pthread -lrt rplidar_driver.cpp thread.cpp net_serial.cpp timer.cpp readlidar.cpp -o readlidar
```
