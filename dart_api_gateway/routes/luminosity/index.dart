import 'package:dart_frog/dart_frog.dart';

import '../../generated/iot_service.pbgrpc.dart';
import '../../repositories/luminosity_repository.dart';

Future<Response> onRequest(RequestContext context) async {
  try {
    final request = context.request;
    final body = await request.json();

    final String sensorName = body['sensorname'] as String? ?? '';
    final String accessToken = body['accesstoken'] as String? ?? '';

    if (sensorName.isEmpty || accessToken.isEmpty) {
      return Response.json(
        statusCode: 400,
        body: "{'message': 'sensorName or accessToken was not received'}",
      );
    }

    switch (context.request.method) {
      case HttpMethod.get:
        final luminosityRequest =
            LuminosityRequest(sensorName: sensorName, accessToken: accessToken);
        final luminosityReply = await LuminosityRepository.sayLuminosity(
            luminosityRequest: luminosityRequest);
        return Response.json(
          body:
              "{ 'luminosity': ${luminosityReply.luminosity}, 'status': ${luminosityReply.status} }",
        );
      // ignore: no_default_cases
      default:
        return Response.json(
          statusCode: 400,
          body: "{'message': 'wrong method'}",
        );
    }
  } catch (e) {
    return Response.json(
      statusCode: 400,
      body:
          "{'message': ${e.toString().replaceAll('\n', '').replaceAll('^', '')}}",
    );
  }
}
