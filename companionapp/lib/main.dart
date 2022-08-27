import 'dart:async';
import 'package:companionapp/constants.dart';
import 'package:companionapp/firebase_options.dart';
import 'package:companionapp/health.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/material.dart';
import 'package:splashscreen/splashscreen.dart';
// import 'package:companionapp/constants.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  readMealData();
  readWaterLogData();
  getCalendarEvents();
  runApp(MaterialApp(
    home: MyApp(),
  ));
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Rudra',
      theme: ThemeData(
        primarySwatch: Colors.grey,
      ),
      home: Splash2(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class Splash2 extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return SplashScreen(
      backgroundColor: Color(0xFF000000),
      seconds: 6,
      navigateAfterSeconds: new Health(),
      title: new Text(
        'RUDRA',
        textScaleFactor: 2,
        style: TextStyle(color: white),
      ),
      image: new Image.asset('assets/images/LOGO.png'),
      loadingText: Text(
        "Loading",
        style: TextStyle(color: white),
      ),
      photoSize: 200.0,
      loaderColor: grey,
    );
  }
}
