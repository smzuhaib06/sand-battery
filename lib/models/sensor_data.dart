class SensorData {
  final double voltage;
  final int current;
  final int power;
  final String status;

  SensorData({
    required this.voltage,
    required this.current,
    required this.power,
    required this.status,
  });

  factory SensorData.fromJson(Map<String, dynamic> json) {
    return SensorData(
      voltage: json['voltage'].toDouble(),
      current: json['current'],
      power: json['power'].toInt(),
      status: json['status'],
    );
  }
}
