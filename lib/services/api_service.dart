import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/sensor_data.dart';
import '../models/ai_data.dart';

class ApiService {
  static Future<SensorData> getSensorData() async {
    final response = await http.get(Uri.parse('http://127.0.0.1:8000/data'));
    if (response.statusCode == 200) {
      final jsonMap = json.decode(response.body);
      return SensorData.fromJson(jsonMap);
    } else {
      throw Exception('Failed to load sensor data');
    }
  }

  static Future<AIData> getAIData() async {
    final response = await http.get(Uri.parse('http://127.0.0.1:8000/ai_status'));
    if (response.statusCode == 200) {
      final jsonMap = json.decode(response.body);
      return AIData.fromJson(jsonMap);
    } else {
      throw Exception('Failed to load AI data');
    }
  }

  
  static Future<bool> controlSwitch(String gpio, bool value) async {
    final response = await http.post(
      Uri.parse('http://127.0.0.1:8000/control'),
      body: {
        'gpio': gpio,
        'value': value ? '1' : '0',
      },
    );
    return response.statusCode == 200;
  }
}
