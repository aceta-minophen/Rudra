import 'package:companionapp/constants.dart';
import 'package:companionapp/custom_icon_icons.dart';
import 'package:companionapp/main.dart';
import 'package:flutter/material.dart';
import 'package:flutter_calendar_carousel/classes/event.dart';
import 'package:flutter_calendar_carousel/flutter_calendar_carousel.dart'
    show CalendarCarousel;

class Calendar extends StatefulWidget {
  const Calendar({Key? key}) : super(key: key);

  @override
  _CalendarState createState() => _CalendarState();
}

class _CalendarState extends State<Calendar> {
  var _currentDate, _markedDateMap;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: grey,
      appBar: AppBar(
        backgroundColor: black,
        leading: IconButton(
          onPressed: () {},
          icon: Icon(
            Icons.arrow_back,
            color: white,
          ),
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
        child: Column(
          children: [
            CalendarCarousel<Event>(
              onDayPressed: (DateTime date, List<Event> events) {
                this.setState(() => _currentDate = date);
              },
              weekdayTextStyle: TextStyle(
                color: Colors.white,
              ),
              weekendTextStyle: TextStyle(
                color: Colors.red,
              ),
              daysTextStyle: TextStyle(color: white),
              thisMonthDayBorderColor: grey,
              weekFormat: false,
              markedDatesMap: _markedDateMap,
              height: 420.0,
              selectedDateTime: _currentDate,
              daysHaveCircularBorder: false,
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
