import 'package:flutter/material.dart';
import '../services/api_service.dart';

class ControlPanelScreen extends StatefulWidget {
  @override
  _ControlPanelScreenState createState() => _ControlPanelScreenState();
}

class _ControlPanelScreenState extends State<ControlPanelScreen> {
  Map<String, bool> deviceStates = {
    'grid': false,
    'sand': false,
    'load': false,
    'heater': false,
  };

  void control(BuildContext context, String device, bool newState) async {
    final success = await ApiService.controlSwitch(device, newState);

    if (success) {
      setState(() {
        deviceStates[device] = newState;
      });
    }

    ScaffoldMessenger.of(context).showSnackBar(SnackBar(
      content: Text(success
          ? "$device turned ${newState ? 'ON' : 'OFF'}"
          : "Failed to control $device"),
    ));
  }

  Widget buildToggleButton(String device, String label) {
    final isOn = deviceStates[device] ?? false;
    return ElevatedButton(
      onPressed: () => control(context, device, !isOn),
      style: ElevatedButton.styleFrom(
        backgroundColor: isOn ? Colors.green : Colors.red,
      ),
      child: Text("$label: ${isOn ? 'ON' : 'OFF'}"),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Control Panel')),
      body: ListView(
        padding: EdgeInsets.all(16),
        children: [
          buildToggleButton('grid', 'Switch to Grid'),
          buildToggleButton('sand', 'Switch to Sand Battery'),
          buildToggleButton('load', 'Load'),
          buildToggleButton('heater', 'Heater'),
        ],
      ),
    );
  }
}
