# POC auth
## Description
This is a POC for authentication using a simple implementation of OAuth2.0 and openID connect. This POC is simple and is not intended to be used in production.

Things like client id's and client secrets are out of scope for this POC. The POC is only intended to show how the authentication works.

The things that are implemented are:

- Implicit flow (so no refresh tokens)
- OpenID connect (so we can get user info which is stored in the id_token)
  


> See the research document for more info