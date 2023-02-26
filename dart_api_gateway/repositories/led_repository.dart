import '../generated/iot_service.pbgrpc.dart';
import '../services/grpc_service.dart';

class LedRepository {
  static Future<LedReply> blinkLed({
    required LedRequest ledRequest,
  }) async {
    final stub = IoTServiceClient(GRPCService.instance.channel);

    final LedReply ledReply = await stub.blinkLed(ledRequest);

    return ledReply;
  }
}
