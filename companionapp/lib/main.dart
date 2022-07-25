import 'package:companionapp/calendar.dart';
import 'package:companionapp/constants.dart';
import 'package:companionapp/custom_icon_icons.dart';
import 'package:flutter/material.dart';
import 'package:syncfusion_flutter_charts/charts.dart';

void main() {
  runApp(MaterialApp(
    home: Health(),
  ));
}

class Health extends StatelessWidget {
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
              style: TextStyle(fontSize: 15),
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
      body: SingleChildScrollView(
        child: Container(
          child: Column(
            children: [
              Container(
                margin: EdgeInsets.all(10),
                padding: EdgeInsets.all(8),
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
                                  Icons.do_not_step,
                                  color: Color(0xFFFE7763),
                                ),
                                SizedBox(
                                  width: 10,
                                ),
                                Text(
                                  'Steps',
                                  style: TextStyle(color: white, fontSize: 20),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                    Container(
                      height: 200,
                      child: Stack(
                        alignment: Alignment.center,
                        children: [
                          SfCircularChart(
                            series: <CircularSeries>[
                              // Renders doughnut chart
                              DoughnutSeries<ChartData, String>(
                                dataSource: chartData,
                                pointColorMapper: (ChartData data, _) =>
                                    data.color,
                                xValueMapper: (ChartData data, _) => data.x,
                                yValueMapper: (ChartData data, _) => data.y,
                                innerRadius: '80%',
                                // radius: '50%',
                              ),
                            ],
                          ),
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.center,
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Text(
                                '850',
                                style: TextStyle(color: white, fontSize: 25),
                                textAlign: TextAlign.center,
                              ),
                              Text(
                                'Steps',
                                style: TextStyle(color: white, fontSize: 20),
                                textAlign: TextAlign.center,
                              ),
                            ],
                          ),
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
                                  Icons.food_bank,
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
                    Text(
                      'LORemihia ihaihd iahsi dai dhiah da aidhai di ',
                      style: TextStyle(color: white),
                    )
                  ],
                ),
              ),
              Row(
                children: [
                  Column(
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
                            Container(
                              margin: EdgeInsets.all(10),
                              child: Column(
                                children: [
                                  Row(
                                    children: [
                                      Text(
                                        'Calories',
                                        style: TextStyle(
                                            color: white, fontSize: 20),
                                      ),
                                      Icon(
                                        Icons.water_drop,
                                        color: Color(0xFFFE7763),
                                      ),
                                    ],
                                  ),
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
                        child: Column(
                          children: [
                            Container(
                              margin: EdgeInsets.all(10),
                              child: Column(
                                children: [
                                  Row(
                                    children: [
                                      Text(
                                        'Sleep',
                                        style: TextStyle(
                                            color: white, fontSize: 20),
                                      ),
                                      Icon(
                                        Icons.nightlight,
                                        color: Color(0xFFFE7763),
                                      ),
                                    ],
                                  ),
                                ],
                              ),
                            ),
                            Row(
                              children: [
                                Text(
                                  '10 ',
                                  style: TextStyle(color: white, fontSize: 20),
                                ),
                                Text(
                                  ' hrs/day',
                                  style: TextStyle(
                                      color: Color(0xFFABABAB), fontSize: 15),
                                ),
                              ],
                            )
                          ],
                        ),
                      ),
                    ],
                  ),
                  Container(
                    margin: EdgeInsets.all(10),
                    padding: EdgeInsets.all(8),
                    decoration: BoxDecoration(
                      color: black,
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Column(
                      children: [
                        Row(
                          children: [
                            Text(
                              'Water',
                              style: TextStyle(color: white, fontSize: 20),
                            ),
                            Icon(
                              Icons.water_drop,
                              color: Color(0xFF50F3F7),
                            ),
                          ],
                        ),
                        Row(
                          children: [
                            Text(
                              '1.5 ',
                              style: TextStyle(color: white, fontSize: 20),
                            ),
                            Text(
                              ' lt',
                              style: TextStyle(
                                  color: Color(0xFFABABAB), fontSize: 15),
                            ),
                          ],
                        )
                      ],
                    ),
                  ),
                ],
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
                  onPressed: () {},
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
