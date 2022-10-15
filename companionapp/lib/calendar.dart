import 'package:companionapp/constants.dart';
import 'package:companionapp/custom_icon_icons.dart';
import 'package:companionapp/health.dart';
import 'package:companionapp/remote-control.dart';
import 'package:flutter/material.dart';
import 'package:flutter_calendar_carousel/classes/event.dart';
import 'package:flutter_calendar_carousel/flutter_calendar_carousel.dart'
    show CalendarCarousel;

class Calendar extends StatefulWidget {
  const Calendar({Key? key}) : super(key: key);
flutter-frontend

  @override
  _CalendarState createState() => _CalendarState();
}

class _CalendarState extends State<Calendar> {
  var _currentDate, _markedDateMap;

  Widget buildReminderWidget(var index, var currentDate) {
    eventObj event = eventsList[index];
    var eventDate = event.startDate;
    if (currentDate.year == eventDate.year &&
        currentDate.month == eventDate.month &&
        currentDate.day == eventDate.day) {
      return Row(
        children: [
          Container(
            padding: EdgeInsets.all(8),
            child: Text(
              eventDate.hour.toString().padLeft(2, '0') +
                  ':' +
                  eventDate.minute.toString().padLeft(2, '0'),
              style: TextStyle(
                color: Colors.grey,
              ),
            ),
          ),
          Expanded(
            child: Container(
              padding: EdgeInsets.all(8),
              margin: EdgeInsets.all(8),
              child: Text(
                event.name,
                style: TextStyle(fontSize: 15),
              ),
              decoration: BoxDecoration(
                color: Colors.red,
                borderRadius: BorderRadius.circular(5),
              ),
            ),
          )
        ],
      );
    }

    return Container();
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
        child: Column(
          children: [
            CalendarCarousel<Event>(
              onDayPressed: (DateTime date, List<Event> events) {
                this.setState(() => _currentDate = date);
              },
              weekdayTextStyle: TextStyle(
                color: white,
              ),
              weekendTextStyle: TextStyle(
                color: Color(0xFFFF0000),
              ),
              daysTextStyle: TextStyle(color: white),
              thisMonthDayBorderColor: grey,
              weekFormat: false,
              markedDatesMap: _markedDateMap,
              height: 370.0,
              selectedDateTime: _currentDate,
              daysHaveCircularBorder: false,
            ),
            // SizedBox(
            //   height: 15,
            // ),
            Container(
              child: Column(
                children: [
                  Text(
                    'Daily Tasks',
                    style: TextStyle(
                      color: white,
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  SizedBox(
                    height: 15,
                  ),
                  Container(
                    child: Column(
                      children: List.generate(eventsList.length, (index) {
                        if (_currentDate == null) {
                          _currentDate = DateTime.now();
                        }
                        return buildReminderWidget(index, _currentDate);
                      }),
                    ),
                  ),
                ],
              ),
            )
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
                    color: purple,
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
