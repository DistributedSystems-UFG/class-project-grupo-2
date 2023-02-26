import 'package:dart_frog/dart_frog.dart';

import '../../generated/iot_service.pbgrpc.dart';
import '../../repositories/temperature_repository.dart';

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
        final temperatureRequest = TemperatureRequest(
            sensorName: sensorName, accessToken: accessToken);
        final temperatureReply = await TemperatureRepository.sayTemperature(
            temperatureRequest: temperatureRequest);
        return Response.json(
          body:
              "{ 'temperature': ${temperatureReply.temperature}, 'status': ${temperatureReply.status} }",
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
