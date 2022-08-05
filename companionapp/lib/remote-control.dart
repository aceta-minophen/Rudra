import 'package:flutter/material.dart';
import 'package:companionapp/websockets.dart';
import 'dart:convert';
import 'dart:typed_data';

class RemoteControl extends StatefulWidget {
  const RemoteControl({Key? key}) : super(key: key);

  @override
  _RemoteControlState createState() => _RemoteControlState();
  /*Widget build(BuildContext context) {
    return Container();
  }*/
}

class _RemoteControlState extends State<RemoteControl>{
  final WebSocket _socket = WebSocket("ws://192.168.29.47:5000");
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

                    if (snapshot.connectionState ==
                        ConnectionState.done) {
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
                    : const Text("Initiate Connection to rpi")
              ],
            ),
          ),
        ),
      ),
    );
  }
}