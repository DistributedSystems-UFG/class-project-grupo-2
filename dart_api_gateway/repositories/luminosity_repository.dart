import '../generated/iot_service.pbgrpc.dart';
import '../services/grpc_service.dart';

class LuminosityRepository {
  static Future<LuminosityReply> sayLuminosity({
    required LuminosityRequest luminosityRequest,
  }) async {
    final stub = IoTServiceClient(GRPCService.instance.channel);

    final LuminosityReply luminosityReply =
        await stub.sayLuminosity(luminosityRequest);

    return luminosityReply;
  }
}
