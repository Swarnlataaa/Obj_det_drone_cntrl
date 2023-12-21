import 'dart:io';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_joystick/flutter_joystick.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Drone Controller',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  Socket? socket;

  double throttle = 0.0;
  double yaw = 0.0;
  double pitch = 0.0;
  double roll = 0.0;

  @override
  void initState() {
    super.initState();
    connectToServer();
  }

  void connectToServer() async {
    try {
      socket = await Socket.connect('192.168.137.33', 9999);
      print('Connected to server');
      listenToServer();
    } catch (e) {
      print('Error connecting to server: $e');
    }
  }

  void listenToServer() {
    socket!.listen(
      (List<int> event) {
        String data = utf8.decode(event);
        print('Received from server: $data');

        // Add your logic to handle the received data here
      },
      onError: (error) {
        print('Error with socket: $error');
      },
      onDone: () {
        print('Connection to server closed');
      },
      cancelOnError: false,
    );
  }

  void sendControlDataToServer() {
    if (socket != null && socket!.writeable) {
      String data = 'throttle:$throttle,yaw:$yaw,pitch:$pitch,roll:$roll';
      socket!.write(data);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Drone Controller'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            JoystickView(
              onDirectionChanged: (double degrees, double distance) {
                // Convert degrees to radians and calculate yaw and throttle
                double radians = degrees * (3.14159265359 / 180.0);
                yaw = radians;
                throttle = distance;
                sendControlDataToServer();
              },
            ),
            SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                JoystickButton(
                  size: 50,
                  color: Colors.green,
                  onPressed: () {
                    // Increase pitch for forward movement
                    pitch = -1.0;
                    sendControlDataToServer();
                  },
                ),
                JoystickButton(
                  size: 50,
                  color: Colors.red,
                  onPressed: () {
                    // Increase pitch for backward movement
                    pitch = 1.0;
                    sendControlDataToServer();
                  },
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  @override
  void dispose() {
    socket?.close();
    super.dispose();
  }
}
