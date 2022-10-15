import 'package:companionapp/health.dart';
import 'package:flutter/material.dart';
import 'package:companionapp/websockets.dart';
import 'dart:ui';
import 'dart:convert';
import 'dart:typed_data';
import 'package:companionapp/calendar.dart';
import 'package:companionapp/constants.dart';
import 'package:companionapp/custom_icon_icons.dart';
import 'package:flutter/material.dart';
import 'package:flutter_joystick/flutter_joystick.dart';
import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart';
import 'package:firebase_database/firebase_database.dart';

class RemoteControl extends StatefulWidget {
  const RemoteControl({Key? key}) : super(key: key);

  @override
  _RemoteControlState createState() => _RemoteControlState();
/*Widget build(BuildContext context) {
    return Container();
  }*/
}

const ballSize = 30.0;
const step = 30.0;

class _RemoteControlState extends State<RemoteControl> {
  final WebSocket _socket = WebSocket("ws://10.5.32.13:8000");
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

  double _x = 300;
  double _y = 300;
  double p = 300;
  double q = 300;
  JoystickMode _joystickMode = JoystickMode.all;

  double a = 0, b = 0, c = 0, d = 0;

  /*void initFirebase(){
    setState(() async {
      await Firebase.initializeApp(
        options: DefaultFirebaseOptions.currentPlatform,
      );
    });
  }*/

  late double x_val, y_val;

  Future<void> writeData() async {
    await Firebase.initializeApp(
      options: DefaultFirebaseOptions.currentPlatform,
    );

    DatabaseReference ref =
        FirebaseDatabase.instance.reference().child('joystick');

    await ref.set({"x": x_val, "y": y_val});
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: grey,
      appBar: AppBar(
        backgroundColor: black,
        leading: Container(
          margin: EdgeInsets.symmetric(horizontal: 10, vertical: 0),
          child: Image.network(
            'https://static.remove.bg/remove-bg-web/5c20d2ecc9ddb1b6c85540a333ec65e2c616dbbd/assets/start-1abfb4fe2980eabfbbaaa4365a0692539f7cd2725f324f904565a9a744f8e214.jpg',
          ),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(20),
          ),
        ),
        title: Column(
          children: [
            Text(
              'Good Morning, Emilie!',
              style: TextStyle(fontSize: 15, color: white),
            ),
            Text('30 April, 2022', style: TextStyle(fontSize: 10))
          ],
        ),
        actions: [
          PopupMenuButton<String>(
            color: black,
            onSelected: menuClick,
            icon: Icon(
              Icons.menu,
            ),
            itemBuilder: (BuildContext context) {
              return {'Notification', 'Privacy', 'Security', 'Account'}
                  .map((String choice) {
                return PopupMenuItem<String>(
                  value: choice,
                  child: Text(
                    choice,
                    style: TextStyle(color: white),
                  ),
                );
              }).toList();
            },
          ),
        ],
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
                height: 20.0,
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
                  : const Text("Initiate Connection to rpi"),

              /*SizedBox(
                width: double.infinity,
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    ElevatedButton(
                      onPressed: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                              builder: (context) => const JoystickExample()),
                        );
                      },
                      child: const Text('Joystick'),
                    ),
                  ],
                ),
              ),*/
              SafeArea(
                child: Stack(
                  children: [
                    Container(
                      color: Colors.grey,
                      child: Text('x:$c, y:$d'),
                    ),
                    Ball(p, q),
                    Align(
                      alignment: const Alignment(0, 0),
                      child: Joystick(
                        mode: JoystickMode.all,
                        listener: (details) {
                          setState(() {
                            p = p + step * details.x;
                            q = q + step * details.y;
                            _x = 300 + step * details.x;
                            _y = 300 + step * details.y;
                            Future.delayed(const Duration(milliseconds: 300),
                                () {
                              a = 300 + step * details.x;
                              b = 300 + step * details.y;
                              if (a != _x && b != _y) {
                                c = (a - 300) / step;
                                d = (b - 300) / step;
                                if (c != 0 && d != 0) {
                                  print('c:$c, d:$d');
                                  x_val = c;
                                  y_val = d;
                                  writeData();
                                }
                              } else if (a == _x && b == _y) {
                                c = 0;
                                d = 0;
                                _x = 300;
                                _y = 300;
                                print('c:$c, d:$d');
                                x_val = c;
                                y_val = d;
                                writeData();
                              }
                            });
                          });
                        },
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
      bottomNavigationBar: Container(
        child: Container(
          margin: EdgeInsets.symmetric(vertical: 15),
          child: Row(
            children: [
              Expanded(
                child: IconButton(
                  onPressed: () {
                    Navigator.pushReplacement(
                      context,
                      MaterialPageRoute<void>(
                        builder: (BuildContext context) => Health(),
                      ),
                    );
                  },
                  icon: Icon(
                    CustomIcon.gym_dumbbell,
                    size: 35,
                    color: white,
                  ),
                ),
              ),
              Expanded(
                child: IconButton(
                  onPressed: () {
                    Navigator.pushReplacement(
                      context,
                      MaterialPageRoute<void>(
                        builder: (BuildContext context) => RemoteControl(),
                      ),
                    );
                  },
                  icon: Icon(
                    CustomIcon.remote_control_line,
                    size: 25,
                    color: purple,
                  ),
                ),
              ),
              Expanded(
                child: IconButton(
                  onPressed: () {
                    Navigator.pushReplacement(
                      context,
                      MaterialPageRoute<void>(
                        builder: (BuildContext context) => Calendar(),
                      ),
                    );
                  },
                  icon: Icon(
                    CustomIcon.daily_schedule,
                    size: 35,
                    color: white,
                  ),
                ),
              ),
              // Expanded(
              //   child: IconButton(
              //     onPressed: (){},
              //     icon: Icon(
              //       CustomIcon.message_phone_chat,
              //       size: 35,
              //       color: white,
              //     ),
              //   ),
              // ),
            ],
          ),
        ),
      ),
    );
  }
}

class JoystickExample extends StatefulWidget {
  const JoystickExample({Key? key}) : super(key: key);

  @override
  _JoystickExampleState createState() => _JoystickExampleState();
}

class _JoystickExampleState extends State<JoystickExample> {
  double _x = 300;
  double _y = 500;
  double p = 300;
  double q = 300;
  JoystickMode _joystickMode = JoystickMode.all;

  double a = 0, b = 0, c = 0, d = 0;

  /*void initFirebase(){
    setState(() async {
      await Firebase.initializeApp(
        options: DefaultFirebaseOptions.currentPlatform,
      );
    });
  }*/

  late double x_val, y_val;

  Future<void> writeData() async {
    await Firebase.initializeApp(
      options: DefaultFirebaseOptions.currentPlatform,
    );

    DatabaseReference ref =
        FirebaseDatabase.instance.reference().child('joystick');

    await ref.set({"x": x_val, "y": y_val});
  }

  /*final _form = GlobalKey<FormState>();
  late double title;
  void writeData() async {
    _form.currentState?.save();
    // Please replace the Database URL
    // which we will get in “Add Realtime
    // Database” step with DatabaseURL
    var url = "https://rudra-x-default-rtdb.firebaseio.com/"+"data.json";
    // (Do not remove “data.json”,keep it as it is)
    try {
      final response = await http.post(
        Uri.parse(url),
        body: json.encode({"title": title}),
      );
    } catch (error) {
      throw error;
    }
  }*/

  //FirebaseDatabase database = FirebaseDatabase.instance;
  @override
  void didChangeDependencies() {
    _x = MediaQuery.of(context).size.width / 2 - ballSize / 2;
    super.didChangeDependencies();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        title: const Text('Joystick'),
        actions: [
          JoystickModeDropdown(
            mode: _joystickMode,
            onChanged: (JoystickMode value) {
              setState(() {
                _joystickMode = value;
              });
            },
          ),
        ],
      ),
      body: SafeArea(
        child: Stack(
          children: [
            Container(
              color: Colors.grey,
              child: Text('x:$c, y:$d'),
            ),
            Ball(p, q),
            Align(
              alignment: const Alignment(0, 1),
              child: Joystick(
                mode: JoystickMode.all,
                listener: (details) {
                  setState(() {
                    p = p + step * details.x;
                    q = q + step * details.y;
                    _x = 300 + step * details.x;
                    _y = 300 + step * details.y;
                    Future.delayed(const Duration(milliseconds: 300), () {
                      a = 300 + step * details.x;
                      b = 300 + step * details.y;
                      if (a != _x && b != _y) {
                        c = (a - 300) / step;
                        d = (b - 300) / step;
                        if (c != 0 && d != 0) {
                          print('c:$c, d:$d');
                          x_val = c;
                          y_val = d;
                          writeData();
                        }
                      } else if (a == _x && b == _y) {
                        c = 0;
                        d = 0;
                        _x = 300;
                        _y = 300;
                        print('c:$c, d:$d');
                        x_val = c;
                        y_val = d;
                        writeData();
                      }
                    });
                  });
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
class JoystickModeDropdown extends StatelessWidget {
  final JoystickMode mode;
  final ValueChanged<JoystickMode> onChanged;

  const JoystickModeDropdown(
      {Key? key, required this.mode, required this.onChanged})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 150,
      child: Padding(
        padding: const EdgeInsets.only(left: 16.0),
        child: FittedBox(
          child: DropdownButton(
            value: mode,
            onChanged: (v) {
              onChanged(v as JoystickMode);
            },
            items: const [
              DropdownMenuItem(
                  child: Text('All Directions'), value: JoystickMode.all),
              DropdownMenuItem(
                  child: Text('Vertical And Horizontal'),
                  value: JoystickMode.horizontalAndVertical),
              DropdownMenuItem(
                  child: Text('Horizontal'), value: JoystickMode.horizontal),
              DropdownMenuItem(
                  child: Text('Vertical'), value: JoystickMode.vertical),
            ],
          ),
        ),
      ),
    );
  }
}

class Ball extends StatelessWidget {
  final double x;
  final double y;

  const Ball(this.x, this.y, {Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Positioned(
      left: x,
      top: y,
      child: Container(
        width: ballSize,
        height: ballSize,
        decoration: const BoxDecoration(
          shape: BoxShape.circle,
          color: Colors.white60,
          boxShadow: [
            BoxShadow(
              color: Colors.black12,
              spreadRadius: 2,
              blurRadius: 3,
              offset: Offset(0, 3),
            )
          ],
        ),
      ),
    );
  }
}

/*BUILD FAILED in 3m 20s

┌─ Flutter Fix ─────────────────────────────────────────────────────────────────────────────────┐
│ The plugin firebase_database requires a higher Android SDK version.                           │
│ Fix this issue by adding the following to the file C:\Computer\Git                            │
│ Repositories\Rudra\companionapp\android\app\build.gradle:                                     │
│ android {                                                                                     │
│   defaultConfig {                                                                             │
│     minSdkVersion 19                                                                          │
│   }                                                                                           │
│ }                                                                                             │
│                                                                                               │
│ Note that your app won't be available to users running Android SDKs below 19.                 │
│ Alternatively, try to find a version of this plugin that supports these lower versions of the │
│ Android SDK.                                                                                  │
│ For more information, see:                                                                    │
│ https://docs.flutter.dev/deployment/android#reviewing-the-build-configuration                 │
└───────────────────────────────────────────────────────────────────────────────────────────────┘
Exception: Gradle task assembleDebug failed with exit code 1
*/