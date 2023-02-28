import 'dart:async';

import 'package:dart_frog/dart_frog.dart';

import '../../generated/iot_service.pbgrpc.dart';
import '../../repositories/auth_repository.dart';

Future<Response> onRequest(RequestContext context) async {
  try {
    final request = context.request;
    final body = await request.json();

    final String login = body['login'] as String? ?? '';
    final String password = body['password'] as String? ?? '';

    if (login.isEmpty || password.isEmpty) {
      return Response.json(
        statusCode: 400,
        body: "{'message': 'login or password was not received'}",
      );
    }

    switch (context.request.method) {
      case HttpMethod.post:
        final credentials = Credentials(login: login, password: password);
        final token =
            await AuthRepository.getAccessToken(credentials: credentials);
        return Response.json(
          body: "{ 'token': ${token.token}, 'status': ${token.status} }",
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
