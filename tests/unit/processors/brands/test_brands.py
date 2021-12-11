# from src.data_access_layer.brand import Brand
# from src.filters import FilterResponse, FilterInterface
#
# user_id = 'user_id'
# email = 'do@notupdate.email'
# event_cognito_user = {
#     'requestContext': {
#         'authorizer': {
#             'jwt': {
#                 'claims': {
#                     'cognito:username': user_id,
#                     'email': email
#                 }
#             }
#         }
#     },
#     'body': {
#         'image': 'image bytes',
#         'email': 'new@email.should.not.update.com'
#     }
# }
#
#
# def mock_no_brand_associated_with_authenticated_user(event):
#     return FilterResponse('', 200, {})
#
#
# def mock_brand_associated_with_authenticated_user(event):
#     return FilterResponse('', 400, {})
#
#
# def mock_get_brand_associated_with_authenticated_user(event):
#     return FilterResponse('', 200, Brand().as_dict())
#
#
# def mock_failed_to_get_associated_cognito_user(event):
#     return FilterResponse('', 404, {})
#
#
# def mock_valid_brand_payload(event):
#     return FilterResponse('', 200, event_cognito_user['body'])
#
#
# def mock_valid_update_brand_payload(event):
#     return FilterResponse('', 200, event_cognito_user['body'])
#
#
# def mock_invalid_update_brand_payload(event):
#     return FilterResponse('', 400, event_cognito_user['body'])
#
#
# def mock_invalid_brand_payload(event):
#     return FilterResponse('', 400, event_cognito_user['body'])
#
#
# def mock_create_new_brand_successful(payload, image_bytes):
#     return Brand()
#
#
# def mock_update_brand_successful(_id, payload):
#     assert payload['email'] == email
#     return Brand()
#
#
# def mock_failed_create_new_brand_successful(payload, image_bytes):
#     raise Exception()
#
#
# def mock_failed_update_brand(_id, payload):
#     raise Exception()
#
#
#
# def mock_unsuccessful_update_brand_image(brand_id, image_bytes, data_manager):
#     raise Exception('failed to write brand image')
