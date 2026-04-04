import 'package:flutter/material.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'ShareBot AI - Indian Constitution',
      theme: ThemeData(
        brightness: Brightness.dark,
        primaryColor: Color(0xFF10A37F),
        scaffoldBackgroundColor: Color(0xFF191919),
        appBarTheme: AppBarTheme(
          backgroundColor: Color(0xFF212121),
          elevation: 1,
        ),
      ),
      home: HomeScreen(),
    );
  }
}
