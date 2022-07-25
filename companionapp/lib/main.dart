import 'dart:convert';
import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:companionapp/websockets.dart';
//import 'package:videostreaming_tut/src/styles/styles.dart';

void main() {
  runApp(VideoStream());
}

class VideoStream extends StatefulWidget {
  const VideoStream({Key? key}) : super(key: key);

  @override
  State<VideoStream> createState() => _VideoStreamState();
}

class _VideoStreamState extends State<VideoStream> {
  final WebSocket _socket = WebSocket("ws://192.168.29.47:8081");
  bool _isConnected = false;
  void connect(BuildContext context) async {
    _socket.connect();
    setState(() {
      _isConnected = true;
    });
  }

  void disconnect() {
    _socket.disconnect();
    setState(() {
      _isConnected = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
    home: Scaffold(
    appBar: AppBar(
    title: const Text("Live Video"),
    ),
    body: Padding(
    padding: const EdgeInsets.all(20.0),
    child: Center(
    child: Column(
    children: [
    Row(
    mainAxisAlignment: MainAxisAlignment.spaceBetween,
    children: [
    ElevatedButton(
    onPressed: () => connect(context),
    //style: buttonStyle,
    child: const Text("Connect"),
    ),
    ElevatedButton(
    onPressed: disconnect,
    //style: buttonStyle,
    child: const Text("Disconnect"),
    ),
    ],
    ),
    const SizedBox(
    height: 50.0,
    ),
    _isConnected
    ? StreamBuilder(
    stream: _socket.stream,
    builder: (context, snapshot) {
    if (!snapshot.hasData) {
    return const CircularProgressIndicator();
    }

    if (snapshot.connectionState == ConnectionState.done) {
    return const Center(
    child: Text("Connection Closed !"),
    );
    }
    //? Working for single frames
    return Image.memory(
    Uint8List.fromList(
    base64Decode(
    (snapshot.data.toString()),
    ),
    ),
    gaplessPlayback: true,
    excludeFromSemantics: true,
    );
    },
    )
        : const Text("Initiate Connection")
    ],
    ),
    ),
    ),
    ),
    );
  }
}


/*import 'package:companionapp/custom_icon_icons.dart';
import 'package:remote_ip_camera/remote_ip_camera.dart';
import 'package:remote_ui/remote_ui.dart';
import 'package:flutter/material.dart';
//import 'package:flutter_remote_ui/flutter_remote_ui.dart';

void main() {
  runApp(Health());
}

class Health extends StatelessWidget {

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        backgroundColor: Color(0xFF171C23),
        appBar: AppBar(
          backgroundColor: Colors.black,
          leading: Container(
            margin: EdgeInsets.symmetric(horizontal: 10, vertical: 0),
            child: Image.network('https://static.remove.bg/remove-bg-web/5c20d2ecc9ddb1b6c85540a333ec65e2c616dbbd/assets/start-1abfb4fe2980eabfbbaaa4365a0692539f7cd2725f324f904565a9a744f8e214.jpg',),
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(20),
            ),
          ),
          title: Column(
            children: [
              Text('Good Morning, Emilie!', style: TextStyle(fontSize: 15),),
              Text('30 April, 2022', style: TextStyle(fontSize: 10))
            ],
          ),
          actions: [
            PopupMenuButton<String>(
              color: Colors.black,
              onSelected: menuClick,
              icon: Icon(
                Icons.menu,
              ),
              itemBuilder: (BuildContext context) {
                return {'Notification', 'Privacy', 'Security', 'Account'}.map((String choice) {
                  return PopupMenuItem<String>(
                    value: choice,
                    child: Text(choice, style: TextStyle(color: Colors.white),),
                  );
                }).toList();
              },
            ),
          ],
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: <Widget>[
              Expanded(
                child: RemoteManagerWidget(
                  parsers: [RemoteIpCameraFactory()],
                  onChanges: (key, value, {associatedData}) =>
                      debugPrint('$key change to $value'),
                  child: RemoteWidget(
                    definition: {
                      'type': 'column',
                      'children': [
                        {
                          'type': 'camera',
                          'stream': 'http://192.168.29.47:8081',
                        }
                      ],
                    }, data: {},
                  ),
                ),
              ),
              Text(
                'You have pushed the button this many times:',
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),
        bottomNavigationBar: Container(
          child: Container(
            margin: EdgeInsets.symmetric(vertical: 15),
            child: Row(
              children: [
                Expanded(
                  child: IconButton(
                      onPressed: (){},
                      icon: Icon(
                        CustomIcon.gym_dumbbell,
                        size: 35,
                        color: Colors.white,
                      ),
                  ),
                ),
                Expanded(
                  child: IconButton(
                    onPressed: (){},
                    icon: Icon(
                      CustomIcon.remote_control_line,
                      size: 25,
                      color: Colors.white,
                    ),
                  ),
                ),
                Expanded(
                  child: IconButton(
                    onPressed: (){},
                    icon: Icon(
                      CustomIcon.daily_schedule,
                      size: 35,
                      color: Colors.white,
                    ),
                  ),
                ),
                Expanded(
                  child: IconButton(
                    onPressed: (){},
                    icon: Icon(
                      CustomIcon.message_phone_chat,
                      size: 35,
                      color: Colors.white,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      )
    );
  }
}

void menuClick(String value) {
  switch (value) {
    case 'Notification':
      break;
    case 'Privacy':
      break;
    case 'Security':
      break;
    case 'Account':
      break;
  }
}*/