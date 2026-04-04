import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  // Use 10.0.2.2 for Android emulator, 127.0.0.1 for web/desktop, localhost for iOS
  static const String baseUrl = "http://127.0.0.1:8000";

  static Future<String> sendMessage(String query) async {
    try {
      print("Sending request to: $baseUrl/chat");
      final response = await http
          .post(
            Uri.parse("$baseUrl/chat"),
            headers: {"Content-Type": "application/json"},
            body: jsonEncode({"query": query}),
          )
          .timeout(Duration(seconds: 10));

      print("Response status: ${response.statusCode}");
      print("Response body: ${response.body}");

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data["answer"] ?? "No answer received";
      } else {
        return "Server Error ${response.statusCode}: ${response.body}";
      }
    } catch (e) {
      print("Exception: $e");
      return "Connection Error: $e";
    }
  }
}
