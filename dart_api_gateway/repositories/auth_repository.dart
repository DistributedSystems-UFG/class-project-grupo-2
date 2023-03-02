import '../generated/iot_service.pbgrpc.dart';
import '../services/grpc_service.dart';

class AuthRepository {
  static Future<Token> getAccessToken({
    required Credentials credentials,
  }) async {
    final stub = IoTServiceClient(GRPCService.instance.channel);

    final Token token = await stub.getAccessToken(credentials);

    return token;
  }

  static Future<AddNewUserReply> addNewUser({
    required Credentials credentials,
  }) async {
    final stub = IoTServiceClient(GRPCService.instance.channel);

    final AddNewUserReply addNewUserReply = await stub.addNewUser(credentials);

    return addNewUserReply;
  }
}
