import 'package:dart_frog/dart_frog.dart';

import '../../generated/iot_service.pbgrpc.dart';
import '../../repositories/regions_repository.dart';
import '../../repositories/route_repository.dart';

Future<Response> onRequest(RequestContext context) async {
  try {
    final request = context.request;
    final body = await request.json();

    final region = body['region'] ?? '';
    final String accessToken = body['accesstoken'] as String? ?? '';

    if (accessToken.isEmpty || region.isEmpty) {
      return Response.json(
        statusCode: 400,
        body: {'message': 'accessToken or region was not received'},
      );
    }

    switch (context.request.method) {
      case HttpMethod.post:
        final addRegionRequest = AddRegionRequest(
          accessToken: accessToken,
          region: Region(
            icon: region['icon'],
            name: region['name'],
          ),
        );
        final addRegionReply = await RegionsRepository.addRegion(
            addRegionRequest: addRegionRequest);

        return Response.json(
          statusCode: 200,
          body: {
            'status': addRegionReply.status,
          },
        );
      case HttpMethod.get:
        final getRegionsRequest = GetRegionsRequest(accessToken: accessToken);
        final regionsReply = await RegionsRepository.getRegions(
          getRegionsRequest: getRegionsRequest,
        );
        return Response.json(
          statusCode: 200,
          body: {
            'status': regionsReply.status,
            'regions': regionsReply.regions,
          },
        );
      case HttpMethod.delete:
        final removeRegionRequest = RemoveRegionRequest(
          region: Region(icon: region['icon'], name: region['name']),
          accessToken: accessToken,
        );

        final removeRegionReply = await RegionsRepository.removeRegions(
            removeRegionRequest: removeRegionRequest);

        return Response.json(
          statusCode: 200,
          body: {
            'status': removeRegionReply.status,
          },
        );
      // ignore: no_default_cases
      default:
        return Response.json(
          statusCode: 400,
          body: {'message': 'wrong method'},
        );
    }
  } catch (e) {
    return Response.json(
      statusCode: 400,
      body: {'message': e.toString().replaceAll('\n', '').replaceAll('^', '')},
    );
  }
}
