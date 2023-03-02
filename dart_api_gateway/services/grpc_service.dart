import 'package:grpc/grpc.dart';

class GRPCService {
  GRPCService();

  ClientChannel? _channel;
  ClientChannel get channel => _channel ?? _openChannel();

  static GRPCService? _instance;
  static GRPCService get instance => _instance ??= GRPCService();

  ClientChannel _openChannel() {
    final channel = ClientChannel(
      '34.170.205.17',
      port: 50051,
      options: const ChannelOptions(
        credentials: ChannelCredentials.insecure(),
      ),
    );
    _channel = channel;
    return channel;
  }
}
