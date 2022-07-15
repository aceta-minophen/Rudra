import 'package:companionapp/custom_icon_icons.dart';
import 'package:flutter/material.dart';

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
            IconButton(
                onPressed: (){},
                icon: Icon(
                  Icons.menu,
                  color: Colors.white,
                )
            ),
          ],
        ),

        bottomNavigationBar: Container(
          child: Container(
            margin: EdgeInsets.symmetric(vertical: 10),
            child: Row(
              children: [
                Expanded(
                  child: IconButton(
                      onPressed: (){},
                      icon: Icon(
                        CustomIcon.gym_dumbbell,
                        size: 40,
                        color: Colors.white,
                      ),
                  ),
                ),
                Expanded(
                  child: IconButton(
                    onPressed: (){},
                    icon: Icon(
                      CustomIcon.remote_control_line,
                      size: 30,
                      color: Colors.white,
                    ),
                  ),
                ),
                Expanded(
                  child: IconButton(
                    onPressed: (){},
                    icon: Icon(
                      CustomIcon.daily_schedule,
                      size: 40,
                      color: Colors.white,
                    ),
                  ),
                ),
                Expanded(
                  child: IconButton(
                    onPressed: (){},
                    icon: Icon(
                      CustomIcon.message_phone_chat,
                      size: 40,
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