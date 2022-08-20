import 'package:flutter/cupertino.dart';
import "package:googleapis_auth/auth_io.dart";
import 'package:googleapis/calendar/v3.dart';

const Color purple = Color(0xFFAC7CFF);
const Color black = Color(0xFF0F0F0F);
const Color grey = Color(0xFF171C23);
const Color white = Color(0xFFF7F7F7);

final accountCredentials = new ServiceAccountCredentials.fromJson({
  "private_key_id": "d0f3532ede830741007d3082aad9b0c0765de495",
  "private_key":
      "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC4fBGyFm/z4IAC\nwPAhINEZCH0ILBUWBFl+5+48zk9yZ2CMImRlaA1BJm6SXlOA1OqHmgHU8yiRXh/U\nuv7mmdPTbhoryeRb56y3n1EBBeVh/sQPy4vKVrUE+gaWqEtmcC8b0yMcGrJ0wAvI\nGHPdQoi2FnbugDn8fZA3pJEIwb6zMKypyOhl9DyQVUGm/VphFxK9MBNPZfx5Za7a\nrv458nElREFUaShLgsI9zTmM8fy+VpJ2o37G8mCg2SW1yn1FMC53/oHYLqm3leyz\naPh69/3ilWFxIixUIw5VT3bFYcw4IZvl9NSLRigs8H514oe4M8LNWyhx/yy48fdk\nwbTJYdc1AgMBAAECggEAAtvAHwLWjvA2ZvkXdj46NgUVXSTD/t9VzxRsTkO9Nj7b\nzT3CCHcN+PK7fiNduP5u+Gd3nF7F1iPo6328hDBzrzAZiNnePjUoKaTAAI3FHl3d\n4YegskgrW4/PmS38pjtjUcFVcDcuQBjXXwiY0LH1f7zBXmrvVn9QH5W6UGj9y/6m\n6Qcdl8A5fUwSC1/Z87mKinQ1jqNzXM7YO1fM8P92oDlnR4pkkBhPWn5qOrnNY/jE\nG5pQecFpCEcdlf6SIiO9ebVVApkIyCHxosfZhdKtViccq2izpLaOG+ERRODaEaRi\nYktbPLAXXyDjn79Yek1FiI1CJ6chXfiD8OJmoD9M0QKBgQDazzWV9RCByZHeG8+g\nns38tEfrjTRViQLCUVoms5phqSQmIS8JYwz3c+0mO75clbRrjg4hZbRMzNS747eH\nNeF2NEfHCdPq1XubP4tMQIza97b+RqIAkdRuvCMkGRCdnyOmcHC3gorKpCicLm3R\nI/i2jHFHhDVKYd/aE7buv4pt2wKBgQDX11PZkdqhCaW72aWvD6GLvErV7uM1o+ij\n9BLu8ydRZoIxuVw80nyO3y7W9I+nDwXS06jwBLX0krgqldDythekBMVQpjjCVays\nLHfjRVEg+r8ibCLE1FZEg1bR92pezmWtePeN0wWK93/g91QZIo5bmtNMdVDm9e4M\nil1x9VTELwKBgCIQnlwRQheipQX6OHHeJ12PR58hZaNnaDmOZsWdsow/w/P3uJXy\niMNBlgscw/8wA123SPXkGpTWUsxJoHn5Znd7ni0bl5V41PyPgQVHC2bPp/qgTnpe\nOb9fpOzqxg50Bx3TZYj8VtVDh1sBU3F68y6gYMZsi8tfv3T5GsLCqS9/AoGBAIkK\n6+9Jf0IeSP+TunIDf7OkUvOwYMzvDEgFMXxMIJu7dVCy+1CW6IUiSbAryYXtsOni\nf/IdW5Y1Df/j7a4dVbdLXCjP0Vv6X89V0K0ZluBUtMTbWdwVYczQg3B/Iied7ssM\n8kk3Qd6xNJ2XC+uFmFOrYxu5pStv3LxToe84MKD7AoGBANjo/dgivaR3I/iSzSKa\nuAM44LN9Vy56Y+ZlplSSStYtEQhgZ818CsNDsjw66OplXOlqJB6u5fj9Uu9uB/0I\nWs8Kz0qHhrvlkQYNfYI3IvAqghLF0u+rbk/mb0RtOx3s7jH1A9NbG0W7zAZqJ/Sf\n1yIv41EFmuntOjb0YxWaH0er\n-----END PRIVATE KEY-----\n",
  "client_email": "rudra-x@appspot.gserviceaccount.com",
  "client_id": "117255225010733105058",
  "type": "service_account"
});
var _scopes = [CalendarApi.CalendarScope];
// var calEvents, calendar;

// var numberOfEvents = 0;

class eventObj {
  var name, location, startDate, timezone;

  eventObj(
      {required this.name,
      required this.location,
      required this.startDate,
      required this.timezone});
}

List<eventObj> eventsList = [];

void getCalendarEvents() {
  clientViaServiceAccount(accountCredentials, _scopes).then((client) {
    eventsList.clear();
    var calendar = new CalendarApi(client);
    var calEvents = calendar.events
        .list("q8evv3ga6cr3aa9fttlm3oq8eg@group.calendar.google.com");

    calEvents.then((Events events) {
      events.items.forEach((Event event) {
        eventObj e = eventObj(
            name: event.summary,
            location: event.location,
            startDate: event.start.dateTime,
            timezone: event.start.timeZone);
        // print(e.name);
        eventsList.add(e);
      });
    });
    // numberOfEvents = eventsList.length;
    // print(eventsList);
  });
}
