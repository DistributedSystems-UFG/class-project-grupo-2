import '../generated/iot_service.pbgrpc.dart';
import '../services/grpc_service.dart';

class RegionsRepository {
  static Future<AddRegionReply> addRegion({
    required AddRegionRequest addRegionRequest,
  }) async {
    final stub = IoTServiceClient(GRPCService.instance.channel);

    final AddRegionReply addRegionReply =
        await stub.addRegion(addRegionRequest);

    return addRegionReply;
  }

  static Future<RegionsReply> getRegions({
    required GetRegionsRequest getRegionsRequest,
  }) async {
    final stub = IoTServiceClient(GRPCService.instance.channel);

    final RegionsReply regionsReply = await stub.getRegions(getRegionsRequest);

    return regionsReply;
  }

  static Future<RemoveRegionReply> removeRegions({
    required RemoveRegionRequest removeRegionRequest,
  }) async {
    final stub = IoTServiceClient(GRPCService.instance.channel);

    final RemoveRegionReply removeRegionReply =
        await stub.removeRegion(removeRegionRequest);

    return removeRegionReply;
  }
}
