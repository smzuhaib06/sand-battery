import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../models/sensor_data.dart';
import '../models/ai_data.dart';
import 'control_panel_screen.dart';
import 'history_screen.dart';

class DashboardScreen extends StatefulWidget {
  @override
  _DashboardScreenState createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  SensorData? sensorData;
  AIData? aiData;

  @override
  void initState() {
    super.initState();
    fetchData();
  }

  Future<void> fetchData() async {
    try {
      final sensor = await ApiService.getSensorData();
      final ai = await ApiService.getAIData();
      setState(() {
        sensorData = sensor;
        aiData = ai;
      });
    } catch (e) {
      print("Error: $e");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Dashboard')),
      body: RefreshIndicator(
        onRefresh: fetchData,
        child: sensorData == null || aiData == null
            ? Center(child: CircularProgressIndicator())
            : ListView(
                padding: EdgeInsets.all(16),
                children: [
                  Text('Voltage: ${sensorData!.voltage} V'),
                  Text('Current: ${sensorData!.current} mA'),
                  Text('Power: ${sensorData!.power} mW'),
                  Text('Battery: ${sensorData!.status}'),
                  Divider(),
                  Text('Estimated Backup: ${aiData!.backupTime}'),
                  Text('Recommendation: ${aiData!.recommendation}'),
                  Text('Mode: ${aiData!.mode}'),
                  Divider(),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: [
                      ElevatedButton(
                        child: Text('Control Panel'),
                        onPressed: () {
                          Navigator.push(context, MaterialPageRoute(builder: (_) => ControlPanelScreen()));
                        },
                      ),
                      ElevatedButton(
                        child: Text('History'),
                        onPressed: () {
                          Navigator.push(context, MaterialPageRoute(builder: (_) => HistoryScreen()));
                        },
                      ),
                    ],
                  )
                ],
              ),
      ),
    );
  }
}
