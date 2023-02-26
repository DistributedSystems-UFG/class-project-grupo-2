import '../generated/iot_service.pbgrpc.dart';
import '../services/grpc_service.dart';

class TemperatureRepository {
  static Future<TemperatureReply> sayTemperature({
    required TemperatureRequest temperatureRequest,
  }) async {
    final stub = IoTServiceClient(GRPCService.instance.channel);

    final TemperatureReply temperatureReply =
        await stub.sayTemperature(temperatureRequest);

    return temperatureReply;
  }
}
