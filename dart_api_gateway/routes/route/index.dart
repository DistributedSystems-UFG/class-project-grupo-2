import 'package:dart_frog/dart_frog.dart';

import '../../generated/iot_service.pbgrpc.dart';
import '../../repositories/route_repository.dart';

Future<Response> onRequest(RequestContext context) async {
  try {
    final request = context.request;
    final body = await request.json();

    final String route = body['route'] as String? ?? '/home';
    final String args = body['args'] as String? ?? '';
    final String accessToken = body['accesstoken'] as String? ?? '';

    if (accessToken.isEmpty) {
      return Response.json(
        statusCode: 400,
        body: {'message': 'accessToken was not received'},
      );
    }

    switch (context.request.method) {
      case HttpMethod.post:
        final setRouteRequest =
            SetRouteRequest(accessToken: accessToken, args: args, route: route);
        final setRouteReply =
            await RouteRepository.setRoute(setRouteRequest: setRouteRequest);

        return Response.json(
          statusCode: 200,
          body: {
            'status': setRouteReply.status,
          },
        );
      case HttpMethod.get:
        final getLastRouteRequest =
            GetLastRouteRequest(accessToken: accessToken);
        final routeReply = await RouteRepository.getLastRoute(
          getLastRouteRequest: getLastRouteRequest,
        );
        return Response.json(
          statusCode: 200,
          body: {
            'route': routeReply.route,
            'args': routeReply.args,
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
