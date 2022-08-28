import 'dart:async';

import 'package:companionapp/calendar.dart';
import 'package:companionapp/constants.dart';
import 'package:companionapp/custom_icon_icons.dart';
import 'package:companionapp/remote-control.dart';
import 'package:firebase_database/firebase_database.dart';
import 'package:flutter/material.dart';
import 'package:syncfusion_flutter_charts/charts.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

FirebaseDatabase databaseRef = FirebaseDatabase.instance;
// List<String> meals = [];
var response, extractedData, likedMeals, waterLog, previousMeals;

void readMealData() async {
  var url =
      "https://rudra-x-default-rtdb.firebaseio.com/" + "Meal Suggestion.json";
  try {
    response = await http.get(Uri.parse(url));
    extractedData = json.decode(response.body) as Map<String, dynamic>;
    likedMeals = Map<String, dynamic>.from(extractedData['Liked meals']);
    previousMeals = Map<String, dynamic>.from(extractedData['Previous mealds']);
  } catch (error) {
    print(error);
    throw error;
  }
}

void readWaterLogData() async {
  var url =
      "https://rudra-x-default-rtdb.firebaseio.com/" + "Computer Vision.json";
  try {
    response = await http.get(Uri.parse(url));
    extractedData = json.decode(response.body);
    waterLog = Map<String, dynamic>.from(
        extractedData['Action Recognition']['Drinking Water']);
  } catch (error) {
    print(error);
    throw error;
  }
}

class Health extends StatefulWidget {
  @override
  State<Health> createState() => _HealthState();
}

class _HealthState extends State<Health> {
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    final List<ChartData> chartData = [
      ChartData('Total Steps', 850, Color(0xFFFE7763)),
      ChartData('Remaining', 2000 - 850, grey),
    ];

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
            Text('30 April, 2022', style: TextStyle(fontSize: 10, color: white))
          ],
        ),
        actions: [
          PopupMenuButton<String>(
            color: black,
            onSelected: menuClick,
            icon: Icon(Icons.menu, color: white),
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
      body: SingleChildScrollView(
        child: Container(
          child: Column(
            children: [
              // Container(
              //   margin: EdgeInsets.all(10),
              //   padding: EdgeInsets.all(8),
              //   decoration: BoxDecoration(
              //     color: black,
              //     borderRadius: BorderRadius.circular(20),
              //   ),
              //   child: Column(
              //     children: [
              //       Container(
              //         margin: EdgeInsets.all(10),
              //         child: Row(
              //           children: [
              //             Expanded(
              //               child: Row(
              //                 children: [
              //                   Icon(
              //                     Icons.directions_walk_outlined,
              //                     color: Color(0xFFFE7763),
              //                   ),
              //                   SizedBox(
              //                     width: 10,
              //                   ),
              //                   Text(
              //                     'Steps',
              //                     style: TextStyle(color: white, fontSize: 20),
              //                   ),
              //                 ],
              //               ),
              //             ),
              //           ],
              //         ),
              //       ),
              //       Container(
              //         height: 200,
              //         child: Stack(
              //           alignment: Alignment.center,
              //           children: [
              //             SfCircularChart(
              //               series: <CircularSeries>[
              //                 DoughnutSeries<ChartData, String>(
              //                   dataSource: chartData,
              //                   pointColorMapper: (ChartData data, _) =>
              //                       data.color,
              //                   xValueMapper: (ChartData data, _) => data.x,
              //                   yValueMapper: (ChartData data, _) => data.y,
              //                   innerRadius: '80%',
              //                 ),
              //               ],
              //             ),
              //             Column(
              //               crossAxisAlignment: CrossAxisAlignment.center,
              //               mainAxisAlignment: MainAxisAlignment.center,
              //               children: [
              //                 Text(
              //                   '850',
              //                   style: TextStyle(color: white, fontSize: 25),
              //                   textAlign: TextAlign.center,
              //                 ),
              //                 Text(
              //                   'Steps',
              //                   style: TextStyle(color: white, fontSize: 20),
              //                   textAlign: TextAlign.center,
              //                 ),
              //               ],
              //             ),
              //           ],
              //         ),
              //       ),
              //     ],
              //   ),
              // ),
              Container(
                margin: EdgeInsets.all(10),
                padding: EdgeInsetsDirectional.all(8),
                decoration: BoxDecoration(
                  color: black,
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Column(
                  children: [
                    Container(
                      margin: EdgeInsets.all(10),
                      child: Row(
                        children: [
                          Expanded(
                            child: Row(
                              children: [
                                Icon(
                                  Icons.lunch_dining,
                                  color: Color(0xFFFE7763),
                                ),
                                SizedBox(
                                  width: 10,
                                ),
                                Text(
                                  'Suggested Meals',
                                  style: TextStyle(color: white, fontSize: 20),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                    Container(
                      padding: EdgeInsets.all(5),
                      child: Column(
                        children: List.generate(2, (index) {
                          String s =
                              likedMeals['meal' + (index + 1).toString()];
                          return Text(s.toUpperCase(),
                              style: TextStyle(
                                  color: white,
                                  fontSize: 15,
                                  fontWeight: FontWeight.bold));
                        }),
                      ),
                    )
                  ],
                ),
              ),
              IntrinsicHeight(
                child: Row(
                  children: [
                    Expanded(
                      child: Column(
                        children: [
                          Container(
                            margin: EdgeInsets.all(10),
                            padding: EdgeInsetsDirectional.all(8),
                            decoration: BoxDecoration(
                              color: black,
                              borderRadius: BorderRadius.circular(20),
                            ),
                            child: Column(
                              children: [
                                Padding(
                                  padding: const EdgeInsets.all(8.0),
                                  child: Column(
                                    children: [
                                      Row(
                                        children: [
                                          Text('Past Meal',
                                              style: TextStyle(
                                                  color: white, fontSize: 20)),
                                          new Spacer(),
                                          Icon(
                                            Icons.local_fire_department,
                                            color: Color(0xFFFE7763),
                                          ),
                                        ],
                                      ),
                                      Container(
                                        padding: EdgeInsets.all(5),
                                        child: Column(
                                          children: List.generate(2, (index) {
                                            String s = previousMeals['meal' +
                                                (index + 1).toString()];
                                            return Text(s.toUpperCase(),
                                                style: TextStyle(
                                                    color: white,
                                                    fontSize: 15,
                                                    fontWeight:
                                                        FontWeight.bold));
                                          }),
                                        ),
                                      )
                                    ],
                                  ),
                                ),
                              ],
                            ),
                          ),
                          Container(
                            margin: EdgeInsets.all(10),
                            padding: EdgeInsetsDirectional.all(8),
                            decoration: BoxDecoration(
                              color: black,
                              borderRadius: BorderRadius.circular(20),
                            ),
                            child: Padding(
                              padding: const EdgeInsets.all(8.0),
                              child: Column(
                                children: [
                                  Column(
                                    children: [
                                      Row(
                                        children: [
                                          Text(
                                            'Sleep',
                                            style: TextStyle(
                                                color: white, fontSize: 20),
                                          ),
                                          new Spacer(),
                                          Icon(
                                            Icons.bedtime,
                                            color: Color(0xFFFFFC700),
                                          ),
                                        ],
                                      ),
                                    ],
                                  ),
                                  SizedBox(
                                    height: 15,
                                  ),
                                  Row(
                                    children: [
                                      Text(
                                        '10 ',
                                        style: TextStyle(
                                            color: white, fontSize: 20),
                                      ),
                                      Text(
                                        ' hrs/day',
                                        style: TextStyle(
                                            color: Color(0xFFABABAB),
                                            fontSize: 15),
                                      ),
                                    ],
                                  )
                                ],
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                    Expanded(
                      child: Container(
                        margin: EdgeInsets.all(10),
                        padding: EdgeInsets.all(8),
                        decoration: BoxDecoration(
                          color: black,
                          borderRadius: BorderRadius.circular(20),
                        ),
                        child: Padding(
                          padding: const EdgeInsets.all(8.0),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.center,
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Row(
                                children: [
                                  Text(
                                    'Water',
                                    style:
                                        TextStyle(color: white, fontSize: 20),
                                  ),
                                  new Spacer(),
                                  Icon(
                                    Icons.local_drink,
                                    color: Color(0xFF50F3F7),
                                  ),
                                ],
                              ),
                              SizedBox(
                                height: 15,
                              ),
                              Image.asset(
                                'assets/images/Wave.png',
                              ),
                              SizedBox(
                                height: 15,
                              ),
                              Row(
                                children: [
                                  Text(
                                    waterLog['Waterlog'].toString() + ' ',
                                    style:
                                        TextStyle(color: white, fontSize: 20),
                                  ),
                                  Text(
                                    ' glass',
                                    style: TextStyle(
                                        color: Color(0xFFABABAB), fontSize: 15),
                                  ),
                                ],
                              )
                            ],
                          ),
                        ),
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
                        builder: (BuildContext context) => RemoteControl(),
                      ),
                    );
                  },
                  icon: Icon(
                    CustomIcon.remote_control_line,
                    size: 25,
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

class ChartData {
  ChartData(this.x, this.y, this.color);
  final String x;
  final double y;
  final Color color;
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
}
