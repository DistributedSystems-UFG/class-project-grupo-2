import 'package:dart_frog/dart_frog.dart';

import '../../generated/iot_service.pbgrpc.dart';
import '../../repositories/led_repository.dart';

Future<Response> onRequest(RequestContext context) async {
  try {
    final request = context.request;
    final body = await request.json();

    final int? state = int.tryParse(body['state']);
    final String sensorName = body['sensorname'] as String? ?? '';
    final String accessToken = body['accesstoken'] as String? ?? '';

    if (sensorName.isEmpty || accessToken.isEmpty || state == null) {
      return Response.json(
        statusCode: 400,
        body: {
          'message': 'sensorName or accessToken or state was not received'
        },
      );
    }

    switch (context.request.method) {
      case HttpMethod.put:
        final ledRequest = LedRequest(
            state: state, sensorName: sensorName, accessToken: accessToken);
        final ledReply = await LedRepository.blinkLed(ledRequest: ledRequest);
        return Response.json(
          body: {
            'ledstate': ledReply.ledstate.entries,
            'status': ledReply.status
          },
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
      body: {'message': e.toString().replaceAll('\n', '').replaceAll('^', '')},
    );
  }
}
