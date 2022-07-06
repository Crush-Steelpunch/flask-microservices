# Bingo

User service provider, because bingo knows everybodies name-o

`GET / `
List all users
Returns JSON

`GET /search/<term>`
return list of matching users
Returns JSON

`POST /adduser`  DATA:`{ "fname":"<name>","lname":"<name>","login":"<login>" }`
Add users
Returns 200

`DELETE /deluser/<uid>` DATA:`{"yes-i-really-really-mean-it": "delete-this-user-i-will-be-responsible-for-the-consiquences"}`
Delete Users
Returns 200
