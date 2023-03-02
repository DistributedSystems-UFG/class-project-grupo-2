import '../generated/iot_service.pbgrpc.dart';
import '../services/grpc_service.dart';

class RouteRepository {
  static Future<SetRouteReply> setRoute({
    required SetRouteRequest setRouteRequest,
  }) async {
    final stub = IoTServiceClient(GRPCService.instance.channel);

    final SetRouteReply setRouteReply = await stub.setRoute(setRouteRequest);

    return setRouteReply;
  }

  static Future<RouteReply> getLastRoute({
    required GetLastRouteRequest getLastRouteRequest,
  }) async {
    final stub = IoTServiceClient(GRPCService.instance.channel);

    final RouteReply routeReply = await stub.getLastRoute(getLastRouteRequest);

    return routeReply;
  }
}
