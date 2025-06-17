class AIData {
  final String backupTime;
  final String recommendation;
  final String mode;

  AIData({
    required this.backupTime,
    required this.recommendation,
    required this.mode,
  });

  factory AIData.fromJson(Map<String, dynamic> json) {
    return AIData(
      backupTime: json['backup_time'],
      recommendation: json['recommendation'],
      mode: json['mode'],
    );
  }
}
